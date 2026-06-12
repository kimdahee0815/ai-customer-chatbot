import json
from typing import AsyncIterator
from typing import Literal

from agents import Runner

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from pydantic import Field

from dotenv import load_dotenv
from backend.agents_config import select_agent


load_dotenv()

router = APIRouter(prefix="/agents", tags=["agents"])

class AgentStreamRequest(BaseModel):
    """Agents SDK 스트림 라우터가 받을 요청 내용"""
    message: str = Field(min_length=1)
    agent_type: Literal["triage", "general", "technical", "refund", "sales"] = "triage"


def extract_txt_delta(event: object) -> str | None:
    """스트림 이벤트에서 화면으로 보낼 텍스트 조각만 꺼내온다"""
    # Agents SDK 기준: 사용자에게 보여줄 텍스트는 raw_response_event의
    # response.output_text.delta 타입만 전달해야 합니다.
    if getattr(event, "type", None) != "raw_response_event":
        return None

    data = getattr(event, "data", None)
    if getattr(data, "type", None) != "response.output_text.delta":
        return None

    data_delta = getattr(data, "delta", None)
    if isinstance(data_delta, str) and data_delta:
        return data_delta
    return None


def sse_data(payload: dict[str, str]) -> str:
    """dict payload를 SSE data 이벤트 문자열로 변환"""
    body = json.dumps(payload, ensure_ascii=False)
    return f"data: {body}\n\n"

async def stream_agent_events(request: AgentStreamRequest) -> AsyncIterator[str]:
    """선택된 에이저트의 실행 결과를 SSE data라인으로 변환"""
    try:
        selected_agent = select_agent(request.agent_type)
        yield sse_data({"type": "status", "label": f"담당 에이전트: {selected_agent.name}"})
        result = Runner.run_streamed(selected_agent, input=request.message)
        async for event in result.stream_events():
            text_delta = extract_txt_delta(event)
            if text_delta:
                yield sse_data({"type": "token", "delta": text_delta})
    except Exception:
        yield sse_data({"type": "status", "label": "에이전트 처리 중 오류가 발생했습니다."})
    finally:
        yield "data: [DONE]\n\n"

@router.post("/stream")
async def stream_agent_response(request: AgentStreamRequest) -> StreamingResponse:
    """Agents SDK 실행 결과를 프론트엔드가 읽을 수 있는 SSE 응답으로 보낸다"""
    return StreamingResponse(
        stream_agent_events(request),
        media_type="text/event-stream",
        headers={
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no"
        }
    )