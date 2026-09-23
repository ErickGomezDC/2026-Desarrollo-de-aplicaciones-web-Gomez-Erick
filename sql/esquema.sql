-- BASE DE DATOS DEL PROYECTO

CREATE DATABASE IF NOT EXISTS sistema_referencial;

USE sistema_referencial;


-- TABLA: PROVEEDORES

CREATE TABLE IF NOT EXISTS proveedores (

    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    correo VARCHAR(150),

    telefono VARCHAR(20)

);


-- TABLA: PRODUCTOS

CREATE TABLE IF NOT EXISTS productos (

    id_producto INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    descripcion TEXT NOT NULL,

    precio DECIMAL(10,2) NOT NULL,

    id_proveedor INT,

    FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)

);


-- TABLA: CLIENTES

CREATE TABLE IF NOT EXISTS clientes (

    id_cliente INT AUTO_INCREMENT PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    correo VARCHAR(150),

    telefono VARCHAR(20)

);


-- TABLA: FACTURAS

CREATE TABLE IF NOT EXISTS facturas (

    id_factura INT AUTO_INCREMENT PRIMARY KEY,

    id_cliente INT NOT NULL,

    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,

    total DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)

);


-- TABLA: USUARIOS

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);