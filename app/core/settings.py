from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # API Configuration
    PROJECT_NAME: str = "Citizen Lawyer API"
    API_V1_STR: str = "/api/v1"

    # LLM & Embedding Models
    OPENAI_API_KEY: str = Field(..., alias="OPENAI_API_KEY")
    LLM_MODEL: str = "gpt-4o"
    EMBEDDING_MODEL: str = "intfloat/multilingual-e5-large"
    RERANKER_MODEL: str = "BAAI/bge-reranker-base"

    # Vector Store (Qdrant)
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str | None = None
    COLLECTION_NAME: str = "legal_articles"

    # RAG Configuration
    RETRIEVAL_LIMIT: int = 10
    RERANK_THRESHOLD: float = 0.7


settings = Settings()
