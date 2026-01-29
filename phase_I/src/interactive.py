"""
Interactive REPL mode for Todo CLI application.

Run with: python -m src.interactive
This allows multiple commands in a single session with persistent task storage.
"""

import sys
from .cli.commands import CLICommands
from .cli.welcome import display_welcome_message
from .services.task_manager import TaskManager
from .utils.colors import get_console, COLOR_SCHEME


def print_welcome():
    """Display welcome message for interactive mode."""
    console = get_console()
    console.print(f"\n[{COLOR_SCHEME['heading']}]=== Interactive Mode ===[/{COLOR_SCHEME['heading']}]\n")
    console.print("[dim]Commands:[/dim]")
    console.print("  add <title> [--description <text>]")
    console.print("  list")
    console.print("  complete <id>")
    console.print("  update <id> [--title <text>] [--description <text>]")
    console.print("  delete <id>")
    console.print("  help")
    console.print("  exit / quit")
    console.print(f"\n[{COLOR_SCHEME['info']}]Type 'help' for more details or 'exit' to quit.[/{COLOR_SCHEME['info']}]\n")


def parse_command(input_line: str):
    """Parse user input into command and arguments."""
    parts = input_line.strip().split(maxsplit=1)
    if not parts:
        return None, ""

    command = parts[0].lower()
    args_str = parts[1] if len(parts) > 1 else ""
    return command, args_str


def parse_args(args_str: str):
    """Parse arguments for flags like --description, --title."""
    import shlex

    try:
        args = shlex.split(args_str)
    except ValueError:
        # Fallback to simple split if shlex fails
        args = args_str.split()

    parsed = {}
    i = 0
    positional = []

    while i < len(args):
        arg = args[i]

        if arg in ['--description', '-d']:
            # Collect all tokens until next flag or end
            value_tokens = []
            i += 1
            while i < len(args) and not args[i].startswith('--') and args[i] not in ['-d', '-t']:
                value_tokens.append(args[i])
                i += 1
            if value_tokens:
                parsed['description'] = ' '.join(value_tokens)
        elif arg in ['--title', '-t']:
            # Collect all tokens until next flag or end
            value_tokens = []
            i += 1
            while i < len(args) and not args[i].startswith('--') and args[i] not in ['-d', '-t']:
                value_tokens.append(args[i])
                i += 1
            if value_tokens:
                parsed['title'] = ' '.join(value_tokens)
        else:
            positional.append(arg)
            i += 1

    # Join positional args back into single string for title
    positional_str = ' '.join(positional) if positional else None
    return positional_str, parsed


def main():
    """Main interactive REPL loop."""
    # Display welcome message
    display_welcome_message()

    # Initialize task manager (persists for entire session)
    task_manager = TaskManager()
    cli = CLICommands(task_manager)

    print_welcome()

    while True:
        try:
            # Read user input
            user_input = input("> ").strip()

            if not user_input:
                continue

            # Parse command
            command, args = parse_command(user_input)

            # Handle exit
            if command in ['exit', 'quit', 'q']:
                print("\nGoodbye!")
                break

            # Handle help
            if command == 'help':
                print_welcome()
                continue

            # Parse arguments
            positional, flags = parse_args(args)

            # Route commands
            if command == 'add':
                if not positional:
                    print("Error: Title is required")
                    print("Usage: add <title> [--description <text>]")
                else:
                    title = positional
                    description = flags.get('description')
                    print(cli.add(title, description))

            elif command == 'list':
                print(cli.list_tasks())

            elif command == 'complete':
                if not positional:
                    print("Error: Task ID is required")
                    print("Usage: complete <id>")
                else:
                    try:
                        task_id = int(positional.split()[0])
                        print(cli.complete(task_id))
                    except ValueError:
                        print(f"Error: Invalid task ID: {positional}")

            elif command == 'update':
                if not positional:
                    print("Error: Task ID is required")
                    print("Usage: update <id> [--title <text>] [--description <text>]")
                else:
                    try:
                        task_id = int(positional.split()[0]) if positional else None
                        if task_id is None:
                            print("Error: Task ID is required")
                        else:
                            title = flags.get('title')
                            description = flags.get('description')

                            if not title and not description:
                                print("Error: At least one of --title or --description must be provided")
                            else:
                                print(cli.update(task_id, title, description))
                    except ValueError:
                        print(f"Error: Invalid task ID: {positional}")

            elif command == 'delete':
                if not positional:
                    print("Error: Task ID is required")
                    print("Usage: delete <id>")
                else:
                    try:
                        task_id = int(positional.split()[0])
                        print(cli.delete(task_id))
                    except ValueError:
                        print(f"Error: Invalid task ID: {positional}")

            else:
                print(f"Error: Unknown command '{command}'")
                print("Type 'help' for available commands")

            print()  # Empty line for readability

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
