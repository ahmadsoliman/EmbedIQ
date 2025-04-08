from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from loguru import logger

# Get database connection string from environment
# Default to a local PostgreSQL connection for development
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@db:5432/embediq"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


# Dependency to get db session
def get_db():
    """
    Dependency for FastAPI routes to get database session.
    Creates a new database session for each request and closes it when the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to initialize db
def init_db():
    """
    Initialize database tables if they don't exist yet.
    In production, we would use Alembic migrations instead.
    """
    try:
        # Import models to ensure they're registered with Base
        # This will be updated as models are created
        # from app.models import your_models_here

        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
