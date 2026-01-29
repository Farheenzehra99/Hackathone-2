# Data Model for Frontend UI

## Entities

### User
- **Fields**:
  - id: string (unique identifier from JWT claims)
  - email: string (email address for login)
  - name: string (display name, optional)
  - createdAt: Date (account creation timestamp)
  - updatedAt: Date (last update timestamp)

- **Validation**:
  - Email must be valid email format
  - Name (if provided) must be 1-50 characters
  - ID must be non-empty string

- **State Transitions**:
  - Unauthenticated → Authenticated (login/signup)
  - Authenticated → Unauthenticated (logout)

### Task
- **Fields**:
  - id: string (unique identifier from backend)
  - userId: string (owner of the task, matches JWT claim)
  - title: string (task title)
  - description: string (optional task details)
  - priority: 'low' | 'medium' | 'high' (priority level)
  - completed: boolean (completion status)
  - createdAt: Date (task creation timestamp)
  - updatedAt: Date (last update timestamp)

- **Validation**:
  - Title must be 1-100 characters
  - Description (if provided) must be 0-500 characters
  - Priority must be one of allowed values
  - UserId must match authenticated user's ID

- **State Transitions**:
  - Active → Completed (toggle completion)
  - Completed → Active (toggle completion)
  - Draft → Saved (after creation)

### Session
- **Fields**:
  - userId: string (authenticated user ID)
  - accessToken: string (JWT token)
  - refreshToken: string (refresh token)
  - expiresAt: Date (token expiration time)
  - isAuthenticated: boolean (authentication status)

- **Validation**:
  - Tokens must be non-empty strings
  - Expiration time must be in the future
  - UserId must correspond to valid user

- **State Transitions**:
  - NoSession → ActiveSession (login)
  - ActiveSession → Refreshing (token refresh)
  - ActiveSession/Refreshing → NoSession (logout/expired)

## Relationships

- **User-Task**: One-to-many (one user owns many tasks)
- **Session-User**: One-to-one (one session corresponds to one user at a time)

## Frontend-Specific Models

### TaskFormData
- **Fields**:
  - title: string
  - description: string
  - priority: 'low' | 'medium' | 'high'

- **Validation**:
  - Same as Task entity but without ID or timestamps

### FormErrors
- **Fields**:
  - title?: string[]
  - description?: string[]
  - priority?: string[]
  - general?: string[]

### ToastNotification
- **Fields**:
  - id: string
  - title: string
  - description?: string
  - type: 'success' | 'error' | 'warning' | 'info'
  - duration?: number

## API Response Models

### ApiResponse<T>
- **Fields**:
  - success: boolean
  - data?: T
  - error?: string
  - message?: string

### PaginatedResponse<T>
- **Fields**:
  - data: T[]
  - total: number
  - page: number
  - pageSize: number
  - totalPages: number