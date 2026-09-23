from flask import Flask, render_template, redirect, url_for, flash

from flask_login import (
    LoginManager,
    login_user,
    current_user,
    login_required,
    logout_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.usuario_form import UsuarioForm
from forms.login_form import LoginForm

from models import Usuario

from conexion.conexion import obtener_conexion


app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-proyecto-2026"


# ==========================================
# FLASK-LOGIN
# ==========================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


# ==========================================
# CARGAR USUARIO
# ==========================================

@login_manager.user_loader
def load_user(user_id):

    conn = obtener_conexion()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id,
            usuario,
            password
        FROM usuarios
        WHERE id = %s
        """,
        (user_id,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario is None:
        return None

    return Usuario(
        id=usuario["id"],
        usuario=usuario["usuario"],
        password=usuario["password"]
    )


# ==========================================
# INICIO
# ==========================================

@app.route("/")
def inicio():

    return render_template("index.html")


# ==========================================
# REGISTRO DE USUARIOS
# ==========================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        usuario_ingresado = form.usuario.data
        password_ingresada = form.password.data

        # ==========================================
        # VERIFICAR USUARIO EXISTENTE
        # ==========================================

        conn = obtener_conexion()

        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE usuario = %s
            """,
            (usuario_ingresado,)
        )

        usuario_existente = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario_existente is not None:

            flash(
                "El nombre de usuario ya está registrado.",
                "warning"
            )

            return render_template(
                "registro.html",
                form=form
            )

        # ==========================================
        # ENCRIPTAR CONTRASEÑA
        # ==========================================

        password_hash = generate_password_hash(
            password_ingresada
        )

        # ==========================================
        # GUARDAR USUARIO
        # ==========================================

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO usuarios
            (usuario, password)
            VALUES (%s, %s)
            """,
            (
                usuario_ingresado,
                password_hash
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Usuario registrado correctamente. Ahora puedes iniciar sesión.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "registro.html",
        form=form
    )


# ==========================================
# INICIAR SESIÓN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    # Si ya inició sesión
    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    form = LoginForm()

    if form.validate_on_submit():

        usuario_ingresado = form.usuario.data
        password_ingresada = form.password.data

        conn = obtener_conexion()

        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                usuario,
                password
            FROM usuarios
            WHERE usuario = %s
            """,
            (usuario_ingresado,)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        # ==========================================
        # VERIFICAR CONTRASEÑA
        # ==========================================

        if usuario is not None and check_password_hash(
            usuario["password"],
            password_ingresada
        ):

            usuario_objeto = Usuario(
                id=usuario["id"],
                usuario=usuario["usuario"],
                password=usuario["password"]
            )

            login_user(usuario_objeto)

            flash(
                "Inicio de sesión exitoso.",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        # ==========================================
        # LOGIN INCORRECTO
        # ==========================================

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


# ==========================================
# CERRAR SESIÓN
# ==========================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# ==========================================
# PRODUCTOS - LISTAR
# ==========================================

@app.route("/productos")
@login_required
def productos():

    conn = obtener_conexion()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            p.id_producto,
            p.nombre,
            p.descripcion,
            p.precio,
            p.id_proveedor,
            pr.nombre AS proveedor
        FROM productos p
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_producto ASC
        """
    )

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# ==========================================
# REGISTRAR PRODUCTO
# ==========================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        nombre = form.nombre.data
        descripcion = form.descripcion.data
        precio = form.precio.data

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO productos
            (nombre, descripcion, precio)
            VALUES (%s, %s, %s)
            """,
            (
                nombre,
                descripcion,
                precio
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("productos")
        )

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ==========================================
# EDITAR PRODUCTO
# ==========================================

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    conn = obtener_conexion()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id_producto,
            nombre,
            descripcion,
            precio
        FROM productos
        WHERE id_producto = %s
        """,
        (id,)
    )

    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    if producto is None:

        flash(
            "Producto no encontrado.",
            "danger"
        )

        return redirect(
            url_for("productos")
        )

    form = ProductoForm()

    if form.validate_on_submit():

        nombre = form.nombre.data
        descripcion = form.descripcion.data
        precio = form.precio.data

        conn = obtener_conexion()

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE productos
            SET
                nombre = %s,
                descripcion = %s,
                precio = %s
            WHERE id_producto = %s
            """,
            (
                nombre,
                descripcion,
                precio,
                id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Producto actualizado correctamente.",
            "success"
        )

        return redirect(
            url_for("productos")
        )

    if not form.is_submitted():

        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = producto["precio"]

    return render_template(
        "formulario_producto.html",
        form=form,
        editar=True
    )


# ==========================================
# ELIMINAR PRODUCTO
# ==========================================

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):

    conn = obtener_conexion()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM productos
        WHERE id_producto = %s
        """,
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Producto eliminado correctamente.",
        "success"
    )

    return redirect(
        url_for("productos")
    )


# ==========================================
# CLIENTES
# ==========================================

@app.route("/clientes")
@login_required
def clientes():

    return render_template(
        "clientes.html"
    )


# ==========================================
# REGISTRAR CLIENTE
# ==========================================

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        nombre = form.nombre.data
        correo = form.correo.data
        telefono = form.telefono.data

        print("Cliente recibido:")
        print("Nombre:", nombre)
        print("Correo:", correo)
        print("Teléfono:", telefono)

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("clientes")
        )

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# ==========================================
# PROVEEDORES
# ==========================================

@app.route("/proveedores")
@login_required
def proveedores():

    return render_template(
        "proveedores.html"
    )


# ==========================================
# REGISTRAR PROVEEDOR
# ==========================================

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        nombre = form.nombre.data
        correo = form.correo.data
        telefono = form.telefono.data

        print("Proveedor recibido:")
        print("Nombre:", nombre)
        print("Correo:", correo)
        print("Teléfono:", telefono)

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("proveedores")
        )

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# ==========================================
# FACTURACIÓN
# ==========================================

@app.route("/facturacion")
@login_required
def facturacion():

    return render_template(
        "facturacion.html"
    )


# ==========================================
# REGISTRAR FACTURACIÓN
# ==========================================

@app.route("/facturacion/nuevo", methods=["GET", "POST"])
@login_required
def formulario_facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        cliente = form.cliente.data
        producto = form.producto.data
        cantidad = form.cantidad.data
        total = form.total.data

        print("Factura recibida:")
        print("Cliente:", cliente)
        print("Producto:", producto)
        print("Cantidad:", cantidad)
        print("Total:", total)

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(
            url_for("facturacion")
        )

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)