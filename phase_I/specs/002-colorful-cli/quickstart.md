# Quickstart Guide: Colorful CLI Interface

**Feature**: 002-colorful-cli
**Audience**: Developers implementing or maintaining this feature
**Date**: 2026-01-01

## Overview

This guide helps you work with the colorful CLI display system. After reading this, you'll know how to:
- Use the color scheme consistently
- Display tasks in colored lists and tables
- Add new colored output to commands
- Test colored output
- Debug terminal compatibility issues

---

## Quick Reference

### Import What You Need

```python
# Get the console singleton
from src.utils.colors import get_console, COLOR_SCHEME

# Display functions
from src.cli.display import (
    display_tasks_as_list,
    display_tasks_as_table,
    display_success_message,
    display_error_message,
    display_info_message
)

# Table formatting
from src.cli.formatting import create_task_table, format_task_row

# Welcome screen
from src.cli.welcome import display_welcome_message
```

### Common Patterns

**Pattern 1: Simple Colored Message**
```python
console = get_console()
console.print(f"[{COLOR_SCHEME['success']}]Operation succeeded![/{COLOR_SCHEME['success']}]")
```

**Pattern 2: Display Task List**
```python
tasks = manager.list_all_tasks()
display_tasks_as_table(tasks)  # Colored table
# OR
display_tasks_as_list(tasks)   # Colored list
```

**Pattern 3: Success/Error Feedback**
```python
try:
    result = manager.add_task("Buy milk")
    display_success_message("Task added successfully!")
    display_tasks_as_table([result])
except Exception as e:
    display_error_message(f"Failed to add task: {e}")
```

---

## Step-by-Step Guides

### Guide 1: Add Color to a New Command

**Scenario**: You're adding a new command and want colored output

**Steps**:

1. **Import display functions**:
   ```python
   from src.cli.display import display_success_message, display_error_message
   from src.utils.colors import get_console, COLOR_SCHEME
   ```

2. **Replace print() with console.print()**:
   ```python
   # Before
   print(f"Found {len(tasks)} tasks")

   # After
   console = get_console()
   console.print(f"[{COLOR_SCHEME['info']}]Found {len(tasks)} tasks[/{COLOR_SCHEME['info']}]")
   ```

3. **Use display functions for feedback**:
   ```python
   # Success
   display_success_message("Command completed successfully")

   # Error
   display_error_message("Command failed: invalid input")

   # Info
   display_info_message("Processing your request...")
   ```

4. **Display data in tables**:
   ```python
   # For task lists
   display_tasks_as_table(tasks)

   # For custom tables
   from src.cli.formatting import create_task_table
   table_data = [
       {"id": "1", "task": "Example", "priority": "High", "status": "Incomplete"}
   ]
   table = create_task_table(table_data)
   console.print(table)
   ```

**Complete Example**:
```python
def search_tasks(query: str):
    """Search tasks and display results with colors"""
    console = get_console()

    # Info message
    display_info_message(f"Searching for: {query}")

    # Perform search
    results = manager.search_tasks(query)

    # Display results
    if results:
        console.print(f"\n[{COLOR_SCHEME['success']}]Found {len(results)} task(s)[/{COLOR_SCHEME['success']}]\n")
        display_tasks_as_table(results)
    else:
        display_info_message("No tasks found matching your query")
```

---

### Guide 2: Update an Existing Command

**Scenario**: Migrate plain-text output to colored output

**Steps**:

1. **Identify print() statements**:
   ```python
   # Find all print() calls in the command function
   print("Task added")
   print(f"Error: {error_message}")
   ```

2. **Map to appropriate display function**:
   - Success messages → `display_success_message()`
   - Error messages → `display_error_message()`
   - Info messages → `display_info_message()`
   - Task lists → `display_tasks_as_list()` or `display_tasks_as_table()`
   - Other → `console.print()` with COLOR_SCHEME

3. **Replace incrementally**:
   ```python
   # Before
   def add_task(title: str):
       task = manager.add_task(title)
       print(f"Task added: {task.title}")

   # After
   def add_task(title: str):
       task = manager.add_task(title)
       display_success_message(f"Task added: {task.title}")
       display_tasks_as_table([task])  # Show the new task
   ```

4. **Test both color and no-color modes**:
   ```bash
   # Test with colors
   todo add "Buy milk"

   # Test without colors
   NO_COLOR=1 todo add "Buy milk"
   ```

