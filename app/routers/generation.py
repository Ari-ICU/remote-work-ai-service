from fastapi import APIRouter, HTTPException, Depends
import logging

from app.services.generation_service import GenerationService
from app.schemas.generation import (
    ProposalRequest, ProposalResponse,
    JobDescriptionRequest, JobDescriptionResponse,
    InterviewQuestionsRequest, InterviewQuestionsResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)

def get_generation_service():
    return GenerationService()

@router.post("/proposal", response_model=ProposalResponse)
async def generate_proposal(
    request: ProposalRequest, 
    service: GenerationService = Depends(get_generation_service)
):
    """Generate an AI-powered project proposal"""
    try:
        proposal = await service.generate_proposal(
            job_title=request.job_title,
            job_description=request.job_description,
            user_skills=request.user_skills,
            user_bio=request.user_bio,
            tone=request.tone
        )
        return ProposalResponse(proposal=proposal)
    except Exception as e:
        logger.error(f"Failed to generate proposal: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate proposal")

@router.post("/job-description", response_model=JobDescriptionResponse)
async def generate_job_description(
    request: JobDescriptionRequest,
    service: GenerationService = Depends(get_generation_service)
):
    """Generate an AI-powered job description"""
    try:
        data = await service.generate_job_description(
            title=request.title,
            industry=request.industry,
            key_points=request.key_points,
            experience_level=request.experience_level
        )
        return JobDescriptionResponse(**data)
    except Exception as e:
        logger.error(f"Failed to generate job description: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate job description")

@router.post("/interview-questions", response_model=InterviewQuestionsResponse)
async def generate_interview_questions(
    request: InterviewQuestionsRequest,
    service: GenerationService = Depends(get_generation_service)
):
    """Generate tailored interview questions"""
    try:
        questions = await service.generate_interview_questions(
            job_title=request.job_title,
            job_description=request.job_description,
            candidate_skills=request.candidate_skills,
            candidate_bio=request.candidate_bio
        )
        return InterviewQuestionsResponse(questions=questions)
    except Exception as e:
        logger.error(f"Failed to generate interview questions: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate interview questions")
