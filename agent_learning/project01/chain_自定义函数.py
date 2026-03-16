#chain = first_prompt | llm | jsonparser | second_prompt | llm | strparser

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_openai.chat_models import ChatOpenAI

from agent_learning.env_utils import OPENAI_API_KEY, OPENAI_BASE_URL
from langchain_core.prompts import PromptTemplate

llm=ChatOpenAI(
    model="kimi-k2.5",
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)
strOutput=StrOutputParser()
jsonOutput=JsonOutputParser()
first_prompt=PromptTemplate.from_template(
    "我的邻居叫{name},生了一个{gender}孩子,帮我取一个名字。仅返回一个名字."
)
second_prompt=PromptTemplate.from_template(
    "解释{name}的含义。"
)

my_func=RunnableLambda(lambda  ai_meg:{"name":ai_meg.content})

chain = first_prompt | llm | my_func | second_prompt | llm |strOutput
for i in chain.stream({"name":"肖世峰","gender":"男"}):
    print(i,end="",flush=True)
