import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

VECTOR_FILE = "data/history/vectors.index"
TEXT_FILE = "data/history/vector_texts.json"

# ✅ Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================
# 🧠 LOAD VECTOR STORE (SAFE)
# =========================
def load_vector_store():
    try:
        if os.path.exists(VECTOR_FILE) and os.path.exists(TEXT_FILE):
            index = faiss.read_index(VECTOR_FILE)

            with open(TEXT_FILE, "r") as f:
                texts = json.load(f)

            return index, texts

    except Exception as e:
        print("⚠️ FAISS index corrupted, recreating...", e)

    # ✅ fallback: create new index
    index = faiss.IndexFlatL2(384)
    return index, []


# =========================
# 💾 SAVE VECTOR STORE (ATOMIC)
# =========================
def save_vector_store(index, texts):
    os.makedirs("data/history", exist_ok=True)

    # ✅ atomic write (prevents corruption)
    temp_file = VECTOR_FILE + ".tmp"
    faiss.write_index(index, temp_file)
    os.replace(temp_file, VECTOR_FILE)

    with open(TEXT_FILE, "w") as f:
        json.dump(texts, f, indent=2)


# =========================
# 🔍 CHECK SIMILARITY
# =========================
def is_similar(question, index, texts, threshold=0.6):
    if len(texts) == 0:
        return False

    q_vec = model.encode([question])
    D, I = index.search(np.array(q_vec), 1)

    return D[0][0] < threshold


# =========================
# ➕ ADD TO VECTOR STORE
# =========================
def add_to_vector_store(question, index, texts):
    vec = model.encode([question])
    index.add(np.array(vec))
    texts.append(question)

    # ✅ limit size (important for GitHub repo)
    if len(texts) > 1000:
        texts = texts[-1000:]

    return index, texts