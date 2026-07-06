// ===============================
// OBTENER ELEMENTOS DEL HTML
// ===============================

const formulario = document.getElementById("formReferencia");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

const mensaje = document.getElementById("mensaje");
const listaReferencias = document.getElementById("listaReferencias");
const total = document.getElementById("total");

let contador = 0;


// ===============================
// VALIDAR NOMBRE
// ===============================

function validarNombre(){

    if(nombre.value.trim() === ""){

        nombre.classList.remove("is-valid");
        nombre.classList.add("is-invalid");

        errorNombre.className = "text-danger";

        errorNombre.textContent = "El nombre es obligatorio.";

        return false;

    }

    if(nombre.value.trim().length < 3){

        nombre.classList.remove("is-valid");
        nombre.classList.add("is-invalid");

        errorNombre.className = "text-danger";

        errorNombre.textContent = "Debe tener al menos 3 caracteres.";

        return false;

    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    errorNombre.className = "text-success";

    errorNombre.textContent = "Nombre válido.";

    return true;

}


// ===============================
// VALIDAR DESCRIPCIÓN
// ===============================

function validarDescripcion(){

    if(descripcion.value.trim() === ""){

        descripcion.classList.remove("is-valid");
        descripcion.classList.add("is-invalid");

        errorDescripcion.className = "text-danger";

        errorDescripcion.textContent = "La descripción es obligatoria.";

        return false;

    }

    if(descripcion.value.trim().length < 15){

        descripcion.classList.remove("is-valid");
        descripcion.classList.add("is-invalid");

        errorDescripcion.className = "text-danger";

        errorDescripcion.textContent = "Debe contener al menos 15 caracteres.";

        return false;

    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    errorDescripcion.className = "text-success";

    errorDescripcion.textContent = "Descripción válida.";

    return true;

    
}

// ===============================
// VALIDAR CATEGORÍA
// ===============================

function validarCategoria(){

    if(categoria.value === ""){

        categoria.classList.remove("is-valid");
        categoria.classList.add("is-invalid");

        errorCategoria.className = "text-danger";

        errorCategoria.textContent = "Seleccione una categoría.";

        return false;

    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    errorCategoria.className = "text-success";

    errorCategoria.textContent = "Categoría válida.";

    return true;

}


// ===============================
// EVENTOS EN TIEMPO REAL
// ===============================

nombre.addEventListener("input", validarNombre);

nombre.addEventListener("blur", validarNombre);

descripcion.addEventListener("input", validarDescripcion);

descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);

categoria.addEventListener("blur", validarCategoria);


// ===============================
// ENVÍO DEL FORMULARIO
// ===============================

formulario.addEventListener("submit", function(event){

    event.preventDefault();

    let nombreCorrecto = validarNombre();

    let descripcionCorrecta = validarDescripcion();

    let categoriaCorrecta = validarCategoria();

    if(
        !nombreCorrecto ||
        !descripcionCorrecta ||
        !categoriaCorrecta
    ){

        mensaje.className = "alert alert-danger mt-3";

        mensaje.textContent =
        "Corrija los errores antes de registrar la información.";

        return;

    }

    mensaje.className = "alert alert-success mt-3";

    mensaje.textContent =
    "Referencia agregada correctamente.";
        // ===============================
    // CREAR COLUMNA
    // ===============================

    const columna = document.createElement("div");

    columna.className = "col-md-6 col-lg-4 mt-4";


    // ===============================
    // CREAR TARJETA
    // ===============================

    const tarjeta = document.createElement("div");

    tarjeta.className = "card shadow p-3 h-100";


    // ===============================
    // TÍTULO
    // ===============================

    const titulo = document.createElement("h4");

    titulo.textContent = nombre.value;


    // ===============================
    // DESCRIPCIÓN
    // ===============================

    const texto = document.createElement("p");

    texto.textContent = descripcion.value;


    // ===============================
    // CATEGORÍA
    // ===============================

    const tipo = document.createElement("span");

    tipo.className = "badge bg-warning text-dark mb-3";

    tipo.textContent = categoria.value;


    // ===============================
    // BOTÓN ELIMINAR
    // ===============================

    const botonEliminar = document.createElement("button");

    botonEliminar.className = "btn btn-danger mt-2";

    botonEliminar.textContent = "Eliminar";


    botonEliminar.addEventListener("click", function(){

        listaReferencias.removeChild(columna);

        contador--;

        total.textContent = contador;

    });


    // ===============================
    // AGREGAR ELEMENTOS
    // ===============================

    tarjeta.appendChild(titulo);
    tarjeta.appendChild(texto);
    tarjeta.appendChild(tipo);
    tarjeta.appendChild(botonEliminar);

    columna.appendChild(tarjeta);

    listaReferencias.appendChild(columna);


    // ===============================
    // ACTUALIZAR CONTADOR
    // ===============================

    contador++;

    total.textContent = contador;


    // ===============================
    // LIMPIAR FORMULARIO
    // ===============================

    formulario.reset();


    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

    nombre.classList.remove("is-invalid");
    descripcion.classList.remove("is-invalid");
    categoria.classList.remove("is-invalid");
    

    errorNombre.textContent = "";
    errorDescripcion.textContent = "";
    errorCategoria.textContent = "";

});