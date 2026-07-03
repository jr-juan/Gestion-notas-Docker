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
- pgAdmin: http://localhost:5050 (usuario: juanromancuero@gmail.com / clave: admin123)
- PostgreSQL: localhost:5432 (usuario: admin / clave: admin123 / bd: gestion_notas)


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

## Bitacora de reflexion (entregable obligatorio - 30% de la nota)

>Proximamente

### Error 1
- **Descripcion del error:**
- **Como lo detectamos:**
- **Solucion aplicada:**

### Error 2
- **Descripcion del error:**
- **Como lo detectamos:**
- **Solucion aplicada:**

### Autoevaluacion (metacognicion)
- **Que concepto de Docker me costo mas comprender?**
- **Que estrategia use para aprenderlo?**

### Coevaluacion entre companeros
- **Comentario tecnico sobre el trabajo de mis companeros:**
