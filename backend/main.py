from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import ChatRequest, ChatResponse


app = FastAPI(title="Customer Support Chatbot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],       # 허용할 출처
    allow_credentials=True,
    allow_methods=["*"],       # 허용할 HTTP 메서드
    allow_headers=["*"],       # 허용할 헤더
)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    reply = f"'{request.message}' 요청을 접수했습니다. 상담 주제는 {request.topic}입니다."
    return ChatResponse(reply=reply)