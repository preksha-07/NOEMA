import json
import os

FILE_PATH = "data/learning.json"


def load_learning():
    if not os.path.exists(FILE_PATH):
        return {"risk_weight": 1.0}

    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_learning(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)