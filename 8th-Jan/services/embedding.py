import numpy as np
from typing import List

class EmbeddingService:
    def __init__(self, model_name: str = "text-embedding-ada-002"):
        self.model_name = model_name
        # In production, load actual model like sentence-transformers or OpenAI
        print(f"Initialized embedding model: {model_name}")
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text
        For demo, returns random embedding. Replace with actual model.
        """
        # Simulate embedding generation
        np.random.seed(hash(text) % 10000)
        embedding = np.random.rand(384).tolist()  # 384-dim vector
        return embedding
    
    def embed_query(self, query: str) -> List[float]:
        """Alias for get_embedding"""
        return self.get_embedding(query)
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts"""
        return [self.get_embedding(text) for text in texts]