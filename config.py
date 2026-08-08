import os
import imgkit
from dotenv import load_dotenv

load_dotenv()

# =========================
# ENV VARIABLES
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", 1920))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", 1080))
DURATION = int(os.getenv("VIDEO_DURATION", 3))

MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

WKHTML_PATH = os.getenv("WKHTMLTOIMAGE_PATH", "/usr/bin/wkhtmltoimage")

IMGKIT_CONFIG = imgkit.config(wkhtmltoimage=WKHTML_PATH)

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

OUTPUT_DIR = "output"
OUTPUT_VIDEO = f"{OUTPUT_DIR}/quiz_video.mp4"