● ---
  ##name: "mcp-task-executor"
  description: "Execute MCP tool calls via official SDK and return structured results with error handling"
  version: "1.0.0"
  ---

  # MCP Task Executor

  ## When to Use This Skill

  - When executing prepared MCP tool calls against an MCP server
  - When communicating with task management MCP servers using the official SDK
  - When handling tool execution errors and timeouts gracefully
  - When transforming raw MCP responses into structured result objects
  - When building the execution layer between orchestration and response formatting

  ## How This Skill Works

  1. Receive tool call object with `tool_name` and `parameters` from orchestrator
  2. Initialize or reuse MCP client connection to target server
  3. Validate connection state and server availability
  4. Execute tool call via `client.call_tool(tool_name, parameters)`
  5. Handle execution errors, timeouts, and connection failures
  6. Parse raw MCP response into structured result object
  7. Return execution result with success/failure status and payload

  ## Output Format

  - Returns a dictionary with `success`, `data`, and `error` keys
  - Success is a boolean indicating execution outcome
  - Data contains the tool response payload on success
  - Error contains structured error information on failure

  ```python
  # Example: Successful task creation
  # Input: {"tool_name": "create_task", "parameters": {"title": "Buy groceries", "description": "Get milk"}}
  # Output:
  {
      "success": True,
      "data": {
          "task_id": "42",
          "title": "Buy groceries",
          "description": "Get milk",
          "status": "pending",
          "created_at": "2026-02-01T10:30:00Z"
      },
      "error": None
  }

  # Example: Successful task list
  # Input: {"tool_name": "list_tasks", "parameters": {"status": "pending"}}
  # Output:
  {
      "success": True,
      "data": {
          "tasks": [
              {"task_id": "1", "title": "Buy groceries", "status": "pending"},
              {"task_id": "3", "title": "Call dentist", "status": "pending"}
          ],
          "total_count": 2
      },
      "error": None
  }

  # Example: Task not found error
  # Input: {"tool_name": "update_task", "parameters": {"task_id": "999", "status": "completed"}}
  # Output:
  {
      "success": False,
      "data": None,
      "error": {
          "code": "NOT_FOUND",
          "message": "Task with id '999' not found",
          "details": {"task_id": "999"}
      }
  }

  # Example: Connection error
  # Input: {"tool_name": "list_tasks", "parameters": {}}
  # Output:
  {
      "success": False,
      "data": None,
      "error": {
          "code": "CONNECTION_ERROR",
          "message": "Failed to connect to MCP server",
          "details": {"server": "task-server", "timeout_ms": 5000}
      }
  }

  Quality Criteria

  - Uses official MCP SDK (mcp package) for all server communication
  - Implements connection pooling or reuse for efficiency
  - Configurable timeout with sensible defaults (5000ms)
  - Comprehensive error taxonomy: NOT_FOUND, VALIDATION_ERROR, CONNECTION_ERROR, TIMEOUT, SERVER_ERROR
  - Structured error responses with code, message, and contextual details
  - No business logic - pure execution and response transformation
  - Async/await support for non-blocking execution
  - Retry logic for transient failures (configurable, disabled by default)
  - Type hints with TypedDict for all input/output structures
  - Unit testable with mocked MCP client responses
  - Logs execution metrics (duration, success/failure) for observability