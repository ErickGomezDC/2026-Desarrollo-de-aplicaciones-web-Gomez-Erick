from flask import Flask, render_template

# APLICACIÓN FLASK---

app = Flask(__name__)

# RUTA PRINCIPAL---

@app.route("/")
def inicio():

    return render_template("index.html")


# RUTA PRODUCTOS---

@app.route("/productos")
def productos():

    return render_template("productos.html")


# RUTA CLIENTES---

@app.route("/clientes")
def clientes():

    return render_template("clientes.html")


# RUTA PROVEEDORES---

@app.route("/proveedores")
def proveedores():

    return render_template("proveedores.html")


# RUTA FACTURACIÓN---

@app.route("/facturacion")
def facturacion():

    return render_template("facturacion.html")

# EJECUTAR APLICACIÓN---

if __name__ == "__main__":

    app.run(debug=True)