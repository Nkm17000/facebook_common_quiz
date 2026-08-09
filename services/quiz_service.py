import json
import re
import requests
from config import GROQ_API_KEY, GROQ_URL, MODEL
from services.prompt import prompt

# 🧠 Memory (exact match)
from utils.memory import load_memory, save_memory, is_duplicate, add_to_memory

# 🚀 Vector memory (semantic match)
from utils.vector_memory import (
    load_vector_store,
    save_vector_store,
    is_similar,
    add_to_vector_store
)


def clean_question(q):
    # remove numbering like "1. ", "2) "
    q = re.sub(r"^\d+[\).\s]*", "", q)
    return q.strip().lower()


def fetch_quiz():
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # =========================
    # 🧠 LOAD BOTH MEMORIES
    # =========================
    memory = load_memory()
    index, texts = load_vector_store()

    history_text = "\n".join(memory["questions"][-20:])

    payload = {
        "model": MODEL,
        "messages": [{
            "role": "user",
            "content": f"""
{prompt}

STRICT RULES:
- Do NOT repeat any previous questions
- Avoid similar questions or rewording
- Avoid common/basic questions
- Try new patterns

Previous questions:
{history_text}
"""
        }]
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        result = response.json()

        print(result)

        # =========================
        # ❌ HANDLE API ERROR
        # =========================
        if "error" in result:
            print("❌ API Error:", result["error"]["message"])
            return fallback_quiz(), True

        # =========================
        # ✅ NORMAL FLOW
        # =========================
        content = result["choices"][0]["message"]["content"]

        match = re.search(r"\[.*\]", content, re.DOTALL)

        if match:
            quiz = json.loads(match.group(0))

            filtered_quiz = []

            for q in quiz:
                question_text = clean_question(q["question"])

                # 🔥 HYBRID CHECK (Exact + Semantic)
                if (not is_duplicate(question_text, memory)) and \
                   (not is_similar(question_text, index, texts)):

                    filtered_quiz.append(q)

                    # save to both memories
                    add_to_memory(q["question"], memory)
                    index, texts = add_to_vector_store(question_text, index, texts)

            # =========================
            # ⚠️ IF ALL DUPLICATES
            # =========================
            if not filtered_quiz:
                print("⚠️ All questions repeated → using partial fallback")
                filtered_quiz = quiz[:2]

            # =========================
            # 💾 SAVE BOTH MEMORIES
            # =========================
            save_memory(memory)
            save_vector_store(index, texts)

            return filtered_quiz, False

        raise Exception("Invalid JSON format")

    except Exception as e:
        print(f"❌ Error generating quiz: {e}")
        print("⚠️ Using fallback quiz")

        return fallback_quiz(), True


# =========================
# ✅ FALLBACK QUIZ
# =========================
def fallback_quiz():
    return [
        {
            "question": "Capital of India?",
            "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
            "answer_index": 0
        },
        {
            "question": "2 + 2 = ?",
            "options": ["3", "4", "5", "6"],
            "answer_index": 1
        }
    ]