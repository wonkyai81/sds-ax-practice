# first_call_raw.py - 원본 요청/응답 JSON 구조 확인
import json
import boto3
from dotenv import load_dotenv

load_dotenv()
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# 요청: modelId + messages 배열이 핵심입니다
response = client.converse(
    modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    messages=[
        {"role": "user", "content": [{"text": "안녕하세요. 자기소개를 한 문장으로 해주세요."}]}
    ],
)

# 응답 전체를 JSON으로 출력해 구조를 눈으로 확인합니다
print(json.dumps(response, indent=2, ensure_ascii=False, default=str))