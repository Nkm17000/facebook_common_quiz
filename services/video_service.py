import imgkit
from moviepy.editor import ImageClip, concatenate_videoclips
from config import IMGKIT_CONFIG, DURATION, VIDEO_WIDTH, VIDEO_HEIGHT

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