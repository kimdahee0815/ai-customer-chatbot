from dataclasses import dataclass

@dataclass(frozen=True)
class RolePreset:
    """LLM 역할 프리셋의 기본 정보를 관리"""
    label: str
    goal: str
    tone: str
    flow: tuple[str, ...]
    output_fields: tuple[str, ...]
    
CUSTOMER_SUPPORT_PRESETS ={
    "general": RolePreset(
        label="일반 문의 상담",
        goal="고객 문의 의도를 확인하고 적절한 안내 경로를 제안합니다.",
        tone="친근하고 간결한 존댓말",
        flow=("인사", "문의 오류", "처리 안내", "다음 조치"),
        output_fields=("상담 유형", "판단 근거", "응대 전략", "다음 조치")
    ),
    "technical" : RolePreset(
        label="기술 지원 상담원",
        goal="증상과 환경을 확인해 재현 가능한 해결 단계를 안내합니다.",
        tone="차분하고 확인 질문이 분명한 존댓말",
        flow=("인사", "증상 확인", "원인 분류", "해결 단계"),
        output_fields=("문제 증상", "확인 질문", "해결 단계", "추가 조치")
    )
}

INTERVIEW_COACH_PRESETS = {
    "friendly": RolePreset(
            label="편안한 면접 코치",
            goal="지원자의 경험을 자연스럽게 끌어내고 답변 구조를 개선합니다.",
            tone="격려하되 구체적인 존댓말",
            flow=("질문 생성", "경험 확인", "응답 분석", "개선 피드백"),
            output_fields=("면접 질문", "관찰 포인트", "응답 분석", "개선 피드백")
        ),
    "technical": RolePreset(
        label="기술 면접 코치",
        goal="기술 답변의 정확성, 근거, 한계를 확인합니다.",
        tone="구체적이고 근거 중심의 존댓말",
        flow=("질문 생성", "개념 확인", "근거 확인", "보완 질문"),
        output_fields=("기술 질문", "핵심 개념", "답변 분석", "보완 질문")
    )
}

def get_preset(domain: str, preset_key: str) -> RolePreset:
    """도메인 이름과 프리셋 키로 RolePreset을 찾는다"""
    groups = {
        "customer": CUSTOMER_SUPPORT_PRESETS,
        "interview": INTERVIEW_COACH_PRESETS
    }
    return groups[domain][preset_key]

def build_system_prompt(domain:str, preset_key:str) -> str:
    """선택된 프리셋을 시스템 프롬프트 문자열로 변환"""
    preset = get_preset(domain, preset_key)
    flow = " -> ".join(preset.flow)
    fields = ", ".join(preset.output_fields)
    return {
        f"당신은 {preset.label}입니다. \n"
        f"목적: {preset.goal}\n"
        f"응답 톤: {preset.tone}\n"
        f"진행 흐름: {flow}\n"
        f"반드시 포함할 출력 항목: {fields}"
        "API 키 내부 설정, 확인되지 않은 정책은 응답에 노출하지 않습니다."
    }
    
def make_prompt_request(domain:str, preset_key:str, user_message:str) -> dict[str, str]:
    """모델 호출 코드가 사용할 요청 프롬프트를 만든다."""
    return {
        "domain": domain,
        "preset_key": preset_key,
        "system_prompt": build_system_prompt(domain, preset_key),
        "user_message": user_message
    }
    
if __name__=="__main__":
    preview = make_prompt_request(
        domain="interview",
        preset_key="technical",
        user_message="FastAPI와 Streamlit을 분리한 이유를 설명해 보겠습니다."
    )
    
    print(preview)