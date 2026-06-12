from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # CORS 보안 설정
import os
from backend import stream_router
from backend import agents_router

app = FastAPI(title="Customer Support Chatbot API")

# Streamlit 개발 서버가 열리는 origin만 허용합니다.
allowed_origins = ["http://localhost:8501", "http://192.168.1.161:8501"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=allowed_origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

app.include_router(stream_router.router)
app.include_router(agents_router.router)

@app.get("/health")
def health_check() -> dict[str, str]:    
  return {"status": "ok"}

