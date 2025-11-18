import json

def load_json(path):
    try:
        return json.loads(path.read_text())
    except:
        return []

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))