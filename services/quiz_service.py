import json
import re
import requests
from config import GROQ_API_KEY, GROQ_URL, MODEL

def fetch_quiz():
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = """
You are a JSON generator.

Return ONLY valid JSON.

SCHEMA:
[
{
"question": "string",
"options": ["string", "string", "string", "string"],
"answer_index": number
}
]

RULES:
- Exactly 20 questions
- Mix subjects
"""

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)
    result = response.json()

    try:
        content = result["choices"][0]["message"]["content"]
        match = re.search(r"\[.*\]", content, re.DOTALL)

        if match:
            return json.loads(match.group(0))

        raise Exception("Invalid JSON")

    except Exception:
        print("⚠️ Using fallback quiz")
        return fallback_quiz()
    
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