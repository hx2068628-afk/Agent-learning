from google.protobuf.internal.well_known_types import Struct
from langchain_community.chat_models import ChatTongyi
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore

from agent_learning.env_utils import DASHBOARD_API_KEY

vector_store=InMemoryVectorStore(embedding=DashScopeEmbeddings(dashscope_api_key=DASHBOARD_API_KEY,model="text-embedding-v4"))

loader=CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source"
)
documents = loader.load()
vector_store.add_documents(documents=documents)
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","你是一个专业的问答机器人,基于{context}信息回答"),
        ("human","告诉我{input}")
    ]
)
llm =ChatTongyi(
    model="qwen-max",
    api_key=DASHBOARD_API_KEY,
)
input_text="Python相关的信息"
retriever =vector_store.as_retriever(search_kwargs={"k":2})
def format_func(docs):
    if not docs:
        return "没有相关信息"
    formatted_str ="["
    for doc in docs:
        formatted_str+=doc.page_content
    formatted_str+="]"
    return formatted_str

def print_prompt(prompt):
    print(prompt.to_string())
    return prompt
chain =(
    {"input":RunnablePassthrough(),"context":retriever|format_func}|prompt|print_prompt|llm|StrOutputParser()
)
res=chain.invoke(input_text)
print(res)