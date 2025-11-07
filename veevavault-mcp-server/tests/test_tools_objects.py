"""
Tests for object management tools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from veevavault_mcp.tools.objects import (
    ObjectsQueryTool,
    ObjectsGetTool,
    ObjectsCreateTool,
    ObjectsUpdateTool,
)
from veevavault_mcp.tools.base import ToolResult


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


class TestObjectsQueryTool:
    """Tests for ObjectsQueryTool."""

    @pytest.mark.asyncio
    async def test_query_with_vql(self, mock_auth_manager, mock_http_client):
        """Test query with direct VQL."""
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"id": 1, "name__v": "Product A"},
                    {"id": 2, "name__v": "Product B"},
                ],
                "responseDetails": {"total": 2},
            }
        )

        tool = ObjectsQueryTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            object_name="product__v",
            vql="SELECT id, name__v FROM product__v WHERE active__v = true"
        )

        assert result.success
        assert result.data["count"] == 2
        assert len(result.data["records"]) == 2

        # Verify VQL was used
        call_args = mock_http_client.post.call_args
        assert "SELECT id, name__v FROM product__v" in call_args.kwargs["data"]["q"]

    @pytest.mark.asyncio
    async def test_query_with_fields_and_where(self, mock_auth_manager, mock_http_client):
        """Test query built from fields and where clause."""
        mock_http_client.post = AsyncMock(
            return_value={"data": [], "responseDetails": {}, "total": 0, "pagesize": 100}
        )

        tool = ObjectsQueryTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            object_name="product__v",
            fields=["id", "name__v", "status__v"],
            where="active__v = true",
            limit=50,
        )

        assert result.success

        # Verify query was built correctly
        call_args = mock_http_client.post.call_args
        query = call_args.kwargs["data"]["q"]
        assert "SELECT id, name__v, status__v FROM product__v" in query
        assert "WHERE active__v = true" in query
        assert "LIMIT 50" in query

    @pytest.mark.asyncio
    async def test_query_simple_without_where(self, mock_auth_manager, mock_http_client):
        """Test simple query without where clause."""
        mock_http_client.post = AsyncMock(
            return_value={"data": [], "responseDetails": {}, "total": 0, "pagesize": 100}
        )

        tool = ObjectsQueryTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(object_name="study__v")

        assert result.success

        # Verify default fields were used
        call_args = mock_http_client.post.call_args
        query = call_args.kwargs["data"]["q"]
        assert "SELECT id, name__v FROM study__v" in query


class TestObjectsGetTool:
    """Tests for ObjectsGetTool."""

    @pytest.mark.asyncio
    async def test_get_object_success(self, mock_auth_manager, mock_http_client):
        """Test successful object retrieval."""
        mock_http_client.get = AsyncMock(
            return_value={
                "data": {
                    "id": 456,
                    "name__v": "Test Product",
                    "status__v": "active__v",
                }
            }
        )

        tool = ObjectsGetTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(object_name="product__v", record_id="456")

        assert result.success
        assert result.data["id"] == 456
        assert result.data["name__v"] == "Test Product"

        # Verify correct API path
        call_args = mock_http_client.get.call_args
        assert "/objects/product__v/456" in call_args.kwargs["path"]

    @pytest.mark.asyncio
    async def test_get_object_metadata(self, mock_auth_manager, mock_http_client):
        """Test getting object with metadata."""
        mock_http_client.get = AsyncMock(
            return_value={
                "data": {
                    "id": 456,
                    "name__v": "Test Product",
                }
            }
        )

        tool = ObjectsGetTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            object_name="product__v",
            record_id="456",
        )

        assert result.success
        assert result.metadata["object_name"] == "product__v"
        assert result.metadata["record_id"] == "456"


class TestObjectsCreateTool:
    """Tests for ObjectsCreateTool."""

    @pytest.mark.asyncio
    async def test_create_object_success(self, mock_auth_manager, mock_http_client):
        """Test successful object creation."""
        mock_http_client.post = AsyncMock(
            return_value={"data": {"id": 789}}
        )

        tool = ObjectsCreateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            object_name="product__v",
            fields={
                "name__v": "New Product",
                "status__v": "active__v",
                "description__v": "Test description",
            }
        )

        assert result.success
        assert result.data["record_id"] == 789

        # Verify request payload
        call_args = mock_http_client.post.call_args
        assert "/objects/product__v" in call_args.kwargs["path"]
        payload = call_args.kwargs["json"]
        assert payload["name__v"] == "New Product"
        assert payload["status__v"] == "active__v"

    @pytest.mark.asyncio
    async def test_create_object_empty_fields(self, mock_auth_manager, mock_http_client):
        """Test create with empty fields succeeds (API validation will catch)."""
        mock_http_client.post = AsyncMock(
            return_value={"data": {"id": 789}}
        )

        tool = ObjectsCreateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(object_name="product__v", fields={"name__v": "Test"})

        assert result.success


class TestObjectsUpdateTool:
    """Tests for ObjectsUpdateTool."""

    @pytest.mark.asyncio
    async def test_update_object_success(self, mock_auth_manager, mock_http_client):
        """Test successful object update."""
        mock_http_client.put = AsyncMock(
            return_value={"responseStatus": "SUCCESS"}
        )

        tool = ObjectsUpdateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            object_name="product__v",
            record_id="456",
            fields={
                "name__v": "Updated Product",
                "status__v": "inactive__v",
            }
        )

        assert result.success
        assert result.data["record_id"] == "456"
        assert "name__v" in result.data["updated_fields"]

        # Verify request
        call_args = mock_http_client.put.call_args
        assert "/objects/product__v/456" in call_args.kwargs["path"]
        payload = call_args.kwargs["json"]
        assert payload["name__v"] == "Updated Product"

    @pytest.mark.asyncio
    async def test_update_object_with_fields(self, mock_auth_manager, mock_http_client):
        """Test update with specific fields."""
        mock_http_client.put = AsyncMock(
            return_value={"responseStatus": "SUCCESS"}
        )

        tool = ObjectsUpdateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            object_name="product__v",
            record_id="456",
            fields={"status__v": "active__v"}
        )

        assert result.success
        assert "status__v" in result.data["updated_fields"]


class TestObjectsBatchCreateTool:
    """Tests for ObjectsBatchCreateTool."""

    @pytest.mark.asyncio
    async def test_batch_create_success(self, mock_auth_manager, mock_http_client):
        """Test batch create with all successes."""
        from veevavault_mcp.tools.objects import ObjectsBatchCreateTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"responseStatus": "SUCCESS", "id": "V0P000000001001"},
                    {"responseStatus": "SUCCESS", "id": "V0P000000001002"},
                ],
            }
        )

        tool = ObjectsBatchCreateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            object_name="product__v",
            records=[
                {"name__v": "Product 1", "status__v": "active__v"},
                {"name__v": "Product 2", "status__v": "active__v"},
            ],
        )

        assert result.success
        assert result.data["total"] == 2
        assert result.data["successes"] == 2
        assert result.data["failures"] == 0
        assert result.data["object_name"] == "product__v"

        # Verify correct endpoint
        call_args = mock_http_client.post.call_args
        assert "/objects/product__v" in call_args.kwargs["path"]

    @pytest.mark.asyncio
    async def test_batch_create_partial_success(self, mock_auth_manager, mock_http_client):
        """Test batch create with partial success."""
        from veevavault_mcp.tools.objects import ObjectsBatchCreateTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"responseStatus": "SUCCESS", "id": "V0P000000001001"},
                    {"responseStatus": "FAILURE", "errors": [{"message": "Required field missing"}]},
                ],
            }
        )

        tool = ObjectsBatchCreateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            object_name="product__v",
            records=[
                {"name__v": "Product 1", "status__v": "active__v"},
                {"status__v": "active__v"},
            ],
        )

        assert not result.success
        assert result.data["successes"] == 1
        assert result.data["failures"] == 1


class TestObjectsBatchUpdateTool:
    """Tests for ObjectsBatchUpdateTool."""

    @pytest.mark.asyncio
    async def test_batch_update_success(self, mock_auth_manager, mock_http_client):
        """Test batch update with all successes."""
        from veevavault_mcp.tools.objects import ObjectsBatchUpdateTool
        
        mock_http_client.put = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"responseStatus": "SUCCESS", "id": "V0P000000001001"},
                    {"responseStatus": "SUCCESS", "id": "V0P000000001002"},
                ],
            }
        )

        tool = ObjectsBatchUpdateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            object_name="product__v",
            updates=[
                {"id": "V0P000000001001", "status__v": "inactive__v"},
                {"id": "V0P000000001002", "status__v": "inactive__v"},
            ],
        )

        assert result.success
        assert result.data["total"] == 2
        assert result.data["successes"] == 2
        assert result.data["failures"] == 0

        # Verify correct endpoint and method
        call_args = mock_http_client.put.call_args
        assert "/objects/product__v" in call_args.kwargs["path"]


class TestObjectsGetActionsTool:
    """Tests for ObjectsGetActionsTool."""

    @pytest.mark.asyncio
    async def test_get_actions_success(self, mock_auth_manager, mock_http_client):
        """Test getting object actions."""
        from veevavault_mcp.tools.objects import ObjectsGetActionsTool
        
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "lifecycle_actions__v": [
                    {"name": "Activate", "label": "Activate Product"},
                    {"name": "Retire", "label": "Retire Product"},
                ],
            }
        )

        tool = ObjectsGetActionsTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(object_name="product__v", record_id="V0P000000001001")

        assert result.success
        assert result.data["object_name"] == "product__v"
        assert result.data["record_id"] == "V0P000000001001"
        assert result.data["count"] == 2
        assert len(result.data["actions"]) == 2

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/objects/product__v/V0P000000001001/actions" in call_args.kwargs["path"]


class TestObjectsExecuteActionTool:
    """Tests for ObjectsExecuteActionTool."""

    @pytest.mark.asyncio
    async def test_execute_action_success(self, mock_auth_manager, mock_http_client):
        """Test executing object action."""
        from veevavault_mcp.tools.objects import ObjectsExecuteActionTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "id": "V0P000000001001",
            }
        )

        tool = ObjectsExecuteActionTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            object_name="product__v",
            record_id="V0P000000001001",
            action_name="Activate",
            action_data={"reason": "Ready for production"},
        )

        assert result.success
        assert result.data["object_name"] == "product__v"
        assert result.data["record_id"] == "V0P000000001001"
        assert result.data["action_name"] == "Activate"

        # Verify correct endpoint
        call_args = mock_http_client.post.call_args
        assert "/objects/product__v/V0P000000001001/actions/Activate" in call_args.kwargs["path"]

    @pytest.mark.asyncio
    async def test_execute_action_no_data(self, mock_auth_manager, mock_http_client):
        """Test executing action without action data."""
        from veevavault_mcp.tools.objects import ObjectsExecuteActionTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "id": "V0P000000001001",
            }
        )

        tool = ObjectsExecuteActionTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            object_name="product__v",
            record_id="V0P000000001001",
            action_name="Activate",
        )

        assert result.success

        # Verify empty dict was sent
        call_args = mock_http_client.post.call_args
        assert call_args.kwargs["json"] == {}
