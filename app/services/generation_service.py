import logging
import json
from typing import List, Optional
from openai import OpenAI
from app.utils.config import settings

logger = logging.getLogger(__name__)

class GenerationService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    async def generate_proposal(
        self, 
        job_title: str, 
        job_description: str, 
        user_skills: List[str],
        user_bio: Optional[str] = None,
        tone: str = "professional"
    ) -> str:
        """Generate a personalized job proposal/cover letter"""
        
        if not self.client:
            return self._mock_proposal(job_title, job_description, user_skills)

        prompt = f"""
        Role: Expert Freelance Career Coach
        Task: Write a high-converting cover letter for a freelancer.
        
        Job Details:
        Title: {job_title}
        Description: {job_description}
        
        Freelancer Details:
        Skills: {", ".join(user_skills)}
        Bio: {user_bio or "N/A"}
        
        Requirements:
        1. Tone should be {tone}.
        2. Keep it concise (under 250 words).
        3. Highlight how the freelancer's specific skills solve the project's needs.
        4. Focus on value and results.
        5. DO NOT use placeholders like [Name] - assume the recipient knows the freelancer's name.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating proposal: {e}")
            return self._mock_proposal(job_title, job_description, user_skills)

    async def generate_job_description(
        self,
        title: str,
        industry: str,
        key_points: Optional[str] = None,
        experience_level: str = "Intermediate"
    ) -> dict:
        """Generate a complete job description with responsibilities and requirements"""
        
        if not self.client:
            return self._mock_job_description(title, industry)

        prompt = f"""
        Task: Create a professional job posting for the position of "{title}" in the "{industry}" industry.
        Experience Level: {experience_level}
        Key Points to include: {key_points or "N/A"}
        
        Return the result as a JSON object with exactly these keys:
        - "description": A 2-3 paragraph overview of the role.
        - "responsibilities": A list of 5-7 bullet points.
        - "requirements": A list of 5-7 technical and soft skill requirements.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error generating job description: {e}")
            return self._mock_job_description(title, industry)

    async def generate_interview_questions(
        self,
        job_title: str,
        job_description: str,
        candidate_skills: List[str],
        candidate_bio: Optional[str] = None
    ) -> List[str]:
        """Generate tailored interview questions based on job and candidate profile"""
        
        if not self.client:
            return self._mock_interview_questions(job_title)

        prompt = f"""
        Role: Expert Technical Interviewer
        Task: Generate 4 unique, challenging interview questions tailored to this specific candidate's profile for the given job.
        
        Job Title: {job_title}
        Job Description: {job_description}
        
        Candidate Skills: {", ".join(candidate_skills)}
        Candidate Bio: {candidate_bio or "N/A"}
        
        Requirements:
        1. Questions should probe the gap between the candidate's skills and the job requirements.
        2. Focus on specific technical scenarios and behavioral insights.
        3. Make them insightful, not generic.
        
        Return the result as a JSON object with a single key "questions" containing a list of strings.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.8
            )
            data = json.loads(response.choices[0].message.content)
            return data.get("questions", self._mock_interview_questions(job_title))
        except Exception as e:
            logger.error(f"Error generating interview questions: {e}")
            return self._mock_interview_questions(job_title)

    def _mock_proposal(self, job_title: str, job_description: str, skills: List[str]) -> str:
        skill_str = ", ".join(skills[:3]) if skills else "relevant technologies"
        all_skills = ", ".join(skills) if skills else "industry-standard tools"
        snippet = " ".join(job_description.split())[:120] + "..." if job_description else "the core tasks outlined in your project requirements"
        
        return (
            f"Dear Hiring Manager,\n\n"
            f"I am writing to express my strong interest in the {job_title} position. "
            f"Having reviewed the project requirements detailing '{snippet}', I am incredibly excited about the "
            f"prospect of bringing my expertise to your team.\n\n"
            f"With a proven track record of delivering high-impact solutions and a robust background in {skill_str}, "
            f"I am fully confident in my ability to immediately add value and help you achieve your goals. "
            f"Throughout my career, I have successfully executed complex, data-driven projects that demanded meticulous "
            f"attention to detail and highly scalable architecture. My deep proficiency in {all_skills} enables me to tackle "
            f"both technical and functional challenges from multiple angles, ensuring resilient and innovative outcomes.\n\n"
            f"I consistently pride myself on developing clean, maintainable systems and building products that offer exceptional user experiences, "
            f"which aligns perfectly with the objectives of your {job_title} initiative. In my past roles, "
            f"I have optimized performance, resolved critical bottlenecks early in the development lifecycle, and "
            f"implemented modernized large-scale workflows seamlessly. I am deeply passionate about "
            f"translating your complex business requirements into tangible metrics of success.\n\n"
            f"I would welcome the opportunity to discuss how my tailored skills in {skill_str} can be effectively leveraged to "
            f"accelerate your timeline and ensure the highest quality results for your platform. Thank you for considering my application. "
            f"I genuinely look forward to the possibility of collaborating with you on this exciting project.\n\n"
            f"Best regards,\n[Your Name]"
        )

    def _mock_job_description(self, title: str, industry: str) -> dict:
        return {
            "description": f"We are seeking a talented {title} to join our team in the {industry} sector. This is an exciting opportunity to work on innovative projects and make a real impact.",
            "responsibilities": [
                f"Develop and maintain {title} solutions",
                "Collaborate with cross-functional teams",
                "Ensure high performance and responsiveness of applications",
                "Participate in code reviews and architectural discussions",
                "Troubleshoot and debug issues"
            ],
            "requirements": [
                f"Proven experience as a {title}",
                f"Strong knowledge of {industry} standards",
                "Excellent communication and teamwork skills",
                "Ability to work independently and meet deadlines",
                "Problem-solving mindset"
            ]
        }

    def _mock_interview_questions(self, title: str) -> List[str]:
        return [
            f"Can you describe a challenging project you've worked on as a {title}?",
            "How do you stay updated with the latest trends and technologies in your field?",
            "Describe a time you had to solve a difficult technical problem with limited information.",
            "What is your preferred workflow when collaborating with a remote team?"
        ]
