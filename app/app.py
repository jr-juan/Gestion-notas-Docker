import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__, template_folder="vistas")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "gestion_notas"),
    "user": os.getenv("DB_USER", "admin"),
    "password": os.getenv("DB_PASSWORD", "admin123"),
}


def get_connection():
    """Devuelve una conexion nueva a PostgreSQL.
    Usala en las funciones CRUD (companero 3) asi:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT ...")
    """
    return psycopg2.connect(**DB_CONFIG)


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login")
def login():
    # TODO (companero 4): formulario y validacion de usuario/contrasena
    return render_template("login.html")


@app.route("/estudiante")
def vista_estudiante():
    # TODO (companero 4): vista de notas del estudiante logueado
    return render_template("estudiante.html")


@app.route("/profesor")
def vista_profesor():
    # TODO (companero 4): vista para que el profesor gestione notas
    return render_template("profesor.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
