from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import get_settings

@lru_cache
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=get_settings().embedding_model)
