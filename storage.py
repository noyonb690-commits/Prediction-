import json
import os

FILE = "feedback.json"

def load_feedback():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_feedback(data):
    with open(FILE, "w") as f:
        json.dump(data, f)
