# check_env.py - 환경 점검 스크립트
import sys
import importlib

print(f"Python 버전: {sys.version}")
assert sys.version_info >= (3, 10), "Python 3.10 이상이 필요합니다."

packages = ["langchain", "langchain_core", "langchain_aws", "dotenv"]
for name in packages:
    try:
        mod = importlib.import_module(name)
        version = getattr(mod, "__version__", "버전 정보 없음")
        print(f"[OK] {name} ({version})")
    except ImportError:
        print(f"[실패] {name} 이 설치되지 않았습니다. pip install 을 확인하세요.")