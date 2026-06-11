import httpx
import streamlit as st
from api_client import get_backend_url

API_BASE_URL = get_backend_url()
ANALYSIS_OPTIONS={
    "요약":"summary",
    "키워드 추출":"keywords",
    "감정 분석":"setiment",
    "영어 번역":"translate_en"
}

def analyze_file_content(content: str, analysis_type: str)->dict[str, str]:
    """FastAPI 파일 분석 라우터에 텍스트와 분석 유형을 적는다"""
    response = httpx.post(
        f"{API_BASE_URL}/files/analyze",
        json={"content":content, "analysis_type":analysis_type},
        timeout=30.0
    )
    response.raise_for_status()
    return response.json()


st.title("문서 분석")
st.caption("적은 텍스트 파일을 업로드하고 분석 유형을 선택하세요.")

upload_file = st.file_uploader(
    "분석할 텍스트 파일",
    type=["txt", "text"],
    help="이번 화면에서는 utf-8 텍스트 파일만 사용."
)

selected_label = st.selectbox("분석 유형", list(ANALYSIS_OPTIONS))
selected_type = ANALYSIS_OPTIONS[selected_label]

if upload_file is not None:
    st.write(f"선택한 파일: {upload_file.name}")
    try:
        file_text = upload_file.read().decode("utf-8")
    except UnicodeDecodeError:
        st.error("utf-8로 읽을 수 없는 파일입니다. 작은 .txt 파일로 다시 시도하세요.")
    else:
        if not file_text.strip():
            st.warning("파일 내용이 비어 있습니다.")
        else:
            st.text_area("읽은 텍스트 미리보기", file_text, height=180)
            if st.button("분석 요청"):
                try:
                    result = analyze_file_content(file_text, selected_type)
                except httpx.ConnectError:
                    st.error("백엔드 서버에 연결할 수 없습니다.")
                except httpx.HTTPStatusError as exc:
                    st.error(f"분석 요청이 실패했습니다. {exc.response.text}")
                except httpx.TimeoutException:
                    st.error("분석 요청 시간이 초과되었습니다...")
                else:
                    st.subheader("분석 결과")
                    st.write(result["result"])
                    st.caption(f"처리 유형: {result['analysis_type']}")