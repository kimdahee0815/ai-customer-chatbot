import httpx
import streamlit as st

from api_client import get_backend_url

API_BASE_URL = get_backend_url()
ANALYSIS_OPTIONS = {
  "요약": "summary",
  "키워드 추출": "keywords",
  "감정 분석": "sentiment",
  "영어 번역": "translate_en"
}

def analyze_file_content(content: str, analysis_type: str) -> dict[str, str]:
  """FastAPI 파일 분석 라우터에 텍슽와 분석 유형을 전다"""
  response = httpx.post(
    f"{API_BASE_URL}/files/analyze",
    json={"content": content, "analysis_type": analysis_type},
    timeout=30.0
  )
  response.raise_for_status()
  return response.json()


st.title("문서 분석")
st.caption("작은 텍스트 파일을 업로드하고 분석 유형을 선택하세요.")

upload_file = st.file_uploader(
  "분석할 텍스트 파일",
  type=["txt", "text"],
  help="이번 홤녀에서는 utf-8 텍스트 파일만 사용."
)

selected_label = st.selectbox("분석 유형", list(ANALYSIS_OPTIONS))
selected_type = ANALYSIS_OPTIONS[selected_label]

if upload_file is not None:
  st.write(f"선택한 파일: {upload_file.name}")
  try:
    # 업로드 파일을 bytes로 읽은 뒤 utf-8 문자열로 변환.
    file_text = upload_file.read().decode("utf-8")
  except UnicodeDecodeError:
    st.error("utf-8로 읽을 수 없는 파일입니다. 작선 .txt파일로 다시 시도하세요.")
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
          st.error("분석 요청이 실패했습니다. {exc.response.text}")
        except httpx.TimeoutException:
          st.error("분석 요청 시간이 초과 되었습니다. ...")
        else:
          st.subheader("분석 결과")
          st.write(result["result"])
          st.caption(f"처리 유형: {result['analysis_type']}")

# from dataclasses import dataclass

# @dataclass
# class DemoUploadFile:
#   """Streamlit 업로드 객체의 핵심 동작"""
#   name: str
#   content: bytes

#   def read(self) -> bytes:
#     return self.content

# def decode_uploaded_text(upload_file: DemoUploadFile) -> str:
#   """업로드 파일을 분석 요청에 사용할 수 있는 문자열로 변환"""
#   raw_bytes = upload_file.read()
#   text = raw_bytes.decode("utf-8")
  
#   if not text.strip():
#     raise ValueError("파일 내용이 비어 있습니다.")
  
#   return text


# if __name__ == "__main__":
#   sample_file = DemoUploadFile(name="customer_note.txt", content="배송이 늦어서 고객이 재문의했습니다.".encode("utf-8"))
  
#   decoded_text = decode_uploaded_text(sample_file)
#   print("파일명: ", sample_file.name)
#   print("분석할 텍스트: ", decoded_text)
  
  