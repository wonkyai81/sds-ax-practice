# chunking.py - 청킹 설정 비교
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

docs = TextLoader("docs/leave_policy.md", encoding="utf-8").load()

for size, overlap in [(100, 0), (100, 50), (300, 50)]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    chunks = splitter.split_documents(docs)
    print(f"\n=== chunk_size={size}, overlap={overlap} -> {len(chunks)}개 청크 ===")
    for i, c in enumerate(chunks):
        print(f"[{i}] ({len(c.page_content)}자) {c.page_content[:40].replace(chr(10), ' ')}...")