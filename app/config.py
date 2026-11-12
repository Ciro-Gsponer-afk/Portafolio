import os

from dotenv import load_dotenv

# Lee el archivo .env y lo carga como variables de entorno.
# Así las credenciales quedan fuera del código y de Git.
load_dotenv()

# La URL de conexión es obligatoria: si falta, el error se ve al instante
# y no más tarde con un mensaje confuso de SQLAlchemy.
URL_BASE_DATOS = os.getenv("DATABASE_URL")
if not URL_BASE_DATOS:
    raise RuntimeError(
        "Falta DATABASE_URL. Copiá .env.example como .env y completá "
        "la conexión a MySQL (por ejemplo: "
        "mysql+mysqlconnector://usuario:clave@localhost:3306/portafolio_db)."
    )


class Config:
    """Configuración que Flask lee al arrancar."""

    SECRET_KEY = os.getenv("SECRET_KEY", "clave-provisional-solo-desarrollo")
    SQLALCHEMY_DATABASE_URI = URL_BASE_DATOS

    # Evita que SQLAlchemy registre cada cambio en memoria: no lo necesitamos.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Antes de usar una conexión del pool, verifica que siga viva.
    # Es útil en hosting gratuito, que suele cerrar conexiones inactivas.
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
