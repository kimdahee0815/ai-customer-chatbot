import time
import streamlit as st 

def fake_openai_stream(user_text:str):
    """OpenAI stream 처럼 텍스트 조각을 하나씩 내보낸다."""
    chunks=[
        "문의 내용을 확인했습니다.",
        f"{user_text} 에 대해",
        "상담 유형을 먼저 분류하고, ",
        "바로 실행할 수 있는 다음 조치를 안내하겠습니다."
    ]
    for chunk in chunks:
        time.sleep(0.2)
        yield chunk
        
st.title("고객 상담 챗봇 - stream 반환값 관찰")
if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
prompt = st.chat_input("고객 문의르 입력하세요")

if prompt:
    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })
    with st.chat_message("user"):
        st.write(prompt)
        
    with st.chat_message("assistant"):
        response_text = st.write_stream(fake_openai_stream(prompt))
        
    st.session_state.messages.append({
        "role":"assistant",
        "content": response_text
    })
    
    st.caption(f"저장된 메시지 수 {len(st.session_state.messages)}")