# why_langchain.py - 직접 호출 vs LangChain 비교
import boto3
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()
MODEL = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"
text = "LangChain is the future of AI development"

# --- A. SDK 직접 호출: provider 전용 형식 ---
client = boto3.client("bedrock-runtime", region_name="us-east-1")
resp = client.converse(
    modelId=MODEL,
    system=[{"text": "너는 짧고 간결한 번역가야."}],
    messages=[{"role": "user", "content": [{"text": f"{text}를 한국어로 번역해."}]}],
)
print("[SDK 직접]", resp["output"]["message"]["content"][0]["text"])

# --- B. LangChain: 표준 인터페이스 ---
messages = [
    SystemMessage(content="너는 짧고 간결한 번역가야."),
    HumanMessage(content=f"{text}를 한국어로 번역해."),
]
llm = ChatBedrockConverse(model=MODEL, region_name="us-east-1")
print("[LangChain]", llm.invoke(messages).content)

# 모델을 다른 provider로 바꿔도 messages와 invoke 코드는 그대로입니다
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(model="gpt-5.4-mini")  # 동일하게 동작