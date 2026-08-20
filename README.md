# YouTube AI Chrome RAG

Runnable architecture:
Chrome Extension -> API Gateway (FastAPI/CORS boundary) -> Transcript Service + RAG Service -> Vector Store -> MMR Retriever -> OpenRouter LLM -> Chrome.

Default local vector store is FAISS. Qdrant and Azure AI Search are provided as adapter extension points.

## Backend
```powershell
cd backend
py -3.12 -m venv venv312
.\venv312\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# edit .env and set OPENROUTER_API_KEY
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Check http://127.0.0.1:8000/health and /docs.

## Chrome
Open chrome://extensions -> Developer mode -> Load unpacked -> select `chrome-extension`.

Open a YouTube video, click the extension icon, and ask questions.

The first question for a video lazily fetches its transcript, chunks it, embeds it and creates a video-specific FAISS index. Later questions reuse that index.

Never put the OpenRouter key in the extension.

## Vector stores
Set `VECTOR_STORE=faiss` for the fully runnable local version.
`qdrant` and `azure` adapters are deliberately separated so they can be implemented/swapped without changing the RAG service.
