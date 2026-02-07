# Todo API Backend

FastAPI backend for the Todo application with JWT authentication and SQLModel database integration.

## Features

- JWT-based authentication with Better Auth integration
- Secure user isolation - users can only access their own tasks
- Async database operations with SQLModel and asyncpg
- RESTful API endpoints for task management
- Comprehensive error handling and validation

## Tech Stack

- Python 3.9+
- FastAPI
- SQLModel
- asyncpg
- python-jose for JWT handling
- Pydantic for data validation

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```

## Running the Application

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## API Documentation

API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

- `BETTER_AUTH_SECRET`: Secret key for JWT token verification
- `BETTER_AUTH_URL`: URL of the Better Auth service
- `DATABASE_URL`: PostgreSQL database URL
- `DEBUG`: Enable/disable debug mode (default: false)
- `LOG_LEVEL`: Logging level (default: info)