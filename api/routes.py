import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas.request_models import (
    ChatRequest, ChatResponse,
    RAGQueryRequest, RAGQueryResponse,
    UploadResponse, HealthResponse,
)
from rag.chunking import process_document
from agents.rag_agent import run_rag_agent
from rag.vector_store import add_documents
from agents.orchestrator import run_orchestrator

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="ok")


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Orchestrator will be wired here in the next step
    try:
        response = run_orchestrator(request.message)
        return ChatResponse(
            response= response,
            agent_used="orchestrator"
        )
    except Exception as e :
       raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=UploadResponse)
# UploadFile -> file object (filename, content, type)
# File(...)  -> tells FastAPI this comes from form-data and (...) -> is required
async def upload_document(file: UploadFile = File(...)):
    # RAG ingestion pipeline will be wired here
    try :
        chunks = await process_document(file)
        add_documents(chunks)
        return UploadResponse(
            message="Document uploaded succesfully",
            filename=file.filename,
            chunks_stored=len(chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rag/query", response_model=RAGQueryResponse)
async def rag_query(request: RAGQueryRequest):
    # RAG query pipeline will be wired here
    try:
       answer = run_rag_agent(request.query)
       return RAGQueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gmail/summary")
async def gmail_summary():
    # Gmail agent will be wired here
    raise HTTPException(status_code=501, detail="Gmail agent not yet implemented")
