from typing import List, Dict, Any

class JobMatchingService:
    async def find_matching_jobs(self, user_id: str, skills: List[str], preferences: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
        # Mock implementation adapting to user's skills for global departments
        matching_skills_1 = skills[:2] if len(skills) >= 2 else (skills if skills else ["Project Management", "Communication"])
        matching_skills_2 = skills[:1] if len(skills) >= 1 else (skills if skills else ["Analysis"])
        return [
            {
                "job_id": "job_1",
                "similarity_score": 0.95,
                "matching_skills": matching_skills_1,
                "missing_skills": ["Leadership"]
            },
            {
                "job_id": "job_2",
                "similarity_score": 0.85,
                "matching_skills": matching_skills_2,
                "missing_skills": ["Problem Solving", "Time Management"]
            }
        ]

    async def find_matching_candidates(self, job_id: str, limit: int) -> List[Dict[str, Any]]:
        return [
            {
                "user_id": "user_1",
                "match_score": 0.92,
                "skills": ["Management", "Communication", "Strategy"]
            }
        ]

    async def calculate_similarity(self, text1: str, text2: str) -> float:
        # Simple overlap coefficient for mock
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0.0
