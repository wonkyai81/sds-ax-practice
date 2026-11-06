# params.py - temperature와 max_tokens 비교
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse

load_dotenv()
MODEL = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"

prompt = "삼성SDS 사내 카페 이름 아이디어를 하나만 제안해줘."

# temperature 0: 결정적인 출력. 반복 호출해도 거의 같은 답
llm_t0 = ChatBedrockConverse(model=MODEL, region_name="us-east-1", temperature=0)
# temperature 1: 다양성 높은 출력. 호출마다 다른 답
llm_t1 = ChatBedrockConverse(model=MODEL, region_name="us-east-1", temperature=1)

print("--- temperature=0 (3회 호출) ---")
for _ in range(3):
    print(llm_t0.invoke(prompt).content)

print("--- temperature=1 (3회 호출) ---")
for _ in range(3):
    print(llm_t1.invoke(prompt).content)

# max_tokens: 출력 길이 제한. 너무 작으면 답이 잘립니다
llm_short = ChatBedrockConverse(model=MODEL, region_name="us-east-1", max_tokens=20)
result = llm_short.invoke("LangChain의 장점을 설명해줘.")
print("--- max_tokens=20 ---")
print(result.content)
print("종료 사유:", result.response_metadata.get("stopReason"))