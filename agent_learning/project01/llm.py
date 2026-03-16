from openai import OpenAI

from agent_learning.env_utils import OPENAI_API_KEY, OPENAI_BASE_URL

client=OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)
message = [
    {"role": "system", "content": "你是一个智能助手，回复简洁"},
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么我可以帮助你的吗？"},
]
while True:
    us = input("用户请输入:")
    if us == "exit":
        break
    message.append({"role": "user", "content": us})

    rep=client.chat.completions.create(
        model="kimi-k2.5",
        messages=message
    )
    message.append({"role": "assistant", "content": rep.choices[0].message.content})
    print(rep.choices[0].message.content)
    print(type(rep.choices[0].message.content))
    print(message)

