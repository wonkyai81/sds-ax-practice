# embedding.py - 임베딩 확인
from dotenv import load_dotenv
from langchain_aws import BedrockEmbeddings

load_dotenv()
embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    region_name="us-east-1",
)

v = embeddings.embed_query("연차 휴가는 며칠인가요?")
print(f"벡터 차원: {len(v)}")
print(f"앞 5개 값: {[round(x, 4) for x in v[:5]]}")