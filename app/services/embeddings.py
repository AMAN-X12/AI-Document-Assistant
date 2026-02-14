import os
import google.generativeai as genai
from app.core.config import key

genai.configure(api_key=key),
def get_embeddings(texts : str):
    result = genai.embed_content(
    model = "models/gemini-embedding-001",
    content=texts,
    task_type="retrieval_document"
    )
    return result["embedding"]
