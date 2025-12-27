# Quick Start Guide - Banking MCP Server

## ✅ Assignment Completion Status

**All requirements have been completed:**

- ✅ **Python-based web server** (FastAPI)
- ✅ **SQL database operations** (SQLite with SQLAlchemy ORM)
- ✅ **Account Creation/Registration** endpoint: `POST /accounts`
- ✅ **Deposit** endpoint: `POST /accounts/deposit`
- ✅ **Withdrawal** endpoint: `POST /accounts/withdraw`
- ✅ **Balance Inquiry** endpoint: `GET /accounts/{account_id}/balance`
- ✅ **Transaction History** endpoint: `GET /accounts/{account_id}/transactions`

---

## 🚀 How to Run the Project

### Prerequisites Check

First, verify Python is installed:

```powershell
python --version
```

You should see: `Python 3.11.x` or higher

If not installed, see `SETUP_WINDOWS.md` for installation instructions.

### Step 1: Install Dependencies

Open PowerShell in the project directory and run:

```powershell
python -m pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.104.1 sqlalchemy-2.0.23 uvicorn-0.24.0 pydantic-2.5.0
```

### Step 2: Start the Server

Run the FastAPI server:

```powershell
python -m uvicorn main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 3: Verify Server is Running

Open your browser and visit:

- **Main API**: http://127.0.0.1:8000/
- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Alternative Docs**: http://127.0.0.1:8000/redoc

You should see the API documentation or JSON response.

---

## 🧪 Testing the Endpoints

### Option 1: Using Swagger UI (Recommended)

1. Go to http://127.0.0.1:8000/docs
2. You'll see all endpoints listed
3. Click on any endpoint → "Try it out"
4. Fill in the request body
5. Click "Execute"
6. See the response

### Option 2: Using PowerShell

#### 1. Create an Account
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"name": "John Doe", "initial_balance": 1000.0}'
```

**Response:**
```json
{
  "account_id": 1,
  "name": "John Doe",
  "balance": 1000.0
}
```

#### 2. Deposit Money
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts/deposit" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"account_id": 1, "amount": 500.0}'
```

**Response:**
```json
{
  "account_id": 1,
  "name": "John Doe",
  "balance": 1500.0
}
```

#### 3. Withdraw Money
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts/withdraw" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"account_id": 1, "amount": 200.0}'
```

**Response:**
```json
{
  "account_id": 1,
  "name": "John Doe",
  "balance": 1300.0
}
```

#### 4. Check Balance
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts/1/balance"
```

**Response:**
```json
{
  "account_id": 1,
  "balance": 1300.0,
  "name": "John Doe"
}
```

#### 5. Get Transaction History
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts/1/transactions?limit=10"
```

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

### Option 3: Using cURL (if available)

```bash
# Create account
curl -X POST "http://127.0.0.1:8000/accounts" -H "Content-Type: application/json" -d "{\"name\": \"John Doe\", \"initial_balance\": 1000.0}"

# Deposit
curl -X POST "http://127.0.0.1:8000/accounts/deposit" -H "Content-Type: application/json" -d "{\"account_id\": 1, \"amount\": 500.0}"

# Withdraw
curl -X POST "http://127.0.0.1:8000/accounts/withdraw" -H "Content-Type: application/json" -d "{\"account_id\": 1, \"amount\": 200.0}"

# Check balance
curl "http://127.0.0.1:8000/accounts/1/balance"

# Get transactions
curl "http://127.0.0.1:8000/accounts/1/transactions?limit=10"
```

---

## 📋 Complete Test Sequence

Run these commands in order to test all functionality:

```powershell
# 1. Create account
$account = Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts" -Method POST -ContentType "application/json" -Body '{"name": "Test User", "initial_balance": 1000.0}'
$accountId = $account.account_id
Write-Host "Created account ID: $accountId with balance: $($account.balance)"

# 2. Deposit
$account = Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts/deposit" -Method POST -ContentType "application/json" -Body "{\"account_id\": $accountId, \"amount\": 500.0}"
Write-Host "After deposit, balance: $($account.balance)"

# 3. Withdraw
$account = Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts/withdraw" -Method POST -ContentType "application/json" -Body "{\"account_id\": $accountId, \"amount\": 200.0}"
Write-Host "After withdrawal, balance: $($account.balance)"

# 4. Check balance
$balance = Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts/$accountId/balance"
Write-Host "Current balance: $($balance.balance)"

# 5. Get transaction history
$history = Invoke-RestMethod -Uri "http://127.0.0.1:8000/accounts/$accountId/transactions"
Write-Host "Total transactions: $($history.total_transactions)"
```

---

## 🗄️ Database

The SQLite database (`banking.db`) is automatically created when you first run the server. It contains:

- **accounts** table: Account information
- **transactions** table: Transaction history

The database file will be in the same directory as your project.

---

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## ❌ Troubleshooting

### "python is not recognized"
- Try: `py -m pip install -r requirements.txt`
- Or install Python from python.org (check "Add to PATH")

### "Module not found"
- Make sure you're in the project directory
- Run: `python -m pip install -r requirements.txt`

### "Address already in use"
- Port 8000 is already in use
- Stop the other process or change port: `python -m uvicorn main:app --reload --port 8001`

### "Connection refused"
- Make sure the server is running
- Check the terminal for error messages
- Verify you're using the correct URL: http://127.0.0.1:8000

---

## 📁 Project Structure

```
Armor-Assingment/
├── main.py              # FastAPI application and endpoints
├── database.py          # Database connection setup
├── models.py            # SQLAlchemy models (Account, Transaction)
├── schemas.py           # Pydantic validation schemas
├── requirements.txt     # Python dependencies
├── README.md           # Full documentation
├── QUICK_START.md      # This file
├── HOW_IT_WORKS.md     # Technical explanation
├── SETUP_WINDOWS.md    # Windows setup guide
└── banking.db          # SQLite database (created automatically)
```

---

## ✅ Verification Checklist

Before submitting, verify:

- [ ] Server starts without errors
- [ ] Can access http://127.0.0.1:8000/docs
- [ ] Can create an account
- [ ] Can deposit money
- [ ] Can withdraw money
- [ ] Can check balance
- [ ] Can view transaction history
- [ ] Database file (banking.db) is created
- [ ] All endpoints return proper JSON responses

---

## 🎯 Next Steps for Assignment

1. ✅ **Development Complete** - All endpoints implemented
2. ⏭️ **Deploy to Cloud Platform** (AWS, Azure, GCP, etc.)
3. ⏭️ **Security Validation** - Use ArmorIQ tools to test security

---

## 📞 Need Help?

- Check `README.md` for detailed API documentation
- Check `HOW_IT_WORKS.md` for technical details
- Check `SETUP_WINDOWS.md` for installation help

