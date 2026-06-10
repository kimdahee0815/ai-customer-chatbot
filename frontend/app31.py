import streamlit as st

from api_client import call_chat_api

st.title("고객 상담 챗봇")
message = st.chat_input("상담 메시지를 입력하세요.")

if message:
    with st.chat_message("user"):
        st.write(message)
        
    with st.chat_message("assistant"):
        try:
            data = call_chat_api(message)
        except Exception as exc:
            st.error(f"백엔드 호출에 실패: {exc}")
        else:
            st.write(data.get("message", data))