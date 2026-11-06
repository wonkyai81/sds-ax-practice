# hello_graph.py - 첫 그래프 전체 코드
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    user_input: str
    response: str


def respond(state: State) -> dict:
    user = state["user_input"]
    return {"response": f"입력하신 내용은 '{user}' 입니다."}


builder = StateGraph(State)
builder.add_node("respond", respond)
builder.add_edge(START, "respond")
builder.add_edge("respond", END)

graph = builder.compile()    # 그래프를 실행 가능한 객체로 변환

result = graph.invoke({"user_input": "안녕하세요"})
print(result)

# 구조 시각화: PNG 저장이 안 되는 환경도 있으므로 try/except로 감쌉니다
try:
    graph.get_graph().draw_mermaid_png(output_file_path="hello_graph.png")
    print("hello_graph.png 저장 완료")
except Exception as e:
    print("PNG 저장은 건너뜁니다:", e)
    print(graph.get_graph().draw_mermaid())   # 텍스트 출력으로 대체