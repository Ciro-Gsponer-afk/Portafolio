from app.extensions import db
from app.models.item_portfolio import ItemPortfolio


class Idioma(ItemPortfolio):
    """Idioma con nivel descriptivo y porcentaje para la barra."""

    __tablename__ = "idioma"

    nombre = db.Column(db.String(80), nullable=False)
    nivel = db.Column(db.String(50), nullable=False)
    porcentaje = db.Column(db.SmallInteger, nullable=False)

    __table_args__ = (
        db.CheckConstraint(
            "porcentaje >= 0 AND porcentaje <= 100",
            name="chk_idioma_porcentaje",
        ),
    )

    def resumen(self):
        return f"{self.nombre} · {self.nivel}"
