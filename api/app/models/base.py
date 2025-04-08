from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from app.core.database import Base
import datetime


class BaseModel(Base):
    """
    Base model for all database models.
    Provides common attributes and functionality.
    """

    __abstract__ = True

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )

    # Table name is based on class name
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Generate table name from class name.
        Convert CamelCase to snake_case.
        """
        # Convert camel case to snake case
        # e.g., DocumentEmbedding -> document_embedding
        name = cls.__name__
        return "".join(["_" + c.lower() if c.isupper() else c for c in name]).lstrip(
            "_"
        )
