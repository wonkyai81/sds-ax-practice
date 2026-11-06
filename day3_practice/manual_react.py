# manual_react.py - ReAct 루프를 while 루프로 직접 구현
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from pydantic import BaseModel

load_dotenv()
llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
)


def get_text(message):
    """ChatBedrockConverse는 content를 블록 리스트로 주기도 하므로 텍스트만 모아 반환합니다."""
    content = message.content
    if isinstance(content, list):
        return "".join(block.get("text", "") for block in content if isinstance(block, dict))
    return content


# ---------- 1) 도구 정의 ----------
@tool
def search_employee(name: str) -> str:
    """임직원 이름으로 소속 팀과 이메일을 조회합니다. 임직원 정보 질문에 사용하세요."""
    # 교육용 더미 데이터입니다. 실제 사내 데이터와 무관합니다.
    employees = {
        "김하늘": "김하늘 / 클라우드운영팀 / haneul.kim@samsungsds.example.com",
        "박도윤": "박도윤 / 물류플랫폼팀 / doyun.park@samsungsds.example.com",
    }
    return employees.get(name, f"'{name}' 님을 찾을 수 없습니다.")

@tool
def calculate(expression: str) -> str:
    """수식 문자열을 계산해 정확한 결과를 반환합니다. 예: '34 * 27', '(15 - 5) / 2'"""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"계산 실패: {e}"


tools = [search_employee, calculate]
tools_by_name = {t.name: t for t in tools}   # 이름으로 도구를 찾기 위한 사전

# ---------- 2) 도구 목록을 모델에 알려주기 ----------
llm_with_tools = llm.bind_tools(tools)

# ---------- 3) 대화 기록 초기화 ----------
messages = [
    SystemMessage(content="너는 삼성SDS 사내 어시스턴트야. 필요하면 도구를 사용해."),
    HumanMessage(content="김하늘 님과 박도윤 님이 각각 어느 팀 소속인지 알려주고, 34 곱하기 27도 계산해줘. 도구의 선택 근거도 알려줘"),
]

# ---------- 4) ReAct 루프: 도구 선택 -> 실행 -> 결과 관찰 -> 재판단 ----------
MAX_TURNS = 10                                     # 안전장치
turn = 0
while turn < MAX_TURNS:
    turn += 1
    ai_message = llm_with_tools.invoke(messages)   # (추론) 모델이 도구 필요 여부를 판단
    messages.append(ai_message)                    # 응답을 기록에 추가

    if not ai_message.tool_calls:                  # 도구 요청이 없으면 최종 답변
        print(f"\n[최종 답변] {get_text(ai_message)}")
        break

    for tool_call in ai_message.tool_calls:        # (행동) 요청된 도구를 전부 실행
        print(f"tool call = {tool_call}")
        tool_fn = tools_by_name[tool_call["name"]]
        result = tool_fn.invoke(tool_call["args"])
        print(f"tool call (Result) = {result}")
        print(f"[턴 {turn}] {tool_call['name']}({tool_call['args']}) -> {result}")
        messages.append(                           # (관찰) 결과를 기록에 추가
            ToolMessage(content=str(result), tool_call_id=tool_call["id"])
        )
    # while 처음으로 돌아감 -> 모델이 도구 결과를 보고 다시 판단 (재판단)
else:
    print("\n[중단] 최대 턴 수를 초과했습니다.")