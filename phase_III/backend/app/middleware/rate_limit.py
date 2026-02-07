"""Rate limiting middleware for chat endpoint."""
import time
from collections import defaultdict
from typing import Dict, Tuple

from fastapi import HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimiter:
    """
    Simple in-memory rate limiter.

    Tracks requests per user with sliding window.
    10 messages per minute per user.
    """

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # Store: {user_id: [(timestamp, request_count)]}
        self.requests: Dict[str, list] = defaultdict(list)

    def is_allowed(self, user_id: str) -> Tuple[bool, int]:
        """
        Check if request is allowed for user.

        Args:
            user_id: User identifier

        Returns:
            Tuple of (is_allowed, retry_after_seconds)
        """
        now = time.time()
        window_start = now - self.window_seconds

        # Clean old requests
        self.requests[user_id] = [
            (ts, count) for ts, count in self.requests[user_id]
            if ts > window_start
        ]

        # Count requests in window
        request_count = sum(count for _, count in self.requests[user_id])

        if request_count >= self.max_requests:
            # Calculate retry after (seconds until oldest request expires)
            if self.requests[user_id]:
                oldest_ts = self.requests[user_id][0][0]
                retry_after = int(oldest_ts + self.window_seconds - now) + 1
                return False, retry_after
            return False, self.window_seconds

        # Add current request
        self.requests[user_id].append((now, 1))
        return True, 0

    def cleanup_old_entries(self):
        """Clean up expired entries to prevent memory bloat."""
        now = time.time()
        window_start = now - self.window_seconds

        # Remove users with no recent requests
        for user_id in list(self.requests.keys()):
            self.requests[user_id] = [
                (ts, count) for ts, count in self.requests[user_id]
                if ts > window_start
            ]
            if not self.requests[user_id]:
                del self.requests[user_id]


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware for FastAPI.

    Only applies to chat endpoints.
    """

    def __init__(self, app, rate_limiter: RateLimiter = None):
        """
        Initialize middleware.

        Args:
            app: FastAPI application
            rate_limiter: Optional rate limiter instance
        """
        super().__init__(app)
        self.rate_limiter = rate_limiter or RateLimiter()

    async def dispatch(self, request: Request, call_next):
        """
        Process request with rate limiting.

        Args:
            request: Incoming request
            call_next: Next middleware/endpoint

        Returns:
            Response

        Raises:
            HTTPException 429 if rate limit exceeded
        """
        # Only apply to chat endpoint
        if not request.url.path.endswith("/chat"):
            return await call_next(request)

        # Extract user_id from path (assumes /api/{user_id}/chat)
        path_parts = request.url.path.split("/")
        if len(path_parts) >= 3 and path_parts[1] == "api":
            user_id = path_parts[2]

            # Check rate limit
            is_allowed, retry_after = self.rate_limiter.is_allowed(user_id)

            if not is_allowed:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"⚠ Too many messages. Please wait {retry_after} seconds.",
                    headers={"Retry-After": str(retry_after)}
                )

        return await call_next(request)


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=10, window_seconds=60)


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance."""
    return rate_limiter
