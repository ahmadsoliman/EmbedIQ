from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from loguru import logger
import time

from app.core.database import get_db
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.document_service import (
    create_document,
    get_document_by_id,
    get_documents,
)

router = APIRouter(
    prefix="/ingest",
    tags=["Document Ingestion"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def ingest_document(document: DocumentCreate, db: Session = Depends(get_db)):
    """
    Ingest a new document into the system.

    This will:
    1. Store the document metadata and content in the database
    2. Process the document into chunks
    3. Generate embeddings for each chunk
    4. Store the embeddings in the database
    """
    logger.info(f"Ingesting document: {document.title}")
    start_time = time.time()

    try:
        # Create the document in the database
        db_document = create_document(db=db, document=document)

        # In a real implementation, we would process the document asynchronously
        # For now, we'll just log that it would happen
        logger.info(
            f"Document ingested successfully. Processing would happen asynchronously."
        )

        # Calculate processing time
        process_time = time.time() - start_time
        logger.info(f"Document ingestion completed in {process_time:.2f}s")

        return db_document
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ingesting document: {str(e)}",
        )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a document by ID.
    """
    document = get_document_by_id(db=db, document_id=document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
    return document


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve a list of documents.
    """
    documents = get_documents(db=db, skip=skip, limit=limit)
    return documents
