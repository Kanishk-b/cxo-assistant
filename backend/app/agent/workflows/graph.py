from langgraph.graph import StateGraph, END
from app.agent.workflows.state import AgentState
from app.agent.nodes.ingestion import fetch_user_data
from app.agent.nodes.filter import filter_confidential_data
from app.agent.nodes.drafter import draft_morning_briefing

def build_graph():
    workflow = StateGraph(AgentState)
    
    # 1. Add all three nodes
    workflow.add_node("fetch_data", fetch_user_data)
    workflow.add_node("filter_data", filter_confidential_data)
    workflow.add_node("draft_briefing", draft_morning_briefing) # NEW!
    
    # 2. Define the exact flow of data (The Hallways)
    workflow.set_entry_point("fetch_data")
    workflow.add_edge("fetch_data", "filter_data")
    workflow.add_edge("filter_data", "draft_briefing")          # NEW!
    workflow.add_edge("draft_briefing", END)                    # NEW!
    
    return workflow.compile()