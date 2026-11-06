# verify.py - RAG 유무 비교 검증
from rag_chain import rag_chain, llm


def get_text(message):
    """ChatBedrockConverse는 content를 블록 리스트로 주기도 하므로 텍스트만 모아 반환합니다."""
    content = message.content
    if isinstance(content, list):
        return "".join(block.get("text", "") for block in content if isinstance(block, dict))
    return content


questions = [
    "국내 출장 식비 한도는 하루 얼마인가요?",   # 문서에 답 있음
    "재택근무는 주 며칠까지 가능한가요?",       # 문서에 답 있음
    "육아휴직은 얼마나 쓸 수 있나요?",          # 문서에 답 없음 -> 모른다고 해야 정답
]

for q in questions:
    print("=" * 60)
    print(f"질문: {q}")
    print(f"\n[RAG 없음] {get_text(llm.invoke(q))[:100]}")
    print(f"\n[RAG 적용] {rag_chain.invoke(q)}")