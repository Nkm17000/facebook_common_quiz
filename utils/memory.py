import json
import os

MEMORY_FILE = "data/history/history.json"
MAX_MEMORY = 500


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"questions": []}

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    os.makedirs("data/history", exist_ok=True)

    # limit memory size
    memory["questions"] = memory["questions"][-MAX_MEMORY:]

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def normalize(text):
    return text.lower().strip()


def is_duplicate(question, memory):
    q = normalize(question)
    return any(normalize(old) == q for old in memory["questions"])


def add_to_memory(question, memory):
    memory["questions"].append(question)