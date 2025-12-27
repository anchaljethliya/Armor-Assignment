# Banking System API

A simple banking system API built with FastAPI. Provides endpoints for account management, deposits, withdrawals, and transaction history.

## Features

- Create bank accounts
- Deposit money
- Withdraw money (with balance validation)
- Check account balance
- View transaction history

## Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set API key (required):
```bash
export ARMOR_API_KEY="your-api-key-here"
```

3. Run the server:
```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

- `POST /accounts` - Create a new account
- `POST /accounts/deposit` - Deposit money
- `POST /accounts/withdraw` - Withdraw money
- `GET /accounts/{account_id}/balance` - Get account balance
- `GET /accounts/{account_id}/transactions` - Get transaction history

All requests require an `X-API-Key` header with your API key.

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example

```bash
# Create account
curl -X POST "http://localhost:8000/accounts" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "initial_balance": 1000.0}'

# Deposit
curl -X POST "http://localhost:8000/accounts/deposit" \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"account_id": 1, "amount": 500.0}'
```

## Database

The SQLite database (`banking.db`) is created automatically on first run.
