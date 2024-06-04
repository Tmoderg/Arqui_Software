import socket
import psycopg2
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

def execute_query(query):
    try:
        connection = psycopg2.connect(
            database="opticommerce",
            user="postgres",
            password="7541",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        if query.strip().upper().startswith("SELECT"):
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            if result:
                return '|'.join([','.join(map(str, row)) for row in result])
            else:
                return "No data found"
        else:
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return "Query executed successfully"
    except (Exception, psycopg2.Error) as error:
        return str(error)

def handle_request(request):
    query = request
    print(f"Query: {query}")
    if query.startswith("INSERT") or query.startswith("UPDATE") or query.startswith("DELETE") or query.startswith("SELECT"):
        return execute_query(query)
    else:
        return "DBS07NKInvalid query type"

try:
    message = b'00010sinitDBS07'
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
            response = handle_request(data.decode()[5:])
            response_message = f"{len(response):05}DBS07OK{response}".encode()
            print('sending {!r}'.format(response_message))
            sock.sendall(response_message)
finally:
    print('closing socket')
    sock.close()
