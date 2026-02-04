from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, List
import logging

from app.services.resume_service import ResumeParserService
from app.schemas.resume import ResumeParseResponse, SkillExtractionResponse

router = APIRouter()
logger = logging.getLogger(__name__)
resume_service = ResumeParserService()

@router.post("/parse", response_model=ResumeParseResponse)
async def parse_resume(file: UploadFile = File(...)):
    """
    Parse resume and extract structured information
    
    - Extracts skills, experience, education
    - Supports PDF, DOCX formats
    - Uses NLP for entity recognition
    """
    try:
        logger.info(f"Parsing resume: {file.filename}")
        
        # Validate file type
        if not file.filename.endswith(('.pdf', '.docx', '.doc')):
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported"
            )
        
        # Parse resume
        result = await resume_service.parse_resume(file)
        
        return result
        
    except Exception as e:
        logger.error(f"Error parsing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-skills", response_model=SkillExtractionResponse)
async def extract_skills(text: str):
    """
    Extract skills from text using NLP
    
    - Uses NER (Named Entity Recognition)
    - Returns categorized skills
    """
    try:
        logger.info("Extracting skills from text")
        
        skills = await resume_service.extract_skills(text)
        
        return {"skills": skills}
        
    except Exception as e:
        logger.error(f"Error extracting skills: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    """
    Deep analysis of resume including:
    - Skill proficiency estimation
    - Experience level detection
    - Resume quality score
    """
    try:
        logger.info(f"Analyzing resume: {file.filename}")
        
        analysis = await resume_service.analyze_resume(file)
        
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
