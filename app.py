from fastapi import FastAPI, BackgroundTasks
from services.pipeline import run_pipeline

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Quiz Video API Running 🚀"}


# ✅ API trigger
@app.get("/generate-video")
def generate_video(bg: BackgroundTasks):
    bg.add_task(run_pipeline)
    return {"status": "Processing started"}


# ✅ CLI support (IMPORTANT)
if __name__ == "__main__":
    run_pipeline()