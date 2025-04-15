from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from loguru import logger
from contextlib import asynccontextmanager

# Get database connection string from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@db:5432/embediq"
).replace("postgresql://", "postgresql+asyncpg://")

# Create async SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=engine
)

# Create base class for models
Base = declarative_base()


@asynccontextmanager
async def get_session():
    """
    Async context manager for database sessions.
    Creates a new async database session and closes it when done.
    """
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


# Dependency to get db session
async def get_db():
    """
    Async dependency for FastAPI routes to get database session.
    """
    async with get_session() as session:
        yield session


# Function to initialize db
async def init_db():
    """
    Initialize database tables if they don't exist yet.
    """
    try:
        async with engine.begin() as conn:
            logger.info("Creating database tables...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
