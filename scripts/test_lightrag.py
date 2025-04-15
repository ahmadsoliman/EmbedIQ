#!/usr/bin/env python3
"""
Test script to verify LightRAG is working correctly.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
import time
from dotenv import load_dotenv

# Load environment variables before imports
load_dotenv()

# Configure base directory and Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_DIR = os.path.join(ROOT_DIR, "api")

# Add root directory to Python path if not already there
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
# Add API directory to Python path if not already there
if API_DIR not in sys.path:
    sys.path.insert(0, API_DIR)

# Configure logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up working directory
WORKING_DIR = os.path.join(ROOT_DIR, "data", "embediq")
os.makedirs(WORKING_DIR, exist_ok=True)

# Set environment variables for PostgreSQL and AGE
os.environ.setdefault("POSTGRES_HOST", "db")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_USER", "postgres")
os.environ.setdefault("POSTGRES_PASSWORD", "postgres")
os.environ.setdefault("POSTGRES_DATABASE", "embediq")
os.environ.setdefault("AGE_GRAPH_NAME", "embediq")

logger.info(f"Python path: {sys.path}")
logger.info(f"Working directory: {WORKING_DIR}")
logger.info(f"Database host: {os.environ['POSTGRES_HOST']}")

# Import LightRAG service
try:
    from app.services.lightrag_service import LightRAGService

    logger.info("✓ Successfully imported LightRAG service")
except ImportError as e:
    logger.error(f"Error importing LightRAG service: {e}")
    logger.error(f"Current working directory: {os.getcwd()}")
    logger.error(f"Current PYTHONPATH: {sys.path}")
    sys.exit(1)


async def test_lightrag():
    """Test LightRAG functionality with all query modes."""
    logger.info("\n==== Testing LightRAG Functionality ====")

    try:
        # Initialize RAG instance
        rag_service = await LightRAGService.get_instance()

        # Test data for ingestion
        test_text = """
        Charles Dickens was an English writer and social critic. He created some of
        the world's best-known fictional characters and is regarded by many as the
        greatest novelist of the Victorian era. His works enjoyed unprecedented 
        popularity during his lifetime, and by the 20th century, critics and scholars
        had recognized him as a literary genius.
        """

        logger.info("\n==== Testing Document Ingestion ====")
        # async with rag_service.db_lock:
        result = await rag_service.ingest_text(test_text)
        if result["status"] != "success":
            logger.error(f"Error during ingestion: {result}")
            return
        logger.info("✓ Document ingested successfully")

        # Test all query modes
        query = "What are the main themes in this text?"

        for mode in ["naive", "local", "global", "hybrid"]:
            logger.info(f"\n**** Start {mode.capitalize()} Query ****")
            start_time = time.time()
            result = await rag_service.query(query, mode=mode)
            logger.info(f"Result: {result.get('result', 'No result')}")
            logger.info(
                f"{mode.capitalize()} Query Time: {time.time() - start_time} seconds"
            )

    except Exception as e:
        logger.error(f"Error during test execution: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_lightrag())
