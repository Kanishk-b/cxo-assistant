from datetime import datetime, timedelta
from typing import List

# Importing the schemas you just created!
from app.schemas.email import EmailForAgent
from app.schemas.calendar import CalendarEventForAgent, Attendee

class MockGraphService:
    """
    A temporary service to generate fake Microsoft 365 data 
    until IT provisions the Azure Entra ID credentials.
    """

    @staticmethod
    def get_recent_emails() -> List[EmailForAgent]:
        now = datetime.now()
        return [
            EmailForAgent(
                subject="Q3 Marketing Budget Approval",
                sender_email="cmo@company.com",
                sender_name="Sarah Jenkins (CMO)",
                received_datetime=now - timedelta(hours=2),
                body_preview="Hi, please review the attached Q3 budget. We need sign-off by EOD tomorrow so we can finalize the ad spend.",
                is_flagged_confidential=False
            ),
            EmailForAgent(
                subject="Project Titan (M&A) - STRICTLY CONFIDENTIAL",
                sender_email="legal@company.com",
                sender_name="Legal Team",
                received_datetime=now - timedelta(hours=4),
                body_preview="Attached is the term sheet for the acquisition. Do not forward.",
                is_flagged_confidential=True # Our AI filter should catch and ignore this!
            ),
            EmailForAgent(
                subject="FYI: Server migration complete",
                sender_email="it.ops@company.com",
                sender_name="IT Operations",
                received_datetime=now - timedelta(hours=12),
                body_preview="Just a heads up that the weekend server migration finished with zero downtime. No action needed.",
                is_flagged_confidential=False
            )
        ]

    @staticmethod
    def get_upcoming_meetings() -> List[CalendarEventForAgent]:
        now = datetime.now()
        return [
            CalendarEventForAgent(
                title="Weekly Executive Sync",
                start_time=now + timedelta(hours=1),
                end_time=now + timedelta(hours=2),
                organizer="ceo@company.com",
                attendees=[Attendee(name="You", email="cxo@company.com")],
                is_out_of_hours=False
            ),
            CalendarEventForAgent(
                title="Vendor Pitch: New AI Tooling",
                start_time=now + timedelta(hours=10), # Scheduled for 10 hours from now (likely evening)
                end_time=now + timedelta(hours=11),
                organizer="sales@randomvendor.com",
                attendees=[Attendee(name="You", email="cxo@company.com")],
                is_out_of_hours=True # Our auto-action engine will decline this!
            )
        ]