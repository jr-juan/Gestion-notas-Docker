# Gestion de Notas de Estudiantes - Docker
## Descripcion

Sistema web para la gestion de notas de estudiantes. Permite a un profesor
registrar notas por materia y periodo, y a un estudiante
consultar las suyas.

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
    ├── vistas/
    │   ├── index.html
    │   ├── login.html
    │   ├── estudiante.html
    │   └── profesor.html
    └── static/
        ├── css/
        └── js/
```

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

- **usuarios**: credenciales y rol (estudiante/profesor)
- **profesores**: datos del profesor, ligado a usuarios
- **estudiantes**: datos del estudiante, ligado a usuarios
- **materias**: materia y profesor a cargo
- **notas**: nota (1 a 100) de un estudiante en una materia y periodo

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
- **Que concepto de Docker me costo mas comprender?**
- **Que estrategia use para aprenderlo?**

### Coevaluacion entre companeros
- **Comentario tecnico sobre el trabajo de mis companeros:**
