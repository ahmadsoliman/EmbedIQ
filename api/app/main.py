from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import uvicorn
import os

from app.core.config import settings
from app.core.database import init_db

# Import routers
from app.routers import ingest, search, query

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A cloud-based RAG system that leverages high-quality embedding search and LLM context-based answers.",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "ok", "service": "embediq-api"}


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint providing basic API information.
    """
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "documentation": "/docs",
    }


# Include routers
app.include_router(ingest.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(query.router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    """
    Actions to perform on application startup.
    """
    logger.info(f"Starting {settings.PROJECT_NAME}")

    # Initialize database
    init_db()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to perform on application shutdown.
    """
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


# Main entry point for running the application directly
if __name__ == "__main__":
    logger.info(f"Starting {settings.PROJECT_NAME}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