---

### Guide 3: Create Custom Colored Output

**Scenario**: You need specialized formatting beyond standard functions

**Steps**:

1. **Use Rich markup syntax**:
   ```python
   console = get_console()
   console.print("[bold cyan]Section Heading[/bold cyan]")
   console.print("[dim]Subtitle or helper text[/dim]")
   console.print("[red]Error details[/red]")
   ```

2. **Combine colors and styles**:
   ```python
   # Bold + colored
   console.print("[bold green]✓[/bold green] Success")

   # Multiple styles
   console.print("[bold yellow on red]WARNING[/bold yellow on red]")
   ```

3. **Use COLOR_SCHEME for consistency**:
   ```python
   # Good - consistent with app color scheme
   console.print(f"[{COLOR_SCHEME['heading']}]Main Title[/{COLOR_SCHEME['heading']}]")

   # Avoid - hardcoded colors may conflict
   console.print("[red]Some text[/red]")  # Use COLOR_SCHEME['error'] instead
   ```

4. **Create reusable formatting functions**:
   ```python
   def display_section_header(title: str):
       """Display a section header with consistent styling"""
       console = get_console()
       console.print(f"\n[{COLOR_SCHEME['heading']}]═══ {title} ═══[/{COLOR_SCHEME['heading']}]\n")
   ```

---

### Guide 4: Work with Tables

**Scenario**: Display structured data in table format

**Basic Table**:
```python
from src.cli.formatting import create_task_table

# Prepare data
tasks_data = [
    {"id": "1", "task": "Buy groceries", "priority": "High", "status": "Incomplete"},
    {"id": "2", "task": "Write report", "priority": "Medium", "status": "Complete"}
]

# Create and display
table = create_task_table(tasks_data)
console = get_console()
console.print(table)
```

**Custom Table** (for non-task data):
```python
from rich.table import Table

console = get_console()
table = Table(header_style="bold magenta", border_style="dim")

# Add columns
table.add_column("Name", style="cyan", width=20)
table.add_column("Value", style="white")

# Add rows
table.add_row("Setting 1", "Enabled")
table.add_row("Setting 2", "Disabled")

console.print(table)
```

**Conditional Row Coloring**:
```python
for task in tasks:
    style = COLOR_SCHEME['completed'] if task.completed else COLOR_SCHEME['incomplete']
    table.add_row(
        str(task.id),
        task.title,
        style=style
    )
```

---

### Guide 5: Handle Terminal Compatibility

**Scenario**: Ensure your code works on all terminals

**Automatic Handling** (Rich does this for you):
```python
# No special code needed!
console = get_console()
console.print("[bold]This works everywhere[/bold]")

# Rich automatically:
# - Detects terminal capabilities
# - Falls back to plain text when needed
# - Respects NO_COLOR environment variable
# - Handles piped output (removes colors)
```

**Manual Testing**:
```bash
# Test with colors disabled
NO_COLOR=1 todo list

# Test with output redirection
todo list > output.txt
cat output.txt  # Should be plain text, no ANSI codes

# Test with piping
todo list | grep "Buy"  # Should work without color interference
```

**Force Color Mode** (for debugging):
```python
# Only use in development/debugging
from rich.console import Console

console = Console(force_terminal=True, force_interactive=True)
```

---

## Color Scheme Reference

### Standard Colors

| Semantic Name | Rich Color | When to Use | Example |
|---------------|------------|-------------|---------|
| `success` | `green` | Successful operations | "Task added successfully!" |
| `error` | `red` | Errors and failures | "Task not found" |
| `info` | `blue` | Informational messages | "Loading tasks..." |
| `warning` | `yellow` | Warnings and cautions | "Storage is full" |
| `heading` | `bold cyan` | Section headers | "Task List" |
| `subheading` | `cyan` | Subsection headers | "Completed Tasks" |
| `priority_high` | `red` | High-priority tasks | Task with urgent deadline |
| `priority_medium` | `yellow` | Medium-priority tasks | Standard task |
| `priority_low` | `green` | Low-priority tasks | Optional task |
| `completed` | `dim white` | Completed tasks | Finished task |
| `incomplete` | `white` | Incomplete tasks | Active task |
| `table_header` | `bold magenta` | Table column headers | "ID", "Task", "Status" |
| `table_border` | `dim` | Table borders | Table frame |

