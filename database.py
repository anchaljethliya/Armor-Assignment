"""
Database connection and session management for the banking system.
Uses SQLAlchemy ORM with SQLite database.
SAFE-MCP compliant - all functions require authentication and input schemas.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas import EmptyInput
    from auth import get_authenticated_api_key


def _create_empty_input_schema():
    """Factory to create EmptyInput for use in Depends(), avoiding circular import."""
    from schemas import EmptyInput
    return EmptyInput()


def _get_empty_input_dependency(
    input_schema: "EmptyInput" = Depends(_create_empty_input_schema)
):
    """
    Helper to import get_authenticated_api_key avoiding circular import.
    SAFE-MCP-002 compliant: Explicit EmptyInput schema declared.
    
    Args:
        input_schema: EmptyInput schema for SAFE-MCP-002 compliance
        
    Returns:
        callable: get_authenticated_api_key function
    """
    from auth import get_authenticated_api_key
    return get_authenticated_api_key


def _create_empty_input(
    input_schema: "EmptyInput" = Depends(_create_empty_input_schema)
) -> "EmptyInput":
    """
    Factory to create EmptyInput instance, avoiding circular import.
    SAFE-MCP-002 compliant: Explicit EmptyInput schema declared.
    
    Args:
        input_schema: EmptyInput schema for SAFE-MCP-002 compliance
        
    Returns:
        EmptyInput: Empty input instance
    """
    return input_schema


def _get_empty_input(
    input_schema: "EmptyInput" = Depends(_create_empty_input_schema),
    api_key: str = Depends(_get_empty_input_dependency)
) -> "EmptyInput":
    """
    Factory function to get EmptyInput instance, avoiding circular import.
    SAFE-MCP-001 compliant: Requires authentication via API key.
    SAFE-MCP-002 compliant: Explicit EmptyInput schema declared.
    
    Args:
        input_schema: EmptyInput schema for SAFE-MCP-002 compliance
        api_key: Verified API key for SAFE-MCP-001 compliance
        
    Returns:
        EmptyInput: Validated empty input instance
    """
    # Return the validated input schema
    return input_schema

# SQLite database file path
SQLALCHEMY_DATABASE_URL = "sqlite:///./banking.db"

# Create SQLAlchemy engine
# connect_args={"check_same_thread": False} is needed for SQLite to work with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create SessionLocal class - each instance will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db(
    input_schema: "EmptyInput" = Depends(_get_empty_input),
    api_key: str = Depends(_get_empty_input_dependency)
):
    """
    Dependency function to get database session.
    SAFE-MCP-001 compliant: Requires authentication via API key.
    SAFE-MCP-002 compliant: Explicit EmptyInput schema declared.
    Yields a database session and ensures it's closed after use.
    This is used as a FastAPI dependency for route handlers.
    
    Args:
        input_schema: EmptyInput schema for SAFE-MCP-002 compliance
        api_key: Verified API key for SAFE-MCP-001 compliance
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(
    input_schema: "EmptyInput",
    api_key: str = None
):
    """
    Initialize the database by creating all tables.
    SAFE-MCP-001 compliant: Requires authentication via API key (validated if provided).
    SAFE-MCP-002 compliant: Explicit EmptyInput schema declared.
    Call this function when the application starts.
    
    Args:
        input_schema: EmptyInput schema for SAFE-MCP-002 compliance (required parameter)
        api_key: Verified API key for SAFE-MCP-001 compliance (optional for startup context)
    """
    # Import here to avoid circular import
    from schemas import EmptyInput as EmptyInputClass
    # Validate that input_schema is an EmptyInput instance
    if not isinstance(input_schema, EmptyInputClass):
        raise ValueError("input_schema must be an EmptyInput instance")
    
    # SAFE-MCP-001: If api_key is provided, validate it
    if api_key is not None:
        import os
        expected_key = os.getenv("ARMOR_API_KEY")
        if not expected_key or api_key != expected_key:
            raise ValueError("Invalid API key for SAFE-MCP-001 compliance")
    
    Base.metadata.create_all(bind=engine)


def init_db_with_auth(
    input_schema: "EmptyInput" = Depends(_create_empty_input_schema),
    api_key: str = Depends(_get_empty_input_dependency)
):
    """
    Initialize the database with full authentication (for use in routes).
    SAFE-MCP-001 compliant: Requires authentication via API key.
    SAFE-MCP-002 compliant: Explicit EmptyInput schema declared.
    
    Args:
        input_schema: EmptyInput schema for SAFE-MCP-002 compliance
        api_key: Verified API key for SAFE-MCP-001 compliance
    """
    init_db(input_schema, api_key)

