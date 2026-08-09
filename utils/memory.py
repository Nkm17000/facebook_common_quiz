import json
import os

MEMORY_FILE = "data/history/history.json"
MAX_MEMORY = 500


# =========================
# 🧠 LOAD MEMORY (SAFE)
# =========================
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"questions": []}

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

        # ✅ FIX: handle old list format
        if isinstance(data, list):
            return {"questions": data}

        # ✅ ensure correct structure
        if "questions" not in data:
            return {"questions": []}

        return data

    except Exception as e:
        print("⚠️ Memory corrupted, resetting...", e)
        return {"questions": []}


# =========================
# 💾 SAVE MEMORY (SAFE)
# =========================
def save_memory(memory):
    os.makedirs("data/history", exist_ok=True)

    # ✅ ensure correct format
    if isinstance(memory, list):
        memory = {"questions": memory}

    if "questions" not in memory:
        memory["questions"] = []

    # ✅ limit memory size
    memory["questions"] = memory["questions"][-MAX_MEMORY:]

    # ✅ safe write
    temp_file = MEMORY_FILE + ".tmp"

    with open(temp_file, "w") as f:
        json.dump(memory, f, indent=2)

    os.replace(temp_file, MEMORY_FILE)


# =========================
# 🔍 NORMALIZE TEXT
# =========================
def normalize(text):
    return text.lower().strip()


# =========================
# ❌ CHECK DUPLICATE
# =========================
def is_duplicate(question, memory):
    q = normalize(question)

    return any(normalize(old) == q for old in memory["questions"])


# =========================
# ➕ ADD TO MEMORY
# =========================
def add_to_memory(question, memory):
    if "questions" not in memory:
        memory["questions"] = []

    memory["questions"].append(question)
    return memory