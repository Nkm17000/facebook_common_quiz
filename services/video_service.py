import os
import imgkit
import base64
from moviepy.editor import (
    ImageClip,
    concatenate_videoclips,
    AudioFileClip,
    CompositeAudioClip
)
from moviepy.audio.fx.all import audio_loop

from config import IMGKIT_CONFIG, VIDEO_WIDTH, VIDEO_HEIGHT, DURATION


# =========================
# GENERATE IMAGES (WITH COUNTDOWN)
# =========================

def generate_images(quiz):
    from services.html_generator import create_html
    from services.answer_html import answer_html   # ✅ FIXED (no circular import)

    images = []

    for i, q in enumerate(quiz):

        # =========================
        # ✅ HANDLE BILINGUAL DATA
        # =========================
        q["question"] = f'{q["question"]["en"]}<br><span style="font-size:30px">{q["question"]["hi"]}</span>'

        q["options"] = [
            f'{opt["en"]}<br><span style="font-size:22px">{opt["hi"]}</span>'
            for opt in q["options"]
        ]

        # 🔥 COUNTDOWN 3 → 1
        for t in range(3, 0, -1):
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

        # =========================
        # ✅ ANSWER SLIDE (FIXED CALL)
        # =========================
        ans_html = answer_html(q, i)

        ans_file = f"answer_{i}.png"

        imgkit.from_string(
            ans_html,
            ans_file,
            config=IMGKIT_CONFIG,
            options={
                "width": VIDEO_WIDTH,
                "height": VIDEO_HEIGHT,
                "enable-local-file-access": ""   # ✅ FIXED
            }
        )

        images.append(ans_file)

    return images


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
            bg = AudioFileClip("assets/bg_music.mp3")
            bg = audio_loop(bg, duration=video.duration)
            audio_clips.append(bg.volumex(0.3))

        # ⏳ Tick sound
        if os.path.exists("assets/tick.mp3"):
            tick = AudioFileClip("assets/tick.mp3")
            current_time = 0

            for img in images:
                if "slide_" in img:
                    audio_clips.append(tick.set_start(current_time).volumex(0.8))
                current_time += DURATION

        # ✅ Correct answer sound
        if os.path.exists("assets/correct.mp3"):
            correct = AudioFileClip("assets/correct.mp3")
            current_time = 0

            for img in images:
                if "answer_" in img:
                    audio_clips.append(correct.set_start(current_time).volumex(1.0))
                current_time += DURATION

        # 🎧 Merge audio
        if audio_clips:
            final_audio = CompositeAudioClip(audio_clips).set_duration(video.duration)
            video = video.set_audio(final_audio)

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        video.write_videofile(
            output_file,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )

        print("✅ Video created!")

        # ✅ MEMORY CLEANUP (IMPORTANT FOR GITHUB)
        video.close()
        for clip in clips:
            clip.close()

    except Exception as e:
        print(f"❌ Error in create_video: {e}")


# =========================
# LOGO BASE64
# =========================

def get_logo_base64():
    # ✅ FIX: GitHub safe path
    logo_path = os.path.join(os.getcwd(), "assets", "logo.png")

    print("📍 Logo path:", logo_path)

    with open(logo_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")