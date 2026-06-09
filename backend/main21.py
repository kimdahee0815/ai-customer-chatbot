from fastapi import FastAPI

from backend.schemas21 import ChatRequest, ChatResponse


app = FastAPI(title="Customer Support Chatbot API", version="0.1.0")

@app.get("/health")
def health_check() -> dict[str, str]:
    """서버가 실행 중인지 확인"""
    return {"status": "김다희"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """고객 상담 메시지를 받아 테스트 응답을 반환"""
    reply = (f"'{request.customer_id}님의 '{request.message}' 요청을 접수했습니다. 상담 주제는 {request.topic}입니다."
            "지금은 FastAPI와 Pydantic 계약을 확인하는 단계")
    return ChatResponse(reply=reply, status="ok")