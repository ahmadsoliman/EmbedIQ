from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class DocumentBase(BaseModel):
    """
    Base schema for document data.
    Used for shared properties between creation and reading.
    """

    title: str = Field(..., description="Document title", min_length=1, max_length=255)
    source: Optional[str] = Field(None, description="Source of the document")
    author: Optional[str] = Field(None, description="Author of the document")
    doc_metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional document metadata"
    )


class DocumentCreate(DocumentBase):
    """
    Schema for creating a new document.
    """

    content: str = Field(..., description="Full document content")


class DocumentResponse(DocumentBase):
    """
    Schema for document responses from the API.
    """

    id: int
    content: Optional[str] = (
        None  # Optional to allow returning metadata without full content
    )
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # Maps ORM objects to response model


class DocumentChunkBase(BaseModel):
    """
    Base schema for document chunk data.
    """

    chunk_index: int = Field(..., description="Index of the chunk within the document")
    chunk_text: str = Field(..., description="Text content of the chunk")
    doc_metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional chunk metadata"
    )


class DocumentChunkCreate(DocumentChunkBase):
    """
    Schema for creating a new document chunk.
    """

    document_id: int = Field(..., description="ID of the parent document")


class DocumentChunkResponse(DocumentChunkBase):
    """
    Schema for document chunk responses from the API.
    """

    id: int
    document_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SearchQuery(BaseModel):
    """
    Schema for search queries.
    """

    query: str = Field(..., description="Search query text", min_length=1)
    top_k: Optional[int] = Field(5, description="Number of results to return")
    filters: Optional[Dict[str, Any]] = Field(
        None, description="Filters to apply to search"
    )


class SearchResult(BaseModel):
    """
    Schema for search results.
    """

    document_id: int
    document_title: str
    chunk_id: int
    chunk_text: str
    score: float
    doc_metadata: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    """
    Schema for search query responses.
    """

    query: str
    results: List[SearchResult]
    total: int
    latency_ms: float


class QueryRequest(BaseModel):
    """
    Schema for LLM query requests.
    """

    query: str = Field(..., description="Natural language query", min_length=1)
    context_filter: Optional[Dict[str, Any]] = Field(
        None, description="Filters for context retrieval"
    )
    top_k: Optional[int] = Field(
        5, description="Number of context documents to retrieve"
    )


class QueryResponse(BaseModel):
    """
    Schema for LLM query responses.
    """

    query: str
    answer: str
    context_chunks: List[Dict[str, Any]]
    sources: List[Dict[str, str]]
    latency_ms: float
