from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EmailBase(BaseModel):
    subject: str = Field(..., description="The subject line of the email")
    sender_email: str = Field(..., description="The email address of the sender")
    sender_name: Optional[str] = Field(None, description="The display name of the sender")
    received_datetime: datetime = Field(..., description="When the email was received")
    
class EmailForAgent(EmailBase):
    """
    This is the stripped-down model that the LangGraph agent will actually read.
    Notice we only allow a 500-character body preview to save on LLM token costs.
    """
    body_preview: str = Field(..., max_length=500, description="A truncated preview of the email body")
    is_flagged_confidential: bool = Field(default=False, description="True if the pre-filter caught M&A/HR keywords")