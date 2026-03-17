from langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

from agent_learning.env_utils import OPENAI_API_KEY, OPENAI_BASE_URL

llm=ChatOpenAI(
    model="kimi-k2.5",
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

chat_prompt=ChatPromptTemplate.from_messages(
    [
        ("system","你是边塞的一位诗人"),
        MessagesPlaceholder("history"),
        ("human","创建一首押韵的诗")
    ]
)
history_input=[
    ("human","创建一首月光的诗"),
    ("ai","床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
]
#print(chat_prompt.invoke({"history":history_input}).to_string())
chain = chat_prompt | llm
for i in chain.stream({"history":history_input}):
    print(i.content,end="",flush=True)

