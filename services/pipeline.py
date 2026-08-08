from services.quiz_service import fetch_quiz
from utils.file_utils import cleanup
from config import OUTPUT_VIDEO
from config import OUTPUT_DIR
from services.facebook_service import upload_video_to_facebook
from services.video_service import generate_images, create_video
import os
def run_pipeline():
    print("create output dir")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("📥 Fetching quiz...")
    quiz, is_fallback = fetch_quiz()

    if is_fallback:
        print("🚫 Fallback detected → stopping pipeline")
        return

    print("🖼️ Generating images...")
    images = generate_images(quiz)

    """print("📊 Adding answer slide...")
    answer_img = generate_answer_slide(quiz)
    images.extend(answer_img)"""

   
    print("🎬 Creating video...")
    create_video(images, OUTPUT_VIDEO)
    
    if not os.path.exists(OUTPUT_VIDEO):
        print("❌ Video not created. Skipping Facebook upload.")
        return

    print("📤 Uploading to Facebook...")

    upload_video_to_facebook(
        OUTPUT_VIDEO,
        caption="""📚 Daily Practice Quiz for SSC | UPSC | Bank | Railway
                👉 Boost your score daily 🚀 Drop your result in comments 👇
                    #sscpreparation #upsc #bankexam #railwayexam #quiz"""
    )

    print("🧹 Cleaning up...")
    cleanup(images)

    print("✅ Done!")