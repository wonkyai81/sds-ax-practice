# verify_sources.py - 근거 문서를 함께 반환
from langchain_core.runnables import RunnableParallel
from rag_chain import rag_chain, retriever

rag_with_sources = RunnableParallel(
    answer=rag_chain,
    sources=retriever | (lambda docs: sorted({d.metadata["source"] for d in docs})),
)
result = rag_with_sources.invoke("물류플랫폼팀 박도윤입니다. 해외 출장 숙박비 한도가 얼마인가요?")
print(result["answer"])
print("근거 문서:", result["sources"])