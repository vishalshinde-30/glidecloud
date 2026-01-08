from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class PDFUploadResponse(BaseModel):
    message: str
    filename: str
    total_chunks: int
    processed_at: datetime

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    pdf_filter: Optional[str] = None

class ChunkResult(BaseModel):
    text: str
    similarity_score: float
    source_pdf: str
    page_number: int
    chunk_index: int

class SearchResponse(BaseModel):
    query: str
    total_chunks_found: int
    chunks: List[ChunkResult]
    pdf_distribution: Dict[str, int]
    search_time: datetime

class HealthResponse(BaseModel):
    status: str
    vector_db_connected: bool
    embedding_model: str
    total_documents: int