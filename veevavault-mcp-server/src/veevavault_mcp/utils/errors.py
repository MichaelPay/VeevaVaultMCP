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
