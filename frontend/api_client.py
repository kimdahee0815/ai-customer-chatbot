import os
from typing import Any
import httpx
import requests
from dotenv import load_dotenv

load_dotenv()

def get_backend_url() -> str:
    """FastAPI 백엔드 기본 주소를 반환"""
    return os.getenv('BACKEND_URL', "http://localhost:8001").rstrip("/")

def call_chat_api(message: str)->dict[str, Any]:
    """백엔드 /chat 엔드포인트에 일반 POST 요청을 보내고 JSON응답을 반환"""
    backend_url = get_backend_url()
    with httpx.Client(base_url=backend_url, timeout=10.0) as client:
        response = client.post("/chat",json={"message":message})
        # 200
        # 2xx, 3xx: 정상처리, 4xx: 주소가 없음, 5xx: 서버 프로그램 오류
        # HTTPStatusError 익셉션 발생
        response.raise_for_status()
        
        return response.json()
        