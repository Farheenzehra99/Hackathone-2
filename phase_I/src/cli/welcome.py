"""Welcome message display for CLI application."""

from src.utils.colors import get_console, COLOR_SCHEME


def display_welcome_message() -> None:
    """
    Display colorful welcome screen when application starts.

    Displays:
    - ASCII art banner with application name
    - Colored subtitle
    - Help hint in info color
    """
    console = get_console()

    # Display colored banner with ASCII-compatible border
    banner = """
+====================================+
|    Welcome to Todo CLI App!        |
+====================================+
"""
    console.print(f"[{COLOR_SCHEME['heading']}]{banner}[/{COLOR_SCHEME['heading']}]")

    # Display subtitle in dim style
    console.print(
        f"[dim]Manage your tasks efficiently from the command line[/dim]\n"
    )

    # Display help hint in info color
    console.print(
        f"[{COLOR_SCHEME['info']}]Type 'todo --help' for available commands[/{COLOR_SCHEME['info']}]\n"
    )
