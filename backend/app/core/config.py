from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openrouter_api_key: str
    llm_model: str = "openai/gpt-4.1-mini"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_store: str = "faiss"
    faiss_root: str = "data/faiss"
    chunk_size: int = 700
    chunk_overlap: int = 120
    retrieval_k: int = 5
    retrieval_fetch_k: int = 15
    retrieval_lambda: float = 0.7
    max_tokens: int = 700
    temperature: float = 0.2
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None
    qdrant_collection: str = "youtube_transcripts"
    azure_search_endpoint: str | None = None
    azure_search_api_key: str | None = None
    azure_search_index: str = "youtube-transcripts"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings():
    return Settings()
