---
  ##name: "mcp-tool-orchestrator"
  description: "Map detected task intents to MCP tool names and parameter schemas for execution"
  version: "1.0.0"
  ---

  # MCP Tool Orchestrator

  ## When to Use This Skill

  - When translating detected user intents into MCP tool call structures
  - When mapping intent types (create, complete, list, update, delete) to specific MCP tool names
  - When extracting and validating parameters from intent data for tool execution
  - When building the bridge layer between intent detection and tool execution
  - When ensuring parameter schemas match MCP server expectations

  ## How This Skill Works

  1. Receive detected intent dictionary with `intent_type` and extracted entities
  2. Validate intent type against supported MCP operations mapping
  3. Lookup corresponding MCP tool name from intent-to-tool registry
  4. Extract relevant parameters from intent entities (task_id, title, description, status, etc.)
  5. Transform parameters into exact schema required by target MCP tool
  6. Return structured tool call object with `tool_name` and `parameters` ready for execution

  ## Output Format

  - Returns a dictionary with `tool_name` (str) and `parameters` (dict) keys
  - Tool names match exact MCP server tool identifiers
  - Parameters are validated and typed according to tool schema
  - Missing optional parameters are omitted (not set to null)
  - Required parameters raise validation errors if absent

  ```python
  # Intent-to-Tool Mapping Examples

  # Input: {"intent_type": "create_task", "title": "Buy groceries", "description": "Get milk and bread"}
  # Output:
  {
      "tool_name": "create_task",
      "parameters": {
          "title": "Buy groceries",
          "description": "Get milk and bread"
      }
  }

  # Input: {"intent_type": "complete_task", "task_id": "5"}
  # Output:
  {
      "tool_name": "update_task",
      "parameters": {
          "task_id": "5",
          "status": "completed"
      }
  }

  # Input: {"intent_type": "list_tasks", "filter_status": "pending"}
  # Output:
  {
      "tool_name": "list_tasks",
      "parameters": {
          "status": "pending"
      }
  }

  Quality Criteria

  - Pure function with deterministic output for same input
  - Complete coverage of all supported intent types in mapping registry
  - Strict parameter validation against MCP tool schemas
  - Clear error messages for unsupported intents or missing required parameters
  - No AI/LLM logic - purely rule-based transformation
  - Type hints on all functions with TypedDict for structured inputs/outputs
  - Unit testable with comprehensive intent-to-tool mapping coverage
  - Extensible registry pattern for adding new intent-to-tool mappings
  - Handles edge cases: unknown intents return error result, not exceptions
