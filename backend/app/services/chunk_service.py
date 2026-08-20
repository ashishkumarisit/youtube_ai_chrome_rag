from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import get_settings

class ChunkService:
    def __init__(self):
        s = get_settings()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=s.chunk_size, chunk_overlap=s.chunk_overlap
        )

    def create_chunks(self, transcript, video_id):
        docs = [
            Document(
                page_content=item.text,
                metadata={"video_id": video_id, "source": "youtube",
                          "start": float(item.start), "duration": float(item.duration)}
            )
            for item in transcript
        ]
        chunks = self.splitter.split_documents(docs)
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = i
        return chunks
