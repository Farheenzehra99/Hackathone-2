"""Update task tool - updates task properties for authenticated user."""
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.task import Task
from ..services.error_formatter import ErrorFormatter


async def update_task(
    task_id: str,
    user_id: str,
    db: AsyncSession = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Update task properties for authenticated user.

    Args:
        task_id: Task ID to update (required)
        user_id: Authenticated user ID from JWT (required)
        db: Database session
        title: New task title (optional)
        description: New task description (optional)
        priority: New priority - "low", "medium", or "high" (optional)
        completed: New completion status (optional)

    Returns:
        {
            "success": bool,
            "task": {...} or None,
            "error": str or None
        }
    """
    try:
        # Validate task_id
        if not task_id or not task_id.strip():
            return {
                "success": False,
                "task": None,
                "error": "Task ID is required"
            }

        # Convert task_id to int
        try:
            task_id_int = int(task_id)
        except ValueError:
            return {
                "success": False,
                "task": None,
                "error": f"⚠ Invalid task ID format: {task_id}"
            }

        # Validate priority if provided
        if priority:
            valid_priorities = ["low", "medium", "high"]
            if priority not in valid_priorities:
                return {
                    "success": False,
                    "task": None,
                    "error": f"Priority must be one of: {', '.join(valid_priorities)}"
                }

        # Query task with user isolation
        query = select(Task).where(
            Task.id == task_id_int,
            Task.user_id == user_id
        )
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return {
                "success": False,
                "task": None,
                "error": f"⚠ I couldn't find task {task_id}. Please check the task ID."
            }

        # Update fields if provided
        if title is not None and title.strip():
            task.title = title.strip()

        if description is not None:
            task.description = description.strip() if description.strip() else None

        if priority is not None:
            task.priority = priority

        if completed is not None:
            task.completed = completed

        await db.commit()
        await db.refresh(task)

        # Convert to dict
        task_data = {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "completed": task.completed,
            "user_id": task.user_id,
            "updated_at": task.updated_at.isoformat()
        }

        return {
            "success": True,
            "task": task_data,
            "error": None,
            "message": f"✓ Task {task_id} updated successfully!"
        }

    except Exception as e:
        return {
            "success": False,
            "task": None,
            "error": ErrorFormatter.format_error(e, context="updating task")
        }


# Tool metadata for Cohere system prompt
TOOL_SCHEMA = {
    "name": "update_task",
    "description": "Update task properties (title, description, priority, completed status)",
    "parameters": {
        "task_id": {
            "type": "string",
            "description": "Task ID to update (required)",
            "required": True
        },
        "user_id": {
            "type": "string",
            "description": "User ID from JWT (automatically injected)",
            "required": True
        },
        "title": {
            "type": "string",
            "description": "New task title (optional)",
            "required": False
        },
        "description": {
            "type": "string",
            "description": "New task description (optional)",
            "required": False
        },
        "priority": {
            "type": "string",
            "description": "New priority: low, medium, or high (optional)",
            "enum": ["low", "medium", "high"],
            "required": False
        },
        "completed": {
            "type": "boolean",
            "description": "New completion status (optional)",
            "required": False
        }
    }
}
