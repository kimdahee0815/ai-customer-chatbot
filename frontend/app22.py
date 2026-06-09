import streamlit as st

ROLE_PRESETS={
    "일반 문의":{
        "summary":"문의 목적을 확인하고 적절한 안내를 제공합니다.",
        "greeting":"안녕하세요, 어떤 문의를 도와드릴까요?"
    },
    "기술 문의":{
        "summary":"증상과 재현 조건을 확인하고 해결 단계를 안내합니다.",
        "greeting":"안녕하세요. 어떤 오류나 증상을 겪고 계신가요?"
    },
    "환불/교환":{
        "summary":"주문 상태와 정책 조건을 확인해 절차를 안내합니다.",
        "greeting":"안녕하세요, 환불 또는 교환 관련 정보를 함께 확인해 보겠습니다."
    }
}

st.title("고객 상담 채팅 UI")
selected_role = st.selectbox("상담 역할", options=list(ROLE_PRESETS.keys()))
selected_preset = ROLE_PRESETS[selected_role]

st.sidebar.write("역할 요약")
st.sidebar.info(selected_preset["summary"])
# st.sidebar.warning
# st.sidebar.error

if "selected_role" not in st.session_state:
    st.session_state.selected_role = selected_role
    
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": selected_preset
        }
    ]

if selected_role != st.session_state.selected_role:
    st.session_state.selected_role = selected_role
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": selected_preset["greeting"]
        }
    ]
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
prompt = st.chat_input("문의 내용을 입력해 주세요.")

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    # 임의 처리
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content": f"{selected_role} 기준으로 문의를 확인했습니다."
        }
    )
    st.rerun()