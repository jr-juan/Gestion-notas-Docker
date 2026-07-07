import os

from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from src.auth import login_required, validar_credenciales
from src import notas as notas_service

app = Flask(__name__, template_folder="vistas", static_folder="static")
app.secret_key = os.getenv("SECRET_KEY", "cambiar-esta-clave-en-produccion")


# ---------------------------------------------------------
# Autenticacion
# ---------------------------------------------------------
@app.route("/")
def home():
    if "usuario_id" in session:
        destino = "menu_profesor" if session["rol"] == "profesor" else "menu_estudiante"
        return redirect(url_for(destino))
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        usuario = validar_credenciales(username, password)
        if usuario:
            session["usuario_id"] = usuario[0]
            session["rol"] = usuario[1]
            session["nombre"] = usuario[2]
            session["username"] = username
            destino = "menu_profesor" if usuario[1] == "profesor" else "menu_estudiante"
            return redirect(url_for(destino))
        error = "Usuario o contrasena incorrectos"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------
# Vistas del estudiante
# ---------------------------------------------------------
@app.route("/estudiante")
@login_required(rol="estudiante")
def menu_estudiante():
    return render_template("estudiante/menu.html")


@app.route("/estudiante/mis-notas")
@login_required(rol="estudiante")
def vista_mis_notas():
    return render_template("estudiante/mis_notas.html")


# ---------------------------------------------------------
# Vistas del profesor
# ---------------------------------------------------------
@app.route("/profesor")
@login_required(rol="profesor")
def menu_profesor():
    return render_template("profesor/menu.html")


@app.route("/profesor/registrar")
@login_required(rol="profesor")
def vista_registrar():
    return render_template("profesor/registrar.html")


@app.route("/profesor/gestionar")
@login_required(rol="profesor")
def vista_gestionar():
    return render_template("profesor/gestionar.html")


# ---------------------------------------------------------
# API - Estudiante
# ---------------------------------------------------------
@app.route("/api/mis-notas")
@login_required(rol="estudiante")
def api_mis_notas():
    return jsonify(notas_service.listar_notas_estudiante(session["usuario_id"]))


# ---------------------------------------------------------
# API - Profesor
# ---------------------------------------------------------
@app.route("/api/materias")
@login_required(rol="profesor")
def api_materias():
    return jsonify(notas_service.listar_materias_profesor(session["usuario_id"]))


@app.route("/api/estudiantes")
@login_required(rol="profesor")
def api_estudiantes():
    return jsonify(notas_service.listar_estudiantes())


@app.route("/api/notas", methods=["GET", "POST"])
@login_required(rol="profesor")
def api_notas():
    if request.method == "POST":
        datos = request.get_json()
        try:
            resultado = notas_service.crear_nota(datos)
            return jsonify(resultado), 201
        except Exception as e:
            return jsonify({"status": "error", "detalle": str(e)}), 400

    materia_id = request.args.get("materia_id")
    return jsonify(notas_service.listar_notas_profesor(session["usuario_id"], materia_id))


@app.route("/api/notas/<int:nota_id>", methods=["PUT", "DELETE"])
@login_required(rol="profesor")
def api_nota_detalle(nota_id):
    if request.method == "PUT":
        datos = request.get_json()
        try:
            resultado = notas_service.actualizar_nota(nota_id, datos)
            return jsonify(resultado)
        except Exception as e:
            return jsonify({"status": "error", "detalle": str(e)}), 400

    return jsonify(notas_service.eliminar_nota(nota_id))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)