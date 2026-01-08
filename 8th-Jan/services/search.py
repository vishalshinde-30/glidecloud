from typing import Dict, List, Any
from datetime import datetime
from services.embedding import EmbeddingService
from services.vector_store import VectorStore
from services.pdf_processor import PDFProcessor

class SearchService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.pdf_processor = PDFProcessor()
        
        # Load sample data for demonstration
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample documents for testing"""
        sample_docs = [
            {
                "text": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience.",
                "metadata": {"source_pdf": "ai_basics.pdf", "page": 1, "chunk_index": 0}
            },
            {
                "text": "Deep learning uses neural networks with multiple layers to analyze various factors of data.",
                "metadata": {"source_pdf": "ai_basics.pdf", "page": 2, "chunk_index": 1}
            },
            {
                "text": "Vector databases store embeddings that represent text, images, or other data as high-dimensional vectors.",
                "metadata": {"source_pdf": "vector_db.pdf", "page": 1, "chunk_index": 0}
            },
            {
                "text": "Embedding models convert text into numerical vectors that capture semantic meaning.",
                "metadata": {"source_pdf": "embeddings.pdf", "page": 3, "chunk_index": 2}
            },
            {
                "text": "Similarity search finds the closest vectors in the database to a query vector.",
                "metadata": {"source_pdf": "vector_db.pdf", "page": 2, "chunk_index": 1}
            }
        ]
        
        for doc in sample_docs:
            embedding = self.embedding_service.get_embedding(doc["text"])
            self.vector_store.add_document(embedding, doc["text"], doc["metadata"])
    
    def search_documents(self, query: str, top_k: int = 5, pdf_filter: str = None) -> Dict[str, Any]:
        """Main search function"""
        start_time = datetime.now()
        
        # 1. Embed query
        query_vector = self.embedding_service.get_embedding(query)
        
        # 2. Search in vector store
        search_results = self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
            pdf_filter=pdf_filter
        )
        
        # 3. Process results
        chunks = []
        pdf_counts = {}
        
        for result in search_results:
            metadata = result["metadata"]
            chunk_data = {
                "text": result["text"],
                "similarity_score": round(result["similarity"], 4),
                "source_pdf": metadata.get("source_pdf", "unknown"),
                "page_number": metadata.get("page", 1),
                "chunk_index": metadata.get("chunk_index", 0)
            }
            chunks.append(chunk_data)
            
            # Count for pie chart data
            pdf_name = metadata.get("source_pdf", "unknown")
            pdf_counts[pdf_name] = pdf_counts.get(pdf_name, 0) + 1
        
        # 4. Calculate search time
        search_time = datetime.now() - start_time
        
        return {
            "query": query,
            "total_chunks_found": len(chunks),
            "chunks": chunks,
            "pdf_distribution": pdf_counts,
            "search_time": datetime.now(),
            "search_duration_ms": round(search_time.total_seconds() * 1000, 2)
        }
    
    def process_and_index_pdf(self, pdf_path: str) -> int:
        """Process PDF and index its content"""
        # Extract text from PDF
        text_chunks = self.pdf_processor.extract_text_from_pdf(pdf_path)
        
        total_indexed = 0
        for chunk_data in text_chunks:
            # Split into smaller chunks
            smaller_chunks = self.pdf_processor.split_into_chunks(chunk_data["text"])
            
            for i, chunk_text in enumerate(smaller_chunks):
                # Generate embedding
                embedding = self.embedding_service.get_embedding(chunk_text)
                
                # Prepare metadata
                metadata = {
                    "source_pdf": chunk_data["pdf_name"],
                    "page": chunk_data["page_number"],
                    "chunk_index": i,
                    "total_pages": chunk_data["total_pages"]
                }
                
                # Add to vector store
                self.vector_store.add_document(embedding, chunk_text, metadata)
                total_indexed += 1
        
        return total_indexed