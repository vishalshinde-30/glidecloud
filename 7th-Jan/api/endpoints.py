from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import QueryWithVector, Document, SearchResult, HealthResponse
from services.search import search_service
from services.embedding import embedding_service

# Create router - THIS LINE WAS MISSING
router = APIRouter()

@router.post("/search", response_model=List[SearchResult])
async def search_documents(query_data: QueryWithVector):
    """Search documents"""
    try:
        results = search_service.search(query_data)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-documents")
async def add_documents(documents: List[Document]):
    """Add documents"""
    try:
        # Extract documents and metadata
        doc_texts = [doc.content for doc in documents]
        metadata_list = [doc.metadata for doc in documents]
        
        result = search_service.add_documents(doc_texts, metadata_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/store-info")
async def get_store_info():
    """Get vector store info"""
    try:
        info = search_service.get_store_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear-store")
async def clear_store():
    """Clear all documents"""
    try:
        result = search_service.clear_store()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check"""
    ollama_available = embedding_service.test_connection()
    store_info = search_service.get_store_info()
    
    return HealthResponse(
        status="healthy" if ollama_available else "degraded",
        ollama_available=ollama_available,
        vector_store_ready=store_info['total_documents'] > 0,
        details={
            "ollama_model": store_info['ollama_model'],
            "total_documents": store_info['total_documents'],
            "embedding_dimension": store_info['embedding_dimension']
        }
    )