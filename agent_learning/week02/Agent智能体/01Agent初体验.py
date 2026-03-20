import datetime
import os

from langchain.agents import create_agent
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from agent_learning.env_utils import DASHBOARD_API_KEY


@tool(description="查询日期")
def get_day(): 
    return "今天是2026年3月20日"

agent = create_agent(
    model=ChatTongyi(model="qwen-max",api_key=DASHBOARD_API_KEY),
    tools=[get_day],
    system_prompt="你是一个专业助手,能够回答用户的问题",
)

res=agent.invoke({
    "messages":[
        {"role":"human","content":"今天星期几"}
    ]
})
for r in res["messages"]:
    print(type(r),r.content)
