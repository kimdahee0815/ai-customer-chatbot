import streamlit as st

st.set_page_config(page_title="AI 고객 상담 챗봇", page_icon="🗨️")

st.title("AI 고객 상담 챗봇")
st.caption("Streamlit 채팅 UI 골격: 메시지 목록, 출력 컨테이너, 입력창")

SUPPORT_REPLY_PREFIX={
    "일반 문의": "문의 목적을 확인했습니다.",
    "기술 지원":"기술 지원 관점에서 증상을 확인했습니다.",
    "환불/교환": "환불 또는 교환 상담 흐름으로 확인했습니다."
}

selected_category = st.selectbox("상담 유형", options=list(SUPPORT_REPLY_PREFIX.keys()))

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role":"assistant",
            "content": "안녕하세요, 상담 유형을 선택하고 문의 내용을 입력해주세요."
        }
    ]
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
            
prompt = st.chat_input("예: 배송이 늦어지고 있어요.")
    
if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
        
    reply = (
        f"{SUPPORT_REPLY_PREFIX[selected_category]}"
        "이번 단계에서는 실제 API 호출 없이 채팅 UI 저장 흐름만 확인"
    )
        
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )
    st.rerun()