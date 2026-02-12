import os
import joblib
import pandas as pd
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        self.model_path = "app/ml_models/salary_model.joblib"
        self.model = self._load_model()

    def _load_model(self):
        try:
            if os.path.exists(self.model_path):
                logger.info(f"Loading model from {self.model_path}")
                return joblib.load(self.model_path)
            else:
                logger.warning(f"No model found at {self.model_path}, using fallback logic")
                return None
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return None

    async def predict_salary(self, skills: List[str], experience_level: str, location: str, job_type: str) -> Dict[str, Any]:
        if self.model:
            try:
                # Prepare input for prediction
                # Skills should be comma-separated string
                skills_str = ", ".join(skills)
                input_df = pd.DataFrame([{
                    "skills": skills_str,
                    "experience_level": experience_level,
                    "location": location
                }])
                
                prediction = self.model.predict(input_df)[0]
                
                return {
                    "estimated_salary": float(prediction),
                    "currency": "USD",
                    "confidence_score": 0.85,
                    "range": {
                        "min": float(prediction * 0.9),
                        "max": float(prediction * 1.1)
                    }
                }
            except Exception as e:
                logger.error(f"Prediction failed: {str(e)}")
        
        # Fallback to hardcoded values if model is missing or fails
        return {
            "estimated_salary": 85000,
            "currency": "USD",
            "confidence_score": 0.85,
            "range": {
                "min": 75000,
                "max": 95000
            }
        }

    async def detect_fraud(self, job_description: str, employer_info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "fraud_probability": 0.05,
            "is_suspicious": False,
            "flags": []
        }

    async def get_recommendations(self, user_id: str, limit: int) -> List[Dict[str, Any]]:
        return [
            {
                "job_id": "rec_1",
                "title": "Recommended Job 1",
                "score": 0.9
            },
            {
                "job_id": "rec_2",
                "title": "Recommended Job 2",
                "score": 0.8
            }
        ]
