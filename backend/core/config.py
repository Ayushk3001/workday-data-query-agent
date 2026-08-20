"""
Centralized Configuration for Workday Data Query Agent.
Loads environment variables from .env if present.
"""

import os
from dotenv import load_dotenv

# Load .env file from project root or backend directory if present
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)


class Settings:
    PROJECT_NAME: str = "Workday Data Query Agent API"
    PROJECT_DESCRIPTION: str = "Backend foundation for Workday-style HR query & reporting agent"
    VERSION: str = "0.1.0"

    # Base Directory (backend/)
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Database Directory & File Path
    DB_DIR: str = os.path.join(BASE_DIR, "database")
    DB_PATH: str = os.path.join(DB_DIR, "workday_hr.db")

    # LLM Settings (properties dynamically fetch from environment)
    @property
    def LLM_PROVIDER(self) -> str:
        load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)
        return os.getenv("LLM_PROVIDER", "openai")

    @property
    def OPENAI_API_KEY(self) -> str:
        load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)
        return os.getenv("OPENAI_API_KEY", "")

    @property
    def OPENAI_MODEL(self) -> str:
        load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)
        return os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    @property
    def OPENAI_BASE_URL(self) -> str:
        load_dotenv(os.path.join(PROJECT_ROOT, ".env"), override=True)
        return os.getenv("OPENAI_BASE_URL", "")


settings = Settings()
