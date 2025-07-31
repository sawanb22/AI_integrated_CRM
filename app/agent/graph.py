from typing import TypedDict
from langgraph.graph import StateGraph, END
from .agent import extract_interaction_from_text

class AgentState(TypedDict):
    message: str
    result: dict

def extract_node(state: AgentState) -> AgentState:
    parsed = extract_interaction_from_text(state["message"])
    return {"message": state["message"], "result": parsed.dict()}

def build_graph():
    sg = StateGraph(AgentState)
    sg.add_node("extract", extract_node)
    sg.set_entry_point("extract")
    sg.add_edge("extract", END)
    return sg.compile()

app_runnable = build_graph()
