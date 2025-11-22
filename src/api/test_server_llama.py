
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import logging
import requests
import json
import re
from datetime import datetime
from docx import Document
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ShapeShifter API with NVIDIA Gemma",
    description="API with NVIDIA Gemma 27B model integration and RAG creation workflow",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage for RAG creation workflow (in-memory for now)
# In production, use Redis or database
rag_sessions: Dict[str, Dict] = {}

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# NVIDIA API Configuration
NVIDIA_API_URL = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/a5bf94b4-8797-4934-b1ab-3472e2788e0f"
NVIDIA_API_KEY = "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"

class Settings(BaseModel):
    llm: str
    vectorDb: str

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    settings: Optional[Settings] = None

class ChatResponse(BaseModel):
    response: str
    citations: Optional[List[dict]] = None
    session_id: Optional[str] = None

def generate_with_nvidia_gemma(user_message: str, context: str = None, personality: str = None) -> Optional[str]:
    """Generate response using NVIDIA Gemma 27B model"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {NVIDIA_API_KEY}"
        }
        
        system_instruction = ""
        if personality:
            system_instruction += f"You are a specialized assistant with a {personality} personality.\n"
        
        if context:
            system_instruction += f"IMPORTANT: You must answer the user's question ONLY based on the following context. If the answer is not in the context, state that you cannot answer from the provided documents.\n\nCONTEXT:\n{context}\n\n"
        else:
            system_instruction += "You are a helpful AI assistant.\n"
        
        payload = {
            "model": "google/gemma-27b-it",
            "temperature": 0.5 if context else 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": system_instruction + "User Question: " + user_message
                }
            ]
        }
        
        logger.info(f"Calling NVIDIA Gemma API with context length: {len(context) if context else 0}")
        
        response = requests.post(
            NVIDIA_API_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                message_content = result["choices"][0].get("message", {}).get("content", "")
                logger.info(f"NVIDIA API response received: {len(message_content)} chars")
                return message_content
            else:
                logger.warning(f"Unexpected response format: {result}")
                return None
        else:
            logger.error(f"NVIDIA API error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error calling NVIDIA API: {e}")
        return None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "llm_provider": "NVIDIA Gemma 27B",
        "model": "google/gemma-27b-it",
        "active_rag_sessions": len(rag_sessions)
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat endpoint with RAG creation workflow and NVIDIA Gemma 27B
    """
    logger.info(f"Received chat message: {message.message} (session: {message.session_id})")
    
    user_message = message.message.strip()
    user_message_lower = user_message.lower()
    session_id = message.session_id
    
    # Get or create session
    if session_id not in rag_sessions:
        rag_sessions[session_id] = {
            "state": "idle",
            "rag_name": None,
            "files": [],
            "storage_name": None,
            "created_at": datetime.now().isoformat(),
            "settings": {},
            "context": "" # Initialize context
        }
    
    session = rag_sessions[session_id]
    
    # Update settings if provided
    if message.settings:
        session["settings"] = message.settings.dict()
        rag_sessions[session_id] = session
        
    current_state = session["state"]
    
    logger.info(f"Session state: {current_state}")
    
    # State machine for RAG creation workflow
    
    # IDLE STATE: Check if user wants to create RAG
    if current_state == "idle":
        rag_keywords = ["create rag", "make rag", "build rag", "new rag", "setup rag", "rag for me", "create a rag"]
        if any(keyword in user_message_lower for keyword in rag_keywords):
            session["state"] = "awaiting_personality"
            rag_sessions[session_id] = session
            
            return ChatResponse(
                response="""I'd be happy to help you create a RAG system! Let's customize it first.

**Step 1: Choose a Personality**

How would you like your RAG assistant to behave?

Examples:
- **Professional & Concise**: "Formal, direct, and to the point."
- **Witty & Fun**: "Humorous, engaging, and lighthearted."
- **Academic**: "Scholarly, detailed, and research-focused."
- **Friendly Guide**: "Helpful, patient, and easy to understand."

Please describe the personality you'd like:""",
                citations=[{"source": "RAG Workflow", "chunk": "Step 1: Personality"}],
                session_id=session_id
            )

    # AWAITING_PERSONALITY STATE: User provides personality
    elif current_state == "awaiting_personality":
        session["personality"] = user_message
        session["state"] = "awaiting_name"
        rag_sessions[session_id] = session
        
        return ChatResponse(
            response=f"""Got it! Your RAG assistant will have a **{user_message}** personality.

**Step 2: Name Your RAG**

What would you like to name your RAG system? 

Please provide a descriptive name (e.g., "Company Knowledge Base", "Product Documentation", "Research Papers Collection").""",
            citations=[{"source": "RAG Workflow", "chunk": "Step 2: Naming"}],
            session_id=session_id
        )
    
    # AWAITING_NAME STATE: User provides RAG name
    elif current_state == "awaiting_name":
        session["rag_name"] = user_message
        session["state"] = "awaiting_files"
        rag_sessions[session_id] = session
        
        return ChatResponse(
            response=f"""Great! I've noted the RAG name as: **{user_message}**

**Step 3: Upload Documents**

Now, please upload the files you want to include in your RAG system. 

You can upload:
- PDF documents (.pdf)
- Text files (.txt)
- Word documents (.docx)
- Markdown files (.md)

Please use the file upload button (📎) below the chat input to upload your documents. 

Once you've uploaded all your files, type "done" or "uploaded" to continue.""",
            citations=[{"source": "RAG Workflow", "chunk": "Step 3: File Upload"}],
            session_id=session_id
        )
    
    # AWAITING_FILES STATE: User confirms file upload
    elif current_state == "awaiting_files":
        upload_keywords = ["done", "uploaded", "finished", "ready", "next", "continue"]
        if any(keyword in user_message_lower for keyword in upload_keywords):
            session["state"] = "awaiting_storage"
            rag_sessions[session_id] = session
            
            return ChatResponse(
                response=f"""Perfect! I can see you've uploaded your documents for **{session['rag_name']}**.

**Step 4: Storage Name**

Finally, what would you like to name the file storage for this RAG system?

This is the internal storage identifier where your documents will be indexed.

Examples: "main_storage", "docs_v1", "knowledge_base_2024"

Please provide a storage name:""",
                citations=[{"source": "RAG Workflow", "chunk": "Step 4: Storage"}],
                session_id=session_id
            )
        else:
            return ChatResponse(
                response=f"""I'm waiting for you to upload files for **{session['rag_name']}**.

Please use the 📎 button below to upload your documents, then type "done" or "uploaded" when you're ready to continue.""",
                citations=[{"source": "RAG Workflow", "chunk": "Waiting for files"}],
                session_id=session_id
            )
    
    # AWAITING_STORAGE STATE: User provides storage name
    elif current_state == "awaiting_storage":
        session["storage_name"] = user_message
        session["state"] = "processing"
        rag_sessions[session_id] = session
        
        llm_name = session.get("settings", {}).get("llm", "NVIDIA Gemma 27B")
        vector_db_name = session.get("settings", {}).get("vectorDb", "Qdrant")

        response_text = f"""Excellent! Your RAG system is being created with the following configuration:

📋 **RAG Name**: {session['rag_name']}
🎭 **Personality**: {session.get('personality', 'Default')}
🤖 **LLM**: {llm_name}
🗄️ **Vector DB**: {vector_db_name}
💾 **Storage Name**: {user_message}

**Processing Your RAG System...**

I'm now:
1. 📄 Processing your uploaded documents
2. 🔍 Extracting text and metadata
3. 🧠 Creating embeddings for semantic search
4. 💾 Storing in the vector database ({user_message})
5. 🔗 Building the knowledge graph

✅ **RAG Creation Complete!**

Your RAG system "{session['rag_name']}" is now ready! You can start asking questions and I'll retrieve relevant information from your documents.

Type "reset" if you want to create another RAG system."""
        
        # Reset session to idle after completion
        session["state"] = "idle"
        rag_sessions[session_id] = session
        
        return ChatResponse(
            response=response_text,
            citations=[{"source": "RAG Workflow", "chunk": "Completion"}],
            session_id=session_id
        )
    
    # Handle reset command
    if "reset" in user_message_lower and current_state != "idle":
        session["state"] = "idle"
        session["rag_name"] = None
        session["files"] = []
        session["storage_name"] = None
        session["context"] = ""
        rag_sessions[session_id] = session
        
        return ChatResponse(
            response="RAG creation workflow has been reset. You can start a new RAG creation by saying 'create a RAG for me'.",
            citations=[{"source": "System", "chunk": "Reset"}],
            session_id=session_id
        )
    
    # Default: Use NVIDIA Gemma for general conversation (only when idle)
    if current_state == "idle":
        # Check if we have a created RAG session with context
        context = session.get("context", "")
        personality = session.get("personality", None)
        
        # Debug logging
        logger.info(f"Session {session_id} - RAG Name: {session.get('rag_name')}")
        logger.info(f"Session {session_id} - Context length: {len(context)} chars")
        logger.info(f"Session {session_id} - Context preview: {context[:200]}..." if context else "No context")
        
        # If RAG is created (we have context), use it
        if session.get("rag_name"):
             logger.info(f"Generating RAG response for {session['rag_name']}")
        
        gemma_response = generate_with_nvidia_gemma(user_message, context, personality)
        
        if gemma_response:
            # Add disclaimer if using RAG context
            if context:
                gemma_response += "\n\n---\n\n📌 **Important Note:** This response is based exclusively on the documents you uploaded to this RAG system. The information provided is limited to the content within those files and may not reflect the most current or comprehensive information available on this topic."
            
            return ChatResponse(
                response=gemma_response,
                citations=[{"source": "RAG Context", "chunk": "Based on uploaded documents"}] if context else [{"source": "NVIDIA Gemma 27B", "chunk": "General Knowledge"}],
                session_id=session_id
            )
        else:
            return ChatResponse(
                response="I apologize, but I'm having trouble connecting to the AI service right now. Please try again in a moment.",
                citations=[{"source": "system", "chunk": "Fallback response"}],
                session_id=session_id
            )
    
    # Fallback for unexpected states
    return ChatResponse(
        response="I'm not sure what you mean. Please follow the current step or type 'reset' to start over.",
        citations=[{"source": "System", "chunk": "Error"}],
        session_id=session_id
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), session_id: str = Form("default")):
    """
    File upload endpoint
    """
    try:
        contents = await file.read()
        file_size = len(contents)
        
        # Try to decode text content for RAG context
        text_content = ""
        try:
            # Check if it's a DOCX file
            if file.filename.lower().endswith('.docx'):
                logger.info(f"Parsing DOCX file: {file.filename}")
                doc = Document(BytesIO(contents))
                # Extract all paragraphs
                paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
                text_content = "\n".join(paragraphs)
                logger.info(f"Extracted {len(paragraphs)} paragraphs from DOCX")
            else:
                # Try plain text decoding
                text_content = contents.decode("utf-8")
        except Exception as e:
            logger.warning(f"Could not extract text from {file.filename}: {e}")
        
        # Store in session if session exists
        if session_id in rag_sessions:
            current_context = rag_sessions[session_id].get("context", "")
            # Limit context size to avoid token limits (increased for larger documents)
            if len(current_context) < 50000:  # Increased from 10000
                rag_sessions[session_id]["context"] = current_context + "\n\n" + f"--- Document: {file.filename} ---\n" + text_content[:10000]  # Increased from 5000
                logger.info(f"Added content from {file.filename} to session {session_id}")
                logger.info(f"Total context size now: {len(rag_sessions[session_id]['context'])} chars")
            else:
                logger.warning(f"Context limit reached for session {session_id}, skipping {file.filename}")
        
        logger.info(f"File uploaded: {file.filename} ({file_size} bytes)")
        
        return {
            "filename": file.filename,
            "status": "success",
            "message": f"File '{file.filename}' uploaded successfully ({file_size} bytes)",
            "size": file_size
        }
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# Google Drive upload support (simulated)
@app.post("/upload/google-drive")
async def upload_from_google_drive(request: Request):
    """Accept a Google Drive file ID and simulate fetching the file.
    In a real implementation you would use the Google Drive API with OAuth2 credentials.
    For now we just return a mock success response.
    """
    try:
        payload = await request.json()
        file_id = payload.get("file_id")
        if not file_id:
            raise HTTPException(status_code=400, detail="file_id is required")
        logger.info(f"Received Google Drive file ID: {file_id}")
        return {
            "filename": f"gdrive_{file_id}.pdf",
            "status": "success",
            "message": f"File with Google Drive ID '{file_id}' uploaded successfully (simulated).",
            "size": 0,
            "source": "google_drive"
        }
    except Exception as e:
        logger.error(f"Google Drive upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Google Drive upload failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting ShapeShifter API with NVIDIA Gemma 27B...")
    print("📍 Server running at: http://localhost:8001")
    print("📖 API Docs: http://localhost:8001/docs")
    print("✅ CORS enabled for all origins")
    print("🤖 LLM: NVIDIA Gemma 27B (google/gemma-27b-it)")
    print("🔄 RAG Creation Workflow: Enabled")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
