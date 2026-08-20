from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from app.core.config import get_settings
from app.services.transcript_service import TranscriptService
from app.services.chunk_service import ChunkService
from app.vectorstores.factory import get_vector_store

PROMPT = PromptTemplate(
    template="""You are a grounded YouTube RAG assistant.
Answer ONLY from the transcript context.
Do not use outside knowledge or invent facts.
If the answer is unavailable, say: I don't know based on the available transcript.
Mention approximate timestamps when useful.

Context:
{context}

Question:
{question}

Answer:""",
    input_variables=["context", "question"],
)

class RAGService:
    def __init__(self):
        s = get_settings()
        self.transcripts = TranscriptService()
        self.chunker = ChunkService()
        self.store = get_vector_store()
        self.model = ChatOpenAI(
            api_key=s.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            model=s.llm_model,
            temperature=s.temperature,
            max_tokens=s.max_tokens,
            max_retries=2,
        )
        self.chain = PROMPT | self.model | StrOutputParser()

    def ensure_index(self, video_id):
        if self.store.exists(video_id):
            return
        transcript = self.transcripts.fetch(video_id)
        chunks = self.chunker.create_chunks(transcript, video_id)
        if not chunks:
            raise RuntimeError("No transcript content available.")
        self.store.create(chunks, video_id)

    def ask(self, video_id, question):
        self.ensure_index(video_id)
        docs = self.store.retriever(video_id).invoke(question)
        context = "\n\n".join(
            f"Timestamp: {d.metadata.get('start', 0):.1f}s\n"
            f"Chunk: {d.metadata.get('chunk_id')}\n{d.page_content}"
            for d in docs
        )
        answer = self.chain.invoke({"context": context, "question": question})
        return {
            "answer": answer,
            "video_id": video_id,
            "sources": [
                {"video_id": d.metadata.get("video_id", video_id),
                 "chunk_id": d.metadata.get("chunk_id"),
                 "start": d.metadata.get("start"),
                 "duration": d.metadata.get("duration")}
                for d in docs
            ],
            "vector_store": get_settings().vector_store,
        }
