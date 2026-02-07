# REST API Contract - Phase II

## Scope and Base Information
- **Base URL**: `http://localhost:8000` (or as configured)
- **Version**: `/api/v1`
- **Protocol**: HTTPS in production, HTTP in development
- **Content-Type**: `application/json` for requests and responses

## Authentication & Authorization

### JWT Authentication Requirements
- **All endpoints require JWT authentication** in the `Authorization` header with format: `Bearer {token}`
- Missing, invalid, or expired tokens return `401 Unauthorized`

### JWT Claim Structure
- Token must contain `sub` (subject/user_id) claim
- Tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 30 minutes)

### Authorization Rules for user_id Path Parameters
- **Never trust `user_id` from path/query/body as the source of truth**
- Always validate that any provided `user_id` matches the authenticated subject (`sub` claim in JWT)
- Return `403 Forbidden` if path `user_id` does not match authenticated user's `sub` claim
- Return `403 Forbidden` if authenticated user attempts to access another user's resources

### Data Scoping and Filtering
- Backend must filter all data by authenticated user (`auth.user_id`)
- Every list/read/update/delete must be scoped to the authenticated user's data
- Prevent horizontal privilege escalation via ID guessing
- Return `404 Not Found` for resources that don't belong to the authenticated user (to avoid leaking existence)

## Conventions

### URL Patterns
- Standard REST patterns: `/users/{user_id}/todos/{todo_id}`
- Collection endpoints: `/users/{user_id}/todos`
- Action endpoints: `/users/{user_id}/todos/{todo_id}/complete`

### Timestamp Format
- ISO 8601 format: `YYYY-MM-DDTHH:MM:SS.ssssssZ`
- Stored as UTC, displayed in user's timezone

### Field Naming
- Snake_case for all field names in request/response bodies
- Consistent naming across all endpoints

## Error Handling

### Standard Error Envelope
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {} // Optional field for additional error details
  }
}
```

### 401 Unauthorized
- Missing `Authorization` header
- Invalid JWT token format
- Expired JWT token
- Malformed JWT token

**Example Response:**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_INVALID_CREDENTIALS",
    "message": "Could not validate credentials"
  }
}
```

### 403 Forbidden
- Authenticated user attempts to access another user's resource
- Path `user_id` does not match authenticated user's `sub` claim
- Insufficient permissions/roles
- Attempting to modify another user's data

**Example Response:**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_INSUFFICIENT_PERMISSIONS",
    "message": "Insufficient permissions to access this resource"
  }
}
```

### 404 Not Found
- Resource does not exist within the caller's authorized scope
- Used to avoid leaking existence of resources belonging to other users
- Return when resource ID does not exist OR does not belong to authenticated user

**Example Response:**
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found"
  }
}
```

## Endpoints

### Users

#### GET /users/me
- **Description**: Get authenticated user's profile information
- **Authentication**: Required (JWT Bearer token)
- **Path Parameters**: None
- **Query Parameters**: None
- **Request Body**: None
- **Response Schema**:
```json
{
  "success": true,
  "data": {
    "id": "string",
    "email": "string",
    "username": "string",
    "created_at": "string",
    "updated_at": "string"
  }
}
```
- **Success Status**: 200 OK
- **Error Statuses**: 401 (Unauthorized)
- **Security Enforcement**: Validates JWT token, no path user_id to validate

---

### Todos

#### GET /users/{user_id}/todos
- **Description**: List all todos for the authenticated user
- **Authentication**: Required (JWT Bearer token)
- **Path Parameters**:
  - `user_id`: String - user identifier from path
- **Query Parameters**:
  - `limit`: Integer (optional, default: 50, max: 100)
  - `offset`: Integer (optional, default: 0)
  - `status`: String (optional, filter by status: "pending", "completed", "archived")
