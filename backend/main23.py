from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI

from backend.schemas import ChatRequest, ChatResponse

load_dotenv()

app = FastAPI(title="Customer Support Chatbot API")

openai_api_key = os.getenv("OPENAI_API_KEY")
# Streamlit 개발 서버가 열리는 origin만 허용합니다.
allowed_origins= ["http://localhost:8501", "http://192.168.1.161:8501"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,       # 허용할 출처
    allow_credentials=True,
    allow_methods=["*"],       # 허용할 HTTP 메서드
    allow_headers=["*"],       # 허용할 헤더
)

# 실제로 API 키가 있을 때만 클라이언트가 준비가 된다.
# 키가 없어도 CORS와 health_check 가능하다.
app.state.openai_client = (
    AsyncOpenAI(api_key=openai_api_key)
    if openai_api_key
    else None
)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/lim/status")
async def lim_status()->dict[str, str]:
    """OpenAI 클라이언트 준비 상태를 확인"""
    if app.state.openai_client is None:
        return {"openai_client": "not_configured"}
    return {"openai_client": "ready"}