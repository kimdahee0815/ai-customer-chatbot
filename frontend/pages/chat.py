import streamlit as st
from api_client import stream_chat
import httpx

st.title("고객 상담 챗봇")
st.caption("채팅 페이지는 화면 렌더링과 입력 처리만 담당합니다.")

if "messages" not in st.session_state:
  st.session_state.messages = []
if "current_status" not in st.session_state:
  st.session_state.current_status = "대기 중"

with st.sidebar:
  st.subheader("채팅 모드")
  chat_mode = st.radio("응답 방식을 선택하세요.", options=["일반 챗봇", "멀티에이전트"], index=1)
  st.caption("일반 챗봇은 /chat/stream, 멀티에이저트는 /agents/stream 호출합니다.")

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

status_box = st.empty()
status_box.caption(f"상태: {st.session_state.current_status}")

prompt = st.chat_input("상담 내용을 입력하세요.")

if prompt:
  user_prompt = {"role": "user", "content": prompt}
  st.session_state.messages.append(
    user_prompt
  )
  with st.chat_message("user"):
    st.markdown(prompt)

  st.info("이 위치에서 백엔드 API 호출.")
  assistant_text = ""
  with st.chat_message("assistant"):
    message_box = st.empty()
    
    try:
      for event in stream_chat(prompt, mode=chat_mode):
        if event.event_type == "token":
          assistant_text += event.text
          message_box.markdown(assistant_text)
        elif event.event_type == "status":
          st.session_state.current_status = event.text
          status_box.caption(f"상태: {event.text}")
        elif event.event_type == "done":
          break
    except httpx.HTTPError as exc:
      st.error(f"백엔드 연결 확인: {exc}")
  if assistant_text:
    st.session_state.messages.append(
      {
        "role": "assistant", "content": assistant_text,
      }
    )