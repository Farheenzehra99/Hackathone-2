"""Color utilities and console management for CLI output."""

from rich.console import Console

# Color scheme with semantic color mappings for consistent visual identity
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
    "table_border": "dim",
}

# Module-level singleton console instance
_console = None


def get_console() -> Console:
    """
    Get or create the singleton Rich Console instance.

    The Console automatically detects terminal capabilities and handles:
    - Color support detection
    - Output redirection (pipes, files)
    - Environment variables (NO_COLOR, FORCE_COLOR)
    - Graceful fallback to plain text

    Returns:
        Console: Singleton Rich Console instance
    """
    global _console
    if _console is None:
        _console = Console()
    return _console
