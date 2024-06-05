# Arqui_Software

# Servicios y sus requerimientos
USR01 -> 1, 7
PRD02 -> 4, 5, 6, 8, 10
CMP03 -> 3, 9, 11
DSC04 -> 2
NOT05 -> 12
SRC06 -> 6, 8
DBS07 -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12

# Requerimientos listos
USR01 -> 1, 7
PRD02 -> 4, 5, 6, 8, 10
CMP03 -> 
DSC04 -> 
NOT05 -> 
SRC06 -> 
DBS07 -> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12

Comandos para Probar los Clientes
Ejecuta el bus de servicios en Docker:
docker run -d -p 5000:5000 jrgiadach/soabus:v1

Inicia el servicio de Gestión de Usuarios (USR01):
python usr01_service.py

Inicia el servicio de Gestión de Productos (PRD02):
python prd02_service.py

Inicia el servicio de Acceso a la Base de Datos (DBS07):
python dbs07_service.py

Ejecuta el cliente normal:
python cliente_normal.py

Ejecuta el cliente administrador:
python cliente_administrador.py

# Documentación del Proceso Cliente y Servicios Implementados

## Cliente Administrador (`cliente_administrador.py`)

**Descripción**: El cliente administrador permite a los usuarios con permisos de administración gestionar productos en el sistema. Las funcionalidades incluyen agregar, eliminar, actualizar productos, ver productos y escanear códigos QR para obtener información del producto.

**Requerimientos Satisfechos**:
1. **Gestión de Inventario**: Agregar, eliminar y actualizar productos.
2. **Escaneo de Códigos QR**: Escaneo de códigos QR para obtener información del producto.
3. **Visualización de Productos**: Ver todos los productos disponibles en el inventario.

**Funciones Principales**:
- `add_product()`: Permite al administrador agregar un nuevo producto al inventario.
- `delete_product()`: Permite al administrador eliminar un producto del inventario.
- `update_product()`: Permite al administrador actualizar la información de un producto.
- `qr_info()`: Permite al administrador obtener información de un producto mediante su ID.
- `scan_qr()`: Permite al administrador escanear un código QR para obtener información del producto.
- `view_products()`: Permite al administrador ver todos los productos disponibles en el inventario, ordenados por nombre.

**Evidencia de Funcionamiento**:
Capturas de pantalla o registros de consola que muestren la adición, eliminación, actualización, visualización de productos y el uso del escáner QR.

## Cliente Normal (`cliente_normal.py`)

**Descripción**: El cliente normal permite a los usuarios sin permisos de administración interactuar con el sistema para registrarse, iniciar sesión, y ver información de productos.

**Requerimientos Satisfechos**:
1. **Registro de Usuario**: Permite a los usuarios registrarse en el sistema.
2. **Inicio de Sesión**: Permite a los usuarios iniciar sesión en el sistema.
3. **Actualización de Perfil**: Permite a los usuarios actualizar su perfil.
4. **Visualización de Productos**: Permite a los usuarios ver y buscar productos en el inventario.

**Funciones Principales**:
- `create_user()`: Permite al usuario registrarse en el sistema.
- `update_user()`: Permite al usuario actualizar su perfil.
- `login()`: Permite al usuario iniciar sesión en el sistema.
- `search_products()`: Permite al usuario buscar productos en el inventario.
- `check_stock()`: Permite al usuario consultar la disponibilidad y precio de un producto.
- `view_products()`: Permite al usuario ver todos los productos disponibles en el inventario.

**Evidencia de Funcionamiento**:
Capturas de pantalla o registros de consola que muestren el registro, inicio de sesión, actualización de perfil y la visualización de productos.

## Servicio de Gestión de Usuarios (`usr01_service.py`)

**Descripción**: Este servicio maneja la creación, actualización, inicio de sesión y verificación de usuarios.

**Requerimientos Satisfechos**:
1. **Registro de Usuarios**: Permite crear usuarios normales.
2. **Actualización de Usuarios**: Permite actualizar la información de los usuarios.
3. **Inicio de Sesión de Usuarios**: Permite a los usuarios iniciar sesión en el sistema.

**Funciones Principales**:
- `handle_request(data)`: Maneja las solicitudes de creación, actualización, inicio de sesión y verificación de usuarios.
- `send_message_to_dbs07(message)`: Envía consultas al servicio de base de datos.

**Evidencia de Funcionamiento**:
Capturas de pantalla o registros de consola que muestren la creación, actualización, inicio de sesión y verificación de usuarios.

## Servicio de Gestión de Productos (`prd02_service.py`)

**Descripción**: Este servicio maneja la gestión de productos en el sistema, incluyendo la adición, eliminación, actualización, visualización y consulta de productos por código QR.

**Requerimientos Satisfechos**:
1. **Gestión de Inventario**: Agregar, eliminar y actualizar productos.
2. **Visualización de Productos**: Ver todos los productos disponibles en el inventario.
3. **Escaneo de Códigos QR**: Obtener información de productos mediante códigos QR.

**Funciones Principales**:
- `handle_request(data)`: Maneja las solicitudes de gestión de productos.
- `send_message_to_dbs07(message)`: Envía consultas al servicio de base de datos.

**Evidencia de Funcionamiento**:
Capturas de pantalla o registros de consola que muestren la adición, eliminación, actualización, visualización y consulta de productos por código QR.

## Servicio de Base de Datos (`dbs07_service.py`)

**Descripción**: Este servicio se encarga de ejecutar consultas SQL en la base de datos para satisfacer las solicitudes de otros servicios.

**Requerimientos Satisfechos**:
1. **Ejecución de Consultas SQL**: Ejecuta consultas de inserción, actualización, eliminación y selección en la base de datos.

**Funciones Principales**:
- `execute_query(query)`: Ejecuta consultas SQL y retorna los resultados.
- `handle_request(request)`: Maneja las solicitudes de ejecución de consultas SQL.