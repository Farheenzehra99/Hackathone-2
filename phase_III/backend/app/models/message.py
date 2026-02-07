"""Message model for AI chatbot conversation history."""
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .conversation import Conversation


class Message(SQLModel, table=True):
    """
    Message model - represents a single message in a conversation.

    Attributes:
        id: Unique message identifier (UUID)
        conversation_id: Foreign key to conversations table (indexed)
        role: Message role - either "user" or "assistant"
        content: Message text content
        tool_calls: Optional JSON array of tool names invoked for this message
        created_at: Timestamp when message was created
        conversation: Relationship to Conversation model (many-to-one)
    """
    __tablename__ = "messages"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        description="Unique message identifier"
    )
    conversation_id: str = Field(
        foreign_key="conversations.id",
        index=True,
        description="Parent conversation ID"
    )
    role: str = Field(
        description="Message role: 'user' or 'assistant'",
        regex="^(user|assistant)$"
    )
    content: str = Field(
        description="Message text content"
    )
    tool_calls: Optional[str] = Field(
        default=None,
        description="JSON array of tool names invoked (optional)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Message creation timestamp"
    )

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
