import time

import streamlit as st
from knowledge_base import KnowledgeBaseService
st.title("知识库更新服务")
uploaded_file = st.file_uploader(
    label="请上传txt文件",
    type=["txt"],
    accept_multiple_files=False,
)
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()
if uploaded_file is not None:
    file_name=uploaded_file.name
    file_type=uploaded_file.type
    file_size=uploaded_file.size

    st.subheader(f"文件名:{file_name}")
    st.write(f"格式{file_type}|大小{file_size:.2f}KB")

    text =uploaded_file.getvalue().decode("utf-8")
    with st.spinner("载入知识库中..."):
        time.sleep(1)
        res=st.session_state["service"].upload_by_str(text,file_name)
        st.write(res)



