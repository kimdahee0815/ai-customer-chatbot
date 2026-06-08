import streamlit as st

def main() -> None:
    """상담 챗봇 설정값을 사이드바와 본문 레이아웃으로 나눠 보여준다."""
    st.set_page_config(page_title="상담 설정")
    st.title("AI 고객 상담 챗봇")
    
    with st.sidebar:
        st.header("상담 설정")
        inquiry_type = st.selectbox("상담유형:", ["일반 문의", "기술 지원","환불/교환","영업"])
        model_name = st.selectbox("모델", ["gpt-4.1-mini", "gpt-4.1"])
        urgency = st.slider("긴급도", 1, 5, 3)
        
if __name__ == "__main__":
    main()