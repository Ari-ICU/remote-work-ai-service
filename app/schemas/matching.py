from pydantic import BaseModel
from typing import List, Optional, Dict

class JobMatchRequest(BaseModel):
    user_id: str
    skills: List[str]
    preferences: Optional[Dict[str, str]] = None
    limit: int = 10

class JobMatchResponse(BaseModel):
    job_id: str
    title: str
    match_score: float
    matching_skills: List[str]
    missing_skills: List[str]

class SimilarityRequest(BaseModel):
    job_description: str
    resume_text: str
