from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from api.endpoints import router
from config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title="Ollama Vector Search API",
    description="API for semantic search using Ollama embeddings and FAISS vector store",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Ollama Vector Search API",
        "docs": "/docs",
        "endpoints": {
            "search": "POST /api/v1/search",
            "add_documents": "POST /api/v1/add-documents",
            "store_info": "GET /api/v1/store-info",
            "health": "GET /api/v1/health"
        }
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    from services.embedding import embedding_service
    
    # Test Ollama connection
    if embedding_service.test_connection():
        logging.info(f"✅ Ollama is available (model: {settings.OLLAMA_MODEL})")
    else:
        logging.warning("⚠️ Ollama is not available. Check if Ollama is running.")

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level="info"
    )