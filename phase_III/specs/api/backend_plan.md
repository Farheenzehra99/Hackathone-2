# FastAPI Backend Implementation Plan - Todo Application

## 1. Repository & Folder Structure

### Directory Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/                   # Core configurations and settings
│   │   ├── __init__.py
│   │   ├── config.py           # Settings and environment variables
│   │   └── security.py         # JWT utilities and authentication
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependency injection
│   │   ├── v1/                 # Version 1 API routes
│   │   │   ├── __init__.py
│   │   │   ├── router.py       # Main API router
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       ├── tasks.py    # Task-related endpoints
│   │   │       └── auth.py     # Authentication endpoints
│   ├── models/                 # Database models
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   └── task.py             # Task model
│   ├── db/                     # Database utilities
│   │   ├── __init__.py
│   │   ├── base.py             # Base model and engine
│   │   └── session.py          # Async session dependency
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       └── exceptions.py       # Custom exceptions
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

### Specification Placement
- `specs/api/v1_backend.spec.md` - API specification document
- `specs/database/v1_backend.spec.md` - Database specification document

## 2. Environment & Configuration

### Environment Variables Setup
1. Create `.env` file with required variables:
   ```
   BETTER_AUTH_SECRET=Z7F1EOlUGrDvs0aCbYzP02NdW6GMQdMY
   BETTER_AUTH_URL=http://localhost:3000
   DATABASE_URL=postgresql+psycopg://neondb_owner:npg_H48eIOvjDREM@ep-blue-hall-ahvfu7pz-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   DEBUG=false
   LOG_LEVEL=info
   ```

2. Create `app/core/config.py` with Pydantic BaseSettings:
   - Define Settings class with validation
   - Load environment variables
   - Validate required variables exist

3. Implement configuration loading in main application
4. Add environment variable validation at startup

## 3. Database Layer (SQLModel + Async)

### Async Engine Setup
1. Create `app/db/base.py`:
   - Import SQLModel and create Base class
   - Initialize async engine with DATABASE_URL
   - Configure engine with proper pool settings

2. Create `app/db/session.py`:
   - Define get_async_session dependency
   - Implement async context manager
   - Handle session lifecycle properly

### SQLModel Models
1. Create `app/models/user.py`:
   - Define UserBase with id, email, name, timestamps
   - Define User table with proper constraints
   - Add indexes for email field

2. Create `app/models/task.py`:
   - Define TaskBase with title, description, completed, user_id
   - Define Task table with foreign key to User
   - Add indexes for user_id and completed fields
   - Establish relationship with User model

### Migration Strategy
1. Prepare initial schema creation function
2. Create alembic configuration for future migrations
3. Document manual schema creation for initial setup

## 4. Authentication & Security Flow

### JWT Utilities
1. Create `app/core/security.py`:
   - JWT token validation function
   - Token decoding with BETTER_AUTH_SECRET
   - User ID extraction from token
   - Token expiration checking

### Authentication Middleware
1. Implement JWT bearer token extraction
2. Create get_current_user dependency
3. Implement validate_user_ownership function
4. Add token validation in dependency injection

### Security Enforcement
1. Implement user ID validation in all routes
2. Return 403 for user ID mismatches
3. Return 401 for invalid/expired tokens
4. Protect all endpoints with authentication

## 5. API Routing Strategy

### Router Organization
1. Create `app/api/v1/router.py`:
   - Initialize main API router
   - Include all endpoint routers
   - Add version prefix (/api/v1/)

2. Create `app/api/v1/endpoints/tasks.py`:
   - All task-related endpoints
   - Proper path parameter handling
   - Dependency injection for auth

3. Set up route inclusion in main application

### Path Parameter Handling
1. Implement {user_id} parameter validation
2. Ensure user_id matches JWT token
3. Handle path parameter extraction and validation

## 6. Endpoint-by-Endpoint Implementation Plan

### GET /api/{user_id}/tasks
1. **Dependencies**: get_current_user, get_async_session
2. **Request Model**: Query parameters for status, limit, offset
3. **DB Operations**: Query tasks filtered by user_id and status
4. **Response Model**: List of tasks with pagination info
5. **Error Cases**: 401 (invalid token), 403 (user mismatch)
6. **Control Flow**: Validate user, query tasks, apply filters, return results

### POST /api/{user_id}/tasks
1. **Dependencies**: get_current_user, get_async_session
2. **Request Model**: CreateTaskRequest with title (required), description (optional)
3. **DB Operations**: Create new task with user_id from token
4. **Response Model**: Created task object
5. **Error Cases**: 400 (validation), 401 (invalid token), 403 (user mismatch)
6. **Control Flow**: Validate input, create task, return created object

### GET /api/{user_id}/tasks/{id}
1. **Dependencies**: get_current_user, get_async_session
2. **Request Model**: Path parameters only
3. **DB Operations**: Query specific task by ID and user_id
4. **Response Model**: Single task object
5. **Error Cases**: 401 (invalid token), 403 (user mismatch), 404 (not found)
6. **Control Flow**: Validate user, find task for user, return if exists

