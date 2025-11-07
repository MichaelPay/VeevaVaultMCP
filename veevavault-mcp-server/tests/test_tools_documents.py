"""
Tests for document management tools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from veevavault_mcp.tools.documents import (
    DocumentsQueryTool,
    DocumentsGetTool,
    DocumentsCreateTool,
    DocumentsUpdateTool,
    DocumentsDeleteTool,
    DocumentsLockTool,
    DocumentsUnlockTool,
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


class TestDocumentsQueryTool:
    """Tests for DocumentsQueryTool."""

    @pytest.mark.asyncio
    async def test_query_with_vql(self, mock_auth_manager, mock_http_client):
        """Test query with direct VQL."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"id": 1, "name__v": "Test Document 1"},
                    {"id": 2, "name__v": "Test Document 2"},
                ],
                "responseDetails": {"total": 2},
            }
        )

        tool = DocumentsQueryTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(vql="SELECT id, name__v FROM documents")

        assert result.success
        assert result.data["count"] == 2
        assert len(result.data["documents"]) == 2

        # Verify VQL was used directly
        call_args = mock_http_client.get.call_args
        assert "SELECT id, name__v FROM documents" in call_args.kwargs["params"]["q"]

    @pytest.mark.asyncio
    async def test_query_with_filters(self, mock_auth_manager, mock_http_client):
        """Test query with filter-based parameters."""
        mock_http_client.get = AsyncMock(
            return_value={"data": [], "responseDetails": {}}
        )

        tool = DocumentsQueryTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            name_contains="protocol",
            document_type="protocol__c",
            status="steady_state__c",
            limit=50,
        )

        assert result.success

        # Verify query was built from filters
        call_args = mock_http_client.get.call_args
        query = call_args.kwargs["params"]["q"]
        assert "name__v CONTAINS" in query
        assert "type__v =" in query
        assert "status__v =" in query
        assert "LIMIT 50" in query

    @pytest.mark.asyncio
    async def test_query_empty_results(self, mock_auth_manager, mock_http_client):
        """Test query with no results."""
        mock_http_client.get = AsyncMock(
            return_value={"data": [], "responseDetails": {}}
        )

        tool = DocumentsQueryTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(name_contains="nonexistent")

        assert result.success
        assert result.data["count"] == 0
        assert result.data["documents"] == []


class TestDocumentsGetTool:
    """Tests for DocumentsGetTool."""

    @pytest.mark.asyncio
    async def test_get_document_latest(self, mock_auth_manager, mock_http_client):
        """Test getting latest version of a document."""
        mock_http_client.get = AsyncMock(
            return_value={
                "data": {
                    "id": 123,
                    "name__v": "Test Document",
                    "status__v": "draft__c",
                    "version__v": "0.1",
                }
            }
        )

        tool = DocumentsGetTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123)

        assert result.success
        assert result.data["id"] == 123
        assert result.data["name__v"] == "Test Document"

        # Verify correct API path
        call_args = mock_http_client.get.call_args
        assert "/objects/documents/123" in call_args.kwargs["path"]

    @pytest.mark.asyncio
    async def test_get_document_specific_version(self, mock_auth_manager, mock_http_client):
        """Test getting specific version of a document."""
        mock_http_client.get = AsyncMock(
            return_value={
                "data": {
                    "id": 123,
                    "name__v": "Test Document",
                    "version__v": "1.0",
                }
            }
        )

        tool = DocumentsGetTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123, major_version=1, minor_version=0)

        assert result.success
        assert result.metadata["version_requested"] == "1.0"

        # Verify version-specific path
        call_args = mock_http_client.get.call_args
        assert "/objects/documents/123/versions/1/0" in call_args.kwargs["path"]


