from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

from conexion.conexion import obtener_conexion


app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-proyecto-2026"


# ==========================================
# INICIO
# ==========================================

@app.route("/")
def inicio():
    return render_template("index.html")


# ==========================================
# PRODUCTOS - LISTAR
# ==========================================

@app.route("/productos")
def productos():

    conn = obtener_conexion()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
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
    """)

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
            (nombre, descripcion, precio)
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


# ==========================================
# EDITAR PRODUCTO
# ==========================================

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
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

        return redirect(url_for("productos"))

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

        return redirect(url_for("productos"))

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


# ==========================================
# CLIENTES
# ==========================================

@app.route("/clientes")
def clientes():

    return render_template("clientes.html")


@app.route("/clientes/nuevo", methods=["GET", "POST"])
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

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# ==========================================
# PROVEEDORES
# ==========================================

@app.route("/proveedores")
def proveedores():

    return render_template("proveedores.html")


@app.route("/proveedores/nuevo", methods=["GET", "POST"])
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

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# ==========================================
# FACTURACIÓN
# ==========================================

@app.route("/facturacion")
def facturacion():

    return render_template("facturacion.html")


@app.route("/facturacion/nuevo", methods=["GET", "POST"])
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

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)