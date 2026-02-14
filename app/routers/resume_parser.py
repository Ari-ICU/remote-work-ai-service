from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
import logging
from app.services.resume_service import ResumeParserService

router = APIRouter()
logger = logging.getLogger(__name__)

def get_resume_service():
    return ResumeParserService()

@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...),
    service: ResumeParserService = Depends(get_resume_service)
):
    """Parse a resume file and extract structured data"""
    try:
        result = await service.parse_resume(file)
        return result
    except Exception as e:
        logger.error(f"Failed to parse resume: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse resume")

@router.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    service: ResumeParserService = Depends(get_resume_service)
):
    """Analyze a resume and provide feedback"""
    try:
        result = await service.analyze_resume(file)
        return result
    except Exception as e:
        logger.error(f"Failed to analyze resume: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze resume")
