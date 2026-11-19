from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import DateField, HiddenField, IntegerField, SelectField, StringField
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

# Extensiones aceptadas para imágenes. La lista se usa en la validación,
# así un visitante no puede subir un archivo ejecutable haciéndolo pasar por foto.
IMAGENES_PERMITIDAS = ["jpg", "jpeg", "png", "webp", "gif", "svg"]


class PerfilForm(FlaskForm):
    """Datos visibles de 'Acerca de' y archivos opcionales (foto, banner, CV)."""

    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    titulo = StringField("Título", validators=[DataRequired(), Length(max=120)])
    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    foto = FileField("Foto de perfil", validators=[FileAllowed(IMAGENES_PERMITIDAS, "Solo imágenes")])
    banner = FileField("Banner", validators=[FileAllowed(IMAGENES_PERMITIDAS, "Solo imágenes")])
    cv = FileField("CV en PDF", validators=[FileAllowed(["pdf"], "Solo archivos PDF")])
    submit = SubmitField("Guardar perfil")


class RedSocialForm(FlaskForm):
    item_id = HiddenField()
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=60)])
    icono = StringField("Clase del ícono", validators=[DataRequired(), Length(max=80)])
    url = StringField("URL", validators=[DataRequired(), Length(max=255)])
    orden = IntegerField("Orden", validators=[DataRequired(), NumberRange(min=0)], default=0)
    submit = SubmitField("Guardar red")


class ExperienciaForm(FlaskForm):
    item_id = HiddenField()
    puesto = StringField("Puesto", validators=[DataRequired(), Length(max=120)])
    empresa = StringField("Empresa", validators=[DataRequired(), Length(max=120)])
    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    fecha_inicio = DateField("Desde", format="%Y-%m-%d", validators=[DataRequired()])
    # Vacío = "Actualidad". Por eso el validador es Optional.
    fecha_fin = DateField("Hasta (opcional)", format="%Y-%m-%d", validators=[Optional()])
    orden = IntegerField("Orden", validators=[DataRequired(), NumberRange(min=0)], default=0)
    submit = SubmitField("Guardar experiencia")


class EducacionForm(FlaskForm):
    item_id = HiddenField()
    institucion = StringField("Institución", validators=[DataRequired(), Length(max=120)])
    titulo = StringField("Título", validators=[DataRequired(), Length(max=120)])
    fecha_inicio = DateField("Desde", format="%Y-%m-%d", validators=[DataRequired()])
    fecha_fin = DateField("Hasta (opcional)", format="%Y-%m-%d", validators=[Optional()])
    logo = FileField("Logo", validators=[FileAllowed(IMAGENES_PERMITIDAS, "Solo imágenes")])
    orden = IntegerField("Orden", validators=[DataRequired(), NumberRange(min=0)], default=0)
    submit = SubmitField("Guardar estudio")


class SkillForm(FlaskForm):
    item_id = HiddenField()
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=80)])
    porcentaje = IntegerField(
        "Porcentaje", validators=[DataRequired(), NumberRange(min=0, max=100)]
    )
    tipo = SelectField("Tipo", choices=[("hard", "Hard skill"), ("soft", "Soft skill")])
    orden = IntegerField("Orden", validators=[DataRequired(), NumberRange(min=0)], default=0)
    submit = SubmitField("Guardar skill")


class IdiomaForm(FlaskForm):
    item_id = HiddenField()
    nombre = StringField("Idioma", validators=[DataRequired(), Length(max=80)])
    nivel = StringField("Nivel", validators=[DataRequired(), Length(max=50)])
    porcentaje = IntegerField(
        "Porcentaje", validators=[DataRequired(), NumberRange(min=0, max=100)]
    )
    orden = IntegerField("Orden", validators=[DataRequired(), NumberRange(min=0)], default=0)
    submit = SubmitField("Guardar idioma")


class ProyectoForm(FlaskForm):
    item_id = HiddenField()
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=120)])
    descripcion = TextAreaField("Descripción", validators=[DataRequired()])
    fecha = DateField("Fecha", format="%Y-%m-%d", validators=[DataRequired()])
    link = StringField("Link a la evidencia", validators=[DataRequired(), Length(max=255)])
    imagen = FileField("Captura", validators=[FileAllowed(IMAGENES_PERMITIDAS, "Solo imágenes")])
    orden = IntegerField("Orden", validators=[DataRequired(), NumberRange(min=0)], default=0)
    submit = SubmitField("Guardar proyecto")
