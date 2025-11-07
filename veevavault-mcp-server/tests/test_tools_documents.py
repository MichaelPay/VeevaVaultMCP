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
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"id": 1, "name__v": "Test Document 1"},
                    {"id": 2, "name__v": "Test Document 2"},
                ],
                "responseDetails": {"total": 2},
                "total": 2,
                "pagesize": 100,
            }
        )

        tool = DocumentsQueryTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(vql="SELECT id, name__v FROM documents")

        assert result.success
        assert result.data["count"] == 2
        assert len(result.data["documents"]) == 2
        assert result.data["total"] == 2
        assert "pagination" in result.data

        # Verify POST was used with form data
        call_args = mock_http_client.post.call_args
        assert "SELECT id, name__v FROM documents" in call_args.kwargs["data"]["q"]
        assert call_args.kwargs["headers"]["Content-Type"] == "application/x-www-form-urlencoded"

    @pytest.mark.asyncio
    async def test_query_with_filters(self, mock_auth_manager, mock_http_client):
        """Test query with filter-based parameters."""
        mock_http_client.post = AsyncMock(
            return_value={"data": [], "responseDetails": {}, "total": 0, "pagesize": 50}
        )

        tool = DocumentsQueryTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            name_contains="protocol",
            document_type="protocol__c",
            status="steady_state__c",
            limit=50,
        )

        assert result.success

        # Verify query was built from filters using POST
        call_args = mock_http_client.post.call_args
        query = call_args.kwargs["data"]["q"]
        assert "name__v CONTAINS" in query
        assert "type__v =" in query
        assert "status__v =" in query
        assert "LIMIT 50" in query

    @pytest.mark.asyncio
    async def test_query_empty_results(self, mock_auth_manager, mock_http_client):
        """Test query with no results."""
        mock_http_client.post = AsyncMock(
            return_value={"data": [], "responseDetails": {}, "total": 0, "pagesize": 100}
        )

        tool = DocumentsQueryTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(name_contains="nonexistent")

        assert result.success
        assert result.data["count"] == 0
        assert result.data["documents"] == []
        assert result.data["total"] == 0


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
        assert "/documents/123" in call_args.kwargs["path"]

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
        assert "/documents/123/versions/1/0" in call_args.kwargs["path"]


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
        assert "/documents/123" in call_args.kwargs["path"]


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
        assert "/documents/123/lock" in call_args.kwargs["path"]


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
        assert "/documents/123/lock" in call_args.kwargs["path"]


class TestDocumentsDownloadFileTool:
    """Tests for DocumentsDownloadFileTool."""

    @pytest.mark.asyncio
    async def test_download_file_success(self, mock_auth_manager, mock_http_client):
        """Test downloading document file."""
        from veevavault_mcp.tools.documents import DocumentsDownloadFileTool
        
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "file": "test.pdf",
                "url": "https://vault.example.com/files/test.pdf",
            }
        )

        tool = DocumentsDownloadFileTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123)

        assert result.success
        assert result.data["document_id"] == 123
        assert "download_url" in result.data
        assert "response" in result.data
        assert result.data["response"]["url"] == "https://vault.example.com/files/test.pdf"

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/documents/123/file" in call_args.kwargs["path"]


class TestDocumentsDownloadVersionFileTool:
    """Tests for DocumentsDownloadVersionFileTool."""

    @pytest.mark.asyncio
    async def test_download_version_file_success(self, mock_auth_manager, mock_http_client):
        """Test downloading specific version file."""
        from veevavault_mcp.tools.documents import DocumentsDownloadVersionFileTool
        
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "file": "test_v1.0.pdf",
                "url": "https://vault.example.com/files/test_v1.0.pdf",
            }
        )

        tool = DocumentsDownloadVersionFileTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123, major_version=1, minor_version=0)

        assert result.success
        assert result.data["document_id"] == 123
        assert result.data["version"] == "1.0"
        assert "download_url" in result.data
        assert "response" in result.data

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/documents/123/versions/1/0/file" in call_args.kwargs["path"]


