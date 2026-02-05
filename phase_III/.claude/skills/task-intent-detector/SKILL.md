---
  ##name: "task-intent-detector"
  description: "Parse natural language input to classify task intent and extract relevant entities"
  version: "1.0.0"
  ---

  # Task Intent Detector

  ## When to Use This Skill

  - When parsing user messages to determine their intended task management action
  - When extracting task entities (title, description, task_id, status) from natural language
  - When classifying user input into actionable intent categories before routing
  - When building the first stage of a task management chatbot pipeline
  - When needing pure intent classification without executing any operations

  ## How This Skill Works

  1. Receive raw user message string as input
  2. Normalize input (lowercase, trim whitespace, handle common variations)
  3. Apply intent classification using pattern matching or LLM-based detection
  4. Extract relevant entities based on detected intent type
  5. Validate extracted entities for completeness and format
  6. Return structured intent object with classification and entities

  ## Output Format

  - Returns a dictionary with `intent_type`, `confidence`, and `entities` keys
  - Intent types are one of: `create_task`, `complete_task`, `update_task`, `delete_task`, `list_tasks`, `get_task`,
  `unknown`
  - Confidence is a float between 0.0 and 1.0
  - Entities vary by intent type (see examples below)

  ```python
  # Example: Create task intent
  # Input: "Add a new task called 'Buy groceries' with description 'Get milk and bread'"
  # Output:
  {
      "intent_type": "create_task",
      "confidence": 0.95,
      "entities": {
          "title": "Buy groceries",
          "description": "Get milk and bread"
      }
  }

  # Example: Complete task intent
  # Input: "Mark task 5 as done"
  # Output:
  {
      "intent_type": "complete_task",
      "confidence": 0.92,
      "entities": {
          "task_id": "5"
      }
  }

  # Example: List tasks intent
  # Input: "Show me all my pending tasks"
  # Output:
  {
      "intent_type": "list_tasks",
      "confidence": 0.88,
      "entities": {
          "filter_status": "pending"
      }
  }

  # Example: Update task intent
  # Input: "Change the title of task 3 to 'Call dentist tomorrow'"
  # Output:
  {
      "intent_type": "update_task",
      "confidence": 0.90,
      "entities": {
          "task_id": "3",
          "title": "Call dentist tomorrow"
      }
  }

  # Example: Unknown intent
  # Input: "What's the weather like?"
  # Output:
  {
      "intent_type": "unknown",
      "confidence": 0.15,
      "entities": {}
  }

  Quality Criteria

  - Stateless function with no side effects or database operations
  - Clear separation between intent classification and entity extraction
  - Handles ambiguous input gracefully with lower confidence scores
  - Supports common linguistic variations (add/create, done/complete/finish, show/list/get)
  - Returns unknown intent for off-topic or unrecognized requests
  - All extracted entities are strings (type conversion happens downstream)
  - Confidence threshold recommendations documented for routing decisions
  - Unit testable with comprehensive input/output examples
  - Handles edge cases: empty input, special characters, multi-language fragments