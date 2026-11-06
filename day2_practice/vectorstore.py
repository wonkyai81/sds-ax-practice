# vectorstore.py - 벡터 저장소 구축과 디스크 저장
from dotenv import load_dotenv
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma
from metadata import load_chunks

load_dotenv()
embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    region_name="us-east-1",
)

db = Chroma.from_documents(
    documents=load_chunks(),
    embedding=embeddings,
    collection_name="sds_policies",
    persist_directory="./chroma_db",   # 이 폴더에 저장됩니다 (6일차까지 사용)
)
print(f"적재 완료: {db._collection.count()}개 청크")

# 의미 검색 확인 (점수 포함)
for q in ["월차 며칠 받을 수 있어?", "집에서 일해도 되나요?", "법카 등록 기한"]:
    hits = db.similarity_search_with_score(q, k=2)
    print(f"\n질문: {q}")
    for doc, score in hits:
        print(f"  [{doc.metadata['source']}] (거리 {score:.3f}) {doc.page_content[:40]}...")

# 메타데이터 필터 검색
hits = db.similarity_search("경비 정산 규정", k=2, filter={"department": "총무팀"})
print(f"\n총무팀 문서로 한정 검색: {[h.metadata['source'] for h in hits]}")