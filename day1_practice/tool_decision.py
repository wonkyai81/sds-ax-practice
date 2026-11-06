# tool_decision.py - 모델의 도구 호출 "결정" 확인
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_aws import ChatBedrockConverse

load_dotenv()

@tool
def multiply(a: int, b: int) -> int:
    """두 정수 a와 b를 입력받아 곱을 반환한다. 정확한 산술 계산이 필요할 때 사용."""
    return a * b

@tool
def search_tool(name: str) -> str:
    """삼성SDS 임직원 디렉터리에서 이름으로 직원 정보를 조회한다."""
    # 교육용 더미 데이터입니다
    fake_db = {
        "김하늘": "김하늘 / 클라우드운영팀 / haneul.kim@samsungsds.example.com",
        "박도윤": "박도윤 / 물류플랫폼팀 / doyun.park@samsungsds.example.com",
    }
    return fake_db.get(name, f"{name}을(를) 찾을 수 없습니다.")

# bind_tools: 모델에게 "이런 도구들이 있다"고 알려줍니다
llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
)
llm_with_tools = llm.bind_tools([multiply, search_tool])

queries = [
    "1234567 곱하기 8901234 계산해줘.",              # 단일 도구
    "김하늘 찾아서 이메일 알려주고 15 곱하기 25도.",  # 복합 (도구 2개)
    "그냥 안녕이라고만 인사해줘.",                    # 도구 불필요
]

for q in queries:
    response = llm_with_tools.invoke(q)
    print(f"[질문] {q}")
    if response.tool_calls:  # 모델이 호출하기로 "결정"한 도구 목록 (아직 실행 전)
        for call in response.tool_calls:
            print(f"  -> 호출 결정: {call['name']}({call['args']})")
    else:
        print(f"  -> 직접 응답: {response.content}")
    print()