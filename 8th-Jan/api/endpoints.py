from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Optional
import os
import shutil
from datetime import datetime

from models.schemas import (
    SearchRequest, SearchResponse, PDFUploadResponse, HealthResponse
)
from services.search import SearchService
from services.vector_store import VectorStore

router = APIRouter(tags=["Search"])
search_service = SearchService()
vector_store = VectorStore()

@router.post("/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    """
    Search through indexed PDF documents
    
    - **query**: Search query text
    - **top_k**: Number of results to return (default: 5)
    - **pdf_filter**: Filter results by specific PDF filename
    """
    try:
        results = search_service.search_documents(
            query=request.query,
            top_k=request.top_k,
            pdf_filter=request.pdf_filter
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(
    file: UploadFile = File(..., description="PDF file to upload and index"),
    chunk_size: int = Query(500, description="Chunk size in characters"),
    overlap: int = Query(50, description="Overlap between chunks")
):
    """
    Upload and index a PDF document
    
    The PDF will be:
    1. Saved to server
    2. Extracted text content
    3. Split into chunks
    4. Embedded and indexed in vector database
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Create upload directory
        upload_dir = "data/uploaded_pdfs"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process and index PDF
        total_chunks = search_service.process_and_index_pdf(file_path)
        
        return PDFUploadResponse(
            message="PDF uploaded and indexed successfully",
            filename=file.filename,
            total_chunks=total_chunks,
            processed_at=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API and vector database health"""
    try:
        stats = vector_store.get_stats()
        return HealthResponse(
            status="healthy",
            vector_db_connected=True,
            embedding_model="text-embedding-ada-002",
            total_documents=stats["total_documents"]
        )
    except Exception as e:
        return HealthResponse(
            status="degraded",
            vector_db_connected=False,
            embedding_model="unknown",
            total_documents=0
        )

@router.get("/stats")
async def get_statistics():
    """Get search statistics"""
    stats = vector_store.get_stats()
    return {
        "vector_store_stats": stats,
        "timestamp": datetime.now(),
        "service": "PDF Vector Search"
    }