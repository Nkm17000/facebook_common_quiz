import os
import json
import requests
import imgkit
from moviepy.editor import ImageClip, concatenate_videoclips

# =========================
# CONFIG
# =========================
OUTPUT_VIDEO = "quiz_video.mp4"
DURATION = 3

# wkhtmltoimage config (for GitHub Actions / Linux)
config = imgkit.config(wkhtmltoimage='/usr/bin/wkhtmltoimage')

# =========================
# FALLBACK QUIZ (SAFE MODE)
# =========================
def fallback_quiz():
    return [
        {
            "question": "What is the capital of India?",
            "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
            "answer": "Delhi"
        },
        {
            "question": "Largest planet in solar system?",
            "options": ["Earth", "Mars", "Jupiter", "Venus"],
            "answer": "Jupiter"
        }
    ]

# =========================
# FETCH QUIZ FROM GROQ API
# =========================
def fetch_quiz():
    try:
        API_KEY = os.getenv("GROQ_API_KEY")

        if not API_KEY:
            print("❌ GROQ_API_KEY missing → using fallback")
            return fallback_quiz()

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "user",
                    "content": """
Generate 5 quiz questions in JSON format.

Format:
[
  {
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "correct option text"
  }
]
"""
                }
            ]
        }

        response = requests.post(url, json=payload, headers=headers)
        result = response.json()

        print("DEBUG API RESPONSE:", result)

        # ✅ SAFE PARSING
        if "choices" in result:
            content = result["choices"][0]["message"]["content"]

            try:
                quiz = json.loads(content)
                return quiz
            except:
                print("⚠️ JSON parsing failed → fallback used")
                return fallback_quiz()

        else:
            print("❌ API ERROR:", result)
            return fallback_quiz()

    except Exception as e:
        print("❌ EXCEPTION:", e)
        return fallback_quiz()

# =========================
# CSS DESIGN (FUTURISTIC UI)
# =========================
CSS = """
<style>
body {
background: radial-gradient(circle at center, #0A254F, #071A3D);
color: white;
display: flex;
justify-content: center;
align-items: center;
height: 100vh;
font-family: Arial;
}

.quiz-card {
width: 1200px;
padding: 50px;
border-radius: 30px;
border: 2px solid #22D3EE;
text-align: center;
box-shadow: 0 0 30px rgba(34,211,238,0.3);
}

.option {
padding: 20px;
margin: 15px;
border-radius: 40px;
border: 2px solid #3B82F6;
font-size: 28px;
}

h2 {
font-size: 42px;
margin-bottom: 30px;
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
        options_html += f"<div class='option'>{labels[i]}. {opt}</div>"

    return f"""
    <html>
    <head>{CSS}</head>
    <body>
    <div class="quiz-card">
        <h2>Q{index+1}. {q['question']}</h2>
        {options_html}
    </div>
    </body>
    </html>
    """

# =========================
# MAIN PROCESS
# =========================
def main():
    quiz = fetch_quiz()

    # Safety: if API returns wrong type
    if not isinstance(quiz, list):
        quiz = fallback_quiz()

    images = []

    print("🖼️ Generating slides...")

    # Question slides
    for i, q in enumerate(quiz):
        filename = f"slide_{i}.png"

        imgkit.from_string(
            create_html(q, i),
            filename,
            config=config,
            options={"width": 1920, "height": 1080}
        )

        images.append(filename)

    # Answer slide
    answer_html = "<h1 style='color:white;text-align:center;'>Answers</h1>"

    for i, q in enumerate(quiz):
        answer_html += f"<h2 style='color:white;text-align:center;'>Q{i+1}: {q['answer']}</h2>"

    imgkit.from_string(
        answer_html,
        "answer.png",
        config=config,
        options={"width": 1920, "height": 1080}
    )

    images.append("answer.png")

    print("🎬 Creating video...")

    # Create video
    clips = [ImageClip(img).set_duration(DURATION) for img in images]
    video = concatenate_videoclips(clips)
    video.write_videofile(OUTPUT_VIDEO, fps=24)

    # Cleanup
    for img in images:
        os.remove(img)

    print("✅ Video Created Successfully!")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()