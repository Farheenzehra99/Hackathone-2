import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List

# BASE_DIR points to the backend folder (project root)
BASE_DIR = Path(__file__).resolve().parent.parent  # app/core -> backend/

class Settings(BaseSettings):
    BETTER_AUTH_SECRET: str = ""
    BETTER_AUTH_URL: str = ""
    DATABASE_URL: str
    DEBUG: bool = False
    LOG_LEVEL: str = "info"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://yourdomain.com"
    ]

    class Config:
        # correctly point to backend/.env
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create settings instance
settings = Settings()
