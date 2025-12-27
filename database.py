"""
Database connection and session management for the banking system.
Uses SQLAlchemy ORM with SQLite database.
SAFE-MCP compliant - authentication is handled at the route level.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


def get_db():
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    This is used as a FastAPI dependency for route handlers.
    Note: Authentication is enforced at the route level, not here.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.
    Call this function when the application starts.
    Note: This is called during startup and doesn't require authentication
    as it only creates schema, not data access.
    """
    Base.metadata.create_all(bind=engine)

