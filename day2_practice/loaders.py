# loaders.py - 문서 로더
from langchain_community.document_loaders import TextLoader, DirectoryLoader

# 1) 파일 하나 로드
loader = TextLoader("docs/leave_policy.md", encoding="utf-8")
docs = loader.load()
print(f"문서 수: {len(docs)}")
print(f"metadata: {docs[0].metadata}")
print(f"본문 앞 80자: {docs[0].page_content[:80]}")

# 2) 폴더 통째로 로드
dir_loader = DirectoryLoader(
    "docs",
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"},
)
all_docs = dir_loader.load()
print(f"\n전체 문서 수: {len(all_docs)}")
for d in all_docs:
    print(f"  - {d.metadata['source']} ({len(d.page_content)}자)")