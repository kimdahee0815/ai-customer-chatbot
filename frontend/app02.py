import streamlit as st

st.title("상태가 유지되는 카운터")

if "counter" not in st.session_state:
    st.session_state.counter = 0
    
st.write("현재 카운터 값", st.session_state.counter)

if st.button("1 증가"):
    st.session_state.counter += 1
    st.write("증가 버튼을 눌렀습니다.")

if st.button("초기화"):
    st.session_state.counter = 0
    st.write("카운터를 0으로 초기화")
    
st.write("Rerun 이후에도 유지되는 카운터 값 확인")

