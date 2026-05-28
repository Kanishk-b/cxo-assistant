from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.agent.workflows.graph import build_graph
from app.db.database import get_db
from app.db.models import SavedBriefing
from app.schemas.briefing import MorningBriefing # 👈 Pointing to your existing file

router = APIRouter()

@router.get("/morning-briefing")
async def get_morning_briefing(db: Session = Depends(get_db)):
    print("🌐 API Hit: Triggering LangGraph Orchestrator...")
    
    blank_state = {
        "raw_emails": [],
        "raw_meetings": [],
        "safe_emails": [],
        "morning_briefing": None,
        "error_message": None
    }
    
    app = build_graph()
    final_state = app.invoke(blank_state)
    briefing_data = final_state["morning_briefing"]
    
    print("💾 Saving briefing to PostgreSQL vault...")
    db_briefing = SavedBriefing(
        shape_of_the_day=briefing_data.shape_of_the_day,
        critical_attention_items=briefing_data.critical_attention_items,
        open_commitments=[item.model_dump() for item in briefing_data.open_commitments],
        pre_meeting_flags=briefing_data.pre_meeting_flags
    )
    
    db.add(db_briefing)
    db.commit()
    db.refresh(db_briefing)
    print(f"✅ Briefing saved with ID: {db_briefing.id}")
    
    return {"status": "success", "data": final_state["morning_briefing"]}