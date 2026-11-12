from app.extensions import db
from app.models.item_portfolio import ItemPortfolio


class Educacion(ItemPortfolio):
    """Estudios formales: institución, título, logo y período."""

    __tablename__ = "educacion"

    institucion = db.Column(db.String(120), nullable=False)
    titulo = db.Column(db.String(120), nullable=False)
    logo_url = db.Column(
        db.String(255), nullable=False, default="img/instituciones/default.png"
    )
    fecha_inicio = db.Column(db.Date, nullable=False)
    # NULL significa que la carrera sigue en curso.
    fecha_fin = db.Column(db.Date, nullable=True)

    @property
    def periodo(self):
        return f"{self._mes_anio(self.fecha_inicio)} — {self._mes_anio(self.fecha_fin)}"

    def resumen(self):
        return f"{self.titulo} · {self.institucion}"
