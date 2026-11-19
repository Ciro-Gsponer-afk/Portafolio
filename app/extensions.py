# Acá se crea el objeto "db" UNA sola vez.
# Va en un archivo aparte para que los modelos y la app lo importen
# sin caer en importaciones circulares (app -> models -> app).
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()

# CSRFProtect agrega un token oculto a cada formulario y lo valida en el POST.
# Se crea acá, igual que db, para que toda la app use el mismo objeto.
csrf = CSRFProtect()
