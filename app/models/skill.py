from app.extensions import db
from app.models.item_portfolio import ItemPortfolio


class Skill(ItemPortfolio):
    """Habilidad dura o blanda, con un porcentaje de 0 a 100."""

    __tablename__ = "skill"

    nombre = db.Column(db.String(80), nullable=False)
    porcentaje = db.Column(db.SmallInteger, nullable=False)
    # Una sola tabla para hard y soft, separadas por este campo.
    tipo = db.Column(
        db.Enum("hard", "soft", name="tipo_skill"), nullable=False, default="hard"
    )

    # El CHECK lo valida MySQL; en SQLite también se respeta.
    __table_args__ = (
        db.CheckConstraint(
            "porcentaje >= 0 AND porcentaje <= 100",
            name="chk_skill_porcentaje",
        ),
    )

    def resumen(self):
        return f"{self.nombre} ({self.porcentaje}%)"
