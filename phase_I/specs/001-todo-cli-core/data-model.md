# Data Model: Todo CLI Core Functionality

**Purpose**: Define Task entity structure, validation rules, and state management interfaces
**Date**: 2026-01-01

## Task Entity

### Fields

| Field         | Type       | Constraint                   | Default | Description |
|--------------|------------|-----------------------------|----------|-------------|
| `id`          | int        | immutable, unique, >= 1  | generated | Sequential identifier for task |
| `title`        | str        | required, non-empty, non-whitespace | N/A     | Task name or summary |
| `description`  | str or null| optional                     | None     | Detailed task information |
| `completed`    | bool       | required                   | False    | Task completion status |

### Immutable Fields
- `id`: Generated once at creation, never changes

### Mutable Fields
- `title`: Can be updated, must remain non-empty and non-whitespace
- `description`: Can be updated, set, or removed (null)
- `completed`: Can be toggled between True and False

## Validation Rules

### Title Validation
- **Required**: Must be provided on task creation
- **Non-empty**: Cannot be empty string ""
- **Non-whitespace**: Cannot contain only whitespace characters
- **Type**: Must be string
- **Error**: "Title is required and cannot be empty or whitespace only"

### ID Validation
- **Required**: Must be provided for update, delete, and complete operations
- **Type**: Must be integer
- **Exists**: Must correspond to an existing task
- **Not deleted**: Task must not already deleted (if soft delete is implemented)
- **Range**: Must be positive (> 0)
- **Error**: "Task not found: {id}" or "Invalid task ID: {id}"

### Description Validation
- **Optional**: Can be None or empty string
- **Type**: Must be string or None
- **Update**: Can be set to empty string to remove description

## State Operations

### Create Task

**Input**: title (required), description (optional)

**Process**:
1. Validate title is non-empty and non-whitespace
2. Generate unique sequential ID
3. Set completed = False
4. Set description = provided value or None
5. Add to in-memory storage

**Output**: Created task with generated ID

**Errors**: Title validation failure

---

### Update Task

**Input**: id (required), title (optional), description (optional)

**Process**:
1. Validate ID exists and is not deleted
2. Validate title if provided (non-empty, non-whitespace)
3. Update provided fields only
4. Do not modify id or completed fields
5. Keep unchanged fields as-is

**Output**: Updated task

**Errors**: ID not found, title validation failure

---

### Delete Task

**Input**: id (required)

**Process**:
1. Validate ID exists
2. Remove task from storage permanently
3. Cannot be recovered

**Output**: Success message

**Errors**: ID not found

---

### Toggle Complete

**Input**: id (required)

**Process**:
1. Validate ID exists and is not deleted
2. Invert completed field (True ↔ False)
3. Update task in storage

**Output**: Updated task with new completion status

**Errors**: ID not found

---

### List Tasks

**Input**: None

**Process**:
1. Retrieve all tasks from storage
2. Filter out deleted tasks (if soft delete implemented)
3. Return list in order of creation (or ID order)

**Output**: List of tasks with all fields

**Errors**: None (empty list if no tasks exist)

---

### Get Task by ID

**Input**: id (required)

**Process**:
1. Validate ID exists and is not deleted
2. Retrieve task from storage

**Output**: Task object

**Errors**: ID not found

## Storage Interface

### In-Memory Storage Structure

```python
# Dictionary with task ID as key for O(1) access
tasks: Dict[int, Task] = {}

# Counter for generating sequential IDs
next_id: int = 1
```

### Storage Operations

- **add(task)**: Insert into tasks dictionary
- **get(id)**: Retrieve from tasks dictionary
- **update(id, updates)**: Modify task in dictionary
- **delete(id)**: Remove from dictionary
- **list()**: Return all values from dictionary
- **exists(id)**: Check if key exists

## Error Types

### Validation Errors
- **EmptyTitleError**: Title is empty or whitespace
- **InvalidIDError**: Task ID is not valid integer or out of range

### Operation Errors
- **TaskNotFoundError**: Task with given ID does not exist
- **TaskAlreadyDeletedError**: Task exists but was already deleted

## State Transitions

Task states are simple and linear:

```
Created (incomplete) ←→ Completed ←→ Incomplete
                          ↑           ↓
                      (toggle_complete operation)
```

No complex state machines or intermediate states in Phase I.
