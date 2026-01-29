# Skill: Todo State Manager

## 1. Purpose
Implement core task state management logic for the Todo CLI application. This skill focuses exclusively on business logic, data models, and state operations without touching user interfaces, APIs, or natural language processing.

## 2. Owned By
Agent: **todo-state-manager**

## 3. When to Use
Invoke this skill when:
- Specification for todo state management has been created and approved
- User needs to implement core task state management logic
- Before implementing CLI or API layers
- Refactoring state management to be more robust or storage-agnostic
- Setting up the foundational task management system

## 4. Input

**Required Input:**
```
feature_spec_path: string
```
Path to the feature specification defining task state requirements.

**Optional Inputs:**
```
output_directory: string (default: "src/core" or project-specific location)
language: string (default: inferred from project structure)
```

**Constraints:**
- Spec must be complete and approved
- Implementation must follow spec exactly
- No feature creep beyond spec requirements
- Storage-agnostic design (Phase I: in-memory)

## 5. Step-by-Step Process

### Step 1: Read and Parse Specification
Read the feature specification to understand requirements.

**Parsing Actions:**
- Read task model requirements (fields, types, constraints)
- Identify required operations (create, update, delete, etc.)
- Extract validation rules
- Note error handling requirements
- Understand business logic requirements

**Completeness Check:**
- If spec is incomplete or ambiguous:
  - Identify missing specifications
  - Ask clarifying questions
  - Do not assume or infer requirements

### Step 2: Define Task Data Model
Create the task data model according to specification.

**Model Requirements:**

**Immutable Fields:**
- `id`: Unique identifier (string or number)
  - Generated on creation
  - Never changes
  - Must be unique across all tasks

**Mutable Fields:**
- `title`: Required string, non-empty
  - Task name or summary
  - Must be non-empty on creation
  - Can be updated

- `description`: Optional string
  - Detailed task information
  - Can be null or empty string
  - Can be updated

- `completed`: Boolean, defaults to false
  - Task completion status
  - Can be toggled

- `priority`: Optional (e.g., "low", "medium", "high")
  - Task importance or urgency
  - Must match allowed values if implemented
  - Can be updated

- `due_date`: Optional date/timestamp
  - Task deadline
  - Must be valid date if present
  - Can be updated

**Internal Fields (for state tracking):**
- `created_at`: Timestamp of task creation
- `updated_at`: Timestamp of last modification
- `deleted`: Boolean flag for soft deletion

### Step 3: Implement Storage Layer
Create storage-agnostic storage interface.

**Phase I Implementation:**
- Use in-memory storage (array, Map, or object)
- Simple implementation: Map<string, Task> for O(1) lookups
- Separate deleted tasks from active tasks

**Storage Requirements:**
- Methods: add, get, update, delete, list
- Support filtering capabilities
- Maintain deleted tasks separate from active
- Easy to extend for database storage later

**Storage Interface:**
```typescript
interface TaskStorage {
  add(task: Task): void
  get(id: string): Task | null
  update(id: string, updates: Partial<Task>): Task | null
  delete(id: string): boolean
  list(): Task[]
}
```

### Step 4: Implement Validation Logic
Create validation functions for task operations.

**Creation Validation:**
- Title must be non-empty
- Due date must be valid (if provided)
- Priority must match allowed values (if provided)
- No validation for description (optional)

**Update Validation:**
- Task must exist and not be deleted
- Cannot modify immutable fields (id, created_at)
- Title must be non-empty if updating title
- Due date must be valid if updating
- Priority must match allowed values if updating

**Delete Validation:**
- Task must exist
- Task must not already be deleted

**General Validation:**
- ID must be valid string or number
- All required fields present

### Step 5: Implement Core Operations
Implement required state management operations.

**Operation 1: create_task(title, description?, priority?, due_date?)**
- Generate unique ID
- Create task object with all fields
- Validate required fields
- Set defaults (completed: false, timestamps)
- Add to storage
- Return created task
- Throw error on validation failure

**Operation 2: update_task(id, updates)**
- Validate task exists and not deleted
- Validate ID is not in updates (immutable)
- Validate each update field
- Apply updates to task
- Update updated_at timestamp
- Update in storage
- Return updated task
- Throw error if task not found, deleted, or validation fails

**Operation 3: delete_task(id)**
- Validate task exists and not deleted
- Mark task as deleted (set deleted=true)
- Remove from active task list
- Keep in storage for reference
- Throw error if task not found or already deleted

