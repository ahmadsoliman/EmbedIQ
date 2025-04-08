from lightrag import LightRAG, QueryParam
from sentence_transformers import SentenceTransformer
import numpy as np
import asyncio
import os
import time
from typing import List, Dict, Any, Optional
from loguru import logger

# Get environment variables for LightRAG configuration
WORKING_DIR = os.environ.get("LIGHTRAG_WORKING_DIR", "./data")
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@db:5432/embediq"
)
GRAPH_NAME = os.environ.get("AGE_GRAPH_NAME", "embediq")

# Ensure working directory exists
os.makedirs(WORKING_DIR, exist_ok=True)


class LightRAGService:
    _instance = None
    _rag = None

    @classmethod
    async def get_instance(cls):
        """Singleton pattern to get or create the LightRAG instance"""
        if cls._instance is None:
            cls._instance = LightRAGService()
            cls._rag = await cls._instance._initialize_rag()
        return cls._instance

    async def _embedding_func(self, texts: List[str]) -> np.ndarray:
        """Embedding function using sentence-transformers"""
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(texts, convert_to_numpy=True)
        return embeddings

    async def _initialize_rag(self) -> LightRAG:
        """Initialize LightRAG with PostgreSQL storage"""
        # setup_logger("lightrag", level="INFO")

        # Try with retry logic
        max_retries = 3
        retry_delay = 2  # seconds

        for retry in range(max_retries):
            try:
                logger.info(
                    f"Initializing LightRAG (attempt {retry+1}/{max_retries})..."
                )
                logger.info(f"Using database: {DATABASE_URL}")
                logger.info(f"Using graph name: {GRAPH_NAME}")
                logger.info(f"Using working directory: {WORKING_DIR}")

                # Initialize LightRAG with PostgreSQL storage
                rag = LightRAG(
                    working_dir=WORKING_DIR,
                    embedding_func=self._embedding_func,
                    vector_storage="PostgresVectorStorage",
                    graph_storage="PostgresGraphStorage",
                    kv_storage="PostgresKVStorage",
                    graph_name=GRAPH_NAME,
                    database_uri=DATABASE_URL,
                )

                # Initialize database connections
                await rag.initialize_storages()

                logger.info("LightRAG instance initialized with PostgreSQL storage")
                return rag
            except Exception as e:
                logger.error(
                    f"Error initializing LightRAG (attempt {retry+1}/{max_retries}): {e}"
                )
                if retry < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error("All retry attempts failed")
                    raise RuntimeError(
                        f"Failed to initialize LightRAG after {max_retries} attempts: {str(e)}"
                    )

    async def ingest_text(
        self, text: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Ingest text into LightRAG"""
        try:
            # Use doc_metadata internally to avoid conflicts with SQLAlchemy
            doc_metadata = metadata if metadata is not None else {}
            await self._rag.insert(text, metadata=doc_metadata)
            return {"status": "success", "message": "Text ingested successfully"}
        except Exception as e:
            logger.error(f"Error ingesting text: {e}")
            return {"status": "error", "message": str(e)}

    async def ingest_documents(
        self, documents: List[str], file_paths: List[str]
    ) -> Dict[str, Any]:
        """Ingest documents with file paths into LightRAG"""
        try:
            await self._rag.insert(documents, file_paths=file_paths)
            return {"status": "success", "message": "Documents ingested successfully"}
        except Exception as e:
            logger.error(f"Error ingesting documents: {e}")
            return {"status": "error", "message": str(e)}

    async def query(
        self,
        query_text: str,
        mode: str = "global",
        top_k: int = 60,
        only_context: bool = False,
    ) -> Dict[str, Any]:
        """Query LightRAG with various search modes"""
        try:
            # Validate mode
            valid_modes = ["local", "global", "hybrid", "naive", "mix"]
            if mode not in valid_modes:
                mode = "global"

            result = await self._rag.query(
                query_text,
                param=QueryParam(
                    mode=mode, top_k=top_k, only_need_context=only_context
                ),
            )

            return {"query": query_text, "result": result, "mode": mode, "top_k": top_k}
        except Exception as e:
            logger.error(f"Error querying LightRAG: {e}")
            return {"status": "error", "message": str(e)}
