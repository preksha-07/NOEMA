import requests

HARDWARE_URL = "http://172.17.10.9:9000"

def execute_plotter(commands):

    print("SENDING TO:")
    print(f"{HARDWARE_URL}/execute_plotter")

    response = requests.post(
    f"{HARDWARE_URL}/execute_plotter",
    json={
        "commands": commands
    }
)

    print("STATUS:", response.status_code)
    print("TEXT:")
    print(response.text)

    return response.json()