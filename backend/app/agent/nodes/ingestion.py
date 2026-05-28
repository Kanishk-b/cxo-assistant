from app.agent.workflows.state import AgentState
from app.agent.gmail_service import fetch_live_gmails

def fetch_user_data(state: AgentState):
    print("Node 1: Fetching LIVE data from Gmail...")
    
    # 🔌 We are bypassing the Mock data and calling our live Gmail adapter!
    live_emails = fetch_live_gmails(limit=5)
    
    # For testing, we will just use an empty list for meetings to focus on the emails
    mock_meetings = []
    
    # We return the live emails into the LangGraph state memory
    return {"raw_emails": live_emails, "raw_meetings": mock_meetings}