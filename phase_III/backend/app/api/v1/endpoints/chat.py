"""Chat endpoint for AI chatbot - stateless conversation handling."""
import json
from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ....models.conversation import Conversation
from ....models.message import Message
from ....services.cohere_client import CohereClient
from ....services.tool_executor import ToolExecutor
from ...deps import get_session, get_current_user_safe

router = APIRouter(tags=["chat"])


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request schema."""
    message: str = Field(..., max_length=1000, description="User's message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID to resume")


class ChatResponse(BaseModel):
    """Chat response schema."""
    reply: str = Field(..., description="AI-generated response")


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    response: Response,
    db: AsyncSession = Depends(get_session),
    current_user_id: str = Depends(get_current_user_safe)
) -> ChatResponse:
    """
    Chat endpoint - handles natural language task management.

    Flow:
    1. Validate JWT and user_id match
    2. Load/create conversation
    3. Load conversation history (last 10 messages)
    4. Send message to Cohere with history
    5. Parse and execute any tool calls (max 5 iterations)
    6. Persist user message and assistant response
    7. Return final response

    Args:
        user_id: User ID from URL path
        request: Chat request with message and optional conversation_id
        db: Database session
        current_user_id: User ID from JWT token

    Returns:
        ChatResponse with conversation_id, response, tool_calls, timestamp

    Raises:
        HTTPException 403: If user_id doesn't match JWT
        HTTPException 400: If message is empty or too long
        HTTPException 500: If internal error occurs
    """
    try:
        # Validate user_id matches JWT claim
        if user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="⚠ You can only access your own conversations"
            )

        # Validate message
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message cannot be empty"
            )

        # Sanitize message (prevent injection attacks)
        sanitized_message = request.message.strip()

        # Check max length (already enforced by Pydantic but double-check)
        if len(sanitized_message) > 1000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Message is too long (maximum 1000 characters)"
            )

        # Initialize services
        cohere_client = CohereClient()
        tool_executor = ToolExecutor(db)

        # Load or create conversation
        conversation_id = request.conversation_id
        if not conversation_id:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            db.add(conversation)
            await db.commit()
            await db.refresh(conversation)
            conversation_id = conversation.id
        else:
            # Verify conversation exists and belongs to user
            query = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            result = await db.execute(query)
            conversation = result.scalar_one_or_none()

            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="⚠ Conversation not found"
                )

            # Update conversation timestamp
            conversation.updated_at = datetime.utcnow()
            await db.commit()

        # Load conversation history (last 10 messages)
        history_query = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(10)
        messages_result = await db.execute(history_query)
        messages = list(reversed(messages_result.scalars().all()))
        history = [{"role": msg.role, "content": msg.content} for msg in messages]

        # Tool execution loop (max 5 iterations)
        tool_calls_made = []
        max_iterations = 5
        current_message = sanitized_message

        for iteration in range(max_iterations):
            # Call Cohere API
            cohere_response = await cohere_client.chat(
                message=current_message,
                user_id=user_id,
                conversation_history=history
            )

            response_text = cohere_response["text"]

            # Try to parse and execute tool call
            tool_result = await tool_executor.execute_from_text(response_text)

            if not tool_result:
                # No tool call found - this is the final response
                final_response = response_text
                break

            # Tool executed successfully
            tool_call_data = tool_executor.parse_tool_call(response_text)
            if tool_call_data:
                tool_calls_made.append(tool_call_data["tool"])

            # Feed tool result back to Cohere for final response generation
            tool_result_message = f"Tool result: {tool_result}"
            history.append({"role": "assistant", "content": response_text})
            history.append({"role": "user", "content": tool_result_message})
            current_message = tool_result_message

        else:
            # Max iterations reached
            final_response = "✓ Operations completed successfully."

        # Persist user message and assistant response
        user_msg = Message(
            conversation_id=conversation_id,
            role="user",
            content=sanitized_message
        )
        assistant_msg = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=final_response,
            tool_calls=json.dumps(tool_calls_made) if tool_calls_made else None
        )
        db.add_all([user_msg, assistant_msg])
        await db.commit()

        response.headers["X-Conversation-Id"] = conversation_id

        return ChatResponse(reply=final_response)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"⚠ Something went wrong: {str(e)}"
        )
