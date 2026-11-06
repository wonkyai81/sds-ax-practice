# chain_limit.py - 체인에는 되돌아가기를 적을 자리가 없다는 것을 확인합니다.
#
# 이 파일은 LLM을 부르지 않습니다. 모델을 부르면 실행할 때마다 답이 달라져서
# 무엇 때문에 막히는지가 잘 안 보이기 때문입니다.
# 그래서 검색과 생성을 흉내만 내는 함수 세 개로 2일차와 같은 모양의 체인을 만듭니다.
# 누가 돌려도 결과가 똑같이 나옵니다.

from langchain_core.runnables import RunnableLambda


# ---------- 1) 체인에 끼울 부품 세 개를 만듭니다 ----------

def retrieve(question: str) -> dict:
    """2일차 retriever 자리입니다.
    진짜 벡터 검색 대신, 질문에 '재택'이라는 말이 있을 때만
    문서를 찾았다고 치는 가짜 검색기입니다."""
    if "재택" in question:
        found = ["재택근무는 주 2회까지 가능하다."]   # 검색 성공
    else:
        found = []                                    # 검색 실패: 관련 문서를 못 찾음
    print(f"  [retrieve] 질문={question!r} -> 문서 {len(found)}건")
    return {"question": question, "docs": found}


def build_prompt(data: dict) -> dict:
    """2일차 prompt 자리입니다. 찾은 문서를 문자열 하나로 합칩니다."""
    context = "\n".join(data["docs"]) if data["docs"] else "(근거 문서 없음)"
    return {"question": data["question"], "context": context}


def generate(data: dict) -> str:
    """2일차 llm 자리입니다. 근거가 없으면 모른다고 답하도록 흉내만 냅니다."""
    if data["context"] == "(근거 문서 없음)":
        return "죄송합니다. 관련 규정을 찾지 못했습니다."
    return f"답변: {data['context']}"


# ---------- 2) 부품을 체인으로 잇습니다. 2일차와 같은 모양입니다 ----------
# retrieve -> build_prompt -> generate 로 왼쪽에서 오른쪽으로 한 번 흐릅니다.
chain = RunnableLambda(retrieve) | RunnableLambda(build_prompt) | RunnableLambda(generate)


# ---------- 3) 검색이 실패하는 질문을 넣어 봅니다 ----------
# '재택'이라는 말이 없으므로 retrieve가 빈손으로 돌아옵니다.
print("[1] 체인을 한 번 실행합니다")
print("  결과:", chain.invoke("집에서 일해도 되나요?"))


# ---------- 4) 여기서 요구가 하나 늘어납니다 ----------
# "검색 결과가 없으면 질문을 바꿔서 다시 찾아라."
#
# 이 지시를 위의 chain 안에 적을 수 있을까요? 적을 칸이 없습니다.
# chain은 부품을 | 로 이어 붙인 파이프라서, 사이에 놓을 수 있는 것은
# 다음에 실행할 부품뿐입니다. "실패했으면 앞으로 돌아가라"를 넣을 자리가 없습니다.
#
# 그래서 아래처럼 체인 바깥에 while 루프를 따로 둘 수밖에 없습니다.

print("\n[2] 재검색을 넣으려면 체인 바깥에 루프를 둬야 합니다")

question = "집에서 일해도 되나요?"
alternatives = ["재택근무 규정", "재택근무 며칠"]   # 바꿔서 다시 물어볼 질문 후보
attempt = 0

answer = chain.invoke(question)                    # 첫 시도

while "찾지 못했습니다" in answer and attempt < len(alternatives):
    question = alternatives[attempt]               # 질문을 바꾸고
    attempt += 1
    print(f"  [바깥 루프] {attempt}번째 재시도 -> 질문을 {question!r} 로 바꿉니다")
    answer = chain.invoke(question)                # 체인을 처음부터 다시 실행

print(f"\n최종 답변: {answer}")
print(f"재시도 횟수: {attempt}")

# ---------- 5) 무엇을 봐야 하는지 ----------
print("\n[관찰] 다시 찾을지 말지를 판단하는 코드와 반복하는 코드가")
print("       chain 안에 있습니까, 이 파일의 while 문 안에 있습니까?")