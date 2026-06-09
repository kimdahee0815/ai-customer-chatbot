from pydantic import BaseModel
from pydantic import Field

class ChatRequest(BaseModel):
    """고객 상담 챗봇에 들어오는 한 번의 메시지 요청"""
    message: str = Field(min_length=1, description="고객 또는 상담원이 입력한 메시지 입니다.",
                        examples=["배송이 늦어지고 있어요. 현재 상태를 확인해 주세요."])
    customer_id: str | None = Field(default=None, description="고객을 구분하기 위한 선택 입력값입니다.",
                                    examples=["C-1001"])
    topic: str = Field(default="general", description="상담 주제입니다. 예: general, refund, delivery",
                    examples=["delivery"])

class ChatResponse(BaseModel):
    """FastAPI 백엔드가 프론트엔드로 돌려주는 응답."""
    reply: str = Field(description="프론트엔드가 화면에 표시할 상담 응답 문장입니다.",
                    examples=["배송 상태를 확인하는 절차를 안내해 드리겠습니다."]),
    status: str = Field(default="ok", description="요청 처리 상태입니다.", examples=["ok"])
