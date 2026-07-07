# Gestion de Notas de Estudiantes - Docker
## Descripcion

Sistema web para la gestion de notas de estudiantes. Permite a un profesor
registrar notas por materia y periodo, y a un estudiante
consultar las suyas.

## Situación problémica

La Universidad necesita un sistema de gestión de notas que funcione de manera
idéntica en cualquier computador, sin importar el sistema
operativo o las dependencias instaladas previamente. Este proyecto resuelve
ese problema empaquetando la aplicación web (Flask), la base de datos
(PostgreSQL) y su administrador (pgAdmin) en contenedores Docker
independientes, orquestados con Docker Compose, garantizando portabilidad
y consistencia entre entornos de desarrollo.

## Integrantes y roles

| Integrante | Rol |
|---|---|
| Juan Roman Cuero Ordonez | Configuracion Docker, levantar la base, frontend base (HTML/CSS/JS) |
| Jhon Jader Riascos Angulo | Inserts / poblado de datos |
| Dario Restrepo Landazury | Conexion a la base y metodos CRUD |
| Esteban David Ruiz | Vistas: login, estudiante, profesor |



## Stack

- Python 3.13 + Flask
- PostgreSQL 18
- pgAdmin 4
- Docker Compose

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
        └── js/
            └── main.js      
```

## Backend - Como funciona

- **db.py**: centraliza la conexion a PostgreSQL con `psycopg2`, leyendo host, puerto, usuario y password desde variables de entorno.
- **auth.py**: valida credenciales contra la tabla `usuarios` (solo activos) y expone el decorador `login_required(rol=...)` para proteger rutas por sesion y por rol.
- **notas.py**: logica de negocio de notas — consultas para estudiante (detalle + definitivas por materia) y profesor (materias, estudiantes, notas), mas el CRUD (`crear_nota`, `actualizar_nota`, `eliminar_nota`) con commit/rollback.
- **app.py**: arma las rutas Flask en tres grupos — autenticacion (`/login`, `/logout`), vistas por rol (`/estudiante/...`, `/profesor/...`) y API JSON (`/api/mis-notas`, `/api/materias`, `/api/estudiantes`, `/api/notas`) que consume `main.js` por fetch. No tiene logica propia, solo llama a `auth.py` y `notas.py`.

**Nota:** la definitiva de una materia solo se muestra cuando el porcentaje acumulado de notas llega al 100%; si no, se marca como "en proceso".


## Frontend - Como funciona

Interfaz basada en una plantilla comun (`index.html`) que cambia segun haya
o no sesion iniciada. Cada rol tiene su propio menu de navegacion y sus
vistas (estudiante: consultar notas y definitivas; profesor: registrar,
editar y eliminar notas). Todo el diseño vive en un unico CSS, y un solo
archivo JS (`main.js`) detecta la vista actual y consume la API del backend
via `fetch` para mostrar y actualizar la informacion sin recargar la pagina.

## Como levantar el proyecto

```bash
docker compose up --build
```

- App web: http://localhost:5000
- pgAdmin: http://localhost:5050
- PostgreSQL: localhost:5432

**Credenciales:** ver el archivo `.env.example`.
Antes de correr el proyecto, copia ese archivo a `.env` y ajusta los valores si lo necesitas:

```bash
cp .env.example .env
```

Para apagar los contenedores:

```bash
docker compose down
```

(los datos quedan guardados en la carpeta local `pgdata/`, no se pierden)

Para apagar y borrar tambien los datos (empezar de cero):

```bash
docker compose down
```
y luego borra manualmente el contenido de la carpeta `pgdata/`.


## Modelo relacional

- **usuarios**: credenciales de acceso (username, password, rol: estudiante/profesor), estado activo
- **profesores**: documento, nombre, correo, teléfono, especialidad — ligado a usuarios
- **estudiantes**: código, nombre, correo, teléfono, programa académico — ligado a usuarios
- **materias**: código de materia, nombre, créditos, profesor a cargo
- **notas**: nota (0 a 100) de un estudiante en una materia, por periodo y tipo
  de evaluación (Parcial 1, Parcial 2, Seguimiento, Examen Final), con su
  porcentaje correspondiente

## Cómo probar la portabilidad (evidencia para la rúbrica)

Para confirmar que el proyecto corre igual en cualquier equipo:

```bash
git clone https://github.com/jr-juan/Gestion-notas-Docker.git
cd Gestion-notas-Docker
docker compose up --build
```

En el otro equipo levantar sin modificar nada y accedera a
`http://localhost:5000` y `http://localhost:5050` sin errores, quedara
demostrada la portabilidad.

## Bitacora de reflexion 

### Error 1
- **Descripcion del error:** Al ejecutar `docker compose up --build`, la terminal respondio `no configuration file provided: not found`.
- **Como lo detectamos:** El comando se corrio desde `C:\Users\hp` en vez de la carpeta del proyecto, por lo que Docker no encontraba el `docker-compose.yml`.
- **Solucion aplicada:** Nos movimos con `cd` hasta la carpeta que contiene el `docker-compose.yml` y confirmamos con `dir docker-compose.yml` antes de volver a correr el comando.

### Error 2
- **Descripcion del error:** Al construir la imagen de la app, `pip install` fallaba con `Error: pg_config executable not found` al intentar instalar `psycopg2-binary`.
- **Como lo detectamos:** El log de `docker compose up --build` mostraba que pip intentaba compilar `psycopg2-binary` desde codigo fuente en vez de descargar un paquete precompilado.
- **Solucion aplicada:** Investigamos y encontramos que la version fijada (`2.9.9`) no tenia wheel precompilado para Python 3.13. Actualizamos `requirements.txt` a `psycopg2-binary==2.9.10`, version que si incluye wheel para esa version de Python, y el build paso sin errores.

### Autoevaluacion (metacognicion)
- **Que concepto de Docker me costo mas comprender?** Los volumenes.
  No tenia claro que el volumen es lo que hace que los datos de la base
  de datos no se pierdan cuando se apaga o se borra el contenedor. Se
  me complico en el archivo `docker-compose.yml`, en la parte donde se
  monta el volumen del servicio `db` (`./pgdata:/var/lib/postgresql`):
  al principio lo tenia mal escrito como `/var/lib/postgresql/data` y
  el contenedor `notas_db` no arrancaba, quedaba en estado "unhealthy".
- **Que estrategia use para aprenderlo?** Lei el mensaje de error completo
  que mostraba la terminal (no solo la primera linea) y busque en la
  documentacion oficial de la imagen de Postgres en Docker Hub. Ahi
  entendi que desde la version 18 de Postgres, el volumen se debe montar
  en `/var/lib/postgresql` y no en `/var/lib/postgresql/data` como antes.
  Cambiando esa linea en el `docker-compose.yml`, el contenedor arranco bien.

### Coevaluacion entre companeros
- **Comentario tecnico sobre el trabajo de mis companeros:** El script de
  Jhon Jader (poblado de datos) esta muy bien resuelto: uso
  `setval(pg_get_serial_sequence(...))` despues de insertar usuarios con ID
  manual, lo que evita errores de llave duplicada mas adelante, y genero las
  800 notas con `INSERT ... SELECT ... FROM estudiantes` usando `random()`
  en vez de escribirlas una por una. 
