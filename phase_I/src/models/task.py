"""
Task data model for Todo CLI application.

This module defines the Task entity, validation rules, and error types
for the Phase I in-memory Todo CLI application.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """Represents a single todo item."""

    id: int  # Immutable, unique identifier
    title: str  # Required, non-empty, non-whitespace
    description: Optional[str] = None  # Optional detailed information
    completed: bool = False  # Completion status


class EmptyTitleError(Exception):
    """Raised when task title is empty or whitespace only."""
    pass


class InvalidIDError(Exception):
    """Raised when task ID is invalid (not an integer or out of range)."""
    pass


class TaskNotFoundError(Exception):
    """Raised when a task with given ID does not exist."""
    pass


class TaskAlreadyDeletedError(Exception):
    """Raised when an operation is attempted on an already deleted task."""
    pass


def validate_title(title: str) -> None:
    """
    Validate that a task title is not empty or whitespace only.

    Args:
        title: The title string to validate

    Returns:
        None if valid

    Raises:
        EmptyTitleError: If title is empty or whitespace only
    """
    if not title or not isinstance(title, str):
        raise EmptyTitleError("Title is required and must be a non-empty string")

    stripped = title.strip()
    if not stripped or stripped.isspace():
        raise EmptyTitleError("Title cannot be empty or whitespace only")


def validate_id(id_value: int, existing_ids: set) -> None:
    """
    Validate that a task ID is valid and exists.

    Args:
        id_value: The ID to validate
        existing_ids: Set of existing task IDs (for existence check)

    Returns:
        None if valid

    Raises:
        InvalidIDError: If ID is invalid
        TaskNotFoundError: If ID does not exist
    """
    if not isinstance(id_value, int) or id_value <= 0:
        raise InvalidIDError(f"Invalid task ID: {id_value}")

    if id_value not in existing_ids:
        raise TaskNotFoundError(f"Task not found: {id_value}")
