import os
import google.generativeai as genai
from app.core.config import key


def get_embeddings(texts : str):
    result = genai.embed_content(
    genai.configure(api_key=key),
    model = "models/embedding-001",
    context=texts
    )
    return result["embedding"]
