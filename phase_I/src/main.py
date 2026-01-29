"""
Main entry point for Todo CLI application.

This is the primary executable for the Phase I Todo CLI application.
Run with: python -m src.main <command> [arguments]
"""

import sys
from .cli.commands import create_parser, CLICommands
from .services.task_manager import TaskManager


def main():
    """Main entry point for CLI application."""
    # Create argument parser
    parser = create_parser()

    # Parse command line arguments
    args = parser.parse_args()

    # Initialize task manager (in-memory storage)
    task_manager = TaskManager()

    # Initialize CLI commands
    cli = CLICommands(task_manager)

    # Route to appropriate command
    if args.command == 'add':
        description = getattr(args, 'description', None)
        print(cli.add(args.title, description))

    elif args.command == 'list':
        print(cli.list_tasks())

    elif args.command == 'complete':
        print(cli.complete(args.id))

    elif args.command == 'update':
        title = getattr(args, 'title', None)
        description = getattr(args, 'description', None)

        if title is None and description is None:
            print("Error: At least one of --title or --description must be provided.")
        else:
            print(cli.update(args.id, title, description))

    elif args.command == 'delete':
        print(cli.delete(args.id))

    else:
        # No command provided, show help
        parser.print_help()


if __name__ == '__main__':
    main()
