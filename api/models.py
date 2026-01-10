"""
Pydantic Models for Request Validation
Mirrors the TypeScript interfaces from the frontend.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class ContactInfo(BaseModel):
    """Contact information model"""
    name: str = Field(..., min_length=1, max_length=100, description="Contact name")
    email: EmailStr = Field(..., description="Contact email address")
    phone: str = Field(..., min_length=8, max_length=20, description="Contact phone number")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format"""
        # Remove common separators
        cleaned = v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not cleaned.replace('+', '').isdigit():
            raise ValueError('Phone number must contain only digits and optional + prefix')
        return v


class QuoteData(BaseModel):
    """Quote request data model - mirrors frontend QuoteData interface"""
    serviceId: str = Field(..., description="Service identifier")
    date: str = Field(..., description="Preferred service date")
    contact: ContactInfo = Field(..., description="Contact information")
    
    # Optional fields based on service type
    fromZip: Optional[str] = Field(None, max_length=10, description="Origin postal code")
    toZip: Optional[str] = Field(None, max_length=10, description="Destination postal code")
    volume: Optional[int] = Field(None, ge=0, description="Volume in cubic meters")
    rooms: Optional[float] = Field(None, ge=0, description="Number of rooms (can be decimal like 2.5)")
    housingType: Optional[str] = Field(None, max_length=50, description="Type of housing")
    surface: Optional[int] = Field(None, ge=0, description="Surface area in square meters")
    duration: Optional[str] = Field(None, description="Service duration")
    floor: Optional[int] = Field(None, ge=0, le=100, description="Floor number")
    
    @validator('serviceId')
    def validate_service_id(cls, v):
        """Validate service ID matches frontend options"""
        valid_ids = ['priv', 'pro', 'clean', 'storage', 'lift', 'inter', 'general']
        if v not in valid_ids:
            raise ValueError(f'Invalid service ID. Must be one of: {", ".join(valid_ids)}')
        return v
    
    @validator('date')
    def validate_date(cls, v):
        """Validate date format"""
        try:
            # Try to parse the date to ensure it's valid
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError('Invalid date format. Expected ISO 8601 format')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "serviceId": "demenagement",
                "date": "2026-02-15T10:00:00Z",
                "contact": {
                    "name": "Jean Dupont",
                    "email": "jean.dupont@example.com",
                    "phone": "+33612345678"
                },
                "fromZip": "75001",
                "toZip": "75015",
                "rooms": 3,
                "volume": 45,
                "floor": 2
            }
        }


class ContactMessage(BaseModel):
    """Contact form message model"""
    name: str = Field(..., min_length=1, max_length=100, description="Sender name")
    email: EmailStr = Field(..., description="Sender email address")
    subject: str = Field(..., min_length=1, max_length=200, description="Message subject")
    message: str = Field(..., min_length=10, max_length=2000, description="Message content")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Marie Martin",
                "email": "marie.martin@example.com",
                "subject": "Question sur les services",
                "message": "Bonjour, j'aimerais avoir plus d'informations sur vos services de déménagement premium."
            }
        }


class BusinessLead(BaseModel):
    """B2B lead capture model"""
    companyName: str = Field(..., min_length=1, max_length=200, description="Company name")
    contactName: str = Field(..., min_length=1, max_length=100, description="Contact person name")
    email: EmailStr = Field(..., description="Business email address")
    phone: str = Field(..., min_length=8, max_length=20, description="Contact phone number")
    employeeCount: Optional[str] = Field(None, description="Number of employees")
    serviceNeeds: str = Field(..., min_length=10, max_length=1000, description="Description of service needs")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format"""
        cleaned = v.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not cleaned.replace('+', '').isdigit():
            raise ValueError('Phone number must contain only digits and optional + prefix')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "companyName": "TechCorp SAS",
                "contactName": "Pierre Dubois",
                "email": "p.dubois@techcorp.fr",
                "phone": "+33612345678",
                "employeeCount": "50-100",
                "serviceNeeds": "Nous recherchons un partenaire pour gérer les déménagements de nos employés."
            }
        }


class QuoteResponse(BaseModel):
    """Response model for quote submission"""
    success: bool
    quoteId: str
    message: str


class ContactResponse(BaseModel):
    """Response model for contact submission"""
    success: bool
    messageId: str
    message: str


class BusinessResponse(BaseModel):
    """Response model for business lead"""
    success: bool
    leadId: str
    message: str


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    detail: Optional[str] = None
