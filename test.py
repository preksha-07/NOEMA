import requests

response = requests.post(
    "http://172.17.10.9:9000/execute_plotter",
    json={
        "commands": [
            "G01 X10 Y10",
            "G01 X20 Y20"
        ]
    }
)

print(response.text)