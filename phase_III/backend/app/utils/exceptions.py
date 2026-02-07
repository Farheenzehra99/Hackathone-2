class AuthException(Exception):
    """Base authentication exception"""
    def __init__(self, message: str, code: str = "AUTH_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class UserMismatchException(AuthException):
    """Raised when user ID in token doesn't match URL parameter"""
    def __init__(self, message: str = "User ID in token doesn't match URL parameter"):
        super().__init__(message, "AUTH_USER_MISMATCH")

class ResourceNotFoundException(Exception):
    """Raised when requested resource doesn't exist"""
    def __init__(self, resource_type: str, resource_id: any):
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.code = "RESOURCE_NOT_FOUND"
        super().__init__(f"{resource_type} with ID {resource_id} not found")