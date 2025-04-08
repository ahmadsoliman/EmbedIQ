import os
from pydantic import BaseModel
from typing import List


class Settings(BaseModel):
    """
    Application settings loaded from environment variables.
    Provides default values for development.
    """

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "EmbedIQ API"
    VERSION: str = "0.1.0"

    # CORS settings - Frontend URL for production, allow all in development
    CORS_ORIGINS: List[str] = ["*"]

    # JWT Authentication settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key_replace_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@db:5432/embediq"
    )

    # LLM API settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "openai")

    # Embedding settings
    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    EMBEDDING_DIMENSION: int = 384  # Depends on the model

    # Vector search settings
    SEARCH_TOP_K: int = 5
    SEARCH_SCORE_THRESHOLD: float = 0.7

    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


# Create global settings instance
settings = Settings()

# Update settings from environment variables if provided
for field in settings.model_fields:
    env_value = os.getenv(field.upper())
    if env_value is not None:
        setattr(settings, field, env_value)
