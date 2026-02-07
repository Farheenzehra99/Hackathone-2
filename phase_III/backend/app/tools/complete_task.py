"""Complete task tool - marks task as complete or incomplete."""
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.task import Task
from ..services.error_formatter import ErrorFormatter


async def complete_task(
    task_id: str,
    user_id: str,
    completed: bool,
    db: AsyncSession = None
) -> Dict[str, Any]:
    """
    Mark task as complete or incomplete for authenticated user.

    Args:
        task_id: Task ID to update (required)
        user_id: Authenticated user ID from JWT (required)
        completed: True to mark complete, False to mark incomplete (required)
        db: Database session

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

        # Update completion status
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

        status_text = "complete" if completed else "incomplete"

        return {
            "success": True,
            "task": task_data,
            "error": None,
            "message": f"✓ Task {task_id} marked as {status_text}!"
        }

    except Exception as e:
        return {
            "success": False,
            "task": None,
            "error": ErrorFormatter.format_error(e, context="updating task")
        }


# Tool metadata for Cohere system prompt
TOOL_SCHEMA = {
    "name": "complete_task",
    "description": "Mark task as complete or incomplete",
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
        "completed": {
            "type": "boolean",
            "description": "True to mark complete, False to mark incomplete",
            "required": True
        }
    }
}
