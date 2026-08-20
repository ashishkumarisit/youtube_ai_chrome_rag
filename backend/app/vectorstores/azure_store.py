class AzureAIStore:
    # Production adapter extension point for Azure AI Search vector/hybrid/semantic search.
    def exists(self, video_id): raise NotImplementedError("Implement Azure AI Search index operations or use VECTOR_STORE=faiss.")
    def create(self, documents, video_id): raise NotImplementedError
    def retriever(self, video_id): raise NotImplementedError