### Usage Examples

```python
# Success feedback
console.print(f"[{COLOR_SCHEME['success']}]✓ Task marked as complete[/{COLOR_SCHEME['success']}]")

# Error feedback
console.print(f"[{COLOR_SCHEME['error']}]✗ Invalid task ID[/{COLOR_SCHEME['error']}]")

# Section headers
console.print(f"[{COLOR_SCHEME['heading']}]\n═══ Your Tasks ═══[/{COLOR_SCHEME['heading']}]\n")

# Priority indicators
priority_color = COLOR_SCHEME[f'priority_{priority.lower()}']
console.print(f"[{priority_color}]Priority: {priority}[/{priority_color}]")
```

---

## Testing Guide

### Unit Testing Colored Output

**Test Color Functions**:
```python
# tests/unit/test_colors.py

def test_get_console_singleton():
    """Test console singleton returns same instance"""
    console1 = get_console()
    console2 = get_console()
    assert console1 is console2

def test_color_scheme_contains_all_keys():
    """Test COLOR_SCHEME has all required keys"""
    required_keys = ['success', 'error', 'info', 'warning', 'heading']
    for key in required_keys:
        assert key in COLOR_SCHEME
```

**Test Display Functions**:
```python
# tests/unit/test_display.py

def test_display_success_message(capsys):
    """Test success message output"""
    display_success_message("Test message")
    captured = capsys.readouterr()
    assert "Test message" in captured.out
    # Note: ANSI codes may be present depending on terminal

def test_format_task_row():
    """Test task formatting"""
    from src.models.task import Task
    task = Task(id=1, title="Test Task", description="", completed=False)
    row = format_task_row(task)
    assert row['id'] == "1"
    assert row['task'] == "Test Task"
    assert row['status'] == "Incomplete"
```

### Integration Testing

**Test End-to-End Display**:
```python
# tests/integration/test_cli_display.py

def test_list_command_colored_output(capsys):
    """Test list command produces colored output"""
    # Add some tasks
    manager = TaskManager()
    manager.add_task("Task 1")
    manager.add_task("Task 2")

    # Display with colors
    tasks = manager.list_all_tasks()
    display_tasks_as_table(tasks)

    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" in captured.out
```

### Manual Testing Checklist

- [ ] Run on Windows Terminal
- [ ] Run on PowerShell
- [ ] Run on cmd.exe
- [ ] Run on bash (Linux/macOS)
- [ ] Run on zsh (macOS)
- [ ] Test with `NO_COLOR=1`
- [ ] Test with output redirection (`> file.txt`)
- [ ] Test with piping (`| grep`)
- [ ] Test on narrow terminal (80 columns)
- [ ] Test on wide terminal (200+ columns)
- [ ] Test with dark terminal background
- [ ] Test with light terminal background

---

## Troubleshooting

### Problem: Colors not appearing

**Possible Causes**:
1. Terminal doesn't support colors
2. `NO_COLOR` environment variable is set
3. Output is redirected/piped

**Solution**:
```python
# Check if terminal supports colors
console = get_console()
if console.is_terminal:
    print("Terminal supports colors")
else:
    print("Terminal is non-interactive or colors disabled")

# Check environment
import os
if os.getenv('NO_COLOR'):
    print("NO_COLOR is set - colors are disabled")
```

### Problem: Table columns misaligned

**Possible Cause**: Terminal width too narrow

**Solution**:
```python
# Check terminal size
console = get_console()
width, height = console.size
print(f"Terminal size: {width}x{height}")

# Tables need at least 80 columns
if width < 80:
    # Fall back to list view
    display_tasks_as_list(tasks)
else:
    display_tasks_as_table(tasks)
```

### Problem: Tests fail with ANSI code artifacts

**Possible Cause**: Rich outputs ANSI codes even in tests

**Solution**:
```python
# Disable colors in tests
import os
os.environ['NO_COLOR'] = '1'

# Or use Rich's record feature
from io import StringIO
from rich.console import Console

string_io = StringIO()
console = Console(file=string_io, force_terminal=False)
console.print("[bold]Test[/bold]")
output = string_io.getvalue()
assert "Test" in output
assert "\x1b" not in output  # No ANSI codes
```

### Problem: Colors look bad on light background

**Solution**: Test on both dark and light backgrounds. Rich's default colors work well on both, but custom colors should be tested:

