# metadata.py - 메타데이터 부착 (뒤 실습에서 재사용)
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 파일별 업무 메타데이터 (교육용 더미 데이터)
FILE_META = {
    "docs/leave_policy.md":       {"department": "인사팀", "updated_at": "2026-01-15"},
    "docs/remote_work_policy.md": {"department": "인사팀", "updated_at": "2026-03-02"},
    "docs/travel_policy.md":      {"department": "총무팀", "updated_at": "2025-11-20"},
}


def load_chunks():
    """세 문서를 로드해 메타데이터를 붙이고 청크로 나눕니다."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    all_chunks = []
    for path, meta in FILE_META.items():
        docs = TextLoader(path, encoding="utf-8").load()
        for d in docs:
            d.metadata.update(meta)      # source 위에 업무 정보 추가
        all_chunks.extend(splitter.split_documents(docs))
    return all_chunks


if __name__ == "__main__":
    chunks = load_chunks()
    for c in chunks[:3]:
        print(c.metadata)
    print(f"\n총 청크 수: {len(chunks)}")