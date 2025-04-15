import os
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Provides default values for development.
    """

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "EmbedIQ API"
    VERSION: str = "0.1.0"

    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DATABASE: str = "embediq"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@db:5432/embediq"
    )

    # CORS settings
    CORS_ORIGINS: str = "*"

    # JWT Authentication settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key_replace_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    # LLM API settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "openai")

    # Vector search settings
    SEARCH_TOP_K: int = 5
    SEARCH_SCORE_THRESHOLD: float = 0.7

    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # LightRAG settings
    LIGHTRAG_WORKING_DIR: str = "./data"
    LIGHTRAG_GRAPH_NAME: str = "embediq"

    # Model settings
    MODEL_BASE_URL: str = os.getenv("MODEL_BASE_URL", "https://api.deepseek.com/v1")
    MODEL_API_KEY: str = os.getenv("MODEL_API_KEY", "")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "deepseek-chat")
    EMBEDDING_MODEL_BASE_URL: str = os.getenv(
        "EMBEDDING_MODEL_BASE_URL", "https://api.cohere.ai/compatibility/v1"
    )
    EMBEDDING_MODEL_NAME: str = os.getenv(
        "EMBEDDING_MODEL_NAME", "embed-multilingual-v3.0"
    )
    EMBEDDING_MODEL_API_KEY: str = os.getenv("EMBEDDING_MODEL_API_KEY", "")
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", 1024))
    MAX_TOKEN_SIZE: int = int(os.getenv("MAX_TOKEN_SIZE", 8192))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", 32768))
    LLM_MAX_ASYNC: int = int(os.getenv("LLM_MAX_ASYNC", 4))

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

# Update settings from environment variables if provided
for field in settings.model_fields:
    env_value = os.getenv(field.upper())
    if env_value is not None:
        setattr(settings, field, env_value)