```python
# Good for both backgrounds
"cyan", "blue", "magenta", "green", "yellow"

# Avoid on light backgrounds
"white", "bright_white"

# Avoid on dark backgrounds
"black", "dark_gray"
```

---

## Best Practices

### DO ✅

- **Use COLOR_SCHEME constants** for all colors (consistency)
- **Replace print() with console.print()** in all new code
- **Test with NO_COLOR=1** before committing
- **Use semantic color names** (success, error) not literal colors
- **Keep table columns to 5 or fewer** for readability
- **Display task tables after add/update** for immediate feedback

### DON'T ❌

- **Don't hardcode color names** (`"red"` → use `COLOR_SCHEME['error']`)
- **Don't override terminal detection** without good reason
- **Don't use too many colors** in one output (overwhelming)
- **Don't assume colors will render** (always works in plain text too)
- **Don't use Rich features beyond Phase I scope** (keep it simple)

---

## Examples Collection

### Example 1: Command with Full Color Treatment

```python
def mark_complete(task_id: int):
    """Mark a task as complete with colored feedback"""
    console = get_console()

    try:
        # Attempt operation
        task = manager.mark_complete(task_id)

        # Success feedback
        display_success_message(f"Task #{task_id} marked as complete!")

        # Show updated task
        display_tasks_as_table([task])

    except ValueError as e:
        # Error feedback
        display_error_message(str(e))
    except Exception as e:
        # Unexpected error
        console.print(f"[{COLOR_SCHEME['error']}]Unexpected error: {e}[/{COLOR_SCHEME['error']}]")
```

### Example 2: List with Grouping

```python
def display_tasks_by_priority():
    """Display tasks grouped by priority with colored headers"""
    console = get_console()
    tasks = manager.list_all_tasks()

    # Group by priority
    high = [t for t in tasks if t.priority == "High"]
    medium = [t for t in tasks if t.priority == "Medium"]
    low = [t for t in tasks if t.priority == "Low"]

    # Display each group
    if high:
        console.print(f"\n[{COLOR_SCHEME['priority_high']}]═══ HIGH PRIORITY ═══[/{COLOR_SCHEME['priority_high']}]\n")
        display_tasks_as_table(high)

    if medium:
        console.print(f"\n[{COLOR_SCHEME['priority_medium']}]═══ MEDIUM PRIORITY ═══[/{COLOR_SCHEME['priority_medium']}]\n")
        display_tasks_as_table(medium)

    if low:
        console.print(f"\n[{COLOR_SCHEME['priority_low']}]═══ LOW PRIORITY ═══[/{COLOR_SCHEME['priority_low']}]\n")
        display_tasks_as_table(low)
```

### Example 3: Progress Indicator

```python
def bulk_operation(task_ids: List[int]):
    """Perform operation on multiple tasks with progress feedback"""
    console = get_console()

    console.print(f"[{COLOR_SCHEME['info']}]Processing {len(task_ids)} tasks...[/{COLOR_SCHEME['info']}]")

    success_count = 0
    for task_id in task_ids:
        try:
            manager.delete_task(task_id)
            console.print(f"[{COLOR_SCHEME['success']}]✓[/{COLOR_SCHEME['success']}] Task #{task_id} deleted")
            success_count += 1
        except Exception as e:
            console.print(f"[{COLOR_SCHEME['error']}]✗[/{COLOR_SCHEME['error']}] Task #{task_id} failed: {e}")

    display_success_message(f"Completed: {success_count}/{len(task_ids)} tasks processed")
```

---

## Additional Resources

- **Rich Documentation**: https://rich.readthedocs.io/
- **Rich Table Guide**: https://rich.readthedocs.io/en/stable/tables.html
- **Rich Console API**: https://rich.readthedocs.io/en/stable/console.html
- **Feature Research**: See `research.md` for library comparison and decisions
- **API Contracts**: See `contracts/display_api.md` for complete function signatures
- **Data Model**: See `data-model.md` for entity definitions

---

## Getting Help

If you encounter issues:
1. Check the Troubleshooting section above
2. Review `research.md` for design decisions
3. Check `contracts/display_api.md` for API details
4. Run tests to verify your implementation
5. Test manually with `NO_COLOR=1` for fallback behavior

---

**Last Updated**: 2026-01-01
**Feature Status**: Planning Phase Complete
**Next Phase**: Implementation (run `/sp.tasks` to generate task list)
