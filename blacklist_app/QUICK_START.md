# Quick Start Guide - Blacklist API

## ✅ Current Status

Your Flask Blacklist API is **running successfully**!

- **PostgreSQL Database**: Running on port `5433` (Docker container)
- **Flask Application**: Running on port `5001` (local with Poetry)
- **Bearer Token**: `6tFpnHrro6wjsZnd8roWQMsTffBPcitQy2BgeOBQMUQ`

## 🚀 Quick Commands

### Start Services

```bash
# Start PostgreSQL only (already running)
cd blacklist_app
docker compose up -d

# Start Flask app
cd blacklist_app
source venv/bin/activate
make run
```

### Stop Services

```bash
# Stop Flask (if running in background)
# Press Ctrl+C or find process with: ps aux | grep flask

# Stop PostgreSQL
cd blacklist_app
docker compose down
```

## 🧪 Test the API

### 1. Health Check (No Auth Required)
```bash
curl http://localhost:5001/health
# Response: {"status": "healthy", "service": "blacklist-api"}

curl http://localhost:5001/blacklists/ping
# Response: {"message": "pong"}
```

### 2. Add Email to Blacklist
```bash
curl -X POST http://localhost:5001/blacklists \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer 6tFpnHrro6wjsZnd8roWQMsTffBPcitQy2BgeOBQMUQ" \
  -d '{
    "email": "baduser@example.com",
    "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    "blocked_reason": "Fraudulent activity"
  }'
```

**Response (201):**
```json
{
  "message": "Email baduser@example.com added to blacklist successfully",
  "id": "437116b6-d37d-43c5-be98-173b138e226e",
  "email": "baduser@example.com",
  "created_at": "2025-10-13T18:59:28.773314"
}
```

### 3. Check if Email is Blacklisted
```bash
# Check blacklisted email
curl http://localhost:5001/blacklists/baduser@example.com \
  -H "Authorization: Bearer 6tFpnHrro6wjsZnd8roWQMsTffBPcitQy2BgeOBQMUQ"
```

**Response (200):**
```json
{
  "is_blacklisted": true,
  "email": "baduser@example.com",
  "blocked_reason": "Fraudulent activity"
}
```

```bash
# Check non-blacklisted email
curl http://localhost:5001/blacklists/gooduser@example.com \
  -H "Authorization: Bearer 6tFpnHrro6wjsZnd8roWQMsTffBPcitQy2BgeOBQMUQ"
```

**Response (200):**
```json
{
  "is_blacklisted": false,
  "email": "gooduser@example.com",
  "blocked_reason": null
}
```

## 🧪 Test Scenarios Verified

✅ **Authentication works**: Requests without Bearer token are rejected (401)  
✅ **Duplicate prevention**: Adding same email twice returns 409 Conflict  
✅ **Email validation**: Invalid emails are rejected (400)  
✅ **Database persistence**: Data is stored in PostgreSQL and persists  
✅ **IP tracking**: Client IP is captured from X-Forwarded-For header  

## 📁 Project Structure

```
blacklist_app/
├── src/
│   ├── db/                    # Database layer
│   │   ├── database.py        # SQLAlchemy setup
│   │   └── models.py          # Blacklist model
│   ├── models/                # Schemas & errors
│   │   ├── blacklist.py       # Marshmallow schemas
│   │   └── errors.py          # Custom exceptions
│   ├── repositories/          # Data access layer
│   │   └── blacklist_repository.py
│   ├── services/              # Business logic
│   │   └── blacklist_service.py
│   ├── routes/                # API endpoints
│   │   └── blacklist_router.py
│   ├── middleware/            # Authentication
│   │   └── auth_middleware.py
│   ├── utils/                 # Utilities
│   │   └── validation.py      # IP & UUID validation
│   └── main.py                # Flask app initialization
├── tests/                     # Test suite
├── .env                       # Environment variables
├── docker-compose.yml         # PostgreSQL container
├── Makefile                   # Automation commands
└── README.md                  # Full documentation
```

## 🔧 Makefile Commands

```bash
make setup          # Install Poetry & dependencies
make install        # Install dependencies only
make run            # Run Flask app locally
make test           # Run all tests
make test-cov       # Run tests with coverage
make clean          # Clean up cache files

# Docker commands
make docker-compose-up      # Start PostgreSQL
make docker-compose-down    # Stop PostgreSQL
make docker-compose-build   # Rebuild & start all services
```

## 🗄️ Database Info

**Connection String:**
```
postgresql://postgres:postgres@localhost:5433/blacklist_db
```

**Connect with psql:**
```bash
psql -h localhost -p 5433 -U postgres -d blacklist_db
# Password: postgres
```

**View data:**
```sql
SELECT * FROM blacklists;
```

## 📝 Environment Variables

Located in `.env` file:
```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/blacklist_db
BEARER_TOKEN=6tFpnHrro6wjsZnd8roWQMsTffBPcitQy2BgeOBQMUQ
FLASK_ENV=development
FLASK_DEBUG=1
```

## 🎯 API Specification Summary

### POST /blacklists
Add email to blacklist
- **Auth**: Bearer token required
- **Body**: `email`, `app_uuid`, `blocked_reason` (optional)
- **Returns**: 201 with email details
- **Errors**: 400 (validation), 401 (auth), 409 (duplicate)

### GET /blacklists/<email>
Check if email is blacklisted
- **Auth**: Bearer token required
- **Returns**: 200 with `is_blacklisted`, `email`, `blocked_reason`

### GET /blacklists/ping
Health check (no auth required)
- **Returns**: 200 with `{"message": "pong"}`

## 📚 Additional Resources

- Full API documentation: `README.md`
- Postman guide: `POSTMAN_COLLECTION.md`
- Sample tests: `tests/unit/test_blacklist_service.py`

## 🚨 Important Notes

1. **Port 5000 vs 5001**: We use port 5001 because macOS Control Center uses port 5000
2. **Bearer Token**: Stored in `.env` - keep it secret!
3. **PostgreSQL Port**: 5433 to avoid conflict with other PostgreSQL instances
4. **IP Tracking**: Automatically captures client IP from X-Forwarded-For header (Elastic Beanstalk ready)

---

**Need help?** Check the main `README.md` or `POSTMAN_COLLECTION.md` for more examples!

