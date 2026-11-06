# build_chroma.py - 2일차 벡터 DB(chroma_db)를 한 번에 만드는 스크립트
"""강사용. 실행하면 docs/ 3종을 청킹·임베딩해 ./chroma_db 를 만듭니다.

실행: python build_chroma.py
     (레포 루트의 .env 에 AWS 자격 증명이 있어야 합니다)

만들어진 chroma_db 폴더를 이 checkpoint zip에 함께 넣어 배포합니다.
collection_name 과 persist_directory 는 전 과정에서 고정이므로 바꾸지 않습니다.
"""
from dotenv import load_dotenv
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

FILE_META = {
    "docs/leave_policy.md":       {"department": "인사팀", "updated_at": "2026-01-15"},
    "docs/remote_work_policy.md": {"department": "인사팀", "updated_at": "2026-03-02"},
    "docs/travel_policy.md":      {"department": "총무팀", "updated_at": "2025-11-20"},
}


def load_chunks():
    """세 문서를 로드해 메타데이터를 붙이고 청크로 나눕니다."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = []
    for path, meta in FILE_META.items():
        docs = TextLoader(path, encoding="utf-8").load()
        for d in docs:
            d.metadata.update(meta)
        chunks.extend(splitter.split_documents(docs))
    return chunks


if __name__ == "__main__":
    embeddings = BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0",
        region_name="us-east-1",
    )
    db = Chroma.from_documents(
        documents=load_chunks(),
        embedding=embeddings,
        collection_name="sds_policies",
        persist_directory="./chroma_db",
    )
    print(f"적재 완료: {db._collection.count()}개 청크")
    print("이제 chroma_db 폴더를 checkpoint zip에 함께 넣어 배포하세요.")
