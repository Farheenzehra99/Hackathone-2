from fastapi import Depends, HTTPException, status
from typing import Dict, Any
from ..core.security import get_current_user, validate_user_ownership
from ..db.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.exceptions import UserMismatchException

async def get_current_user_safe(
    token_data: dict = Depends(get_current_user)
) -> Dict[str, Any]:
    return token_data["user_id"]

async def get_session() -> AsyncSession:
    async for session in get_async_session():
        yield session

