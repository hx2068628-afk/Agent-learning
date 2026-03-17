from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from agent_learning.env_utils import OPENAI_API_KEY, OPENAI_BASE_URL

llm =ChatOpenAI(
    model="kimi-k2.5",
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    temperature=0.0
)
class Movie(BaseModel):
    title:str = Field(description="电影的标题")
    describe:str = Field(description="电影的大致内容")
    director:str = Field(default="未知",description="电影的导演")

llm_struct_out=llm.with_structured_output(Movie)
# for chunk in llm_struct_out.stream("请推荐一部关于机器人的电影，包括标题、描述和导演"):
#     print(chunk,end="",flush=True)
result = llm_struct_out.invoke("请推荐一部关于机器人的电影，包括标题、描述和导演。请严格按照指定的JSON格式返回结果，导演名字返回中文名字。")
print(result)