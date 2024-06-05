import subprocess
import os

def start_service(script_name):
    script_path = os.path.join(os.getcwd(), script_name)
    subprocess.Popen(['python', script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":
    services = [
        'dbs07_service.py',
        'prd02_service.py',
        'usr01_service.py'
    ]

    for service in services:
        start_service(service)
