"""Delete task tool - removes task for authenticated user."""
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.task import Task
from ..services.error_formatter import ErrorFormatter


async def delete_task(
    task_id: str,
    user_id: str,
    db: AsyncSession = None
) -> Dict[str, Any]:
    """
    Delete task for authenticated user.

    Args:
        task_id: Task ID to delete (required)
        user_id: Authenticated user ID from JWT (required)
        db: Database session

    Returns:
        {
            "success": bool,
            "message": str or None,
            "error": str or None
        }
    """
    try:
        # Validate task_id
        if not task_id or not task_id.strip():
            return {
                "success": False,
                "message": None,
                "error": "Task ID is required"
            }

        # Convert task_id to int
        try:
            task_id_int = int(task_id)
        except ValueError:
            return {
                "success": False,
                "message": None,
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
                "message": None,
                "error": f"⚠ I couldn't find task {task_id}. Please check the task ID."
            }

        # Store title for confirmation message
        task_title = task.title

        # Delete task
        await db.delete(task)
        await db.commit()

        return {
            "success": True,
            "message": f"✓ Task '{task_title}' (ID: {task_id}) deleted successfully!",
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "message": None,
            "error": ErrorFormatter.format_error(e, context="deleting task")
        }


# Tool metadata for Cohere system prompt
TOOL_SCHEMA = {
    "name": "delete_task",
    "description": "Delete a task permanently",
    "parameters": {
        "task_id": {
            "type": "string",
            "description": "Task ID to delete (required)",
            "required": True
        },
        "user_id": {
            "type": "string",
            "description": "User ID from JWT (automatically injected)",
            "required": True
        }
    }
}
