from flask import Flask, render_template, redirect, url_for, flash
import sqlite3
import os

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "clave-secreta-proyecto-2026"


# ==========================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE = os.path.join(DATA_DIR, "ferreteria.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    os.makedirs(DATA_DIR, exist_ok=True)

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# INICIO
# ==========================================

@app.route("/")
def inicio():
    return render_template("index.html")


# ==========================================
# PRODUCTOS
# ==========================================

@app.route("/productos")
def productos():

    conn = get_db_connection()

    productos = conn.execute("""
        SELECT id, nombre, descripcion, precio
        FROM productos
        ORDER BY id ASC
    """).fetchall()

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
        precio = float(form.precio.data)

        conn = get_db_connection()

        conn.execute(
            """
            INSERT INTO productos
            (nombre, descripcion, precio)
            VALUES (?, ?, ?)
            """,
            (nombre, descripcion, precio)
        )

        conn.commit()
        conn.close()

        print("Producto guardado en SQLite:")
        print("Nombre:", nombre)
        print("Descripción:", descripcion)
        print("Precio:", precio)

        flash("Producto registrado correctamente.", "success")

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ==========================================
# ELIMINAR PRODUCTO
# ==========================================

@app.route("/productos/eliminar/<int:id>", methods=["POST"])
def eliminar_producto(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM productos WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Producto eliminado correctamente.", "success")

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

        flash("Cliente registrado correctamente.", "success")

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

        flash("Proveedor registrado correctamente.", "success")

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

        flash("Factura registrada correctamente.", "success")

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================

if __name__ == "__main__":

    init_db()

    app.run(debug=True)