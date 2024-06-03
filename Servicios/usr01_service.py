from flask import Flask, request
import requests

app = Flask(__name__)

users = {}

@app.route('/usr01', methods=['POST'])
def user_management():
    data = request.get_data(as_text=True)
    print(f"Received data: {data}")
    operation = data[5:10].strip()
    details = data[10:]
    print(f"Operation: {operation}, Details: {details}")

    if operation == "Crear":
        rut, name, email, password = details.split(',')
        users[rut] = {"name": name, "email": email, "password": password}
        response = "OK"
    elif operation == "Actual":
        rut, name, email, password = details.split(',')
        if rut in users:
            users[rut].update({"name": name, "email": email, "password": password})
            response = "OK"
        else:
            response = "NK"
    elif operation == "Enviar":
        rut, email = details.split(',')
        if rut in users and users[rut]["email"] == email:
            # Simulate sending email
            response = "OK"
        else:
            response = "NK"
    else:
        response = "NK"

    response_message = f"{len(response + details):05}usr01{response}{details}"
    print(f"Response: {response_message}")
    return response_message, 200

@app.route('/sinit', methods=['POST'])
def sinit():
    response_message = "00005usr01OK"
    print(f"Service Initialization: {response_message}")
    return response_message, 200

def register_service():
    message = "00005sinitusr01"
    try:
        response = requests.post('http://localhost:5000/sinit', data=message)
        print(f"sinit response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error registering service: {e}")

if __name__ == '__main__':
    print("Starting USR01 service...")
    register_service()
    app.run(host='0.0.0.0', port=5001)
