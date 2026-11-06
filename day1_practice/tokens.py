# tokens.py - 응답의 토큰 사용량 확인
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse

load_dotenv()
llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
)

result = llm.invoke("LangChain을 한 문장으로 설명해줘.")

print("응답:", result.content)

# 사용량은 호출 방식에 따라 안 실려 올 수 있으므로 먼저 있는지 확인합니다
if result.usage_metadata:
    usage = result.usage_metadata
    print(f"입력 토큰: {usage['input_tokens']}")
    print(f"출력 토큰: {usage['output_tokens']}")
    print(f"전체 토큰: {usage['total_tokens']}")
else:
    print("이번 응답에는 토큰 사용량이 실려 오지 않았습니다.")