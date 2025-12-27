"""
Authentication module for SAFE-MCP compliance.
Implements API key-based authentication using X-API-Key header.
"""

import os
from fastapi import Header, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional

# API Key header name
API_KEY_HEADER = "X-API-Key"

# Get API key from environment variable
ARMOR_API_KEY = os.getenv("ARMOR_API_KEY")

# API Key Header dependency
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


def verify_api_key(api_key: Optional[str] = Header(None, alias=API_KEY_HEADER)) -> str:
    """
    Verify API key from X-API-Key header.
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        str: The verified API key
        
    Raises:
        HTTPException: 401 if API key is missing or invalid
    """
    # Check if ARMOR_API_KEY is configured
    if not ARMOR_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key not configured on server"
        )
    
    # Check if API key is provided
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Please provide X-API-Key header"
        )
    
    # Verify API key matches
    if api_key != ARMOR_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return api_key


def get_authenticated_api_key(api_key: Optional[str] = Header(None, alias=API_KEY_HEADER)) -> str:
    """
    Dependency function for FastAPI to verify API key.
    Can be used as a dependency in route handlers.
    
    Usage:
        @app.get("/endpoint")
        async def my_endpoint(api_key: str = Depends(get_authenticated_api_key)):
            ...
    """
    return verify_api_key(api_key)

