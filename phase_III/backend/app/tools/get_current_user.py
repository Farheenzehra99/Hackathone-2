"""Get current user tool - retrieves user information."""
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.user import User
from ..services.error_formatter import ErrorFormatter


async def get_current_user(
    user_id: str,
    db: AsyncSession = None
) -> Dict[str, Any]:
    """
    Get current user information.

    Args:
        user_id: Authenticated user ID from JWT (required)
        db: Database session

    Returns:
        {
            "success": bool,
            "user": {"id": str, "email": str, "name": str?} or None,
            "error": str or None
        }
    """
    try:
        # Query user
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            return {
                "success": False,
                "user": None,
                "error": f"⚠ User not found"
            }

        # Convert to dict (exclude sensitive data)
        user_data = {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }

        return {
            "success": True,
            "user": user_data,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "user": None,
            "error": ErrorFormatter.format_error(e, context="retrieving user information")
        }


# Tool metadata for Cohere system prompt
TOOL_SCHEMA = {
    "name": "get_current_user",
    "description": "Get information about the current logged-in user",
    "parameters": {
        "user_id": {
            "type": "string",
            "description": "User ID from JWT (automatically injected)",
            "required": True
        }
    }
}
