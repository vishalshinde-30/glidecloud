import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Ollama Configuration
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "nomic-embed-text")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # ChromaDB Configuration (instead of FAISS)
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
    
    # Embedding Configuration
    EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "768"))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))
    
    # API Configuration
    API_HOST = "0.0.0.0"
    API_PORT = 8000

settings = Settings()