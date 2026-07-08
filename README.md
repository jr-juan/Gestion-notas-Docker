# Gestion de Notas de Estudiantes

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker%20Compose-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/uso-academico-lightgrey?style=for-the-badge)

Sistema web contenerizado para la gestion de notas universitarias. Los
profesores registran, editan y eliminan calificaciones por materia y
periodo; los estudiantes consultan sus notas y definitivas en tiempo real.

---

## Tabla de contenido

- [Situacion problemica](#situacion-problemica)
- [Integrantes y roles](#integrantes-y-roles)
- [Stack tecnologico](#stack-tecnologico)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Backend: como funciona](#backend-como-funciona)
- [Frontend: como funciona](#frontend-como-funciona)
- [Guia de inicio](#guia-de-inicio)
- [Modelo relacional](#modelo-relacional)
- [Prueba de portabilidad](#prueba-de-portabilidad)
- [Flujo de contribucion](#flujo-de-contribucion)
- [Bitacora de reflexion](#bitacora-de-reflexion)

---

## Situacion problemica

La Universidad necesita un sistema de gestion de notas que funcione de
manera identica en cualquier computador, sin importar el sistema operativo
o las dependencias instaladas previamente. Este proyecto resuelve ese
problema empaquetando la aplicacion web (Flask), la base de datos
(PostgreSQL) y su administrador (pgAdmin) en contenedores Docker
independientes, orquestados con Docker Compose, garantizando **portabilidad**
y **consistencia** entre entornos de desarrollo.

---

## Integrantes y roles

| Integrante | Rol |
|---|---|
| Juan Roman Cuero Ordonez | Configuracion Docker, base de datos, backend (Flask + API + CRUD) |
| Jhon Jader Riascos Angulo | Inserts y poblado de datos |
| Dario Restrepo Landazury | Apoyo en pruebas de conexion a la base |
| Esteban David Ruiz | Diseno y estilos de las vistas: login, estudiante, profesor |

---

## Stack tecnologico

| Componente | Tecnologia |
|---|---|
| Backend | Python 3.13 + Flask |
| Base de datos | PostgreSQL 18 |
| Administrador de BD | pgAdmin 4 |
| Orquestacion | Docker Compose |

---

## Estructura del proyecto

```
gestion-notas/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── pgdata/
└── app/
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py
    ├── src/
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── db.py
    │   └── notas.py
    ├── vistas/
    │   ├── index.html
    │   ├── login.html
    │   ├── estudiante/
    │   │   ├── menu.html
    │   │   └── mis_notas.html
    │   └── profesor/
    │       ├── menu.html
    │       ├── registrar.html
    │       └── gestionar.html
    └── static/
        ├── css/
        │   └── style.css
        └── js/
            └── main.js
```

---

## Backend: como funciona

| Archivo | Responsabilidad |
|---|---|
| `db.py` | Centraliza la conexion a PostgreSQL con `psycopg2`, leyendo host, puerto, usuario y password desde variables de entorno. |
| `auth.py` | Valida credenciales contra la tabla `usuarios` (solo activos) y expone el decorador `login_required(rol=...)` para proteger rutas por sesion y por rol. |
| `notas.py` | Logica de negocio: consultas para estudiante (detalle y definitivas por materia) y profesor (materias, estudiantes, notas), mas el CRUD (`crear_nota`, `actualizar_nota`, `eliminar_nota`) con validacion de porcentajes y control de transacciones (commit/rollback). |
| `app.py` | Define las rutas Flask en tres grupos: autenticacion (`/login`, `/logout`), vistas por rol (`/estudiante/...`, `/profesor/...`) y API JSON consumida por `main.js`. No contiene logica propia; delega en `auth.py` y `notas.py`. |

> **Nota:** la nota definitiva de una materia solo se muestra cuando el
> porcentaje acumulado de evaluaciones llega al 100%; de lo contrario se
> marca como "en proceso". Ademas, el backend **rechaza** registrar o editar
> una nota si el porcentaje acumulado de esa materia superaria el 100%.

---

## Frontend: como funciona

La interfaz se apoya en una plantilla comun (`index.html`) que cambia segun
haya o no una sesion iniciada. Cada rol cuenta con su propio menu de
navegacion y vistas dedicadas: el estudiante consulta sus notas y
definitivas; el profesor registra, edita y elimina calificaciones. Todo el
diseno vive en una sola hoja de estilos, y un unico archivo JavaScript
(`main.js`) detecta la vista activa y consume la API del backend mediante
`fetch`, actualizando la informacion sin recargar la pagina.

---

## Guia de inicio

```bash
git clone https://github.com/jr-juan/Gestion-notas-Docker.git
cd Gestion-notas-Docker
cp .env.example .env
docker compose up --build
```

| Servicio | URL |
|---|---|
| Aplicacion web | http://localhost:5000 |
| pgAdmin | http://localhost:5050 |
| PostgreSQL | localhost:5432 |

Para apagar los contenedores (los datos se conservan en `pgdata/`):

```bash
docker compose down
```

Para reiniciar desde cero, ademas borra manualmente el contenido de `pgdata/`.

---

## Modelo relacional

| Tabla | Descripcion |
|---|---|
| `usuarios` | Credenciales de acceso (username, password, rol: estudiante/profesor) y estado activo. |
| `profesores` | Documento, nombre, correo, telefono y especialidad, ligado a `usuarios`. |
| `estudiantes` | Codigo, nombre, correo, telefono y programa academico, ligado a `usuarios`. |
| `materias` | Codigo de materia, nombre, creditos y profesor a cargo. |
| `notas` | Nota (0 a 100) de un estudiante en una materia, por periodo y tipo de evaluacion (Parcial 1, Parcial 2, Seguimiento, Examen Final), con su porcentaje correspondiente. |

---

## Prueba de portabilidad

Si el equipo de un companero clona el repositorio y ejecuta
`docker compose up --build` sin modificar nada, y accede correctamente a
`http://localhost:5000` y `http://localhost:5050`, queda demostrada la
**portabilidad** del proyecto entre distintos entornos.

---

## Flujo de contribucion

1. Ejecutar `git pull` antes de iniciar cualquier cambio.
2. Trabajar unicamente sobre la carpeta o archivo correspondiente al rol asignado.
3. Probar localmente con `docker compose up --build` antes de subir cambios.
4. Confirmar los cambios: `git add .` seguido de `git commit -m "mensaje descriptivo"` y `git push`.
5. Avisar al equipo si el cambio afecta rutas de la API o el modelo de datos.

---

## Bitacora de reflexion

### Error 1

**Descripcion del error:** al ejecutar `docker compose up --build`, la
terminal respondio `no configuration file provided: not found`.

**Como lo detectamos:** el comando se ejecuto desde `C:\Users\hp` en vez de
la carpeta del proyecto, por lo que Docker no encontraba el
`docker-compose.yml`.

**Solucion aplicada:** nos movimos con `cd` hasta la carpeta que contiene el
`docker-compose.yml` y confirmamos con `dir docker-compose.yml` antes de
volver a ejecutar el comando.

### Error 2

**Descripcion del error:** al construir la imagen de la aplicacion,
`pip install` fallaba con `Error: pg_config executable not found` al
intentar instalar `psycopg2-binary`.

**Como lo detectamos:** el log de `docker compose up --build` mostraba que
pip intentaba compilar `psycopg2-binary` desde codigo fuente en vez de
descargar un paquete precompilado.

**Solucion aplicada:** investigamos y encontramos que la version fijada
(`2.9.9`) no tenia wheel precompilado para Python 3.13. Actualizamos
`requirements.txt` a `psycopg2-binary==2.9.10`, version que si incluye
wheel para esa version de Python, y el build paso sin errores.

### Autoevaluacion (metacognicion)

**Que concepto de Docker me costo mas comprender?** Los volumenes. No tenia
claro que el volumen es lo que hace que los datos de la base de datos no se
pierdan cuando se apaga o se borra el contenedor. Se me complico en el
archivo `docker-compose.yml`, en la parte donde se monta el volumen del
servicio `db` (`./pgdata:/var/lib/postgresql`): al principio lo tenia mal
escrito como `/var/lib/postgresql/data` y el contenedor `notas_db` no
arrancaba, quedaba en estado "unhealthy".

**Que estrategia use para aprenderlo?** Lei el mensaje de error completo que
mostraba la terminal (no solo la primera linea) y busque en la
documentacion oficial de la imagen de Postgres en Docker Hub. Ahi entendi
que desde la version 18 de Postgres, el volumen se debe montar en
`/var/lib/postgresql` y no en `/var/lib/postgresql/data` como antes.
Cambiando esa linea en el `docker-compose.yml`, el contenedor arranco bien.

### Coevaluacion entre compañeros

**Comentario tecnico sobre el trabajo de mis compañeros:** el script de
Jhon Jader (poblado de datos) esta muy bien resuelto: uso
`setval(pg_get_serial_sequence(...))` despues de insertar usuarios con ID
manual, lo que evita errores de llave duplicada mas adelante, y genero las
800 notas con `INSERT ... SELECT ... FROM estudiantes` usando `random()` en
vez de escribirlas una por una.
Coevaluación entre compañeros

**Comentario técnico sobre el trabajo del compañero encargado de Docker:** El trabajo de Juan Román en la configuración de Docker fue fundamental para el proyecto. Organizó correctamente los servicios de la aplicación, PostgreSQL y pgAdmin mediante Docker Compose, configuró las redes, volúmenes y variables de entorno para que todos los integrantes pudiéramos ejecutar el sistema con el mismo comando y sin diferencias entre equipos. Gracias a esa configuración, la integración del frontend, el backend y la base de datos se realizó de forma estable y facilitó las pruebas y el desarrollo colaborativo.

**Comentario técnico sobre el trabajo de Darío (Desarrollo del Backend y API):**
El trabajo de Darío con la lógica del backend y la API facilitó mucho la integración de todo el proyecto. Organizó muy bien el control de acceso usando sesiones y un decorador personalizado (`login_required`) para separar de forma segura lo que puede ver un estudiante de lo que hace el profesor. En `notas.py`, implementó las consultas de SQL de manera limpia, manejando transacciones con commit y rollback para evitar fallas en la base de datos, y haciendo que la nota definitiva se calcule directamente desde la consulta SQL. Además, conectó todo con el JavaScript del frontend usando fetch para que las acciones de crear, editar y borrar notas funcionen al instante sin tener que recargar la página.