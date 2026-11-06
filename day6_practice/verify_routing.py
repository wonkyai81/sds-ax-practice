# verify_routing.py - 단일 질문과 복합 질문 검증
from supervisor_assembled import run

if __name__ == "__main__":
    # 단일 질문 3종 (Agent별 1개)
    # run("물류플랫폼팀 임직원 명단 조회해줘")            # data_agent만
    # run("재택근무는 주 며칠까지 가능해?")               # research_agent만
    run("한국의 수도는?")                  # general_agent만
    run("고마워, 오늘 도움 많이 됐어")                  # general_agent만

    # 복합 질문 (data + research)
    # run("클라우드운영팀 GPU 서버 자산 현황을 알려주고, 출장 규정상 식비 한도도 함께 알려줘")