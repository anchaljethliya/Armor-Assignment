"""
API key authentication.
"""

import os
from fastapi import Header, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional

API_KEY_HEADER = "X-API-Key"
ARMOR_API_KEY = os.getenv("ARMOR_API_KEY")
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


def verify_api_key(api_key: Optional[str] = Header(None, alias=API_KEY_HEADER)) -> str:
    """Verify API key from header."""
    if not ARMOR_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key not configured on server"
        )
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Please provide X-API-Key header"
        )
    
    if api_key != ARMOR_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return api_key


def get_authenticated_api_key(api_key: Optional[str] = Header(None, alias=API_KEY_HEADER)) -> str:
    """FastAPI dependency to verify API key."""
    return verify_api_key(api_key)

