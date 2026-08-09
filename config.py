import os
import imgkit
from dotenv import load_dotenv

load_dotenv()

# =========================
# 🎥 VIDEO CONFIG
# =========================

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920   # 🔥 vertical reels
DURATION = 3

# =========================
# 🖼️ IMAGE CONFIG
# =========================

WKHTML_PATH = os.getenv("WKHTMLTOIMAGE_PATH", "/usr/bin/wkhtmltoimage")

try:
    IMGKIT_CONFIG = imgkit.config(wkhtmltoimage=WKHTML_PATH)
except:
    print("⚠️ wkhtmltoimage not found, using default config")
    IMGKIT_CONFIG = None

# =========================
# 📁 OUTPUT CONFIG
# =========================

OUTPUT_DIR = "output"
OUTPUT_VIDEO = f"{OUTPUT_DIR}/quiz_video.mp4"

# =========================
# 📘 FACEBOOK CONFIG
# =========================

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

# =========================
# ⚠️ SAFETY CHECKS
# =========================

if not FACEBOOK_ACCESS_TOKEN:
    print("⚠️ WARNING: FACEBOOK_ACCESS_TOKEN is not set")

if not FACEBOOK_PAGE_ID:
    print("⚠️ WARNING: FACEBOOK_PAGE_ID is not set")