class TestDocumentsBatchCreateTool:
    """Tests for DocumentsBatchCreateTool."""

    @pytest.mark.asyncio
    async def test_batch_create_success(self, mock_auth_manager, mock_http_client):
        """Test batch create with all successes."""
        from veevavault_mcp.tools.documents import DocumentsBatchCreateTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"responseStatus": "SUCCESS", "id": 1},
                    {"responseStatus": "SUCCESS", "id": 2},
                ],
            }
        )

        tool = DocumentsBatchCreateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            documents=[
                {"name": "Doc1", "type": "protocol__c", "lifecycle": "base__v", "title": "Title1"},
                {"name": "Doc2", "type": "protocol__c", "lifecycle": "base__v", "title": "Title2"},
            ]
        )

        assert result.success
        assert result.data["total"] == 2
        assert result.data["successes"] == 2
        assert result.data["failures"] == 0

    @pytest.mark.asyncio
    async def test_batch_create_partial_success(self, mock_auth_manager, mock_http_client):
        """Test batch create with partial success."""
        from veevavault_mcp.tools.documents import DocumentsBatchCreateTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"responseStatus": "SUCCESS", "id": 1},
                    {"responseStatus": "FAILURE", "errors": [{"message": "Invalid type"}]},
                ],
            }
        )

        tool = DocumentsBatchCreateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            documents=[
                {"name": "Doc1", "type": "protocol__c", "lifecycle": "base__v", "title": "Title1"},
                {"name": "Doc2", "type": "invalid__c", "lifecycle": "base__v", "title": "Title2"},
            ]
        )

        assert not result.success
        assert result.data["total"] == 2
        assert result.data["successes"] == 1
        assert result.data["failures"] == 1


class TestDocumentsBatchUpdateTool:
    """Tests for DocumentsBatchUpdateTool."""

    @pytest.mark.asyncio
    async def test_batch_update_success(self, mock_auth_manager, mock_http_client):
        """Test batch update with all successes."""
        from veevavault_mcp.tools.documents import DocumentsBatchUpdateTool
        
        mock_http_client.put = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"responseStatus": "SUCCESS", "id": 1},
                    {"responseStatus": "SUCCESS", "id": 2},
                ],
            }
        )

        tool = DocumentsBatchUpdateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            updates=[
                {"id": 1, "title__v": "Updated Title 1"},
                {"id": 2, "title__v": "Updated Title 2"},
            ]
        )

        assert result.success
        assert result.data["total"] == 2
        assert result.data["successes"] == 2
        assert result.data["failures"] == 0


class TestDocumentsGetActionsTool:
    """Tests for DocumentsGetActionsTool."""

    @pytest.mark.asyncio
    async def test_get_actions_success(self, mock_auth_manager, mock_http_client):
        """Test getting document actions."""
        from veevavault_mcp.tools.documents import DocumentsGetActionsTool
        
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "lifecycle_actions__v": [
                    {"name": "Approve", "label": "Approve Document"},
                    {"name": "Reject", "label": "Reject Document"},
                ],
            }
        )

        tool = DocumentsGetActionsTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123)

        assert result.success
        assert result.data["document_id"] == 123
        assert result.data["count"] == 2
        assert len(result.data["actions"]) == 2

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/documents/123/actions" in call_args.kwargs["path"]


class TestDocumentsExecuteActionTool:
    """Tests for DocumentsExecuteActionTool."""

    @pytest.mark.asyncio
    async def test_execute_action_success(self, mock_auth_manager, mock_http_client):
        """Test executing document action."""
        from veevavault_mcp.tools.documents import DocumentsExecuteActionTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "id": 123,
            }
        )

        tool = DocumentsExecuteActionTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            document_id=123,
            action_name="Approve",
            action_data={"comment": "Looks good"},
        )

        assert result.success
        assert result.data["document_id"] == 123
        assert result.data["action_name"] == "Approve"

        # Verify correct endpoint
        call_args = mock_http_client.post.call_args
        assert "/documents/123/actions/Approve" in call_args.kwargs["path"]


class TestDocumentsUploadFileTool:
    """Tests for DocumentsUploadFileTool."""

    @pytest.mark.asyncio
    async def test_upload_file_with_staging(self, mock_auth_manager, mock_http_client):
        """Test document creation with staged file."""
        from veevavault_mcp.tools.documents import DocumentsUploadFileTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "id": 123,
            }
        )

        tool = DocumentsUploadFileTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            name="Test Document",
            type="protocol__c",
            lifecycle="base__v",
            title="Test Title",
            staging_path="u123/test.pdf",
        )

        assert result.success
        assert result.data["document_id"] == 123
        assert result.data["name"] == "Test Document"

        # Verify staging path was included
        call_args = mock_http_client.post.call_args
        assert call_args.kwargs["json"]["file"] == "u123/test.pdf"

    @pytest.mark.asyncio
    async def test_upload_file_with_metadata(self, mock_auth_manager, mock_http_client):
        """Test document upload with additional metadata."""
        from veevavault_mcp.tools.documents import DocumentsUploadFileTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "id": 456,
            }
        )

        tool = DocumentsUploadFileTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            name="Protocol",
            type="protocol__c",
            lifecycle="base__v",
            title="Clinical Protocol",
            staging_path="u123/protocol.pdf",
            metadata={"study_id": "STUDY-001", "version": "1.0"},
        )

        assert result.success

        # Verify metadata fields were included with __v suffix
        call_args = mock_http_client.post.call_args
        assert call_args.kwargs["json"]["study_id__v"] == "STUDY-001"
        assert call_args.kwargs["json"]["version__v"] == "1.0"


