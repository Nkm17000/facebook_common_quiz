prompt = """
You are an expert viral quiz creator for SSC, UPSC, Banking, and Railway exams.

Generate a HIGH-ENGAGEMENT mixed-subject quiz in STRICT JSON format.
Return ONLY valid JSON (no explanation, no extra text).

SCHEMA:
[
{
"question": "English / हिंदी",
"options": [
"A / विकल्प A",
"B / विकल्प B",
"C / विकल्प C",
"D / विकल्प D"
],
"answer_index": 0-3
}
]

REQUIREMENTS:

* Generate EXACTLY 20 questions
* All questions and options must be bilingual (English + Hindi)
* answer_index must be 0, 1, 2, or 3

DISTRIBUTION:

* 4 Mathematics
* 3 GK
* 3 Science
* 3 English
* 3 Reasoning
* 2 Computer
* 2 Mixed

ENGAGEMENT RULES:

* Start with 2 EASY questions (hook users)
* Gradually increase difficulty (easy → medium → tricky)
* Include 3 elimination-based/tricky questions
* Include 2 surprising or lesser-known facts


CONTENT STYLE:

* Short, crisp, scroll-stopping questions
* Concept-based and exam-relevant
* Not too basic, not too obscure
* Ensure factual accuracy


OUTPUT:
Return ONLY the JSON array with 20 questions.

"""