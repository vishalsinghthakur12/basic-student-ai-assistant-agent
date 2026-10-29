from state import AgentState
from tools import calculator, search_tool
from langchain_core.messages import SystemMessage
from prompts import SYSTEM_PROMPT

def agent_node(state: AgentState, llm_with_tools):
    """
    A node that represents an agent with access to tools.

    Args:
        state (AgentState): The current state of the agent.
        llm_with_tools: The language model with access to tools.

    Returns:
        AgentState: The updated state of the agent.
    """
    # Use the llm_with_tools to generate a response based on the current state
    response = llm_with_tools.invoke(
        [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]
    )

    return {"messages": [response]}


def should_use_tools(state: AgentState):
    """
    Determines whether the agent should use tools based on the current state.

    Args:
        state (AgentState): The current state of the agent.

    Returns:
        str: "tool" if the agent should use tools, "end" otherwise.
    """
    print("reached")
    last_message = state["messages"][-1]


    if getattr(last_message, "tool_calls", None):
        print("tool required")
        return "tool"
    print("end required")
    return "end"