from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph , END , START
from langgraph.graph.message import add_messages
from typing import Annotated , TypedDict
from tools.retriever import document_retriever
from tools.web_search import web_search
from langgraph.prebuilt import ToolNode
from config.settings import settings
from tools.code_pipeline import code_tool

class AgentState(TypedDict):
    messages : Annotated[list , add_messages]


tools = [
    # gmail_tools,
    web_search,
    document_retriever,
    code_tool
]

def orchestrator(state:AgentState):
    llm = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.BASE_URL,
        model=settings.OPENAI_MODEL,
        max_tokens=2048
    )
    llm_with_tool = llm.bind_tools(tools)

    result = llm_with_tool.invoke(state["messages"])
    return {"messages" : [result]}

def should_continue(state:AgentState):
    last_msg = state["messages"][-1]
    if last_msg.tool_calls:
        return "tools"
    return END

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("agent",orchestrator)
    graph.add_node("tools",ToolNode(tools))

    graph.add_edge(START,"agent")
    graph.add_conditional_edges("agent" , should_continue),
    graph.add_edge("tools","agent")

    return graph.compile()

def run_orchestrator(user_message:str):
    app = build_graph()
    result = app.invoke({"messages":[("human",user_message)]})
    return result["messages"][-1].content