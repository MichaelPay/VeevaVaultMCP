"""
Tests for file staging tools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from veevavault_mcp.tools.file_staging import (
    FileStagingUploadTool,
    FileStagingListTool,
    FileStagingDownloadTool,
    FileStagingDeleteTool,
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


class TestFileStagingUploadTool:
    """Tests for FileStagingUploadTool."""

    @pytest.mark.asyncio
    async def test_upload_file_success(self, mock_auth_manager, mock_http_client):
        """Test file upload to staging."""
        tool = FileStagingUploadTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(file_path="/path/to/file.pdf", file_name="file.pdf")

        assert result.success
        assert "endpoint" in result.data
        assert result.data["file_name"] == "file.pdf"

    @pytest.mark.asyncio
    async def test_upload_file_default_name(self, mock_auth_manager, mock_http_client):
        """Test file upload with default file name."""
        tool = FileStagingUploadTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(file_path="/path/to/document.pdf")

        assert result.success
        assert result.data["file_name"] == "document.pdf"


class TestFileStagingListTool:
    """Tests for FileStagingListTool."""

    @pytest.mark.asyncio
    async def test_list_files_success(self, mock_auth_manager, mock_http_client):
        """Test listing staged files."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"name": "file1.pdf", "size": 1024},
                    {"name": "file2.pdf", "size": 2048},
                ],
            }
        )

        tool = FileStagingListTool(mock_auth_manager, mock_http_client)
        result = await tool.execute()

        assert result.success
        assert result.data["count"] == 2
        assert len(result.data["files"]) == 2

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/services/file_staging" in call_args.kwargs["path"]

    @pytest.mark.asyncio
    async def test_list_files_with_folder(self, mock_auth_manager, mock_http_client):
        """Test listing files in specific folder."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [],
            }
        )

        tool = FileStagingListTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(folder="my_folder")

        assert result.success
        assert result.data["folder"] == "my_folder"

        # Verify folder parameter was passed
        call_args = mock_http_client.get.call_args
        assert call_args.kwargs["params"]["folder"] == "my_folder"


class TestFileStagingDownloadTool:
    """Tests for FileStagingDownloadTool."""

    @pytest.mark.asyncio
    async def test_download_file_success(self, mock_auth_manager, mock_http_client):
        """Test downloading file from staging."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "file": "test.pdf",
            }
        )

        tool = FileStagingDownloadTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(staging_path="u123/test.pdf")

        assert result.success
        assert result.data["staging_path"] == "u123/test.pdf"
        assert "download_url" in result.data

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/services/file_staging/u123/test.pdf" in call_args.kwargs["path"]


class TestFileStagingDeleteTool:
    """Tests for FileStagingDeleteTool."""

    @pytest.mark.asyncio
    async def test_delete_file_success(self, mock_auth_manager, mock_http_client):
        """Test deleting file from staging."""
        mock_http_client.delete = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
            }
        )

        tool = FileStagingDeleteTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(staging_path="u123/test.pdf")

        assert result.success
        assert result.data["staging_path"] == "u123/test.pdf"
        assert "deleted" in result.data["message"].lower()

        # Verify correct endpoint and method
        call_args = mock_http_client.delete.call_args
        assert "/services/file_staging/u123/test.pdf" in call_args.kwargs["path"]
