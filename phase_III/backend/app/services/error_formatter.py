"""Error formatter service - converts exceptions to user-friendly messages."""
from typing import Any, Dict


class ErrorFormatter:
    """
    Formats error messages for user-friendly display.

    Converts technical exceptions into friendly messages with ✓/⚠ symbols.
    """

    @staticmethod
    def format_error(error: Exception, context: str = "") -> str:
        """
        Format exception into user-friendly message.

        Args:
            error: Exception to format
            context: Optional context for the error (e.g., "creating task")

        Returns:
            Formatted error message string
        """
        error_msg = str(error)

        # Already formatted errors (with ⚠ symbol)
        if error_msg.startswith("⚠"):
            return error_msg

        # Database errors
        if "connection" in error_msg.lower() or "database" in error_msg.lower():
            return f"⚠ Database connection issue. Please try again in a moment."

        # Validation errors
        if "validation" in error_msg.lower() or "invalid" in error_msg.lower():
            return f"⚠ {error_msg}"

        # Not found errors
        if "not found" in error_msg.lower():
            return f"⚠ {error_msg}"

        # Permission errors
        if "permission" in error_msg.lower() or "forbidden" in error_msg.lower():
            return f"⚠ You don't have permission to perform this action."

        # Generic error with context
        if context:
            return f"⚠ Error {context}: {error_msg}"

        # Generic error
        return f"⚠ Something went wrong. Please try again."

    @staticmethod
    def format_success(message: str, data: Any = None) -> Dict[str, Any]:
        """
        Format success response.

        Args:
            message: Success message
            data: Optional data to include

        Returns:
            Success response dict
        """
        # Add checkmark if not present
        if not message.startswith("✓"):
            message = f"✓ {message}"

        response = {
            "success": True,
            "message": message,
            "error": None
        }

        if data is not None:
            response["data"] = data

        return response

    @staticmethod
    def format_tool_error(
        tool_name: str,
        error: Exception,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Format tool execution error.

        Args:
            tool_name: Name of the tool that failed
            error: Exception that occurred
            params: Optional tool parameters for context

        Returns:
            Error response dict
        """
        formatted_msg = ErrorFormatter.format_error(
            error,
            context=f"executing {tool_name}"
        )

        return {
            "success": False,
            "error": formatted_msg,
            "tool": tool_name,
            "data": None
        }
