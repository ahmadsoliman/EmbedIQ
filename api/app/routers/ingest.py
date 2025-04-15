from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from loguru import logger
import time
import json

from app.core.database import get_db
from app.schemas.document import DocumentCreate, DocumentResponse
from app.services.document_service import (
    create_document,
    get_document_by_id,
    get_documents,
)
from app.services.lightrag_service import LightRAGService

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
        db_documentId = create_document(db=db, document=document)

        # Also ingest into LightRAG if content is available
        if document.content:
            rag_service = await LightRAGService.get_instance()
            doc_metadata = {
                "title": document.title,
                "document_id": db_documentId,
                "source": document.source,
            }
            await rag_service.ingest_text(document.content, doc_metadata=doc_metadata)

        # Calculate processing time
        process_time = time.time() - start_time
        logger.info(f"Document ingestion completed in {process_time:.2f}s")

        return {"id": db_documentId}
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ingesting document: {str(e)}",
        )


@router.post("/text", status_code=status.HTTP_201_CREATED)
async def ingest_text(text: str = Form(...), metadata_json: Optional[str] = Form(None)):
    """
    Ingest plain text into LightRAG.

    This endpoint allows ingesting text directly into LightRAG without storing it in the SQL database.
    Optionally provide metadata as a JSON string.
    """
    logger.info("Ingesting text into LightRAG")
    start_time = time.time()

    try:
        # Parse metadata if provided
        doc_metadata = None
        if metadata_json:
            try:
                doc_metadata = json.loads(metadata_json)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid metadata JSON format",
                )

        # Ingest text into LightRAG
        rag_service = await LightRAGService.get_instance()
        result = await rag_service.ingest_text(text, doc_metadata=doc_metadata)

        if result.get("status") == "error":
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("message", "Error ingesting text"),
            )

        # Calculate processing time
        process_time = time.time() - start_time
        logger.info(f"Text ingestion completed in {process_time:.2f}s")

        return {
            "status": "success",
            "message": "Text ingested successfully",
            "latency_ms": process_time * 1000,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting text: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ingesting text: {str(e)}",
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
