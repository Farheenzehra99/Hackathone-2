---
id: 001
title: Backend Audit Psycopg Error
stage: general
date: 2026-01-20
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-frontend-ui
user: claude
command: "perform a full backend audit of the current FastAPI application structure"
labels: [backend,audit,database,psycopg,error]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - /mnt/d/hackathone-02/phase_2/backend/app/main.py
  - /mnt/d/hackathone-02/phase_2/backend/app/db/base.py
  - /mnt/d/hackathone-02/phase_2/backend/app/db/session.py
  - /mnt/d/hackathone-02/phase_2/backend/app/core/config.py
  - /mnt/d/hackathone-02/phase_2/backend/app/api/v1/endpoints/tasks.py
  - /mnt/d/hackathone-02/phase_2/backend/requirements.txt
  - /mnt/d/hackathone-02/phase_2/backend/README.md
  - /mnt/d/hackathone-02/phase_2/backend/.env.example
tests:
  - /mnt/d/hackathone-02/phase_2/backend/run_server.py
---

## Prompt

Perform a full backend audit of the current FastAPI application structure. Identify all database-related files, engine initialization, and connection handling. Focus on identifying where the psycopg import error might be occurring, especially looking for SQLAlchemy engine creation, database URL configuration, and any import statements that might trigger psycopg.

## Response snapshot

## Backend Architecture Audit Report

### 1) Backend folder structure

The backend follows a well-organized FastAPI + SQLModel structure:

```
backend/
├── app/                    # Main application package
│   ├── __init__.py         # Package initialization
│   ├── main.py            # FastAPI app factory and main entry point
│   ├── lifespan.py        # Application lifespan management
│   ├── core/              # Core utilities and configurations
│   │   ├── __init__.py
│   │   ├── config.py      # Settings and environment variables
│   │   └── security.py    # JWT authentication utilities
│   ├── db/                # Database layer
│   │   ├── __init__.py
│   │   ├── base.py        # SQLModel base and engine creation
│   │   └── session.py     # Async session dependency
│   ├── models/            # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py        # User model definition
│   │   └── task.py        # Task model definition
│   ├── api/               # API routes and dependencies
│   │   ├── __init__.py
│   │   ├── deps.py        # Dependency injection utilities
│   │   ├── v1/            # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── router.py  # Main API router composition
│   │   │   └── endpoints/ # Individual route modules
│   │   │       ├── __init__.py
│   │   │       └── tasks.py # Task-related endpoints
│   ├── utils/             # Utility functions
│   │   └── exceptions.py  # Custom exception classes
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variable examples
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
└── run_server.py         # Server startup script
```

### 2) Middleware responsibilities

**JWT Middleware/Dependency:**
- Extracts JWT token from Authorization header (`Authorization: Bearer <token>`)
- Validates signature and expiration using HS256 algorithm
- Attaches user identity to request state via `get_current_user()` dependency
- Distinguishes authN (401) vs authZ (403) through `validate_user_ownership()`
- Bypass rules: Not applicable (all protected routes require authentication)
- Security notes: Tokens are not logged; uses fixed secret from settings

**Other middleware:**
- CORS: Handles cross-origin requests with configured allowed origins
- Request validation: Handles Pydantic validation errors
- Exception handling: Global handlers for various error types

**What middleware must NOT do:**
- Perform DB reads per request unless necessary
- Contain business logic (should remain thin)

### 3) Route organization under /api/

- URL shape: `/api/v1/{resource}/{id}` (e.g., `/api/v1/users/{user_id}/tasks`)
- Versioning: API version 1 mounted at `/api/v1`
- Router composition: Main router in `app/api/v1/router.py` aggregates resource routers
- Dependency injection: DB session via `Depends(get_session)`, auth via `Depends(get_current_user_safe)`
- Resource grouping: Currently only tasks, organized by resource type

**Example router skeleton:**
```python
@router.get("/", response_model=dict)
async def get_tasks(
    user_id: str = Path(...),
    current_user_id: str = Depends(get_current_user_safe),
    session: AsyncSession = Depends(get_session)
):
    # Implementation
```

### 4) Error handling conventions

**Global exception handlers:**
- Validation errors (422): `RequestValidationError`
- Auth errors (401): `AuthException`
- AuthZ errors (403): `UserMismatchException`
- Not found (404): `ResourceNotFoundException`
- General errors (500): Generic exception handler

**Response schema:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message",
    "details": {} // Optional
  }
}
```

**Logging rules:**
- Info: General operations
- Warning: Client errors (4xx)
- Error: Server errors (5xx)
- Redaction: No sensitive data logged in production

### 5) The psycopg Import Error Root Cause

The issue is in the `DATABASE_URL` configuration. The current URL contains PostgreSQL-specific SSL parameters that `asyncpg` doesn't recognize:

❌ **Current (problematic)**:
```
postgresql+asyncpg://neondb_owner:npg_H48eIOvjDREM@ep-blue-hall-ahvfu7pz-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

❌ **Error**: `TypeError: connect() got an unexpected keyword argument 'sslmode'`

✅ **Solution**: Replace with asyncpg-compatible parameters:
```
postgresql+asyncpg://neondb_owner:npg_H48eIOvjDREM@ep-blue-hall-ahvfu7pz-pooler.c-3.us-east-1.aws.neon.tech/neondb?ssl=require
```

### 6) Acceptance checks

- [x] All routers mounted under `/api/v1`
- [x] JWT required on protected routes via dependency
- [x] Standard error schema returned consistently
- [x] DB session lifecycle implemented with async generators
- [ ] ✅ **Issue Found**: DATABASE_URL contains invalid asyncpg parameters causing startup failure

## Follow-up Actions & Risks

1. **Immediate fix needed**: Update DATABASE_URL in config.py and .env.example to use asyncpg-compatible SSL parameters
2. **Security risk**: Current hardcoded secret in config.py should be moved to environment variables only
3. **Connectivity risk**: The Neon database URL may require different connection parameters for asyncpg

## Resolution of the psycopg Error

The error occurs because SQLAlchemy's asyncpg dialect doesn't accept the same SSL parameters as psycopg2. The URL parameter `sslmode=require&channel_binding=require` should be changed to `ssl=require`.

---

## Outcome

- ✅ Impact: Identified the exact root cause of the psycopg import error in the database configuration
- 🧪 Tests: Verified the error by running the server which reproduced the TypeError
- 📁 Files: Audited all backend files including main.py, db/base.py, config.py, and endpoints
- 🔁 Next prompts: Should address the DATABASE_URL configuration issue
- 🧠 Reflection: The error was not an import error per se, but a parameter compatibility issue between SQLAlchemy and asyncpg

## Evaluation notes (flywheel)

- Failure modes observed: Server startup fails due to incompatible SSL parameters in DATABASE_URL
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Update the DATABASE_URL to use asyncpg-compatible SSL parameters