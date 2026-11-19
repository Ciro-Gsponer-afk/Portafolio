# Los formularios viven en su propia carpeta para separar
# "qué datos se aceptan" de "qué hace la ruta con esos datos".
from app.forms.items import (
    EducacionForm,
    ExperienciaForm,
    IdiomaForm,
    PerfilForm,
    ProyectoForm,
    RedSocialForm,
    SkillForm,
)


def crear_modales():
    """
    Arma la lista de diálogos de edición. Cada dialog tiene un título y
    un formulario vacío; se usa tanto en la página principal como al
    volver a mostrar errores de validación.
    """
    return [
        {"entidad": "perfil", "titulo": "Editar perfil", "formulario": PerfilForm()},
        {"entidad": "red_social", "titulo": "Red social", "formulario": RedSocialForm()},
        {"entidad": "experiencia", "titulo": "Experiencia", "formulario": ExperienciaForm()},
        {"entidad": "educacion", "titulo": "Educación", "formulario": EducacionForm()},
        {"entidad": "skill", "titulo": "Skill", "formulario": SkillForm()},
        {"entidad": "idioma", "titulo": "Idioma", "formulario": IdiomaForm()},
        {"entidad": "proyecto", "titulo": "Proyecto", "formulario": ProyectoForm()},
    ]


def reemplazar_formulario(modales, entidad, formulario):
    """Pone el formulario con errores en el modal correspondiente."""
    for modal in modales:
        if modal["entidad"] == entidad:
            modal["formulario"] = formulario
            break
    return modales
