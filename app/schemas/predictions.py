from pydantic import BaseModel
from typing import List, Optional, Dict

class SalaryPredictionRequest(BaseModel):
    skills: List[str]
    experience_level: str
    location: Optional[str] = None
    job_type: Optional[str] = None

class SalaryPredictionResponse(BaseModel):
    estimated_salary: float
    currency: str = "USD"
    confidence_score: float

class FraudDetectionRequest(BaseModel):
    job_id: str
    job_description: str
    employer_info: Dict[str, str]

class FraudDetectionResponse(BaseModel):
    is_fraudulent: bool
    risk_score: float
    flags: List[str]
