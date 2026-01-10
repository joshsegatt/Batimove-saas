"""
Mock Database for Development
In-memory storage for prototyping without Firebase
"""

from datetime import datetime
from typing import Dict, List
import uuid


class MockDatabase:
    """In-memory database for development/prototyping"""
    
    def __init__(self):
        self.quotes: Dict[str, dict] = {}
        self.messages: Dict[str, dict] = {}
        self.business_leads: Dict[str, dict] = {}
    
    def add_quote(self, data: dict) -> str:
        """Add a quote and return its ID"""
        quote_id = str(uuid.uuid4())
        self.quotes[quote_id] = {
            **data,
            "createdAt": datetime.utcnow().isoformat(),
            "status": "pending"
        }
        return quote_id
    
    def add_message(self, data: dict) -> str:
        """Add a contact message and return its ID"""
        message_id = str(uuid.uuid4())
        self.messages[message_id] = {
            **data,
            "createdAt": datetime.utcnow().isoformat(),
            "status": "unread"
        }
        return message_id
    
    def add_business_lead(self, data: dict) -> str:
        """Add a business lead and return its ID"""
        lead_id = str(uuid.uuid4())
        self.business_leads[lead_id] = {
            **data,
            "createdAt": datetime.utcnow().isoformat(),
            "status": "new",
            "leadType": "b2b"
        }
        return lead_id
    
    def get_all_quotes(self) -> List[dict]:
        """Get all quotes (for debugging)"""
        return list(self.quotes.values())
    
    def get_all_messages(self) -> List[dict]:
        """Get all messages (for debugging)"""
        return list(self.messages.values())
    
    def get_all_business_leads(self) -> List[dict]:
        """Get all business leads (for debugging)"""
        return list(self.business_leads.values())


# Global mock database instance
_mock_db = MockDatabase()


def get_mock_db() -> MockDatabase:
    """Get the mock database instance"""
    return _mock_db
