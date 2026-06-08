import streamlit as st

def main():
    """고객 상담 챗봇의 기본 입력값을 화면에서 받습니다."""
    st.title("AI 고객 상담 챗봇 설정")
    st.caption("입력 위젯이 현재 화면의 상담 설정 값을 만듭니다")
    
    customer_name = st.text_input("고객 이름: ", placeholder="예: 홍길동")
    inquiry_type = st.selectbox("상담유형: ", ["일반문의", "기술지원", "환불/교환", "영업"])
    urgency = st.slider("긴급도", min_value=1, max_value=5, value=3)
    message = st.text_area("상담 메시지", placeholder="고객이 남긴 문의 내용을 입력합니다", height=120)
    uploaded_file = st.file_uploader("첨부 파일", type=["txt", "pdf", "png", "jpg"])
    
    st.divider()
    
    st.write("고객 이름: ", customer_name if customer_name else "아직 입력 없음")
    st.write("상담 유형: ", inquiry_type)
    st.write("긴급도: ", urgency)
    st.write("메시지 길이: ", len(message))
    
    if uploaded_file is None:
        st.info("첨부 파일은 아직 없습니다.")
    else:
        st.success(f"첨부 파일을 받았습니다.: {uploaded_file.name}")

if __name__ == "__main__":
    main()