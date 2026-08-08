import os
import json
import re
import requests
import imgkit
from moviepy.editor import ImageClip, concatenate_videoclips

# =========================
# CONFIG
# =========================
OUTPUT_VIDEO = "quiz_video.mp4"
DURATION = 3

config = imgkit.config(wkhtmltoimage='/usr/bin/wkhtmltoimage')

# =========================
# FETCH QUIZ (WITH SCHEMA)
# =========================
def fetch_quiz():
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    prompt = """
You are a JSON generator.

Return ONLY valid JSON. No explanation.

SCHEMA:
[
  {
    "question": "string",
    "options": ["string", "string", "string", "string"],
    "answer_index": number (0-3)
  }
]

RULES:
- Exactly 20 questions
- Each question must have 4 options
- answer_index must match correct option
- Mix subjects: English, GK, CS, Reasoning, Science, Math
"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    print("DEBUG API RESPONSE:", result)

    try:
        content = result["choices"][0]["message"]["content"]

        # Extract JSON safely
        match = re.search(r"\[.*\]", content, re.DOTALL)
        if match:
            return json.loads(match.group(0))

        raise Exception("Invalid JSON")

    except Exception as e:
        print("⚠️ Fallback quiz used")

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

# =========================
# CSS DESIGN
# =========================
CSS = """
<style>
body {
  margin: 0;
  background: radial-gradient(circle at center, #0A254F, #071A3D);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-family: Arial, sans-serif;
}
.quiz-container {
  width: 1400px;
}
.quiz-card {
  background: rgba(10, 37, 79, 0.9);
  border-radius: 30px;
  padding: 60px;
  border: 2px solid #22D3EE;
  box-shadow: 0 0 40px rgba(34, 211, 238, 0.3);
}
.question-text {
  font-size: 52px;
  text-align: center;
  color: white;
  font-weight: bold;
  margin-bottom: 50px;
}
.options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}
.option {
  padding: 30px;
  border-radius: 50px;
  border: 2px solid #3B82F6;
  font-size: 30px;
  color: white;
  text-align: center;
}
</style>
"""

# =========================
# HTML GENERATOR
# =========================
def create_html(q, index):
    labels = ["A", "B", "C", "D"]

    options_html = ""
    for i, opt in enumerate(q["options"]):
        options_html += f"""
        <div class="option">
            <b>{labels[i]}.</b> {opt}
        </div>
        """

    return f"""
<html>
<head>{CSS}</head>
<body>
<div class="quiz-container">
  <div class="quiz-card">
    <div class="question-text">Q{index+1}. {q['question']}</div>
    <div class="options">
      {options_html}
    </div>
  </div>
</div>
</body>
</html>
"""

# =========================
# MAIN
# =========================
def main():
    quiz = fetch_quiz()
    images = []

    print("🖼️ Generating slides...")

    for i, q in enumerate(quiz):
        html = create_html(q, i)
        file = f"slide_{i}.png"

        imgkit.from_string(
            html,
            file,
            config=config,
            options={"width": 1920, "height": 1080}
        )

        images.extend(file)

    # =========================
    # ANSWER SLIDE
    # =========================
    answer_html = "<h1 style='color:white;text-align:center'>Answers</h1>"

    for i, q in enumerate(quiz):
        correct = q["options"][q["answer_index"]]
        answer_html += f"<p style='color:white;font-size:40px;text-align:center'>Q{i+1}: {correct}</p>"

    final_page = f"<html><body style='background:black'>{answer_html}</body></html>"

    imgkit.from_string(
        final_page,
        "answer.png",
        config=config,
        options={"width": 1920, "height": 1080}
    )

    images.extend("answer.png")

    print("🎬 Creating video...")

    clips = [ImageClip(img).set_duration(DURATION) for img in images]
    video = concatenate_videoclips(clips)

    video.write_videofile(OUTPUT_VIDEO, fps=24)

    # Cleanup
    for img in images:
        os.remove(img)

    print("✅ Video Created!")

# =========================
if __name__ == "__main__":
    main()