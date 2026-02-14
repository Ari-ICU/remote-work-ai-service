from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, generation, training, predictions, job_matching, resume_parser
import uvicorn
import os

app = FastAPI(
    title="Freelance Platform AI Service",
    description="AI Service for Freelance Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://remote-work-frontend-flame.vercel.app",
    "https://freelance-backend.onrender.com",
    "*" # Allow all for now, restrict in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Freelance Platform AI Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Include routers - Mapped to match NestJS backend expectations
app.include_router(chat.router, prefix="/api/ai/chat", tags=["Chat"])
app.include_router(generation.router, prefix="/api/ai/generation", tags=["Generation"])
app.include_router(training.router, prefix="/api/ai/training", tags=["Training"])
app.include_router(predictions.router, prefix="/api/ai/predictions", tags=["Predictions"])
app.include_router(job_matching.router, prefix="/api/ai/matching", tags=["Matching"])
app.include_router(resume_parser.router, prefix="/api/ai/resume", tags=["Resume"])

# Legacy v1 prefixes for backward compatibility if any
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Legacy Chat"])
app.include_router(generation.router, prefix="/api/v1/generation", tags=["Legacy Generation"])
app.include_router(training.router, prefix="/api/v1/training", tags=["Legacy Training"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
