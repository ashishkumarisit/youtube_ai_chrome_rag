import os, re
from langchain_community.vectorstores import FAISS
from app.core.config import get_settings
from app.services.embedding_service import get_embeddings

class FAISSStore:
    def __init__(self):
        s = get_settings()
        self.root = s.faiss_root
        self.embeddings = get_embeddings()
        self.k, self.fetch_k, self.lam = s.retrieval_k, s.retrieval_fetch_k, s.retrieval_lambda

    def path(self, video_id):
        safe = re.sub(r"[^A-Za-z0-9_-]", "_", video_id)
        return os.path.join(self.root, safe)

    def exists(self, video_id):
        return os.path.exists(os.path.join(self.path(video_id), "index.faiss"))

    def create(self, documents, video_id):
        path = self.path(video_id)
        os.makedirs(path, exist_ok=True)
        store = FAISS.from_documents(documents, self.embeddings)
        store.save_local(path)
        return store

    def retriever(self, video_id):
        store = FAISS.load_local(self.path(video_id), self.embeddings,
                                 allow_dangerous_deserialization=True)
        return store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": self.k, "fetch_k": self.fetch_k, "lambda_mult": self.lam}
        )
