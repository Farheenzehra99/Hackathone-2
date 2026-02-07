# Phase II Database Schema Specification

## Overview
This document defines the PostgreSQL database schema for the Phase II multi-user todo application using Neon Serverless PostgreSQL backend with SQLModel ORM.

## Assumptions
- Users are authenticated via Better Auth and have unique user IDs
- Multi-tenancy is enforced through application-level filtering on `user_id`
- Soft deletes are not implemented (hard deletes used)
- The application follows a standard user-task relationship model

## Entity Relationship Overview
- Users own multiple tasks (one-to-many relationship)
- Each task belongs to exactly one user
- Access control is enforced by filtering queries by `user_id`

```
Users (1) -----> (*) Tasks
```

## Tables

### users
**Purpose**: Stores user account information for multi-tenant isolation

| Column | Type | Nullable | Default | Constraints |
|--------|------|----------|---------|-------------|
| id | VARCHAR(36) | NOT NULL | `uuid_generate_v4()` | PRIMARY KEY, UNIQUE |
| email | VARCHAR(255) | NOT NULL | N/A | UNIQUE |
| name | VARCHAR(255) | YES | NULL | |
| created_at | TIMESTAMPTZ | YES | CURRENT_TIMESTAMP | |
| updated_at | TIMESTAMPTZ | YES | CURRENT_TIMESTAMP | ON UPDATE |

**Keys & Constraints**:
- Primary Key: `id`
- Unique Constraint: `email`

**Indexes**:
- `idx_users_email`: `(email)` - for authentication lookups
- `idx_users_created_at`: `(created_at DESC)` - for user registration ordering

**Notes**:
- Uses UUID strings as primary key for distributed systems compatibility
- Email is unique across all users
- Updated timestamp automatically managed by triggers/application logic

### tasks
**Purpose**: Stores individual todo tasks owned by users

| Column | Type | Nullable | Default | Constraints |
|--------|------|----------|---------|-------------|
| id | INTEGER | NOT NULL | `nextval('tasks_id_seq')` | PRIMARY KEY |
| title | VARCHAR(255) | NOT NULL | N/A | |
| description | VARCHAR(1000) | YES | NULL | |
| completed | BOOLEAN | NOT NULL | FALSE | |
| user_id | VARCHAR(36) | NOT NULL | N/A | FOREIGN KEY |
| created_at | TIMESTAMPTZ | YES | CURRENT_TIMESTAMP | |
| updated_at | TIMESTAMPTZ | YES | CURRENT_TIMESTAMP | ON UPDATE |

**Keys & Constraints**:
- Primary Key: `id`
- Foreign Key: `user_id` REFERENCES `users(id)` ON DELETE CASCADE
- Check Constraint: `completed IN (TRUE, FALSE)`

**Indexes**:
- `idx_tasks_user_id`: `(user_id)` - for user-specific task queries
- `idx_tasks_user_id_created_at`: `(user_id, created_at DESC)` - for per-user chronological listing
- `idx_tasks_user_id_completed`: `(user_id, completed)` - for filtered task views
- `idx_tasks_completed`: `(completed)` - for global completion status queries

**Notes**:
- Implements multi-tenant isolation via `user_id` foreign key
- ON DELETE CASCADE ensures tasks are removed when user is deleted
- Composite indexes support the most common query patterns

## Isolation Strategy

### Application-Enforced Tenant Isolation
- All user-specific queries must include `WHERE user_id = $current_user_id`
- API endpoints validate that requested resources belong to the authenticated user
- No Row Level Security (RLS) is currently implemented; relies on application-level enforcement

### Required Query Patterns
```sql
-- Per-user task listing
SELECT * FROM tasks WHERE user_id = $current_user_id ORDER BY created_at DESC;

-- Single task lookup with ownership verification
SELECT * FROM tasks WHERE id = $task_id AND user_id = $current_user_id;

-- Count user's tasks
SELECT COUNT(*) FROM tasks WHERE user_id = $current_user_id AND completed = false;
```

## Acceptance Checklist
- [x] Every user-owned table has `user_id` and a FK to users
- [x] Indexes exist for the primary access paths
- [x] Constraints are enforceable in Postgres
- [x] Multi-user isolation strategy is explicitly defined
- [x] Schema is compatible with SQLModel
- [x] Neon serverless considerations are addressed (UUIDs, timestamptz)

## Open Questions
- Should we implement soft deletes for audit purposes?
- Are there any additional indexes needed for complex task filtering (tags, priority, etc.)?
- Should we consider Row Level Security for additional protection?