from fastapi import APIRouter, HTTPException, Depends
import logging
from app.services.job_matching_service import JobMatchingService
from app.schemas.matching import SimilarityRequest

router = APIRouter()
logger = logging.getLogger(__name__)

def get_matching_service():
    return JobMatchingService()

@router.post("/similarity-score")
async def get_similarity_score(
    request: SimilarityRequest,
    service: JobMatchingService = Depends(get_matching_service)
):
    """Calculate similarity score between job and resume"""
    try:
        score = await service.calculate_similarity(
            job_description=request.job_description,
            resume_text=request.resume_text
        )
        return {"similarity_score": score}
    except Exception as e:
        logger.error(f"Failed to calculate similarity score: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate similarity score")
