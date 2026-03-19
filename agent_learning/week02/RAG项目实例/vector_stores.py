from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

import config_data as config
from agent_learning.env_utils import DASHBOARD_API_KEY


class VectorStoreService(object):
    def __init__(self,embedding):
        self.embedding=embedding
        self.vector_stor=Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )

    def get_retriever(self):
        return self.vector_stor.as_retriever(search_kwargs={"k":config.similarity_threshold})

if __name__=="__main__":
    retriever=VectorStoreService(DashScopeEmbeddings(dashscope_api_key=DASHBOARD_API_KEY,model="text-embedding-v4")).get_retriever()
    results=retriever.invoke("你好的翻译")
    print(results)
