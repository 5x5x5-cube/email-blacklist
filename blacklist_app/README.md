# Blacklist API

Microservice for managing email blacklist in the system. Built with Flask and PostgreSQL.

## Features

- Add emails to a global blacklist
- Check if an email is blacklisted
- Store IP address and timestamp of requests
- Bearer token authentication
- RESTful API design

## Tech Stack

- **Python 3.10+**
- **Flask 3.0**: Micro web framework
- **Flask-SQLAlchemy**: ORM for database operations
- **Flask-RESTful**: REST API development
- **Flask-Marshmallow**: Object serialization/deserialization
- **Flask-JWT-Extended**: JWT token handling
- **PostgreSQL**: Relational database
- **Poetry**: Dependency management
- **Docker**: Containerization

## Project Structure

```
blacklist_app/
├── src/
│   ├── db/
│   │   ├── database.py       # Database configuration
│   │   └── models.py          # SQLAlchemy models
│   ├── models/
│   │   ├── blacklist.py       # Marshmallow schemas
│   │   └── errors.py          # Custom exceptions
│   ├── repositories/
│   │   └── blacklist_repository.py  # Database operations
│   ├── services/
│   │   └── blacklist_service.py     # Business logic
│   ├── routes/
│   │   └── blacklist_router.py      # API endpoints
│   ├── middleware/
│   │   └── auth_middleware.py       # Authentication
│   ├── utils/
│   │   └── validation.py            # Validation utilities
│   └── main.py                # Flask app initialization
├── tests/
│   ├── unit/
│   └── integration/
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## API Endpoints

### POST /blacklists
Add an email to the global blacklist.

**Request:**
```json
{
  "email": "user@example.com",
  "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "blocked_reason": "Spam activity detected"  // Optional, max 255 chars
}
```

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Response (201):**
```json
{
  "message": "Email user@example.com added to blacklist successfully",
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "created_at": "2025-10-13T10:30:00"
}
```

### GET /blacklists/<email>
Check if an email is in the blacklist.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "is_blacklisted": true,
  "email": "user@example.com",
  "blocked_reason": "Spam activity detected"
}
```

### GET /blacklists/ping
Health check endpoint (no authentication required).

**Response (200):**
```json
{
  "message": "pong"
}
```

## Setup

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher
- Poetry (for dependency management)
- Docker and Docker Compose (optional)

### Installation

1. **Clone the repository:**
```bash
cd blacklist_app
```

2. **Install dependencies:**
```bash
make setup
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `BEARER_TOKEN`: Authentication token for API access

### Running Locally

**With Poetry:**
```bash
make run
```

**With Docker Compose:**
```bash
make docker-compose-build
```

The API will be available at `http://localhost:5000`

## Development

### Running Tests

```bash
# Run all tests
make test

# Run unit tests only
make test-unit

# Run tests with coverage
make test-cov
```

### Database Migrations

The application automatically creates tables on startup. For production, consider using Flask-Migrate for proper database migrations.

## Deployment

### Docker

1. **Build the image:**
```bash
make docker-build
```

2. **Run the container:**
```bash
make docker-run
```

### AWS Elastic Beanstalk

The application is configured to work with AWS Elastic Beanstalk:

- The `X-Forwarded-For` header is automatically handled to capture the real client IP
- Port 5000 is exposed for the Flask application
- Environment variables should be configured in the EB environment

### Push to AWS ECR

```bash
# Configure AWS credentials first
aws configure

# Push to ECR
make docker-push
```

## Authentication

All endpoints (except `/blacklists/ping`) require a Bearer token in the Authorization header:

```
Authorization: Bearer your-token-here
```

The token is configured via the `BEARER_TOKEN` environment variable.

## IP Address Tracking

The service automatically captures the client's IP address for each blacklist request:
- Checks `X-Forwarded-For` header (for load balancers)
- Falls back to direct connection IP
- Stores IP with each blacklist entry

## Database Schema

### Blacklist Table

| Column | Type | Description |
|--------|------|-------------|
| id | String (UUID) | Primary key |
| email | String (255) | Email address (unique) |
| app_uuid | String (UUID) | Application identifier |
| blocked_reason | String (255) | Reason for blocking (optional) |
| ip_address | String (45) | IP address of requester |
| created_at | DateTime | Timestamp of creation |

## Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `500 Internal Server Error`: Server error

Error responses follow this format:
```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "details": {}  // Optional validation details
}
```

## License

This project is part of Universidad de los Andes coursework.

## Contact

andres.pena@uniandes.edu.co

