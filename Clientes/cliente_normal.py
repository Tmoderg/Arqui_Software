import socket
import sys
import re
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

def send_message(service, action, data):
    message_data = f"{action}{data}"
    message = f"{len(message_data):05}{service}{message_data}".encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5000)
    sock.connect(bus_address)
    try:
        sock.sendall(message)
        amount_expected = int(sock.recv(5))
        amount_received = 0
        response = b''
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            response += chunk
    finally:
        sock.close()
    return response.decode()

def validate_rut(rut):
    pattern = r'^\d{7,8}-[kK\d]$'
    return re.match(pattern, rut)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)
    
def validate_name(name):
    return re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]{1,20}$', name) is not None

def validate_password(password):
    return re.match(r'^.{1,20}$', password) is not None

def validate_celular(celular):
    return re.match(r'^\+569\d{8}$', celular) is not None

def validate_direccion(direccion):
    return re.match(r'^[^,]{1,50}$', direccion) is not None

def prompt_for_input(prompt, validation_func, error_message):
    while True:
        value = input(prompt)
        if validation_func(value):
            return value
        print(error_message)

def create_user():
    rut = prompt_for_input("Ingrese RUT (formato: 12345678-9): ", validate_rut, "RUT inválido. Debe ser del formato 12345678-9.")
    name = prompt_for_input("Ingrese nombre: ", validate_name, "Nombre inválido. Solo puede contener letras, tildes y espacios, y hasta 20 caracteres.")
    apellido = prompt_for_input("Ingrese apellido: ", validate_name, "Apellido inválido. Solo puede contener letras, tildes y espacios, y hasta 20 caracteres.")
    email = prompt_for_input("Ingrese email: ", validate_email, "Email inválido. Debe ser un correo electrónico válido.")
    direccion = prompt_for_input("Ingrese direccion: ", validate_direccion, "Dirección inválida. No debe contener comas y no debe superar los 50 caracteres.")
    password = prompt_for_input("Ingrese contraseña (1-20 caracteres): ", validate_password, "Contraseña inválida. Debe tener entre 1 y 20 caracteres.")
    celular = prompt_for_input("Ingrese celular (formato: +569XXXXXXXX): ", validate_celular, "Celular inválido. Debe ser del formato +569XXXXXXXX.")
    data = f"{rut},{name},{apellido},{email},{direccion},{password},{celular}"
    response = send_message("USR01", "CREAT", data)
    print(f"Respuesta: {response}")

def update_user(logged_in_rut):
    name = prompt_for_input("Ingrese nombre: ", validate_name, "Nombre inválido. Solo puede contener letras, tildes y espacios, y hasta 20 caracteres.")
    apellido = prompt_for_input("Ingrese apellido: ", validate_name, "Apellido inválido. Solo puede contener letras, tildes y espacios, y hasta 20 caracteres.")
    email = prompt_for_input("Ingrese email: ", validate_email, "Email inválido. Debe ser un correo electrónico válido.")
    direccion = prompt_for_input("Ingrese direccion: ", validate_direccion, "Dirección inválida. No debe contener comas y no debe superar los 50 caracteres.")
    password = prompt_for_input("Ingrese contraseña (1-20 caracteres): ", validate_password, "Contraseña inválida. Debe tener entre 1 y 20 caracteres.")
    celular = prompt_for_input("Ingrese celular (formato: +569XXXXXXXX): ", validate_celular, "Celular inválido. Debe ser del formato +569XXXXXXXX.")
    data = f"{logged_in_rut},{name},{apellido},{email},{direccion},{password},{celular}"
    response = send_message("USR01", "UPDAT", data)
    print(f"Respuesta: {response}")
    if "USR01NK,Email already in use" in response:
        print("El correo electrónico ya está en uso por otro usuario. Intente con uno diferente.")

def login():
    rut = prompt_for_input("Ingrese RUT: ", validate_rut, "RUT inválido. Debe ser del formato 12345678-9.")
    password = prompt_for_input("Ingrese contraseña: ", validate_password, "Contraseña inválida. Debe tener entre 1 y 20 caracteres.")
    data = f"{rut},{password}"
    response = send_message("USR01", "LOGIN", data)
    if "USR01OK" in response:
        print("Inicio de sesión exitoso")
        name = response.split(",")[1] if "," in response else ""
        return rut, name
    else:
        print("Inicio de sesión fallido")
        return None, None

def search_products():
    search_params = {
        "keyword": input("Ingrese palabra clave: "),
        "min_price": int(input("Ingrese precio mínimo: ")),
        "max_price": int(input("Ingrese precio máximo: "))
    }
    data = json.dumps(search_params)
    response = send_message("PRD02", "SRCHP", data)
    try:
        if response.startswith("PRD02OK"):
            products_data = response.split("PRD02OKOK,DBS07OKOK")[1]
            print("Products data: ", products_data)
            products = [item.split(",") for item in products_data.split("|")]
            for product in products:
                print(f"ID: {product[0]}, Nombre: {product[1]}, Precio: {product[2]}, Cantidad: {product[3]}, Precio Descuento: {product[4]}, Descripción: {product[5]}")
        else:
            print("Error en la respuesta del servidor")
    except (IndexError, ValueError) as e:
        print(f"Error al procesar la respuesta del servidor: {str(e)}")


def check_stock():
    product_id = input("Ingrese ID del producto: ")
    response = send_message("PRD02", "CHKST", product_id)
    response = response.split("PRD02OKOK,DBS07OKOK")[1]
    #Separar por comas, primer valor es stock, segundo es precio
    response = response.split(",")
    #Si responsos[0] es 0, no hay stock
    if response[0] == "0":
        print("Producto sin stock")
    else:
        print(f"Stock: {response[0]}, Precio: {response[1]}")

def view_products():
    response = send_message("PRD02", "GETPR", "")
    try:
        if response.startswith("PRD02OK"):
            products_data = response.split("PRD02OKOK,DBS07OKOK")[1]
            print("Products data: ", products_data)       
            products = [item.split(",") for item in products_data.split("|")]
            sorted_products = sorted(products, key=lambda x: x[1])  # Ordenar por nombre del producto
            for product in sorted_products:
                print(f"ID: {product[0]}, Nombre: {product[1]}, Precio: {product[2]}, Cantidad: {product[3]}, Precio Descuento: {product[4]}, Descripción: {product[5]}")
        else:
            print("Error en la respuesta del servidor")
    except (IndexError, ValueError):
        print("Error al procesar la respuesta del servidor")

try:
    logged_in_rut = None
    logged_in_name = None
    while True:
        if logged_in_rut:
            print(f"Hola, {logged_in_name[9:]}!")
            print("Menú de opciones:")
            print("1. Actualizar perfil")
            print("2. Buscar productos")
            print("3. Consultar disponibilidad y precio de producto")
            print("4. Ver productos")
            print("5. Cerrar sesión")
            option = input("Seleccione una opción: ")
            if option == "1":
                update_user(logged_in_rut)
            elif option == "2":
                search_products()
            elif option == "3":
                check_stock()
            elif option == "4":
                view_products()
            elif option == "5":
                logged_in_rut = None
                logged_in_name = None
                print("Sesión cerrada")
            else:
                print("Opción no válida")
        else:
            print("Menú de opciones:")
            print("1. Crear usuario")
            print("2. Iniciar sesión")
            print("3. Salir")
            option = input("Seleccione una opción: ")
            if option == "1":
                create_user()
            elif option == "2":
                logged_in_rut, logged_in_name = login()
            elif option == "3":
                break
            else:
                print("Opción no válida")
finally:
    print('Cerrando el cliente normal')
