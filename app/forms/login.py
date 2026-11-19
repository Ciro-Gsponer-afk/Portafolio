from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """
    Formulario de ingreso.

    FlaskForm ya incluye el campo oculto 'csrf_token' y lo valida solo,
    por eso no hace falta escribir esa parte a mano. Acá solo definimos
    qué campos pedimos y sus reglas.
    """

    username = StringField(
        "Usuario", validators=[DataRequired(), Length(min=3, max=50)]
    )
    password = PasswordField("Contraseña", validators=[DataRequired()])
    recordar = BooleanField("Recordarme")
    submit = SubmitField("Ingresar")
