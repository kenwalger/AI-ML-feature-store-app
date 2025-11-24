"""Application configuration management"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database URLs - handle both DATABASE_URL (Heroku) and database_url
    database_url: str = os.getenv("DATABASE_URL", "")
    follower_database_url: Optional[str] = os.getenv("FOLLOWER_DATABASE_URL")
    
    # Heroku Managed Inference (Cohere)
    heroku_ai_api_key: Optional[str] = None
    heroku_ai_model_id: str = "cohere-embed-english-v3.0"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Application settings
    use_follower_pool: bool = False
    log_level: str = "INFO"
    environment: str = "development"
    
    # Heroku specific
    port: int = 5000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

