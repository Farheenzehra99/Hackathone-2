from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from pydantic import BaseModel
from ....models.task import Task, TaskBase, TaskCreate
from ....models.user import User
from ....api.deps import get_session, get_current_user_safe
from ....core.security import validate_user_ownership
from ....utils.exceptions import UserMismatchException, ResourceNotFoundException
from ....core.config import settings
import logging
from typing import Optional, Literal
from sqlmodel import SQLModel, Field

# Request body model for updating a task (all fields optional)
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[Literal["low", "medium", "high"]] = None

class UpdateCompletionRequest(BaseModel):
    completed: bool

router = APIRouter()

# Configure logger
logger = logging.getLogger(__name__)

@router.get("/", response_model=dict)
async def get_tasks(
    current_user_id: str = Depends(get_current_user_safe),
    session: AsyncSession = Depends(get_session),
    status: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    # Build query based on status filter
    query = select(Task).where(Task.user_id == current_user_id)

    if status and status != "all":
        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)

    query = query.offset(offset).limit(limit).order_by(Task.created_at.desc())
    result = await session.execute(query)
    tasks = result.scalars().all()

    count_query = select(func.count(Task.id)).where(Task.user_id == current_user_id)
    if status and status != "all":
        if status == "completed":
            count_query = count_query.where(Task.completed == True)
        elif status == "pending":
            count_query = count_query.where(Task.completed == False)

    count_result = await session.execute(count_query)
    total = count_result.scalar()

    return {
        "success": True,
        "data": {
            "tasks": tasks,
            "total": total,
            "page": (offset // limit) + 1,
            "limit": limit
        },
        "message": "Tasks retrieved successfully"
    }


@router.post("/", response_model=dict)
async def create_task(
    task_data: TaskCreate = Body(...),   # <-- Change here
    current_user_id: str = Depends(get_current_user_safe),
    session: AsyncSession = Depends(get_session)
):
    if not task_data.title or len(task_data.title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required"
        )

    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,   # <-- use completed from TaskCreate
        priority=task_data.priority,
        user_id=current_user_id
    )

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return {
        "success": True,
        "data": db_task,
        "message": "Task created successfully"
    }

@router.get("/{task_id}", response_model=dict)
async def get_task(
    task_id: int = Path(..., description="Task ID"),
    current_user_id: str = Depends(get_current_user_safe),
    session: AsyncSession = Depends(get_session)
):
    query = select(Task).where(Task.id == task_id).where(Task.user_id == current_user_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    return {
        "success": True,
        "data": task,
        "message": "Task retrieved successfully"
    }
@router.put("/{task_id}", response_model=dict)
async def update_task(
    task_id: int = Path(..., description="Task ID"),
    task_data: TaskUpdate = Body(...),
    current_user_id: str = Depends(get_current_user_safe),
    session: AsyncSession = Depends(get_session)
):
    # Query task by ID and user_id
    query = select(Task).where(Task.id == task_id).where(Task.user_id == current_user_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    # Update fields only if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
    if task_data.priority is not None:
        task.priority = task_data.priority

    await session.commit()
    await session.refresh(task)

    return {
        "success": True,
        "data": task,
        "message": "Task updated successfully"
    }

@router.delete("/{task_id}", response_model=dict)
async def delete_task(
    task_id: int = Path(..., description="Task ID"),
    current_user_id: str = Depends(get_current_user_safe),
    session: AsyncSession = Depends(get_session)
):
    query = select(Task).where(Task.id == task_id).where(Task.user_id == current_user_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    await session.delete(task)
    await session.commit()

    return {
        "success": True,
        "data": None,
        "message": "Task deleted successfully"
    }

@router.patch("/{task_id}/complete", response_model=dict)
async def update_task_completion(
    task_id: int = Path(..., description="Task ID"),
    update_data: UpdateCompletionRequest = Body(...),
    current_user_id: str = Depends(get_current_user_safe),
    session: AsyncSession = Depends(get_session)
):
    query = select(Task).where(Task.id == task_id).where(Task.user_id == current_user_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found"
        )

    task.completed = update_data.completed

    await session.commit()
    await session.refresh(task)

    return {
        "success": True,
        "data": task,
        "message": "Task completion status updated"
    }
