from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(
                message="El nombre del producto es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            DataRequired(
                message="La descripción es obligatoria."
            ),
            Length(
                min=5,
                message="La descripción debe tener al menos 5 caracteres."
            )
        ]
    )

    precio = DecimalField(
        "Precio",
        validators=[
            DataRequired(
                message="El precio es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El precio debe ser mayor o igual a 0."
            )
        ]
    )

    id_proveedor = SelectField(
        "Proveedor",
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un proveedor."
            )
        ]
    )