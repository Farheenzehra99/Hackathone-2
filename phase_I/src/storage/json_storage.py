"""
JSON-based persistent storage for Todo CLI application.

Provides simple file-based persistence to maintain task state
across CLI command invocations.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class JSONStorage:
    """Handles JSON file operations for task persistence."""

    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize JSON storage.

        Args:
            file_path: Path to JSON file. Defaults to ~/.todo-cli/tasks.json
        """
        if file_path is None:
            # Use user's home directory for cross-platform compatibility
            home = Path.home()
            storage_dir = home / ".todo-cli"
            storage_dir.mkdir(exist_ok=True)
            file_path = str(storage_dir / "tasks.json")

        self.file_path = file_path

    def load(self) -> Dict[str, Any]:
        """
        Load task data from JSON file.

        Returns:
            Dictionary containing tasks and next_id, or empty structure if file doesn't exist

        Structure:
            {
                "tasks": {
                    "1": {"id": 1, "title": "...", "description": "...", "completed": false},
                    ...
                },
                "next_id": 2
            }
        """
        if not os.path.exists(self.file_path):
            return {"tasks": {}, "next_id": 1}

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure structure is correct
                if not isinstance(data, dict):
                    return {"tasks": {}, "next_id": 1}
                if "tasks" not in data:
                    data["tasks"] = {}
                if "next_id" not in data:
                    data["next_id"] = 1
                return data
        except (json.JSONDecodeError, IOError):
            # If file is corrupted or unreadable, start fresh
            return {"tasks": {}, "next_id": 1}

    def save(self, tasks: Dict[int, Any], next_id: int) -> None:
        """
        Save task data to JSON file.

        Args:
            tasks: Dictionary mapping task IDs to task dictionaries
            next_id: Next available task ID
        """
        # Convert task objects to dictionaries
        tasks_dict = {}
        for task_id, task in tasks.items():
            if hasattr(task, '__dict__'):
                # Task object - convert to dict
                tasks_dict[str(task_id)] = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed
                }
            else:
                # Already a dict
                tasks_dict[str(task_id)] = task

        data = {
            "tasks": tasks_dict,
            "next_id": next_id
        }

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        # Write atomically by writing to temp file then renaming
        temp_path = self.file_path + ".tmp"
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            # Atomic rename (works on Windows and Unix)
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
            os.rename(temp_path, self.file_path)
        except Exception as e:
            # Clean up temp file if something went wrong
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
