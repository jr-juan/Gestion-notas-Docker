from functools import wraps

from flask import session, redirect, url_for, jsonify

from src.db import get_connection


def validar_credenciales(username, password):
    """Devuelve (id, rol) si el usuario existe y esta activo, o None si no."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, rol FROM usuarios WHERE username = %s AND password = %s AND activo = TRUE",
        (username, password),
    )
    usuario = cur.fetchone()
    cur.close()
    conn.close()
    return usuario


def login_required(rol=None):
    """Decorador: exige sesion iniciada, y opcionalmente un rol especifico."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "usuario_id" not in session:
                return redirect(url_for("login"))
            if rol and session.get("rol") != rol:
                return jsonify({"error": "No autorizado para este rol"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator