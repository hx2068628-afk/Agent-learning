from langchain_community.chat_models import ChatTongyi


from pydantic import BaseModel, Field

from agent_learning.env_utils import DASHBOARD_API_KEY

llm =ChatTongyi(
    model="qwen-max",
    api_key=DASHBOARD_API_KEY,
)
class Movie(BaseModel):
    title:str = Field(description="电影的标题")
    describe:str = Field(description="电影的描述")
    director:str = Field(description="电影的导演")

llm_struct_out=llm.with_structured_output(Movie)
for chunk in llm_struct_out.stream("介绍《机器人总动员》，包括标题、描述和导演"):
    print(chunk,end="",flush=True)
