from app.extensions import db


class Perfil(db.Model):
    """
    Datos del dueño del portfolio: banner, foto, nombre, título y "Acerca de".
    Es una sola fila por usuario (usuario_id es UNIQUE).
    """

    __tablename__ = "perfil"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuario.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    nombre = db.Column(db.String(100), nullable=False)
    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    foto_url = db.Column(db.String(255), nullable=False, default="img/perfil.jpg")
    banner_url = db.Column(db.String(255), nullable=False, default="img/banner.jpg")
    cv_url = db.Column(
        db.String(255), nullable=False, default="cv/Ciro_Gsponer_CV.pdf"
    )
