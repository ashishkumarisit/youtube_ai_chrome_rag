"""
YouTube AI RAG Backend - FastAPI Application
Corrected version with proper imports and error handling
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import router - choose based on your directory structure:
# Option A: If you use flat structure (no app/ folder)
try:
    from rag import router
    logger.info("✓ Imported router from flat structure")
except ImportError:
    # Option B: If you create proper app/ directory structure
    try:
        from app.api.routes.rag import router
        logger.info("✓ Imported router from app/api/routes/")
    except ImportError as e:
        logger.error(f"Failed to import router: {e}")
        raise

# Initialize FastAPI app
app = FastAPI(
    title="YouTube AI RAG API",
    version="1.0.0",
    description="RAG system for YouTube video transcripts",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Frontend dev server
        "http://localhost:5173",      # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        # "https://yourdomain.com",   # Production domain
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Include API routes
app.include_router(router)

# Root endpoint
@app.get("/")
def root():
    """API root endpoint with documentation links."""
    return {
        "service": "YouTube AI RAG API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "rag_ask": "POST /api/v1/rag/ask",
            "docs": "/docs",
            "openapi": "/openapi.json"
        },
        "description": "RAG system for querying YouTube video transcripts"
    }

# Health check endpoint
@app.get("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "youtube-ai-rag",
        "version": "1.0.0"
    }

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_type": type(exc).__name__
        }
    )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting YouTube AI RAG API server...")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )