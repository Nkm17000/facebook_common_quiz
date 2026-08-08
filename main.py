import os
import requests
import imgkit
from moviepy.editor import ImageClip, concatenate_videoclips

# ================= CONFIG =================
OUTPUT_VIDEO = "quiz_video.mp4"
DURATION = 3
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set in GitHub secrets

config = imgkit.config(wkhtmltoimage='/usr/bin/wkhtmltoimage')

# ================= GROQ CALL =================
def fetch_quiz():
    url = "https://api.groq.com/openai/v1/chat/completions"

    prompt = """
    Generate 20 multiple choice quiz questions.

    Format strictly as JSON like this:
    [
      {
        "question": "...",
        "options": ["A", "B", "C", "D"],
        "answer": "correct option text"
      }
    ]

    Only return JSON. No explanation.
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    content = result["choices"][0]["message"]["content"]

    import json
    quiz_data = json.loads(content)

    return quiz_data


# ================= CSS =================
CSS = """
<style>
body {
    background: radial-gradient(circle, #0A254F, #071A3D);
    font-family: Arial;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.quiz-card {
    width: 1200px;
    padding: 40px;
    border-radius: 20px;
    border: 2px solid cyan;
}
h2 {
    font-size: 50px;
}
.option {
    font-size: 35px;
    margin: 10px 0;
}
</style>
"""

# ================= HTML BUILDER =================
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


# ================= MAIN =================
quiz = fetch_quiz()

images = []

# 🎬 Generate question slides
for i, q in enumerate(quiz):
    file = f"slide_{i}.png"
    imgkit.from_string(
        create_html(q, i),
        file,
        config=config,
        options={"width": 1920, "height": 1080}
    )
    images.append(file)

# ✅ Answer slide
answer_html = f"""
<html>
<head>{CSS}</head>
<body>
<div class="quiz-card">
<h2>Answers</h2>
"""

for i, q in enumerate(quiz):
    answer_html += f"<div class='option'>Q{i+1}: {q['answer']}</div>"

answer_html += "</div></body></html>"

imgkit.from_string(
    answer_html,
    "answer.png",
    config=config,
    options={"width": 1920, "height": 1080}
)
images.append("answer.png")

# 🎥 Create video
clips = [ImageClip(img).set_duration(DURATION) for img in images]
video = concatenate_videoclips(clips)

video.write_videofile(OUTPUT_VIDEO, fps=24)

# 🧹 Cleanup
for img in images:
    os.remove(img)

print("✅ Video Created!")