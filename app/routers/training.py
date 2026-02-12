from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
import logging
from app.services.training_service import TrainingService

router = APIRouter()
logger = logging.getLogger(__name__)

# Mock dependency for TrainingService
def get_training_service():
    return TrainingService()

async def train_model_task(model_type: str, dataset_path: str, training_service: TrainingService):
    """Background task for model training"""
    try:
        if model_type == "salary_prediction":
            await training_service.train_salary_model(dataset_path)
        elif model_type == "fraud_detection":
            await training_service.train_fraud_model(dataset_path)
        elif model_type == "intent_classification":
            await training_service.train_intent_model(dataset_path)
        else:
            logger.error(f"Unknown model type: {model_type}")
    except Exception as e:
        logger.error(f"Background training failed: {str(e)}")

@router.post("/train-model")
async def train_model(
    model_type: str,
    dataset_path: str = None,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    training_service: TrainingService = Depends(get_training_service)
):
    """
    Train or retrain ML models
    
    - Runs in background
    - Supports: salary_prediction, fraud_detection
    """
    try:
        logger.info(f"Starting training for model: {model_type}")
        
        # Add training task to background
        background_tasks.add_task(train_model_task, model_type, dataset_path, training_service)
        
        return {
            "status": "training_started",
            "model_type": model_type,
            "message": "Model training has been queued"
        }
        
    except Exception as e:
        logger.error(f"Error starting training: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-status/{model_type}")
async def get_model_status(model_type: str):
    """Get training status and model metrics"""
    try:
        # TODO: Implement actual status check from a database or file
        import os
        model_path = f"app/ml_models/{model_type.replace('_prediction', '_model')}.joblib"
        exists = os.path.exists(model_path)
        
        return {
            "model_type": model_type,
            "status": "ready" if exists else "no_model_found",
            "accuracy": 0.85 if exists else 0.0,
            "last_trained": "2024-02-04T10:00:00Z" if exists else None
        }
        
    except Exception as e:
        logger.error(f"Error getting model status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
