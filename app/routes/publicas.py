from flask import Blueprint, render_template

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


@publicas_bp.route("/")
def inicio():
    """Página principal: lee todo el contenido desde MySQL."""
    # El portfolio tiene un solo perfil, entonces alcanza con el primero.
    perfil = Perfil.query.first()

    # Si la base está vacía, la plantilla muestra un mensaje en vez de fallar.
    if perfil is None:
        return render_template("index.html", perfil=None)

    # Se consulta cada sección por separado para que la plantilla
    # reciba exactamente las listas que necesita.
    skills = _listar_por_orden(Skill, perfil.id)

    return render_template(
        "index.html",
        perfil=perfil,
        redes=_listar_por_orden(RedSocial, perfil.id),
        experiencias=_listar_por_orden(Experiencia, perfil.id),
        educaciones=_listar_por_orden(Educacion, perfil.id),
        # Se separan acá para no hacer lógica en la plantilla.
        skills_hard=[s for s in skills if s.tipo == "hard"],
        skills_soft=[s for s in skills if s.tipo == "soft"],
        idiomas=_listar_por_orden(Idioma, perfil.id),
        proyectos=_listar_por_orden(Proyecto, perfil.id),
    )
