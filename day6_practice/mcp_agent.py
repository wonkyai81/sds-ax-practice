# mcp_agent.py - 4일차 MCP 서버를 data_agent에 연결
import asyncio
import sys
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

load_dotenv()

def get_text(message):
    """ChatBedrockConverse는 content를 블록 리스트로 주기도 하므로 텍스트만 모아 반환합니다."""
    content = message.content
    if isinstance(content, list):
        return "".join(block.get("text", "") for block in content if isinstance(block, dict))
    return content

async def build_data_agent():
    # 4일차에서 만든 MCP 서버를 stdio 방식으로 기동하고 접속합니다
    client = MultiServerMCPClient(
        {
            "company": {
                "command": sys.executable,
                "args": ["mcp_server.py"],
                "transport": "stdio",
            }
        }
    )
    mcp_tools = await client.get_tools()
    print("MCP 도구 목록:", [t.name for t in mcp_tools])

    worker_llm = ChatBedrockConverse(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        region_name="us-east-1",
        temperature=0,
    )
    data_agent = create_agent(
        worker_llm,
        mcp_tools,                    # MCP 도구가 일반 도구처럼 들어갑니다
        system_prompt=(
            "너는 삼성SDS 사내 데이터 조회 전문가다. 임직원, 자산, 프로젝트 조회만 담당한다.\n"
            "반드시 도구로 조회한 결과에 근거해 답하고, 한 문단으로 정리해 보고하라.\n"
            "담당 범위 밖 질문에는 '담당 범위가 아닙니다'라고만 답하라."
        ),
        name="data_agent",
    )
    return data_agent

async def main():
    data_agent = await build_data_agent()
    result = await data_agent.ainvoke(
        {"messages": [HumanMessage("클라우드운영팀 GPU 서버 몇 대야?")]}
    )
    print(get_text(result["messages"][-1]))

if __name__ == "__main__":
    asyncio.run(main())