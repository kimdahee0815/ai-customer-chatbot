import json
from datetime import datetime
from typing import Any

import streamlit as st 

def get_messages() -> list[dict[str, Any]]:
    """세션 산태에서 대화 기록을 꺼냅니다."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    return st.session_state.messages

def message_to_markdown(message: dict[str,Any])-> str:
    """대화 메시지 한 건을 마크다운 문단으로 변환"""
    role = str(message.get("role", "unknown"))
    content = str(message.get("content", "")).strip()
    tool_calls = message.get("tool_calls", [])
    
    lines = [f"### {role}", "", content or "(내용 없음)"]
    if tool_calls:
        lines.append("")
        lines.append("도구 호출: ")
        for index, tool_call in enumerate(tool_calls, start=1):
            lines.append(f"- {index}. '{tool_call}'")
    return "\n".join(lines)

def export_messages_markdown(messages: list[dict[str, Any]])-> str:
    """대화 목록을 사람이 읽기 쉬운 마크다운 리포트로 변환"""
    exported_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    blocks = [
        "# 고객 상담 대화 내역",
        "",
        f"- 내보낸 시각: {exported_at}",
        f"- 메시지 수: {len(messages)}"
    ]
    
    if not messages:
        blocks.append("아직 저장할 대화가 없습니다.")
        return "\n".join(blocks)
    
    for message in messages:
        blocks.append(message_to_markdown(message))
        blocks.append("")
        
    return "\n".join(blocks).strip() + "\n"

def export_messages_json(messages: list[dict[str, Any]]) -> str:
    """대화 목록을 JSON 문자열로 변환"""
    payload = {
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "message_count": len(messages),
        "messages": messages
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)

def calculate_message_stats(messages: list[dict[str, Any]]) -> dict[str, float | int]:
    """대화 기록에서 대시보드 지표를 계산"""
    total_count = len(messages)
    user_count = sum(1 for message in messages if message.get("role") == "user")
    assistant_count = sum(1 for message in messages if message.get("role") == "assistant")

    assistant_length = [
        len(str(message.get("content", "")))
        for message in messages
        if message.get("role") == "assistant"
    ]
    if assistant_length:
        average_response_length = sum(assistant_length) / len(assistant_length)
    else:
        average_response_length = 0.0
        
    if total_count:
        assistant_ratio = assistant_count / total_count
    else:
        assistant_ratio = 0.0
        
    safe_progress = min(max(assistant_ratio, 0.0),1.0)
    
    return {
        "total_count": total_count,
        "user_count": user_count,
        "assistant_count": assistant_count,
        "average_response_length": average_response_length,
        "assistant_ratio": safe_progress
    }

st.title("대시보드")

messages = get_messages()
markdwon_report = export_messages_markdown(messages)
json_report = export_messages_json(messages)

st.subheader("대화 내보내기")
st.caption("API 키와 secrets 값은 리포트에 포함하지 않습니다.")

st.download_button(
    label="마크다운으로 다운로드",
    data=markdwon_report,
    file_name="chat_history.md",
    mime="text/markdown",
    disabled=not messages 
)

st.download_button(
    label="JSON으로 다운로드",
    data=json_report,
    file_name="chat_history.json",
    mime="application/json",
    disabled=not messages 
)

st.subheader("대화 통계")
st.caption("API 키와 secrets 값은 리포트에 포함하지 않습니다.")
messages = get_messages()
stats = calculate_message_stats(messages)

left, middle, right = st.columns(3)

left.metric("총 메시지", int(stats["total_count"]))
middle.metric("사용자 메시지", int(stats["user_count"]))
right.metric("평균 AI 응답 길이", f"{stats['average_response_length']:.0f}자")

chart_data = {
    "사용자": [int(stats["user_count"])],
    "AI": [int(stats["assistant_count"])]
}

st.bar_chart(chart_data)
# st.line_chart
# st.histogram

st.write("AI 메시지 비율")
st.progress(float(stats["assistant_ratio"]))

if not messages:
    st.info("대화가 쌓이면 다운로드 버튼을 사용할 수 있습니다.")