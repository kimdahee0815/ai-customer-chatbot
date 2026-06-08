import streamlit as st

def initialize_counter() -> None:
    """카운터 상태가 없으면 처음 값 0을 준비"""
    if "counter" not in st.session_state:
        st.session_state.counter = 0

def increase_counter() -> None:
    """저장된 카운터 값을 1증가"""
    st.session_state.counter = st.session_state.counter + 1
    
def reset_counter() -> None:
    """저장된 카운터 값을 0으로 되돌린다."""
    st.session_state.counter = 0
    
st.title("버튼 상호작용으로 상태 바꾸기")

initialize_counter()

st.write("현재 카운터 값: ", st.session_state.counter)

increase_clicked = st.button("1 증가")
reset_clicked = st.button("초기화")
    
# 증가 버튼이 눌린 상황에서는 저장된 값 1을 올린다.
if increase_clicked:
    increase_counter()
    st.success("카운터를 1 증가 했습니다.")

# 초기화 버튼이 눌린 실행에서는 저장된 값을 0으로 돌린다.
if reset_clicked:
    st.session_state.counter = 0
    st.success("카운터를 초기화 했습니다.")

st.write("Rerun 이후에도 유지되는 카운터 값 확인")