import os
from moviepy.editor import TextClip, CompositeVideoClip, concatenate_videoclips, ColorClip

# CONFIG
WIDTH, HEIGHT = 1080, 1920   # Reels/Shorts format
DURATION = 3
OUTPUT_VIDEO = "quiz_video.mp4"

# QUIZ DATA
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

# 🎨 COLORS
BG_COLOR = (7, 26, 61)          # Dark blue
TEXT_COLOR = "white"
OPTION_COLOR = "#3B82F6"
ANSWER_COLOR = "#22D3EE"

# 🎬 CREATE QUESTION SLIDE
def create_question_slide(q, index):
    bg = ColorClip(size=(WIDTH, HEIGHT), color=BG_COLOR, duration=DURATION)

    # Question
    question = TextClip(
        f"Q{index+1}. {q['question']}",
        fontsize=60,
        color=TEXT_COLOR,
        method="caption",
        size=(900, None)
    ).set_position(("center", 300)).set_duration(DURATION)

    # Options
    option_clips = []
    labels = ["A", "B", "C", "D"]

    for i, opt in enumerate(q["options"]):
        txt = TextClip(
            f"{labels[i]}. {opt}",
            fontsize=45,
            color="white",
            method="caption",
            size=(800, None)
        ).set_position(("center", 700 + i*150)).set_duration(DURATION)

        option_clips.append(txt)

    return CompositeVideoClip([bg, question, *option_clips])

# 🎬 CREATE ANSWER SLIDE
def create_answer_slide():
    bg = ColorClip(size=(WIDTH, HEIGHT), color=BG_COLOR, duration=DURATION)

    title = TextClip(
        "Answers",
        fontsize=70,
        color=ANSWER_COLOR
    ).set_position(("center", 200)).set_duration(DURATION)

    answers = []
    for i, q in enumerate(quiz):
        txt = TextClip(
            f"Q{i+1}: {q['answer']}",
            fontsize=50,
            color="white"
        ).set_position(("center", 400 + i*120)).set_duration(DURATION)

        answers.append(txt)

    return CompositeVideoClip([bg, title, *answers])

# 🎥 BUILD VIDEO
clips = []

for i, q in enumerate(quiz):
    clips.append(create_question_slide(q, i))

clips.append(create_answer_slide())

final_video = concatenate_videoclips(clips)

final_video.write_videofile(OUTPUT_VIDEO, fps=24)

print("✅ Video Created!")