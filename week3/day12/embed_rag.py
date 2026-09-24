import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
from abc import ABC, abstractmethod


def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


model = SentenceTransformer("all-MiniLM-L6-v2") #384
text = "Machine learning is fun."

# embedding=model.encode(text)
# print(embedding.shape)
# print(embedding[:10])

t1="There are 24 paid leaves"
t2="cat is a wild animal"
t3= "How to play cricket"
t4="How to play football"
t5="How to cook pasta"
t6="How to repair a laptop"

v1=model.encode(t1)
v2=model.encode(t2)
v3=model.encode(t3)
v4=model.encode(t4)
v5=model.encode(t5)
v6=model.encode(t6)


class V6Interface(ABC):
    @abstractmethod
    def encode(self, text: str) -> np.ndarray:
        pass

    @abstractmethod
    def add(self, text: str):
        pass

    @abstractmethod
    def most_similar(self, query: str, top_k: int = 3):
        pass


class v6(V6Interface):
    """Simple in-memory vector store using the global SentenceTransformer model."""

    def __init__(self):
        self.texts = []
        self.vectors = []

    def encode(self, text: str) -> np.ndarray:
        return model.encode(text)

    def add(self, text: str):
        vec = self.encode(text)
        self.texts.append(text)
        self.vectors.append(vec)
        return len(self.texts) - 1

    def most_similar(self, query: str, top_k: int = 3):
        if not self.vectors:
            return []
        qv = self.encode(query)
        sims = [cosine_similarity(qv, v) for v in self.vectors]
        idxs = np.argsort(sims)[::-1][:top_k]
        return [(self.texts[i], float(sims[i])) for i in idxs]



store = v6()
for t in (t1, t2, t3, t4, t5, t6):
    store.add(t)


print(store.most_similar("How do I  pasta?", top_k=3))