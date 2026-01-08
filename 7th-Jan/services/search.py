import logging
from typing import List, Optional
from models.schemas import QueryWithVector, SearchResult
from services.embedding import embedding_service
from services.vector_store import vector_store

logger = logging.getLogger(__name__)

class SearchService:
    """Service for handling search operations"""
    
    def __init__(self):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
    
    def search(self, query_data: QueryWithVector) -> List[SearchResult]:
        """
        Perform search combining text query and optional custom vector
        
        Args:
            query_data: QueryWithVector object containing search parameters
            
        Returns:
            List of SearchResult objects
        """
        # Step 1: Generate embedding for text query
        query_embedding = self.embedding_service.generate_embedding(query_data.query)
        
        if query_embedding is None:
            logger.error(f"Failed to generate embedding for query: {query_data.query}")
            return []
        
        # Step 2: Combine with custom vector if provided
        if query_data.vectors:
            combined_embedding = self.embedding_service.combine_vectors(
                text_embedding=query_embedding,
                custom_vector=query_data.vectors,
                weight_text=query_data.weight_text,
                weight_custom=query_data.weight_custom
            )
        else:
            combined_embedding = query_embedding
        
        # Step 3: Search in vector store
        search_results = self.vector_store.search(
            query_embedding=combined_embedding,
            top_k=query_data.top_k
        )
        
        # Step 4: Format results
        results = []
        for idx, similarity in search_results:
            try:
                content, metadata = self.vector_store.get_document(idx)
                results.append(SearchResult(
                    content=content,
                    similarity=similarity,
                    metadata=metadata,
                    index=idx
                ))
            except Exception as e:
                logger.error(f"Error retrieving document {idx}: {str(e)}")
        
        return results
    
    def add_documents(self, documents: List[str], 
                     metadata_list: Optional[List[dict]] = None) -> dict:
        """
        Add documents to the vector store
        
        Args:
            documents: List of document texts
            metadata_list: Optional list of metadata dictionaries
            
        Returns:
            Dictionary with operation result
        """
        if metadata_list is None:
            metadata_list = [{} for _ in documents]
        
        # Generate embeddings for all documents
        logger.info(f"Generating embeddings for {len(documents)} documents...")
        embeddings = self.embedding_service.batch_generate_embeddings(documents)
        
        # Filter out documents with failed embeddings
        valid_docs = []
        valid_embeddings = []
        valid_metadata = []
        
        for doc, emb, meta in zip(documents, embeddings, metadata_list):
            if emb is not None:
                valid_docs.append(doc)
                valid_embeddings.append(emb)
                valid_metadata.append(meta)
            else:
                logger.warning(f"Failed to generate embedding for document: {doc[:50]}...")
        
        if not valid_docs:
            return {"success": False, "message": "No valid embeddings generated"}
        
        # Add to vector store
        self.vector_store.add_documents(
            documents=valid_docs,
            embeddings=valid_embeddings,
            metadata_list=valid_metadata
        )
        
        return {
            "success": True,
            "message": f"Added {len(valid_docs)} documents to vector store",
            "total_documents": len(valid_docs),
            "failed": len(documents) - len(valid_docs)
        }
    
    def get_store_info(self) -> dict:
        """Get information about the vector store"""
        return self.vector_store.get_info()
    
    def clear_store(self) -> dict:
        """Clear all documents from the vector store"""
        self.vector_store.clear()
        return {"success": True, "message": "Vector store cleared"}

# Singleton instance
search_service = SearchService()