from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from typing import TypedDict, Annotated, List, Literal
from helper import *
import json

class MathMod(TypedDict):
    cat: str
    sets: dict
    dv: dict
    params: dict
    obj: str
    cons: dict


class AgentState(TypedDict):
    llm: str
    messages: Annotated[List[HumanMessage | AIMessage], "MessageList"]
    mode: str
    mathmod: MathMod
    code: str


def select_next(state: AgentState) -> Literal["primary", "coding", "__end__"]:
    # Determine the tool to be used. If no tool usage necessary, go to end.
    # TODO
    # I'm not sure if it is better to go to __end__ or primary.
    if state["mode"] == "coding":
        return "coding"
    
    return "__end__"
    

def primary_agent(state: AgentState):
    """
    Primary agent that constructs the mathematical model with the user. It can offload the coding part to the other agent.
    Inputs:
        state: Current state of the LangChain. It includes the model, code, and discussions so far.
    Outputs:
        state: Resulting state. It will either go back to the user, or go to the coding agent after this state, as depicted in the state field 'mode'
    """
    llm = LLM_CONS[state['llm']](**LLM_PARAMS[state['llm']])
        
    # TODO: I don't know if making this a seperate message hurts the process. I might consider combining it with the last message.
    prompt = [] # This is the auxilarry prompt to pass the model in the user's system into the chat, if there is one.
    if 'mathmod' in state:
        prefix = f"Here is my current model. If my question is not related to changing my model, just ignore the model and reply to my question."
        last_model = state['mathmod']
        prompt = [HumanMessage(content=f"\n{prefix}\n{last_model}")]

    # Process the user's request.
    request = llm.invoke(state['messages'] + prompt)

    # Construct the json
    if request.content[:8] ==  '```json\n':
        request_text = request.content[8:-4] # Remove  ```json ... ``` headers
    else:
        request_text = request.content
    try:
        request_json = json.loads(request_text)
    except:
        request_json = {'messages': request_text}

    # If the result has a mathematical model, construct the code for it.

    
    mode = "modeling"
    msg = []
    msg.extend([AIMessage(content=f"{_msg}") for _msg in request_json["messages"]])
    if 'mathmod' in request_json:
        if request_json['mathmod'] != {}:
            state["mathmod"] = request_json["mathmod"]
            # msg.append(AIMessage(content=f"Let me (re)build the code of your mathematical model!"))
            mode =  "coding"
    

    state["messages"].extend(msg)
    state["mode"] = mode
    return state


def coding_agent(state: AgentState):
    """
    Coding agent that constructs the Python code
    """

    llm = LLM_CONS[state['llm']](**LLM_PARAMS[state['llm']])

    # Process the code conversion request.
    
    sys_prompt = SystemMessage(content=CODING_MASTER_PROMPT)
    code = state.get('code')
    _prompt = {'mathmod': state['mathmod']}
    if code is not None:
        _prompt['code'] = "```python\n" + code + "\n```"
    prompt = HumanMessage(content=f"{_prompt}")
    
    request = llm.invoke([sys_prompt, prompt])

    # Construct the json
    request_text = request.content[8:-4] # Remove  ```json ... ``` headers
    request_json = json.loads(request_text)

    code = request_json["code"]
    # Remove  ```python ... ``` headers if there are any.
    if code[:9] == "```python":
        code = code[10:-4] 

    state['code'] = code
    state['mode'] = "modeling"
    return state
    

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("primary", primary_agent)
workflow.add_node("coding", coding_agent)

# Add edges
workflow.add_edge(START, "primary")
workflow.add_conditional_edges("primary", 
                                select_next)

# Compile the graph
app = workflow.compile()

print("Successfully compiled")