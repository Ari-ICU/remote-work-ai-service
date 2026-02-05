from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routers import resume_parser, job_matching, predictions, training, chat
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
    logger.info("Loading ML models...")
    # TODO: Load models here
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
