import socket
import sys
import smtplib
import random
import string
from email.mime.text import MIMEText

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
    return data.decode()  # Decoding the bytes to string

def send_email(to_email, subject, body):
    from_email = "your_email@example.com"
    from_password = "your_email_password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL('smtp.example.com', 465)
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def handle_request(data):
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
    elif action == "LINKR":
        rut, email = payload.split(',')
        query = f"SELECT rut FROM Usuario_Cliente WHERE rut='{rut}'"
        db_response = send_message_to_dbs07(f"{len(query):05}DBS07{query}".encode())
        if "No data found" in db_response:
            password = generate_random_password()
            subject = "Invitación a registrarse en el sistema"
            body = f"Estimado cliente,\n\nPara completar su registro, utilice el siguiente RUT ({rut}) y la contraseña generada ({password}) en el siguiente enlace:\n\nhttp://example.com/registro\n\nGracias."
            email_response = send_email(email, subject, body)
            insert_query = f"INSERT INTO Usuario_Cliente (rut, email, password) VALUES ('{rut}', '{email}', '{password}')"
            db_insert_response = send_message_to_dbs07(f"{len(insert_query):05}DBS07{insert_query}".encode())
            return f"USR01OK,{email_response},{db_insert_response}"
        else:
            return "USR01OK,RUT already exists"
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