class TestDocumentsCreateVersionTool:
    """Tests for DocumentsCreateVersionTool."""

    @pytest.mark.asyncio
    async def test_create_version_success(self, mock_auth_manager, mock_http_client):
        """Test creating new document version."""
        from veevavault_mcp.tools.documents import DocumentsCreateVersionTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": {
                    "version": "2.0",
                    "major_version_number__v": 2,
                    "minor_version_number__v": 0,
                },
            }
        )

        tool = DocumentsCreateVersionTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            document_id=123,
            staging_path="u123/version2.pdf",
        )

        assert result.success
        assert result.data["document_id"] == 123
        assert result.data["version"] == "2.0"
        assert result.data["major_version"] == 2
        assert result.data["minor_version"] == 0

        # Verify correct endpoint
        call_args = mock_http_client.post.call_args
        assert "/documents/123/versions" in call_args.kwargs["path"]
        assert call_args.kwargs["json"]["file"] == "u123/version2.pdf"

    @pytest.mark.asyncio
    async def test_create_version_with_metadata(self, mock_auth_manager, mock_http_client):
        """Test creating version with metadata updates."""
        from veevavault_mcp.tools.documents import DocumentsCreateVersionTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": {
                    "version": "1.1",
                    "major_version_number__v": 1,
                    "minor_version_number__v": 1,
                },
            }
        )

        tool = DocumentsCreateVersionTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            document_id=456,
            metadata={"status": "draft", "reason__c": "Updated content"},
        )

        assert result.success

        # Verify metadata was included
        call_args = mock_http_client.post.call_args
        assert call_args.kwargs["json"]["status__v"] == "draft"
        assert call_args.kwargs["json"]["reason__c"] == "Updated content"


class TestDocumentsAttachmentsListTool:
    """Tests for DocumentsAttachmentsListTool."""

    @pytest.mark.asyncio
    async def test_list_attachments_success(self, mock_auth_manager, mock_http_client):
        """Test listing document attachments."""
        from veevavault_mcp.tools.documents import DocumentsAttachmentsListTool
        
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"id": "A001", "file_name__v": "data.xlsx", "size__v": 1024},
                    {"id": "A002", "file_name__v": "notes.pdf", "size__v": 2048},
                ],
            }
        )

        tool = DocumentsAttachmentsListTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123)

        assert result.success
        assert result.data["document_id"] == 123
        assert result.data["count"] == 2

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/objects/documents/123/attachments" in call_args.kwargs["path"]


class TestDocumentsAttachmentsUploadTool:
    """Tests for DocumentsAttachmentsUploadTool."""

    @pytest.mark.asyncio
    async def test_upload_attachment_success(self, mock_auth_manager, mock_http_client):
        """Test uploading document attachment."""
        from veevavault_mcp.tools.documents import DocumentsAttachmentsUploadTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "id": "A003",
            }
        )

        tool = DocumentsAttachmentsUploadTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            document_id=123,
            staging_path="u456/data.xlsx",
            description="Supporting data",
        )

        assert result.success
        assert result.data["attachment_id"] == "A003"

        # Verify correct data was sent
        call_args = mock_http_client.post.call_args
        assert call_args.kwargs["json"]["file"] == "u456/data.xlsx"
        assert call_args.kwargs["json"]["description__v"] == "Supporting data"


class TestDocumentsAttachmentsDownloadTool:
    """Tests for DocumentsAttachmentsDownloadTool."""

    @pytest.mark.asyncio
    async def test_download_attachment_success(self, mock_auth_manager, mock_http_client):
        """Test downloading document attachment."""
        from veevavault_mcp.tools.documents import DocumentsAttachmentsDownloadTool
        
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "file": "data.xlsx",
            }
        )

        tool = DocumentsAttachmentsDownloadTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123, attachment_id="A001")

        assert result.success
        assert result.data["attachment_id"] == "A001"
        assert "download_url" in result.data

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/objects/documents/123/attachments/A001" in call_args.kwargs["path"]


