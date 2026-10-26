# check_credentials.py - 자격 증명 로드 확인
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일의 내용을 환경변수로 읽어 들입니다

key = os.getenv("AWS_ACCESS_KEY_ID")
if key:
    # 키 전체를 출력하면 안 되므로 앞 4자리만 확인합니다
    print(f"[OK] AWS_ACCESS_KEY_ID 로드됨: {key[:4]}...")
else:
    print("[실패] AWS_ACCESS_KEY_ID 가 없습니다. .env 파일 위치와 내용을 확인하세요.")