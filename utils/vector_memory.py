import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

VECTOR_FILE = "data/history/vectors.index"
TEXT_FILE = "data/history/vector_texts.json"

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_vector_store():
    if os.path.exists(VECTOR_FILE) and os.path.exists(TEXT_FILE):
        index = faiss.read_index(VECTOR_FILE)

        with open(TEXT_FILE, "r") as f:
            texts = json.load(f)

        return index, texts

    # new store
    index = faiss.IndexFlatL2(384)
    return index, []


def save_vector_store(index, texts):
    os.makedirs("data/history", exist_ok=True)

    faiss.write_index(index, VECTOR_FILE)

    with open(TEXT_FILE, "w") as f:
        json.dump(texts, f, indent=2)


def is_similar(question, index, texts, threshold=0.6):
    if len(texts) == 0:
        return False

    q_vec = model.encode([question])
    D, I = index.search(np.array(q_vec), 1)

    return D[0][0] < threshold


def add_to_vector_store(question, index, texts):
    vec = model.encode([question])
    index.add(np.array(vec))
    texts.append(question)

    return index, texts