import ollama
import numpy as np
from typing import List, Optional
import logging
from config import settings

logger = logging.getLogger(__name__)

class OllamaEmbeddingService:
    """Service for generating embeddings using Ollama"""
    
    def __init__(self):
        self.model = settings.OLLAMA_MODEL
        self.base_url = settings.OLLAMA_BASE_URL
        self.dimension = settings.EMBEDDING_DIMENSION
        
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for text using Ollama
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding
        """
        try:
            response = ollama.embeddings(
                model=self.model,
                prompt=text
            )
            embedding = response.get("embedding", [])
            
            if not embedding:
                logger.warning(f"No embedding returned for text: {text[:50]}...")
                return None
                
            # Ensure the embedding has correct dimension
            if len(embedding) != self.dimension:
                logger.warning(f"Embedding dimension mismatch: {len(embedding)} != {self.dimension}")
                # Pad or truncate to correct dimension
                if len(embedding) < self.dimension:
                    embedding = embedding + [0.0] * (self.dimension - len(embedding))
                else:
                    embedding = embedding[:self.dimension]
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return None
    
    def batch_generate_embeddings(self, texts: List[str]) -> List[Optional[List[float]]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings (some may be None if failed)
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    def combine_vectors(self, 
                       text_embedding: List[float], 
                       custom_vector: List[float],
                       weight_text: float = 0.7,
                       weight_custom: float = 0.3) -> List[float]:
        """
        Combine text embedding with custom vector using weighted sum
        
        Args:
            text_embedding: Text embedding from Ollama
            custom_vector: Custom vector provided by user
            weight_text: Weight for text embedding
            weight_custom: Weight for custom vector
            
        Returns:
            Combined vector
        """
        # Ensure vectors have same dimension
        min_dim = min(len(text_embedding), len(custom_vector))
        text_embedding = text_embedding[:min_dim]
        custom_vector = custom_vector[:min_dim]
        
        # Weighted combination
        combined = [
            (weight_text * t + weight_custom * c) 
            for t, c in zip(text_embedding, custom_vector)
        ]
        
        # Normalize the combined vector
        norm = np.linalg.norm(combined)
        if norm > 0:
            combined = [v / norm for v in combined]
        
        return combined
    
    def test_connection(self) -> bool:
        """Test if Ollama is available"""
        try:
            ollama.list()
            return True
        except Exception as e:
            logger.error(f"Ollama connection test failed: {str(e)}")
            return False

# Singleton instance
embedding_service = OllamaEmbeddingService()