### PUT /api/{user_id}/tasks/{id}
1. **Dependencies**: get_current_user, get_async_session
2. **Request Model**: UpdateTaskRequest with all fields
3. **DB Operations**: Update specific task by ID and user_id
4. **Response Model**: Updated task object
5. **Error Cases**: 400 (validation), 401 (invalid token), 403 (user mismatch), 404 (not found)
6. **Control Flow**: Validate input, find task for user, update, return updated

### DELETE /api/{user_id}/tasks/{id}
1. **Dependencies**: get_current_user, get_async_session
2. **Request Model**: Path parameters only
3. **DB Operations**: Delete specific task by ID and user_id
4. **Response Model**: Success message
5. **Error Cases**: 401 (invalid token), 403 (user mismatch), 404 (not found)
6. **Control Flow**: Validate user, find task for user, delete, return success

### PATCH /api/{user_id}/tasks/{id}/complete
1. **Dependencies**: get_current_user, get_async_session
2. **Request Model**: UpdateCompletionRequest with completed field
3. **DB Operations**: Update completion status by ID and user_id
4. **Response Model**: Updated task object
5. **Error Cases**: 400 (validation), 401 (invalid token), 403 (user mismatch), 404 (not found)
6. **Control Flow**: Validate input, find task for user, update completion, return updated

## 7. Error Handling Strategy

### Exception Classes
1. Create custom exception classes in `app/utils/exceptions.py`:
   - AuthException
   - UserMismatchException
   - ResourceNotFoundException

### HTTP Exception Handling
1. Implement centralized error handlers
2. Return consistent error response format
3. Handle validation errors with 422 status
4. Handle authentication errors with 401 status
5. Handle authorization errors with 403 status
6. Handle not found errors with 404 status

### Error Response Format
1. Ensure all errors follow the standardized format:
   ```json
   {
     "success": false,
     "error": {
       "code": "ERROR_CODE",
       "message": "Human-readable error message",
       "details": {}
     }
   }
   ```

## 8. Async Best Practices

### Session Lifecycle
1. Use async context managers for database sessions
2. Implement proper session cleanup
3. Handle async transactions correctly

### Non-blocking Operations
1. Use async database operations throughout
2. Avoid synchronous calls in route handlers
3. Implement proper async dependency injection

### Safe Commit/Rollback Patterns
1. Use try/catch blocks for database transactions
2. Implement proper error handling for database operations
3. Ensure session cleanup on exceptions

## 9. Logging & Debugging Hints

### What to Log
1. Authentication successes/failures (without tokens)
2. Database errors and connection issues
3. Request/response information (excluding sensitive data)
4. Performance metrics for key operations

### What NOT to Log
1. JWT tokens or sensitive authentication data
2. User passwords or personal secrets
3. Database credentials
4. Other sensitive information

### Debugging Configuration
1. Implement configurable log levels
2. Add debug mode for development
3. Ensure production logging doesn't expose sensitive data

## 10. Testing & Verification Scenarios

### Authentication Testing
1. Valid token acceptance
2. Invalid token rejection (401)
3. Expired token handling (401)
4. Missing token handling (401)

### Cross-user Access Prevention
1. User A attempting to access User B's tasks (403)
2. User A modifying User B's tasks (403)
3. User ID mismatch validation (403)

### Data Operations Testing
1. Complete CRUD lifecycle for tasks
2. Validation error handling
3. Database connection resilience
4. Pagination functionality

### Frontend Integration Testing
1. API response format compliance
2. Status code accuracy
3. Authentication header handling
4. Error response format consistency

## 11. Acceptance Criteria Checklist

### Security Requirements
- [ ] All routes protected with JWT authentication
- [ ] User ID validation enforced on every request
- [ ] No cross-user data access possible
- [ ] Proper error codes returned (401, 403, 404, 422)

### Functional Requirements
- [ ] GET /api/{user_id}/tasks returns user's tasks
- [ ] POST /api/{user_id}/tasks creates new task
- [ ] GET /api/{user_id}/tasks/{id} returns specific task
- [ ] PUT /api/{user_id}/tasks/{id} updates task
- [ ] DELETE /api/{user_id}/tasks/{id} deletes task
- [ ] PATCH /api/{user_id}/tasks/{id}/complete updates completion status

### Technical Requirements
- [ ] Async operations throughout (database, routes, dependencies)
- [ ] SQLModel models with proper relationships
- [ ] Proper indexing on database tables
- [ ] Consistent error response format
- [ ] Frontend API contract alignment

### Quality Requirements
- [ ] Enterprise-ready code quality
- [ ] Comprehensive error handling
- [ ] Proper logging without sensitive data
- [ ] Performance considerations implemented
- [ ] Production-ready configuration