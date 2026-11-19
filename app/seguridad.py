from functools import wraps

from flask import flash, redirect, request, session, url_for


def login_requerido(funcion):
    """
    Decorador para proteger las rutas de edición (se usará en la Fase 5).

    Si no hay sesión, redirige al login y guarda la URL pedida en 'next'
    para que el usuario vuelva ahí después de identificarse.
    """

    @wraps(funcion)
    def envoltorio(*args, **kwargs):
        if not session.get("usuario_id"):
            flash("Iniciá sesión para acceder a esa sección.", "aviso")
            return redirect(url_for("auth.login", next=request.path))
        return funcion(*args, **kwargs)

    return envoltorio
