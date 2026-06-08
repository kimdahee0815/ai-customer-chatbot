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
    
st.title("상태가 유지되는 카운터")

initialize_counter()

st.write("현재 카운터 값: ", st.session_state.counter)

if st.button("1 증가"):
    increase_counter()
    
if st.button("초기화"):
    reset_counter()
    
st.write("Rerun 이후에도 유지되는 카운터 값 확인")