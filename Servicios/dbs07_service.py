from flask import Flask, request
import requests
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    database="opticommerce",
    user="postgres",
    password="7541",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

@app.route('/dbs07', methods=['POST'])
def database_access():
    data = request.get_data(as_text=True)
    print(f"Received data: {data}")
    operation = data[5:10].strip()
    query = data[10:]
    print(f"Operation: {operation}, Query: {query}")

    try:
        if operation == "Query":
            cur.execute(query)
            result = cur.fetchall()
            response = "OK"
            response_details = str(result)
        elif operation in ["Insert", "Updat", "Delet"]:
            cur.execute(query)
            conn.commit()
            response = "OK"
            response_details = ""
        else:
            response = "NK"
            response_details = ""
    except Exception as e:
        response = "NK"
        response_details = str(e)

    response_message = f"{len(response + response_details):05}dbs07{response}{response_details}"
    print(f"Response: {response_message}")
    return response_message, 200

@app.route('/sinit', methods=['POST'])
def sinit():
    response_message = "00005dbs07OK"
    print(f"Service Initialization: {response_message}")
    return response_message, 200

def register_service():
    message = "00005sinitdbs07"
    try:
        response = requests.post('http://localhost:5000/sinit', data=message)
        print(f"sinit response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error registering service: {e}")

if __name__ == '__main__':
    print("Starting DBS07 service...")
    register_service()
    app.run(host='0.0.0.0', port=5003)
