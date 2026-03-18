from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

from agent_learning.env_utils import DASHBOARD_API_KEY


vector_store=InMemoryVectorStore(embedding=DashScopeEmbeddings(dashscope_api_key=DASHBOARD_API_KEY))

loader =CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source"
)
documents = loader.load()

vector_store.add_documents(
    documents=documents,
    ids=["id"+str(i) for i in range(1,len(documents)+1)]
)
vector_store.delete(["id1","id2"])

result=vector_store.similarity_search(
    query="Python",
    k=2
)
print(result)