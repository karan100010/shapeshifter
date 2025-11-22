# ShapeShifter RAG Implementation Summary

## Overview
ShapeShifter now implements a **context-aware RAG system** that ensures the chatbot answers questions **only from uploaded documents**, not from general internet knowledge.

## Key Changes Implemented

### 1. Backend Context Storage (`src/api/test_server_llama.py`)

#### File Upload Enhancement
- **Modified `/upload` endpoint** to accept `session_id` as a form parameter
- Uploaded text files are now **decoded and stored** in the session's context
- Context is limited to 10,000 characters total (5,000 per file) to avoid token limits
- Non-text files are handled gracefully with warnings

```python
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), session_id: str = Form("default")):
    # Decodes file content
    # Stores in rag_sessions[session_id]["context"]
```

#### Context-Aware LLM Generation
- **Updated `generate_with_nvidia_gemma()`** to accept `context` and `personality` parameters
- When context is provided, the LLM receives a **strict instruction**:
  > "IMPORTANT: You must answer the user's question ONLY based on the following context. If the answer is not in the context, state that you cannot answer from the provided documents."
- Temperature is lowered to 0.5 (from 0.7) when using context for more factual responses

#### Chat Endpoint Integration
- After RAG creation is complete, the chat endpoint checks for stored context
- If context exists (files were uploaded), it's passed to the LLM
- Citations now show "RAG Context - Based on uploaded documents" instead of "General Knowledge"

### 2. Frontend File Upload (`src/frontend/src/lib/api.ts` & `src/frontend/src/app/page.tsx`)

#### API Client Update
- **`uploadFile()`** now accepts `sessionId` parameter
- Session ID is appended to FormData as `session_id`

```typescript
async uploadFile(file: File, sessionId: string = 'default'): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', sessionId);
    // ...
}
```

#### Page Component Update
- **`handleFileUpload()`** now actually uploads files to the backend
- Passes `activeChat` (which is the session ID) to `api.uploadFile()`
- Files are uploaded asynchronously before the user types "uploaded"

### 3. Settings Modal (`src/frontend/src/components/SettingsModal.tsx`)

#### Features
- Users can select their preferred **LLM** (NVIDIA Gemma 27B, Meta Llama 3 70B, Mistral Large, GPT-4)
- Users can select their preferred **Vector Database** (Qdrant, ChromaDB, Milvus, pgvector)
- Settings are stored in state and sent with every chat message
- Backend displays selected LLM and Vector DB in the RAG creation summary

#### CSS Fix
- Updated CSS variables to match `globals.css` theme variables
- Fixed visibility issues in both light and dark modes
- Modal now properly displays with correct background, text, and button colors

## How It Works

### RAG Creation Flow
1. User initiates: "Create a RAG for me"
2. **Step 1**: Select personality (e.g., "Formal & Concise")
3. **Step 2**: Name the RAG (e.g., "Constitution Guardian")
4. **Step 3**: Upload documents (files are uploaded to `/upload` with session_id)
   - Backend decodes text content
   - Stores in `rag_sessions[session_id]["context"]`
5. **Step 4**: Name the storage (e.g., "india_law_v1")
6. RAG creation complete

### Query Flow (After RAG Creation)
1. User asks a question (e.g., "What are the Fundamental Rights?")
2. Backend retrieves `context` from `rag_sessions[session_id]`
3. Backend calls `generate_with_nvidia_gemma(user_message, context, personality)`
4. LLM receives:
   - System instruction with personality
   - **Strict context-only instruction**
   - The full document context
   - User's question
5. LLM generates answer **only from the provided context**
6. Response is returned with citation: "RAG Context - Based on uploaded documents"

## Limitations & Future Enhancements

### Current Limitations
1. **Context Size**: Limited to 10,000 characters total (simple truncation)
2. **File Types**: Only text-decodable files (`.txt`, `.md`, etc.) are processed
3. **No Chunking**: Entire file content is used as context (no smart chunking)
4. **No Vector Search**: True semantic search not implemented (simulated)
5. **In-Memory Storage**: Sessions are lost on server restart

### Recommended Enhancements
1. **Implement Real Vector DB**: Use Qdrant/ChromaDB for actual embedding storage
2. **Document Chunking**: Split large documents into semantic chunks
3. **Embedding Generation**: Create embeddings for uploaded documents
4. **Semantic Retrieval**: Retrieve only relevant chunks for each query
5. **PDF Support**: Add PDF parsing (PyPDF2, pdfplumber)
6. **Persistent Storage**: Use Redis or database for session persistence
7. **Context Window Management**: Implement sliding window for large documents

## Testing the RAG System

### Demo Script
Use the provided `DEMO_SCRIPT.md` for recording a demo video.

### Test Flow
1. Start both servers:
   ```bash
   # Frontend
   cd src/frontend && npm run dev
   
   # Backend
   python -m src.api.test_server_llama
   ```

2. Navigate to `http://localhost:3000`

3. Create a RAG:
   - Type: "Create a RAG for me"
   - Personality: "Formal & Concise"
   - Name: "Constitution Guardian"
   - Upload: Constitution of India text files
   - Type: "uploaded"
   - Storage: "india_law_v1"

4. Test with specific questions:
   - "What are the Fundamental Rights guaranteed under Part III?"
   - "Explain the procedure for amendment of the Constitution."

5. Verify the bot answers **only from uploaded documents**, not general knowledge.

## Configuration

### Environment Variables
- `NEXT_PUBLIC_API_URL`: Frontend API URL (default: `http://localhost:8001`)
- `NVIDIA_API_KEY`: NVIDIA Cloud Functions API key (hardcoded in backend)

### Adjustable Parameters
- **Context Limit**: `test_server_llama.py` line 387 (`if len(current_context) < 10000`)
- **Per-File Limit**: `test_server_llama.py` line 388 (`text_content[:5000]`)
- **Temperature**: `test_server_llama.py` line 88 (`0.5 if context else 0.7`)

---

**Status**: ✅ Implemented and Tested
**Date**: 2025-11-23
**Version**: Alpha
