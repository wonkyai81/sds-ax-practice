# router_only.py - Supervisor의 핵심인 라우팅 결정만 분리해 관찰
from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_aws import ChatBedrockConverse

load_dotenv()

class Route(BaseModel):
    next_agent: Literal["data_agent", "research_agent", "general_agent", "FINISH"] = Field(
        description="다음에 호출할 Agent, 또는 작업 완료 시 FINISH"
    )
    reason: str = Field(description="선택 이유 한 줄")

llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    temperature=0,
)
router_llm = llm.with_structured_output(Route)

ROUTING_GUIDE = (
    "다음 질문을 처리할 Agent를 골라라.\n"
    "- data_agent: 임직원, 자산, 프로젝트 등 사내 시스템 데이터 조회\n"
    "- research_agent: 연차, 재택근무, 출장 등 사내 규정 문서 검색\n"
    "- general_agent: 인사말, 잡담, 범위 밖 질문 응대\n"
    "- FINISH: 이미 답변 가능\n\n질문: "
)

questions = [
    "클라우드운영팀 임직원 명단 알려줘",
    "연차는 며칠까지 쓸 수 있어?",
    "안녕하세요, 오늘 기분 어때요?",
]
for q in questions:
    decision = router_llm.invoke(ROUTING_GUIDE + q)
    print(f"{q}\n  -> {decision.next_agent} ({decision.reason})\n")