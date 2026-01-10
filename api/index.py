"""
Batimove Backend API
FastAPI application for Batimove SaaS platform - Serverless deployment on Vercel
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
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

# Initialize FastAPI app
app = FastAPI(
    title="Batimove API",
    description="Backend API for Batimove Premium Moving Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import after app initialization to avoid circular imports
if DEV_MODE:
    logger.warning("⚠️  Running in DEVELOPMENT MODE with mock database (no Firebase)")
    logger.warning("⚠️  Data will NOT be persisted and will be lost on restart")
    from .mock_db import get_mock_db
else:
    logger.info("Running in PRODUCTION MODE with Firebase")
    from .firebase_config import get_firestore_client

from .models import (
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
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def create_quote(quote_data: QuoteData) -> Union[QuoteResponse, JSONResponse]:
    """
    Create a new quote request.
    
    Validates the quote data and saves it to Firestore or mock database.
    Returns a unique quote ID for reference.
    """
    try:
        # Prepare document data
        quote_dict = quote_data.dict()
        
        if DEV_MODE:
            # Use mock database in development mode
            mock_db = get_mock_db()
            doc_id = mock_db.add_quote(quote_dict)
            logger.info(f"[DEV MODE] Quote created in mock database: {doc_id}")
        else:
            # Use Firebase in production mode
            db = get_firestore_client()
            quote_dict["createdAt"] = datetime.utcnow().isoformat()
            quote_dict["status"] = "pending"
            doc_ref = db.collection("quotes").document()
            doc_ref.set(quote_dict)
            doc_id = doc_ref.id
            logger.info(f"Quote created in Firebase: {doc_id}")
        
        return QuoteResponse(
            success=True,
            quoteId=doc_id,
            message="Votre demande de devis a été enregistrée avec succès. Nous vous contacterons sous 24h.",
        )
        
    except Exception as e:
        logger.error(f"Error creating quote: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                success=False,
                error="Failed to create quote",
                detail=str(e),
            ).dict(),
        )


@app.post(
    "/api/contact",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def create_contact_message(
    contact: ContactMessage,
) -> Union[ContactResponse, JSONResponse]:
    """
    Submit a contact form message.
    
    Saves the message to Firestore or mock database for follow-up.
    """
    try:
        # Prepare document data
        message_dict = contact.dict()
        
        if DEV_MODE:
            # Use mock database in development mode
            mock_db = get_mock_db()
            doc_id = mock_db.add_message(message_dict)
            logger.info(f"[DEV MODE] Contact message created in mock database: {doc_id}")
        else:
            # Use Firebase in production mode
            db = get_firestore_client()
            message_dict["createdAt"] = datetime.utcnow().isoformat()
            message_dict["status"] = "unread"
            doc_ref = db.collection("messages").document()
            doc_ref.set(message_dict)
            doc_id = doc_ref.id
            logger.info(f"Contact message created in Firebase: {doc_id}")
        
        # Optional: Log email simulation
        logger.info(f"[EMAIL SIMULATION] Confirmation sent to {contact.email}")
        
        return ContactResponse(
            success=True,
            messageId=doc_id,
            message="Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.",
        )
        
    except Exception as e:
        logger.error(f"Error creating contact message: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                success=False,
                error="Failed to send message",
                detail=str(e),
            ).dict(),
        )


@app.post(
    "/api/business",
    response_model=BusinessResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def create_business_lead(
    business_lead: BusinessLead,
) -> Union[BusinessResponse, JSONResponse]:
    """
    Capture B2B lead from "Sur Mesure" modal.
    
    Saves business inquiry to Firestore or mock database for sales team follow-up.
    """
    try:
        # Prepare document data
        lead_dict = business_lead.dict()
        
        if DEV_MODE:
            # Use mock database in development mode
            mock_db = get_mock_db()
            doc_id = mock_db.add_business_lead(lead_dict)
            logger.info(f"[DEV MODE] Business lead created in mock database: {doc_id}")
        else:
            # Use Firebase in production mode
            db = get_firestore_client()
            lead_dict["createdAt"] = datetime.utcnow().isoformat()
            lead_dict["status"] = "new"
            lead_dict["leadType"] = "b2b"
            doc_ref = db.collection("business_leads").document()
            doc_ref.set(lead_dict)
            doc_id = doc_ref.id
            logger.info(f"Business lead created in Firebase: {doc_id}")
        
        return BusinessResponse(
            success=True,
            leadId=doc_id,
            message="Merci pour votre intérêt. Notre équipe commerciale vous contactera sous 48h pour discuter de vos besoins.",
        )
        
    except Exception as e:
        logger.error(f"Error creating business lead: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                success=False,
                error="Failed to submit business inquiry",
                detail=str(e),
            ).dict(),
        )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error=exc.detail,
        ).dict(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            success=False,
            error="Internal server error",
            detail=str(exc) if os.getenv("DEBUG") else None,
        ).dict(),
    )


# For Vercel serverless deployment
handler = app
