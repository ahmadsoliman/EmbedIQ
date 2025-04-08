from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from loguru import logger
import time

from app.core.database import get_db
from app.schemas.document import QueryRequest, QueryResponse
from app.services.query_service import process_query
from app.services.search_service import search_documents

router = APIRouter(
    prefix="/query",
    tags=["LLM Query"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=QueryResponse)
async def query(query_request: QueryRequest, db: Session = Depends(get_db)):
    """
    Process a natural language query with RAG.

    This endpoint:
    1. Takes a natural language query
    2. Retrieves relevant context from the document store
    3. Uses an LLM to generate an answer based on the retrieved context
    4. Returns the answer along with source information
    """
    logger.info(f"Query: {query_request.query}")
    start_time = time.time()

    try:
        # Retrieve relevant context
        search_results, _ = search_documents(
            db=db,
            query=query_request.query,
            top_k=query_request.top_k or 5,
            filters=query_request.context_filter,
        )

        # Process the query with the context
        answer, context_chunks, sources = process_query(
            query=query_request.query, search_results=search_results
        )

        # Calculate processing time
        process_time = (time.time() - start_time) * 1000  # Convert to ms
        logger.info(f"Query processed in {process_time:.2f}ms")

        return QueryResponse(
            query=query_request.query,
            answer=answer,
            context_chunks=context_chunks,
            sources=sources,
            latency_ms=process_time,
        )
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query processing failed: {str(e)}",
        )
