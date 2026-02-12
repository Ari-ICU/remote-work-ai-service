import os
import joblib
import pandas as pd
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PredictionService:
    def __init__(self):
        self.model_path = "app/ml_models/salary_model.joblib"
        self.dl_model_path = "app/ml_models/salary_dl_model.h5"
        self.preprocessor_path = "app/ml_models/salary_preprocessor.joblib"
        
        self.model = self._load_model()
        self.dl_model = self._load_dl_model()
        self.preprocessor = self._load_preprocessor()

    def _load_model(self):
        try:
            if os.path.exists(self.model_path):
                return joblib.load(self.model_path)
            return None
        except Exception as e:
            logger.error(f"Error loading scikit model: {e}")
            return None

    def _load_dl_model(self):
        try:
            if os.path.exists(self.dl_model_path):
                import tensorflow as tf
                return tf.keras.models.load_model(self.dl_model_path)
            return None
        except Exception as e:
            logger.error(f"Error loading DL model: {e}")
            return None

    def _load_preprocessor(self):
        try:
            if os.path.exists(self.preprocessor_path):
                return joblib.load(self.preprocessor_path)
            return None
        except Exception as e:
            logger.error(f"Error loading preprocessor: {e}")
            return None

    async def predict_salary(self, skills: List[str], experience_level: str, location: str, job_type: str) -> Dict[str, Any]:
        skills_str = ", ".join(skills)
        input_data = pd.DataFrame([{
            "skills": skills_str,
            "experience_level": experience_level,
            "location": location
        }])

        # 1. Try Deep Learning model first
        if self.dl_model and self.preprocessor:
            try:
                X_encoded = self.preprocessor.transform(input_data)
                prediction = float(self.dl_model.predict(X_encoded)[0][0])
                return self._format_response(prediction, 0.95, "deep_learning")
            except Exception as e:
                logger.error(f"DL Prediction failed: {e}")

        # 2. Try Scikit-learn model second
        if self.model:
            try:
                prediction = float(self.model.predict(input_data)[0])
                return self._format_response(prediction, 0.85, "random_forest")
            except Exception as e:
                logger.error(f"Scikit Prediction failed: {e}")
        
        # 3. Last Fallback
        return self._format_response(85000, 0.5, "fallback")

    def _format_response(self, value: float, confidence: float, model_type: str) -> Dict[str, Any]:
        return {
            "estimated_salary": value,
            "currency": "USD",
            "confidence_score": confidence,
            "model_used": model_type,
            "range": {
                "min": value * 0.9,
                "max": value * 1.1
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
