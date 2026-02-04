from fastapi import APIRouter, HTTPException
import logging

from app.services.prediction_service import PredictionService
from app.schemas.predictions import SalaryPredictionRequest, FraudDetectionRequest

router = APIRouter()
logger = logging.getLogger(__name__)
prediction_service = PredictionService()

@router.post("/salary")
async def predict_salary(request: SalaryPredictionRequest):
    """
    Predict salary for a job posting
    
    - Uses ML model trained on historical data
    - Considers skills, experience, location
    """
    try:
        logger.info("Predicting salary")
        
        prediction = await prediction_service.predict_salary(
            skills=request.skills,
            experience_level=request.experience_level,
            location=request.location,
            job_type=request.job_type
        )
        
        return prediction
        
    except Exception as e:
        logger.error(f"Error predicting salary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fraud-detection")
async def detect_fraud(request: FraudDetectionRequest):
    """
    Detect potentially fraudulent job postings
    
    - Analyzes job description patterns
    - Checks for red flags
    - Returns fraud probability score
    """
    try:
        logger.info(f"Checking fraud for job: {request.job_id}")
        
        result = await prediction_service.detect_fraud(
            job_description=request.job_description,
            employer_info=request.employer_info
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error detecting fraud: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend")
async def get_recommendations(user_id: str, limit: int = 10):
    """
    Get personalized job recommendations
    
    - Uses collaborative filtering
    - Considers user behavior and preferences
    """
    try:
        logger.info(f"Getting recommendations for user: {user_id}")
        
        recommendations = await prediction_service.get_recommendations(
            user_id=user_id,
            limit=limit
        )
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
