# tool_error.py - 실패를 메시지로 돌려주고 Agent가 복구하게 만들기
from langchain_core.tools import tool

# 교육용 더미 데이터입니다!
EMPLOYEES = [
    {"name": "김하늘", "team": "클라우드운영팀", "email": "haneul.kim@samsungsds.example.com"},
    {"name": "박도윤", "team": "물류플랫폼팀", "email": "doyun.park@samsungsds.example.com"},
    {"name": "이서준", "team": "클라우드운영팀", "email": "seojun.lee@samsungsds.example.com"},
]


@tool
def search_employee(name: str) -> str:
    """삼성SDS 임직원 디렉터리에서 이름으로 직원 정보를 조회한다.

    Args:
        name: 직원의 정확한 한국어 이름 (최소 2자)

    Returns:
        직원 정보 문자열, 또는 다음 행동을 안내하는 에러 메시지
    """
    try:
        # 1) 입력 검증 실패 -> raise 대신 안내 메시지 반환
        if not name or len(name) < 2:
            return "에러: 이름이 너무 짧습니다. 최소 2자 이상의 정확한 한국어 이름으로 다시 호출하세요."

        # 2) 정상 검색
        for emp in EMPLOYEES:
            if emp["name"] == name:
                return f"{emp['name']} / {emp['team']} / {emp['email']}"

        # 3) 결과 없음 -> 후보를 함께 알려주면 LLM이 다음 판단을 하기 쉬움
        candidates = ", ".join(e["name"] for e in EMPLOYEES)
        return f"'{name}' 직원을 찾을 수 없습니다. 등록된 직원: {candidates}"

    except Exception as e:
        # 4) 예상 못한 예외도 그래프를 죽이지 않고 메시지로 변환
        return f"에러: 조회 중 문제가 발생했습니다 ({type(e).__name__}). 잠시 후 다시 시도하세요."


if __name__ == "__main__":
    print(search_employee.invoke({"name": "김"}))       # 너무 짧음
    print(search_employee.invoke({"name": "홍길동"}))   # 없는 직원
    print(search_employee.invoke({"name": "김하늘"}))   # 정상