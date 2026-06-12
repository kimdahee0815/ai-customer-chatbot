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
    already_submitted = message_id in st.session_state.submitted_feedback
    
    feedback_value = st.feedback(
        "thumbs",
        key=widget_key,
        disabled=already_submitted
    )
    # 선택 전 None 상태는 저장 요청으로 보내지 X
    if feedback_value is None:
        return
    # 이미 저장한 메시지는 리턴이 일어나도 다시 보내지 X
    if already_submitted:
        st.caption("이미 저장된 피드백입니다.")
        return
    
    rating = thumb_to_rating(feedback_value)
    result = post_feedback(conversation_id, message_id, rating)
    st.session_state.submitted_feedback.add(message_id)
    st.caption(f"저장 완료: {result['message_id']} / {result['rating']}")
    
demo_message = {
    "role":"assistant",
    "message_id": "msg-ai-003",
    "content":"환불 절차는 주문 번호 확인 뒤 고객센터에서 접수할 수 있습니다."
}

st.title("피드백 데모")

with st.chat_message("assistant"):
    st.write(demo_message["content"])
    render_feedback_for_message(
        conversation_id="conv-001",
        message=demo_message,
        index=0
    )