from typing import Any
from typing import Literal

import httpx
import streamlit as st 
from api_client import get_backend_url

Rating = Literal["up", "down"]

def ensure_feedback_state() -> None:
    """중복 제출을 막기 위한 feedback 상태 저장소를 준비"""
    if "submitted_feedback" not in st.session_state:
        st.session_state.submitted_feedback = set()
        
def thumb_to_rating(value: int) -> Rating:
    """st.feedback 선택 인덱스를 저장용 rating 문자열로 변환"""
    return "up" if value == 1 else "down"

def post_feedback(conversation_id: str, message_id: str, rating: Rating) -> dict[str, Any]:
    """백엔드에 피드백을 저장하고 JSON 응답을 돌려받는다."""
    payload = {
        "conversation_id": conversation_id,
        "message_id": message_id,
        "rating": rating
    }
    
    response = httpx.post(get_backend_url() + "/feedback", json=payload, timeout=5.0)
    response.raise_for_status()
    return response.json()

def render_feedback_for_message(conversation_id: str, message: dict[str, str], index:int) -> None:
    """AI message 1개 아래에 피드백 위젯과 저장 상태를 표시"""
    ensure_feedback_state()
    
    message_id = message["message_id"]
    widget_key=  f"fb_{message_id}_{index}"