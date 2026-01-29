from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from uuid import uuid4
from datetime import datetime

app = FastAPI(title="Chatbot Lead Capture API")


class LeadRequest(BaseModel):
    is_owner: bool
    speciality: Optional[str] = None
    city: str
    full_name: str
    website: Optional[HttpUrl] = None
    preferred_contact_time: Optional[str] = None
    
    monthly_appointments: Optional[int] = Field(
        None, description="How many appointments can your clinic handle in a month?"
    )
    average_ticket_size: Optional[float] = Field(
        None, description="What is your average ticket size (treatment cost)?"
    )
    ad_budget: Optional[float] = Field(
        None, description="How much are you ready to invest in advertisements for acquiring new patients?"
    )

    # New field
    implementation_timeline: Optional[str] = Field(
        None, description="How soon would you like to begin implementing the digital patient acquisition solution to start generating new patients?"
    )


class LeadResponse(BaseModel):
    success: bool
    message: str
    lead_id: str
    timestamp: datetime


@app.post("/api/chatbot/lead", response_model=LeadResponse)
def create_lead(lead: LeadRequest):
    if not lead.full_name.strip():
        raise HTTPException(status_code=400, detail="Full name is required")

    if not lead.city.strip():
        raise HTTPException(status_code=400, detail="City is required")

    lead_id = str(uuid4())

    print({
        "lead_id": lead_id,
        "data": lead.dict(),
        "created_at": datetime.utcnow()
    })

    return LeadResponse(
        success=True,
        message="Lead captured successfully",
        lead_id=lead_id,
        timestamp=datetime.utcnow()
    )
