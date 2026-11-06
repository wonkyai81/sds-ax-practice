[Day6] 공통 checkpoint

6일차 통합 실습은 개인 결과물이 아니라 검증된 공통 checkpoint에서 시작합니다.
day6_practice 폴더에 풀어 두고 씁니다.

담긴 것
  chroma_db/         2일차 벡터 DB (사내 정책 문서 임베딩 완료, 6개 청크)
  docs/              벡터 DB의 원본 문서 3종
  build_chroma.py    chroma_db 재생성 스크립트 (문서를 고쳤을 때만 사용)
  mcp_server.py      4일차 MCP 서버
  make_data.py       임직원·자산·프로젝트 JSON 3종 생성기
  eval_set.json      2~5일차 누적 평가셋 12문항 (전날 미션을 못 따라온 경우에만 사용)

chroma_db 는 이미 생성해 넣었습니다 (사내 정책 문서 3종, 6개 청크).
문서를 고쳤을 때만 build_chroma.py 를 다시 돌려 재생성하면 됩니다.
  python build_chroma.py

시작 전에 할 것
  1) python make_data.py 로 JSON 3종 생성 (4일차 폴더에서 복사해도 동일)
  2) 이 폴더에 새 가상환경을 만들고 레포 루트의 requirements.txt 로 설치
       python -m venv .venv
       .venv\Scripts\activate
       python -m pip install -r ..\requirements.txt
  3) .env 는 레포 루트의 것을 씁니다

주의
  eval_set.json 은 전날 실습 폴더(day5_practice)에서 누적해 온 본인 파일을 이 폴더로 복사해 쓰는 것이 기본입니다.
  여기 들어 있는 것은 전날 미션을 못 따라온 경우의 대체본입니다. 그냥 쓰면 누적 문항이 날아갑니다.
