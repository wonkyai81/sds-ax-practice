# trace.py - messages 리스트를 순회하며 실행 과정을 표 형태로 출력
import json
from langchain_core.messages import HumanMessage
from toolnode_parallel import graph   # 지난 실습부분에서 사용한 그래프를 그대로 사용


def get_text(message):
    """ChatBedrockConverse는 content를 블록 리스트로 주기도 하므로 텍스트만 모아 반환합니다."""
    content = message.content
    if isinstance(content, list):
        return "".join(block.get("text", "") for block in content if isinstance(block, dict))
    return content


def print_trace(result: dict):
    """messages 리스트를 순회하며 실행 과정을 표 형태로 출력."""
    print(f"{'순서':<4} {'타입':<10} {'내용'}")
    print("-" * 70)
    for i, m in enumerate(result["messages"]):
        if m.type == "human":
            print(f"{i:<4} {'사용자':<10} {get_text(m)}")
        elif m.type == "ai" and getattr(m, "tool_calls", None):
            for tc in m.tool_calls:
                print(f"{i:<4} {'도구요청':<10} {tc['name']} args={json.dumps(tc['args'], ensure_ascii=False)}")
        elif m.type == "tool":
            print(f"{i:<4} {'도구결과':<10} [{m.name}] {get_text(m)[:60]}")
        elif m.type == "ai":
            print(f"{i:<4} {'최종답변':<10} {get_text(m)[:60]}")


if __name__ == "__main__":
    result = graph.stream({"messages": [HumanMessage(content="서울 온도를 100으로 나눈 값은?")]})
    print_trace(result)