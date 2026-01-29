"""
Output formatting utilities for Todo CLI application.

Provides functions to format tasks, task lists, success messages,
and error messages for human-readable command-line display.
"""

from typing import List, Optional
from ..models.task import Task
from ..utils.colors import get_console, COLOR_SCHEME
from .formatting import format_task_row, create_task_table


def format_task(task: Task) -> str:
    """
    Format a single task for display.

    Args:
        task: Task object to format

    Returns:
        Formatted task string with status, ID, title, and optional description
    """
    status = "[X]" if task.completed else "[ ]"

    if task.description:
        return f"{status} {task.id}: {task.title} ({task.description})"
    else:
        return f"{status} {task.id}: {task.title}"


def format_task_list(tasks: List[Task]) -> str:
    """
    Format a list of tasks for display.

    Args:
        tasks: List of Task objects to format

    Returns:
        Formatted task list for display
    """
    if not tasks:
        return "No tasks exist. Use 'add' to create your first task."

    lines = ["Your Tasks:", ""]
    for task in tasks:
        lines.append(format_task(task))

    return "\n".join(lines)


def format_success(action: str, task: Optional[Task] = None,
                   custom_text: Optional[str] = None) -> str:
    """
    Format success message.

    Args:
        action: Action that was completed (e.g., "Task created")
        task: Task object that was acted on (optional)
        custom_text: Custom text for success message (optional)

    Returns:
        Formatted success message
    """
    if custom_text:
        return f"{custom_text}"

    if task:
        lines = [f"{action} successfully."]
        lines.append(f"ID: {task.id}")
        lines.append(f"Title: {task.title}")
        if task.description:
            lines.append(f"Description: {task.description}")
        lines.append(f"Status: {'Complete' if task.completed else 'Incomplete'}")
        return "\n".join(lines)

    return f"{action} successfully."


def format_error(message: str) -> str:
    """
    Format error message.

    Args:
        message: Error message to format

    Returns:
        Formatted error message
    """
    return f"Error: {message}"


# Colored display functions for User Story 2

def display_success_message(message: str) -> None:
    """
    Display success message in green color with checkmark symbol.

    Args:
        message: Success message text
    """
    console = get_console()
    console.print(f"[{COLOR_SCHEME['success']}][OK] {message}[/{COLOR_SCHEME['success']}]")


def display_error_message(message: str) -> None:
    """
    Display error message in red color with cross symbol.

    Args:
        message: Error message text
    """
    console = get_console()
    console.print(f"[{COLOR_SCHEME['error']}][ERROR] {message}[/{COLOR_SCHEME['error']}]")


def display_info_message(message: str) -> None:
    """
    Display informational message in blue color with info symbol.

    Args:
        message: Info message text
    """
    console = get_console()
    console.print(f"[{COLOR_SCHEME['info']}][INFO] {message}[/{COLOR_SCHEME['info']}]")


def display_tasks_as_list(tasks: List[Task]) -> None:
    """
    Display tasks as a colored list grouped by completion status.

    Groups tasks by completion status with colored headings and
    colored priority indicators for each task.

    Args:
        tasks: List of Task entities
    """
    console = get_console()

    if not tasks:
        display_info_message("No tasks found")
        return

    # Group tasks by completion status
    incomplete = [t for t in tasks if not t.completed]
    completed = [t for t in tasks if t.completed]

    # Display incomplete tasks
    if incomplete:
        console.print(f"\n[{COLOR_SCHEME['heading']}]Incomplete Tasks:[/{COLOR_SCHEME['heading']}]\n")
        for task in incomplete:
            # Use white color for incomplete tasks
            status_symbol = "[ ]"
            task_text = f"{task.title}"
            if task.description:
                task_text += f" ({task.description})"
            console.print(
                f"[{COLOR_SCHEME['incomplete']}]{status_symbol} [ID: {task.id}] {task_text}[/{COLOR_SCHEME['incomplete']}]"
            )

    # Display completed tasks
    if completed:
        console.print(f"\n[{COLOR_SCHEME['subheading']}]Completed Tasks:[/{COLOR_SCHEME['subheading']}]\n")
        for task in completed:
            # Use dim white color for completed tasks
            status_symbol = "[X]"
            task_text = f"{task.title}"
            if task.description:
                task_text += f" ({task.description})"
            console.print(
                f"[{COLOR_SCHEME['completed']}]{status_symbol} [ID: {task.id}] {task_text}[/{COLOR_SCHEME['completed']}]"
            )

    console.print()  # Empty line for spacing


def display_tasks_as_table(tasks: List[Task]) -> None:
    """
    Display tasks as a formatted table with colored headers.

    Converts tasks using format_task_row(), creates table using
    create_task_table(), and prints via Rich Console.

    Args:
        tasks: List of Task entities
    """
    console = get_console()

    if not tasks:
        display_info_message("No tasks found")
        return

    # Convert tasks to display format
    tasks_data = [format_task_row(task) for task in tasks]

    # Create and display table
    table = create_task_table(tasks_data, show_all_columns=True)
    console.print()
    console.print(table)
    console.print()
