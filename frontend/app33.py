import streamlit as st 
import os
import httpx
import json

from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

def parse_sse_payload(raw_payload:str) -> dict[str, str]:
    """SSE data payload를 token/status dict로 정규화한다."""
    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError:
        return {"type": "token", "delta":raw_payload}
    if isinstance(payload, dict):
        return {str(key): str(value) for key,value in payload.items()}
    return {"type":"token", "delta": str(payload)}

def stream_backend_response(endpoint: str, message: str, status_area, message_area) -> str:
    """선택된 endpoint 에서 SSE를 받아 본문과 상태 표시를 갱신합니다."""
    collected = ""
    url = f"{BACKEND_URL}{endpoint}"
    with httpx.stream(
        "POST",
        url,
        json={"message":message},
        timeout=60.0
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line.startswith("data:"):
                continue
            raw_payload = line[len("data:"):].strip()
            if raw_payload == "[DONE]":
                break
            payload = parse_sse_payload(raw_payload)
            if payload.get("type") == "status":
                status_area.caption(payload.get("label", "진행 상태 갱신"))
            else:
                collected += payload.get("delta", "")
                message_area.markdown(collected)
    return collected   

st.title("고객 상담 챗봇")
mode = st.sidebar.radio("모드", ["일반 챗봇", "기술 챗봇", "멀티에이전트"])
endpoint = "/agents/stream" if mode == "멀티에이전트" else "/chat/stream"

prompt = st.chat_input("상담 내용을 입력해 주세요.")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        status_area = st.empty()
        message_area = st.empty()
        
        final_text = stream_backend_response(endpoint, prompt, status_area, message_area)
    st.session_state["last_mode"] = mode
    st.session_state["last_response"] = final_text