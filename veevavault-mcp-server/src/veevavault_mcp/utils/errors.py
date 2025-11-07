"""
Exception hierarchy for VeevaVault MCP Server.

All custom exceptions inherit from VeevaVaultError base class.
Provides structured error handling with error codes and context.
"""

from typing import Any, Optional


class VeevaVaultError(Exception):
    """Base exception for all VeevaVault MCP errors."""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        """
        Initialize VeevaVault error.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code (e.g., "INVALID_CREDENTIALS")
            context: Additional context about the error
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__.upper()
        self.context = context or {}

    def __str__(self) -> str:
        """String representation of error."""
        base = f"[{self.error_code}] {self.message}"
        if self.context:
            base += f" | Context: {self.context}"
        return base

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary for structured logging."""
        return {
            "error": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "context": self.context,
        }


class AuthenticationError(VeevaVaultError):
    """Raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication failed",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "AUTHENTICATION_FAILED",
            context=context,
        )


class AuthorizationError(VeevaVaultError):
    """Raised when user lacks permissions for an operation."""

    def __init__(
        self,
        message: str = "Insufficient permissions",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "INSUFFICIENT_PERMISSIONS",
            context=context,
        )


class ValidationError(VeevaVaultError):
    """Raised when request validation fails."""

    def __init__(
        self,
        message: str = "Validation failed",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "VALIDATION_FAILED",
            context=context,
        )


class NotFoundError(VeevaVaultError):
    """Raised when requested resource does not exist."""

    def __init__(
        self,
        message: str = "Resource not found",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "RESOURCE_NOT_FOUND",
            context=context,
        )


class RateLimitError(VeevaVaultError):
    """Raised when API rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
        retry_after: Optional[int] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "RATE_LIMIT_EXCEEDED",
            context=context,
        )
        self.retry_after = retry_after  # Seconds until retry allowed


class APIError(VeevaVaultError):
    """Raised when Veeva Vault API returns an error."""

    def __init__(
        self,
        message: str = "API request failed",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
        status_code: Optional[int] = None,
        response_data: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "API_ERROR",
            context=context,
        )
        self.status_code = status_code
        self.response_data = response_data or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary including API response."""
        base = super().to_dict()
        base["status_code"] = self.status_code
        base["response_data"] = self.response_data
        return base


class ConfigurationError(VeevaVaultError):
    """Raised when configuration is invalid or missing."""

    def __init__(
        self,
        message: str = "Configuration error",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "CONFIGURATION_ERROR",
            context=context,
        )


class CacheError(VeevaVaultError):
    """Raised when cache operation fails."""

    def __init__(
        self,
        message: str = "Cache operation failed",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "CACHE_ERROR",
            context=context,
        )


class TimeoutError(VeevaVaultError):
    """Raised when operation times out."""

    def __init__(
        self,
        message: str = "Operation timed out",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "TIMEOUT",
            context=context,
        )


class QuerySyntaxError(VeevaVaultError):
    """Raised when VQL query has syntax errors."""

    def __init__(
        self,
        message: str = "Query syntax error",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "MALFORMED_URL",
            context=context,
        )


class FieldNotFoundError(VeevaVaultError):
    """Raised when referenced field does not exist."""

    def __init__(
        self,
        message: str = "Field not found",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "ATTRIBUTE_NOT_SUPPORTED",
            context=context,
        )


class StateError(VeevaVaultError):
    """Raised when operation not allowed in current state."""

    def __init__(
        self,
        message: str = "Operation not allowed in current state",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "OPERATION_NOT_ALLOWED",
            context=context,
        )


class SessionExpiredError(VeevaVaultError):
    """Raised when session has expired."""

    def __init__(
        self,
        message: str = "Session expired",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "SESSION_EXPIRED",
            context=context,
        )


class NetworkError(VeevaVaultError):
    """Raised when network operation fails."""

    def __init__(
        self,
        message: str = "Network operation failed",
        error_code: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            error_code=error_code or "NETWORK_ERROR",
            context=context,
        )


# Map Vault API error codes to specific exception classes
ERROR_CODE_MAP = {
    # Authentication errors
    "INVALID_SESSION_ID": SessionExpiredError,
    "NO_PERMISSION": AuthorizationError,
    "INSUFFICIENT_ACCESS": AuthorizationError,
    # Query errors
    "MALFORMED_URL": QuerySyntaxError,
    "INVALID_QUERY": QuerySyntaxError,
    # Field errors
    "ATTRIBUTE_NOT_SUPPORTED": FieldNotFoundError,
    "INVALID_FIELD": FieldNotFoundError,
    # State errors
    "OPERATION_NOT_ALLOWED": StateError,
    "INVALID_DOCUMENT_STATE": StateError,
    "INVALID_OBJECT_STATE": StateError,
    # Validation errors
    "INVALID_DATA": ValidationError,
    "PARAMETER_REQUIRED": ValidationError,
    "METHOD_NOT_SUPPORTED": ValidationError,
    # Rate limiting
    "API_LIMIT_EXCEED": RateLimitError,
    "RATE_LIMIT_EXCEEDED": RateLimitError,
}


def create_error_from_response(
    response_data: dict[str, Any],
    status_code: Optional[int] = None,
    default_message: str = "API request failed",
) -> VeevaVaultError:
    """
    Create appropriate exception from Vault API error response.

    Args:
        response_data: API response dictionary
        status_code: HTTP status code
        default_message: Default error message if none in response

    Returns:
        Appropriate VeevaVaultError subclass instance
    """
    # Extract error information
    error_type = response_data.get("responseStatus")
    error_message = response_data.get("responseMessage", default_message)
    
    # Get first error from errors array if present
    errors = response_data.get("errors", [])
    if errors and isinstance(errors, list) and len(errors) > 0:
        first_error = errors[0]
        error_type = first_error.get("type", error_type)
        error_message = first_error.get("message", error_message)

    # Map to specific exception class
    exception_class = ERROR_CODE_MAP.get(error_type, APIError)

    # Create context
    context = {
        "response_status": response_data.get("responseStatus"),
        "status_code": status_code,
    }
    if errors:
        context["errors"] = errors

    # Handle rate limiting specially to extract retry_after
    if exception_class == RateLimitError:
        retry_after = response_data.get("retry_after")
        return exception_class(
            message=error_message,
            error_code=error_type,
            context=context,
            retry_after=retry_after,
        )

    # Handle API errors specially to include response data
    if exception_class == APIError:
        return exception_class(
            message=error_message,
            error_code=error_type,
            context=context,
            status_code=status_code,
            response_data=response_data,
        )

    # Create specific error type
    return exception_class(
        message=error_message,
        error_code=error_type,
        context=context,
    )