**Operation 4: toggle_complete(id)**
- Validate task exists and not deleted
- Toggle completed status (true ↔ false)
- Update updated_at timestamp
- Update in storage
- Return updated task
- Throw error if task not found or deleted

**Operation 5: list_tasks(filters?)**
- Retrieve all non-deleted tasks
- Apply optional filters:
  - completed status (true/false)
  - priority (specific value)
  - due date (before/after/specific)
- Return filtered list
- Return empty list if no tasks match

**Operation 6: get_task_by_id(id)**
- Validate task exists and not deleted
- Return task object
- Throw error if task not found or deleted

### Step 6: Implement Error Handling
Create structured error types and messages.

**Error Types:**

**TaskNotFoundError:**
- Task with given ID not found
- HTTP status: 404
- Message: "Task not found: {id}"

**TaskAlreadyDeletedError:**
- Task exists but is already deleted
- HTTP status: 400
- Message: "Task already deleted: {id}"

**ValidationError:**
- Validation rule failed
- HTTP status: 400
- Message: Specific to validation failure (e.g., "Title cannot be empty")

**DuplicateIdError:**
- Attempt to create task with existing ID
- HTTP status: 400
- Message: "Task with ID {id} already exists"

**ImmutableFieldError:**
- Attempt to modify immutable field
- HTTP status: 400
- Message: "Cannot modify immutable field: {field}"

**Error Structure:**
```typescript
interface TaskError {
  code: string
  message: string
  context?: {
    operation: string
    field?: string
    value?: any
  }
}
```

### Step 7: Create Types and Interfaces
Define TypeScript types (if using TypeScript).

**Core Types:**
```typescript
type Priority = 'low' | 'medium' | 'high'

interface Task {
  id: string
  title: string
  description?: string
  completed: boolean
  priority?: Priority
  due_date?: string | Date
  created_at: string | Date
  updated_at: string | Date
  deleted: boolean
}

interface CreateTaskInput {
  title: string
  description?: string
  priority?: Priority
  due_date?: string | Date
}

interface UpdateTaskInput {
  title?: string
  description?: string
  completed?: boolean
  priority?: Priority
  due_date?: string | Date
}

interface TaskFilters {
  completed?: boolean
  priority?: Priority
  due_date_before?: string | Date
  due_date_after?: string | Date
}
```

### Step 8: Write Unit Tests
Create tests for all operations.

**Test Coverage:**
- Test each operation success path
- Test each error condition
- Test edge cases (empty lists, boundary values)
- Test validation rules

**Test Examples:**
- create_task with valid input
- create_task with empty title (should fail)
- update_task existing task
- update_task non-existent task (should fail)
- delete_task existing task
- delete_task already deleted (should fail)
- toggle_complete multiple times
- list_tasks with and without filters
- get_task_by_id for existing and non-existent

## 6. Output

**Output Files:**

1. **Task Model**: `src/models/task.ts` or similar
   - Task interface/type definition
   - Input types for create/update
   - Filter types

2. **Storage Layer**: `src/storage/task-storage.ts` or similar
   - TaskStorage interface
   - In-memory implementation
   - Storage operations

3. **State Manager**: `src/core/task-manager.ts` or similar
   - All six required operations
   - Error handling
   - Validation logic

4. **Errors**: `src/errors/task-errors.ts` or similar
   - Error types/interfaces
   - Error factory functions

5. **Tests**: `src/core/task-manager.test.ts` or similar
   - Unit tests for all operations
   - Test coverage for error cases

**Output Constraints:**
- Only code related to state management
- No CLI, API, or NLP code
- No database-specific logic (Phase I)
- Clean, modular architecture
- Follow project coding standards

## 7. Failure Handling

### Specification Issues
- If spec is incomplete:
  - Identify missing requirements
  - Ask clarifying questions
  - Do not implement missing features

### Implementation Errors
- If implementation fails validation:
  - Identify validation failure
  - Fix implementation
  - Re-test

### Test Failures
- If tests fail:
  - Identify failing test
  - Debug implementation
  - Fix and re-test

**Non-Destructive Behavior:**
- Never implement CLI or API code
- Never add features beyond specification
- Never modify unrelated code
- Fail gracefully on specification issues

**Quality Assurance:**
- All six required operations implemented
- Task model matches specification
- Validation rules enforced
- Error handling comprehensive
- Storage-agnostic design maintained
- No CLI/API/NLP code present
- Tests cover all operations and edge cases
