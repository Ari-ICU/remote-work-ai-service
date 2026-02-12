from pydantic import BaseModel
from typing import List, Optional

class ProposalRequest(BaseModel):
    job_title: str
    job_description: str
    user_skills: List[str]
    user_bio: Optional[str] = None
    tone: Optional[str] = "professional"

class ProposalResponse(BaseModel):
    proposal: str

class JobDescriptionRequest(BaseModel):
    title: str
    industry: str
    key_points: Optional[str] = None
    experience_level: Optional[str] = "Intermediate"

class JobDescriptionResponse(BaseModel):
    description: str
    responsibilities: List[str]
    requirements: List[str]

class InterviewQuestionsRequest(BaseModel):
    job_title: str
    job_description: str
    candidate_bio: Optional[str] = None
    candidate_skills: List[str]

class InterviewQuestionsResponse(BaseModel):
    questions: List[str]
