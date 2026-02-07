"""Tool executor service - parses and executes MCP tool calls."""
import json
import re
from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..tools import add_task, list_tasks, complete_task, update_task, delete_task, get_current_user


class ToolExecutor:
    """
    Executes MCP tools based on parsed Cohere responses.

    Supports:
    - JSON tool call parsing from Cohere output
    - Tool execution with database session
    - Error handling and validation
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize tool executor.

        Args:
            db: Database session for tool operations
        """
        self.db = db

        # Map tool names to functions
        self.tools = {
            "add_task": add_task.add_task,
            "list_tasks": list_tasks.list_tasks,
            "complete_task": complete_task.complete_task,
            "update_task": update_task.update_task,
            "delete_task": delete_task.delete_task,
            "get_current_user": get_current_user.get_current_user,
        }

    def parse_tool_call(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Parse tool call from Cohere response text.

        Looks for JSON code blocks in format:
        ```json
        {"tool": "tool_name", "params": {...}}
        ```

        Args:
            text: Cohere response text

        Returns:
            Parsed tool call dict or None if no tool call found
        """
        try:
            # Extract JSON from code block
            pattern = r'```json\s*(\{.*?\})\s*```'
            matches = re.findall(pattern, text, re.DOTALL)

            if not matches:
                return None

            # Parse first JSON block
            tool_call = json.loads(matches[0])

            # Validate structure
            if "tool" not in tool_call or "params" not in tool_call:
                return None

            return tool_call

        except (json.JSONDecodeError, IndexError):
            return None

    async def execute_tool(
        self,
        tool_name: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool by name with given parameters.

        Args:
            tool_name: Name of tool to execute
            params: Tool parameters

        Returns:
            Tool execution result
        """
        try:
            # Check if tool exists
            if tool_name not in self.tools:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}"
                }

            # Get tool function
            tool_func = self.tools[tool_name]

            # Add database session to params
            params["db"] = self.db

            # Execute tool
            result = await tool_func(**params)

            return result

        except TypeError as e:
            return {
                "success": False,
                "error": f"Invalid parameters for {tool_name}: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}"
            }

    async def execute_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Parse and execute tool call from Cohere response text.

        Args:
            text: Cohere response text

        Returns:
            Tool execution result or None if no tool call found
        """
        tool_call = self.parse_tool_call(text)

        if not tool_call:
            return None

        tool_name = tool_call["tool"]
        params = tool_call["params"]

        result = await self.execute_tool(tool_name, params)

        return result
