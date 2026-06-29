// Obtener elementos del HTML

const formulario = document.getElementById("formReferencia");
const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const mensaje = document.getElementById("mensaje");
const listaReferencias = document.getElementById("listaReferencias");
const total = document.getElementById("total");

let contador = 0;

// Evento del formulario

formulario.addEventListener("submit", function(event){

    // Evita que la página se recargue

    event.preventDefault();

    // Validación

    if(
        nombre.value.trim() === "" ||
        descripcion.value.trim() === "" ||
        categoria.value === ""
    ){

        mensaje.className = "text-danger mt-3";
        mensaje.textContent = "Todos los campos son obligatorios.";

        return;

    }

    // Borra el mensaje de error

    mensaje.className = "text-success mt-3";
    mensaje.textContent = "Referencia agregada correctamente.";

    // Crear columna

    const columna = document.createElement("div");

    columna.className = "col-md-4 mt-4";

    // Crear tarjeta

    const tarjeta = document.createElement("div");

    tarjeta.className = "card shadow p-3 h-100";

    // Título

    const titulo = document.createElement("h4");

    titulo.textContent = nombre.value;

    // Descripción

    const texto = document.createElement("p");

    texto.textContent = descripcion.value;

    // Categoría

    const tipo = document.createElement("span");

    tipo.className = "badge bg-primary mb-3";

    tipo.textContent = categoria.value;

    // Botón eliminar

    const botonEliminar = document.createElement("button");

    botonEliminar.className = "btn btn-danger";

    botonEliminar.textContent = "Eliminar";

    // Evento eliminar

    botonEliminar.addEventListener("click", function(){

        listaReferencias.removeChild(columna);

        contador--;

        total.textContent = contador;

    });

    // Agregar elementos

    tarjeta.appendChild(titulo);
    tarjeta.appendChild(texto);
    tarjeta.appendChild(tipo);
    tarjeta.appendChild(botonEliminar);

    columna.appendChild(tarjeta);

    listaReferencias.appendChild(columna);

    // Actualizar contador

    contador++;

    total.textContent = contador;

    // Limpiar formulario

    formulario.reset();

});