class TestDocumentsCreateTool:
    """Tests for DocumentsCreateTool."""

    @pytest.mark.asyncio
    async def test_create_document_success(self, mock_auth_manager, mock_http_client):
        """Test successful document creation."""
        mock_http_client.post = AsyncMock(
            return_value={"data": {"id": 999}}
        )

        tool = DocumentsCreateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            name="New Test Document",
            type="protocol__c",
            lifecycle="general_lifecycle__c",
            title="Test Document Title",
        )

        assert result.success
        assert result.data["document_id"] == 999

        # Verify request payload
        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]
        assert payload["name__v"] == "New Test Document"
        assert payload["type__v"] == "protocol__c"
        assert payload["lifecycle__v"] == "general_lifecycle__c"
        assert payload["title__v"] == "Test Document Title"

    @pytest.mark.asyncio
    async def test_create_document_with_optional_fields(self, mock_auth_manager, mock_http_client):
        """Test document creation with optional fields."""
        mock_http_client.post = AsyncMock(
            return_value={"data": {"id": 999}}
        )

        tool = DocumentsCreateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            name="New Document",
            type="protocol__c",
            lifecycle="general_lifecycle__c",
            classification="unclassified__c",
            subtype="investigational_product__c",
            title="Document Title",
        )

        assert result.success

        # Verify optional fields
        payload = mock_http_client.post.call_args.kwargs["json"]
        assert payload["classification__v"] == "unclassified__c"
        assert payload["subtype__v"] == "investigational_product__c"
        assert payload["title__v"] == "Document Title"


class TestDocumentsUpdateTool:
    """Tests for DocumentsUpdateTool."""

    @pytest.mark.asyncio
    async def test_update_document_success(self, mock_auth_manager, mock_http_client):
        """Test successful document update."""
        mock_http_client.put = AsyncMock(
            return_value={"responseStatus": "SUCCESS"}
        )

        tool = DocumentsUpdateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            document_id=123,
            title="Updated Title",
            description="New description",
        )

        assert result.success
        assert result.data["document_id"] == 123
        assert "title__v" in result.data["updated_fields"]

        # Verify only provided fields are in payload
        payload = mock_http_client.put.call_args.kwargs["json"]
        assert payload["title__v"] == "Updated Title"
        assert payload["description__v"] == "New description"

    @pytest.mark.asyncio
    async def test_update_document_no_fields(self, mock_auth_manager, mock_http_client):
        """Test update with no fields fails."""
        tool = DocumentsUpdateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123)

        assert not result.success
        assert "No fields provided" in result.error


class TestDocumentsDeleteTool:
    """Tests for DocumentsDeleteTool."""

    @pytest.mark.asyncio
    async def test_delete_document_success(self, mock_auth_manager, mock_http_client):
        """Test successful document deletion."""
        mock_http_client.delete = AsyncMock(
            return_value={"responseStatus": "SUCCESS"}
        )

        tool = DocumentsDeleteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123)

        assert result.success
        assert result.data["document_id"] == 123
        assert result.data["deleted"] is True

        # Verify correct API path
        call_args = mock_http_client.delete.call_args
        assert "/objects/documents/123" in call_args.kwargs["path"]


class TestDocumentsLockTool:
    """Tests for DocumentsLockTool."""

    @pytest.mark.asyncio
    async def test_lock_document_success(self, mock_auth_manager, mock_http_client):
        """Test successful document lock."""
        mock_http_client.post = AsyncMock(
            return_value={"responseStatus": "SUCCESS"}
        )

        tool = DocumentsLockTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123)

        assert result.success
        assert result.data["locked"] is True

        # Verify correct API path
        call_args = mock_http_client.post.call_args
        assert "/objects/documents/123/lock" in call_args.kwargs["path"]


class TestDocumentsUnlockTool:
    """Tests for DocumentsUnlockTool."""

    @pytest.mark.asyncio
    async def test_unlock_document_success(self, mock_auth_manager, mock_http_client):
        """Test successful document unlock."""
        mock_http_client.delete = AsyncMock(
            return_value={"responseStatus": "SUCCESS"}
        )

        tool = DocumentsUnlockTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123)

        assert result.success
        assert result.data["unlocked"] is True

        # Verify correct API path
        call_args = mock_http_client.delete.call_args
        assert "/objects/documents/123/lock" in call_args.kwargs["path"]
