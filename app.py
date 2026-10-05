from flask import Flask, render_template, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    current_user,
    login_required,
    logout_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

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


# =========================================================
# FLASK-LOGIN
# =========================================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT id, usuario, password
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


# =========================================================
# INICIO
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


# =========================================================
# REGISTRO DE USUARIOS
# =========================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE usuario = %s
            """,
            (form.usuario.data,)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente:
            flash("El nombre de usuario ya existe.", "danger")

            cursor.close()
            conn.close()

            return render_template(
                "registro.html",
                form=form
            )

        password_hash = generate_password_hash(
            form.password.data
        )

        cursor.execute(
            """
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
            """,
            (
                form.usuario.data,
                password_hash
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Usuario registrado correctamente. Ahora puede iniciar sesión.",
            "success"
        )

        return redirect(url_for("login"))

    return render_template(
        "registro.html",
        form=form
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
            """,
            (form.usuario.data,)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario and check_password_hash(
            usuario["password"],
            form.password.data
        ):

            usuario_obj = Usuario(
                id=usuario["id"],
                usuario=usuario["usuario"],
                password=usuario["password"]
            )

            login_user(usuario_obj)

            flash(
                "Inicio de sesión exitoso.",
                "success"
            )

            return redirect(url_for("dashboard"))

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("login"))


# =========================================================
# PRODUCTOS
# =========================================================

@app.route("/productos")
@login_required
def productos():

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

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


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():

    form = ProductoForm()

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
        """
    )

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    form.id_proveedor.choices = [
        (
            proveedor["id_proveedor"],
            proveedor["nombre"]
        )
        for proveedor in proveedores
    ]

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO productos
            (
                nombre,
                descripcion,
                precio,
                id_proveedor
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.precio.data,
                form.id_proveedor.data
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Producto registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT *
        FROM productos
        WHERE id_producto = %s
        """,
        (id,)
    )

    producto = cursor.fetchone()

    cursor.execute(
        """
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
        """
    )

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    if producto is None:

        flash(
            "Producto no encontrado.",
            "danger"
        )

        return redirect(url_for("productos"))

    form = ProductoForm()

    form.id_proveedor.choices = [
        (
            proveedor["id_proveedor"],
            proveedor["nombre"]
        )
        for proveedor in proveedores
    ]

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE productos
            SET
                nombre = %s,
                descripcion = %s,
                precio = %s,
                id_proveedor = %s
            WHERE id_producto = %s
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.precio.data,
                form.id_proveedor.data,
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

        return redirect(url_for("productos"))

    if not form.is_submitted():

        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = producto["precio"]
        form.id_proveedor.data = producto["id_proveedor"]

    return render_template(
        "formulario_producto.html",
        form=form,
        producto=producto
    )


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

    return redirect(url_for("productos"))


# =========================================================
# PROVEEDORES
# =========================================================

