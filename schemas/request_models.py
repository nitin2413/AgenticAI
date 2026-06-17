from pydantic import BaseModel, Field
from typing import Optional, List


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for memory")


class ChatResponse(BaseModel):
    response: str
    agent_used: str
    session_id: Optional[str] = None


class RAGQueryRequest(BaseModel):
    query: str = Field(..., description="Query to search in documents")
    top_k: int = Field(default=4, description="Number of chunks to retrieve")
    session_id: Optional[str] = None


class RAGQueryResponse(BaseModel):
    answer: str
    sources: List[str] = []


class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_stored: int


class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"
