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

    account_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    balance = Column(Float, nullable=False, default=0.0)
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")


class Transaction(Base):
    """
    Transaction model representing a deposit or withdrawal.
    Each transaction is linked to an account and records the amount and type.
    """
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False, index=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    account = relationship("Account", back_populates="transactions")

