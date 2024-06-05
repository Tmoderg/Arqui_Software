import socket
import sys
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

def send_message_to_dbs07(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5000)
    sock.connect(bus_address)
    try:
        sock.sendall(message)
        print('sending {!r}'.format(message))
        amount_expected = int(sock.recv(5))
        amount_received = 0
        data = b''
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            data += chunk
    finally:
        sock.close()
    return data.decode()

def handle_request(data):
    action = data[:5]
    payload = data[5:]
    print(f"Action: {action}, Payload: {payload}")
    
    if action == "ADDPR":
        product = json.loads(payload)
        query = f"""
            INSERT INTO Producto (nombre, precio, cantidad, precio_descuento, descripcion) 
            VALUES ('{product['nombre']}', {product['precio']}, {product['cantidad']}, {product['precio_descuento']}, '{product['descripcion']}')
        """
        db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query.strip()}".encode())
        return f"PRD02OK,{db_response}"
    elif action == "DELPR":
        product_id = payload.strip()
        query = f"UPDATE Producto SET cantidad = 0 WHERE id_producto = {product_id}"
        db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
        return f"PRD02OK,{db_response}"
    elif action == "UPDPR":
        product = json.loads(payload)
        query = f"""
            UPDATE Producto 
            SET nombre='{product['nombre']}', precio={product['precio']}, cantidad={product['cantidad']}, 
                precio_descuento={product['precio_descuento']}, descripcion='{product['descripcion']}'
            WHERE id_producto={product['id_producto']}
        """
        db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query.strip()}".encode())
        return f"PRD02OK,{db_response}"
    elif action == "QRINF":
        product_id = payload.strip()
        query = f"SELECT nombre, precio, cantidad, precio_descuento, descripcion FROM Producto WHERE id_producto = {product_id}"
        db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
        return f"PRD02OK,{db_response}"
    elif action == "SRCHP":
        search_params = json.loads(payload)
        query = f"""
            SELECT id_producto, nombre, precio, cantidad, precio_descuento, descripcion 
            FROM Producto 
            WHERE nombre ILIKE '%{search_params.get('keyword', '')}%' 
            AND precio BETWEEN {search_params.get('min_price', 0)} AND {search_params.get('max_price', 9999999)}
        """
        db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query.strip()}".encode())
        return f"PRD02OK,{db_response}"
    elif action == "CHKST":
        product_id = payload.strip()
        query = f"SELECT cantidad, precio FROM Producto WHERE id_producto = {product_id}"
        db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
        return f"PRD02OK,{db_response}"
    elif action == "GETPR":
        query = "SELECT id_producto, nombre, precio, cantidad, precio_descuento, descripcion FROM Producto"
        db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
        return f"PRD02OK,{db_response}"
    else:
        return "PRD02NK,Invalid action"

try:
    message = b'00010sinitPRD02'
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
