import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from app.agent.workflows.state import AgentState
from app.schemas.briefing import MorningBriefing

# Load the secret key from the .env file
load_dotenv()

def draft_morning_briefing(state: AgentState):
    print("🧠 Waking up Claude 4.5 Haiku...")
    
    # 1. Initialize the LLM Engine (Set to Haiku as instructed)
    llm = ChatAnthropic(
        model_name="claude-haiku-4-5-20251001",
        temperature=0.1, # Keep it low so the AI is highly analytical, not creative
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    
    # 2. Force the AI to output our strict Pydantic model
    structured_llm = llm.with_structured_output(MorningBriefing)
    
    # 3. Build the System Prompt
    system_instructions = """
    You are an elite, highly analytical Chief of Staff. 
    Your job is to read the executive's upcoming meetings and safe, filtered emails, and generate a concise morning briefing.
    Extract any highly urgent tasks into 'critical_attention_items'.
    Extract outstanding promises or tasks into 'open_commitments'.
    Provide a 2-3 sentence overview of the day in 'shape_of_the_day'.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_instructions),
        ("human", "Here is my data for today.\n\nMeetings: {meetings}\n\nEmails: {emails}")
    ])
    
    # 4. Connect the pipes and trigger the AI
    chain = prompt | structured_llm
    
    print("⏳ Claude is reading the inbox and drafting the briefing...")
    final_briefing = chain.invoke({
        "meetings": state["raw_meetings"],
        "emails": state["safe_emails"]
    })
    
    print("✅ Claude has finished the briefing!")
    
    return {"morning_briefing": final_briefing}