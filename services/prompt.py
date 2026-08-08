prompt = """
You are an expert competitive exam question setter for SSC, UPSC, Banking (PO/Clerk), and Railway exams.

Generate a HIGH-QUALITY mixed-subject quiz in STRICT JSON format.

Return ONLY valid JSON. No explanation, no extra text.

SCHEMA:
[
  {
    "question": "English question / हिंदी प्रश्न",
    "options": [
      "Option A / विकल्प A",
      "Option B / विकल्प B",
      "Option C / विकल्प C",
      "Option D / विकल्प D"
    ],
    "answer_index": number
  }
]

RULES:

- Generate EXACTLY 20 questions
- Each question must be bilingual (English + Hindi)
- Each option must also be bilingual (English + Hindi)
- answer_index must be 0, 1, 2, or 3

- Difficulty Level:
  Match SSC, UPSC Prelims, Bank PO, and Railway exams
  (Conceptual + tricky + elimination-based questions)

- Mix subjects across:
  • Mathematics (Arithmetic, DI, Algebra, Simplification)
  • General Knowledge (India + World, Static GK, Polity, History, Geography)
  • General Science (Physics, Chemistry, Biology)
  • English (Grammar, Vocabulary, Error Detection, Fill in the blanks)
  • Reasoning (Logical, Series, Coding-Decoding, Puzzles)
  • Computer Science (Basic IT, MS Office, Internet, AI basics)

- Ensure balanced distribution:
  • 4 Math
  • 3 GK
  • 3 Science
  • 3 English
  • 3 Reasoning
  • 2 Computer
  • Remaining 2 from any category

- Questions must be:
  ✔ Short and clear
  ✔ Concept-based (not too direct)
  ✔ Non-repetitive
  ✔ Factually correct
  ✔ Useful for real exam preparation

- Avoid very easy or very obscure questions

OUTPUT:
Return ONLY the JSON array with 20 bilingual competitive-level questions.

"""