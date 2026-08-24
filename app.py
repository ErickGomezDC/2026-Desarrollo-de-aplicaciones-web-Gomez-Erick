from flask import Flask, render_template

app = Flask(__name__)


# ==================================================
# DATOS EN EJEMPLO DEL SISTEMA
# ==================================================

nombre_sistema = "Sistema de Gestión de Contenido Referencial"


# ==================================================
# PRODUCTOS / RECURSOS
# Lista en diccionarios
# ==================================================

productos_lista = [

    {
        "nombre": "Ilustración digital",
        "descripcion": "Referencia visual para proyectos de ilustración.",
        "categoria": "Ilustración",
        "estado": "Disponible"
    },

    {
        "nombre": "Video de animación",
        "descripcion": "Recurso audiovisual para estudiar movimiento.",
        "categoria": "Animación",
        "estado": "Disponible"
    },

    {
        "nombre": "Modelo 3D",
        "descripcion": "Referencia tridimensional para proyectos digitales.",
        "categoria": "Modelado 3D",
        "estado": "Agotado"
    }

]


# ==================================================
# CLIENTES
# Lista en diccionarios
# ==================================================

clientes_lista = [

    {
        "nombre": "Carlos Pérez",
        "correo": "carlos@email.com",
        "tipo": "Ilustrador"
    },

    {
        "nombre": "María González",
        "correo": "maria@email.com",
        "tipo": "Diseñadora"
    },

    {
        "nombre": "Juan Rodríguez",
        "correo": "juan@email.com",
        "tipo": "Animador"
    }

]


# ==================================================
# PROVEEDORES
# Lista en diccionarios
# ==================================================

proveedores_lista = [

    {
        "nombre": "Adobe",
        "servicio": "Software creativo",
        "estado": "Activo"
    },

    {
        "nombre": "Canva",
        "servicio": "Diseño gráfico",
        "estado": "Activo"
    },

    {
        "nombre": "Freepik",
        "servicio": "Recursos gráficos",
        "estado": "Activo"
    }

]


# ==================================================
# FACTURAS
# Lista en diccionarios
# ==================================================

facturas_lista = [

    {
        "numero": "FAC-001",
        "cliente": "Carlos Pérez",
        "total": 25.50,
        "estado": "Pagada"
    },

    {
        "numero": "FAC-002",
        "cliente": "María González",
        "total": 40.00,
        "estado": "Pendiente"
    },

    {
        "numero": "FAC-003",
        "cliente": "Juan Rodríguez",
        "total": 15.75,
        "estado": "Pagada"
    }

]


# ==================================================
# RUTA DE PRINCIPAL
# ==================================================

@app.route("/")
def inicio():

    return render_template(
        "index.html",
        nombre_sistema=nombre_sistema
    )


# ==================================================
# RUTA DE PRODUCTOS
# ==================================================

@app.route("/productos")
def productos():

    return render_template(
        "productos.html",
        productos=productos_lista,
        nombre_sistema=nombre_sistema
    )


# ==================================================
# RUTA DE CLIENTES
# ==================================================

@app.route("/clientes")
def clientes():

    return render_template(
        "clientes.html",
        clientes=clientes_lista,
        nombre_sistema=nombre_sistema
    )


# ==================================================
# RUTA DE PROVEEDORES
# ==================================================

@app.route("/proveedores")
def proveedores():

    return render_template(
        "proveedores.html",
        proveedores=proveedores_lista,
        nombre_sistema=nombre_sistema
    )


# ==================================================
# RUTA DE FACTURACIÓN
# ==================================================

@app.route("/facturacion")
def facturacion():

    return render_template(
        "facturacion.html",
        facturas=facturas_lista,
        nombre_sistema=nombre_sistema
    )


# ==================================================
# EJECUTAR LA APLICACIÓN
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)