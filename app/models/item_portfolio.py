from app.extensions import db


class ItemPortfolio(db.Model):
    """
    Clase BASE de todos los elementos que se listan en el portfolio
    (experiencias, educación, skills, idiomas, proyectos y redes).

    # PILAR: ABSTRACCIÓN - Esta clase representa la idea general de
    # "ítem del portfolio": todo ítem tiene un id, pertenece a un perfil
    # y se ordena con un número. No se usa sola, solo se hereda.

    # PILAR: POLIMORFISMO - Define el método resumen(), pero no lo resuelve:
    # cada clase hija lo implementa a su manera y la plantilla puede llamar
    # item.resumen() sin saber de qué clase se trata.
    """

    __abstract__ = True  # No crea una tabla propia: es solo la base.

    # Columnas que comparten todas las tablas hijas.
    id = db.Column(db.Integer, primary_key=True)
    perfil_id = db.Column(
        db.Integer,
        db.ForeignKey("perfil.id", ondelete="CASCADE"),
        nullable=False,
    )
    orden = db.Column(db.Integer, nullable=False, default=0)

    def resumen(self):
        """Devuelve un texto corto para mostrar en la página."""
        raise NotImplementedError("Cada clase hija debe implementar resumen()")

    # PILAR: ENCAPSULAMIENTO - Método interno (empieza con _) que concentra
    # el formateo de fechas. Las hijas lo usan, pero nadie fuera de la clase
    # necesita saber cómo se arma el texto.
    @staticmethod
    def _mes_anio(fecha):
        if fecha is None:
            return "Actualidad"
        return fecha.strftime("%m/%Y")
