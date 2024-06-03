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

class ClienteAdministrador:
    def __init__(self, rut, name, email, password):
        self.rut = rut
        self.name = name
        self.email = email
        self.password = password

    def agregar_producto(self, nombre, precio, cantidad, descripcion):
        query = f"INSERT INTO Producto (nombre, precio, cantidad, descripcion) VALUES ('{nombre}', {precio}, {cantidad}, '{descripcion}')"
        data = f"Insert{query}"
        response = send_request('dbs07', data)
        print("Agregar Producto Response:", response)

    def actualizar_producto(self, id_producto, nombre, precio, cantidad, descripcion):
        query = f"UPDATE Producto SET nombre='{nombre}', precio={precio}, cantidad={cantidad}, descripcion='{descripcion}' WHERE id_producto={id_producto}"
        data = f"Updat{query}"
        response = send_request('dbs07', data)
        print("Actualizar Producto Response:", response)

    def eliminar_producto(self, id_producto):
        query = f"DELETE FROM Producto WHERE id_producto={id_producto}"
        data = f"Delet{query}"
        response = send_request('dbs07', data)
        print("Eliminar Producto Response:", response)

    def menu(self):
        while True:
            print("\nCliente Administrador - Menú")
            print("1. Agregar Producto")
            print("2. Actualizar Producto")
            print("3. Eliminar Producto")
            print("4. Salir")
            choice = input("Seleccione una opción: ")

            if choice == '1':
                nombre = input("Ingrese nombre del producto: ")
                precio = int(input("Ingrese precio del producto: "))
                cantidad = int(input("Ingrese cantidad del producto: "))
                descripcion = input("Ingrese descripción del producto: ")
                self.agregar_producto(nombre, precio, cantidad, descripcion)
            elif choice == '2':
                id_producto = int(input("Ingrese ID del producto: "))
                nombre = input("Ingrese nuevo nombre del producto: ")
                precio = int(input("Ingrese nuevo precio del producto: "))
                cantidad = int(input("Ingrese nueva cantidad del producto: "))
                descripcion = input("Ingrese nueva descripción del producto: ")
                self.actualizar_producto(id_producto, nombre, precio, cantidad, descripcion)
            elif choice == '3':
                id_producto = int(input("Ingrese ID del producto: "))
                self.eliminar_producto(id_producto)
            elif choice == '4':
                break
            else:
                print("Opción inválida. Por favor, intente de nuevo.")

# Ejemplo de uso del Cliente Administrador
cliente_admin = ClienteAdministrador('98765432-1', 'Admin User', 'admin@example.com', 'adminpass')
cliente_admin.menu()
