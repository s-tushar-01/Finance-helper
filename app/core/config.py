from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Finance Backend System"
    # Fallback to SQLite if not provided
    DATABASE_URL: str = "sqlite:///./finance.db"
    
    # JWT Settings (Change in production!)
    SECRET_KEY: str = "supersecretkey" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
