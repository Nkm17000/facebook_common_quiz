import json
import os
from utils.memory import load_memory, save_memory

QUIZ_DIR = "assets/quiz_data"
BATCH_SIZE = 10


def load_all_questions():
    all_questions = []

    for file in os.listdir(QUIZ_DIR):
        if file.endswith(".json"):
            path = os.path.join(QUIZ_DIR, file)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_questions.extend(data)

    return all_questions


def fetch_quiz():
    memory = load_memory()
    counter = memory.get("counter", 0)

    questions = load_all_questions()
    total = len(questions)

    if total == 0:
        raise Exception("No questions found")

    # 🔁 reset if overflow
    if counter >= total:
        counter = 0

    batch = questions[counter:counter + BATCH_SIZE]

    # 🔁 wrap if end reached
    if len(batch) < BATCH_SIZE:
        remaining = BATCH_SIZE - len(batch)
        batch.extend(questions[:remaining])
        counter = remaining
    else:
        counter += BATCH_SIZE

    # 💾 save counter
    memory["counter"] = counter
    save_memory(memory)

    return batch, False