from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Column, DateTime
if TYPE_CHECKING:
    from .user import User
from typing import Optional, Literal
from sqlmodel import SQLModel, Field

# schemas/task.py
class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Literal["low", "medium", "high"] = "medium"


class TaskBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", max_length=10)
    user_id: str = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    # Relationships
    user: "User" = Relationship(back_populates="tasks")