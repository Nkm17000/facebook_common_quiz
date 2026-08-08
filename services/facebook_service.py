import requests
import os

def upload_video_to_facebook(video_path, caption="Daily Quiz 🎯"):
    page_id = os.getenv("FACEBOOK_PAGE_ID")
    access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")

    url = f"https://graph-video.facebook.com/v19.0/{page_id}/videos"

    files = {
        "source": open(video_path, "rb")
    }

    data = {
        "description": caption,
        "access_token": access_token
    }

    response = requests.post(url, files=files, data=data)

    try:
        result = response.json()
        print("📤 Facebook Upload Response:", result)
        return result
    except Exception:
        print("❌ Upload failed:", response.text)
        return None