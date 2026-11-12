from app.extensions import db
from app.models.item_portfolio import ItemPortfolio


class Experiencia(ItemPortfolio):
    """
    # PILAR: HERENCIA - Experiencia hereda de ItemPortfolio, así que ya tiene
    # id, perfil_id y orden sin volver a declararlos. Solo agrega lo propio.
    """

    __tablename__ = "experiencia"

    puesto = db.Column(db.String(120), nullable=False)
    empresa = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    # NULL significa que el trabajo sigue en curso ("Actualidad").
    fecha_fin = db.Column(db.Date, nullable=True)

    # PILAR: ENCAPSULAMIENTO - Propiedad de solo lectura: el período se
    # calcula siempre igual y no se puede modificar desde afuera.
    @property
    def periodo(self):
        return f"{self._mes_anio(self.fecha_inicio)} — {self._mes_anio(self.fecha_fin)}"

    # PILAR: POLIMORFISMO - Misma firma que la clase base, otro resultado.
    def resumen(self):
        return f"{self.puesto} · {self.empresa}"
