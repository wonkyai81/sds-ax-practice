# limits.py - LLM 한계 재현
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse

load_dotenv()
llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    temperature=0,
)

# 1) 환각: 존재하지 않는 사내 규정을 물으면 지어낼 수 있습니다
print(llm.invoke("삼성SDS 연차 이월 규정 제12조 3항 내용을 알려줘.").content)

# 2) 계산 취약: 큰 수 곱셈
print(llm.invoke("1234567 곱하기 8901234는? 숫자만 답해.").content)
print("실제 답:", 1234567 * 8901234)

# 3) 상태 망각: 두 번의 독립 호출은 서로를 모릅니다
llm.invoke("내 이름은 김하늘이야.")
print(llm.invoke("내 이름이 뭐였지?").content)