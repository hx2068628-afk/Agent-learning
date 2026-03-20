from altair import Stream
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda

from file_history_store import get_history
from env_utils import DASHBOARD_API_KEY
from vector_stores import VectorStoreService

import config_data as config

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt
class RagService(object):
    def __init__(self):
        self.vector_service=VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name,dashscope_api_key=DASHBOARD_API_KEY),
        )
        self.prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system","你是一个专业的助手,以我提供的参考资料{context}为主,回答问题"),
                ("system","以下是用户的对话历史记录"),
                MessagesPlaceholder("history"),
                ("human","回答如下问题:{input}"),
            ]
        )
        self.chat_model=ChatTongyi(model=config.chat_model_name,api_key=DASHBOARD_API_KEY)
        self.chain=self._get_chain()

    def _get_chain(self):
        retriever=self.vector_service.get_retriever()

        def format_document(documents):
            if not documents:
                return "无相关参考资料"
            formatted_str =""
            for doc in documents:
                formatted_str +=f"文档片段:{doc.page_content}\n"
            return formatted_str
        def temp2(value):
            new_value={}
            new_value["input"]=value["input"]["input"]
            new_value["context"]=value["context"]
            new_value["history"]=value["input"]["history"]
            return new_value

        def temp1(value):
            return value["input"]
        chain=(
            {
                "input":RunnablePassthrough(),
                "context":RunnableLambda(temp1) | retriever | format_document
            }|RunnableLambda(temp2)|self.prompt_template|print_prompt|self.chat_model|StrOutputParser()
        )
        conversation_chain =RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain

if __name__=="__main__":
    session_config={
        "configurable":{
            "session_id":"user_001"
        }
    }
    res=RagService().chain.invoke({"input":"编程入门的一个输出是什么"},session_config)
    print(res)
