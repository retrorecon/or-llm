import streamlit as st
import time
"""
OR-LLM Application Main code
I will change all the comments, they're just placeholder and don't follow any guideline at all.
"""

# Set up the Streamlit page layout
st.set_page_config(layout="wide", page_title="LangGraph Chat Application")

# Initialize session state for chat history, LaTeX, and code
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "latex_content" not in st.session_state:
    st.session_state["latex_content"] = ""
if "code_content" not in st.session_state:
    st.session_state["code_content"] = ""

# Function to simulate interaction with LLM_0 and other LLMs
def interact_with_llms(user_message):
    """
    Simulates interaction with LLM_0 and other LLMs.
    Replace this with the logic for your actual LLM interaction.
    """
    # Example interaction logic
    latex, code = False, False
    response = "Response from LLM_0"
    if user_message == "give me latex":
        latex = True
        response = "Here's your LaTeX!"
    if user_message == "give me code":
        code = True
        response = "Here's your code!"

    # Simulate JSON responses from tools (LLMs)
    simulated_tool_response = {
        "code": "print('Hello, LangGraph!')" if code else "",
        "latex": r"\int_a^b f(x) dx = F(b) - F(a)" if latex else r""
    }

    # Update LaTeX and code panes with the simulated responses
    if code:
        st.session_state["code_content"] = simulated_tool_response["code"]
    if latex:
        st.session_state["latex_content"] = simulated_tool_response["latex"]
    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# Layout for the application
st.title("LangGraph Chat Application")
st.subheader("Interact with multiple LLMs seamlessly")

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
                stream = interact_with_llms(prompt)
                # This line should be replaced with the LangGraph thingy
                response = st.write_stream(stream)
        st.session_state.chat_history.append({"role": "assistant", "content": response})


# Column 2: LaTeX Section
with col2:
    st.header("LaTeX Output")
    latex_container = st.container()
    with latex_container:
        if st.session_state["latex_content"]:
            st.latex(st.session_state["latex_content"])

# Column 3: Python Code Section
with col3:
    st.header("Python Code Output")
    code_container = st.container()
    with code_container:
        if st.session_state["code_content"]:
            st.code(st.session_state["code_content"], language="python")
