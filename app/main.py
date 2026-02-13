from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, generation, training
# from app.routers import job_matching # Commented out if not ready or use if available
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
    "https://freelance-platform-frontend.vercel.app", # Adjust as needed
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

# Include routers
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(generation.router, prefix="/api/v1/generation", tags=["Generation"])
app.include_router(training.router, prefix="/api/v1/training", tags=["Training"])

# Add other routers as needed
# app.include_router(job_matching.router, prefix="/api/v1/matching", tags=["Matching"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
