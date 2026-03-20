import datetime

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call
from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langgraph.runtime import Runtime

from agent_learning.env_utils import DASHBOARD_API_KEY

@tool(description="查询日期")
def get_day(country:str):
    return f"在{country}，{datetime.datetime.now().strftime('%Y%m%d')}"

@before_agent
def log_before_agent(state:AgentState,runtime:Runtime)->None:
    print(f"[before_agent]agent启动，并附带{len(state['messages'])}条消息")

@after_agent
def log_after_agent(state:AgentState,runtime:Runtime)->None:
    print(f"[after_agent]agent结束，并附带{len(state['messages'])}条消息")

@before_model
def log_before_model(state:AgentState,runtime:Runtime)->None:
    print(f"[before_model]模型启动，并附带{len(state['messages'])}条消息")

@after_model
def log_after_model(state:AgentState,runtime:Runtime)->None:
    print(f"[after_model]模型结束，并附带{len(state['messages'])}条消息")

@wrap_model_call
def model_call_hook(request,handler):
    print("模型调用啦")
    return handler(request)

@wrap_tool_call
def tool_call_hook(request,handler):
    print("工具调用啦")
    print(f"工具执行:{request.tool_call['name']}")
    print(f"工具参数:{request.tool_call['args']}")
    return handler(request)

agent=create_agent(
    model=ChatTongyi(
        model="qwen-max",
        api_key=DASHBOARD_API_KEY,
    ),
    tools=[get_day],
    middleware=[model_call_hook,tool_call_hook,log_before_agent,log_after_agent,log_before_model,log_after_model],
)

# for r in agent.stream({"messages":[{"role":"human","content":"在中国，今天星期几"}]},stream_mode="values"):
#     print(r["messages"][-1].content)
res=agent.invoke({"messages":[{"role":"human","content":"在中国，今天星期几"}]})
print(res["messages"][-1].content)
