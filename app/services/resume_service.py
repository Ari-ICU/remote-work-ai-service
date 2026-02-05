from fastapi import UploadFile
from typing import List, Dict, Any

class ResumeParserService:
    async def parse_resume(self, file: UploadFile) -> Dict[str, Any]:
        # Mock implementation
        return {
            "name": "John Doe",
            "email": "john@example.com",
            "skills": ["Python", "JavaScript", "SQL"],
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "Tech Corp",
                    "duration": "2 years"
                }
            ],
            "education": [
                {
                    "degree": "B.Sc. Computer Science",
                    "university": "University of Technology"
                }
            ]
        }

    async def extract_skills(self, text: str) -> List[str]:
        # Mock skill extraction
        common_skills = ["python", "javascript", "java", "sql", "react", "node", "aws"]
        text_lower = text.lower()
        return [skill for skill in common_skills if skill in text_lower]

    async def analyze_resume(self, file: UploadFile) -> Dict[str, Any]:
        return {
            "score": 85,
            "level": "Senior",
            "suggestions": [
                "Add more quantitative results",
                "Highlight leadership experience"
            ]
        }
