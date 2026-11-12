# Acá se crea el objeto "db" UNA sola vez.
# Va en un archivo aparte para que los modelos y la app lo importen
# sin caer en importaciones circulares (app -> models -> app).
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
