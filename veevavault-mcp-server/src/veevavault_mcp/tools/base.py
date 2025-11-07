"""
Base tool class for all VeevaVault MCP tools.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from dataclasses import dataclass
from datetime import datetime
import structlog

from ..auth.manager import AuthenticationManager
from ..utils.http import VaultHTTPClient
from ..utils.errors import ValidationError

logger = structlog.get_logger(__name__)


@dataclass
class ToolResult:
    """
    Result from a tool execution.

    Attributes:
        success: Whether the tool executed successfully
        data: Result data from the tool
        error: Error message if unsuccessful
        metadata: Additional metadata about the execution
    """

    success: bool
    data: Any = None
    error: Optional[str] = None
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> dict:
        """Convert result to dictionary."""
        result = {
            "success": self.success,
            "data": self.data,
            "metadata": self.metadata,
        }
        if self.error:
            result["error"] = self.error
        return result


class BaseTool(ABC):
    """
    Abstract base class for all VeevaVault MCP tools.

    Provides common functionality:
    - Authentication management
    - HTTP client access
    - Parameter validation
    - Error handling
    - Structured logging
    """

    # API version for Veeva Vault
    API_VERSION = "v25.2"

    def __init__(
        self,
        auth_manager: AuthenticationManager,
        http_client: VaultHTTPClient,
    ):
        """
        Initialize tool.

        Args:
            auth_manager: Authentication manager for session handling
            http_client: HTTP client for API requests
        """
        self.auth_manager = auth_manager
        self.http_client = http_client
        self.logger = logger.bind(tool=self.__class__.__name__)

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name for MCP registration."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for LLM."""
        pass

    @abstractmethod
    def get_parameters_schema(self) -> dict:
        """
        Get JSON schema for tool parameters.

        Returns:
            JSON schema dict for parameter validation
        """
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool with given parameters.

        Args:
            **kwargs: Tool-specific parameters

        Returns:
            ToolResult with execution outcome

        Raises:
            ValidationError: If parameters are invalid
        """
        pass

    async def run(self, **kwargs) -> ToolResult:
        """
        Run the tool with error handling and logging.

        This is the main entry point that wraps execute() with
        common functionality.

        Args:
            **kwargs: Tool parameters

        Returns:
            ToolResult with execution outcome
        """
        start_time = datetime.utcnow()

        self.logger.info(
            "tool_starting",
            tool=self.name,
            params=self._sanitize_params(kwargs),
        )

        try:
            # Validate parameters
            self._validate_parameters(kwargs)

            # Execute the tool
            result = await self.execute(**kwargs)

            # Log success
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.logger.info(
                "tool_completed",
                tool=self.name,
                duration_seconds=duration,
                success=result.success,
            )

            # Add duration to metadata
            if result.metadata is None:
                result.metadata = {}
            result.metadata["duration_seconds"] = duration

            return result

        except ValidationError as e:
            self.logger.warning(
                "tool_validation_error",
                tool=self.name,
                error=str(e),
            )
            return ToolResult(
                success=False,
                error=f"Validation error: {str(e)}",
                metadata={"error_type": "validation"},
            )

        except Exception as e:
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.logger.error(
                "tool_failed",
                tool=self.name,
                error=str(e),
                error_type=type(e).__name__,
                duration_seconds=duration,
            )
            return ToolResult(
                success=False,
                error=f"{type(e).__name__}: {str(e)}",
                metadata={
                    "error_type": type(e).__name__,
                    "duration_seconds": duration,
                },
            )

    def _validate_parameters(self, params: dict) -> None:
        """
        Validate parameters against schema.

        Args:
            params: Parameters to validate

        Raises:
            ValidationError: If validation fails
        """
        schema = self.get_parameters_schema()
        properties = schema.get("properties", {})
        required = schema.get("required", [])

        # Check required parameters
        for param in required:
            if param not in params or params[param] is None:
                raise ValidationError(
                    message=f"Missing required parameter: {param}",
                    context={"parameter": param, "tool": self.name},
                )

        # Validate each provided parameter
        for param_name, param_value in params.items():
            if param_name not in properties:
                continue  # Allow extra params for flexibility

            param_schema = properties[param_name]
            param_type = param_schema.get("type")

            # Skip None values for optional parameters
            if param_value is None:
                continue

            # Type validation
            if param_type == "integer":
                if not isinstance(param_value, int) or isinstance(param_value, bool):
                    raise ValidationError(
                        message=f"Parameter '{param_name}' must be an integer, got {type(param_value).__name__}",
                        context={"parameter": param_name, "value": param_value},
                    )

                # Range validation
                if "minimum" in param_schema and param_value < param_schema["minimum"]:
                    raise ValidationError(
                        message=f"Parameter '{param_name}' must be >= {param_schema['minimum']}, got {param_value}",
                        context={"parameter": param_name, "value": param_value},
                    )

                if "maximum" in param_schema and param_value > param_schema["maximum"]:
                    raise ValidationError(
                        message=f"Parameter '{param_name}' must be <= {param_schema['maximum']}, got {param_value}",
                        context={"parameter": param_name, "value": param_value},
                    )

            elif param_type == "string":
                if not isinstance(param_value, str):
                    raise ValidationError(
                        message=f"Parameter '{param_name}' must be a string, got {type(param_value).__name__}",
                        context={"parameter": param_name, "value": param_value},
                    )

                # Minimum length validation
                if "minLength" in param_schema and len(param_value) < param_schema["minLength"]:
                    raise ValidationError(
                        message=f"Parameter '{param_name}' must be at least {param_schema['minLength']} characters",
                        context={"parameter": param_name},
                    )

                # Enum validation
                if "enum" in param_schema and param_value not in param_schema["enum"]:
                    raise ValidationError(
                        message=f"Parameter '{param_name}' must be one of {param_schema['enum']}, got '{param_value}'",
                        context={"parameter": param_name, "value": param_value},
                    )

            elif param_type == "boolean":
                if not isinstance(param_value, bool):
                    raise ValidationError(
                        message=f"Parameter '{param_name}' must be a boolean, got {type(param_value).__name__}",
                        context={"parameter": param_name, "value": param_value},
                    )

            elif param_type == "array":
                if not isinstance(param_value, list):
                    raise ValidationError(
                        message=f"Parameter '{param_name}' must be an array, got {type(param_value).__name__}",
                        context={"parameter": param_name},
                    )

    def _sanitize_params(self, params: dict) -> dict:
        """
        Sanitize parameters for logging (remove sensitive data).

        Args:
            params: Parameters to sanitize

        Returns:
            Sanitized parameters dict
        """
        sanitized = params.copy()

        # Remove common sensitive fields
        sensitive_fields = {"password", "token", "secret", "api_key"}
        for field in sensitive_fields:
            if field in sanitized:
                sanitized[field] = "***REDACTED***"

        return sanitized

    async def _get_auth_headers(self) -> dict[str, str]:
        """
        Get authentication headers for API requests.

        Returns:
            Dict of HTTP headers with auth token
        """
        session = await self.auth_manager.get_session()
        return self.auth_manager.get_auth_headers(session)

    def _build_api_path(self, endpoint: str) -> str:
        """
        Build full API path from endpoint.

        Args:
            endpoint: API endpoint (e.g., /objects/users)

        Returns:
            Full API path with version
        """
        endpoint = endpoint.lstrip("/")
        return f"/api/{self.API_VERSION}/{endpoint}"
