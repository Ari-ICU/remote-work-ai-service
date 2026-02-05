from typing import List, Dict, Any

class PredictionService:
    async def predict_salary(self, skills: List[str], experience_level: str, location: str, job_type: str) -> Dict[str, Any]:
        return {
            "predicted_salary": 85000,
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
