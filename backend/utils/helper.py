import json
import os

def load_json_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json_data(file_path, data):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
