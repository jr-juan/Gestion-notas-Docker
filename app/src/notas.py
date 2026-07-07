from src.db import get_connection


def listar_notas_estudiante(usuario_id):
    conn = get_connection()
    cur = conn.cursor()

    # Detalle: todas las notas, una fila por evaluacion
    cur.execute(
        """
        SELECT m.nombre, n.periodo, n.tipo_nota, n.porcentaje, n.nota
        FROM notas n
        JOIN estudiantes e ON e.id = n.estudiante_id
        JOIN materias m ON m.id = n.materia_id
        WHERE e.usuario_id = %s
        ORDER BY m.nombre, n.tipo_nota
        """,
        (usuario_id,),
    )
    filas = cur.fetchall()
    notas = [
        {"materia": f[0], "periodo": f[1], "tipo_nota": f[2], "porcentaje": float(f[3]), "nota": float(f[4])}
        for f in filas
    ]

    # Resumen: una sola fila por materia, con su definitiva ya calculada
    cur.execute(
        """
        SELECT
            m.nombre,
            n.periodo,
            ROUND(SUM(n.porcentaje / 100.0 * n.nota), 2) AS definitiva,
            SUM(n.porcentaje) AS porcentaje_acumulado
        FROM notas n
        JOIN estudiantes e ON e.id = n.estudiante_id
        JOIN materias m ON m.id = n.materia_id
        WHERE e.usuario_id = %s
        GROUP BY m.nombre, n.periodo
        ORDER BY m.nombre
        """,
        (usuario_id,),
    )
    filas_def = cur.fetchall()
    definitivas = [
        {
            "materia": f[0],
            "periodo": f[1],
            "definitiva": float(f[2]),
            "completa": float(f[3]) >= 100,
        }
        for f in filas_def
    ]

    cur.close()
    conn.close()
    return {"notas": notas, "definitivas": definitivas}


def listar_materias_profesor(usuario_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT m.id, m.nombre
        FROM materias m
        JOIN profesores p ON p.id = m.profesor_id
        WHERE p.usuario_id = %s
        ORDER BY m.nombre
        """,
        (usuario_id,),
    )
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": f[0], "nombre": f[1]} for f in filas]


def listar_estudiantes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, codigo FROM estudiantes ORDER BY nombre")
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": f[0], "nombre": f[1], "codigo": f[2]} for f in filas]


def listar_notas_profesor(usuario_id, materia_id=None):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT n.id, e.nombre, m.nombre, n.periodo, n.tipo_nota, n.porcentaje, n.nota
        FROM notas n
        JOIN estudiantes e ON e.id = n.estudiante_id
        JOIN materias m ON m.id = n.materia_id
        JOIN profesores p ON p.id = m.profesor_id
        WHERE p.usuario_id = %s
    """
    params = [usuario_id]
    if materia_id:
        query += " AND n.materia_id = %s"
        params.append(materia_id)
    query += " ORDER BY e.nombre, n.tipo_nota"

    cur.execute(query, params)
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": f[0], "estudiante": f[1], "materia": f[2], "periodo": f[3],
            "tipo_nota": f[4], "porcentaje": float(f[5]), "nota": float(f[6]),
        }
        for f in filas
    ]


def crear_nota(datos):
    acumulado = obtener_porcentaje_acumulado(
        datos["estudiante_id"], datos["materia_id"], datos["periodo"]
    )
    nuevo_total = acumulado + float(datos["porcentaje"])

    if nuevo_total > 100:
        raise ValueError(
            f"No se puede registrar: el porcentaje acumulado quedaria en {nuevo_total}% "
            f"(ya hay {acumulado}% registrado para esta materia y periodo). "
            f"Maximo disponible: {100 - acumulado}%."
        )

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO notas (estudiante_id, materia_id, periodo, tipo_nota, porcentaje, nota)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                datos["estudiante_id"], datos["materia_id"], datos["periodo"],
                datos["tipo_nota"], datos["porcentaje"], datos["nota"],
            ),
        )
        nueva_id = cur.fetchone()[0]
        conn.commit()
        return {"status": "ok", "id": nueva_id}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def actualizar_nota(nota_id, datos):
    conn = get_connection()
    cur = conn.cursor()

    
    cur.execute("SELECT estudiante_id, materia_id FROM notas WHERE id = %s", (nota_id,))
    fila = cur.fetchone()
    if not fila:
        cur.close()
        conn.close()
        raise ValueError("La nota que intentas editar no existe.")

    estudiante_id, materia_id = fila
    acumulado = obtener_porcentaje_acumulado(
        estudiante_id, materia_id, datos["periodo"], excluir_nota_id=nota_id
    )
    nuevo_total = acumulado + float(datos["porcentaje"])

    if nuevo_total > 100:
        cur.close()
        conn.close()
        raise ValueError(
            f"No se puede actualizar: el porcentaje acumulado quedaria en {nuevo_total}% "
            f"(ya hay {acumulado}% en las demas notas de esta materia y periodo). "
            f"Maximo disponible: {100 - acumulado}%."
        )

    try:
        cur.execute(
            """
            UPDATE notas
            SET nota = %s, porcentaje = %s, tipo_nota = %s, periodo = %s
            WHERE id = %s
            """,
            (datos["nota"], datos["porcentaje"], datos["tipo_nota"], datos["periodo"], nota_id),
        )
        conn.commit()
        return {"status": "ok"}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def eliminar_nota(nota_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notas WHERE id = %s", (nota_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "eliminado"}

def obtener_porcentaje_acumulado(estudiante_id, materia_id, periodo, excluir_nota_id=None):
    """Suma los porcentajes ya registrados para ese estudiante+materia+periodo.
    Si excluir_nota_id se pasa, no cuenta esa nota (util al editar)."""
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT COALESCE(SUM(porcentaje), 0)
        FROM notas
        WHERE estudiante_id = %s AND materia_id = %s AND periodo = %s
    """
    params = [estudiante_id, materia_id, periodo]
    if excluir_nota_id:
        query += " AND id != %s"
        params.append(excluir_nota_id)

    cur.execute(query, params)
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return float(total)