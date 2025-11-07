"""
Tests for workflow management tools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from veevavault_mcp.tools.workflows import (
    WorkflowsListTool,
    WorkflowsGetTool,
    DocumentsGetWorkflowDetailsTool,
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


class TestWorkflowsListTool:
    """Tests for WorkflowsListTool."""

    @pytest.mark.asyncio
    async def test_list_workflows_success(self, mock_auth_manager, mock_http_client):
        """Test listing workflows."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"id": "wf1", "name__v": "Document Review", "status__v": "active__v"},
                    {"id": "wf2", "name__v": "Change Control", "status__v": "active__v"},
                ],
            }
        )

        tool = WorkflowsListTool(mock_auth_manager, mock_http_client)
        result = await tool.execute()

        assert result.success
        assert result.data["count"] == 2
        assert len(result.data["workflows"]) == 2

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/objects/workflows" in call_args.kwargs["path"]

    @pytest.mark.asyncio
    async def test_list_workflows_with_filters(self, mock_auth_manager, mock_http_client):
        """Test listing workflows with filters."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [],
            }
        )

        tool = WorkflowsListTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(workflow_type="atomic", active_only=True)

        assert result.success

        # Verify parameters were passed
        call_args = mock_http_client.get.call_args
        assert call_args.kwargs["params"]["type"] == "atomic"
        assert call_args.kwargs["params"]["status"] == "active__v"


class TestWorkflowsGetTool:
    """Tests for WorkflowsGetTool."""

    @pytest.mark.asyncio
    async def test_get_workflow_success(self, mock_auth_manager, mock_http_client):
        """Test getting workflow details."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": {
                    "id": "doc_workflow__c",
                    "name__v": "Document Review",
                    "states": ["draft", "review", "approved"],
                },
            }
        )

        tool = WorkflowsGetTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(workflow_id="doc_workflow__c")

        assert result.success
        assert result.data["workflow_id"] == "doc_workflow__c"
        assert "workflow" in result.data

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/objects/workflows/doc_workflow__c" in call_args.kwargs["path"]


class TestDocumentsGetWorkflowDetailsTool:
    """Tests for DocumentsGetWorkflowDetailsTool."""

    @pytest.mark.asyncio
    async def test_get_document_workflow_success(self, mock_auth_manager, mock_http_client):
        """Test getting document workflow details."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": {
                    "state__v": "review_state__c",
                    "workflow__v": "doc_workflow__c",
                    "available_actions": ["approve", "reject"],
                },
            }
        )

        tool = DocumentsGetWorkflowDetailsTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(document_id=123)

        assert result.success
        assert result.data["document_id"] == 123
        assert result.data["current_state"] == "review_state__c"
        assert len(result.data["available_actions"]) == 2

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/objects/documents/123/workflow" in call_args.kwargs["path"]