class TestDocumentsAttachmentsDeleteTool:
    """Tests for DocumentsAttachmentsDeleteTool."""

    @pytest.mark.asyncio
    async def test_delete_attachment_success(self, mock_auth_manager, mock_http_client):
        """Test deleting document attachment."""
        from veevavault_mcp.tools.documents import DocumentsAttachmentsDeleteTool
        
        mock_http_client.delete = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
            }
        )

        tool = DocumentsAttachmentsDeleteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123, attachment_id="A001")

        assert result.success
        assert "deleted" in result.data["message"].lower()

        # Verify correct endpoint and method
        call_args = mock_http_client.delete.call_args
        assert "/objects/documents/123/attachments/A001" in call_args.kwargs["path"]


class TestDocumentsRenditionsListTool:
    """Tests for DocumentsRenditionsListTool."""

    @pytest.mark.asyncio
    async def test_list_renditions_success(self, mock_auth_manager, mock_http_client):
        """Test listing document renditions."""
        from veevavault_mcp.tools.documents import DocumentsRenditionsListTool
        
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "renditions": [
                    {"type": "pdf", "status": "ready"},
                    {"type": "thumbnail", "status": "ready"},
                ],
            }
        )

        tool = DocumentsRenditionsListTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123)

        assert result.success
        assert result.data["document_id"] == 123
        assert result.data["count"] == 2

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/objects/documents/123/renditions" in call_args.kwargs["path"]

    @pytest.mark.asyncio
    async def test_list_renditions_for_version(self, mock_auth_manager, mock_http_client):
        """Test listing renditions for specific version."""
        from veevavault_mcp.tools.documents import DocumentsRenditionsListTool
        
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "renditions": [],
            }
        )

        tool = DocumentsRenditionsListTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123, doc_version="1.0")

        assert result.success
        assert result.data["doc_version"] == "1.0"

        # Verify version in path
        call_args = mock_http_client.get.call_args
        assert "/versions/1.0/renditions" in call_args.kwargs["path"]


class TestDocumentsRenditionsGenerateTool:
    """Tests for DocumentsRenditionsGenerateTool."""

    @pytest.mark.asyncio
    async def test_generate_rendition_success(self, mock_auth_manager, mock_http_client):
        """Test generating document rendition."""
        from veevavault_mcp.tools.documents import DocumentsRenditionsGenerateTool
        
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "job_id": "JOB123",
            }
        )

        tool = DocumentsRenditionsGenerateTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123, rendition_type="pdf")

        assert result.success
        assert result.data["rendition_type"] == "pdf"
        assert result.data["job_id"] == "JOB123"

        # Verify correct endpoint
        call_args = mock_http_client.post.call_args
        assert "/objects/documents/123/renditions/pdf" in call_args.kwargs["path"]


class TestDocumentsRenditionsDownloadTool:
    """Tests for DocumentsRenditionsDownloadTool."""

    @pytest.mark.asyncio
    async def test_download_rendition_success(self, mock_auth_manager, mock_http_client):
        """Test downloading document rendition."""
        from veevavault_mcp.tools.documents import DocumentsRenditionsDownloadTool
        
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "file": "document.pdf",
            }
        )

        tool = DocumentsRenditionsDownloadTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123, rendition_type="pdf")

        assert result.success
        assert result.data["rendition_type"] == "pdf"
        assert "download_url" in result.data

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/objects/documents/123/renditions/pdf/file" in call_args.kwargs["path"]


class TestDocumentsRenditionsDeleteTool:
    """Tests for DocumentsRenditionsDeleteTool."""

    @pytest.mark.asyncio
    async def test_delete_rendition_success(self, mock_auth_manager, mock_http_client):
        """Test deleting document rendition."""
        from veevavault_mcp.tools.documents import DocumentsRenditionsDeleteTool
        
        mock_http_client.delete = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
            }
        )

        tool = DocumentsRenditionsDeleteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123, rendition_type="pdf")

        assert result.success
        assert "deleted" in result.data["message"].lower()

        # Verify correct endpoint and method
        call_args = mock_http_client.delete.call_args
        assert "/objects/documents/123/renditions/pdf" in call_args.kwargs["path"]
