# mcp_verify.py - 파이썬 MCP 클라이언트로 서버를 직접 검증
import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server.py")


async def main():
    # 1) 서버를 자식 프로세스로 띄울 방법을 기술
    #    sys.executable: 현재 파이썬 인터프리터 경로 (python/python3 문제 회피)
    params = StdioServerParameters(command=sys.executable, args=[SERVER_PATH])

    # 2) stdio로 연결하고 세션 시작
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()   # MCP 초기 핸드셰이크

            # 3) 검증 1: 도구 목록 확인
            tools = await session.list_tools()
            print("=== 노출된 도구 목록 ===")
            for t in tools.tools:
                print(f"- {t.name}: {t.description.splitlines()[0]}")

            # 4) 검증 2: 도구 호출
            print("\n=== 도구 호출 검증 ===")
            r1 = await session.call_tool("search_employee", {"name": "김하늘"})
            print(f"search_employee -> {r1.content[0].text}")

            r2 = await session.call_tool("list_team_members", {"team": "클라우드운영팀"})
            print(f"list_team_members -> {r2.content[0].text[:80]}")

            r3 = await session.call_tool("get_asset", {"owner": "김하늘"})
            print(f"get_asset -> {r3.content[0].text}")

            r4 = await session.call_tool("list_projects", {"team": "물류플랫폼팀"})
            print(f"list_projects -> {r4.content[0].text}")

            # 5) 검증 3: 에러 케이스도 확인
            r5 = await session.call_tool("search_employee", {"name": "홍길동"})
            print(f"없는 직원 -> {r5.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())