@app.route("/proveedores")
@login_required
def proveedores():

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT
            id_proveedor,
            nombre,
            correo,
            telefono
        FROM proveedores
        ORDER BY id_proveedor ASC
        """
    )

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO proveedores
            (
                nombre,
                correo,
                telefono
            )
            VALUES (%s, %s, %s)
            """,
            (
                form.nombre.data,
                form.correo.data,
                form.telefono.data
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Proveedor registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


@app.route("/proveedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT *
        FROM proveedores
        WHERE id_proveedor = %s
        """,
        (id,)
    )

    proveedor = cursor.fetchone()

    cursor.close()
    conn.close()

    if proveedor is None:

        flash(
            "Proveedor no encontrado.",
            "danger"
        )

        return redirect(url_for("proveedores"))

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE proveedores
            SET
                nombre = %s,
                correo = %s,
                telefono = %s
            WHERE id_proveedor = %s
            """,
            (
                form.nombre.data,
                form.correo.data,
                form.telefono.data,
                id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Proveedor actualizado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    if not form.is_submitted():

        form.nombre.data = proveedor["nombre"]
        form.correo.data = proveedor["correo"]
        form.telefono.data = proveedor["telefono"]

    return render_template(
        "formulario_proveedor.html",
        form=form,
        proveedor=proveedor
    )


@app.route("/proveedores/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM proveedores
        WHERE id_proveedor = %s
        """,
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Proveedor eliminado correctamente.",
        "success"
    )

    return redirect(url_for("proveedores"))


# =========================================================
# CLIENTES
# =========================================================

@app.route("/clientes")
@login_required
def clientes():

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT
            id_cliente,
            nombre,
            correo,
            telefono
        FROM clientes
        ORDER BY id_cliente ASC
        """
    )

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "clientes.html",
        clientes=clientes
    )


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO clientes
            (
                nombre,
                correo,
                telefono
            )
            VALUES (%s, %s, %s)
            """,
            (
                form.nombre.data,
                form.correo.data,
                form.telefono.data
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Cliente registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )


@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT *
        FROM clientes
        WHERE id_cliente = %s
        """,
        (id,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conn.close()

    if cliente is None:

        flash(
            "Cliente no encontrado.",
            "danger"
        )

        return redirect(url_for("clientes"))

    form = ClienteForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE clientes
            SET
                nombre = %s,
                correo = %s,
                telefono = %s
            WHERE id_cliente = %s
            """,
            (
                form.nombre.data,
                form.correo.data,
                form.telefono.data,
                id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Cliente actualizado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    if not form.is_submitted():

        form.nombre.data = cliente["nombre"]
        form.correo.data = cliente["correo"]
        form.telefono.data = cliente["telefono"]

    return render_template(
        "formulario_cliente.html",
        form=form,
        cliente=cliente
    )


@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_cliente(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM clientes
        WHERE id_cliente = %s
        """,
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Cliente eliminado correctamente.",
        "success"
    )

    return redirect(url_for("clientes"))


# =========================================================
# FACTURACIÓN
# =========================================================

@app.route("/facturacion")
@login_required
def facturacion():

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT
            f.id_factura,
            f.id_cliente,
            c.nombre AS cliente,
            f.producto,
            f.cantidad,
            f.fecha,
            f.total
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        ORDER BY f.id_factura ASC
        """
    )

    facturas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


@app.route("/facturacion/nuevo", methods=["GET", "POST"])
@login_required
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Buscar el cliente por nombre
        cursor.execute(
            """
            SELECT id_cliente
            FROM clientes
            WHERE LOWER(nombre) = LOWER(%s)
            LIMIT 1
            """,
            (form.cliente.data.strip(),)
        )

        cliente = cursor.fetchone()

        if cliente is None:

            cursor.close()
            conn.close()

            flash(
                "El cliente indicado no existe. Registre primero el cliente.",
                "danger"
            )

            return render_template(
                "formulario_facturacion.html",
                form=form
            )

        cursor.close()
        conn.close()

        # Registrar factura
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO facturas
            (
                id_cliente,
                producto,
                cantidad,
                total
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                cliente["id_cliente"],
                form.producto.data.strip(),
                form.cantidad.data,
                form.total.data
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Factura registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


@app.route("/facturacion/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_factura(id):

    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute(
        """
        SELECT
            f.id_factura,
            f.id_cliente,
            c.nombre AS cliente,
            f.producto,
            f.cantidad,
            f.fecha,
            f.total
        FROM facturas f
        INNER JOIN clientes c
            ON f.id_cliente = c.id_cliente
        WHERE f.id_factura = %s
        """,
        (id,)
    )

    factura = cursor.fetchone()

    cursor.close()
    conn.close()

    if factura is None:

        flash(
            "Factura no encontrada.",
            "danger"
        )

        return redirect(url_for("facturacion"))

    form = FacturacionForm()

    if form.validate_on_submit():

        conn = obtener_conexion()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT id_cliente
            FROM clientes
            WHERE LOWER(nombre) = LOWER(%s)
            LIMIT 1
            """,
            (form.cliente.data.strip(),)
        )

        cliente = cursor.fetchone()

        if cliente is None:

            cursor.close()
            conn.close()

            flash(
                "El cliente indicado no existe.",
                "danger"
            )

            return render_template(
                "formulario_facturacion.html",
                form=form,
                factura=factura
            )

        cursor.close()
        conn.close()

        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE facturas
            SET
                id_cliente = %s,
                producto = %s,
                cantidad = %s,
                total = %s
            WHERE id_factura = %s
            """,
            (
                cliente["id_cliente"],
                form.producto.data.strip(),
                form.cantidad.data,
                form.total.data,
                id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Factura actualizada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    if not form.is_submitted():

        form.cliente.data = factura["cliente"]
        form.producto.data = factura["producto"]
        form.cantidad.data = factura["cantidad"]
        form.total.data = factura["total"]

    return render_template(
        "formulario_facturacion.html",
        form=form,
        factura=factura
    )


@app.route("/facturacion/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_factura(id):

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM facturas
        WHERE id_factura = %s
        """,
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Factura eliminada correctamente.",
        "success"
    )

    return redirect(url_for("facturacion"))


# =========================================================
# EJECUCIÓN
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)