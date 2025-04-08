#!/usr/bin/env python3
"""
Test script to verify LightRAG is working correctly.
"""

import asyncio
import os
import sys
import logging
from pathlib import Path
import traceback
import time

# Add api directory to path for imports
api_path = str(Path(__file__).parent.parent / "api")
sys.path.append(api_path)
print(f"Added API path to sys.path: {api_path}")

# Check if running in docker
in_docker = os.path.exists("/.dockerenv")
if in_docker:
    # When in Docker, /app is already the WORKDIR, so we need to adjust paths
    print("Running in Docker container")
    sys.path.append("/app")

# If running locally, use localhost for database connection
if "--local" in sys.argv or "-l" in sys.argv:
    print("Using localhost for database connection")
    os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/embediq"
else:
    # Use Docker service name
    os.environ["DATABASE_URL"] = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@db:5432/embediq"
    )

os.environ["LIGHTRAG_WORKING_DIR"] = os.environ.get("LIGHTRAG_WORKING_DIR", "./data")
os.environ["AGE_GRAPH_NAME"] = os.environ.get("AGE_GRAPH_NAME", "embediq")

# Try to import required dependencies
required_packages = [
    "lightrag",
    "sentence_transformers",
    "faiss",
    "psycopg2",
    "numpy",
    "loguru",
]

missing_packages = []
for package in required_packages:
    try:
        __import__(package)
        print(f"✓ {package} is installed")
    except ImportError:
        missing_packages.append(package)
        print(f"✗ {package} is missing")

if missing_packages:
    print("\nPlease install missing packages:")
    print(f"pip install {' '.join(missing_packages)}")
    sys.exit(1)

# Now try to import LightRAG service
try:
    from app.services.lightrag_service import LightRAGService

    print("✓ Successfully imported LightRAGService")
except ImportError as e:
    print(f"Error importing LightRAG service: {e}")
    print("\nPossible fixes:")
    print("1. Make sure you're running from the project root: cd /path/to/rag-sass")
    print("2. Check that all dependencies are installed")
    print("3. Verify the app/services/lightrag_service.py file exists")
    print("4. If running in Docker, check the container file structure")
    print("\nInstall all dependencies with:")
    print(
        "pip install lightrag faiss-cpu sentence-transformers pgvector psycopg2-binary"
    )
    sys.exit(1)


async def test_lightrag():
    """Test LightRAG functionality."""
    print("\n========================================")
    print("    LightRAG PostgreSQL Integration Test")
    print("========================================\n")

    print("Database URL:", os.environ["DATABASE_URL"])
    print("Working directory:", os.environ["LIGHTRAG_WORKING_DIR"])
    print("Graph name:", os.environ["AGE_GRAPH_NAME"])

    # Test database connection first
    print("\nTesting database connection...")
    try:
        import psycopg2

        db_url = os.environ["DATABASE_URL"]
        conn = psycopg2.connect(db_url, connect_timeout=5)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✓ Connected to PostgreSQL: {version[0]}")

        # Check for extensions
        cursor.execute("SELECT extname FROM pg_extension;")
        extensions = [ext[0] for ext in cursor.fetchall()]
        print(f"Installed extensions: {', '.join(extensions)}")

        if "vector" not in extensions:
            print("⚠ pgvector extension is not installed!")
        if "age" not in extensions:
            print("⚠ Apache AGE extension is not installed!")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        print("Make sure PostgreSQL is running and accessible.")

        if "Connection refused" in str(e):
            if "--local" in sys.argv:
                print("Check that PostgreSQL is running on localhost:5432")
            else:
                print("If running outside Docker, try with --local flag")
        return

    try:
        print("\nInitializing LightRAG service...")
        start_time = time.time()
        rag_service = await LightRAGService.get_instance()
        init_time = time.time() - start_time
        print(f"✓ LightRAG service initialized in {init_time:.2f}s")

        # Test ingestion
        print("\n=== Testing Text Ingestion ===")
        text = """
        LightRAG is a framework for building Retrieval-Augmented Generation (RAG) applications.
        It supports multiple retrieval modes including local, global, hybrid, naive, and mix.
        This text is for testing the ingestion and querying capabilities of LightRAG.
        """

        # Rename metadata to doc_metadata to avoid SQLAlchemy conflict
        doc_metadata = {
            "title": "LightRAG Introduction",
            "source": "Test Script",
            "author": "Test User",
        }

        print(f"Ingesting test text with metadata: {doc_metadata}")
        result = await rag_service.ingest_text(text, metadata=doc_metadata)
        print(f"Ingestion result: {result}")

        if result.get("status") == "error":
            print(f"✗ Error during ingestion: {result.get('message')}")
            return
        else:
            print("✓ Text ingested successfully")

        # Test querying in different modes
        print("\n=== Testing Queries ===")
        query = "What is LightRAG?"

        for mode in ["naive", "local", "global", "hybrid", "mix"]:
            try:
                print(f"\nTesting {mode} mode query: '{query}'")
                start_time = time.time()
                result = await rag_service.query(query, mode=mode, top_k=3)
                query_time = time.time() - start_time

                if result.get("status") == "error":
                    print(f"✗ Error in {mode} mode query: {result.get('message')}")
                else:
                    print(f"✓ {mode} mode query completed in {query_time:.2f}s")
                    print(f"Result: {result.get('result', 'No result')}")
            except Exception as e:
                print(f"✗ Exception in {mode} mode query: {e}")

        print("\n✅ LightRAG test completed successfully!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nDetailed traceback:")
        traceback.print_exc()
        print("\nTroubleshooting tips:")
        print("1. Make sure the PostgreSQL database is running:")
        print("   docker ps | grep postgres")
        print("2. Check that the right extensions are installed:")
        print("   pgvector and Apache AGE")
        print("3. Verify DATABASE_URL environment variable:")
        print(f"   {os.environ['DATABASE_URL']}")
        print("4. If running outside Docker, use --local flag")


if __name__ == "__main__":
    asyncio.run(test_lightrag())
