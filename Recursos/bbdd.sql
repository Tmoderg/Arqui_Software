-- Crea la base de datos
CREATE DATABASE opticommerce;

-- Conéctate a la base de datos opticommerce antes de ejecutar las siguientes líneas
-- Esto debe hacerse manualmente en la terminal de PostgreSQL o en pgAdmin4
-- \c opticommerce

-- Crea las tablas
CREATE TABLE Usuario_Cliente (
    rut VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    email VARCHAR(30),
    direccion VARCHAR(50),
    password VARCHAR(20),
    celular VARCHAR(20)
);

CREATE TABLE Usuario_Administrador (
    rut VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    email VARCHAR(30),
    password VARCHAR(50)
);

CREATE TABLE Producto (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(20),
    precio INT,
    cantidad INT,
    precio_descuento INT,
    descripcion TEXT
);

CREATE TABLE Orden (
    id_orden SERIAL PRIMARY KEY,
    rut VARCHAR(10) REFERENCES Usuario_Cliente(rut),
    id_producto INT REFERENCES Producto(id_producto),
    costo INT,
    estado VARCHAR(20),
    fecha DATE
);
