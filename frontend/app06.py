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
        
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.subheader("고객 입력")
        customer_name = st.text_input("고객이름", "홍길동")
        message = st.text_area("문의 내용", "배송 상태를 알고 싶습니다")
        
    with right_column:
        st.subheader("현재 설정")
        st.metric("긴급도", urgency)
        st.write("상담 유형: ",inquiry_type)
        st.write("모  델:", model_name)
    
    summary_tab, raw_tab, settings_tab = st.tabs(["요약", "원문", "설정"])
    
    with summary_tab:
        st.markdown(f"**{customer_name}** 고객의 **{inquiry_type}** 상담입니다.")
    
    with raw_tab:
        st.write(message)
    
    with settings_tab:
        with st.expander("세부 설정 보기"):
            st.json(
                {
                    "inquiry_type":inquiry_type,
                    "model_name":model_name,
                    "urgency":urgency
                }
            )
        
if __name__ == "__main__":
    main()