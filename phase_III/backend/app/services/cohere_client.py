"""Cohere API client service for natural language understanding."""
import os
from typing import Any, Dict, List, Optional

import cohere


class CohereClient:
    """
    Cohere API client for chatbot natural language processing.

    Uses command-r-plus model with temperature 0.3 for consistent behavior.
    Supports tool calling via structured JSON output parsing.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Cohere client.

        Args:
            api_key: Cohere API key (defaults to COHERE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")

        self.client = cohere.Client(self.api_key)
        # command-r was removed Sept 15, 2025. Use a live model.
        self.model = os.getenv("COHERE_MODEL", "command-a-03-2025")
        self.temperature = 0.3

    def build_system_prompt(self, user_id: str) -> str:
        """
        Build system prompt with tool schemas and instructions.

        Args:
            user_id: User ID to inject into tool calls

        Returns:
            System prompt string
        """
        return f"""You are a helpful task management assistant for the Evolution of Todo app.

AVAILABLE TOOLS:
1. add_task(title: str, description?: str, priority?: "low"|"medium"|"high", user_id: str)
   - Creates a new task for the user
   - Returns: {{"success": bool, "task": object, "error": str?}}
   - Examples: "Add task to buy groceries", "Create a high priority task for the meeting"

2. list_tasks(user_id: str, status?: "pending"|"completed"|"all", priority?: "low"|"medium"|"high", limit?: int)
   - Retrieves tasks with optional filters (default: all tasks, limit 50)
   - Returns: {{"success": bool, "tasks": array, "count": int, "error": str?}}
   - Examples: "Show my tasks", "List pending tasks", "Show high priority tasks"

3. complete_task(task_id: str, user_id: str, completed: bool)
   - Marks task as complete or incomplete
   - Returns: {{"success": bool, "task": object, "message": str, "error": str?}}
   - Examples: "Mark task 5 as done", "Complete the groceries task", "Mark task 3 as incomplete"

4. update_task(task_id: str, user_id: str, title?: str, description?: str, priority?: str, completed?: bool)
   - Updates task properties (title, description, priority, or completion status)
   - Returns: {{"success": bool, "task": object, "message": str, "error": str?}}
   - Examples: "Change priority of task 5 to high", "Update task 3 description to 'Buy milk and bread'"

5. delete_task(task_id: str, user_id: str)
   - Deletes a task permanently
   - Returns: {{"success": bool, "message": str, "error": str?}}
   - Examples: "Delete task 5", "Remove the groceries task"

6. get_current_user(user_id: str)
   - Gets information about the current logged-in user
   - Returns: {{"success": bool, "user": {{"id": str, "email": str, "name": str?}}, "error": str?}}
   - Examples: "Who am I?", "What's my email?", "Show my account info"

MULTI-STEP QUERIES:
- You can handle complex queries that require multiple tool calls
- Execute tools sequentially and use results from one tool in the next
- Examples: "Add task 'Weekly meeting' and list my pending tasks", "Mark task 5 done and show all completed tasks"
- Maximum 5 tool calls per conversation to prevent loops

INSTRUCTIONS:
- Understand the user's intent from their natural language message
- If a tool is needed, output ONLY a JSON code block in this exact format:
  ```json
  {{"tool": "tool_name", "params": {{...}}}}
  ```
- If no tool is needed, respond conversationally
- Always use user_id: "{user_id}" for all tool calls
- Use ✓ for success messages, ⚠ for errors/warnings
- Be concise and friendly
- If user intent is unclear, ask clarifying questions
- After executing a tool, interpret the result and provide a natural language response

EXAMPLES:
User: "Add a task to buy groceries"
Assistant: ```json
{{"tool": "add_task", "params": {{"title": "buy groceries", "user_id": "{user_id}"}}}}
```

User: "Show me my tasks"
Assistant: ```json
{{"tool": "list_tasks", "params": {{"user_id": "{user_id}"}}}}
```

User: "Mark task 5 as done"
Assistant: ```json
{{"tool": "complete_task", "params": {{"task_id": "5", "user_id": "{user_id}", "completed": true}}}}
```

User: "Change priority of task 3 to high"
Assistant: ```json
{{"tool": "update_task", "params": {{"task_id": "3", "user_id": "{user_id}", "priority": "high"}}}}
```

User: "Delete task 7"
Assistant: ```json
{{"tool": "delete_task", "params": {{"task_id": "7", "user_id": "{user_id}"}}}}
```

User: "Who am I?"
Assistant: ```json
{{"tool": "get_current_user", "params": {{"user_id": "{user_id}"}}}}
```

USER_ID: {user_id}
"""

    async def chat(
        self,
        message: str,
        user_id: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Send chat message to Cohere API.

        Args:
            message: User's message
            user_id: User ID for tool calls
            conversation_history: Previous messages [{"role": "user|assistant", "content": "..."}]

        Returns:
            {
                "text": str,  # Cohere response text
                "finish_reason": str
            }
        """
        try:
            # Build conversation with system prompt
            chat_history = conversation_history or []

            # Format for Cohere API
            cohere_history = []
            for msg in chat_history:
                cohere_history.append({
                    "role": "USER" if msg["role"] == "user" else "CHATBOT",
                    "message": msg["content"]
                })

            # Call Cohere API
            response = self.client.chat(
                message=message,
                chat_history=cohere_history,
                model=self.model,
                temperature=self.temperature,
                preamble=self.build_system_prompt(user_id)
            )

            return {
                "text": response.text,
                "finish_reason": "COMPLETE"
            }

        except Exception as e:
            return {
                "text": f"⚠ I'm having trouble connecting right now. Please try again. Error: {str(e)}",
                "finish_reason": "ERROR"
            }
