import imgkit
from config import IMGKIT_CONFIG, VIDEO_WIDTH, VIDEO_HEIGHT, DURATION
import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from config import DURATION
from services.answer_html import answer_format

"""def generate_images(quiz):
    from utils.html_generator import create_html

    images = []

    for i, q in enumerate(quiz):
        html = create_html(q, i)
        file = f"slide_{i}.png"

        imgkit.from_string(
            html,
            file,
            config=IMGKIT_CONFIG,
            options={
                "width": VIDEO_WIDTH,
                "height": VIDEO_HEIGHT
            }
        )

        images.append(file)

    return images
"""
def generate_images(quiz):
    from utils.html_generator import create_html

    images = []

    for i, q in enumerate(quiz):
        # =========================
        # ✅ QUESTION SLIDE
        # =========================
        html = create_html(q, i)
        q_file = f"slide_q_{i}.png"

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

        # =========================
        # ✅ ANSWER SLIDE (NEW)
        # =========================
        correct = q["options"][q["answer_index"]]
        answer_html= answer_format(i+1, correct, q["answer_index"], q["options"])
       

        a_file = f"slide_a_{i}.png"

        imgkit.from_string(
            answer_html,
            a_file,
            config=IMGKIT_CONFIG,
            options={
                "width": VIDEO_WIDTH,
                "height": VIDEO_HEIGHT
            }
        )

        images.append(a_file)

    return images

# ✅ ADD THIS FUNCTION
def generate_answer_slide(quiz):
    slides = []
    answers_per_slide = 7

    # Split quiz into chunks of 7
    for i in range(0, len(quiz), answers_per_slide):
        chunk = quiz[i:i + answers_per_slide]

        answer_html = "<h1 style='color:white;text-align:center'>Answers</h1>"

        for j, q in enumerate(chunk):
            correct = q["options"][q["answer_index"]]
            answer_html += f"""
            <p style='color:white;font-size:40px;text-align:center'>
            Q{i + j + 1}: {correct}
            </p>
            """

        final_html = f"""
        <html>
        <body style='background:black'>
        {answer_html}
        </body>
        </html>
        """

        file_name = f"answer_{i//answers_per_slide + 1}.png"

        imgkit.from_string(
            final_html,
            file_name,
            config=IMGKIT_CONFIG,
            options={
                "width": VIDEO_WIDTH,
                "height": VIDEO_HEIGHT
            }
        )

        slides.append(file_name)

    return slides



    
"""def create_video(images, output_file):
    # ✅ Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    from moviepy.editor import ImageClip, concatenate_videoclips
    from config import DURATION

    clips = [ImageClip(img).set_duration(DURATION) for img in images]
    video = concatenate_videoclips(clips)

    video.write_videofile(output_file, fps=24)    """

def create_video(images, output_file):
    try:
        # ✅ Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        print("🎬 Creating video clips...")
        clips = [ImageClip(img).set_duration(DURATION) for img in images]

        video = concatenate_videoclips(clips)

        # =========================
        # 🎵 ADD BACKGROUND MUSIC
        # =========================
        music_path = "assets/bg_music.mp3"

        if os.path.exists(music_path):
            print("🎵 Adding background music...")

            audio = AudioFileClip(music_path)

            # 🔁 Loop audio if shorter than video
            if audio.duration < video.duration:
                audio = audio.loop(duration=video.duration)
            else:
                audio = audio.subclip(0, video.duration)

            # 🔉 Reduce volume (important)
            audio = audio.volumex(0.2)

            video = video.set_audio(audio)

        else:
            print("⚠️ Background music not found")

        # =========================
        # 🎥 EXPORT VIDEO
        # =========================
        print("📤 Rendering final video...")
        video.write_videofile(output_file, fps=24)

    except Exception as e:
        print("❌ Error in create_video:", e)    