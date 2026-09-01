from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm


app = Flask(__name__)

# ==========================================
# CONFIGURACIÓN DE FLASK-WTF Y CSRF
# ==========================================

app.config["SECRET_KEY"] = "clave-secreta-proyecto-2026"


# ==========================================
# LISTAS TEMPORALES
# Los datos se mantienen mientras Flask
# esté ejecutándose.
# ==========================================

productos_registrados = []

clientes_registrados = []

proveedores_registrados = []

facturas_registradas = []


# ==========================================
# RUTA PRINCIPAL
# ==========================================

@app.route("/")
def inicio():

    return render_template("index.html")


# ==========================================
# PRODUCTOS
# ==========================================

@app.route("/productos")
def productos():

    return render_template(
        "productos.html",
        productos=productos_registrados
    )


# ==========================================
# FORMULARIO DE PRODUCTOS
# ==========================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        producto = {
            "nombre": form.nombre.data,
            "descripcion": form.descripcion.data,
            "precio": form.precio.data
        }

        productos_registrados.append(producto)

        print("Producto recibido:")
        print("Nombre:", producto["nombre"])
        print("Descripción:", producto["descripcion"])
        print("Precio:", producto["precio"])

        flash("Producto registrado correctamente.", "success")

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ==========================================
# CLIENTES
# ==========================================

@app.route("/clientes")
def clientes():

    return render_template(
        "clientes.html",
        clientes=clientes_registrados
    )


# ==========================================
# FORMULARIO DE CLIENTES
# ==========================================

@app.route("/clientes/nuevo", methods=["GET", "POST"])
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        cliente = {
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data
        }

        clientes_registrados.append(cliente)

        print("Cliente recibido:")
        print("Nombre:", cliente["nombre"])
        print("Correo:", cliente["correo"])
        print("Teléfono:", cliente["telefono"])

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

    return render_template(
        "proveedores.html",
        proveedores=proveedores_registrados
    )


# ==========================================
# FORMULARIO DE PROVEEDORES
# ==========================================

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        proveedor = {
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "telefono": form.telefono.data
        }

        proveedores_registrados.append(proveedor)

        print("Proveedor recibido:")
        print("Nombre:", proveedor["nombre"])
        print("Correo:", proveedor["correo"])
        print("Teléfono:", proveedor["telefono"])

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

    return render_template(
        "facturacion.html",
        facturas=facturas_registradas
    )


# ==========================================
# FORMULARIO DE FACTURACIÓN
# ==========================================

@app.route("/facturacion/nuevo", methods=["GET", "POST"])
def formulario_facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        factura = {
            "cliente": form.cliente.data,
            "producto": form.producto.data,
            "cantidad": form.cantidad.data,
            "total": form.total.data
        }

        facturas_registradas.append(factura)

        print("Factura recibida:")
        print("Cliente:", factura["cliente"])
        print("Producto:", factura["producto"])
        print("Cantidad:", factura["cantidad"])
        print("Total:", factura["total"])

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
    app.run(debug=True)