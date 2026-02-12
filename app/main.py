from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routers import resume_parser, job_matching, predictions, training, chat, generation
from app.utils.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("🤖 AI Service starting up...")
    logger.info("Checking for trained models...")
    
    import os
    model_path = "app/ml_models/salary_model.joblib"
    intent_model_path = "app/ml_models/intent_model.joblib"
    
    if os.path.exists(model_path):
        logger.info(f"✅ Found trained salary model at {model_path}")
    else:
        logger.warning("⚠️ No trained salary model found.")
        
    if os.path.exists(intent_model_path):
        logger.info(f"✅ Found trained intent model at {intent_model_path}")
    else:
        logger.warning("⚠️ No trained intent model found. Chat will use rule-based fallback.")
        
    yield
    # Shutdown
    logger.info("🛑 AI Service shutting down...")

# Create FastAPI app
app = FastAPI(
    title="Freelance Platform AI Service",
    description="AI/ML microservice for resume parsing, job matching, and predictions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume_parser.router, prefix="/api/ai/resume", tags=["Resume Parser"])
app.include_router(job_matching.router, prefix="/api/ai/matching", tags=["Job Matching"])
app.include_router(predictions.router, prefix="/api/ai/predictions", tags=["Predictions"])
app.include_router(training.router, prefix="/api/ai/training", tags=["Model Training"])
app.include_router(chat.router, prefix="/api/ai/chat", tags=["AI Chat"])
app.include_router(generation.router, prefix="/api/ai/generation", tags=["AI Generation"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Freelance Platform AI Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "models_loaded": True,  # TODO: Check actual model status
        "database": "connected"  # TODO: Check DB connection
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
