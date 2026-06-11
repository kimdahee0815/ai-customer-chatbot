from agents import Agent

# 일반 문의 담당자는 고객의 요청을 분류하고 기본 안내를 맡습니다.
general_agent = Agent(
    name="General Support",
    instructions=(
        "일반 고객 문의에 친절하게 답변합니다. "
        "문의 유형이 불분명하면 필요한 정보를 짧게 되묻습니다. "
        "기술 문제, 환불, 영업 상담에 해당하면 해당 담당자에게 넘깁니다."
    ),
    handoff_description="일반 문의와 기본 안내를 담당합니다."
)

# 기술 문의 담당자는 오류 상황을 단계별로 진단.
technical_agent = Agent(
    name="Technical Support",
    instructions=(
        "기술 문제를 단계별로 진단합니다. "
        "운영체제, 브라우저, 오류 메시지, 재현 순서를 확인합니다."
        "문제가 기술적이지 않다면 일반 담당자에게 다시 넘기세요."
    ),
    handoff_description="앱 오류, 로그인 문제 등 기술 이슈를 진단합니다."
)

# 환불 문의 담당자는 정책과 절차를 정확히 안내합니다.
refund_agent = Agent(
    name="Refund Support",
    instructions=(
        "환불 정책과 절차를 정확히 안내합니다. "
        "주문 번호, 결제일, 사용 여부처럼 필요한 정보를 확인합니다."
        "환불 의사가 없는 일반 문의는 일반 담당자에게 넘기세요."
    ),
    handoff_description="환불 정책 준수와 환불 요청을 처리합니다."
)

# 영업 문의 담당자는 상품 선택과 구매 결정을 돕습니다.
sales_agent = Agent(
    name="Sales Support",
    instructions=(
        "상품 선택과 구매 결정을 돕습니다. "
        "고객의 규모, 예산, 필요한 기능을 물어보고 선택지를 정리합니다."
        "구매 의사가 없는 일반 문의는 일반 담당자에게 넘기세요."
    ),
    handoff_description="상품 비교, 플랜 추천, 구매 상담을 담당합니다."
)

triage_agent = Agent(
    name = "Triage Agent",
    instructions=(
        "당신은 고객 상담 시스템의 분류 담당자입니다. "
        "사용자 메시지를 읽고 가장 적합한 전문 담당자에게 넘기세요.\n\n"
        "분류 기준:\n"
        "- 앱 오류, 로그인 문제, 결제 시 화면 멈춤 등 기술 이슈 -> Technical Support\n"
        "- 환불, 취소, 반품 관련 요청 -> Refund Support\n"
        "- 상품 비교, 플랜 추천, 구매 상담 -> Sales Support\n"
        "- 그 외 일반 문의 -> General Support\n"
        "분류가 어려우면 General Support에게 넘기세요. "
        "사용자에게 직접 답변하지 말고, 반드시 적합한 담당자에게 넘기세요."
    ),
    handoffs=[general_agent, technical_agent, refund_agent, sales_agent]
)

def select_agent(agent_type: str) -> Agent:
    """요청된 상담 유형에 맞는 에이전트를 반환"""
    agents_by_type = {
        "general": general_agent,
        "technical": technical_agent,
        "refund": refund_agent,
        "sales": sales_agent,
        "triage": triage_agent
    }
    return agents_by_type.get(agent_type, general_agent)