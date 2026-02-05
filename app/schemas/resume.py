from pydantic import BaseModel
from typing import List, Optional, Dict

class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None

class Experience(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None

class ResumeParseResponse(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    education: List[Education] = []
    experience: List[Experience] = []
    raw_text: Optional[str] = None

class SkillExtractionResponse(BaseModel):
    skills: Dict[str, List[str]]
    total_count: int = 0
