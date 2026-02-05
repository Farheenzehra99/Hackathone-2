 ---
  ##name: "conversation-context-builder"
  description: "Transform database chat history into OpenAI-compatible message arrays for agent consumption"
  version: "1.0.0"
  ---

  # Conversation Context Builder

  ## When to Use This Skill

  - When preparing chat history from database for OpenAI Agents SDK calls
  - When transforming stored Message models into properly formatted message arrays
  - When ensuring chronological ordering and message integrity before agent invocation
  - When filtering out malformed or empty messages from conversation context
  - When building stateless, testable conversation preparation pipelines

  ## How This Skill Works

  1. Receive conversation ID and fetch all associated messages from database
  2. Validate each message for required fields (role, content, timestamp)
  3. Filter out empty, malformed, or invalid message entries
  4. Sort messages chronologically by timestamp (ascending order)
  5. Transform database Message models into OpenAI SDK format: `{"role": str, "content": str}`
  6. Return clean, ordered array ready for OpenAI Agents SDK consumption

  ## Output Format

  - Returns a list of dictionaries with `role` and `content` keys
  - Roles are validated against allowed values: `system`, `user`, `assistant`
  - Content is trimmed of leading/trailing whitespace
  - Empty content messages are excluded from output
  - Array is guaranteed to be in chronological order
  - Output is deterministic given same input (pure function)

  ```python
  # Example output structure
  [
      {"role": "system", "content": "You are a helpful task assistant."},
      {"role": "user", "content": "Add a task called Buy groceries"},
      {"role": "assistant", "content": "I've created the task 'Buy groceries' for you."},
      {"role": "user", "content": "Mark it as done"}
  ]

  Quality Criteria

  - Pure function with no side effects (stateless transformation)
  - All messages validated for required fields before inclusion
  - Chronological ordering guaranteed via timestamp sorting
  - Empty or whitespace-only content messages filtered out
  - Role values strictly validated against OpenAI allowed roles
  - Type hints and return type annotations on all functions
  - Unit testable with mock database responses
  - Graceful handling of edge cases: empty history, single message, missing fields
