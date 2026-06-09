import streamlit as st

st.title("AI 고객 상담 챗봇")
st.caption("고객 상담 역할 프리셋을 붙이기 정의 최소 채팅 UI 구현")

# 앱이 처음 열렸을 때만 메시지 목록을 초기화합니다.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요? 무엇을 도와드릴까요?"
        }
    ]
    
# 저장된 메시지를 순서대로 다시 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        
# 사용자가 화면에서 입력차에 메시지를 입력
prompt = st.chat_input("문의 내용을 입력해 주세요")

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    # 여기에 실제 API 호출하는 로직이 있을 예정
    
    # 이번 세션에 실제 API 호출이 없음. 임의의 응답 처리
    reply = f"문의 내용을 확인했습니다.: {prompt}"
    st.session_state.messages.append(
        {
            "role":"assistant",
            "content": reply
        }
    )
    
    # 새 메시지가 지정된 뒤 화면을 다시 그려 전체 대화 기록을 보여 준다.
    st.rerun()
