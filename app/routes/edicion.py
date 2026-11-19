import os
import uuid
from datetime import date

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

from app.extensions import db
from app.forms import crear_modales, reemplazar_formulario
from app.forms.items import (
    EducacionForm,
    ExperienciaForm,
    IdiomaForm,
    PerfilForm,
    ProyectoForm,
    RedSocialForm,
    SkillForm,
)
from app.models import (
    Educacion,
    Experiencia,
    Idioma,
    Perfil,
    Proyecto,
    RedSocial,
    Skill,
)
from app.routes.publicas import datos_index
from app.seguridad import login_requerido

edicion_bp = Blueprint("edicion", __name__, url_prefix="/editar")


# Un diccionario con los datos de cada sección evita escribir tres rutas
# casi idénticas por entidad. No es magia: son solo datos que se leen.
CONFIG_EDICION = {
    "red_social": {
        "modelo": RedSocial,
        "formulario": RedSocialForm,
        "campos": ("nombre", "icono", "url", "orden"),
        "archivos": (),
        "mensaje": "Red social guardada.",
    },
    "experiencia": {
        "modelo": Experiencia,
        "formulario": ExperienciaForm,
        "campos": ("puesto", "empresa", "descripcion", "fecha_inicio", "fecha_fin", "orden"),
        "archivos": (),
        "mensaje": "Experiencia guardada.",
    },
    "educacion": {
        "modelo": Educacion,
        "formulario": EducacionForm,
        "campos": ("institucion", "titulo", "fecha_inicio", "fecha_fin", "orden"),
        # (campo del formulario, columna de la tabla, prefijo del archivo)
        "archivos": (("logo", "logo_url", "logo"),),
        "mensaje": "Estudio guardado.",
    },
    "skill": {
        "modelo": Skill,
        "formulario": SkillForm,
        "campos": ("nombre", "porcentaje", "tipo", "orden"),
        "archivos": (),
        "mensaje": "Skill guardado.",
    },
    "idioma": {
        "modelo": Idioma,
        "formulario": IdiomaForm,
        "campos": ("nombre", "nivel", "porcentaje", "orden"),
        "archivos": (),
        "mensaje": "Idioma guardado.",
    },
    "proyecto": {
        "modelo": Proyecto,
        "formulario": ProyectoForm,
        "campos": ("nombre", "descripcion", "fecha", "link", "orden"),
        "archivos": (("imagen", "imagen_url", "proyecto"),),
        "mensaje": "Proyecto guardado.",
    },
}


def _perfil_actual():
    """Busca el perfil dueño de la sesión; si no existe, corta con 404."""
    perfil = Perfil.query.filter_by(usuario_id=session["usuario_id"]).first()
    if perfil is None:
        abort(404)
    return perfil


def _config_de(entidad):
    """Devuelve la configuración de una sección conocida, o 404."""
    config = CONFIG_EDICION.get(entidad)
    if config is None:
        abort(404)
    return config


def _item_de(config, item_id, perfil):
    """Busca un ítem pero solo dentro del perfil del usuario logueado."""
    return config["modelo"].query.filter_by(
        id=item_id, perfil_id=perfil.id
    ).first_or_404()


def _guardar_archivo(archivo, prefijo):
    """
    Guarda un archivo subido y devuelve la ruta relativa para la base.
    El nombre se vuelve seguro y se le agrega un sufijo único para no
    sobrescribir una imagen anterior con el mismo nombre.
    """
    if not archivo or not archivo.filename:
        return None

    nombre_seguro = secure_filename(archivo.filename)
    nombre = f"{prefijo}_{uuid.uuid4().hex[:8]}_{nombre_seguro}"
    carpeta = current_app.config["RUTA_UPLOADS"]
    os.makedirs(carpeta, exist_ok=True)
    archivo.save(os.path.join(carpeta, nombre))

    # En la base se guarda solo la ruta, no el archivo.
    return f"uploads/{nombre}"


def _aplicar_formulario(item, formulario, config):
    """Copia los valores validados del formulario al objeto de la base."""
    for campo in config["campos"]:
        setattr(item, campo, getattr(formulario, campo).data)

    for campo_formulario, columna, prefijo in config["archivos"]:
        ruta = _guardar_archivo(getattr(formulario, campo_formulario).data, prefijo)
        if ruta:
            setattr(item, columna, ruta)


def _pagina_con_error(entidad, formulario):
    """Vuelve a mostrar el index con el modal abierto y sus errores visibles."""
    contexto = datos_index()
    contexto["modales"] = reemplazar_formulario(
        contexto["modales"], entidad, formulario
    )
    return render_template("index.html", **contexto)


