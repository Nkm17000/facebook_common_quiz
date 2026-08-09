import json
import os

MEMORY_FILE = "data/history/history.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"counter": 0}

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

        if "counter" not in data:
            data["counter"] = 0

        return data

    except:
        return {"counter": 0}


def save_memory(memory):
    os.makedirs("data/history", exist_ok=True)

    temp = MEMORY_FILE + ".tmp"

    with open(temp, "w") as f:
        json.dump(memory, f, indent=2)

    os.replace(temp, MEMORY_FILE)