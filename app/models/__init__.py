# Al importar este paquete se registran TODAS las clases en SQLAlchemy.
# Es necesario que app/__init__.py lo importe antes de usar la base.
from app.models.usuario import Usuario
from app.models.perfil import Perfil
from app.models.red_social import RedSocial
from app.models.experiencia import Experiencia
from app.models.educacion import Educacion
from app.models.skill import Skill
from app.models.idioma import Idioma
from app.models.proyecto import Proyecto

__all__ = [
    "Usuario",
    "Perfil",
    "RedSocial",
    "Experiencia",
    "Educacion",
    "Skill",
    "Idioma",
    "Proyecto",
]
