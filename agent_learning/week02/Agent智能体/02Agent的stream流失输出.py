import datetime

from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool

from agent_learning.env_utils import DASHBOARD_API_KEY

@tool(description="查询日期")
def get_day():
    return datetime.datetime.now()

agent = create_agent(
    model=ChatTongyi(model="qwen-max",api_key=DASHBOARD_API_KEY),
    tools=[get_day],
    system_prompt="你是一个专业助手,能够回答用户的问题",
)


for r in agent.stream({"messages":[{"role":"human","content":"今天星期几"}]},stream_mode="values"):
    latest_message = r["messages"][-1]
    if latest_message.content:
        print(type(latest_message).__name__,latest_message.content)
    try:
        if latest_message.tool_calls:
            print(f"工具调用:{[tc['name'] for tc in latest_message.tool_calls]}")
    except AttributeError:
        pass
