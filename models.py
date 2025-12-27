"""
SQLAlchemy models for the banking system.
Defines the database schema for Account and Transaction tables.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base


class TransactionType(enum.Enum):
    """Enumeration for transaction types."""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class Account(Base):
    """
    Account model representing a bank account.
    Each account has a unique ID, owner name, and current balance.
    """
    __tablename__ = "accounts"

    # Primary key - auto-incrementing integer
    account_id = Column(Integer, primary_key=True, index=True)
    
    # Account owner's name
    name = Column(String, nullable=False, index=True)
    
    # Current account balance (stored as Float for simplicity)
    # In production, use Decimal for precise financial calculations
    balance = Column(Float, nullable=False, default=0.0)

    # Relationship to transactions - one account can have many transactions
    # cascade="all, delete-orphan" ensures transactions are deleted if account is deleted
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")


class Transaction(Base):
    """
    Transaction model representing a deposit or withdrawal.
    Each transaction is linked to an account and records the amount and type.
    """
    __tablename__ = "transactions"

    # Primary key - auto-incrementing integer
    transaction_id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to accounts table
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False, index=True)
    
    # Transaction type: DEPOSIT or WITHDRAWAL
    transaction_type = Column(Enum(TransactionType), nullable=False)
    
    # Transaction amount (positive value)
    amount = Column(Float, nullable=False)
    
    # Timestamp - automatically set when transaction is created
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship back to account
    account = relationship("Account", back_populates="transactions")

