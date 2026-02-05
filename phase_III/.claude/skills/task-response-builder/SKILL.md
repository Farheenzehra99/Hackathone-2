---
  ##name: "task-response-builder"
  description: "Transform MCP tool results into friendly, human-readable assistant messages for users"
  version: "1.0.0"
  ---

  # Task Response Builder

  ## When to Use This Skill

  - When converting raw MCP tool execution results into user-facing messages
  - When formatting task creation, completion, update, and deletion confirmations
  - When presenting task lists in a readable, scannable format
  - When transforming error responses into helpful, non-technical explanations
  - When building the final output layer of a task management chatbot pipeline

  ## How This Skill Works

  1. Receive structured result object from MCP task executor
  2. Determine result type based on original operation and success status
  3. Select appropriate message template for the operation type
  4. Extract relevant data fields for template interpolation
  5. Format message with proper tone, grammar, and optional details
  6. Return human-friendly response string ready for display

  ## Output Format

  - Returns a dictionary with `message` (str) and `message_type` (str) keys
  - Message types: `confirmation`, `info`, `error`, `warning`
  - Messages use natural language with friendly, professional tone
  - Success messages include relevant task details
  - Error messages are helpful without exposing technical details

  ```python
  # Example: Task created successfully
  # Input: {"success": True, "data": {"task_id": "42", "title": "Buy groceries"}, "operation": "create_task"}
  # Output:
  {
      "message": "I've created your task 'Buy groceries'. You can find it in your task list.",
      "message_type": "confirmation"
  }

  # Example: Task completed successfully
  # Input: {"success": True, "data": {"task_id": "5", "title": "Call dentist", "status": "completed"}, "operation":
  "complete_task"}
  # Output:
  {
      "message": "Nice work! I've marked 'Call dentist' as complete.",
      "message_type": "confirmation"
  }

  # Example: Task list returned
  # Input: {"success": True, "data": {"tasks": [{"task_id": "1", "title": "Buy groceries", "status": "pending"},
  {"task_id": "3", "title": "Call dentist", "status": "pending"}], "total_count": 2}, "operation": "list_tasks"}
  # Output:
  {
      "message": "Here are your pending tasks:\n\n1. Buy groceries\n2. Call dentist\n\nYou have 2 tasks waiting.",
      "message_type": "info"
  }

  # Example: Empty task list
  # Input: {"success": True, "data": {"tasks": [], "total_count": 0}, "operation": "list_tasks"}
  # Output:
  {
      "message": "You don't have any tasks right now. Would you like to create one?",
      "message_type": "info"
  }

  # Example: Task not found error
  # Input: {"success": False, "error": {"code": "NOT_FOUND", "message": "Task not found"}, "operation": "complete_task"}
  # Output:
  {
      "message": "I couldn't find that task. It may have been deleted or the task ID might be incorrect.",
      "message_type": "error"
  }

  # Example: Connection error
  # Input: {"success": False, "error": {"code": "CONNECTION_ERROR", "message": "Server unavailable"}, "operation":
  "list_tasks"}
  # Output:
  {
      "message": "I'm having trouble reaching the task service right now. Please try again in a moment.",
      "message_type": "error"
  }

  # Example: Task deleted
  # Input: {"success": True, "data": {"task_id": "7", "title": "Old reminder"}, "operation": "delete_task"}
  # Output:
  {
      "message": "Done! I've removed 'Old reminder' from your tasks.",
      "message_type": "confirmation"
  }

  Quality Criteria

  - Pure function with no side effects or external calls
  - Consistent, friendly tone across all message types
  - Encouragement on task completion without being excessive
  - Clear, actionable guidance in error messages
  - No technical jargon or error codes exposed to users
  - Proper grammar and punctuation in all outputs
  - Handles all operation types: create, complete, update, delete, list, get
  - Graceful handling of missing or malformed input data
  - Supports singular/plural grammar (1 task vs 2 tasks)
  - Unit testable with comprehensive operation/result combinations
  - Extensible template system for adding new operation types