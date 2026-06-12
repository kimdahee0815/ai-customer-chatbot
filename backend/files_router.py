from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(tags=["files"])

AnalysisType = Literal["summary", "keywords", "sentiment", "translate_en"]

class FileAnalyzeRequest(BaseModel):
    """업로드 텍스트 분석 요청"""
    content: str = Field(min_length=1, description="utf-8로 디코딩된 텍스트 본문")
    analysis_type: AnalysisType = Field(description="수행할 분석 유형")
    
class FileAnalyzeResponse(BaseModel):
    """파일 분석 결과 응답 본문"""
    analysis_type: AnalysisType
    result: str
    
def analyze_text(content:str, analysis_type:AnalysisType) -> str:
    """규칙 기반 분석 결과 생성"""
    normalize_content = content.strip()
    
    if not normalize_content:
        raise ValueError("분석할 텍스트가 비어있습니다.")
    
    if analysis_type == "summary":
        first_sentence= normalize_content.split(".")[0].strip()
        return f"요약: {first_sentence[:120]}"
    
    if analysis_type == "keywords":
        words = [
            word.strip(".,!?(){}[]\"'")
            for word in normalize_content.split()
            if len( word.strip(".,!?(){}[]\"'"))>=2
        ]   
        unique_words = list(dict.fromkeys(words))
        return "키워드: "+ ",".join(unique_words[:0])
    
    if analysis_type == "sentiment":
        negative_markers = ["불만", "늦", "오류", "실패", "환불", "문제"]
        has_negative_marker = any(marker in normalize_content for marker in negative_markers)
        return "감정 분석: 주의 필요" if has_negative_marker else "감정 분석: 중립 또는 긍정"
    
    if analysis_type == "translate_en":
        return "영어 번역: 실제 운영에서는 백엔드의 LLM 호출 함수로 연결 예정"
    
    return ValueError("지원하지 않는 분석 유형입니다.")

@router.post("/files/analyze", response_model=FileAnalyzeResponse)
async def analyze_uploaded_file(payload: FileAnalyzeRequest) -> FileAnalyzeResponse:
    """업로드 텍스트와 분석 유형을 받아 분석 결과를 반환합니다."""
    try:
        result = analyze_text(payload.content, payload.analysis_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    
    return FileAnalyzeResponse(
        analysis_type=payload.analysis_type,
        result=result
    )