@edicion_bp.route("/perfil", methods=["POST"])
@login_requerido
def editar_perfil():
    """Actualiza nombre, título, descripción y archivos del perfil."""
    perfil = _perfil_actual()
    formulario = PerfilForm()

    if not formulario.validate_on_submit():
        return _pagina_con_error("perfil", formulario)

    perfil.nombre = formulario.nombre.data
    perfil.titulo = formulario.titulo.data
    perfil.descripcion = formulario.descripcion.data

    archivos = (
        ("foto", "foto_url", "perfil"),
        ("banner", "banner_url", "banner"),
        ("cv", "cv_url", "cv"),
    )
    for campo_formulario, columna, prefijo in archivos:
        ruta = _guardar_archivo(getattr(formulario, campo_formulario).data, prefijo)
        if ruta:
            setattr(perfil, columna, ruta)

    db.session.commit()
    flash("Perfil actualizado.", "exito")
    return redirect(url_for("publicas.inicio"))


@edicion_bp.route("/<entidad>/guardar", methods=["POST"])
@login_requerido
def guardar(entidad):
    """Alta o edición de un ítem: decide según el campo oculto item_id."""
    config = _config_de(entidad)
    perfil = _perfil_actual()
    formulario = config["formulario"]()

    if not formulario.validate_on_submit():
        return _pagina_con_error(entidad, formulario)

    item_id = formulario.item_id.data
    if item_id:
        item = _item_de(config, int(item_id), perfil)
        accion = "actualizado"
    else:
        item = config["modelo"](perfil_id=perfil.id)
        db.session.add(item)
        accion = "agregado"

    _aplicar_formulario(item, formulario, config)
    db.session.commit()
    flash(f"{config['mensaje']} ({accion}).", "exito")
    return redirect(url_for("publicas.inicio"))


@edicion_bp.route("/perfil/datos", methods=["GET"])
@login_requerido
def datos_perfil():
    """Valores del perfil para precargar el modal de 'Editar perfil'."""
    perfil = _perfil_actual()
    return jsonify(
        {
            "nombre": perfil.nombre,
            "titulo": perfil.titulo,
            "descripcion": perfil.descripcion,
        }
    )


@edicion_bp.route("/<entidad>/<int:item_id>", methods=["GET"])
@login_requerido
def datos_para_editar(entidad, item_id):
    """
    Devuelve los valores de un ítem en JSON. JavaScript los copia al modal
    cuando se hace clic en el lápiz. Los archivos no se precargan porque
    los navegadores no permiten rellenar un input type=file.
    """
    config = _config_de(entidad)
    perfil = _perfil_actual()
    item = _item_de(config, item_id, perfil)

    datos = {}
    for campo in config["campos"]:
        valor = getattr(item, campo)
        # Las fechas viajan como "YYYY-MM-DD", que es lo que espera el input.
        datos[campo] = valor.isoformat() if isinstance(valor, date) else valor

    return jsonify(datos)


@edicion_bp.route("/<entidad>/<int:item_id>/eliminar", methods=["POST"])
@login_requerido
def eliminar(entidad, item_id):
    """Baja de un ítem. El botón pide confirmación antes de enviar el POST."""
    config = _config_de(entidad)
    perfil = _perfil_actual()
    item = _item_de(config, item_id, perfil)

    db.session.delete(item)
    db.session.commit()
    flash("Elemento eliminado.", "aviso")
    return redirect(url_for("publicas.inicio"))


@edicion_bp.route("/<entidad>/reordenar", methods=["POST"])
@login_requerido
def reordenar(entidad):
    """
    Guarda el orden nuevo que mandó el drag & drop.

    JavaScript envía la lista de ids en el orden deseado. Acá se verifican
    dos cosas: que la sección exista y que TODOS los ids pertenezcan al
    perfil de la sesión (así nadie puede reordenar contenido ajeno).
    """
    config = _config_de(entidad)
    perfil = _perfil_actual()
    datos = request.get_json(silent=True) or {}
    ids = datos.get("ids", [])

    if not isinstance(ids, list) or len(ids) != len(set(ids)):
        abort(400)

    items = (
        config["modelo"]
        .query.filter(
            config["modelo"].id.in_(ids),
            config["modelo"].perfil_id == perfil.id,
        )
        .all()
    )
    if len(items) != len(ids):
        abort(400)

    por_id = {item.id: item for item in items}
    for indice, item_id in enumerate(ids):
        por_id[item_id].orden = indice + 1

    db.session.commit()
    return jsonify({"ok": True})
