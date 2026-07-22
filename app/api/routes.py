import os
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.services.pdf_processor import extract_text_from_pdf, chunk_text
from app.services.vector_store import add_documents_to_store
from app.graph.rag_graph import rag_app

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    thread_id: str = "default_thread"

class ChatResponse(BaseModel):
    answer: str
    citations: list[str]

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Handles PDF upload, processing, and vector store ingestion."""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        
    file_path = f"uploads/{uuid.uuid4()}_{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_path, "wb") as f:
        f.write(await file.read())
        
    try:
        text = extract_text_from_pdf(file_path)
        chunks = chunk_text(text, source_name=file.filename)
        add_documents_to_store(chunks)
        return {"message": f"Successfully processed {file.filename}", "chunks_created": len(chunks)}
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail="Error processing PDF.")

@router.post("/chat", response_model=ChatResponse)
async def chat_with_docs(request: ChatRequest):
    """Handles user questions using the RAG graph."""
    config = {"configurable": {"thread_id": request.thread_id}}
    
    # We pass an empty history list here; LangGraph's MemorySaver handles the actual history internally
    inputs = {"question": request.question, "chat_history": [], "documents": [], "generation": "", "citations": []}
    
    result = rag_app.invoke(inputs, config)
    
    return ChatResponse(
        answer=result["generation"],
        citations=result["citations"]
    )