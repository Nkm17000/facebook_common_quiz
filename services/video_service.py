import os
import imgkit
import base64
from moviepy.editor import (
    ImageClip,
    concatenate_videoclips,
    AudioFileClip,
    CompositeAudioClip
)
from config import IMGKIT_CONFIG, VIDEO_WIDTH, VIDEO_HEIGHT, DURATION


# =========================
# GENERATE IMAGES (WITH COUNTDOWN)
# =========================
def generate_images(quiz):
    from utils.html_generator import create_html
    from services.video_service import answer_html

    images = []

    for i, q in enumerate(quiz):

        # 🔥 COUNTDOWN 5 → 1
        for t in range(5, 0, -1):
            html = create_html(q, i, timer=t)
            file = f"slide_{i}_{t}.png"

            imgkit.from_string(
                html,
                file,
                config=IMGKIT_CONFIG,
                options={
                    "width": VIDEO_WIDTH,
                    "height": VIDEO_HEIGHT,
                    "enable-local-file-access": ""
                }
            )

            images.append(file)

        # ✅ ANSWER SLIDE
        correct = q["options"][q["answer_index"]]

        ans_html = answer_html(
            i + 1,
            correct,
            q["answer_index"],
            q["options"]
        )

        ans_file = f"answer_{i}.png"

        imgkit.from_string(
            ans_html,
            ans_file,
            config=IMGKIT_CONFIG,
            options={
                "width": VIDEO_WIDTH,
                "height": VIDEO_HEIGHT
            }
        )

        images.append(ans_file)

    return images


# =========================
# ANSWER HTML
# =========================
def answer_html(page, correct, correct_index, options):
    highlighted = []

    for i, opt in enumerate(options):
        if i == correct_index:
            highlighted.append(
                f"<div class='option correct'>✔ {opt}</div>"
            )
        else:
            highlighted.append(
                f"<div class='option'>{opt}</div>"
            )

    options_html = "".join(highlighted)

    return f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            font-family: Arial;
            height: 100vh;
            background: linear-gradient(180deg, #020d18, #0a2a43);
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }}

        .container {{
            width: 90%;
            text-align: center;
        }}

        .title {{
            font-size: 50px;
            margin-bottom: 30px;
        }}

        .option {{
            margin: 20px 0;
            padding: 20px;
            border-radius: 15px;
            border: 2px solid #00c3ff;
            font-size: 30px;
        }}

        .correct {{
            background: #00ff9d;
            color: black;
            box-shadow: 0 0 25px #00ff9d;
            font-weight: bold;
        }}
    </style>
    </head>

    <body>
        <div class="container">
            <div class="title">✅ Answer</div>
            {options_html}
        </div>
    </body>
    </html>
    """


# =========================
# CREATE VIDEO (WITH SOUND)
# =========================
def create_video(images, output_file):
    try:
        print("🎬 Creating video clips...")

        clips = [ImageClip(img).set_duration(DURATION) for img in images]
        video = concatenate_videoclips(clips)

        print("🎵 Adding audio...")

        audio_clips = []

        # 🎵 Background music
        if os.path.exists("assets/bg_music.mp3"):
            bg = AudioFileClip("assets/bg_music.mp3").set_duration(video.duration)
            audio_clips.append(bg.volumex(0.3))

        # ⏳ Tick sound
        if os.path.exists("assets/tick.mp3"):
            tick = AudioFileClip("assets/tick.mp3")
            current_time = 0

            for img in images:
                if "slide_" in img:
                    audio_clips.append(tick.set_start(current_time).volumex(0.8))
                current_time += DURATION

        # ✅ Correct sound
        if os.path.exists("assets/correct.mp3"):
            correct = AudioFileClip("assets/correct.mp3")
            current_time = 0

            for img in images:
                if "answer_" in img:
                    audio_clips.append(correct.set_start(current_time).volumex(1.0))
                current_time += DURATION

        if audio_clips:
            final_audio = CompositeAudioClip(audio_clips)
            video = video.set_audio(final_audio)

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        video.write_videofile(
            output_file,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )

        print("✅ Video created!")

    except Exception as e:
        print(f"❌ Error in create_video: {e}")
        

def get_logo_base64():
    with open("assets/logo.png", "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")        