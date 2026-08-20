class QdrantStore:
    # Production adapter extension point.
    def exists(self, video_id): raise NotImplementedError("Implement Qdrant persistence/retrieval or use VECTOR_STORE=faiss.")
    def create(self, documents, video_id): raise NotImplementedError
    def retriever(self, video_id): raise NotImplementedError
