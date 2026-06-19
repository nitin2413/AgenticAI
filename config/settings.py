from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Multi-Agent AI System"
    DEBUG: bool = False

    # LLM
    OPENAI_API_KEY: str = "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"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    BASE_URL: str = "https://openrouter.ai/api/v1"
    MAX_TOKEN: int  = 4096

    # Embeddings
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # ChromaDB
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "documents"

    # Redis
    REDIS_URL: Optional[str] = "redis://localhost:6379"
    REDIS_HOST: str = "birds-megabright-sail -58709.db.redis.io"
    REDIS_PORT: int  = 10409
    REDIS_USERNAME: str = "default"
    REDIS_PASSWORD: str  = "oWmwqC0rcQ6GFq2lli4eBaYMJ4EWBaJa"

    # PostgreSQL
    POSTGRES_URL: Optional[str] = None

    # Gmail
    GMAIL_CREDENTIALS_PATH: Optional[str] = "credentials.json"
    GMAIL_TOKEN_PATH : Optional[str] = "./token.json"
    SCOPES : str = "https://www.googleapis.com/auth/gmail.readonly"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
