from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from loguru import logger
import time

from app.core.database import get_db
from app.schemas.document import SearchQuery, SearchResponse, SearchResult
from app.services.search_service import search_documents

router = APIRouter(
    prefix="/search",
    tags=["Search"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=SearchResponse)
async def search(search_query: SearchQuery, db: Session = Depends(get_db)):
    """
    Search for documents based on vector similarity.

    This endpoint:
    1. Converts the query to a vector using the same embedding model
    2. Searches for similar vectors in the database
    3. Returns the most relevant document chunks
    """
    logger.info(f"Search query: {search_query.query}")
    start_time = time.time()

    try:
        # Perform the search
        results, total = search_documents(
            db=db,
            query=search_query.query,
            top_k=search_query.top_k,
            filters=search_query.filters,
        )

        # Calculate processing time
        process_time = (time.time() - start_time) * 1000  # Convert to ms
        logger.info(f"Search completed in {process_time:.2f}ms")

        return SearchResponse(
            query=search_query.query,
            results=results,
            total=total,
            latency_ms=process_time,
        )
    except Exception as e:
        logger.error(f"Error during search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}",
        )


@router.get("/", response_model=SearchResponse)
async def search_get(query: str, top_k: int = 5, db: Session = Depends(get_db)):
    """
    GET version of the search endpoint for simple queries.
    """
    search_query = SearchQuery(query=query, top_k=top_k)
    return await search(search_query=search_query, db=db)
