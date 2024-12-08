from llm_handler import *
import streamlit as st
import time
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from helper import *

# """
# OR-LLM Application Main code
# I will change all the comments, they're just placeholder and don't follow any guideline at all.
# """

# Set up the Streamlit page layout
st.set_page_config(layout="wide", page_title="LangGraph Chat Application")

# Initialize session state for chat history, LaTeX, and code
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "latex_content" not in st.session_state:
    st.session_state["latex_content"] = ""# {"dv": "", "params": "", "obj": "", "cons": "",}
if "code_content" not in st.session_state:
    st.session_state["code_content"] = ""#{"code": ""}
if "agent_history" not in st.session_state:
    st.session_state["agent_history"] = {"messages": [SystemMessage(content=MODELING_MASTER_PROMPT)]}


# Layout for the application
st.title("OR-LLM")
st.subheader("Develop mathematical optimization models and code with LLMs!")

# LLM Picking point
llm_provider = st.sidebar.selectbox("Choose LLM Provider:", ["OpenAI", "Gemini"])
llm_dict = {"OpenAI": "openai", "Gemini":"gemini"}
# selected_page = st.sidebar.text_input("API Key:", type="password")


col1, col2, col3 = st.columns([1, 1, 1])

# Column 1: Chat Section
with col1:
    st.header("Chat")
    chat_container = st.container(height=400)
    with chat_container:
        for message in st.session_state["chat_history"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Fixed chat input at the bottom
    prompt = st.chat_input("What is up?")
    if prompt:
        # Display user message in chat message container
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Generate and display assistant response
        with chat_container:
            with st.chat_message("assistant"):
                

                inputs = st.session_state["agent_history"]
                inputs["messages"].append(HumanMessage(content=prompt)) # In addition to the previous history, append the new message.
                inputs["llm"] = llm_dict[llm_provider]
                result = app.invoke(inputs)
                st.session_state["agent_history"] = result # Save the agent state.
                for i in range(len(st.session_state["chat_history"]), len(result['messages'])):
                    st.markdown(result['messages'][i].content)

        for i in range(len(st.session_state["chat_history"]), len(result['messages'])):
            st.session_state.chat_history.append({"role": "assistant", "content": result['messages'][i].content})
        if "code" in result:
            st.session_state["code_content"] = result["code"]
        if "mathmod" in result:
            st.session_state["latex_content"] = result["mathmod"]


# Column 2: LaTeX Section
with col2:
    st.header("LaTeX Output")
    latex_container = st.container()
    with latex_container:
        if st.session_state["latex_content"]:
            # I know this is not the prettiest way to do it. But I wanted to do sth that is fast to see temporarily
            mathmod = st.session_state["latex_content"]
            st.markdown("## Category:")
            st.markdown(f"{mathmod['cat']}")
            st.markdown("## Sets:")
            for v in mathmod["sets"].values():
                st.latex(v)
            st.markdown("## Decision Variables:")
            for v in mathmod["dv"].values():
                st.latex(v)
            st.markdown("## Parameters:")
            for v in mathmod["params"].values():
                st.latex(v)
            st.markdown("## Objective Function:")
            st.latex(mathmod["obj"])
            st.markdown("## Constraints:")
            for v in mathmod["cons"].values():
                st.latex(v["cons"])
                st.markdown(v["desc"])


# Column 3: Python Code Section
with col3:
    st.header("Python Code Output")
    code_container = st.container()
    with code_container:
        if st.session_state["code_content"]:
            st.code(st.session_state["code_content"], language="python")
