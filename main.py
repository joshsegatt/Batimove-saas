"""
Batimove Backend API
FastAPI application for Batimove SaaS platform
"""

import os
from datetime import datetime
from typing import Union
import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if running in development mode (no Firebase)
DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"

if DEV_MODE:
    logger.warning("⚠️  Running in DEVELOPMENT MODE with mock database (no Firebase)")
    logger.warning("⚠️  Data will NOT be persisted and will be lost on restart")

# Initialize FastAPI app
app = FastAPI(
    title="Batimove API",
    description="Backend API for Batimove Premium Moving Platform",
    version="1.0.0",
)

# Configure CORS - Allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import models after app initialization
from api.models import (
    QuoteData,
    ContactMessage,
    BusinessLead,
    QuoteResponse,
    ContactResponse,
    BusinessResponse,
    ErrorResponse,
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Batimove API is running",
        "version": "1.0.0",
        "status": "healthy",
        "mode": "development" if DEV_MODE else "production"
    }


@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "message": "Batimove API",
        "endpoints": {
            "quote": "/api/quote",
            "contact": "/api/contact",
            "business": "/api/business",
        },
    }


@app.post(
    "/api/quote",
    response_model=QuoteResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_quote(quote_data: QuoteData) -> Union[QuoteResponse, JSONResponse]:
    """Create a new quote request"""
    try:
        from api.mock_db import get_mock_db
        
        quote_dict = quote_data.dict()
        mock_db = get_mock_db()
        doc_id = mock_db.add_quote(quote_dict)
        logger.info(f"[DEV MODE] Quote created: {doc_id}")
        
        return QuoteResponse(
            success=True,
            quoteId=doc_id,
            message="Votre demande de devis a été enregistrée avec succès. Nous vous contacterons sous 24h.",
        )
    except Exception as e:
        logger.error(f"Error creating quote: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "error": str(e)},
        )


@app.post(
    "/api/contact",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact_message(contact: ContactMessage) -> Union[ContactResponse, JSONResponse]:
    """Submit a contact form message"""
    try:
        from api.mock_db import get_mock_db
        
        message_dict = contact.dict()
        mock_db = get_mock_db()
        doc_id = mock_db.add_message(message_dict)
        logger.info(f"[DEV MODE] Contact message created: {doc_id}")
        
        return ContactResponse(
            success=True,
            messageId=doc_id,
            message="Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.",
        )
    except Exception as e:
        logger.error(f"Error creating contact message: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "error": str(e)},
        )


@app.post(
    "/api/business",
    response_model=BusinessResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_business_lead(business_lead: BusinessLead) -> Union[BusinessResponse, JSONResponse]:
    """Capture B2B lead"""
    try:
        from api.mock_db import get_mock_db
        
        lead_dict = business_lead.dict()
        mock_db = get_mock_db()
        doc_id = mock_db.add_business_lead(lead_dict)
        logger.info(f"[DEV MODE] Business lead created: {doc_id}")
        
        return BusinessResponse(
            success=True,
            leadId=doc_id,
            message="Merci pour votre intérêt. Notre équipe commerciale vous contactera sous 48h.",
        )
    except Exception as e:
        logger.error(f"Error creating business lead: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "error": str(e)},
        )


# Vercel/Railway handler
handler = app
