"""Add task tool - creates new task for authenticated user."""
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.task import Task
from ..services.error_formatter import ErrorFormatter


async def add_task(
    title: str,
    user_id: str,
    description: Optional[str] = None,
    priority: Optional[str] = "medium",
    db: AsyncSession = None
) -> Dict[str, Any]:
    """
    Create a new task for the authenticated user.

    Args:
        title: Task title (required)
        user_id: Authenticated user ID from JWT (required)
        description: Task description (optional)
        priority: Task priority - "low", "medium", or "high" (default: "medium")
        db: Database session

    Returns:
        {
            "success": bool,
            "task": {...} or None,
            "error": str or None
        }
    """
    try:
        # Validate priority
        valid_priorities = ["low", "medium", "high"]
        if priority and priority not in valid_priorities:
            return {
                "success": False,
                "task": None,
                "error": f"Priority must be one of: {', '.join(valid_priorities)}"
            }

        # Validate title
        if not title or not title.strip():
            return {
                "success": False,
                "task": None,
                "error": "Task title is required"
            }

        # Create task
        task = Task(
            title=title.strip(),
            description=description.strip() if description else None,
            priority=priority or "medium",
            completed=False,
            user_id=user_id
        )

        db.add(task)
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
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }

        return {
            "success": True,
            "task": task_data,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "task": None,
            "error": ErrorFormatter.format_error(e, context="creating task")
        }


# Tool metadata for Cohere system prompt
TOOL_SCHEMA = {
    "name": "add_task",
    "description": "Create a new task for the user",
    "parameters": {
        "title": {
            "type": "string",
            "description": "Task title (required)",
            "required": True
        },
        "description": {
            "type": "string",
            "description": "Task description (optional)",
            "required": False
        },
        "priority": {
            "type": "string",
            "description": "Task priority: low, medium, or high (default: medium)",
            "enum": ["low", "medium", "high"],
            "required": False
        },
        "user_id": {
            "type": "string",
            "description": "User ID from JWT (automatically injected)",
            "required": True
        }
    }
}
