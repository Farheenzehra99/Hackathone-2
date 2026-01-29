"""
Command-line interface commands for Todo CLI application.

Provides command parsing and command handlers for all 5 core features:
- Add Task
- View Task List
- Mark Task Complete/Incomplete
- Update Task
- Delete Task
- Help
"""

import argparse
import sys
from typing import Optional

from ..services.task_manager import (
    TaskManager,
    EmptyTitleError,
    InvalidIDError,
    TaskNotFoundError
)
from .display import (
    format_task,
    format_task_list,
    format_success,
    format_error,
    display_success_message,
    display_error_message,
    display_tasks_as_list,
    display_tasks_as_table,
)


class CLICommands:
    """Handles all CLI commands for Todo application."""

    def __init__(self, task_manager: TaskManager):
        """Initialize CLI with task manager instance."""
        self.task_manager = task_manager

    def add(self, title: str, description: Optional[str] = None):
        """
        Add command: Create a new task.

        Args:
            title: Task title (required, non-empty)
            description: Optional task description

        Returns:
            Success message with task details or error message
        """
        try:
            task = self.task_manager.create_task(title, description)
            # T017: Use colored success message
            display_success_message(f"Task created: {task.title}")
            # T024: Show new task in table format
            display_tasks_as_table([task])
            return ""  # Return empty string since display function prints directly
        except EmptyTitleError as e:
            return format_error(str(e))

    def list_tasks(self):
        """
        List command: Display all tasks.

        Returns:
            Task list formatted for display
        """
        tasks = self.task_manager.list_tasks()

        # T016: Use colored task list display
        display_tasks_as_list(tasks)
        return ""  # Return empty string since display function prints directly

    def complete(self, id: int):
        """
        Complete command: Mark task as complete.

        Args:
            id: Task ID to mark complete

        Returns:
            Success message or error message
        """
        try:
            task = self.task_manager.toggle_complete(id)
            # T019: Use colored success message
            status = "complete" if task.completed else "incomplete"
            display_success_message(f"Task marked as {status}: {task.title}")
            return ""  # Return empty string since display function prints directly
        except (InvalidIDError, TaskNotFoundError) as e:
            # Use colored error message
            display_error_message(str(e))
            return ""

    def update(self, id: int, title: Optional[str] = None,
              description: Optional[str] = None):
        """
        Update command: Modify existing task.

        Args:
            id: Task ID to update
            title: Optional new title (non-empty if provided)
            description: Optional new description

        Returns:
            Success message with updated task or error message
        """
        try:
            task = self.task_manager.update_task(id, title, description)
            # T027: Use colored success/error messages consistently
            display_success_message(f"Task updated: {task.title}")
            display_tasks_as_table([task])
            return ""  # Return empty string since display function prints directly
        except (InvalidIDError, TaskNotFoundError, EmptyTitleError) as e:
            display_error_message(str(e))
            return ""

    def delete(self, id: int):
        """
        Delete command: Remove a task.

        Args:
            id: Task ID to delete

        Returns:
            Success message or error message
        """
        try:
            task = self.task_manager.get_task_by_id(id)
            task_title = task.title
            self.task_manager.delete_task(id)
            # T018: Use colored success/error messages
            display_success_message(f"Task deleted: {task_title}")
            return ""  # Return empty string since display function prints directly
        except (InvalidIDError, TaskNotFoundError) as e:
            display_error_message(str(e))
            return ""


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Todo CLI - Phase I",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Add command
    add_parser = subparsers.add_parser('add', help='Create a new task')
    add_parser.add_argument('title', type=str, help='Task title (required)')
    add_parser.add_argument('--description', '-d', type=str,
                          help='Task description (optional)')

    # List command
    subparsers.add_parser('list', help='View all tasks')

    # Complete command
    complete_parser = subparsers.add_parser('complete',
                                           help='Mark task as complete')
    complete_parser.add_argument('id', type=int, help='Task ID (required)')

    # Update command
    update_parser = subparsers.add_parser('update',
                                           help='Update existing task')
    update_parser.add_argument('id', type=int, help='Task ID (required)')
    update_parser.add_argument('--title', '-t', type=str,
                          help='New task title (optional)')
    update_parser.add_argument('--description', '-d', type=str,
                          help='New task description (optional)')

    # Delete command
    delete_parser = subparsers.add_parser('delete',
                                           help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID (required)')

    return parser


def main():
    """Main entry point for CLI application."""
    parser = create_parser()
    args = parser.parse_args()

    # Initialize task manager
    task_manager = TaskManager()

    # Initialize CLI commands
    cli = CLICommands(task_manager)

    # Route to appropriate command
    if args.command == 'add':
        description = args.description if hasattr(args, 'description') else None
        print(cli.add(args.title, description))
    elif args.command == 'list':
        print(cli.list_tasks())
    elif args.command == 'complete':
        print(cli.complete(args.id))
    elif args.command == 'update':
        title = args.title if hasattr(args, 'title') else None
        description = args.description if hasattr(args, 'description') else None
        print(cli.update(args.id, title, description))
    elif args.command == 'delete':
        print(cli.delete(args.id))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
