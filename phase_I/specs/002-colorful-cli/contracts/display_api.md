# Display API Contracts

**Feature**: 002-colorful-cli
**Date**: 2026-01-01
**Version**: 1.0.0

## Overview

This document defines the API contracts for all display and formatting functions. These functions transform domain data (Task entities) into colored, formatted terminal output.

---

## Color Utilities API

### Module: `src/utils/colors.py`

#### Function: `get_console()`

**Purpose**: Get or create the singleton Rich Console instance

**Signature**:
```python
def get_console() -> Console
```

**Inputs**: None

**Outputs**:
- **Type**: `rich.console.Console`
- **Description**: Singleton console instance with automatic terminal detection

**Behavior**:
- Creates Console instance on first call
- Returns same instance on subsequent calls
- Console automatically detects terminal capabilities

**Error Conditions**: None (cannot fail)

**Example**:
```python
console = get_console()
console.print("[bold]Hello[/bold]")
```

---

#### Constant: `COLOR_SCHEME`

**Purpose**: Define consistent color mappings for all application output

**Type**: Dictionary

**Structure**:
```python
COLOR_SCHEME = {
    "success": "green",
    "error": "red",
    "info": "blue",
    "warning": "yellow",
    "heading": "bold cyan",
    "subheading": "cyan",
    "priority_high": "red",
    "priority_medium": "yellow",
    "priority_low": "green",
    "completed": "dim white",
    "incomplete": "white",
    "table_header": "bold magenta",
    "table_border": "dim"
}
```

**Usage**:
```python
from src.utils.colors import COLOR_SCHEME

console.print(f"[{COLOR_SCHEME['success']}]Task added![/{COLOR_SCHEME['success']}]")
```

---

## Welcome Message API

### Module: `src/cli/welcome.py`

#### Function: `display_welcome_message()`

**Purpose**: Display colorful welcome screen when application starts

**Signature**:
```python
def display_welcome_message() -> None
```

**Inputs**: None

**Outputs**: None (prints to console)

**Behavior**:
- Displays ASCII art banner with cyan color
- Shows application subtitle in dim style
- Shows help hint in info color
- Uses Rich Console for output

**Side Effects**:
- Writes colored text to stdout
- Output automatically adapts to terminal capabilities

**Error Conditions**: None (gracefully handles non-color terminals)

**Console Output Example**:
```
╔════════════════════════════════════╗
║      Welcome to Todo CLI App       ║
╚════════════════════════════════════╝

Manage your tasks efficiently from the command line

Type 'todo --help' for available commands
```

**Example Usage**:
```python
# In main.py
from src.cli.welcome import display_welcome_message

def main():
    display_welcome_message()
    # ... rest of CLI logic
```

---

## Table Formatting API

### Module: `src/cli/formatting.py`

#### Function: `create_task_table()`

**Purpose**: Create a Rich Table with colored headers for displaying tasks

**Signature**:
```python
def create_task_table(
    tasks: List[Dict[str, str]],
    show_all_columns: bool = True
) -> Table
```

**Inputs**:
- `tasks`: List of task dictionaries with keys:
  - `id` (str): Task ID
  - `task` (str): Task title/description
  - `priority` (str): "High", "Medium", or "Low" (optional)
  - `status` (str): "Complete" or "Incomplete"
  - `due_date` (str): Due date string (optional)
- `show_all_columns` (bool): Whether to show all columns or minimal set

**Outputs**:
- **Type**: `rich.table.Table`
- **Description**: Formatted table with colored headers and styled rows

**Behavior**:
- Creates table with magenta headers
- Applies column-specific colors:
  - ID: cyan
  - Task: white
  - Priority: red/yellow/green based on value
  - Status: dim white (complete) or white (incomplete)
  - Due Date: blue
- Handles text wrapping/truncation for long task descriptions
- Applies consistent spacing and borders

**Error Conditions**:
- If `tasks` is empty, returns empty table (still shows headers)
- If task dict missing required keys, raises `ValueError`

**Example**:
```python
from src.cli.formatting import create_task_table

tasks_data = [
    {"id": "1", "task": "Buy groceries", "priority": "High", "status": "Incomplete"},
    {"id": "2", "task": "Write report", "priority": "Medium", "status": "Complete"}
]

table = create_task_table(tasks_data)
console = get_console()
console.print(table)
```

