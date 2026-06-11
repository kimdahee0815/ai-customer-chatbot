import streamlit as st 

st.title("고객 상담 챗봇")
st.caption("채팅 페이지는 화면 렌더링과 입력 처리만 담당합니다.")

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("상담 내용을 입력하세요.")

if prompt:
    st.session_state.messages.append(
        {"role":"user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)
        
    st.info("이 위치에서 백엔드 API 호출.")