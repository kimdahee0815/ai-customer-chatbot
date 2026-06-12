import streamlit as st

st.title("전역 설정 확인")

ROLE_PRESETS = {
    "고객 상담": "당신은 친절한 고객 상담 도우미입니다. 사용자의 문제를 짧고 명확하게 정리해주세요.",
    "기술 지원":"당신은 기술 지원 담당자입니다. 재현 절차, 오류 메시지를 차례로 확인해주세요.",
    "영업":"당신은 영업 상담 담당자입니다. 고객의 필요를 확인하고 적절한 다음 행동을 제안해주세요."
}

# settings 키워드가 없을 때만 기본값을 만듬
if "settings" not in st.session_state:
    st.session_state.settings = {
        "model": "gpt-5.4-nano",
        "temperature": 0.7,
        "system_prompt": ROLE_PRESETS["고객 상담"],
        "role_preset": "고객 상담"
    }
    
settings = st.session_state.settings 

selected_role = st.selectbox("역할 프리셋", list(ROLE_PRESETS.keys()),
                            index=list(ROLE_PRESETS.keys()).index(settings.get("role_preset", "고객 상담")))

default_prompt = (
    ROLE_PRESETS[selected_role]
    if selected_role != settings.get("role_preset")
    else settings.get("system_prompt", ROLE_PRESETS[selected_role])
)

edited_prompt = st.text_area("시스템 프롬프트", value=default_prompt, height=160)

if st.button("프롬프트 설정 저장"):
    st.session_state.settings["role_preset"] = selected_role
    st.session_state.settings["system_prompt"] = edited_prompt
    st.success("프롬프트 설정을 저장했습니다.")
    
st.json(
    {
        "role_preset": st.session_state.settings["role_preset"],
        "system_prompt":st.session_state.settings["system_prompt"]
    }
)
st.write("현재 settings:",st.session_state.settings)