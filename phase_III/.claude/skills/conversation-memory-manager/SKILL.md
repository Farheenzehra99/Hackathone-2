---
  ##name: "conversation-memory-manager"
  description: "Persist and retrieve conversation messages from database for stateless chat architecture"
  version: "1.0.0"
  ---

  # Conversation Memory Manager

  ## When to Use This Skill

  - When storing new user or assistant messages to the database
  - When retrieving conversation history for a specific session or user
  - When implementing stateless chat flows that require persistence between requests
  - When managing conversation lifecycle (create, append, retrieve, clear)
  - When building the data layer for chat-based applications with SQLModel/Postgres

  ## How This Skill Works

  1. Receive operation request (store, retrieve, clear) with conversation context
  2. Validate required fields (conversation_id, user_id, message content)
  3. Connect to database using async SQLModel session
  4. Execute appropriate CRUD operation based on request type
  5. Handle database errors and constraint violations gracefully
  6. Return operation result with stored/retrieved data or error status

  ## Output Format

  - All operations return a dictionary with `success`, `data`, and `error` keys
  - Store operations return the created message record
  - Retrieve operations return ordered list of messages
  - Clear operations return count of deleted messages

  ```python
  # Example: Store user message
  # Input: {"operation": "store", "conversation_id": "conv-123", "user_id": "user-456", "role": "user", "content": "Add
  a task called Buy milk"}
  # Output:
  {
      "success": True,
      "data": {
          "message_id": "msg-789",
          "conversation_id": "conv-123",
          "user_id": "user-456",
          "role": "user",
          "content": "Add a task called Buy milk",
          "created_at": "2026-02-01T14:30:00Z"
      },
      "error": None
  }

  # Example: Store assistant message
  # Input: {"operation": "store", "conversation_id": "conv-123", "user_id": "user-456", "role": "assistant", "content":
  "I've created the task 'Buy milk' for you."}
  # Output:
  {
      "success": True,
      "data": {
          "message_id": "msg-790",
          "conversation_id": "conv-123",
          "user_id": "user-456",
          "role": "assistant",
          "content": "I've created the task 'Buy milk' for you.",
          "created_at": "2026-02-01T14:30:01Z"
      },
      "error": None
  }

  # Example: Retrieve conversation history
  # Input: {"operation": "retrieve", "conversation_id": "conv-123", "user_id": "user-456", "limit": 50}
  # Output:
  {
      "success": True,
      "data": {
          "conversation_id": "conv-123",
          "messages": [
              {"message_id": "msg-789", "role": "user", "content": "Add a task called Buy milk", "created_at":
  "2026-02-01T14:30:00Z"},
              {"message_id": "msg-790", "role": "assistant", "content": "I've created the task 'Buy milk' for you.",
  "created_at": "2026-02-01T14:30:01Z"}
          ],
          "total_count": 2
      },
      "error": None
  }

  # Example: Clear conversation history
  # Input: {"operation": "clear", "conversation_id": "conv-123", "user_id": "user-456"}
  # Output:
  {
      "success": True,
      "data": {
          "conversation_id": "conv-123",
          "deleted_count": 15
      },
      "error": None
  }

  # Example: Retrieve with empty history
  # Input: {"operation": "retrieve", "conversation_id": "conv-new", "user_id": "user-456"}
  # Output:
  {
      "success": True,
      "data": {
          "conversation_id": "conv-new",
          "messages": [],
          "total_count": 0
      },
      "error": None
  }

  # Example: Store with invalid conversation
  # Input: {"operation": "store", "conversation_id": "", "user_id": "user-456", "role": "user", "content": "Hello"}
  # Output:
  {
      "success": False,
      "data": None,
      "error": {
          "code": "VALIDATION_ERROR",
          "message": "conversation_id is required",
          "details": {"field": "conversation_id"}
      }
  }

  Quality Criteria

  - Uses SQLModel with async session for all database operations
  - Enforces user isolation: all queries filter by user_id (multi-tenant safety)
  - Messages always retrieved in chronological order (ORDER BY created_at ASC)
  - Configurable message limit with sensible default (50 messages)
  - Supports pagination for large conversation histories
  - Validates role against allowed values: system, user, assistant
  - Handles database connection errors and constraint violations
  - Error taxonomy: VALIDATION_ERROR, NOT_FOUND, DATABASE_ERROR, CONSTRAINT_VIOLATION
  - Type hints with Pydantic models for request/response validation
  - Async/await throughout for non-blocking I/O
  - Unit testable with mock database sessions
  - Indexes on (conversation_id, user_id, created_at) for query performance
