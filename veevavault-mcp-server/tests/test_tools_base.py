"""
Tests for BaseTool class.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from veevavault_mcp.tools.base import BaseTool, ToolResult
from veevavault_mcp.utils.errors import ValidationError


class TestToolResult:
    """Tests for ToolResult dataclass."""

    def test_success_result(self):
        """Test creating a successful result."""
        result = ToolResult(
            success=True,
            data={"key": "value"},
            metadata={"duration": 1.5},
        )

        assert result.success
        assert result.data == {"key": "value"}
        assert result.error is None
        assert result.metadata["duration"] == 1.5

    def test_error_result(self):
        """Test creating an error result."""
        result = ToolResult(
            success=False,
            error="Something went wrong",
            metadata={"error_type": "APIError"},
        )

        assert not result.success
        assert result.error == "Something went wrong"
        assert result.data is None

    def test_to_dict(self):
        """Test converting result to dictionary."""
        result = ToolResult(
            success=True,
            data={"test": "data"},
            metadata={"duration": 2.0},
        )

        result_dict = result.to_dict()

        assert result_dict["success"] is True
        assert result_dict["data"] == {"test": "data"}
        assert result_dict["metadata"]["duration"] == 2.0
        assert "error" not in result_dict  # No error in successful result

    def test_to_dict_with_error(self):
        """Test converting error result to dictionary."""
        result = ToolResult(
            success=False,
            error="Test error",
        )

        result_dict = result.to_dict()

        assert result_dict["success"] is False
        assert result_dict["error"] == "Test error"


class MockTool(BaseTool):
    """Mock tool for testing BaseTool functionality."""

    @property
    def name(self) -> str:
        return "test_tool"

    @property
    def description(self) -> str:
        return "A test tool"

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "required_param": {"type": "string"},
                "optional_param": {"type": "integer"},
            },
            "required": ["required_param"],
        }

    async def execute(self, required_param: str, optional_param: int = 0) -> ToolResult:
        return ToolResult(
            success=True,
            data={"required_param": required_param, "optional_param": optional_param},
        )


class MockFailingTool(BaseTool):
    """Mock tool that raises an exception."""

    @property
    def name(self) -> str:
        return "failing_tool"

    @property
    def description(self) -> str:
        return "A tool that fails"

    def get_parameters_schema(self) -> dict:
        return {"type": "object", "properties": {}, "required": []}

    async def execute(self) -> ToolResult:
        raise ValueError("Test error")


class TestBaseTool:
    """Tests for BaseTool abstract class."""

    @pytest.fixture
    def mock_auth_manager(self):
        """Create mock authentication manager."""
        auth_manager = AsyncMock()
        auth_manager.get_session = AsyncMock(
            return_value=MagicMock(session_id="test-session")
        )
        auth_manager.get_auth_headers = MagicMock(
            return_value={"Authorization": "test-session"}
        )
        return auth_manager

    @pytest.fixture
    def mock_http_client(self):
        """Create mock HTTP client."""
        return AsyncMock()

    @pytest.mark.asyncio
    async def test_run_success(self, mock_auth_manager, mock_http_client):
        """Test successful tool execution via run()."""
        tool = MockTool(mock_auth_manager, mock_http_client)

        result = await tool.run(required_param="test_value", optional_param=42)

        assert result.success
        assert result.data["required_param"] == "test_value"
        assert result.data["optional_param"] == 42
        assert "duration_seconds" in result.metadata

    @pytest.mark.asyncio
    async def test_run_missing_required_param(self, mock_auth_manager, mock_http_client):
        """Test run() with missing required parameter."""
        tool = MockTool(mock_auth_manager, mock_http_client)

        result = await tool.run(optional_param=42)  # Missing required_param

        assert not result.success
        assert "Validation error" in result.error
        assert "required_param" in result.error
        assert result.metadata["error_type"] == "validation"

    @pytest.mark.asyncio
    async def test_run_exception_handling(self, mock_auth_manager, mock_http_client):
        """Test run() handles exceptions from execute()."""
        tool = MockFailingTool(mock_auth_manager, mock_http_client)

        result = await tool.run()

        assert not result.success
        assert "ValueError" in result.error
        assert "Test error" in result.error
        assert result.metadata["error_type"] == "ValueError"
        assert "duration_seconds" in result.metadata

    def test_sanitize_params(self, mock_auth_manager, mock_http_client):
        """Test parameter sanitization for logging."""
        tool = MockTool(mock_auth_manager, mock_http_client)

        params = {
            "username": "test_user",
            "password": "secret123",
            "api_key": "key_12345",
            "data": "normal_data",
        }

        sanitized = tool._sanitize_params(params)

        assert sanitized["username"] == "test_user"
        assert sanitized["password"] == "***REDACTED***"
        assert sanitized["api_key"] == "***REDACTED***"
        assert sanitized["data"] == "normal_data"

    def test_build_api_path(self, mock_auth_manager, mock_http_client):
        """Test API path building."""
        tool = MockTool(mock_auth_manager, mock_http_client)

        # With leading slash
        path1 = tool._build_api_path("/objects/documents")
        assert path1 == "/api/v25.2/objects/documents"

        # Without leading slash
        path2 = tool._build_api_path("objects/documents")
        assert path2 == "/api/v25.2/objects/documents"

    @pytest.mark.asyncio
    async def test_get_auth_headers(self, mock_auth_manager, mock_http_client):
        """Test authentication header retrieval."""
        tool = MockTool(mock_auth_manager, mock_http_client)

        headers = await tool._get_auth_headers()

        assert headers["Authorization"] == "test-session"
        mock_auth_manager.get_session.assert_called_once()
