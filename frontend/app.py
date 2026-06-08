import os
import httpx
import streamlit as st

def get_backend_url():
    return os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

BACKEND_URL = get_backend_url()

st.set_page_config(page_title="AI 고객 상담 챗봇")
st.caption(f"Backend: {BACKEND_URL}")
st.title("AI 고객 상담 챗봇")
st.write("프론트엔드 Streamlit 화면에서 백엔드 FastAPI 서버로 요청을 보내는 예제.")
message = st.text_input("상담 메시지", placeholder="예: 베송이 지연되고 있어요.")
topic = st.selectbox("상담 주제", ["general", "delivery", "refund", "technical"])

if st.button("백엔드로 보내기"):
    if not message.strip():
        st.warning("메시지를 먼저 입력하세요.")
    else:
        try:
            with httpx.Client(base_url=BACKEND_URL, timeout=10.0) as client:
                response = client.post("/chat", json={"message": message, "topic": topic})
                response.raise_for_status()
            data = response.json()
            st.success(data["reply"])
            st.json(data)
        except httpx.ConnectError:
            st.error("백엔드 서버에 연결할 수 없습니다.")
        except httpx.HTTPStatusError as exc:
            st.error(f"백엔드가 오류 응답을 보냈습니다. {exc.response.status_code}")