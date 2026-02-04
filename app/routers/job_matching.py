from fastapi import APIRouter, HTTPException
from typing import List
import logging

from app.services.job_matching_service import JobMatchingService
from app.schemas.matching import JobMatchRequest, JobMatchResponse

router = APIRouter()
logger = logging.getLogger(__name__)
matching_service = JobMatchingService()

@router.post("/match-jobs", response_model=List[JobMatchResponse])
async def match_jobs(request: JobMatchRequest):
    """
    Find best matching jobs for a freelancer
    
    - Uses semantic similarity
    - Considers skills, experience, preferences
    - Returns ranked job recommendations
    """
    try:
        logger.info(f"Matching jobs for user: {request.user_id}")
        
        matches = await matching_service.find_matching_jobs(
            user_id=request.user_id,
            skills=request.skills,
            preferences=request.preferences,
            limit=request.limit or 10
        )
        
        return matches
        
    except Exception as e:
        logger.error(f"Error matching jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/match-candidates")
async def match_candidates(job_id: str, limit: int = 10):
    """
    Find best matching candidates for a job
    
    - Analyzes job requirements
    - Matches with freelancer profiles
    - Returns ranked candidates
    """
    try:
        logger.info(f"Matching candidates for job: {job_id}")
        
        candidates = await matching_service.find_matching_candidates(
            job_id=job_id,
            limit=limit
        )
        
        return candidates
        
    except Exception as e:
        logger.error(f"Error matching candidates: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/similarity-score")
async def calculate_similarity(job_description: str, resume_text: str):
    """
    Calculate similarity score between job and resume
    
    - Uses sentence transformers
    - Returns 0-1 similarity score
    """
    try:
        score = await matching_service.calculate_similarity(
            job_description,
            resume_text
        )
        
        return {"similarity_score": score}
        
    except Exception as e:
        logger.error(f"Error calculating similarity: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
