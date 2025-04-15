from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
from lightrag.kg.shared_storage import initialize_pipeline_status
import textract
import asyncio
import os
import time
from typing import List, Dict, Any, Optional
from loguru import logger
from dotenv import load_dotenv
from app.core.config import settings
from app.services.llm_service import openai_complete_if_cache, openai_embed
from app.services.document_service import DocumentService
from app.services.search_service import SearchService

load_dotenv()


class LightRAGService:
    _instance = None
    _lock = asyncio.Lock()

    def __init__(self):
        """Initialize the LightRAG service."""
        self.db_lock = asyncio.Lock()
        self.document_service = DocumentService()
        self.search_service = SearchService()
        self.rag = None

    @classmethod
    async def get_instance(cls) -> "LightRAGService":
        """Get or create a singleton instance of LightRAGService."""
        if not cls._instance:
            async with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance

    async def _llm_model_func(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        history_messages: List[Dict[str, str]] = [],
        keyword_extraction: bool = False,
        **kwargs,
    ) -> str:
        """LLM model function wrapper for LightRAG."""
        return await openai_complete_if_cache(
            settings.LLM_MODEL_NAME,
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key=settings.MODEL_API_KEY,
            base_url=settings.MODEL_BASE_URL,
        )

    def _create_embedding_func(self):
        """Create embedding function using OpenAI-compatible API."""
        return EmbeddingFunc(
            embedding_dim=settings.EMBEDDING_DIM,
            max_token_size=settings.MAX_TOKEN_SIZE,
            func=lambda texts: openai_embed(
                texts,
                model=settings.EMBEDDING_MODEL_NAME,
                api_key=settings.EMBEDDING_MODEL_API_KEY,
                base_url=settings.EMBEDDING_MODEL_BASE_URL,
            ),
        )

    async def _initialize_rag(self) -> LightRAG:
        """Initialize LightRAG with PostgreSQL storage"""
        max_retries = 3
        retry_delay = 2

        for retry in range(max_retries):
            try:
                logger.info(
                    f"Initializing LightRAG (attempt {retry+1}/{max_retries})..."
                )

                # Initialize LightRAG with complete configuration
                embedding_func = self._create_embedding_func()
                self.rag = LightRAG(
                    working_dir=settings.LIGHTRAG_WORKING_DIR,
                    llm_model_func=self._llm_model_func,
                    llm_model_name=settings.LLM_MODEL_NAME,
                    llm_model_max_async=int(settings.LLM_MAX_ASYNC),
                    llm_model_max_token_size=int(settings.LLM_MAX_TOKENS),
                    enable_llm_cache_for_entity_extract=True,
                    embedding_func=embedding_func,
                    kv_storage="PGKVStorage",
                    doc_status_storage="PGDocStatusStorage",
                    graph_storage="PGGraphStorage",
                    vector_storage="PGVectorStorage",
                    auto_manage_storages_states=False,
                )

                # Initialize storages and pipeline status
                await self.rag.initialize_storages()
                await initialize_pipeline_status()

                # Set embedding function for graph database
                self.rag.chunk_entity_relation_graph.embedding_func = embedding_func

                logger.info("LightRAG instance initialized successfully")
                return self.rag

            except Exception as e:
                logger.error(
                    f"Error initializing LightRAG (attempt {retry+1}/{max_retries}): {e}"
                )
                if retry < max_retries - 1:
                    logger.info(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    logger.error("All retry attempts failed")
                    raise RuntimeError(
                        f"Failed to initialize LightRAG after {max_retries} attempts: {str(e)}"
                    )

    async def ingest_text(
        self, text: str, doc_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Ingest text with thread-safe database operations and LightRAG ingestion."""
        try:
            async with self.db_lock:  # Ensure thread-safe database access
                documentId = await self.document_service.create_document(
                    text, doc_metadata
                )
                await self.search_service.index_document(documentId)

                # Ingest into LightRAG
                if not self.rag:
                    self.rag = await self._initialize_rag()
                await self.rag.ainsert(
                    text, ids=[str(documentId)], file_paths=[str(documentId)]
                )

                return {"status": "success", "document_id": documentId}
        except Exception as e:
            logger.error(f"Error during text ingestion: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def ingest_documents(self, file_paths: List[str]) -> Dict[str, Any]:
        """Ingest documents with file paths into LightRAG and database."""
        try:
            async with self.db_lock:  # Ensure thread-safe database access
                for file_path in file_paths:
                    text = textract.process(file_path).decode("utf-8")

                    documentId = await self.document_service.create_document(
                        text, {"file_path": file_path}
                    )
                    await self.search_service.index_document(documentId)

                    # Ingest into LightRAG
                    if not self.rag:
                        self.rag = await self._initialize_rag()
                    await self.rag.ainsert(
                        text, ids=[str(documentId)], file_paths=[file_path]
                    )

                return {
                    "status": "success",
                    "message": "Documents ingested successfully",
                }
        except Exception as e:
            logger.error(f"Error ingesting documents: {e}")
            return {"status": "error", "message": str(e)}

    async def query(
        self, query_text: str, mode: str = "hybrid", top_k: int = 3, **kwargs
    ) -> Dict[str, Any]:
        """
        Query the RAG system with support for multiple modes.

        Args:
            query_text: The query text to search for
            mode: Search mode ('naive', 'local', 'global', or 'hybrid')
            top_k: Number of top results to return
            **kwargs: Additional parameters to pass to the query

        Returns:
            Dictionary containing query results and timing information
        """
        start_time = time.time()
        try:
            async with self.db_lock:
                # Ensure RAG instance is initialized
                if not self.rag:
                    self.rag = await self._initialize_rag()

                # Validate mode
                valid_modes = ["naive", "local", "global", "hybrid"]
                if mode not in valid_modes:
                    raise ValueError(
                        f"Invalid mode '{mode}'. Must be one of {valid_modes}"
                    )

                # Execute query with specified mode
                param = QueryParam(mode=mode, top_k=top_k, **kwargs)

                result = await self.rag.aquery(query_text, param=param)

                # Calculate execution time
                execution_time = time.time() - start_time

                return {
                    "status": "success",
                    "mode": mode,
                    "result": result,
                    "execution_time": execution_time,
                    "metadata": {"top_k": top_k, "query_params": kwargs},
                }

        except Exception as e:
            logger.error(f"Error during {mode} query execution: {str(e)}")
            return {
                "status": "error",
                "mode": mode,
                "message": str(e),
                "execution_time": time.time() - start_time,
            }
