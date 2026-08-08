import imgkit
from moviepy.editor import ImageClip, concatenate_videoclips
from config import IMGKIT_CONFIG, VIDEO_WIDTH, VIDEO_HEIGHT, DURATION
import os

def generate_images(quiz):
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


# ✅ ADD THIS FUNCTION
def generate_answer_slide(quiz):
    answer_html = "<h1 style='color:white;text-align:center'>Answers</h1>"

    for i, q in enumerate(quiz):
        correct = q["options"][q["answer_index"]]
        answer_html += f"<p style='color:white;font-size:40px;text-align:center'>Q{i+1}: {correct}</p>"

    final_html = f"<html><body style='background:black'>{answer_html}</body></html>"

    imgkit.from_string(
        final_html,
        "answer.png",
        config=IMGKIT_CONFIG,
        options={
            "width": VIDEO_WIDTH,
            "height": VIDEO_HEIGHT
        }
    )

    return "answer.png"



    
def create_video(images, output_file):
    # ✅ Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    from moviepy.editor import ImageClip, concatenate_videoclips
    from config import DURATION

    clips = [ImageClip(img).set_duration(DURATION) for img in images]
    video = concatenate_videoclips(clips)

    video.write_videofile(output_file, fps=24)    