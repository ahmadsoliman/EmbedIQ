from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from loguru import logger
import time
from enum import Enum

from app.core.database import get_db
from app.services.lightrag_service import LightRAGService
from pydantic import BaseModel

router = APIRouter(
    prefix="/query",
    tags=["LLM Query"],
    responses={404: {"description": "Not found"}},
)


class QueryMode(str, Enum):
    naive = "naive"
    local = "local"
    global_ = "global"
    hybrid = "hybrid"


class QueryRequest(BaseModel):
    query: str
    mode: QueryMode = QueryMode.hybrid
    top_k: Optional[int] = 3
    params: Optional[Dict[str, Any]] = None


@router.post("/query")
async def query(request: QueryRequest):
    """
    Query the RAG system with various search modes.

    Args:
        request: QueryRequest containing:
            - query: The text to search for
            - mode: Search mode (naive/local/global/hybrid)
            - top_k: Number of top results to return
            - params: Additional query parameters
    """
    try:
        service = await LightRAGService.get_instance()
        params = request.params or {}

        result = await service.query(
            query_text=request.query,
            mode=request.mode.value,
            top_k=request.top_k,
            **params,
        )

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])

        return result

    except Exception as e:
        logger.error(f"Error processing query request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
