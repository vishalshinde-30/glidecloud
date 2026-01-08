# Ollama Vector Search API with FastAPI

A backend RESTful API developed using **FastAPI**, **Ollama**, and a **Vector Database (FAISS)**.  
This project demonstrates how to convert user queries into vectors (embeddings) using Ollama and perform **vector-based search**.

---

## Key Highlights
- REST API built with FastAPI
- Vector creation using **Ollama embeddings**
- Vector storage and similarity search using **FAISS**
- Query + vector-based retrieval
- Clean and modular project structure

---

## Technologies Used
- Python
- FastAPI
- Ollama
- FAISS (Vector Database)
- NumPy
- Uvicorn

---

## API Validation & Testing
- All API endpoints were tested using **Swagger UI**
- Vector creation and search were validated through API responses
- Ollama was used locally for generating embeddings

---

## Getting Started

### Prerequisites
- Python 3.9+
- Ollama installed and running locally

---

### Steps to Run the Project

1. **Install Ollama**
   - Download and install from: https://ollama.com

2. **Pull embedding model**
   - ollama pull nomic-embed-text

3. **Install required libraries**
   - pip install -r requirements.txt

4. **Run the server**
   - uvicorn main:app --reload

3. **Access API documentation**
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
