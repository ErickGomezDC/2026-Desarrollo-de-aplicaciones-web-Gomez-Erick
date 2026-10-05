-- =========================================================
-- BASE DE DATOS
-- =========================================================

CREATE DATABASE sistema_referencial;


-- =========================================================
-- NOTA:
-- Después de crear la base de datos, seleccionar
-- "sistema_referencial" en pgAdmin antes de ejecutar
-- las siguientes tablas.
-- =========================================================


-- =========================================================
-- TABLA: USUARIOS
-- =========================================================

CREATE TABLE IF NOT EXISTS usuarios (

    id SERIAL PRIMARY KEY,

    usuario VARCHAR(50) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL

);


-- =========================================================
-- TABLA: PROVEEDORES
-- =========================================================

CREATE TABLE IF NOT EXISTS proveedores (

    id_proveedor SERIAL PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    correo VARCHAR(150),

    telefono VARCHAR(20)

);


-- =========================================================
-- TABLA: PRODUCTOS
-- =========================================================

CREATE TABLE IF NOT EXISTS productos (

    id_producto SERIAL PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    descripcion TEXT NOT NULL,

    precio NUMERIC(10,2) NOT NULL,

    id_proveedor INTEGER,

    CONSTRAINT fk_producto_proveedor

        FOREIGN KEY (id_proveedor)

        REFERENCES proveedores(id_proveedor)

);


-- =========================================================
-- TABLA: CLIENTES
-- =========================================================

CREATE TABLE IF NOT EXISTS clientes (

    id_cliente SERIAL PRIMARY KEY,

    nombre VARCHAR(100) NOT NULL,

    correo VARCHAR(150),

    telefono VARCHAR(20)

);


-- =========================================================
-- TABLA: FACTURAS
-- =========================================================

CREATE TABLE IF NOT EXISTS facturas (

    id_factura SERIAL PRIMARY KEY,

    id_cliente INTEGER NOT NULL,

    producto VARCHAR(100),

    cantidad INTEGER,

    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    total NUMERIC(10,2) NOT NULL,

    CONSTRAINT fk_factura_cliente

        FOREIGN KEY (id_cliente)

        REFERENCES clientes(id_cliente)

);