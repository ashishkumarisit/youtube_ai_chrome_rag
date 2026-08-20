from app.core.config import get_settings
from app.vectorstores.faiss_store import FAISSStore
from app.vectorstores.qdrant_store import QdrantStore
from app.vectorstores.azure_store import AzureAIStore

def get_vector_store():
    name = get_settings().vector_store.lower()
    if name == "faiss": return FAISSStore()
    if name == "qdrant": return QdrantStore()
    if name in {"azure", "azure_ai_search"}: return AzureAIStore()
    raise ValueError(f"Unsupported VECTOR_STORE={name}")
