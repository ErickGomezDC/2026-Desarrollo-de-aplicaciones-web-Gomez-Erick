from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):

    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired(
                message="El nombre del cliente es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    producto = StringField(
        "Producto",
        validators=[
            DataRequired(
                message="El producto es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El producto debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    cantidad = IntegerField(
        "Cantidad",
        validators=[
            DataRequired(
                message="La cantidad es obligatoria."
            ),
            NumberRange(
                min=1,
                message="La cantidad debe ser mayor o igual a 1."
            )
        ]
    )

    total = DecimalField(
        "Total",
        validators=[
            DataRequired(
                message="El total es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El total debe ser mayor o igual a 0."
            )
        ]
    )