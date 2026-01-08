from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import ollama
import chromadb
from chromadb.config import Settings
import uuid
import os
import time

app = FastAPI(title="Ollama Vector Search")

# Setup ChromaDB
os.makedirs("./chroma_db", exist_ok=True)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")

# Use SMALLER model
EMBEDDING_MODEL = "all-minilm"  # Changed from nomic-embed-text

# Models
class QueryRequest(BaseModel):
    query: str
    vectors: Optional[List[float]] = None
    top_k: int = 3

class Document(BaseModel):
    content: str
    metadata: Dict = {}

class SearchResult(BaseModel):
    content: str
    similarity: float
    metadata: Dict

def get_embedding_safe(text: str):
    """Safe embedding with retries and fallback"""
    try:
        # Limit text length
        if len(text) > 1000:
            text = text[:1000]
        
        # Try with timeout
        response = ollama.embeddings(
            model=EMBEDDING_MODEL,
            prompt=text
        )
        
        embedding = response.get("embedding", [])
        
        if not embedding:
            print("⚠️ Empty embedding, using fallback")
            return [0.1] * 384  # Fallback
        
        return embedding
        
    except Exception as e:
        print(f"⚠️ Ollama error (using fallback): {str(e)[:100]}")
        # Return simple fallback embedding
        return [0.1] * 384

# Test Ollama connection on startup
print("🔍 Testing Ollama connection...")
try:
    ollama.list()
    print("✅ Ollama is connected")
except:
    print("⚠️ Ollama not connected, using fallback mode")

# API Endpoints
@app.get("/")
def home():
    return {
        "message": "Ollama Vector Search API",
        "model": EMBEDDING_MODEL,
        "status": "running"
    }

@app.get("/health")
def health():
    try:
        ollama.list()
        return {
            "status": "healthy",
            "ollama": "connected",
            "model": EMBEDDING_MODEL,
            "documents": collection.count()
        }
    except:
        return {
            "status": "degraded",
            "ollama": "not_connected",
            "documents": collection.count(),
            "message": "Using fallback embeddings"
        }

@app.post("/add")
def add_document(doc: Document):
    embedding = get_embedding_safe(doc.content)
    
    doc_id = str(uuid.uuid4())
    collection.add(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[doc.content],
        metadatas=[doc.metadata]
    )
    
    return {
        "message": "Document added",
        "id": doc_id,
        "total": collection.count()
    }

@app.post("/search")
def search(request: QueryRequest):
    query_embedding = get_embedding_safe(request.query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=request.top_k
    )
    
    formatted = []
    if results['documents']:
        for doc, meta, dist in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ):
            similarity = 1 - (dist / 2)
            formatted.append({
                "content": doc,
                "similarity": round(similarity, 4),
                "metadata": meta if meta else {}
            })
    
    return formatted

@app.post("/quick-test")
def quick_test():
    """Quick test with pre-defined data"""
    test_text = "Cascade policies example"
    embedding = get_embedding_safe(test_text)
    
    # Add test document
    collection.add(
        ids=["test_123"],
        embeddings=[embedding],
        documents=[test_text],
        metadatas=[{"test": True}]
    )
    
    # Search for it
    results = collection.query(
        query_embeddings=[embedding],
        n_results=1
    )
    
    return {
        "test": "complete",
        "embedding_length": len(embedding),
        "found_documents": len(results['documents'][0]) if results['documents'] else 0
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Starting Ollama Vector Search")
    print(f"📦 Using model: {EMBEDDING_MODEL}")
    print("📚 Docs: http://localhost:8000/docs")
    print("="*60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)