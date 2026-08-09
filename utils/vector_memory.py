import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_FILE = "data/history/vectors.index"
TEXT_FILE = "data/history/texts.json"

model = SentenceTransformer("all-MiniLM-L6-v2")


def ensure_files():
    os.makedirs("data/history", exist_ok=True)

    if not os.path.exists(TEXT_FILE):
        with open(TEXT_FILE, "w") as f:
            json.dump([], f)


def load_vector_store():
    ensure_files()

    texts = []
    if os.path.exists(TEXT_FILE):
        try:
            with open(TEXT_FILE, "r") as f:
                texts = json.load(f)
        except:
            texts = []

    # ✅ Handle FAISS safely
    if os.path.exists(VECTOR_FILE):
        try:
            index = faiss.read_index(VECTOR_FILE)
        except Exception as e:
            print("⚠️ FAISS index corrupted, recreating...", e)
            index = faiss.IndexFlatL2(384)
    else:
        index = faiss.IndexFlatL2(384)

    return index, texts


def save_vector_store(index, texts):
    faiss.write_index(index, VECTOR_FILE)

    with open(TEXT_FILE, "w") as f:
        json.dump(texts, f, indent=2)


def add_to_memory(question, index, texts):
    embedding = model.encode([question])
    index.add(np.array(embedding).astype("float32"))

    texts.append(question)

    save_vector_store(index, texts)


def is_duplicate(question, index, texts, threshold=0.85):
    if len(texts) == 0:
        return False

    embedding = model.encode([question])
    D, I = index.search(np.array(embedding).astype("float32"), k=1)

    similarity = 1 - D[0][0]

    print(f"🔍 Similarity: {similarity}")

    return similarity > threshold