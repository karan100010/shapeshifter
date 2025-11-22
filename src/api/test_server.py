from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ShapeShifter Test API",
    description="Simplified test API for frontend integration",
    version="1.0.0"
)

# Enable CORS for frontend - must be before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    citations: Optional[List[dict]] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Simple chat endpoint that returns a mock response
    """
    return ChatResponse(
        response=f"I received your message: '{message.message}'. This is a test response from the backend. In production, this would connect to the RAG system to retrieve relevant documents and generate an AI response.",
        citations=[
            {"source": "test_document.pdf", "chunk": "Page 1, Section 1.1"},
            {"source": "sample_doc.txt", "chunk": "Line 42-58"}
        ]
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Simple upload endpoint that accepts files
    """
    try:
        # Read file content (for testing, we just validate it exists)
        contents = await file.read()
        file_size = len(contents)
        
        return {
            "filename": file.filename,
            "status": "success",
            "message": f"File '{file.filename}' uploaded successfully ({file_size} bytes)",
            "size": file_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting ShapeShifter Test API Server...")
    print("📍 Server running at: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("✅ CORS enabled for all origins")
    uvicorn.run(app, host="0.0.0.0", port=8000)
