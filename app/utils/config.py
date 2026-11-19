"""Centralized environment configuration."""
from dataclasses import dataclass
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///data/documind.db")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
