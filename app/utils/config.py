from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False
    )

    APP_NAME: str = "Freelance Platform AI Service"
    API_V1_STR: str = "/api/v1"
    
    # AI Models
    INTENT_MODEL_PATH: str = "app/ml_models/intent_model.joblib"
    SALARY_MODEL_PATH: str = "app/ml_models/salary_model.joblib"
    MATCHING_MODEL_PATH: str = "app/ml_models/matching_model.pkl"
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Redis & Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # Cors
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001", "https://remote-work-frontend-flame.vercel.app"]

settings = Settings()
