import socket

def send_request(service_name, data):
    message = f"{len(data):05}{service_name}{data}"
    print(f"Sending request: {message}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 5000))
        s.sendall(message.encode())
        response = s.recv(1024)
    print(f"Received response: {response.decode()}")
    return response.decode()

class ClienteNormal:
    def __init__(self, rut, name, email, password):
        self.rut = rut
        self.name = name
        self.email = email
        self.password = password

    def crear_cuenta(self):
        data = f"Crear,{self.rut},{self.name},{self.email},{self.password}"
        response = send_request('usr01', data)
        print("Crear Cuenta Response:", response)

    def realizar_compra(self, product_list, payment_method):
        query = f"INSERT INTO Orden (rut, id_producto, costo, estado, fecha) VALUES ('{self.rut}', {product_list}, 100, 'pendiente', CURRENT_DATE)"
        data = f"Insert{query}"
        response = send_request('dbs07', data)
        print("Realizar Compra Response:", response)

    def consultar_historial(self):
        query = f"SELECT * FROM Orden WHERE rut = '{self.rut}'"
        data = f"Query{query}"
        response = send_request('dbs07', data)
        print("Consultar Historial Response:", response)

    def menu(self):
        while True:
            print("\nCliente Normal - Menú")
            print("1. Crear Cuenta")
            print("2. Realizar Compra")
            print("3. Consultar Historial")
            print("4. Salir")
            choice = input("Seleccione una opción: ")

            if choice == '1':
                self.crear_cuenta()
            elif choice == '2':
                product_list = input("Ingrese ID del producto: ")
                payment_method = input("Ingrese método de pago: ")
                self.realizar_compra(product_list, payment_method)
            elif choice == '3':
                self.consultar_historial()
            elif choice == '4':
                break
            else:
                print("Opción inválida. Por favor, intente de nuevo.")

# Ejemplo de uso del Cliente Normal
cliente_normal = ClienteNormal('12345678-9', 'Juan Perez', 'juan@example.com', '1234')
cliente_normal.menu()
