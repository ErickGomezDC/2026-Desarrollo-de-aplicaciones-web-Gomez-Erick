from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import DataRequired, Length, Email


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre del proveedor",
        validators=[
            DataRequired(
                message="El nombre del proveedor es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    correo = EmailField(
        "Correo electrónico",
        validators=[
            DataRequired(
                message="El correo electrónico es obligatorio."
            ),
            Email(
                message="Ingrese un correo electrónico válido."
            )
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(
                message="El teléfono es obligatorio."
            ),
            Length(
                min=7,
                max=20,
                message="El teléfono debe tener entre 7 y 20 caracteres."
            )
        ]
    )