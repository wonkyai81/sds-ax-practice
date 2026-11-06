# mcp_agent.py - MCP 서버 + 일반 도구를 함께 쓰는 LangGraph 통합 Agent
import asyncio
import os
import sys
import tempfile
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()


def get_text(message):
    """ChatBedrockConverse는 content를 블록 리스트로 주기도 하므로 텍스트만 모아 반환합니다."""
    content = message.content
    if isinstance(content, list):
        return "".join(block.get("text", "") for block in content if isinstance(block, dict))
    return content


SERVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server.py")

SYSTEM_PROMPT = """당신은 삼성SDS 사내 어시스턴트입니다. 교육용 더미 데이터를 조회해 답합니다.

[도구 사용 규칙]
- 임직원 개인 정보 -> search_employee
- 팀 인원수, 팀 명단 -> list_team_members
- 자산 현황 -> get_asset
- 프로젝트 현황 -> list_projects
- 수치 계산 -> calculator (암산하지 말고 반드시 도구 사용)
- 현재 주가 -> 주가 조회 도구 (get_history를 쓰면 period="5d", interval="1d"로 최근 값만 조회)
- 역사적 최고가/장기 추이 -> get_history를 period="max", interval="3mo"로 호출 (일봉 전체는 데이터가 너무 커서 금지)

도구에서 에러 메시지가 오면 그 지침을 따라 수정해서 다시 시도하세요.
도구 결과에 근거해서만 답하세요."""


# MCP 도구와 섞어 쓸 일반 도구
@tool
def calculator(expression: str) -> str:
    """수학 계산을 정확하게 수행한다. 예: '3 * 2000000'"""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"에러: 계산식이 잘못되었습니다 ({e}). 올바른 수식으로 다시 호출하세요."

EXTERNAL = {
    "command": sys.executable,
    "args": ["-m", "openmarkets"],
    "transport": "stdio",
    # openmarkets는 실행 폴더의 .env를 읽고 모르는 키(AWS 등)가 있으면 죽으므로, .env 없는 폴더에서 실행
    "cwd": tempfile.gettempdir(),
}

async def main():
    # 1) MCP 클라이언트 설정: 서버 이름 -> 실행 방법
    client = MultiServerMCPClient({
        "sds-company-data": {
            "command": sys.executable,
            "args": [SERVER_PATH],
            "transport": "stdio",
        },
        "yfinance":EXTERNAL
        # 서버를 더 붙이고 싶으면 여기에 항목 추가

    })

    # 2) MCP 도구를 LangChain Tool로 변환해 가져오기 (await 필수)
    mcp_tools = await client.get_tools()
    print(f"MCP 도구 {len(mcp_tools)}개: {[t.name for t in mcp_tools]}")

    # 3) 일반 도구와 합치기: 여기부터는 MCP 여부 구분이 사라집니다
    tools = mcp_tools + [calculator]

    # 4) 2-2에서 손으로 조립한 ReAct 구조를 한 줄로
    llm = ChatBedrockConverse(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        region_name="us-east-1",
    )
    agent = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT)

    # 5) 단일 도구 질문과 복합 질문을 섞어 검증
    queries = [
        # 단일 MCP 도구
        "구글, 애플 현재 주가 알려줘", 
        "삼성전자 역사적 최고가 얼마인지 알려줘"
    ]

    for q in queries:
        print(f"\n{'=' * 60}\n질문: {q}\n{'=' * 60}")
        async for event in agent.astream(
            {"messages": [("user", q)]},
            stream_mode="updates",
        ):
            for node, update in event.items():
                for m in update.get("messages", []):
                    if getattr(m, "tool_calls", None):
                        for tc in m.tool_calls:
                            print(f"  도구 호출: {tc['name']}({tc['args']})")
                    elif m.type == "tool":
                        print(f"  도구 결과: [{m.name}] {get_text(m)[:80]}")
                    elif m.content:
                        print(f"  답변: {get_text(m)}")

    # 5) 실행: MCP 도구가 섞여 있으므로 비동기 호출(ainvoke) 사용
    # result = await agent.ainvoke(
    #     # {"messages": [("user", "김하늘 님이 무슨 자산을 갖고 있는지 알려주세요.")]}
    #     {"messages": [("user", "노트북 자산이 총 몇 대인지 세고 한 대당 200만원이면 총액은? (호출된 tool을 순서대로 목록으로 출력해줘)")]}
    # )
    # print(f"\n답변: {get_text(result['messages'][-1])}")


if __name__ == "__main__":
    asyncio.run(main())