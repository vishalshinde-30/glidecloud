#!/usr/bin/env python3
"""
Setup script for Ollama Vector Search API
"""
import json
import os
import requests
from services.search import search_service

def setup_sample_data():
    """Load sample data into the vector store"""
    sample_file = "./data/sample_docs.json"
    
    if not os.path.exists(sample_file):
        print("❌ Sample data file not found")
        return
    
    with open(sample_file, 'r') as f:
        sample_data = json.load(f)
    
    # Extract documents and metadata
    documents = [item["content"] for item in sample_data]
    metadata_list = [item["metadata"] for item in sample_data]
    
    print(f"📄 Loading {len(documents)} sample documents...")
    result = search_service.add_documents(documents, metadata_list)
    
    if result["success"]:
        print(f"✅ Successfully loaded {result['total_documents']} documents")
        print(f"⚠️  Failed to load: {result.get('failed', 0)} documents")
    else:
        print(f"❌ Failed to load sample data: {result['message']}")

def test_search():
    """Test the search functionality"""
    print("\n🔍 Testing search functionality...")
    
    # Test query
    from models.schemas import QueryWithVector
    
    query = QueryWithVector(
        query="What are cascade policies?",
        top_k=3
    )
    
    results = search_service.search(query)
    
    print(f"📊 Found {len(results)} results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Similarity: {result.similarity:.4f}")
        print(f"   Content: {result.content[:100]}...")
        print(f"   Metadata: {result.metadata}")

if __name__ == "__main__":
    print("🚀 Setting up Ollama Vector Search API")
    print("=" * 50)
    
    setup_sample_data()
    print("\n" + "=" * 50)
    test_search()
    
    print("\n✅ Setup complete! Run 'python app.py' to start the API server.")