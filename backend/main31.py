from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import Field

class ChatRequest(BaseModel):
    """프론트엔드가 /chat으로 보내는 요청 형식"""
    message: str = Field(min_length=1)
    
class ChatResponse(BaseModel):
    """프론트엔드가 화면에 표시할 일반 응답"""
    message: str
    
app = FastAPI(title="고객 상담 챗봇")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(message=f"접수된 상담 메시지: {request.message}")