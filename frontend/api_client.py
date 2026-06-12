import os
from typing import Any
import httpx
from dotenv import load_dotenv
from collections.abc import Iterator
from dataclasses import dataclass
import json

load_dotenv()

@dataclass(frozen=True)
class ChatStreamEvent:
  """프론트 화면이 이해하는 채팅 스트림 이벤트"""
  event_type: str
  text: str

def get_backend_url() -> str:
  """FastAPI 백엔드 기본 주소를 반환"""
  return os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

def call_chat_api(message: str) -> Any:
  """백엔드 /chat 엔드포인드에 일반 POST 요청을 보내고 JSON응답을 반환"""
  backend_url = get_backend_url()
  with httpx.Client(base_url=backend_url, timeout=10.0) as client:
    response = client.post("/chat", json={"message": message})
    # 2xx, 3xx : 정상처리, 4xx : 주소가 없음, 5xx : 서버 프로그램 오류
    # HTTPStatusError 입셉션 발생
    response.raise_for_status()
    
    return response.json()["answer"]

def parse_sse_line(line: str) -> ChatStreamEvent | None:
  """SSE data 라인을 token/status/done 이벤트로 변환"""
  # SSE의 빈 줄/주석/비 data 라인은 건너뜁니다.
  if not line or not line.startswith("data:"):
    return None
  
  # 마지막 줄
  raw_payload = line[len("data:") :].strip()
  if raw_payload == "[DONE]":
    return ChatStreamEvent(event_type="done", text="")
  
  # token 처리
  try:
    payload = json.loads(raw_payload)
  except json.JSONDecodeError:
    return ChatStreamEvent(event_type="status", text="수신된 스트림 데이터를 해석하지 못했습니다.")

  if not isinstance(payload, dict):
    return ChatStreamEvent(event_type="status", text="알 수 없는 스트림 형식입니다.")

  payload_type = payload.get("type", "status")
  if payload_type == "token":
    return ChatStreamEvent(event_type="token", text=payload.get("delta", ""))
  
  # status 처리
  return ChatStreamEvent(event_type="status", text=payload.get("label", "상태를 갱신했습니다."))



def stream_chat(message: str, mode: str = "멀티에이전트") -> Iterator[ChatStreamEvent]:
  """스트리밍 응답을 줄 단위로 일고 토큰을 하나씩 내보낸다. (SSE)
  FastAPI SSE endpoint를 호출하고 화면용 이벤트를 순서대로 반환
  """
  endpoint = "/agents/stream" if mode == "멀티에이전트" else "/chat/stream"
  url = f"{get_backend_url()}{endpoint}" # http://localhost:8000/ + endpoint => http://localhost:8000/agents/stream

  payload = {"message": message}
  try:
    with httpx.stream(
      "POST",
      url,
      json=payload,
      timeout=60.0
      ) as response:
      response.raise_for_status()
      # SSE 응답은 줄 단위로 흘러오므로 iter_lines()로 반복합니다.
      for line in response.iter_lines():
        print(repr(line)) 
        event = parse_sse_line(line)
        if event is None:
          continue
        yield event
        if event.event_type == "done":
          break
  except httpx.ConnectError as exc:
    # 백엔드 서버가 꺼졌거나 포트가 다를때.
    raise RuntimeError("백엔드 실행 여부와 8000번 포트를 확인하세요.") from exc
  except httpx.HTTPStatusError as exc:
    # 404 는 path (url) 오타, 500은  백엔드 내부 오류 가능성
    status_code = exc.response.status_code
    raise RuntimeError(f"HTTP 상태 코드를 확인하세요: {status_code}") from exc
  except httpx.ReadTimeout as exc:
    # SSE 라인이 오래 오지 않거나 종료 신호가 누락.
    raise RuntimeError("SSE라인 수진이 지연되었습니다. [DONE]처리와 백엔드 yield확인!") from exc


if __name__ == "__main__":
  sample_lines = [
    'data: {"type": "status", "label": "담당 전환: refund_agent"}',
    'data: {"type": "token", "delta": "환불 요청을 "}',
    'data: [DONE]'
  ]
  
  for sample_line in sample_lines:
    print(parse_sse_line(sample_line))
