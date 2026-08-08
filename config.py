import os
import imgkit
from dotenv import load_dotenv

load_dotenv()

# =========================
# ENV VARIABLES
# =========================

# 🔐 AI API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🎥 Video Config
"""VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", 1920))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", 1080))
DURATION = int(os.getenv("VIDEO_DURATION", 3))"""

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920   # 🔥 vertical reels
DURATION = 4    

MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")

# 🖼️ Image Config
WKHTML_PATH = os.getenv("WKHTMLTOIMAGE_PATH", "/usr/bin/wkhtmltoimage")
IMGKIT_CONFIG = imgkit.config(wkhtmltoimage=WKHTML_PATH)

# 🌐 API URL
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# 📁 Output
OUTPUT_DIR = "output"
OUTPUT_VIDEO = f"{OUTPUT_DIR}/quiz_video.mp4"

# =========================
# 📘 FACEBOOK CONFIG (NEW)
# =========================

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

# ✅ Optional safety check 
if not FACEBOOK_ACCESS_TOKEN:
    print("⚠️ WARNING: FACEBOOK_ACCESS_TOKEN is not set")

if not FACEBOOK_PAGE_ID:
    print("⚠️ WARNING: FACEBOOK_PAGE_ID is not set")