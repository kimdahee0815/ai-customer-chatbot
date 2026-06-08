import streamlit as st

st.title("Rerun 관찰용 카운터")

# 일반 변수는 파일이 다시 실행될 때마다 새로 만들어진다.
counter = 0

st.write("현재 카운터 값:", counter)
if st.button("1 증가"):
    counter += 1
    st.write("버튼 클릭 직후 값:",counter)

st.caption("버튼을 다시 누를 때 값이 누적이 되는지 확인.")
