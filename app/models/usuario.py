from app.extensions import db


class Usuario(db.Model):
    """Cuenta que puede iniciar sesión para editar el portfolio."""

    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    # Nunca se guarda la contraseña real, solo su hash (Fase 4).
    password_hash = db.Column(db.String(255), nullable=False)
    creado_en = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
