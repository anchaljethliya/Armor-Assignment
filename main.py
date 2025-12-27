"""
FastAPI application for the banking system MCP server.
Provides RESTful endpoints for account management and transactions.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db, init_db
from models import Account, Transaction, TransactionType
from schemas import (
    AccountCreate,
    AccountResponse,
    DepositRequest,
    WithdrawRequest,
    BalanceResponse,
    TransactionHistoryResponse,
    TransactionResponse
)

# Initialize FastAPI app
app = FastAPI(
    title="Banking System MCP Server",
    description="A simple banking system API for account management and transactions",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup."""
    init_db()


@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Banking System MCP Server",
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
async def create_account(account_data: AccountCreate, db: Session = Depends(get_db)):
    """
    Create a new bank account.
    
    - **name**: Account owner's name
    - **initial_balance**: Starting balance (must be >= 0)
    
    Returns the created account with auto-generated account_id.
    """
    # Create new account instance
    new_account = Account(
        name=account_data.name,
        balance=account_data.initial_balance
    )
    
    # Add to database session
    db.add(new_account)
    db.commit()  # Commit to get the account_id
    db.refresh(new_account)  # Refresh to get the generated account_id
    
    return new_account


@app.post("/accounts/deposit", response_model=AccountResponse)
async def deposit_money(deposit_data: DepositRequest, db: Session = Depends(get_db)):
    """
    Deposit money into an account.
    
    - **account_id**: ID of the account to deposit into
    - **amount**: Amount to deposit (must be > 0)
    
    Returns updated account information.
    """
    # Find the account
    account = db.query(Account).filter(Account.account_id == deposit_data.account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {deposit_data.account_id} not found"
        )
    
    # Update account balance
    account.balance += deposit_data.amount
    
    # Create transaction record
    transaction = Transaction(
        account_id=account.account_id,
        transaction_type=TransactionType.DEPOSIT,
        amount=deposit_data.amount
    )
    db.add(transaction)
    
    # Commit changes
    db.commit()
    db.refresh(account)
    
    return account


@app.post("/accounts/withdraw", response_model=AccountResponse)
async def withdraw_money(withdraw_data: WithdrawRequest, db: Session = Depends(get_db)):
    """
    Withdraw money from an account.
    
    - **account_id**: ID of the account to withdraw from
    - **amount**: Amount to withdraw (must be > 0)
    
    Returns updated account information.
    Raises 400 error if balance is insufficient.
    """
    # Find the account
    account = db.query(Account).filter(Account.account_id == withdraw_data.account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {withdraw_data.account_id} not found"
        )
    
    # Check if balance is sufficient
    if account.balance < withdraw_data.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient balance. Current balance: {account.balance}, Requested: {withdraw_data.amount}"
        )
    
    # Update account balance
    account.balance -= withdraw_data.amount
    
    # Create transaction record
    transaction = Transaction(
        account_id=account.account_id,
        transaction_type=TransactionType.WITHDRAWAL,
        amount=withdraw_data.amount
    )
    db.add(transaction)
    
    # Commit changes
    db.commit()
    db.refresh(account)
    
    return account


@app.get("/accounts/{account_id}/balance", response_model=BalanceResponse)
async def get_balance(account_id: int, db: Session = Depends(get_db)):
    """
    Get the current balance of an account.
    
    - **account_id**: ID of the account to query
    
    Returns account balance and name.
    """
    # Find the account
    account = db.query(Account).filter(Account.account_id == account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {account_id} not found"
        )
    
    return BalanceResponse(
        account_id=account.account_id,
        balance=account.balance,
        name=account.name
    )


@app.get("/accounts/{account_id}/transactions", response_model=TransactionHistoryResponse)
async def get_transaction_history(
    account_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get transaction history for an account.
    
    - **account_id**: ID of the account to query
    - **limit**: Maximum number of transactions to return (default: 50)
    
    Returns list of recent transactions ordered by timestamp (newest first).
    """
    # Verify account exists
    account = db.query(Account).filter(Account.account_id == account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with ID {account_id} not found"
        )
    
    # Query transactions for this account, ordered by timestamp (newest first)
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

