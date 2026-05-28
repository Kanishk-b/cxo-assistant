from app.agent.workflows.graph import build_graph

def run_test():
    print("🤖 Booting up LangGraph Orchestrator...")
    
    blank_state = {
        "raw_emails": [],
        "raw_meetings": [],
        "safe_emails": [],
        "morning_briefing": None,
        "error_message": None
    }
    
    app = build_graph()
    final_state = app.invoke(blank_state)
    
    print("\n✅ Full Graph Execution Complete!")
    print("=" * 40)
    print("📊 FINAL MORNING BRIEFING OUTPUT")
    print("=" * 40)
    
    briefing = final_state['morning_briefing']
    
    print(f"🌅 Shape of the Day:\n  {briefing.shape_of_the_day}\n")
    print("🔥 Critical Attention Items:")
    for item in briefing.critical_attention_items:
        print(f"  - {item}")
        
    print("\n📝 Open Commitments:")
    for task in briefing.open_commitments:
        print(f"  - [{task.urgency}] {task.task}")

if __name__ == "__main__":
    run_test()