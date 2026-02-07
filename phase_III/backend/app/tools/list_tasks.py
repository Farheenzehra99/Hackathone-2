"""List tasks tool - retrieves user's tasks with optional filters."""
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.task import Task
from ..services.error_formatter import ErrorFormatter


async def list_tasks(
    user_id: str,
    db: AsyncSession = None,
    status: Optional[str] = "all",
    priority: Optional[str] = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    Retrieve tasks for authenticated user with optional filters.

    Args:
        user_id: Authenticated user ID from JWT (required)
        db: Database session
        status: Filter by status - "pending", "completed", or "all" (default: "all")
        priority: Filter by priority - "low", "medium", or "high" (optional)
        limit: Maximum number of tasks to return (default: 50, max: 100)

    Returns:
        {
            "success": bool,
            "tasks": [...] or None,
            "count": int,
            "error": str or None
        }
    """
    try:
        # Validate status
        valid_statuses = ["pending", "completed", "all"]
        if status not in valid_statuses:
            return {
                "success": False,
                "tasks": None,
                "count": 0,
                "error": f"Status must be one of: {', '.join(valid_statuses)}"
            }

        # Validate priority if provided
        if priority:
            valid_priorities = ["low", "medium", "high"]
            if priority not in valid_priorities:
                return {
                    "success": False,
                    "tasks": None,
                    "count": 0,
                    "error": f"Priority must be one of: {', '.join(valid_priorities)}"
                }

        # Validate limit
        if limit > 100:
            limit = 100
        if limit < 1:
            limit = 1

        # Build query
        query = select(Task).where(Task.user_id == user_id)

        # Apply status filter
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        # Apply priority filter
        if priority:
            query = query.where(Task.priority == priority)

        # Apply limit and order by created_at desc
        query = query.order_by(Task.created_at.desc()).limit(limit)

        # Execute query
        result = await db.execute(query)
        tasks_db = result.scalars().all()

        # Convert to dict format
        tasks = [
            {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks_db
        ]

        return {
            "success": True,
            "tasks": tasks,
            "count": len(tasks),
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "tasks": None,
            "count": 0,
            "error": ErrorFormatter.format_error(e, context="retrieving tasks")
        }


# Tool metadata for Cohere system prompt
TOOL_SCHEMA = {
    "name": "list_tasks",
    "description": "Retrieve user's tasks with optional filters",
    "parameters": {
        "user_id": {
            "type": "string",
            "description": "User ID from JWT (automatically injected)",
            "required": True
        },
        "status": {
            "type": "string",
            "description": "Filter by status: pending, completed, or all (default: all)",
            "enum": ["pending", "completed", "all"],
            "required": False
        },
        "priority": {
            "type": "string",
            "description": "Filter by priority: low, medium, or high (optional)",
            "enum": ["low", "medium", "high"],
            "required": False
        },
        "limit": {
            "type": "integer",
            "description": "Maximum number of tasks (default: 50, max: 100)",
            "required": False
        }
    }
}
