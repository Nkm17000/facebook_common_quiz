import os
import imgkit
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from config import IMGKIT_CONFIG, VIDEO_WIDTH, VIDEO_HEIGHT, DURATION


# =========================
# GENERATE QUESTION + ANSWER IMAGES (ALTERNATE FLOW)
# =========================
def generate_images(quiz):
    from utils.html_generator import create_html
    from services.video_service import answer_html

    images = []

    for i, q in enumerate(quiz):

        # ✅ QUESTION SLIDE
        html = create_html(q, i)
        q_file = f"slide_{i}.png"

        imgkit.from_string(
            html,
            q_file,
            config=IMGKIT_CONFIG,
            options={
                "width": VIDEO_WIDTH,
                "height": VIDEO_HEIGHT
            }
        )

        images.append(q_file)

        # ✅ ANSWER SLIDE (IMMEDIATELY AFTER QUESTION)
        correct = q["options"][q["answer_index"]]

        ans_html = answer_html(
            i + 1,
            correct,
            q["answer_index"],
            q["options"]
        )

        a_file = f"answer_{i}.png"

        imgkit.from_string(
            ans_html,
            a_file,
            config=IMGKIT_CONFIG,
            options={
                "width": VIDEO_WIDTH,
                "height": VIDEO_HEIGHT
            }
        )

        images.append(a_file)

    return images


# =========================
# ANSWER HTML (GREEN HIGHLIGHT)
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
# CREATE VIDEO (WITH SAFE AUDIO)
# =========================
def create_video(images, output_file):
    try:
        print("🎬 Creating video clips...")

        clips = [ImageClip(img).set_duration(DURATION) for img in images]
        video = concatenate_videoclips(clips)

        print("🎵 Adding background music...")

        audio_path = "assets/bg_music.mp3"

        if os.path.exists(audio_path):
            try:
                audio = AudioFileClip(audio_path)

                # ✅ FIX: no .loop() (this was your bug)
                audio = audio.set_duration(video.duration)

                video = video.set_audio(audio)

            except Exception as e:
                print(f"⚠️ Audio failed, continuing without sound: {e}")

        else:
            print("⚠️ No background music found, skipping audio")

        # ✅ Ensure output dir exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        print("🎥 Rendering final video...")

        video.write_videofile(
            output_file,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )

        print("✅ Video created successfully!")

    except Exception as e:
        print(f"❌ Error in create_video: {e}")