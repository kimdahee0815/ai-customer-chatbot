from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from backend.schemas import ChatRequest, ChatResponse

load_dotenv()

app = FastAPI(title="Customer Support Chatbot API")

# Streamlit 개발 서버가 열리는 origin만 허용합니다.
allowed_origins= ["http://localhost:8501", "http://192.168.1.161:8501"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,       # 허용할 출처
    allow_credentials=True,
    allow_methods=["*"],       # 허용할 HTTP 메서드
    allow_headers=["*"],       # 허용할 헤더
)

@app.get("/health")
def health_check() -> dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    value = ""
    if not api_key:
        value = "false"
    else:
        value = "true"
    return {"status": value}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    reply = f"'{request.message}' 요청을 접수했습니다. 상담 주제는 {request.topic}입니다."
    return ChatResponse(reply=reply)