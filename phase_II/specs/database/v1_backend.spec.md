# Database Schema Specification - Todo Application v1.0

## Metadata
- **Version**: 1.0
- **Created**: 2026-01-18
- **Database System**: Neon PostgreSQL with SQLModel
- **Technology**: Python SQLModel ORM
- **Status**: Production Ready

## Overview
This specification defines the database schema for the multi-user todo application backend. The schema implements proper user isolation, efficient querying through indexing, and follows best practices for data integrity and performance.

## Database Configuration

### Connection Details
- **Database URL**: `postgresql+psycopg://neondb_owner:npg_H48eIOvjDREM@ep-blue-hall-ahvfu7pz-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require`
- **Driver**: asyncpg (via SQLAlchemy async engine)
- **Pool Size**: 20 connections
- **Max Overflow**: 30 connections
- **Connection Recycle**: 300 seconds
- **Pool Pre-ping**: Enabled

### Async Engine Setup
```python
from sqlalchemy.ext.asyncio import create_async_engine
import os

engine = create_async_engine(
    os.getenv("DATABASE_URL"),
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False  # Set to True for debugging
)
```

## Table Definitions

### Users Table
The users table stores user account information, compatible with Better Auth integration.

#### Schema
```sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Unique user identifier, compatible with Better Auth |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| name | VARCHAR(255) | Nullable | User's display name |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

#### Indexes
```sql
-- Primary key index (automatically created)
-- Unique constraint on email
CREATE INDEX idx_users_email ON users(email);
```

#### SQLModel Definition
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class UserBase(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class User(UserBase, table=True):
    __tablename__ = "users"

    # Indexes
    __table_args__ = (
        Index("idx_user_email", "email"),
    )
```

### Tasks Table
The tasks table stores todo items with proper foreign key relationships to users.

#### Schema
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-incrementing task identifier |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | Nullable | Task description (optional) |
| completed | BOOLEAN | DEFAULT FALSE | Task completion status |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY | Reference to user who owns the task |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record last update timestamp |

#### Indexes
```sql
-- Primary key index (automatically created)
-- Foreign key index for user_id
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
-- Index for completed status
CREATE INDEX idx_tasks_completed ON tasks(completed);
-- Composite index for user_id and completed for common queries
CREATE INDEX idx_tasks_user_completed ON tasks(user_id, completed);
-- Composite index for efficient filtering
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

#### SQLModel Definition
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .user_model import User

class TaskBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: str = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    # Relationships
    user: "User" = Relationship(back_populates="tasks")

    # Indexes
    __table_args__ = (
        Index("idx_task_user_id", "user_id"),
        Index("idx_task_completed", "completed"),
        Index("idx_task_user_completed", "user_id", "completed"),
        Index("idx_task_created_at", "created_at", postgresql_ops={"created_at": "DESC"}),
    )
```

## Relationship Mapping

### User-Task Relationship
- **Relationship Type**: One-to-Many (One user can have many tasks)
- **Foreign Key**: `tasks.user_id` references `users.id`
- **Cascade Behavior**: ON DELETE CASCADE (deleting a user removes all their tasks)
- **Back Reference**: `User.tasks` provides access to user's tasks

### SQLModel Relationship Definition
```python
# In User model
tasks: List["Task"] = Relationship(back_populates="user")

# In Task model
user: "User" = Relationship(back_populates="tasks")
```

## Indexing Strategy

### Primary Indexes
- **users.id**: Primary key index for user identification
- **tasks.id**: Primary key index for task identification

### Secondary Indexes
- **users.email**: Unique index for email lookup and uniqueness
- **tasks.user_id**: Index for efficient user-based filtering
- **tasks.completed**: Index for completion status filtering
- **tasks.user_id, tasks.completed**: Composite index for combined filtering

### Query Optimization Indexes
- **tasks.created_at**: Index for chronological sorting and filtering
- **tasks.updated_at**: Index for tracking recent updates

## Data Integrity Constraints

### Referential Integrity
- Foreign key constraint ensures tasks always reference valid users
- Cascade delete removes tasks when user is deleted
- Prevents orphaned records in tasks table

### Uniqueness Constraints
- Email addresses must be unique across all users
- Primary keys ensure record uniqueness

### Check Constraints
- Title length validation (max 255 characters)
- Description length validation (max 1000 characters)
- Boolean values for completed field

## Security Considerations

### Data Isolation
- Foreign key relationships enforce user-task association
- Application layer must validate user ownership before operations
- No direct cross-user access without proper authorization

### Audit Trail
- `created_at` and `updated_at` fields track record lifecycle
- Timestamps stored in UTC for consistency
- Immutable creation timestamp

## Performance Guidelines

### Query Optimization
- Use indexed columns in WHERE clauses
- Leverage composite indexes for multi-column filters
- Limit result sets with pagination
- Use EXPLAIN ANALYZE for query performance analysis

### Connection Management
- Implement connection pooling
- Close connections properly after use
- Monitor connection count and performance
- Use async sessions for concurrent operations

## Migration Strategy

### Initial Schema Creation
```python
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### Future Schema Changes
- Use Alembic for database migrations
- Maintain backward compatibility
- Plan for zero-downtime deployments
- Test migrations on staging environment

## Backup and Recovery

### Backup Strategy
- Regular automated backups of Neon PostgreSQL
- Point-in-time recovery enabled
- Offsite backup storage
- Test restore procedures regularly

### Recovery Procedures
- Document recovery steps
- Regular testing of backup restoration
- Minimize data loss windows
- Plan for disaster recovery scenarios

## Monitoring and Maintenance

### Performance Monitoring
- Query execution time tracking
- Connection pool utilization
- Index usage statistics
- Deadlock detection

### Maintenance Tasks
- Regular vacuum and analyze operations
- Index rebuilds when fragmentation occurs
- Statistics updates
- Storage capacity monitoring

## Compliance and Data Governance

### Data Retention
- Define data retention policies
- Automated cleanup procedures
- Audit trail preservation
- GDPR compliance for data deletion

### Access Control
- Role-based access control
- Principle of least privilege
- Regular access reviews
- Secure credential management