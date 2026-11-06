# checkpointer_basic.py - SQLite 체크포인터와 thread_id 기초
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_aws import ChatBedrockConverse
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
)

# SqliteSaver: 파일에 저장하므로 스크립트를 껐다가 다시 켜도 대화가 유지됩니다
def get_text(message):
    """ChatBedrockConverse는 content를 블록 리스트로 주기도 하므로 텍스트만 모아 반환합니다."""
    content = message.content
    if isinstance(content, list):
        return "".join(block.get("text", "") for block in content if isinstance(block, dict))
    return content


with SqliteSaver.from_conn_string("checkpoints.sqlite") as checkpointer:
    agent = create_agent(
        model=llm,
        tools=[],
        checkpointer=checkpointer,   # 여기에 체크포인터를 간단하게 붙일 수 있습니다.
    )

    # thread_id는 config로 전달합니다. 이 형태를 그대로 익혀 둡니다.
    config = {"configurable": {"thread_id": "user_A"}}

    # 실제로는 아래와 같이 유저와 대화 ID를 기반으로 구분을 합니다.
    # config = {"configurable": {"thread_id":f"{current_user.id}:{conversation_id}"}}
    
    r1 = agent.invoke({"messages": [HumanMessage("내 이름은 김하늘이야")]}, config=config)
    print("1차:", get_text(r1["messages"][-1]))

    r2 = agent.invoke({"messages": [HumanMessage("내 이름이 뭐였지?")]}, config=config)
    print("2차(같은 thread):", get_text(r2["messages"][-1]))

    config_b = {"configurable": {"thread_id": "user_B"}}
    r3 = agent.invoke({"messages": [HumanMessage("내 이름이 뭐였지?")]}, config=config_b)
    print("3차(다른 thread):", get_text(r3["messages"][-1]))


        # 이 thread의 체크포인트 목록 (최신순)
    for snap in agent.get_state_history(config):
        print(snap.config["configurable"]["checkpoint_id"], len(snap.values["messages"]))

    # 돌아가고 싶은 시점의 config를 그대로 넘기면 그 상태에서 이어서 실행됩니다
    past = list(agent.get_state_history(config))[2]     # 2단계 전
    agent.invoke(None, config=past.config)

    # 그 시점의 State를 고쳐서 다시 실행할 수도 있습니다
    agent.update_state(past.config, {"messages": [HumanMessage("질문을 바꿉니다")]})