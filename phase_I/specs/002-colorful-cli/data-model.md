# Data Model: Colorful CLI Interface

**Feature**: 002-colorful-cli
**Date**: 2026-01-01
**Phase**: 1 - Design

## Overview

This feature is **presentation-layer only** and does not introduce new domain entities. It enhances how existing Task entities are displayed. The data model focuses on display configuration and formatting structures.

## Existing Entities (No Changes)

### Task
- **Source**: `src/models/task.py`
- **Fields**: `id`, `title`, `description`, `completed`
- **Status**: **Unchanged** - No modifications to Task entity per Constitution Check

## Display Entities (New)

These entities represent display configuration and formatting logic, not persistent domain data.

### ColorScheme

**Purpose**: Defines the application's color palette for consistent visual identity

**Attributes**:
- `success`: Color for success messages (value: `"green"`)
- `error`: Color for error messages (value: `"red"`)
- `info`: Color for informational messages (value: `"blue"`)
- `warning`: Color for warning messages (value: `"yellow"`)
- `heading`: Color for main headings (value: `"bold cyan"`)
- `subheading`: Color for subheadings (value: `"cyan"`)
- `priority_high`: Color for high-priority tasks (value: `"red"`)
- `priority_medium`: Color for medium-priority tasks (value: `"yellow"`)
- `priority_low`: Color for low-priority tasks (value: `"green"`)
- `completed`: Color/style for completed tasks (value: `"dim white"`)
- `incomplete`: Color for incomplete tasks (value: `"white"`)
- `table_header`: Style for table headers (value: `"bold magenta"`)
- `table_border`: Style for table borders (value: `"dim"`)

**Type**: Configuration constant (not a class instance)

**Validation Rules**: None (fixed constants per Determinism principle)

**State Transitions**: N/A (immutable configuration)

**Relationships**: Referenced by all display functions

**Implementation Location**: `src/utils/colors.py`

---

### TableConfig

**Purpose**: Standard configuration for table display formatting

**Attributes**:
- `header_style`: Style applied to all table headers (value: `"bold magenta"`)
- `border_style`: Style applied to table borders (value: `"dim"`)
- `show_header`: Whether to display column headers (value: `True`)
- `show_edge`: Whether to display table borders (value: `True`)
- `padding`: Tuple of (vertical, horizontal) padding for cells (value: `(0, 1)`)
- `column_configs`: Dictionary mapping column names to configuration

**Column Configuration Structure**:
```python
{
    "ID": {
        "style": "cyan",
        "width": 6,
        "justify": "right"
    },
    "Task": {
        "style": "white",
        "justify": "left",
        "overflow": "fold"
    },
    "Priority": {
        "style_map": {
            "High": "red",
            "Medium": "yellow",
            "Low": "green"
        },
        "width": 10
    },
    "Status": {
        "style_map": {
            "Complete": "dim white",
            "Incomplete": "white"
        },
        "width": 12
    }
}
```

**Type**: Configuration object

**Validation Rules**: None (fixed configuration)

**State Transitions**: N/A (immutable configuration)

**Relationships**: Used by table formatting functions

**Implementation Location**: `src/cli/formatting.py`

---

### WelcomeMessage

**Purpose**: Structured representation of the welcome screen content

**Attributes**:
- `banner`: ASCII art or styled text banner (multi-line string)
- `subtitle`: Brief description text
- `help_hint`: Instruction for getting help

**Type**: Configuration constant or simple data structure

**Example Structure**:
```python
{
    "banner": """
╔════════════════════════════════════╗
║      Welcome to Todo CLI App       ║
╚════════════════════════════════════╝
    """,
    "subtitle": "Manage your tasks efficiently from the command line",
    "help_hint": "Type 'todo --help' for available commands"
}
```

**Validation Rules**: None

**State Transitions**: N/A

**Relationships**: Displayed by welcome screen function

**Implementation Location**: `src/cli/welcome.py`

---

### ConsoleWrapper

**Purpose**: Singleton instance of Rich Console for consistent output handling

**Attributes**:
- `console`: Instance of `rich.console.Console`
- Automatically detects terminal capabilities
- Handles color fallback and output redirection

**Type**: Singleton wrapper

**Validation Rules**:
- Must be initialized once at application startup
- Should not be recreated during runtime

**State Transitions**: N/A (stateless output handler)

**Relationships**: Used by all display and formatting functions

**Implementation Location**: `src/utils/colors.py`

**Implementation Pattern**:
```python
from rich.console import Console

# Module-level singleton
_console = None

def get_console() -> Console:
    """Get or create the singleton Console instance."""
    global _console
    if _console is None:
        _console = Console()
    return _console
```

---

## Data Flow

### Display Pipeline

```
Task Entity (Domain)
    ↓
Format Function (maps Task → Display Data)
    ↓
Display Data (dict with styled fields)
    ↓
Rendering Function (uses ColorScheme + TableConfig)
    ↓
Rich Console Output
    ↓
Terminal (auto-detects capabilities, applies fallbacks)
```

### Example: Displaying Task List

```
1. tasks = TaskManager.list_all_tasks()
   → Returns: List[Task]

2. display_data = format_tasks_for_table(tasks)
   → Returns: List[Dict] with fields:
      {
        "id": "1",
        "task": "Buy groceries",
        "priority": "High",
        "status": "Incomplete"
      }

3. table = create_task_table(display_data, TableConfig)
   → Returns: rich.table.Table

4. console.print(table)
   → Renders colored table to terminal
```

## Non-Persistent Nature

**Important**: All display entities are ephemeral and exist only during rendering:
- No database storage
- No file persistence
- No state management beyond single render cycle
- Configuration constants are hardcoded per Constitution's Determinism principle

## Separation of Concerns

**Architectural Boundaries** (per Constitution):
- **Domain Layer** (`src/models/`, `src/services/`): Unchanged, no awareness of colors
- **Display Layer** (`src/cli/`, `src/utils/`): All color and formatting logic isolated here
- **No mixing**: Business logic does not format output; display logic does not mutate state

## Changes from Existing Code

### Modified Files
- `src/cli/display.py`: Add color formatting to existing display functions
- `src/cli/commands.py`: Replace print() calls with console.print()
- `src/main.py`: Add welcome message display on startup
- `src/interactive.py`: Use colored display functions

### New Files
- `src/utils/colors.py`: ColorScheme constants + ConsoleWrapper singleton
- `src/utils/terminal.py`: (If needed) Additional terminal helpers beyond Rich
- `src/cli/formatting.py`: Table creation and formatting functions
- `src/cli/welcome.py`: Welcome message display logic

### No Changes
- `src/models/task.py`: Task entity unchanged
- `src/services/task_manager.py`: Business logic unchanged
- Test files (except adding new display tests)

## Validation Against Constitution

✅ **Data Model Constraints**: Task entity (`id`, `title`, `description`, `completed`) unchanged

✅ **Storage Rules**: No new persistence. Display entities are in-memory only during render.

✅ **Separation of Concerns**: Display logic fully isolated from state management and business logic.

✅ **Simplicity by Design**: Minimal display-only entities. No abstractions for future phases.

## Summary

This feature introduces **zero new domain entities** and adds only display configuration structures. The "data model" is primarily constants and configuration objects that define HOW to display existing Task entities, not WHAT data to store. This aligns with the feature's presentation-layer-only scope and Constitution principles.
