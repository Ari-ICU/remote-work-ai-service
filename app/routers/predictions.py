from fastapi import APIRouter, HTTPException, Depends
import logging
from app.services.prediction_service import PredictionService
from app.schemas.predictions import SalaryPredictionRequest, SalaryPredictionResponse

router = APIRouter()
logger = logging.getLogger(__name__)

def get_prediction_service():
    return PredictionService()

@router.post("/salary", response_model=SalaryPredictionResponse)
async def predict_salary(
    request: SalaryPredictionRequest,
    service: PredictionService = Depends(get_prediction_service)
):
    """Predict market salary based on skills and experience"""
    try:
        result = await service.predict_salary(
            skills=request.skills,
            experience_level=request.experience_level,
            location=request.location or "Remote",
            job_type=request.job_type or "Full-time"
        )
        return SalaryPredictionResponse(**result)
    except Exception as e:
        logger.error(f"Failed to predict salary: {e}")
        raise HTTPException(status_code=500, detail="Failed to predict salary")
