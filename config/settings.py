from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Nass Agent"
    DEBUG: bool = False

    # LLM
    OPENAI_API_KEY: str
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
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str

    # PostgreSQL
    POSTGRES_URL: Optional[str] = None
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # Gmail
    GMAIL_CREDENTIALS_PATH: Optional[str] = "credentials.json"
    GMAIL_TOKEN_PATH : Optional[str] = "./token.json"
    SCOPES : str = "https://www.googleapis.com/auth/gmail.readonly"

    def get_llm_config(self) -> dict:
        return {
            "provider": "openai",
            "model": self.OPENAI_MODEL,
            "api_key": self.OPENAI_API_KEY,
            "base_url": self.BASE_URL,
            "temperature": 0.7,
            "max_tokens": self.MAX_TOKEN,
        }

    class Config:
        env_file = str(ENV_PATH)  # Fixed: absolute path to .env
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
