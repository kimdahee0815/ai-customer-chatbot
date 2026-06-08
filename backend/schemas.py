from pydantic import BaseModel
from pydantic import Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="사용자가 입력한 상담 메시지")
    topic: str = Field(default="general", description="상담 주제")
    
class ChatResponse(BaseModel):
    reply: str
    status: str = "ok"