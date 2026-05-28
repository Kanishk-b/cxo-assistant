from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class Attendee(BaseModel):
    name: str
    email: str

class CalendarEventForAgent(BaseModel):
    """
    The strict representation of a meeting for the Morning Briefing.
    """
    title: str = Field(..., description="Title of the calendar event")
    start_time: datetime
    end_time: datetime
    organizer: str
    attendees: List[Attendee] = []
    is_out_of_hours: bool = Field(default=False, description="Flagged for auto-decline if outside working hours")