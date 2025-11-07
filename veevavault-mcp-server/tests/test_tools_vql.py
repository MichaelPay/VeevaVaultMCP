"""
Tests for VQL execution tools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from veevavault_mcp.tools.vql import (
    VQLExecuteTool,
    VQLValidateTool,
)
from veevavault_mcp.tools.base import ToolResult
from veevavault_mcp.utils.errors import APIError


@pytest.fixture
def mock_auth_manager():
    """Mock authentication manager."""
    auth_manager = AsyncMock()
    auth_manager.get_session = AsyncMock(return_value=MagicMock(session_id="test-session"))
    auth_manager.get_auth_headers = MagicMock(
        return_value={"Authorization": "test-session"}
    )
    return auth_manager


@pytest.fixture
def mock_http_client():
    """Mock HTTP client."""
    return AsyncMock()


class TestVQLExecuteTool:
    """Tests for VQLExecuteTool."""

    @pytest.mark.asyncio
    async def test_execute_vql_success(self, mock_auth_manager, mock_http_client):
        """Test successful VQL execution."""
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"id": 1, "name__v": "Document 1"},
                    {"id": 2, "name__v": "Document 2"},
                    {"id": 3, "name__v": "Document 3"},
                ],
                "responseDetails": {"total": 3},
            }
        )

        tool = VQLExecuteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            query="SELECT id, name__v FROM documents WHERE type__v = 'protocol__c'"
        )

        assert result.success
        assert result.data["count"] == 3
        assert len(result.data["results"]) == 3
        assert result.data["query"] == "SELECT id, name__v FROM documents WHERE type__v = 'protocol__c'"

        # Verify API call
        call_args = mock_http_client.post.call_args
        assert "/query" in call_args.kwargs["path"]
        assert call_args.kwargs["data"]["q"] == "SELECT id, name__v FROM documents WHERE type__v = 'protocol__c'"

    @pytest.mark.asyncio
    async def test_execute_vql_with_limit_override(self, mock_auth_manager, mock_http_client):
        """Test VQL execution with limit override."""
        mock_http_client.post = AsyncMock(
            return_value={"data": [], "responseDetails": {}}
        )

        tool = VQLExecuteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            query="SELECT id FROM documents LIMIT 100",
            limit=50
        )

        assert result.success

        # Verify limit was overridden
        call_args = mock_http_client.post.call_args
        executed_query = call_args.kwargs["data"]["q"]
        assert "LIMIT 50" in executed_query
        assert "LIMIT 100" not in executed_query

    @pytest.mark.asyncio
    async def test_execute_vql_empty_results(self, mock_auth_manager, mock_http_client):
        """Test VQL execution with no results."""
        mock_http_client.post = AsyncMock(
            return_value={"data": [], "responseDetails": {}}
        )

        tool = VQLExecuteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            query="SELECT id FROM documents WHERE 1=0"
        )

        assert result.success
        assert result.data["count"] == 0
        assert result.data["results"] == []

    @pytest.mark.asyncio
    async def test_execute_vql_api_error(self, mock_auth_manager, mock_http_client):
        """Test VQL execution with API error."""
        # Mock an APIError being raised
        async def raise_api_error(*args, **kwargs):
            raise APIError(
                message="Invalid VQL syntax",
                error_code="MALFORMED_URL",
                status_code=400
            )

        mock_http_client.post = AsyncMock(side_effect=raise_api_error)

        tool = VQLExecuteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(query="SELECT invalid syntax")

        assert not result.success
        assert "VQL query failed" in result.error
        assert result.metadata["error_code"] == "MALFORMED_URL"


class TestVQLValidateTool:
    """Tests for VQLValidateTool."""

    @pytest.mark.asyncio
    async def test_validate_vql_success(self, mock_auth_manager, mock_http_client):
        """Test successful VQL validation."""
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [],
                "responseDetails": {},
                "total": 3,
                "pagesize": 100,
            }
        )

        tool = VQLValidateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            query="SELECT id, name__v FROM documents WHERE type__v = 'protocol__c'"
        )

        assert result.success
        assert result.data["valid"] is True
        assert result.data["query"] == "SELECT id, name__v FROM documents WHERE type__v = 'protocol__c'"
        assert result.data["message"] == "Query syntax is valid"

        # Verify validation used LIMIT 0
        call_args = mock_http_client.post.call_args
        executed_query = call_args.kwargs["data"]["q"]
        assert "LIMIT 0" in executed_query

    @pytest.mark.asyncio
    async def test_validate_vql_removes_existing_limit(self, mock_auth_manager, mock_http_client):
        """Test that validation removes existing LIMIT clause."""
        mock_http_client.post = AsyncMock(
            return_value={"responseStatus": "SUCCESS", "data": [], "responseDetails": {}}
        )

        tool = VQLValidateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            query="SELECT id FROM documents LIMIT 100"
        )

        assert result.success

        # Verify original LIMIT was removed and replaced with LIMIT 0
        call_args = mock_http_client.post.call_args
        executed_query = call_args.kwargs["data"]["q"]
        assert "LIMIT 0" in executed_query
        assert "LIMIT 100" not in executed_query

    @pytest.mark.asyncio
    async def test_validate_vql_syntax_error(self, mock_auth_manager, mock_http_client):
        """Test VQL validation with syntax error."""
        # Mock an APIError being raised for invalid syntax
        async def raise_api_error(*args, **kwargs):
            raise APIError(
                message="Invalid field name: invalid_field",
                error_code="MALFORMED_URL",
                status_code=400
            )

        mock_http_client.post = AsyncMock(side_effect=raise_api_error)

        tool = VQLValidateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(query="SELECT invalid_field FROM documents")

        assert not result.success
        assert "Query validation failed" in result.error
        assert result.data["valid"] is False
        assert result.data["query"] == "SELECT invalid_field FROM documents"
        assert "Invalid field name" in result.data["error"]
        assert result.metadata["validation"] == "failed"


class TestVQLExecuteToolEnhancements:
    """Tests for VQL Execute Tool enhancements (Phase 3)."""

    @pytest.mark.asyncio
    async def test_execute_with_describe_query(self, mock_auth_manager, mock_http_client):
        """Test VQL execution with describe_query header."""
        mock_http_client.post = AsyncMock(
            return_value={
                "data": [{"id": 1}],
                "total": 1,
                "pagesize": 100,
                "queryDescribe": {
                    "fields": [{"name": "id", "type": "ID"}],
                    "object": "documents",
                },
            }
        )

        tool = VQLExecuteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            query="SELECT id FROM documents",
            describe_query=True,
        )

        assert result.success
        assert "query_describe" in result.data
        assert result.data["query_describe"]["object"] == "documents"
        assert result.metadata["describe_query"] is True

        # Verify header was sent
        call_args = mock_http_client.post.call_args
        assert call_args.kwargs["headers"]["X-VaultAPI-DescribeQuery"] == "true"

    @pytest.mark.asyncio
    async def test_execute_with_record_properties(self, mock_auth_manager, mock_http_client):
        """Test VQL execution with record_properties header."""
        mock_http_client.post = AsyncMock(
            return_value={
                "data": [{"id": 1}],
                "total": 1,
                "pagesize": 100,
                "recordProperties": {
                    "1": {"editable": True, "locked": False},
                },
            }
        )

        tool = VQLExecuteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            query="SELECT id FROM documents",
            record_properties=True,
        )

        assert result.success
        assert "record_properties" in result.data
        assert "1" in result.data["record_properties"]
        assert result.metadata["record_properties"] is True

        # Verify header was sent
        call_args = mock_http_client.post.call_args
        assert call_args.kwargs["headers"]["X-VaultAPI-RecordProperties"] == "true"

    @pytest.mark.asyncio
    async def test_execute_with_facets(self, mock_auth_manager, mock_http_client):
        """Test VQL execution with facets header."""
        mock_http_client.post = AsyncMock(
            return_value={
                "data": [{"id": 1}],
                "total": 1,
                "pagesize": 100,
                "facets": [
                    {"field": "type__v", "values": [{"value": "protocol__c", "count": 10}]},
                ],
            }
        )

        tool = VQLExecuteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            query="SELECT id FROM documents",
            enable_facets=True,
        )

        assert result.success
        assert "facets" in result.data
        assert len(result.data["facets"]) == 1
        assert result.data["facets"][0]["field"] == "type__v"
        assert result.metadata["enable_facets"] is True

        # Verify header was sent
        call_args = mock_http_client.post.call_args
        assert call_args.kwargs["headers"]["X-VaultAPI-Facets"] == "true"

    @pytest.mark.asyncio
    async def test_execute_with_all_headers(self, mock_auth_manager, mock_http_client):
        """Test VQL execution with all enhancement headers."""
        mock_http_client.post = AsyncMock(
            return_value={
                "data": [{"id": 1}],
                "total": 1,
                "pagesize": 100,
                "queryDescribe": {"fields": []},
                "recordProperties": {},
                "facets": [],
            }
        )

        tool = VQLExecuteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            query="SELECT id FROM documents",
            describe_query=True,
            record_properties=True,
            enable_facets=True,
        )

        assert result.success
        assert "query_describe" in result.data
        assert "record_properties" in result.data
        assert "facets" in result.data

        # Verify all headers were sent
        call_args = mock_http_client.post.call_args
        headers = call_args.kwargs["headers"]
        assert headers["X-VaultAPI-DescribeQuery"] == "true"
        assert headers["X-VaultAPI-RecordProperties"] == "true"
        assert headers["X-VaultAPI-Facets"] == "true"

    @pytest.mark.asyncio
    async def test_execute_without_enhancement_headers(self, mock_auth_manager, mock_http_client):
        """Test VQL execution without enhancement headers (default behavior)."""
        mock_http_client.post = AsyncMock(
            return_value={
                "data": [{"id": 1}],
                "total": 1,
                "pagesize": 100,
            }
        )

        tool = VQLExecuteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(query="SELECT id FROM documents")

        assert result.success
        assert "query_describe" not in result.data
        assert "record_properties" not in result.data
        assert "facets" not in result.data

        # Verify enhancement headers were NOT sent
        call_args = mock_http_client.post.call_args
        headers = call_args.kwargs["headers"]
        assert "X-VaultAPI-DescribeQuery" not in headers
        assert "X-VaultAPI-RecordProperties" not in headers
        assert "X-VaultAPI-Facets" not in headers
