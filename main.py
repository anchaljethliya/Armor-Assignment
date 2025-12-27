"""
Banking system API with FastAPI.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List
from database import get_db, init_db
from models import Account, Transaction, TransactionType
from auth import get_authenticated_api_key
from schemas import (
    AccountCreate,
    AccountResponse,
    DepositRequest,
    WithdrawRequest,
    BalanceResponse,
    TransactionHistoryResponse,
    TransactionResponse,
    EmptyInput,
    BalanceQueryInput,
    TransactionHistoryQueryInput
)


app = FastAPI(
    title="Banking System API",
    description="Banking system API for account management and transactions",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    import os
    api_key = os.getenv("ARMOR_API_KEY")
    if not api_key:
        raise RuntimeError("ARMOR_API_KEY environment variable must be set")
    
    empty_input = EmptyInput()
    init_db(empty_input, api_key=api_key)


@app.get("/", response_model=dict)
async def root(api_key: str = Depends(get_authenticated_api_key)):
    """Root endpoint with API information."""
    return {
        "message": "Banking System API",
        "version": "1.0.0",
        "endpoints": {
            "create_account": "POST /accounts",
            "deposit": "POST /accounts/deposit",
            "withdraw": "POST /accounts/withdraw",
            "balance": "GET /accounts/{account_id}/balance",
            "transactions": "GET /accounts/{account_id}/transactions"
        }
    }


@app.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_authenticated_api_key)
):
    """Create a new bank account."""
    new_account = Account(
        name=account_data.name,
        balance=account_data.initial_balance
    )
    
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    
    return new_account


@app.post("/accounts/deposit", response_model=AccountResponse)
async def deposit_money(
    deposit_data: DepositRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_authenticated_api_key)
):
    """Deposit money into an account."""
    account = db.query(Account).filter(Account.account_id == deposit_data.account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Account not found",
                "account_id": deposit_data.account_id,
                "message": "The specified account does not exist"
            }
        )
    
    account.balance += deposit_data.amount
    
    transaction = Transaction(
        account_id=account.account_id,
        transaction_type=TransactionType.DEPOSIT,
        amount=deposit_data.amount
    )
    db.add(transaction)
    db.commit()
    db.refresh(account)
    
    return account


@app.post("/accounts/withdraw", response_model=AccountResponse)
async def withdraw_money(
    withdraw_data: WithdrawRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_authenticated_api_key)
):
    """Withdraw money from an account."""
    account = db.query(Account).filter(Account.account_id == withdraw_data.account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Account not found",
                "account_id": withdraw_data.account_id,
                "message": "The specified account does not exist"
            }
        )
    
    if account.balance < withdraw_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "Insufficient balance",
                "current_balance": account.balance,
                "requested_amount": withdraw_data.amount,
                "message": "Account balance is insufficient for this withdrawal"
            }
        )
    
    account.balance -= withdraw_data.amount
    
    transaction = Transaction(
        account_id=account.account_id,
        transaction_type=TransactionType.WITHDRAWAL,
        amount=withdraw_data.amount
    )
    db.add(transaction)
    db.commit()
    db.refresh(account)
    
    return account


@app.get("/accounts/{account_id}/balance", response_model=BalanceResponse)
async def get_balance(
    account_id: int = Path(..., gt=0, description="Account ID to query"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_authenticated_api_key)
):
    """Get the current balance of an account."""
    account = db.query(Account).filter(Account.account_id == account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Account not found",
                "account_id": account_id,
                "message": "The specified account does not exist"
            }
        )
    
    return BalanceResponse(
        account_id=account.account_id,
        balance=account.balance,
        name=account.name
    )


@app.get("/accounts/{account_id}/transactions", response_model=TransactionHistoryResponse)
async def get_transaction_history(
    account_id: int = Path(..., gt=0, description="Account ID to query"),
    limit: int = Query(default=50, ge=1, le=1000, description="Maximum number of transactions to return"),
    db: Session = Depends(get_db),
    api_key: str = Depends(get_authenticated_api_key)
):
    """Get transaction history for an account."""
    account = db.query(Account).filter(Account.account_id == account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Account not found",
                "account_id": account_id,
                "message": "The specified account does not exist"
            }
        )
    
    transactions = db.query(Transaction)\
        .filter(Transaction.account_id == account_id)\
        .order_by(Transaction.timestamp.desc())\
        .limit(limit)\
        .all()
    
    return TransactionHistoryResponse(
        account_id=account_id,
        transactions=transactions,
        total_transactions=len(transactions)
    )

