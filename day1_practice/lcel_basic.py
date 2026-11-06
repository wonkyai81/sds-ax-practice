# lcel_basic.py - 체인 구성과 invoke, stream, batch
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

prompt = PromptTemplate.from_template(
    "너는 삼성SDS 사내 커뮤니케이션 담당자야. {topic}에 대한 공지 문구를 두 문장으로 써줘."
)
llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
)
parser = StrOutputParser()

# 파이프 하나로 조립: dict -> 프롬프트 -> AIMessage -> str
chain = prompt | llm | parser

# 1) invoke: 단건 호출
print("[invoke]")
print(chain.invoke({"topic": "사내 시스템 정기 점검"}))
print("---")

# 2) stream: 토큰 단위 실시간 출력 (챗봇 UI의 타이핑 효과)
print("[stream] ", end="", flush=True)
for chunk in chain.stream({"topic": "보안 교육 일정"}):
    print(chunk, end="", flush=True)
print("\n---")

# 3) batch: 여러 입력을 한꺼번에 병렬 처리
inputs = [
    {"topic": "주차장 공사"},
    {"topic": "구내식당 메뉴 개편"},
    {"topic": "사원증 재발급 안내"},
]
results = chain.batch(inputs)
print("[batch]")
for i, r in zip(inputs, results):
    print(f"- {i['topic']}: {r[:30]}...")