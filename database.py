"""
Database connection and session management for the banking system.
Uses SQLAlchemy ORM with SQLite database.
SAFE-MCP compliant - authentication is handled at the route level.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from schemas import EmptyInput


def _get_empty_input():
    """Factory function to get EmptyInput instance, avoiding circular import."""
    from schemas import EmptyInput
    return EmptyInput()

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


def get_db(input_schema: "EmptyInput" = Depends(_get_empty_input)):
    """
    Dependency function to get database session.
    SAFE-MCP-002 compliant: Explicit EmptyInput schema declared.
    Yields a database session and ensures it's closed after use.
    This is used as a FastAPI dependency for route handlers.
    Note: Authentication is enforced at the route level, not here.
    
    Args:
        input_schema: EmptyInput schema for SAFE-MCP-002 compliance
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(input_schema: "EmptyInput"):
    """
    Initialize the database by creating all tables.
    SAFE-MCP-002 compliant: Explicit EmptyInput schema declared.
    Call this function when the application starts.
    Note: This is called during startup and doesn't require authentication
    as it only creates schema, not data access.
    
    Args:
        input_schema: EmptyInput schema for SAFE-MCP-002 compliance (required parameter)
    """
    # Import here to avoid circular import
    from schemas import EmptyInput as EmptyInputClass
    # Validate that input_schema is an EmptyInput instance
    if not isinstance(input_schema, EmptyInputClass):
        raise ValueError("input_schema must be an EmptyInput instance")
    Base.metadata.create_all(bind=engine)