**Console Output Example**:
```
┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ ID ┃ Task           ┃ Priority ┃ Status     ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━┩
│  1 │ Buy groceries  │ High     │ Incomplete │
│  2 │ Write report   │ Medium   │ Complete   │
└────┴────────────────┴──────────┴────────────┘
```

---

#### Function: `format_task_row()`

**Purpose**: Format a single task for display in list or table format

**Signature**:
```python
def format_task_row(task: Task) -> Dict[str, str]
```

**Inputs**:
- `task`: Task entity from domain model

**Outputs**:
- **Type**: Dictionary with string values
- **Keys**: `id`, `task`, `priority`, `status`
- **Example**:
  ```python
  {
      "id": "1",
      "task": "Buy groceries",
      "priority": "High",
      "status": "Incomplete"
  }
  ```

**Behavior**:
- Converts Task entity to display-friendly dictionary
- Maps `completed` boolean to "Complete"/"Incomplete" string
- Extracts priority from task (if available, else "N/A")
- Truncates long task titles (>50 chars) with "..."

**Error Conditions**:
- If `task` is None, raises `ValueError`
- If `task` missing required fields, raises `AttributeError`

**Example**:
```python
from src.models.task import Task
from src.cli.formatting import format_task_row

task = Task(id=1, title="Buy groceries", description="", completed=False)
row = format_task_row(task)
# Returns: {"id": "1", "task": "Buy groceries", "priority": "N/A", "status": "Incomplete"}
```

---

## Display Functions API

### Module: `src/cli/display.py`

#### Function: `display_tasks_as_list()`

**Purpose**: Display tasks as a colored list (not table format)

**Signature**:
```python
def display_tasks_as_list(tasks: List[Task]) -> None
```

**Inputs**:
- `tasks`: List of Task entities

**Outputs**: None (prints to console)

**Behavior**:
- Prints each task with colored status indicator
- Groups tasks by completion status (incomplete first, then completed)
- Uses section headings with colored text
- Formats: `[priority_color]• Task title[/priority_color] (Status)`

**Side Effects**: Writes to stdout

**Error Conditions**:
- If `tasks` is empty, displays "No tasks found" message
- Gracefully handles None values in task fields

**Console Output Example**:
```
Incomplete Tasks:
• Buy groceries (High Priority)
• Write report (Medium Priority)

Completed Tasks:
• Call dentist (Low Priority)
```

**Example Usage**:
```python
from src.services.task_manager import TaskManager
from src.cli.display import display_tasks_as_list

manager = TaskManager()
tasks = manager.list_all_tasks()
display_tasks_as_list(tasks)
```

---

#### Function: `display_tasks_as_table()`

**Purpose**: Display tasks as a formatted table with colored headers

**Signature**:
```python
def display_tasks_as_table(tasks: List[Task]) -> None
```

**Inputs**:
- `tasks`: List of Task entities

**Outputs**: None (prints to console)

**Behavior**:
- Converts tasks to display format using `format_task_row()`
- Creates table using `create_task_table()`
- Prints table via Rich Console
- Shows all columns by default

**Side Effects**: Writes to stdout

**Error Conditions**:
- If `tasks` is empty, displays empty table with headers
- Gracefully handles missing task fields

**Console Output**: See `create_task_table()` example

**Example Usage**:
```python
from src.services.task_manager import TaskManager
from src.cli.display import display_tasks_as_table

manager = TaskManager()
tasks = manager.list_all_tasks()
display_tasks_as_table(tasks)
```

---

#### Function: `display_success_message()`

**Purpose**: Display success message in green color

**Signature**:
```python
def display_success_message(message: str) -> None
```

**Inputs**:
- `message` (str): Success message text

**Outputs**: None (prints to console)

**Behavior**:
- Wraps message in green color
- Prepends checkmark symbol (✓)
- Uses Rich Console for output

**Console Output Example**:
```
✓ Task added successfully!
```

**Example Usage**:
```python
from src.cli.display import display_success_message

display_success_message("Task added successfully!")
```

---

#### Function: `display_error_message()`

**Purpose**: Display error message in red color

**Signature**:
```python
def display_error_message(message: str) -> None
```

**Inputs**:
- `message` (str): Error message text

**Outputs**: None (prints to console)

**Behavior**:
- Wraps message in red color
- Prepends cross symbol (✗)
- Uses Rich Console for output

**Console Output Example**:
```
✗ Task not found
```

