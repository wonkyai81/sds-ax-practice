# load_db.py - 두 번째 실행부터는 이렇게 (임베딩 비용 0)
from dotenv import load_dotenv
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma

load_dotenv()
embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    region_name="us-east-1",
)

db = Chroma(
    collection_name="sds_policies",
    embedding_function=embeddings,     # 질문을 임베딩할 때 필요하므로 여전히 지정
    persist_directory="./chroma_db",
)
print(f"불러온 청크 수: {db._collection.count()}")