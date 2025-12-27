"""
Pydantic schemas for request/response validation.
Defines the data structures for API requests and responses.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from models import TransactionType


# Request schemas
class AccountCreate(BaseModel):
    """Schema for creating a new account."""
    name: str = Field(..., min_length=1, max_length=100, description="Account owner's name")
    initial_balance: float = Field(..., ge=0, description="Initial account balance (must be >= 0)")


class DepositRequest(BaseModel):
    """Schema for deposit request."""
    account_id: int = Field(..., gt=0, description="Account ID to deposit into")
    amount: float = Field(..., gt=0, description="Amount to deposit (must be > 0)")


class WithdrawRequest(BaseModel):
    """Schema for withdrawal request."""
    account_id: int = Field(..., gt=0, description="Account ID to withdraw from")
    amount: float = Field(..., gt=0, description="Amount to withdraw (must be > 0)")


# Response schemas
class AccountResponse(BaseModel):
    """Schema for account information response."""
    account_id: int
    name: str
    balance: float

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models


class TransactionResponse(BaseModel):
    """Schema for transaction information response."""
    transaction_id: int
    account_id: int
    transaction_type: TransactionType
    amount: float
    timestamp: datetime

    class Config:
        from_attributes = True


class BalanceResponse(BaseModel):
    """Schema for balance inquiry response."""
    account_id: int
    balance: float
    name: str


class TransactionHistoryResponse(BaseModel):
    """Schema for transaction history response."""
    account_id: int
    transactions: List[TransactionResponse]
    total_transactions: int

