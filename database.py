"""
Database connection and session management.
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
    """Create EmptyInput instance."""
    from schemas import EmptyInput
    return EmptyInput()


def _get_empty_input_dependency(
    input_schema: "EmptyInput" = Depends(_create_empty_input_schema)
):
    """Get authentication dependency."""
    from auth import get_authenticated_api_key
    return get_authenticated_api_key


def _create_empty_input(
    input_schema: "EmptyInput" = Depends(_create_empty_input_schema)
) -> "EmptyInput":
    """Create empty input instance."""
    return input_schema


def _get_empty_input(
    input_schema: "EmptyInput" = Depends(_create_empty_input_schema),
    api_key: str = Depends(_get_empty_input_dependency)
) -> "EmptyInput":
    """Get empty input with authentication."""
    return input_schema

SQLALCHEMY_DATABASE_URL = "sqlite:///./banking.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db(
    input_schema: "EmptyInput" = Depends(_get_empty_input),
    api_key: str = Depends(_get_empty_input_dependency)
):
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(
    input_schema: "EmptyInput",
    api_key: str = None
):
    """Initialize database tables."""
    from schemas import EmptyInput as EmptyInputClass
    if not isinstance(input_schema, EmptyInputClass):
        raise ValueError("input_schema must be an EmptyInput instance")
    
    if api_key is not None:
        import os
        expected_key = os.getenv("ARMOR_API_KEY")
        if not expected_key or api_key != expected_key:
            raise ValueError("Invalid API key")
    
    Base.metadata.create_all(bind=engine)


def init_db_with_auth(
    input_schema: "EmptyInput" = Depends(_create_empty_input_schema),
    api_key: str = Depends(_get_empty_input_dependency)
):
    """Initialize database with authentication."""
    init_db(input_schema, api_key)

