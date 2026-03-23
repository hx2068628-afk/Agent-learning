import streamlit as st

from agent.react_agent import ReactAgent


st.set_page_config(page_title="智能客服 Agent", page_icon="🤖", layout="wide")
st.title("智能客服 Agent")

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("智能客服思考中..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        if response_messages:
            st.session_state["message"].append(
                {"role": "assistant", "content": response_messages[-1]}
            )
        st.rerun()
