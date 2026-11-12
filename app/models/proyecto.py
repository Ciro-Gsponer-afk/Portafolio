from app.extensions import db
from app.models.item_portfolio import ItemPortfolio


class Proyecto(ItemPortfolio):
    """Proyecto con descripción, fecha, link a la evidencia e imagen."""

    __tablename__ = "proyecto"

    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    link = db.Column(db.String(255), nullable=False)
    imagen_url = db.Column(
        db.String(255), nullable=False, default="img/proyectos/default.jpg"
    )

    @property
    def anio(self):
        return self.fecha.year

    def resumen(self):
        return f"{self.nombre} ({self.anio})"
