# messages_role.py - role별 동작 차이 확인
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()
llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
)

# 1) system 메시지 없이
r1 = llm.invoke([HumanMessage(content="사내 메신저가 접속이 안 됩니다.")])
print("[system 없음]", r1.content)

# 2) system 메시지로 페르소나 지정
r2 = llm.invoke([
    SystemMessage(content="너는 삼성SDS IT지원팀 상담원이야. 접수 확인과 예상 처리 절차를 정중한 존댓말 두 문장으로 안내해."),
    HumanMessage(content="사내 메신저가 접속이 안 됩니다."),
])
print("[system 있음]", r2.content)

# 3) 대화 기록(assistant 메시지 포함)으로 맥락 전달
r3 = llm.invoke([
    SystemMessage(content="너는 삼성SDS IT지원팀 상담원이야."),
    HumanMessage(content="사내 메신저가 접속이 안 됩니다."),
    AIMessage(content="접수되었습니다. 사용 중인 운영체제를 알려주시겠어요?"),
    HumanMessage(content="Windows 11이요."),  # 모델이 '메신저 장애' 맥락을 알고 답합니다
])
print("[대화 기록]", r3.content)