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

-- Inserta un administrador
INSERT INTO Usuario_Administrador (rut, nombre, apellido, email, password)
VALUES ('12345678-9', 'Admin', 'User', 'admin@example.com', 'password123');

-- Inserta productos ficticios
INSERT INTO Producto (nombre, precio, cantidad, precio_descuento, descripcion)
VALUES 
('Lentes de Sol', 50000, 10, 45000, 'Lentes de sol polarizados'),
('Lentes de Lectura', 30000, 15, 25000, 'Lentes de lectura con aumento'),
('Lentes de Contacto', 20000, 20, 18000, 'Lentes de contacto diarios'),
('Gafas Deportivas', 60000, 5, 55000, 'Gafas deportivas para ciclismo'),
('Lentes para Computadora', 40000, 12, 35000, 'Lentes con filtro de luz azul'),
('Lentes de Moda', 35000, 8, 30000, 'Lentes de moda con marco de acetato'),
('Lentes de Seguridad', 25000, 20, 22000, 'Lentes de seguridad industrial'),
('Lentes de Niños', 30000, 10, 27000, 'Lentes de sol para niños'),
('Lentes Bifocales', 45000, 7, 40000, 'Lentes bifocales para visión de cerca y de lejos'),
('Lentes Progresivos', 70000, 4, 65000, 'Lentes progresivos sin línea de bifocalidad');
