import os

from flask import Blueprint, abort, current_app, render_template, send_from_directory, session

from app.forms import crear_modales
from app.models import (
    Educacion,
    Experiencia,
    Idioma,
    Perfil,
    Proyecto,
    RedSocial,
    Skill,
)

# Un "blueprint" agrupa rutas relacionadas. Todas las de este archivo
# son públicas: no requieren iniciar sesión.
publicas_bp = Blueprint("publicas", __name__)


def _listar_por_orden(modelo, perfil_id):
    """
    Devuelve los ítems de un perfil ordenados por la columna 'orden'.
    Se usa para las seis secciones y evita repetir la misma consulta.
    """
    return (
        modelo.query.filter_by(perfil_id=perfil_id)
        .order_by(modelo.orden)
        .all()
    )


def datos_index():
    """
    Arma los datos de la página principal.

    Esta función se llama desde la ruta pública y también desde el modo
    edición cuando un formulario tiene errores: así no repetimos las
    mismas consultas en dos archivos.
    """
    perfil = Perfil.query.first()

    # Si la base está vacía, la plantilla muestra un mensaje en vez de fallar.
    if perfil is None:
        return {
            "perfil": None,
            "demo_url": current_app.config.get("DEMO_URL", ""),
            "modales": [],
        }

    skills = _listar_por_orden(Skill, perfil.id)

    return {
        "perfil": perfil,
        "redes": _listar_por_orden(RedSocial, perfil.id),
        "experiencias": _listar_por_orden(Experiencia, perfil.id),
        "educaciones": _listar_por_orden(Educacion, perfil.id),
        # Se separan acá para no hacer lógica en la plantilla.
        "skills_hard": [s for s in skills if s.tipo == "hard"],
        "skills_soft": [s for s in skills if s.tipo == "soft"],
        "idiomas": _listar_por_orden(Idioma, perfil.id),
        "proyectos": _listar_por_orden(Proyecto, perfil.id),
        "demo_url": current_app.config.get("DEMO_URL", ""),
        # Los modales solo se crean si hay sesión: así no se generan
        # tokens CSRF innecesarios para un visitante cualquiera.
        "modales": crear_modales() if session.get("usuario_id") else [],
    }


@publicas_bp.route("/")
def inicio():
    """Página principal: lee todo el contenido desde MySQL."""
    return render_template("index.html", **datos_index())


@publicas_bp.route("/descargar-cv")
def descargar_cv():
    """
    Descarga el PDF indicado en la base con un nombre amigable.

    send_from_directory ya evita rutas con '..', y as_attachment=True
    hace que el navegador descargue en vez de mostrar el PDF.
    """
    perfil = Perfil.query.first()
    if perfil is None or not perfil.cv_url:
        abort(404)

    return send_from_directory(
        os.path.join(current_app.root_path, "static"),
        perfil.cv_url,
        as_attachment=True,
        download_name=f"CV_{perfil.nombre.replace(' ', '_')}.pdf",
    )
