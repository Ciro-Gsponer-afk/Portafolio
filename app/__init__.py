from flask import Flask

from app.config import Config
from app.extensions import db
from app.routes.publicas import publicas_bp

# Importar los modelos hace que SQLAlchemy conozca todas las tablas.
from app import models  # noqa: F401


def crear_app():
    """
    Crea y configura la aplicación Flask.
    Se usa una función para poder crear la app también desde tests
    o desde el servidor de producción (gunicorn).
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Conecta SQLAlchemy con esta app (antes no sabía cuál usar).
    db.init_app(app)

    # Registra las rutas públicas.
    app.register_blueprint(publicas_bp)

    return app
