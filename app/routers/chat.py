from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.chat_service import ChatService

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

def get_chat_service():
    return ChatService()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, service: ChatService = Depends(get_chat_service)):
    reply = await service.get_response(request.message)
    return ChatResponse(reply=reply)
