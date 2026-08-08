import json
import re
import requests
from config import GROQ_API_KEY, GROQ_URL, MODEL
from services.prompt import prompt

def fetch_quiz():
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        result = response.json()

        print(result)

        # =========================
        # ❌ HANDLE API ERROR FIRST
        # =========================
        if "error" in result:
            print("❌ API Error:", result["error"]["message"])
            return fallback_quiz(), True   # ✅ fallback flag

        # =========================
        # ✅ NORMAL FLOW
        # =========================
        content = result["choices"][0]["message"]["content"]

        match = re.search(r"\[.*\]", content, re.DOTALL)

        if match:
            return json.loads(match.group(0)), False  # ✅ success

        raise Exception("Invalid JSON format")

    except Exception as e:
        print(f"❌ Error generating quiz: {e}")
        print("⚠️ Using fallback quiz")

        return fallback_quiz(), True   # ✅ fallback flag


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