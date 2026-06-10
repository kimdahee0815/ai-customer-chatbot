from typing import AsyncIterator
from typing import Literal

from agents import Agent
from agents import Runner

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/agents", tags=["agents"])

class AgentStreamRequest(BaseModel):
    """Agents SDK 스트림 라우터가 받을 요청 내용"""
    message: str
    agent_type: Literal["general", "technical", "refund", "sales"] = "general"
    
# 일반 문의 담당자는 고객의 요청을 분류하고 기본 안내를 맡습니다.
general_agent = Agent(
    name="General Support",
    instructions=(
        "일반 고객 문의에 친절하게 답변합니다. "
        "문의 유형이 불분명하면 필요한 정보를 짧게 되묻습니다."
    )
)

# 기술 문의 담당자는 오류 상황을 단계별로 진단.
technical_agent = Agent(
    name="Technical Support",
    instructions=(
        "기술 문제를 단계별로 진단합니다. "
        "운영체제, 브라우저, 오류 메시지, 재현 순서를 확인합니다."
    )
)

# 환불 문의 담당자는 정책과 절차를 정확히 안내합니다.
refund_agent = Agent(
    name="Refund Support",
    instructions=(
        "환불 정책과 절차를 정확히 안내합니다. "
        "주문 번호, 결제일, 사용 여부처럼 필요한 정보를 확인합니다."
    )
)

# 영업 문의 담당자는 상품 선택과 구매 결정을 돕습니다.
sales_agent = Agent(
    name="Sales Support",
    instructions=(
        "상품 선택과 구매 결정을 돕습니다. "
        "고객의 규모, 예산, 필요한 기능을 물어보고 선택지를 정리합니다."
    )
)

def select_agent(agent_type: str) -> Agent:
    """요청된 상담 유형에 맞는 에이전트를 반환"""
    agents_by_type = {
        "general": general_agent,
        "technical": technical_agent,
        "refund": refund_agent,
        "sales": sales_agent
    }
    return agents_by_type.get(agent_type, general_agent)

def extract_txt_delta(event: object) -> str|None:
    """스트림 이벤트에서 화면으로 보낼 텍스트 조각만 꺼내온다"""
    delta = getattr(event, "delta", None)
    if isinstance(delta, str) and delta:
        return delta
    data = getattr(event, "data", None)
    data_delta = getattr(data, "delta", None)
    if isinstance(data_delta, str) and data_delta:
        return data_delta
    return None

async def stream_agent_events(request: AgentStreamRequest )->AsyncIterator[str]:
    """선택된 에이전트의 실행 결과를 SSE data 라인으로 변환"""
    selected_agent = select_agent(request.agent_type)
    result = Runner.run_streamed(selected_agent, input=request.message)
    async for event in result.stream_events():
        text_delta = extract_txt_delta(event)
        if text_delta:
            yield f"data: {text_delta}\n\n"
            
    yield "data: [DONE]"
    
@router.post("/stream")
async def stream_agent_response(request: AgentStreamRequest) -> StreamingResponse:
    """Agents SDK 실행 결과를 프론트엔드가 읽을 수 있는 SSE 응답으로 보낸다."""
    return StreamingResponse(
        stream_agent_events(request),
        media_type="text/event-stream"
    )