from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime, timezone
from app.db.database import Base

class SavedBriefing(Base):
    __tablename__ = "morning_briefings"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # We store the high-level summary as text
    shape_of_the_day = Column(Text)
    
    # We can store the lists of action items as JSON arrays so they are easy to retrieve
    critical_attention_items = Column(JSON)
    open_commitments = Column(JSON)
    pre_meeting_flags = Column(JSON)