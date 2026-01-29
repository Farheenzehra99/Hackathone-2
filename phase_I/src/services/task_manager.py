"""
Task state management operations for Todo CLI application.

Provides in-memory storage with JSON file persistence and CRUD operations
for Task entities following Phase I specification requirements.
"""

from typing import Dict, List, Optional
from ..models.task import (
    Task,
    validate_title,
    validate_id,
    EmptyTitleError,
    InvalidIDError,
    TaskNotFoundError
)
from ..storage.json_storage import JSONStorage


class TaskManager:
    """Manages task state with in-memory storage and JSON persistence."""

    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize task manager with JSON persistence.

        Args:
            storage_path: Path to JSON file (optional, defaults to ~/.todo-cli/tasks.json)
        """
        self.storage = JSONStorage(storage_path)
        self.tasks: Dict[int, Task] = {}
        self.next_id: int = 1
        self._load_from_storage()

    def _load_from_storage(self) -> None:
        """Load tasks from JSON file into memory."""
        data = self.storage.load()
        self.next_id = data.get("next_id", 1)

        # Convert stored dictionaries back to Task objects
        tasks_data = data.get("tasks", {})
        for task_id_str, task_dict in tasks_data.items():
            task_id = int(task_id_str)
            task = Task(
                id=task_dict["id"],
                title=task_dict["title"],
                description=task_dict.get("description"),
                completed=task_dict.get("completed", False)
            )
            self.tasks[task_id] = task

    def _save_to_storage(self) -> None:
        """Save current tasks to JSON file."""
        self.storage.save(self.tasks, self.next_id)

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task with a unique ID.

        Args:
            title: Task title (required, non-empty)
            description: Optional task description

        Returns:
            Created Task object

        Raises:
            EmptyTitleError: If title validation fails
        """
        validate_title(title)

        task_id = self.next_id
        self.next_id += 1

        task = Task(
            id=task_id,
            title=title,
            description=description,
            completed=False
        )

        self.tasks[task_id] = task
        self._save_to_storage()
        return task

    def update_task(self, id: int, title: Optional[str] = None,
                  description: Optional[str] = None) -> Task:
        """
        Update an existing task's mutable fields.

        Args:
            id: Task ID to update
            title: New task title (optional)
            description: New task description (optional)

        Returns:
            Updated Task object

        Raises:
            InvalidIDError: If ID is invalid
            TaskNotFoundError: If task does not exist
            EmptyTitleError: If title validation fails
        """
        validate_id(id, set(self.tasks.keys()))

        if id not in self.tasks:
            raise TaskNotFoundError(f"Task not found: {id}")

        task = self.tasks[id]

        if title is not None:
            validate_title(title)
            task.title = title

        if description is not None:
            task.description = description

        self._save_to_storage()
        return task

    def delete_task(self, id: int) -> None:
        """
        Delete a task permanently.

        Args:
            id: Task ID to delete

        Raises:
            InvalidIDError: If ID is invalid
            TaskNotFoundError: If task does not exist
        """
        validate_id(id, set(self.tasks.keys()))

        if id not in self.tasks:
            raise TaskNotFoundError(f"Task not found: {id}")

        del self.tasks[id]
        self._save_to_storage()
        return None

    def toggle_complete(self, id: int) -> Task:
        """
        Toggle the completion status of a task.

        Args:
            id: Task ID to toggle

        Returns:
            Updated Task object

        Raises:
            InvalidIDError: If ID is invalid
            TaskNotFoundError: If task does not exist
        """
        validate_id(id, set(self.tasks.keys()))

        if id not in self.tasks:
            raise TaskNotFoundError(f"Task not found: {id}")

        task = self.tasks[id]
        task.completed = not task.completed

        self._save_to_storage()
        return task

    def list_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks in order of creation (by ID)
        """
        return sorted(self.tasks.values(), key=lambda t: t.id)

    def get_task_by_id(self, id: int) -> Task:
        """
        Retrieve a single task by ID.

        Args:
            id: Task ID to retrieve

        Returns:
            Task object

        Raises:
            InvalidIDError: If ID is invalid
            TaskNotFoundError: If task does not exist
        """
        validate_id(id, set(self.tasks.keys()))

        if id not in self.tasks:
            raise TaskNotFoundError(f"Task not found: {id}")

        return self.tasks[id]
