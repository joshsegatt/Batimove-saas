"""
Batimove Backend API
FastAPI application for Batimove SaaS platform
"""

import os
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Simple in-memory database
class MockDB:
    def __init__(self):
        self.quotes = {}
        self.messages = {}
        self.leads = {}
    
    def add_quote(self, data):
        id = str(uuid.uuid4())
        self.quotes[id] = {**data, "createdAt": datetime.utcnow().isoformat()}
        return id
    
    def add_message(self, data):
        id = str(uuid.uuid4())
        self.messages[id] = {**data, "createdAt": datetime.utcnow().isoformat()}
        return id
    
    def add_lead(self, data):
        id = str(uuid.uuid4())
        self.leads[id] = {**data, "createdAt": datetime.utcnow().isoformat()}
        return id

db = MockDB()

# Models
class ContactInfo(BaseModel):
    name: str
    email: EmailStr
    phone: str

class QuoteData(BaseModel):
    serviceId: str
    date: str
    contact: ContactInfo
    fromZip: Optional[str] = None
    toZip: Optional[str] = None
    volume: Optional[int] = None
    rooms: Optional[float] = None
    housingType: Optional[str] = None
    surface: Optional[int] = None
    duration: Optional[str] = None
    floor: Optional[int] = None

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class BusinessLead(BaseModel):
    companyName: str
    contactName: str
    email: EmailStr
    phone: str
    employeeCount: Optional[str] = None
    serviceNeeds: str

# Initialize FastAPI
app = FastAPI(title="Batimove API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Batimove API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/api")
async def api_root():
    return {
        "message": "Batimove API",
        "endpoints": {
            "quote": "/api/quote",
            "contact": "/api/contact",
            "business": "/api/business"
        }
    }

@app.post("/api/quote", status_code=status.HTTP_201_CREATED)
async def create_quote(quote_data: QuoteData):
    try:
        doc_id = db.add_quote(quote_data.dict())
        return {
            "success": True,
            "quoteId": doc_id,
            "message": "Votre demande de devis a été enregistrée avec succès."
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/contact", status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactMessage):
    try:
        doc_id = db.add_message(contact.dict())
        return {
            "success": True,
            "messageId": doc_id,
            "message": "Votre message a été envoyé avec succès."
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/business", status_code=status.HTTP_201_CREATED)
async def create_business(business_lead: BusinessLead):
    try:
        doc_id = db.add_lead(business_lead.dict())
        return {
            "success": True,
            "leadId": doc_id,
            "message": "Merci pour votre intérêt. Notre équipe vous contactera sous 48h."
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

handler = app
