import chromadb
from chromadb.config import Settings
import numpy as np
import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from config import settings
import json

logger = logging.getLogger(__name__)

class ChromaVectorStore:
    """Vector store using ChromaDB for similarity search (Windows compatible)"""
    
    def __init__(self):
        self.db_path = settings.CHROMA_DB_PATH
        self.dimension = settings.EMBEDDING_DIMENSION
        
        # Create directory if it doesn't exist
        os.makedirs(self.db_path, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}  # Cosine similarity
        )
        
        # Track document count
        self.document_count = self.collection.count()
        
        logger.info(f"ChromaDB initialized at {self.db_path} with {self.document_count} documents")
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]], 
                     metadata_list: Optional[List[Dict[str, Any]]] = None):
        """
        Add documents to the vector store
        
        Args:
            documents: List of document texts
            embeddings: List of embeddings for each document
            metadata_list: Optional list of metadata dictionaries
        """
        if metadata_list is None:
            metadata_list = [{} for _ in documents]
        
        # Generate unique IDs for each document
        import uuid
        ids = [str(uuid.uuid4()) for _ in documents]
        
        # Add to ChromaDB collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadata_list
        )
        
        # Update document count
        self.document_count = self.collection.count()
        
        logger.info(f"Added {len(documents)} documents to vector store. Total: {self.document_count}")
        
        return ids
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            
        Returns:
            List of tuples (index, similarity_score)
        """
        if self.document_count == 0:
            return []
        
        try:
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, self.document_count),
                include=["documents", "metadatas", "distances"]
            )
            
            search_results = []
            
            if results['distances'] and results['distances'][0]:
                for i, (distance, doc, metadata) in enumerate(zip(
                    results['distances'][0],
                    results['documents'][0],
                    results['metadatas'][0]
                )):
                    # Convert distance to similarity score
                    # ChromaDB returns cosine distance (0-2), convert to similarity (0-1)
                    similarity = 1 - (distance / 2) if distance is not None else 0.0
                    
                    # We need to return the index, but ChromaDB doesn't give us the original index
                    # We'll use the position in results as a pseudo-index
                    search_results.append((i, float(similarity)))
            
            return search_results
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []
    
    def get_document(self, result_index: int) -> Tuple[str, Dict[str, Any]]:
        """Get document and metadata by result index"""
        try:
            # Get all documents from the collection
            all_docs = self.collection.get()
            
            if result_index < len(all_docs['documents']):
                return (
                    all_docs['documents'][result_index],
                    all_docs['metadatas'][result_index] if all_docs['metadatas'] else {}
                )
            else:
                logger.error(f"Document index {result_index} out of range")
                return "", {}
                
        except Exception as e:
            logger.error(f"Error getting document: {str(e)}")
            return "", {}
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the vector store"""
        return {
            'total_documents': self.document_count,
            'embedding_dimension': self.dimension,
            'chroma_db_path': self.db_path,
            'ollama_model': settings.OLLAMA_MODEL,
            'collection_name': 'documents'
        }
    
    def clear(self):
        """Clear all documents from the vector store"""
        try:
            # Delete the collection
            self.client.delete_collection("documents")
            logger.info("Deleted existing collection")
        except Exception as e:
            logger.warning(f"Error deleting collection (may not exist): {str(e)}")
        
        # Create new collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.document_count = 0
        
        logger.info("Cleared vector store")

# Singleton instance
vector_store = ChromaVectorStore()