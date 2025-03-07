import socket
import sys
import json
import cv2
import re

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
    except Exception as e:
        print(f"Error in send_message: {str(e)}")
        return "Error in send_message"
    finally:
        sock.close()
    return response.decode()

def validate_rut(rut):
    pattern = r'^\d{7,8}-[kK\d]$'
    return re.match(pattern, rut)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def validate_password(password):
    return len(password) <= 50

def admin_login():
    rut = input("Ingrese su RUT: ")
    if not validate_rut(rut):
        print("RUT inválido. Debe ser del formato 12345678-9.")
        return False
    password = input("Ingrese su contraseña: ")
    if not validate_password(password):
        print("Contraseña inválida. Debe tener menos de 50 caracteres.")
        return False
    data = f"{rut},{password}"
    response = send_message("USR01", "ADMLG", data)
    if response.startswith("USR01OK"):
        name = response.split(",")[1]
        if name == "Login failed":
            print("Inicio de sesión fallido")
            return False
        else:
            print(f"Bienvenido, {name[9:]}")
            return True
    else:
        print("Inicio de sesión fallido")
        return False

def add_product():
    product = {
        "nombre": input("Ingrese nombre del producto: "),
        "precio": int(input("Ingrese precio del producto: ")),
        "cantidad": int(input("Ingrese cantidad del producto: ")),
        "precio_descuento": int(input("Ingrese precio de descuento del producto: ")),
        "descripcion": input("Ingrese descripción del producto: ")
    }
    data = json.dumps(product)
    response = send_message("PRD02", "ADDPR", data)
    print(f"Respuesta: {response}")

def delete_product():
    product_id = input("Ingrese ID del producto a eliminar: ")
    response = send_message("PRD02", "DELPR", product_id)
    print(f"Respuesta: {response}")

def update_product():
    product = {
        "id_producto": int(input("Ingrese ID del producto: ")),
        "nombre": input("Ingrese nombre del producto: "),
        "precio": int(input("Ingrese precio del producto: ")),
        "cantidad": int(input("Ingrese cantidad del producto: ")),
        "precio_descuento": int(input("Ingrese precio de descuento del producto: ")),
        "descripcion": input("Ingrese descripción del producto: ")
    }
    data = json.dumps(product)
    response = send_message("PRD02", "UPDPR", data)
    print(f"Respuesta: {response}")

def qr_info():
    product_id = input("Ingrese ID del producto: ")
    response = send_message("PRD02", "QRINF", product_id)
    print(f"Respuesta: {response}")

def scan_qr():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            print(f"QR Code detected: {data}")
            response = send_message("PRD02", "QRINF", data)
            response = response.split("PRD02OKOK,DBS07OKOK")[1]
            response = response.split(",")
            print(f"Nombre: {response[0]}, Precio: {response[1]}, Cantidad: {response[2]}, Precio Descuento: {response[3]}, Descripción: {response[4]}")
            break

        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

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
    except (IndexError, ValueError) as e:
        print(f"Error al procesar la respuesta del servidor: {str(e)}")

def link_user_product():
    new_or_existing = input("¿Es un cliente nuevo o existente? (nuevo/existente): ").strip().lower()
    if new_or_existing not in ["nuevo", "existente"]:
        print("Opción no válida. Debe ser 'nuevo' o 'existente'.")
        return

    if new_or_existing == "nuevo":
        rut = input("Ingrese RUT del cliente: ")
        if not validate_rut(rut):
            print("RUT inválido. Debe ser del formato 12345678-9.")
            return
        email = input("Ingrese email del cliente: ")
        if not validate_email(email):
            print("Email inválido. Debe ser un email válido.")
            return
        id_producto = input("Ingrese ID del producto: ")
        data = f"new,{rut},{email},{id_producto}"
    else:
        rut = input("Ingrese RUT del cliente: ")
        if not validate_rut(rut):
            print("RUT inválido. Debe ser del formato 12345678-9.")
            return
        email = input("Ingrese email del cliente: ")
        if not validate_email(email):
            print("Email inválido. Debe ser un email válido.")
            return
        id_producto = input("Ingrese ID del producto: ")
        data = f"existing,{rut},{email},{id_producto}"

    response = send_message("USR01", "LINKR", data)
    print(f"Respuesta: {response}")

try:
    if not admin_login():
        sys.exit()

    while True:
        print("Menú de opciones del Administrador:")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Ver productos")
        print("5. Escanear QR de producto")
        print("6. Asociar cliente y producto")
        print("7. Salir")
        option = input("Seleccione una opción: ")
        if option == "1":
            add_product()
        elif option == "2":
            delete_product()
        elif option == "3":
            update_product()
        elif option == "4":
            view_products()
        elif option == "5":
            scan_qr()
        elif option == "6":
            link_user_product()
        elif option == "7":
            break
        else:
            print("Opción no válida")
finally:
    print('Saliendo del cliente administrador')