- **Request Body**: None
- **Response Schema**:
```json
{
  "success": true,
  "data": {
    "todos": [
      {
        "id": "string",
        "title": "string",
        "description": "string",
        "status": "string",
        "priority": "string",
        "due_date": "string",
        "completed_at": "string",
        "created_at": "string",
        "updated_at": "string",
        "user_id": "string"
      }
    ],
    "total": 0,
    "offset": 0,
    "limit": 50
  }
}
```
- **Success Status**: 200 OK
- **Error Statuses**: 401 (Unauthorized), 403 (Forbidden - user_id mismatch), 404 (Not Found - if user doesn't exist)
- **Security Enforcement**: Validates JWT token, validates path `user_id` matches authenticated `sub` claim, filters results by authenticated user

#### POST /users/{user_id}/todos
- **Description**: Create a new todo for the authenticated user
- **Authentication**: Required (JWT Bearer token)
- **Path Parameters**:
  - `user_id`: String - user identifier from path
- **Query Parameters**: None
- **Request Body Schema**:
```json
{
  "title": "string",
  "description": "string",
  "priority": "string",
  "due_date": "string"
}
```
- **Response Schema**:
```json
{
  "success": true,
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "status": "pending",
    "priority": "string",
    "due_date": "string",
    "completed_at": "string",
    "created_at": "string",
    "updated_at": "string",
    "user_id": "string"
  }
}
```
- **Success Status**: 201 Created
- **Error Statuses**: 401 (Unauthorized), 403 (Forbidden - user_id mismatch)
- **Security Enforcement**: Validates JWT token, validates path `user_id` matches authenticated `sub` claim, sets user_id from authenticated user

#### GET /users/{user_id}/todos/{todo_id}
- **Description**: Get a specific todo for the authenticated user
- **Authentication**: Required (JWT Bearer token)
- **Path Parameters**:
  - `user_id`: String - user identifier from path
  - `todo_id`: String - todo identifier from path
- **Query Parameters**: None
- **Request Body**: None
- **Response Schema**:
```json
{
  "success": true,
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "status": "string",
    "priority": "string",
    "due_date": "string",
    "completed_at": "string",
    "created_at": "string",
    "updated_at": "string",
    "user_id": "string"
  }
}
```
- **Success Status**: 200 OK
- **Error Statuses**: 401 (Unauthorized), 403 (Forbidden - user_id mismatch), 404 (Not Found - todo doesn't exist or doesn't belong to user)
- **Security Enforcement**: Validates JWT token, validates path `user_id` matches authenticated `sub` claim, verifies todo belongs to authenticated user

#### PUT /users/{user_id}/todos/{todo_id}
- **Description**: Update a specific todo for the authenticated user
- **Authentication**: Required (JWT Bearer token)
- **Path Parameters**:
  - `user_id`: String - user identifier from path
  - `todo_id`: String - todo identifier from path
- **Query Parameters**: None
- **Request Body Schema**:
```json
{
  "title": "string",
  "description": "string",
  "status": "string",
  "priority": "string",
  "due_date": "string"
}
```
- **Response Schema**:
```json
{
  "success": true,
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "status": "string",
    "priority": "string",
    "due_date": "string",
    "completed_at": "string",
    "created_at": "string",
    "updated_at": "string",
    "user_id": "string"
  }
}
```
- **Success Status**: 200 OK
- **Error Statuses**: 401 (Unauthorized), 403 (Forbidden - user_id mismatch), 404 (Not Found - todo doesn't exist or doesn't belong to user)
- **Security Enforcement**: Validates JWT token, validates path `user_id` matches authenticated `sub` claim, verifies todo belongs to authenticated user

#### PATCH /users/{user_id}/todos/{todo_id}
- **Description**: Partially update a specific todo for the authenticated user
- **Authentication**: Required (JWT Bearer token)
- **Path Parameters**:
  - `user_id`: String - user identifier from path
  - `todo_id`: String - todo identifier from path
- **Query Parameters**: None
- **Request Body Schema** (any combination of):
```json
{
  "title": "string",
  "description": "string",
  "status": "string",
  "priority": "string",
  "due_date": "string",
  "completed_at": "string"
}
```
- **Response Schema**:
```json
{
  "success": true,
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "status": "string",
    "priority": "string",
    "due_date": "string",
    "completed_at": "string",
    "created_at": "string",
    "updated_at": "string",
    "user_id": "string"
  }
}
```
- **Success Status**: 200 OK
- **Error Statuses**: 401 (Unauthorized), 403 (Forbidden - user_id mismatch), 404 (Not Found - todo doesn't exist or doesn't belong to user)
- **Security Enforcement**: Validates JWT token, validates path `user_id` matches authenticated `sub` claim, verifies todo belongs to authenticated user

#### DELETE /users/{user_id}/todos/{todo_id}
- **Description**: Delete a specific todo for the authenticated user
- **Authentication**: Required (JWT Bearer token)
- **Path Parameters**:
  - `user_id`: String - user identifier from path
  - `todo_id`: String - todo identifier from path
- **Query Parameters**: None
- **Request Body**: None
- **Response Schema**:
```json
{
  "success": true,
  "data": {
    "id": "string",
    "message": "Todo deleted successfully"
  }
}
```
- **Success Status**: 200 OK
- **Error Statuses**: 401 (Unauthorized), 403 (Forbidden - user_id mismatch), 404 (Not Found - todo doesn't exist or doesn't belong to user)
- **Security Enforcement**: Validates JWT token, validates path `user_id` matches authenticated `sub` claim, verifies todo belongs to authenticated user

## Appendix

### Shared Schemas

#### Todo Object
```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "status": "string",
  "priority": "string",
  "due_date": "string",
  "completed_at": "string",
  "created_at": "string",
  "updated_at": "string",
  "user_id": "string"
}
```

#### User Object
```json
{
  "id": "string",
  "email": "string",
  "username": "string",
  "created_at": "string",
  "updated_at": "string"
}
```

### Priority Values
- `low`
- `medium`
- `high`
- `urgent`

### Status Values
- `pending`
- `in_progress`
- `completed`
- `archived`