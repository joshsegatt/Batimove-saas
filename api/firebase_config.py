"""
Firebase Configuration Module
Initializes Firebase Admin SDK using environment variables for secure credential management.
"""

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from typing import Optional

# Global Firestore client
_db: Optional[firestore.Client] = None


def initialize_firebase() -> firestore.Client:
    """
    Initialize Firebase Admin SDK and return Firestore client.
    
    Uses FIREBASE_CREDENTIALS environment variable containing the service account JSON.
    Falls back to FIREBASE_PROJECT_ID for local development.
    
    Returns:
        firestore.Client: Initialized Firestore database client
        
    Raises:
        ValueError: If Firebase credentials are not properly configured
    """
    global _db
    
    # Return existing client if already initialized
    if _db is not None:
        return _db
    
    try:
        # Check if Firebase app is already initialized
        if not firebase_admin._apps:
            # Try to get credentials from environment variable
            firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
            
            if firebase_creds:
                # Parse JSON credentials from environment variable
                cred_dict = json.loads(firebase_creds)
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            else:
                # Fallback: Use project ID for local development (requires gcloud auth)
                project_id = os.getenv("FIREBASE_PROJECT_ID")
                if not project_id:
                    raise ValueError(
                        "Firebase credentials not found. Set FIREBASE_CREDENTIALS or FIREBASE_PROJECT_ID environment variable."
                    )
                
                # Initialize with project ID (uses Application Default Credentials)
                firebase_admin.initialize_app(
                    options={"projectId": project_id}
                )
        
        # Initialize and cache Firestore client
        _db = firestore.client()
        return _db
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in FIREBASE_CREDENTIALS: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to initialize Firebase: {str(e)}")


def get_firestore_client() -> firestore.Client:
    """
    Get the Firestore client instance.
    
    Returns:
        firestore.Client: Firestore database client
    """
    if _db is None:
        return initialize_firebase()
    return _db
