# lcel_debug.py - 중간 단계 입출력 추적
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()

def tap(label):
    """값을 출력하고 그대로 다음 단계로 통과시키는 관찰 지점을 만듭니다."""
    def _tap(value):
        print(f"\n=== [{label}] 타입: {type(value).__name__} ===")
        print(value)
        return value  # 반드시 그대로 반환해야 체인이 이어집니다
    return RunnableLambda(_tap)

prompt = PromptTemplate.from_template("{word}의 반대말 하나만 답해.")
llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    temperature=0,
)

# 각 단계 사이에 관찰 지점을 끼워 넣습니다.
chain = (
    tap("입력")
    | prompt
    | tap("프롬프트 완성 후")
    | llm
    | tap("모델 응답 후")
    | StrOutputParser()
)

result = chain.invoke({"word": "출근"})
print("\n최종 결과:", result)