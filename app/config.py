import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

# Lee el archivo .env y lo carga como variables de entorno.
# Así las credenciales quedan fuera del código y de Git.
load_dotenv()


def _url_desde_addon():
    """
    En Clever Cloud el add-on MySQL inyecta variables MYSQL_ADDON_*.
    Construimos la URL con esos datos para no copiar contraseñas a mano.
    """
    host = os.getenv("MYSQL_ADDON_HOST")
    if not host:
        return None

    # quote_plus escapa caracteres especiales (por ejemplo un @ en la clave).
    usuario = quote_plus(os.getenv("MYSQL_ADDON_USER", ""))
    clave = quote_plus(os.getenv("MYSQL_ADDON_PASSWORD", ""))
    base = os.getenv("MYSQL_ADDON_DB", "")
    puerto = os.getenv("MYSQL_ADDON_PORT", "3306")
    return f"mysql+mysqlconnector://{usuario}:{clave}@{host}:{puerto}/{base}"


# En local se usa DATABASE_URL del .env; en producción, la del add-on.
# Si falta, el error se ve al instante y no más tarde con un mensaje confuso.
URL_BASE_DATOS = os.getenv("DATABASE_URL") or _url_desde_addon()
if not URL_BASE_DATOS:
    raise RuntimeError(
        "Falta la conexión a MySQL. En local copiá .env.example como .env "
        "y completá DATABASE_URL. En Clever Cloud linkeá el add-on MySQL."
    )

# En producción no aceptamos una clave provisional: las sesiones deben
# firmarse con un valor secreto y distinto en cada despliegue.
CLAVE_SECRETA = os.getenv("SECRET_KEY")
if not CLAVE_SECRETA:
    if os.getenv("FLASK_DEBUG", "1") == "0":
        raise RuntimeError(
            "Falta SECRET_KEY. Generala con: "
            "python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    CLAVE_SECRETA = "clave-provisional-solo-desarrollo"


class Config:
    """Configuración que Flask lee al arrancar."""

    SECRET_KEY = CLAVE_SECRETA
    SQLALCHEMY_DATABASE_URI = URL_BASE_DATOS

    # Video o demo que se muestra en el iframe de la página principal.
    # Vacío por defecto: la plantilla muestra un aviso en su lugar.
    DEMO_URL = os.getenv("DEMO_URL", "").strip()

    # Evita que SQLAlchemy registre cada cambio en memoria: no lo necesitamos.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Antes de usar una conexión del pool, verifica que siga viva.
    # Es útil en hosting gratuito, que suele cerrar conexiones inactivas.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # Los archivos que sube el dueño se guardan en static/uploads.
    RUTA_UPLOADS = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "static", "uploads"
    )

    # Límite de 5 MB por petición: evita subir archivos gigantes por accidente.
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
