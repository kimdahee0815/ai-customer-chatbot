import streamlit as st

def build_payload(
    customer_name: str,
    inquiry_type: str,
    urgency: int,
    message: str,
) -> dict[str, object]:
    """상담 화면 입력값을 요청 payload 형태로 정리"""
    return {
        "customer_name": customer_name.strip() or "익명 고객",
        "inquiry_type": inquiry_type,
        "urgency": urgency,
        "message": message.strip(),
        "message_length": len(message)
    }

def main() -> None:
    st.title("상담 입력 값 확인")
    customer_name = st.text_input("고객 이름", "홍길동")
    inquiry_type = st.selectbox("상담 유형", ["일반 문의", "기술 지원","환불/교환", "영업"])
    urgency = st.slider("긴급도", 1, 5, 3)
    message = st.text_area("문의 내용", "배송 상태를 알고 싶습니다.")
    
    payload = build_payload(customer_name, inquiry_type, urgency, message)
    
    st.markdown(
        f"**{payload['customer_name']}** 고객의"
        f"**{payload['inquiry_type']}** 상담 요청입니다."
    )
    st.metric("긴급도", payload['urgency'])
    st.write("백엔드로 보낼 수 있는 설정 구조")
    st.json(payload)
    
if __name__ == "__main__":
    main()