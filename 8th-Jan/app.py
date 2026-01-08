from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from api.endpoints import router as api_router

# Initialize FastAPI app
app = FastAPI(
    title="PDF Vector Search API",
    description="API for searching through PDF documents using vector embeddings",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Home page with API documentation"""
    html_content = """
    <html>
        <head>
            <title>PDF Vector Search API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .method { color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold; }
                .post { background: #49cc90; }
                .get { background: #61affe; }
            </style>
        </head>
        <body>
            <h1>📚 PDF Vector Search API</h1>
            <p>Welcome to the PDF search API. Upload PDFs and search through them using semantic search.</p>
            
            <h2>Available Endpoints:</h2>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/upload-pdf</strong> - Upload and index a PDF
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <strong>/api/v1/search</strong> - Search through indexed documents
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/health</strong> - Check API health
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <strong>/api/v1/stats</strong> - Get statistics
            </div>
            
            <h2>Quick Links:</h2>
            <ul>
                <li><a href="/docs">Interactive API Documentation (Swagger)</a></li>
                <li><a href="/redoc">Alternative Documentation (ReDoc)</a></li>
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "message": "PDF Vector Search API is running",
        "timestamp": "2024-01-08",
        "endpoints": [
            {"method": "POST", "path": "/api/v1/upload-pdf", "desc": "Upload PDF"},
            {"method": "POST", "path": "/api/v1/search", "desc": "Search documents"},
            {"method": "GET", "path": "/docs", "desc": "API Documentation"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)