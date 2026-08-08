from services.quiz_service import fetch_quiz
from services.video_service import generate_images, generate_answer_slide, create_video
from utils.file_utils import cleanup
from config import OUTPUT_VIDEO
from config import OUTPUT_DIR
import os
def run_pipeline():
    print("create output dir")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("📥 Fetching quiz...")
    quiz = fetch_quiz()

    print("🖼️ Generating images...")
    images = generate_images(quiz)

    print("📊 Adding answer slide...")
    answer_img = generate_answer_slide(quiz)
    images.append(answer_img)

    print("🎬 Creating video...")
    create_video(images, OUTPUT_VIDEO)

    print("🧹 Cleaning up...")
    cleanup(images)

    print("✅ Done!")