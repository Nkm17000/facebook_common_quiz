import os
import imgkit
from moviepy.editor import ImageClip, concatenate_videoclips

# CONFIG
OUTPUT_VIDEO = "quiz_video.mp4"
DURATION = 3

config = imgkit.config(wkhtmltoimage='/usr/bin/wkhtmltoimage')

quiz = [
    {
        "question": "What is the capital of Japan?",
        "options": ["Beijing", "Seoul", "Tokyo", "Bangkok"],
        "answer": "Tokyo"
    },
    {
        "question": "Largest planet in solar system?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Jupiter"
    }
]

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
}
.option {
padding: 20px;
margin: 15px;
border-radius: 40px;
border: 2px solid #3B82F6;
font-size: 26px;
}
h2 {
font-size: 40px;
}
</style>
"""

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

images = []

# Generate slides
for i, q in enumerate(quiz):
    file = f"slide_{i}.png"
    imgkit.from_string(create_html(q, i), file, config=config, options={"width":1920,"height":1080})
    images.append(file)

# Answer slide
answer_html = "<h1 style='color:white;text-align:center;'>Answers</h1>"
for i, q in enumerate(quiz):
    answer_html += f"<h2 style='color:white;text-align:center;'>Q{i+1}: {q['answer']}</h2>"

imgkit.from_string(answer_html, "answer.png", config=config, options={"width":1920,"height":1080})
images.append("answer.png")

# Create video
clips = [ImageClip(img).set_duration(DURATION) for img in images]
video = concatenate_videoclips(clips)
video.write_videofile(OUTPUT_VIDEO, fps=24)

# Cleanup
for img in images:
    os.remove(img)

print("✅ Video Created!")