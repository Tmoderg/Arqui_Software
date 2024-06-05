import socket
import sys
import random
import string

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

def send_message_to_dbs07(message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bus_address = ('localhost', 5000)
        sock.connect(bus_address)
        sock.sendall(message)
        print('sending {!r}'.format(message))
        amount_expected = int(sock.recv(5))
        amount_received = 0
        data = b''
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            data += chunk
    except Exception as e:
        print(f"Error in send_message_to_dbs07: {str(e)}")
        return "DBS07NK,Error"
    finally:
        sock.close()
    return data.decode()

def simulate_send_email(email, password):
    print(f"Simulating sending email to {email} with password {password}")
    return "Email sent successfully"

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def handle_request(data):
    try:
        action = data[:5]
        payload = data[5:]
        print(f"Action: {action}, Payload: {payload}")
        if action == "CREAT":
            rut, name, apellido, email, direccion, password, celular = payload.split(',')
            query = f"INSERT INTO Usuario_Cliente (rut, nombre, apellido, email, direccion, password, celular) VALUES ('{rut}', '{name}', '{apellido}', '{email}', '{direccion}', '{password}', '{celular}')"
            db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
            return f"USR01OK{db_response}"
        elif action == "UPDAT":
            rut, name, apellido, email, direccion, password, celular = payload.split(',')
            check_email_query = f"SELECT rut FROM Usuario_Cliente WHERE email='{email}' AND rut!='{rut}'"
            email_check_response = send_message_to_dbs07(f"{len(check_email_query):05}DBS07{check_email_query}".encode())
            if "No data found" not in email_check_response:
                return "USR01NK,Email already in use"
            query = f"UPDATE Usuario_Cliente SET nombre='{name}', apellido='{apellido}', email='{email}', direccion='{direccion}', password='{password}', celular='{celular}' WHERE rut='{rut}'"
            db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
            return f"USR01OK{db_response}"
        elif action == "LOGIN":
            rut, password = payload.split(',')
            query = f"SELECT nombre, password FROM Usuario_Cliente WHERE rut='{rut}'"
            db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
            if "No data found" in db_response or "DBS07NK" in db_response:
                return "USR01NK,Login failed"
            else:
                name, db_password = db_response.split(',')
                if password == db_password:
                    return f"USR01OK,{name}"
                else:
                    return "USR01NK,Login failed"
        elif action == "ADMLG":
            rut, password = payload.split(',')
            query = f"SELECT nombre, password FROM Usuario_Administrador WHERE rut='{rut}'"
            db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
            if "No data found" in db_response or "DBS07NK" in db_response:
                return "USR01NK,Login failed"
            else:
                name, db_password = db_response.split(',')
                if password == db_password:
                    return f"USR01OK,{name}"
                else:
                    return "USR01NK,Login failed"
        elif action == "LINKR":
            option, rut, email, id_producto = payload.split(',')
            if option == "new":
                query = f"SELECT rut FROM Usuario_Cliente WHERE rut='{rut}' AND email='{email}'"
                db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
                if "No data found" in db_response:
                    password = generate_random_password()
                    email_response = simulate_send_email(email, password)
                    insert_query = f"INSERT INTO Usuario_Cliente (rut, email, password) VALUES ('{rut}', '{email}', '{password}')"
                    db_insert_response = send_message_to_dbs07(f"{len(insert_query):05}DBS07{insert_query}".encode())
                else:
                    db_insert_response = "User already exists"
            else:  # Existing client
                query = f"SELECT rut FROM Usuario_Cliente WHERE rut='{rut}' AND email='{email}'"
                db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
                if "No data found" in db_response:
                    return "USR01NK,User does not exist"
                db_insert_response = "User exists"

            # Verificar stock
            stock_query = f"SELECT cantidad FROM Producto WHERE id_producto={id_producto}"
            stock_response = send_message_to_dbs07(f"{len(stock_query):05}DBS07{stock_query}".encode())
            stock_count = int(stock_response.split("DBS07OKOK")[1])
            if stock_count < 1:
                return "USR01NK,Insufficient stock"

            # Descontar stock
            update_stock_query = f"UPDATE Producto SET cantidad = cantidad - 1 WHERE id_producto={id_producto}"
            update_stock_response = send_message_to_dbs07(f"{len(update_stock_query):05}DBS07{update_stock_query}".encode())

            # Insertar en la tabla de órdenes
            insert_order_query = f"INSERT INTO Orden (rut, id_producto, costo, estado, fecha) VALUES ('{rut}', {id_producto}, (SELECT precio FROM Producto WHERE id_producto={id_producto}), 'pendiente', NOW())"
            db_insert_order_response = send_message_to_dbs07(f"{len(insert_order_query):05}DBS07{insert_order_query}".encode())

            return f"USR01OK,Email enviado con su contraseña y pedido realizado al correo {email},{db_insert_response},{db_insert_order_response}"
        elif action == "CHKRT":
            query = f"SELECT rut FROM Usuario_Cliente WHERE rut='{payload}'"
            db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
            if "No data found" in db_response:
                return "USR01OK,RUT does not exist"
            else:
                return "USR01OK,RUT exists"
        elif action == "CHKEM":
            query = f"SELECT email FROM Usuario_Cliente WHERE email='{payload}'"
            db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
            if "No data found" in db_response:
                return "USR01OK,Email does not exist"
            else:
                return "USR01OK,Email exists"
        else:
            return "USR01NK,Invalid action"
    except Exception as e:
        print(f"Error handling request: {str(e)}")
        return "USR01NK,Error handling request"

try:
    message = b'00010sinitUSR01'
    print('sending {!r}'.format(message))
    sock.sendall(message)
    sinit = 1
    while True:
        print("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
        print("Processing ...")
        print('received {!r}'.format(data))
        if sinit == 1:
            sinit = 0
            print('Received sinit answer')
        else:
            print("Send answer")
            data = data.decode()[5:]  # Remove the first 5 characters (service name)
            response = handle_request(data)
            response_message = f"{len(response):05}{response}".encode()
            print('sending {!r}'.format(response_message))
            sock.sendall(response_message)
finally:
    print('closing socket')
    sock.close()
