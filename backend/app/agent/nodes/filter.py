from app.agent.workflows.state import AgentState

def filter_confidential_data(state: AgentState) -> dict:
    """
    Node 2: The Security Guardrail.
    This iterates through the raw data and drops anything flagged as confidential
    before the LLM ever gets a chance to look at it.
    """
    print("-> Running Confidentiality Filter...")
    
    safe_emails = []
    
    for email in state["raw_emails"]:
        if email.is_flagged_confidential:
            print(f"   🚨 [BLOCKED] Sensitive content detected: '{email.subject}'")
        else:
            safe_emails.append(email)
            
    # LangGraph automatically takes this dictionary and updates the state memory
    return {
        "safe_emails": safe_emails
    }