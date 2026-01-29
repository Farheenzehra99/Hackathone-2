# CLI Interface Contract

**Purpose**: Define command-line interface specifications for user interactions
**Date**: 2026-01-01

## Command Structure

### Application Entry Point

```
python main.py [command] [arguments]
```

### Commands

All commands are case-sensitive and must be one of the following:

## 1. Add Task

**Command**: `add`

**Arguments**:
```
add <title> [--description <description>]
```

**Required Arguments**:
- `title`: Task title (string, non-empty, non-whitespace)

**Optional Arguments**:
- `--description` / `-d`: Task description (string, optional)

**Examples**:
```
python main.py add "Buy groceries"
python main.py add "Write report" --description "Quarterly sales report"
python main.py add "Meeting" -d "Team sync at 2pm"
```

**Success Output**:
```
Task created successfully.
ID: 1
Title: Buy groceries
Status: Incomplete
```

**Error Output**:
```
Error: Title is required and cannot be empty or whitespace only.
```

---

## 2. View Task List

**Command**: `list`

**Arguments**:
```
list
```

**Required Arguments**: None

**Optional Arguments**: None (all tasks listed)

**Examples**:
```
python main.py list
```

**Success Output (with tasks)**:
```
Your Tasks:

[✓] 1: Buy groceries (Weekly shopping list)
[ ] 2: Write report
[ ] 3: Call mom
```

**Success Output (empty)**:
```
Your Tasks:

No tasks exist. Use 'add' to create your first task.
```

**Error Output**: None (always succeeds)

---

## 3. Mark Task Complete/Incomplete

**Command**: `complete`

**Arguments**:
```
complete <id>
```

**Required Arguments**:
- `id`: Task ID (integer, positive, must exist)

**Optional Arguments**: None

**Examples**:
```
python main.py complete 1
python main.py complete 3
```

**Success Output**:
```
Task marked as complete: Buy groceries
```

**Error Output (not found)**:
```
Error: Task not found: 999
```

**Error Output (invalid ID)**:
```
Error: Invalid task ID: abc
```

---

## 4. Update Task

**Command**: `update`

**Arguments**:
```
update <id> [--title <title>] [--description <description>]
```

**Required Arguments**:
- `id`: Task ID (integer, positive, must exist)

**Optional Arguments**:
- `--title` / `-t`: New task title (string, non-empty, non-whitespace)
- `--description` / `-d`: New task description (string, optional)
- At least one of --title or --description must be provided

**Examples**:
```
python main.py update 1 --title "Buy groceries and milk"
python main.py update 1 -d "Weekly shopping list"
python main.py update 1 -t "Buy groceries" -d "Weekly list"
```

**Success Output**:
```
Task updated successfully.
ID: 1
Title: Buy groceries and milk
Description: Weekly shopping list
```

**Error Output (not found)**:
```
Error: Task not found: 999
```

**Error Output (empty title)**:
```
Error: Title is required and cannot be empty or whitespace only.
```

**Error Output (no updates)**:
```
Error: At least one of --title or --description must be provided.
```

---

## 5. Delete Task

**Command**: `delete`

**Arguments**:
```
delete <id>
```

**Required Arguments**:
- `id`: Task ID (integer, positive, must exist)

**Optional Arguments**: None

**Examples**:
```
python main.py delete 1
python main.py delete 3
```

**Success Output**:
```
Task deleted successfully: Buy groceries
```

**Error Output (not found)**:
```
Error: Task not found: 999
```

**Error Output (invalid ID)**:
```
Error: Invalid task ID: abc
```

---

## 6. Help

**Command**: `help` or no command

**Arguments**:
```
help
```

**Required Arguments**: None

**Success Output**:
```
Todo CLI - Phase I

Commands:
  add <title> [--description <text>]      Create a new task
  list                                      View all tasks
  complete <id>                            Mark task as complete
  update <id> [--title] [--description] Update existing task
  delete <id>                              Delete a task
  help                                      Show this help message

Examples:
  python main.py add "Buy groceries"
  python main.py add "Meeting" -d "Team sync"
  python main.py list
  python main.py complete 1
  python main.py update 1 --title "New title"
  python main.py delete 1
```

---

## Common Error Messages

All error messages must:
- Start with "Error:" prefix
- Be clear and user-friendly
- Explain what went wrong
- Suggest corrective action when applicable

### Error Message Examples

```
Error: Title is required and cannot be empty or whitespace only.
Error: Task not found: 999
Error: Invalid task ID: abc
Error: At least one of --title or --description must be provided.
```

## Output Format Standards

### Task Display Format

Each task in list output follows this format:

```
[STATUS] ID: Title (Description if present)
```

Where:
- `[STATUS]`: `[✓]` for completed, `[ ]` for incomplete
- `ID`: Task's unique identifier
- `Title`: Task title
- `Description`: Optional, shown in parentheses if present

### Success Message Format

```
<action> successfully.
ID: <id>
<Field>: <value>
...
```

### Error Message Format

```
Error: <clear, user-friendly message>
```

No technical jargon, stack traces, or system error codes in user-facing output.
