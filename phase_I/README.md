# Todo CLI Application - Phase I

A simple command-line todo application with in-memory storage, built using Spec-Driven Development with Claude Code and Spec-Kit Plus.

## Features

- ✅ Add tasks with title and optional description
- ✅ View all tasks with status indicators
- ✅ Mark tasks as complete/incomplete
- ✅ Update task title and description
- ✅ Delete tasks permanently
- 🎨 **Colorful CLI interface** with:
  - Colored welcome banner on startup
  - Color-coded task lists (incomplete/completed sections)
  - Formatted tables with colored headers
  - Success/error/info messages with semantic colors
  - Cross-platform terminal support

## Technology Stack

- **UV** - Modern Python package manager
- **Python 3.13+** - Programming language
- **Rich** - Terminal formatting and color library
- **Claude Code** - AI-powered code generation
- **Spec-Kit Plus** - Spec-driven development framework

## Terminal Compatibility

### Colored Output

The application features a colorful CLI interface with:
- **Colored welcome banner** on startup
- **Color-coded task lists** (grouped by status)
- **Formatted tables** with colored headers
- **Semantic colors**: Green (success), Red (error), Blue (info)

### Disabling Colors

Set the `NO_COLOR` environment variable to disable colored output:

**Windows (PowerShell)**:
```powershell
$env:NO_COLOR=1; uv run todo list
```

**Windows (CMD)**:
```cmd
set NO_COLOR=1 && uv run todo list
```

**macOS/Linux**:
```bash
NO_COLOR=1 uv run todo list
```

### Output Redirection

Colors are automatically disabled when output is redirected to files or piped:

```bash
# Save to file (plain text, no ANSI codes)
uv run todo list > tasks.txt

# Pipe to grep (no color interference)
uv run todo list | grep "Buy"
```

## Prerequisites

- Python 3.13 or higher
- UV package manager

### Installing UV

**Windows (PowerShell)**:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd todo-cli-app
```

### 2. Install Dependencies

```bash
uv sync
```

This will create a virtual environment and install all dependencies.

## Usage

### Interactive Mode (Recommended)

Run the interactive mode for a continuous session where tasks persist:

```bash
uv run python -m src.interactive
```

**Example Session**:
```
> add Buy groceries
Task created successfully.
ID: 1
Title: Buy groceries
Status: Incomplete

> add Write report --description Quarterly sales report
Task created successfully.
ID: 2
Title: Write report
Description: Quarterly sales report
Status: Incomplete

> list
Your Tasks:

[ ] 1: Buy groceries
[ ] 2: Write report (Quarterly sales report)

> complete 1
Task marked as complete: Buy groceries

> list
Your Tasks:

[✓] 1: Buy groceries
[ ] 2: Write report (Quarterly sales report)

> update 2 --title Annual report
Task updated successfully.
ID: 2
Title: Annual report
Description: Quarterly sales report

> delete 1
Task deleted successfully: Buy groceries

> list
Your Tasks:

[ ] 2: Annual report (Quarterly sales report)

> exit
Goodbye!
```

### Single Command Mode

Run individual commands (tasks don't persist between commands):

```bash
# Add a task
uv run python -m src.main add "Buy groceries"

# Add task with description
uv run python -m src.main add "Write report" --description "Sales report"

# List all tasks
uv run python -m src.main list

# Mark task as complete
uv run python -m src.main complete 1

# Update task
uv run python -m src.main update 1 --title "New title"

# Delete task
uv run python -m src.main delete 1

# Show help
uv run python -m src.main --help
```

## Commands Reference

### Add Task
```bash
add <title> [--description <text>]
```
Create a new task with required title and optional description.

### List Tasks
```bash
list
```
Display all tasks with IDs, titles, descriptions, and completion status.

### Complete Task
```bash
complete <id>
```
Mark a task as complete (or toggle back to incomplete if already complete).

### Update Task
```bash
update <id> [--title <text>] [--description <text>]
```
Update task title or description. At least one field must be provided.

### Delete Task
```bash
delete <id>
```
Permanently remove a task from the list.

### Help
```bash
help
```
Display available commands and usage information.

### Exit
```bash
exit
quit
```
Exit the interactive mode.

## Development

### Project Structure

```
src/
├── models/
│   └── task.py              # Task data model and validation
├── services/
│   └── task_manager.py      # Task state management operations
├── cli/
│   ├── commands.py          # Command parsing and routing
│   └── display.py           # Output formatting utilities
├── main.py                  # Single command entry point
└── interactive.py           # Interactive REPL mode

tests/
├── unit/
│   ├── test_task.py         # Task model tests
│   └── test_task_manager.py # State management tests
└── integration/
    └── test_cli.py          # CLI integration tests

specs/
└── 001-todo-cli-core/       # Feature specifications
    ├── spec.md              # Feature requirements
    ├── plan.md              # Implementation plan
    ├── tasks.md             # Task breakdown
    ├── data-model.md        # Data model design
    ├── research.md          # Technical decisions
    └── contracts/           # CLI interface contracts
```

### Running Tests

```bash
uv run pytest tests/
```

### Spec-Driven Development Workflow

This project was built following the Spec-Kit Plus workflow:

1. **Constitution** - Define project principles and constraints
2. **Specification** - Write feature requirements (`/sp.specify`)
3. **Planning** - Create implementation plan (`/sp.plan`)
4. **Task Breakdown** - Decompose into atomic tasks (`/sp.tasks`)
5. **Implementation** - Execute tasks (`/sp.implement`)

See `specs/001-todo-cli-core/` for complete specification artifacts.

## Important Notes

### Task Persistence

All tasks are persisted to a local JSON file at `~/.todo-cli/tasks.json`. This ensures:
- Tasks persist across CLI command invocations
- Tasks are maintained between interactive sessions
- No external database required - simple file-based storage

The application loads tasks from the JSON file on startup and saves after each operation (add, update, delete, complete).

### Task IDs

- Task IDs are sequential integers starting from 1
- IDs increment with each new task
- IDs are never reused, even after deletion

## Troubleshooting

### Command Not Found

Make sure you're in the project root directory and using `uv run`:

```bash
uv run python -m src.interactive
```

### Module Import Errors

Ensure dependencies are installed:

```bash
uv sync
```

### Python Version Error

Check Python version:

```bash
python --version
```

Must be 3.13 or higher.

## Phase I Limitations

The following are intentionally NOT included in Phase I:

- Persistent storage (files, databases)
- Task search or filtering
- Task priorities or due dates
- Task categories or tags
- User authentication
- Cloud sync or API
- Configuration files

## Contributing

This project follows strict spec-driven development:
- No manual code changes without specification
- All features must be specified first
- Use Claude Code for implementation
- Follow constitution principles

## License

MIT License

## Contact

For issues or questions, please open a GitHub issue.
