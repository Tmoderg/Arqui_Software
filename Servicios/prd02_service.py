from flask import Flask, request
import requests

app = Flask(__name__)

products = {}

@app.route('/prd02', methods=['POST'])
def product_management():
    data = request.get_data(as_text=True)
    print(f"Received data: {data}")
    operation = data[5:10].strip()
    details = data[10:]
    print(f"Operation: {operation}, Details: {details}")

    if operation == "Agreg":
        sku, description, price, quantity = details.split(',')
        products[sku] = {"description": description, "price": price, "quantity": quantity}
        response = "OK"
    elif operation == "Actua":
        sku, description, price, quantity = details.split(',')
        if sku in products:
            products[sku].update({"description": description, "price": price, "quantity": quantity})
            response = "OK"
        else:
            response = "NK"
    elif operation == "Elimi":
        sku = details
        if sku in products:
            del products[sku]
            response = "OK"
        else:
            response = "NK"
    else:
        response = "NK"

    response_message = f"{len(response + details):05}prd02{response}{details}"
    print(f"Response: {response_message}")
    return response_message, 200

@app.route('/sinit', methods=['POST'])
def sinit():
    response_message = "00005prd02OK"
    print(f"Service Initialization: {response_message}")
    return response_message, 200

def register_service():
    message = "00005sinitprd02"
    try:
        response = requests.post('http://localhost:5000/sinit', data=message)
        print(f"sinit response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error registering service: {e}")

if __name__ == '__main__':
    print("Starting PRD02 service...")
    register_service()
    app.run(host='0.0.0.0', port=5002)
