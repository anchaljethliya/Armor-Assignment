 # Banking System MCP Server

A simple banking system API built with FastAPI, SQLAlchemy, and SQLite. This server provides RESTful endpoints for account management, deposits, withdrawals, balance inquiries, and transaction history.

## Tech Stack

- **Python 3.10+**
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation using Python type annotations

## Project Structure

```
.
├── main.py           # FastAPI application and route handlers
├── database.py       # Database connection and session management
├── models.py         # SQLAlchemy models (Account, Transaction)
├── schemas.py        # Pydantic request/response schemas
├── requirements.txt  # Python dependencies
├── README.md        # This file
└── banking.db       # SQLite database (created automatically)
```

## 🔒 Security (SAFE-MCP Compliant)

This server implements API key authentication for SAFE-MCP compliance.

**Required**: Set the `ARMOR_API_KEY` environment variable before starting the server.

```powershell
# Windows PowerShell
$env:ARMOR_API_KEY="your-secret-api-key-here"

# Then start server
python -m uvicorn main:app --reload
```

**All requests must include the API key in the header**:
```bash
curl -H "X-API-Key: your-secret-api-key-here" http://localhost:8000/
```

See `SECURITY_COMPLIANCE.md` for detailed security information.

---

## Setup Instructions

### Prerequisites

Make sure you have **Python 3.10 or higher** installed. To check if Python is installed:

**Windows (PowerShell):**
```powershell
py --version
# or
python --version
```

**Linux/Mac:**
```bash
python3 --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/). Make sure to check "Add Python to PATH" during installation on Windows.

### 1. Install Dependencies

Install the required packages:

**Windows (PowerShell):**
```powershell
py -m pip install -r requirements.txt
# or if python is in PATH:
python -m pip install -r requirements.txt
```

**Linux/Mac:**
```bash
python3 -m pip install -r requirements.txt
# or
pip install -r requirements.txt
```

### 2. Run the Server

Start the FastAPI server using Uvicorn:

**Windows (PowerShell):**
```powershell
py -m uvicorn main:app --reload
# or
python -m uvicorn main:app --reload
```

**Linux/Mac:**
```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reload on code changes (useful for development).

The server will start at: `http://localhost:8000`

### Troubleshooting

**"python is not recognized" error on Windows:**

1. Try using `py` instead of `python`:
   ```powershell
   py -m pip install -r requirements.txt
   py -m uvicorn main:app --reload
   ```

2. If `py` doesn't work, check if Python is installed:
   - Open PowerShell and run: `Get-Command python*`
   - Check if Python is in your PATH: `$env:PATH`

3. If Python is installed but not in PATH:
   - Find your Python installation (usually `C:\Users\YourName\AppData\Local\Programs\Python\`)
   - Add it to your system PATH, or use the full path:
     ```powershell
     C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\python.exe -m pip install -r requirements.txt
     ```

4. Reinstall Python from [python.org](https://www.python.org/downloads/) and make sure to check "Add Python to PATH" during installation.

### 3. Access API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Create Account
**POST** `/accounts`

Create a new bank account with a name and initial balance.

**Request Body:**
```json
{
  "name": "John Doe",
  "initial_balance": 1000.0
}
```

**Response:**
```json
{
  "account_id": 1,
  "name": "John Doe",
  "balance": 1000.0
}
```

### 2. Deposit Money
**POST** `/accounts/deposit`

Deposit money into an existing account.

**Request Body:**
```json
{
  "account_id": 1,
  "amount": 500.0
}
```

**Response:**
```json
{
  "account_id": 1,
  "name": "John Doe",
  "balance": 1500.0
}
```

### 3. Withdraw Money
**POST** `/accounts/withdraw`

Withdraw money from an account. Returns an error if balance is insufficient.

**Request Body:**
```json
{
  "account_id": 1,
  "amount": 200.0
}
```

**Response:**
```json
{
  "account_id": 1,
  "name": "John Doe",
  "balance": 1300.0
}
```

**Error Response (Insufficient Balance):**
```json
{
  "detail": "Insufficient balance. Current balance: 100.0, Requested: 500.0"
}
```

### 4. Get Balance
**GET** `/accounts/{account_id}/balance`

Retrieve the current balance of an account.

**Example:** `GET /accounts/1/balance`

**Response:**
```json
{
  "account_id": 1,
  "balance": 1300.0,
  "name": "John Doe"
}
```

### 5. Get Transaction History
**GET** `/accounts/{account_id}/transactions?limit=50`

Retrieve recent transactions for an account.

**Query Parameters:**
- `limit` (optional): Maximum number of transactions to return (default: 50)

**Example:** `GET /accounts/1/transactions?limit=10`

**Response:**
```json
{
  "account_id": 1,
  "transactions": [
    {
      "transaction_id": 3,
      "account_id": 1,
      "transaction_type": "withdrawal",
      "amount": 200.0,
      "timestamp": "2024-01-15T10:30:00"
    },
    {
      "transaction_id": 2,
      "account_id": 1,
      "transaction_type": "deposit",
      "amount": 500.0,
      "timestamp": "2024-01-15T09:15:00"
    }
  ],
  "total_transactions": 2
}
```

## Example Usage with cURL

### Create an account:
```bash
curl -X POST "http://localhost:8000/accounts" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Smith", "initial_balance": 500.0}'
```

### Deposit money:
```bash
curl -X POST "http://localhost:8000/accounts/deposit" \
  -H "Content-Type: application/json" \
  -d '{"account_id": 1, "amount": 250.0}'
```

### Withdraw money:
```bash
curl -X POST "http://localhost:8000/accounts/withdraw" \
  -H "Content-Type: application/json" \
  -d '{"account_id": 1, "amount": 100.0}'
```

### Check balance:
```bash
curl "http://localhost:8000/accounts/1/balance"
```

### Get transaction history:
```bash
curl "http://localhost:8000/accounts/1/transactions?limit=10"
```

## Database

The application uses SQLite and automatically creates a `banking.db` file in the project root when first run. The database schema includes:

- **accounts** table: Stores account information (account_id, name, balance)
- **transactions** table: Stores transaction history (transaction_id, account_id, transaction_type, amount, timestamp)

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful request
- `201 Created` - Account created successfully
- `400 Bad Request` - Invalid input or insufficient balance
- `404 Not Found` - Account not found

## Notes

- Account IDs are auto-generated integers starting from 1
- All transactions are automatically recorded with timestamps
- Withdrawals are blocked if the account balance is insufficient
- The database is initialized automatically on server startup
- This is a simple implementation; for production use, consider:
  - Using Decimal instead of Float for precise financial calculations
  - Adding authentication and authorization
  - Implementing database migrations
  - Adding comprehensive logging
  - Using a more robust database (PostgreSQL, MySQL)

