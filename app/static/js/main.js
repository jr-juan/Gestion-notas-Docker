document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("cuerpo-tabla-notas")) {
        cargarMisNotas();
    }
    if (document.getElementById("form-registrar")) {
        inicializarRegistrar();
    }
    if (document.getElementById("cuerpo-tabla-notas-profesor")) {
        inicializarGestionar();
    }
});

// ============================================
// ESTUDIANTE
// ============================================
async function cargarMisNotas() {
    const cuerpoNotas = document.getElementById("cuerpo-tabla-notas");
    const cuerpoDefinitivas = document.getElementById("cuerpo-tabla-definitivas");

    try {
        const resp = await fetch("/api/mis-notas");
        if (!resp.ok) {
            cuerpoNotas.innerHTML = `<tr><td colspan="5">No se pudieron cargar las notas.</td></tr>`;
            return;
        }
        const data = await resp.json();

        // Tabla de detalle
        if (data.notas.length === 0) {
            cuerpoNotas.innerHTML = `<tr><td colspan="5">Aun no tienes notas registradas.</td></tr>`;
        } else {
            cuerpoNotas.innerHTML = data.notas.map(n => `
                <tr>
                    <td>${n.materia}</td>
                    <td>${n.periodo}</td>
                    <td>${n.tipo_nota}</td>
                    <td>${n.porcentaje}%</td>
                    <td>${n.nota}</td>
                </tr>
            `).join("");
        }

        // Tabla de definitivas por materia
        if (data.definitivas.length === 0) {
            cuerpoDefinitivas.innerHTML = `<tr><td colspan="3">Sin definitivas todavia.</td></tr>`;
        } else {
            cuerpoDefinitivas.innerHTML = data.definitivas.map(d => `
                <tr>
                    <td>${d.materia}</td>
                    <td>${d.periodo}</td>
                    <td>${d.completa ? `<strong>${d.definitiva}</strong>` : "En proceso"}</td>
                </tr>
            `).join("");
        }
    } catch (e) {
        cuerpoNotas.innerHTML = `<tr><td colspan="5">Error de conexion con el servidor.</td></tr>`;
    }
}

// ============================================
// PROFESOR - Registrar
// ============================================
async function inicializarRegistrar() {
    await cargarEstudiantes();
    await cargarMaterias();
    document.getElementById("form-registrar").addEventListener("submit", crearNota);
}

async function cargarEstudiantes() {
    const select = document.getElementById("estudiante");
    const resp = await fetch("/api/estudiantes");
    const estudiantes = await resp.json();
    select.innerHTML = estudiantes
        .map(e => `<option value="${e.id}">${e.nombre} (${e.codigo})</option>`)
        .join("");
}

async function cargarMaterias() {
    const select = document.getElementById("materia");
    const resp = await fetch("/api/materias");
    const materias = await resp.json();
    select.innerHTML = materias
        .map(m => `<option value="${m.id}">${m.nombre}</option>`)
        .join("");
}

async function crearNota(evento) {
    evento.preventDefault();
    const mensaje = document.getElementById("mensaje");

    const datos = {
        estudiante_id: document.getElementById("estudiante").value,
        materia_id: document.getElementById("materia").value,
        periodo: document.getElementById("periodo").value,
        tipo_nota: document.getElementById("tipo_nota").value,
        porcentaje: parseFloat(document.getElementById("porcentaje").value),
        nota: parseFloat(document.getElementById("nota").value),
    };

    const resp = await fetch("/api/notas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
    });

    if (resp.ok) {
        mensaje.textContent = "Nota registrada correctamente.";
        mensaje.className = "exito";
        document.getElementById("form-registrar").reset();
    } else {
        const error = await resp.json();
        mensaje.textContent = "Error: " + (error.detalle || "no se pudo guardar la nota.");
        mensaje.className = "error";
    }
}

// ============================================
// PROFESOR - Gestionar (editar / eliminar)
// ============================================
async function inicializarGestionar() {
    await cargarNotasGestion();
    document.getElementById("form-editar-nota").addEventListener("submit", actualizarNota);
    document.getElementById("btn-cancelar").addEventListener("click", cancelarEdicion);
}

async function cargarNotasGestion() {
    const cuerpo = document.getElementById("cuerpo-tabla-notas-profesor");
    const resp = await fetch("/api/notas");
    const notas = await resp.json();

    if (notas.length === 0) {
        cuerpo.innerHTML = `<tr><td colspan="7">No hay notas registradas todavia.</td></tr>`;
        return;
    }

    cuerpo.innerHTML = notas.map(n => `
        <tr>
            <td>${n.estudiante}</td>
            <td>${n.materia}</td>
            <td>${n.periodo}</td>
            <td>${n.tipo_nota}</td>
            <td>${n.porcentaje}%</td>
            <td>${n.nota}</td>
            <td>
                <button onclick="editarNota(${n.id}, '${n.periodo}', '${n.tipo_nota}', ${n.porcentaje}, ${n.nota})">Editar</button>
                <button onclick="eliminarNota(${n.id})">Eliminar</button>
            </td>
        </tr>
    `).join("");
}

function editarNota(id, periodo, tipoNota, porcentaje, nota) {
    document.getElementById("form-editar-nota").style.display = "flex";
    document.getElementById("nota_id").value = id;
    document.getElementById("periodo").value = periodo;
    document.getElementById("tipo_nota").value = tipoNota;
    document.getElementById("porcentaje").value = porcentaje;
    document.getElementById("nota").value = nota;
}

function cancelarEdicion() {
    document.getElementById("form-editar-nota").style.display = "none";
    document.getElementById("form-editar-nota").reset();
}

async function actualizarNota(evento) {
    evento.preventDefault();
    const mensaje = document.getElementById("mensaje");
    const notaId = document.getElementById("nota_id").value;

    const datos = {
        periodo: document.getElementById("periodo").value,
        tipo_nota: document.getElementById("tipo_nota").value,
        porcentaje: parseFloat(document.getElementById("porcentaje").value),
        nota: parseFloat(document.getElementById("nota").value),
    };

    const resp = await fetch(`/api/notas/${notaId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
    });

    if (resp.ok) {
        mensaje.textContent = "Nota actualizada.";
        mensaje.className = "exito";
        cancelarEdicion();
        cargarNotasGestion();
    } else {
        const error = await resp.json();
        mensaje.textContent = "Error: " + (error.detalle || "no se pudo actualizar.");
        mensaje.className = "error";
    }
}

async function eliminarNota(id) {
    if (!confirm("Seguro que quieres eliminar esta nota?")) return;
    const resp = await fetch(`/api/notas/${id}`, { method: "DELETE" });
    if (resp.ok) {
        cargarNotasGestion();
    } else {
        alert("No se pudo eliminar la nota.");
    }
}