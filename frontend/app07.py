import os
import streamlit as st
from dotenv import load_dotenv

def get_openai_api_key() -> str | None:
    """환경변수와 Streamlit secrets에서 API 키이름을 기준으로 값을 찾습니다."""
    load_dotenv()
    env_key = os.getenv("OPENAI_API_KEY")
    streamlit_key = st.secrets.get("OPENAI_API_KEY")
    return env_key or streamlit_key

def main() -> None:
    """API 키 값을 출력하지 않고 설정 여부만 표시"""
    api_key = get_openai_api_key()
    
    st.markdown("'OPENAI_API_KEY' 설정 상태를 확인합니다.")
    
    if api_key:
        st.success("API 키가 코드 밖에서 설정되어 있습니다.")
    else:
        st.warning("API 키가 아직 설정되지 않았습니다.")
        
    st.info("실제 키 값은 화면에 출력하지 않습니다.")
    
if __name__ == "__main__":
    main()