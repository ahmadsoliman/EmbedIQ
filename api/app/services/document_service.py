from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from loguru import logger
import asyncio

from app.models.document import Document, DocumentChunk
from app.schemas.document import DocumentCreate, DocumentChunkCreate
from app.core.database import get_session


class DocumentService:
    def __init__(self):
        self.db_lock = asyncio.Lock()

    async def create_document(
        self, text: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Document:
        """Create a document with thread-safe database access."""
        async with self.db_lock:
            async with get_session() as session:
                document = Document(content=text, metadata=metadata or {}, title="")
                session.add(document)
                await session.commit()
                await session.refresh(document)
                return document.id

    async def get_document(self, document_id: int) -> Optional[Document]:
        """Get a document by ID with thread-safe database access."""
        async with self.db_lock:
            async with get_session() as session:
                result = await session.get(Document, document_id)
                return result

    async def get_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """Get a list of documents with pagination."""
        async with self.db_lock:
            async with get_session() as session:
                result = await session.execute(
                    select(Document).offset(skip).limit(limit)
                )
                return result.scalars().all()

    async def delete_document(self, document_id: int) -> bool:
        """Delete a document by ID."""
        async with self.db_lock:
            async with get_session() as session:
                document = await session.get(Document, document_id)
                if not document:
                    return False
                await session.delete(document)
                await session.commit()
                return True


def create_document(db: Session, document: DocumentCreate) -> Document:
    """
    Create a new document in the database.
    """
    # Create document object
    db_document = Document(
        title=document.title,
        source=document.source,
        author=document.author,
        content=document.content,
        doc_metadata=document.doc_metadata or {},
    )

    # Add to database
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # In a real implementation, we would handle chunking and embedding generation
    # For now, we'll leave this as a placeholder

    return db_document


def get_document_by_id(db: Session, document_id: int) -> Optional[Document]:
    """
    Get a document by ID.
    """
    return db.query(Document).filter(Document.id == document_id).first()


def get_documents(db: Session, skip: int = 0, limit: int = 100) -> List[Document]:
    """
    Get a list of documents with pagination.
    """
    return db.query(Document).offset(skip).limit(limit).all()


def delete_document(db: Session, document_id: int) -> bool:
    """
    Delete a document by ID.
    """
    document = get_document_by_id(db, document_id)
    if not document:
        return False

    db.delete(document)
    db.commit()
    return True


def create_document_chunk(db: Session, chunk: DocumentChunkCreate) -> DocumentChunk:
    """
    Create a new document chunk in the database.
    """
    db_chunk = DocumentChunk(
        document_id=chunk.document_id,
        chunk_index=chunk.chunk_index,
        chunk_text=chunk.chunk_text,
        chunk_metadata=chunk.doc_metadata or {},
    )

    db.add(db_chunk)
    db.commit()
    db.refresh(db_chunk)

    return db_chunk


def process_document(db: Session, document_id: int) -> bool:
    """
    Process a document into chunks and generate embeddings.
    This would typically be run asynchronously.
    """
    # Get the document
    document = get_document_by_id(db, document_id)
    if not document:
        logger.error(f"Document {document_id} not found for processing")
        return False

    try:
        # In a real implementation, we would:
        # 1. Split the document into chunks
        # 2. Generate embeddings for each chunk
        # 3. Store the chunks and embeddings

        # For now, we'll create a single chunk as a placeholder
        chunk = DocumentChunkCreate(
            document_id=document.id,
            chunk_index=0,
            chunk_text=document.content[
                :1000
            ],  # Just the first 1000 chars as an example
            doc_metadata={"is_placeholder": True},
        )
        create_document_chunk(db, chunk)

        logger.info(f"Document {document_id} processed successfully")
        return True
    except Exception as e:
        logger.error(f"Error processing document {document_id}: {e}")
        return False
