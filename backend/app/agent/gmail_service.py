import os
import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from dotenv import load_dotenv
from app.schemas.email import EmailForAgent

# ⚠️ REPLACE THESE WITH YOUR CREDENTIALS FOR THE TEST
GMAIL_USER = "kanishk15bansal@gmail.com"
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def fetch_live_gmails(limit: int = 5) -> list[EmailForAgent]:
    print("📡 Connecting to live Gmail inbox...")
    emails_for_agent = []
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL") # Let's just grab Unread emails!
        email_ids = messages[0].split()
        latest_email_ids = email_ids[-limit:] 

        for e_id in reversed(latest_email_ids):
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # 1. Decode the subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                        
                    # 2. Extract Sender
                    sender_raw = msg.get("From", "Unknown Sender")
                    
                    # 3. Extract and format the Date
                    date_raw = msg.get("Date")
                    try:
                        received_date = parsedate_to_datetime(date_raw).isoformat()
                    except:
                        received_date = datetime.now(timezone.utc).isoformat()
                    
                    # 4. Extract Body
                    body = "No text content found."
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                try:
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                    break 
                                except:
                                    continue
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    # 5. SATISFY PYDANTIC STRICTLY
                    safe_email = EmailForAgent(
                        id=f"gmail_{e_id.decode()}",
                        sender=sender_raw[:50], 
                        sender_email=sender_raw[:100],     # Added missing field
                        subject=subject[:100],
                        body=body[:500],
                        body_preview=body[:100],           # Added missing field
                        received_datetime=received_date,   # Added missing field
                        importance="Normal",
                        is_confidential=False 
                    )
                    emails_for_agent.append(safe_email)

        mail.logout()
        print(f"✅ Successfully fetched and validated {len(emails_for_agent)} live emails!")
        return emails_for_agent

    except Exception as e:
        print(f"❌ Failed to fetch Gmail: {e}")
        return []