**Example Usage**:
```python
from src.cli.display import display_error_message

display_error_message("Task not found")
```

---

#### Function: `display_info_message()`

**Purpose**: Display informational message in blue color

**Signature**:
```python
def display_info_message(message: str) -> None
```

**Inputs**:
- `message` (str): Info message text

**Outputs**: None (prints to console)

**Behavior**:
- Wraps message in blue color
- Prepends info symbol (ℹ)
- Uses Rich Console for output

**Console Output Example**:
```
ℹ No tasks match your query
```

**Example Usage**:
```python
from src.cli.display import display_info_message

display_info_message("No tasks match your query")
```

---

## Integration Contracts

### Updated Command Flow

**Before (existing)**:
```python
# src/cli/commands.py
def add_task(title: str, description: str = ""):
    task = manager.add_task(title, description)
    print(f"Task added: {task.title}")  # Plain text
```

**After (with colors)**:
```python
# src/cli/commands.py
from src.cli.display import display_success_message, display_tasks_as_table

def add_task(title: str, description: str = ""):
    task = manager.add_task(title, description)
    display_success_message(f"Task added: {task.title}")
    display_tasks_as_table([task])  # Show new task in table
```

### Main Entry Point

**Before**:
```python
# src/main.py
def main():
    # Start CLI directly
    cli()
```

**After**:
```python
# src/main.py
from src.cli.welcome import display_welcome_message

def main():
    display_welcome_message()  # Show colored welcome
    cli()
```

---

## Testing Contracts

### Unit Test Interface

```python
# tests/unit/test_display.py

def test_format_task_row():
    """Test task formatting with mock Task"""
    task = Mock(id=1, title="Test", description="", completed=False)
    row = format_task_row(task)
    assert row["id"] == "1"
    assert row["status"] == "Incomplete"

def test_create_task_table_empty():
    """Test table creation with no tasks"""
    table = create_task_table([])
    assert table.row_count == 0
    assert len(table.columns) > 0  # Headers still present

def test_display_success_message_no_color(capsys):
    """Test success message in no-color mode"""
    import os
    os.environ["NO_COLOR"] = "1"
    display_success_message("Test")
    captured = capsys.readouterr()
    assert "Test" in captured.out
```

---

## Dependency Requirements

**pyproject.toml**:
```toml
dependencies = [
    "rich>=13.0.0",
]
```

**Import Structure**:
```python
# All display code imports from rich
from rich.console import Console
from rich.table import Table
```

---

## Backward Compatibility

**Existing Functions**:
- All existing display functions in `src/cli/display.py` remain available
- Old plain-text functions still work (but updated internally to use colors)
- No breaking changes to public API

**Migration Path**:
- Replace `print()` calls with `console.print()` gradually
- Replace plain display functions with colored equivalents
- Update command functions to use new display API

---

## Error Handling Contract

**Principle**: Display functions never crash the application

**Error Behavior**:
1. Invalid inputs → Log warning, display fallback message
2. Terminal errors → Fall back to plain text automatically (Rich handles this)
3. Missing task fields → Display "N/A" or skip column

**Example**:
```python
def format_task_row(task: Task) -> Dict[str, str]:
    try:
        # Normal formatting
        return {"id": str(task.id), "task": task.title, ...}
    except AttributeError as e:
        # Fallback for missing fields
        return {"id": "?", "task": "Invalid Task", "status": "Error"}
```

---

## Performance Contracts

**Constraints** (from research.md):
- Display rendering: < 50ms for 100 tasks
- No noticeable delay in colored output vs plain text

**Implementation Requirements**:
- Rich Console is lightweight (minimal overhead)
- Table creation is O(n) where n = number of tasks
- No network calls or heavy computation in display functions

**Measurement**:
```python
import time

start = time.perf_counter()
display_tasks_as_table(tasks)
elapsed = (time.perf_counter() - start) * 1000
assert elapsed < 50, f"Display took {elapsed}ms (should be < 50ms)"
```

---

## Summary

This API contract defines:
- ✅ 3 utility modules (colors, terminal, formatting)
- ✅ 2 display modules (welcome, display)
- ✅ 10 public functions with clear signatures
- ✅ 1 configuration constant (COLOR_SCHEME)
- ✅ Integration points with existing commands
- ✅ Error handling and performance contracts
- ✅ Testing interface requirements

All contracts are deterministic, testable, and aligned with Phase I Constitution principles.
