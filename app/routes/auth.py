from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from app.forms.login import LoginForm
from app.models import Usuario

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _url_segura(destino):
    """
    Acepta solo rutas internas (que empiezan con '/').
    Así un link externo no puede usar 'next' para redirigir al usuario
    a otro sitio después del login.
    """
    if destino and destino.startswith("/") and not destino.startswith("//"):
        return destino
    return url_for("publicas.inicio")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Muestra el formulario y valida usuario + contraseña."""
    if session.get("usuario_id"):
        return redirect(url_for("publicas.inicio"))

    formulario = LoginForm()

    if formulario.validate_on_submit():
        usuario = Usuario.query.filter_by(username=formulario.username.data).first()

        # check_password_hash compara con el hash guardado: en ningún momento
        # se guarda ni se compara la contraseña en texto plano.
        if usuario and check_password_hash(
            usuario.password_hash, formulario.password.data
        ):
            session.clear()
            session["usuario_id"] = usuario.id
            session.permanent = formulario.recordar.data
            flash(f"¡Bienvenido, {usuario.username}!", "exito")
            return redirect(_url_segura(request.args.get("next")))

        # Mensaje genérico a propósito: no revelamos si el usuario existe.
        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("auth/login.html", formulario=formulario)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Cierra la sesión. Es POST (no GET) para que el token CSRF también
    proteja este cambio de estado.
    """
    session.clear()
    flash("Cerraste sesión.", "aviso")
    return redirect(url_for("publicas.inicio"))
