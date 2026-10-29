from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from nodes import agent_node, should_use_tools
from tools import calculator, search_tool
from state import AgentState
import os
from functools import partial

load_dotenv()

def build_graph():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        api_key = os.getenv("GOOGLE_API_KEY")
    )

    llm_with_tools = model.bind_tools([calculator,  search_tool])

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", partial(agent_node, llm_with_tools = llm_with_tools))
    workflow.add_node("tool", ToolNode(tools=[calculator, search_tool]))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        should_use_tools,
        {
            "tool": "tool",
            "end": END
        }
    )
    workflow.add_edge("tool", "agent")

    return workflow.compile()