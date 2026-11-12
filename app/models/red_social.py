from app.extensions import db
from app.models.item_portfolio import ItemPortfolio


class RedSocial(ItemPortfolio):
    """
    Ícono del header (GitHub, LinkedIn, correo).
    Hereda id, perfil_id y orden desde ItemPortfolio.
    """

    __tablename__ = "red_social"

    nombre = db.Column(db.String(60), nullable=False)
    # Clase de FontAwesome, por ejemplo: "fa-brands fa-github".
    icono = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    # PILAR: POLIMORFISMO - Sobrescribe el resumen() de la clase base.
    def resumen(self):
        return self.nombre
