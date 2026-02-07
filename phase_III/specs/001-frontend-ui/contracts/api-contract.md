# API Contracts for Frontend UI

## Authentication Endpoints

### POST /api/auth/register
Register a new user account

**Request Body**:
```json
{
  "email": "string",
  "password": "string",
  "name": "string"
}
```

**Responses**:
- 200: User registered successfully
- 400: Invalid input data
- 409: User already exists

### POST /api/auth/login
Login with existing credentials

**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Responses**:
- 200: Login successful, returns JWT tokens
- 400: Invalid input data
- 401: Invalid credentials

### POST /api/auth/logout
Logout current user

**Headers**:
- Authorization: Bearer {token}

**Responses**:
- 200: Logout successful
- 401: Unauthorized

## Task Management Endpoints

### GET /api/tasks
Retrieve all tasks for authenticated user

**Headers**:
- Authorization: Bearer {token}

**Query Parameters**:
- page (optional): Page number for pagination
- limit (optional): Number of items per page
- status (optional): Filter by completion status ('all', 'completed', 'pending')
- priority (optional): Filter by priority ('low', 'medium', 'high')

**Responses**:
- 200: Array of tasks
```json
{
  "data": [
    {
      "id": "string",
      "userId": "string",
      "title": "string",
      "description": "string",
      "priority": "low|medium|high",
      "completed": "boolean",
      "createdAt": "ISO date string",
      "updatedAt": "ISO date string"
    }
  ],
  "pagination": {
    "page": "number",
    "limit": "number",
    "total": "number",
    "totalPages": "number"
  }
}
```
- 401: Unauthorized
- 500: Internal server error

### POST /api/tasks
Create a new task for authenticated user

**Headers**:
- Authorization: Bearer {token}

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "priority": "low|medium|high",
  "completed": "boolean"
}
```

**Responses**:
- 201: Task created successfully
```json
{
  "id": "string",
  "userId": "string",
  "title": "string",
  "description": "string",
  "priority": "low|medium|high",
  "completed": "boolean",
  "createdAt": "ISO date string",
  "updatedAt": "ISO date string"
}
```
- 400: Invalid input data
- 401: Unauthorized
- 500: Internal server error

### GET /api/tasks/{id}
Retrieve a specific task by ID

**Headers**:
- Authorization: Bearer {token}

**Parameters**:
- id: Task ID

**Responses**:
- 200: Task data
- 401: Unauthorized
- 404: Task not found
- 500: Internal server error

### PUT /api/tasks/{id}
Update a specific task by ID

**Headers**:
- Authorization: Bearer {token}

**Parameters**:
- id: Task ID

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "priority": "low|medium|high",
  "completed": "boolean"
}
```

**Responses**:
- 200: Task updated successfully
- 400: Invalid input data
- 401: Unauthorized
- 404: Task not found
- 500: Internal server error

### DELETE /api/tasks/{id}
Delete a specific task by ID

**Headers**:
- Authorization: Bearer {token}

**Parameters**:
- id: Task ID

**Responses**:
- 204: Task deleted successfully
- 401: Unauthorized
- 404: Task not found
- 500: Internal server error

### PATCH /api/tasks/{id}/complete
Toggle task completion status

**Headers**:
- Authorization: Bearer {token}

**Parameters**:
- id: Task ID

**Request Body**:
```json
{
  "completed": "boolean"
}
```

**Responses**:
- 200: Task status updated
```json
{
  "id": "string",
  "completed": "boolean",
  "updatedAt": "ISO date string"
}
```
- 400: Invalid input data
- 401: Unauthorized
- 404: Task not found
- 500: Internal server error

## Error Response Format

All error responses follow this format:
```json
{
  "success": false,
  "error": "string",
  "message": "string"
}
```

## Authentication Headers

All authenticated endpoints require the Authorization header:
- `Authorization: Bearer {jwt_token}`

## Success Response Format

Successful responses (except 204) follow this format:
```json
{
  "success": true,
  "data": {},
  "message": "string"
}
```

## Rate Limiting

All endpoints are subject to rate limiting:
- 100 requests per minute per IP
- 429 response code when limit exceeded