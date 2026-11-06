# chunking_md.py - 마크다운 헤더 기준 분할
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter

docs = TextLoader("docs/leave_policy.md", encoding="utf-8").load()

headers = [("#", "title"), ("##", "section")]
md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)
md_chunks = md_splitter.split_text(docs[0].page_content)
for c in md_chunks:
    print(c.metadata, "->", c.page_content[:30])