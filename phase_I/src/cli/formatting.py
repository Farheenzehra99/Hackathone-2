"""Table formatting utilities for CLI display."""

from typing import Dict, List
from rich.table import Table
from src.utils.colors import get_console, COLOR_SCHEME


def format_task_row(task) -> Dict[str, str]:
    """
    Format a single task for display in list or table format.

    Args:
        task: Task entity from domain model

    Returns:
        Dict with keys: id, task, priority, status
    """
    # Truncate long task titles to 50 characters
    task_text = task.title if len(task.title) <= 50 else task.title[:47] + "..."

    # Add description if present
    if task.description:
        desc_preview = task.description if len(task.description) <= 30 else task.description[:27] + "..."
        task_text += f" ({desc_preview})"

    return {
        "id": str(task.id),
        "task": task_text,
        "priority": "N/A",  # Priority not in Phase I Task model
        "status": "Complete" if task.completed else "Incomplete"
    }


def create_task_table(tasks: List[Dict[str, str]], show_all_columns: bool = True) -> Table:
    """
    Create a Rich Table with colored headers for displaying tasks.

    Args:
        tasks: List of task dictionaries
        show_all_columns: Whether to show all columns or minimal set

    Returns:
        Rich Table instance with colored headers and styled rows
    """
    # Create table with colored headers and dim borders
    table = Table(
        header_style=COLOR_SCHEME['table_header'],
        border_style=COLOR_SCHEME['table_border'],
        show_header=True,
        show_edge=True,
        padding=(0, 1)
    )

    # Add columns with specific styles
    table.add_column("ID", style="cyan", width=6, justify="right")
    table.add_column("Task", style="white", justify="left", overflow="fold")

    if show_all_columns:
        table.add_column("Status", style="white", width=12)

    # Add rows
    for task_dict in tasks:
        # Determine row style based on status
        status = task_dict.get("status", "Incomplete")
        status_style = COLOR_SCHEME['completed'] if status == "Complete" else COLOR_SCHEME['incomplete']

        if show_all_columns:
            table.add_row(
                task_dict["id"],
                task_dict["task"],
                f"[{status_style}]{status}[/{status_style}]"
            )
        else:
            table.add_row(
                task_dict["id"],
                task_dict["task"]
            )

    return table
