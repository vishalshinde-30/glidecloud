from typing import List, Dict, Any
import numpy as np
from datetime import datetime

class VectorStore:
    def __init__(self):
        self.vectors = []  # List of embeddings
        self.metadata = []  # List of metadata
        self.documents = []  # List of document texts
        print("Initialized in-memory vector store")
    
    def add_document(self, embedding: List[float], text: str, metadata: Dict[str, Any]):
        """Add document to vector store"""
        self.vectors.append(embedding)
        self.documents.append(text)
        self.metadata.append(metadata)
    
    def search(self, query_vector: List[float], top_k: int = 5, pdf_filter: str = None) -> List[Dict[str, Any]]:
        """Search for similar vectors"""
        if not self.vectors:
            return []
        
        # Convert to numpy for efficient computation
        query_vec = np.array(query_vector)
        vectors = np.array(self.vectors)
        
        # Calculate cosine similarity
        similarities = np.dot(vectors, query_vec) / (
            np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_vec)
        )
        
        # Get top_k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Prepare results
        results = []
        for idx in top_indices:
            if pdf_filter and self.metadata[idx].get("source_pdf") != pdf_filter:
                continue
                
            result = {
                "id": idx,
                "text": self.documents[idx],
                "similarity": float(similarities[idx]),
                "metadata": self.metadata[idx]
            }
            results.append(result)
        
        return results[:top_k]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        return {
            "total_documents": len(self.documents),
            "vector_dimension": len(self.vectors[0]) if self.vectors else 0,
            "unique_sources": len(set(m.get("source_pdf", "") for m in self.metadata))
        }