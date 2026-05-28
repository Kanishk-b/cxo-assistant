from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import briefing

# Initialize the web server
app = FastAPI(title="CXO Assistant API", version="0.1.0")

# SECURITY: Allow the Next.js frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect our briefing route to the main app
app.include_router(briefing.router, prefix="/api/v1", tags=["Briefing"])

@app.get("/")
def read_root():
    return {"message": "CXO Assistant Backend is running."}