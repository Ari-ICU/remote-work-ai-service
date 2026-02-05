from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://freelance_user:freelance_pass@localhost:5432/freelance_platform"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # AI/ML
    MODEL_PATH: str = "./app/ml_models"
    HUGGINGFACE_TOKEN: str = ""
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    # Vector DB
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "us-east-1-aws"
    PINECONE_INDEX_NAME: str = "freelance-jobs"
    
    # App
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    
    # Celery
    CELERY_BROKER_URL: str = ""
    CELERY_RESULT_BACKEND: str = ""
    
    def __init__(self, **values):
        super().__init__(**values)
        if not self.CELERY_BROKER_URL:
            self.CELERY_BROKER_URL = f"{self.REDIS_URL}/0"
        if not self.CELERY_RESULT_BACKEND:
            self.CELERY_RESULT_BACKEND = f"{self.REDIS_URL}/0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

settings = get_settings()
