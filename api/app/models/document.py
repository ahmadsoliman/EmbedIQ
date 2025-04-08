from sqlalchemy import (
    Column,
    String,
    Text,
    JSON,
    LargeBinary,
    ForeignKey,
    Integer,
    Float,
)
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Document(BaseModel):
    """
    Model for storing document metadata and content.
    """

    # Document metadata
    title = Column(String(255), nullable=False, index=True)
    source = Column(String(255), nullable=True, index=True)
    author = Column(String(255), nullable=True)

    # Document content
    content = Column(Text, nullable=False)

    # Metadata (file type, creation date, etc.)
    metadata = Column(JSON, nullable=True)

    # Relationship to embedding chunks
    chunks = relationship(
        "DocumentChunk", back_populates="document", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Document(id={self.id}, title='{self.title}')>"


class DocumentChunk(BaseModel):
    """
    Model for storing document chunks and their embeddings.
    This is used for semantic search and retrieval.
    """

    # Relationship to parent document
    document_id = Column(Integer, ForeignKey("document.id"), nullable=False, index=True)
    document = relationship("Document", back_populates="chunks")

    # Chunk information
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)

    # In a real implementation, we would use a PostgreSQL vector extension like pgvector
    # For now, store as binary or use another approach
    embedding = Column(LargeBinary, nullable=True)

    # Metadata about the chunk (e.g., page number, section)
    metadata = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, document_id={self.document_id}, chunk_index={self.chunk_index})>"


class QueryLog(BaseModel):
    """
    Model for storing user queries and retrieval information.
    Useful for analytics and improving the system over time.
    """

    # Query information
    query_text = Column(Text, nullable=False)
    user_id = Column(String(255), nullable=True, index=True)

    # Response information
    response_text = Column(Text, nullable=True)
    retrieval_latency_ms = Column(Integer, nullable=True)
    generation_latency_ms = Column(Integer, nullable=True)

    # Retrieval information
    retrieved_chunk_ids = Column(JSON, nullable=True)  # Store list of chunk IDs
    relevance_scores = Column(JSON, nullable=True)  # Store scores for retrieved chunks

    # Feedback (if provided)
    user_rating = Column(Integer, nullable=True)
    user_feedback = Column(Text, nullable=True)

    def __repr__(self):
        return f"<QueryLog(id={self.id}, query_text='{self.query_text[:20]}...')>"
