from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
import uuid
from sqlalchemy import Column, DateTime, String

if TYPE_CHECKING:
    from .task import Task

class UserBase(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(
    sa_column=Column(String(255), unique=True, nullable=False)
    )
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))

class User(UserBase, table=True):
    __tablename__ = "users"

    hashed_password: str = Field(nullable=False)

    # Relationship back-reference
    tasks: List["Task"] = Relationship(back_populates="user")