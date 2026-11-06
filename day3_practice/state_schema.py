# state_schema.py - State 스키마 정의
from typing import TypedDict


class State(TypedDict):
    user_input: str   # 사용자가 넣는 입력
    response: str     # 그래프가 채울 응답


initial: State = {"user_input": "안녕하세요", "response": ""}
print(initial)
print(type(initial))   # 실행 시점에는 그냥 dict입니다