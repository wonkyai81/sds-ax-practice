[Day5] 공통 checkpoint

5일차 실습을 시작할 때 day5_practice 폴더에 풀어 두고 씁니다.

담긴 것
  mcp_server.py      4일차에 만든 MCP 서버. 5-2 종합 적용에서 그대로 씁니다
  make_data.py       임직원·자산·프로젝트 JSON 3종 생성기
  attack_set.json    도전 미션 채점용 공격 10문항
  normal_set.json    도전 미션 채점용 정상 10문항 (오탐 확인)
  eval_set.json      2~4일차 누적 평가셋 10문항 (전날 미션을 못 따라온 경우에만 사용)

시작 전에 할 것
  1) python make_data.py 를 실행해 employees.json, assets.json, projects.json 을 만듭니다
     (4일차 폴더에서 복사해 와도 결과는 같습니다)
  2) 가상환경은 레포 루트의 .venv 를 그대로 활성화합니다
  3) .env 는 레포 루트의 것을 씁니다. 복사하지 않습니다

들어 있지 않은 것
  guards_*.py, *_middleware.py 는 오늘 직접 만드는 실습 대상이라 넣지 않았습니다

주의
  eval_set.json 은 전날 실습 폴더(day4_practice)에서 누적해 온 본인 파일을 이 폴더로 복사해 쓰는 것이 기본입니다.
  여기 들어 있는 것은 전날 미션을 못 따라온 경우의 대체본입니다. 그냥 쓰면 누적 문항이 날아갑니다.
  도전 미션 마지막에 오늘 guardrail 2문항을 여기에 이어 붙이면 12문항이 됩니다.
