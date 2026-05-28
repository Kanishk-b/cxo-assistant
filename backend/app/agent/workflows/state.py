from typing import TypedDict, List
from app.schemas.email import EmailForAgent
from app.schemas.calendar import CalendarEventForAgent
from app.schemas.briefing import MorningBriefing

class AgentState(TypedDict):
    """
    This is the exact 'memory' the AI uses as it moves through its workflow.
    It starts empty, and each node in the graph fills in a piece of the puzzle.
    """
    # 1. The raw data fetched from Microsoft (or our Mock Service)
    raw_emails: List[EmailForAgent]
    raw_meetings: List[CalendarEventForAgent]
    
    # 2. The filtered data (after we strip out M&A, HR, etc.)
    safe_emails: List[EmailForAgent]
    
    # 3. The final generated output
    morning_briefing: MorningBriefing | None
    
    # 4. Any errors that occur during the process
    error_message: str | None