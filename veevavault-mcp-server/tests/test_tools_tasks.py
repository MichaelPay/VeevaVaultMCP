"""
Tests for task management tools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from veevavault_mcp.tools.tasks import (
    TasksListTool,
    TasksGetTool,
    TasksExecuteActionTool,
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


class TestTasksListTool:
    """Tests for TasksListTool."""

    @pytest.mark.asyncio
    async def test_list_tasks_success(self, mock_auth_manager, mock_http_client):
        """Test listing tasks."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"id": "T001", "task_type__v": "review", "status__v": "open__v"},
                    {"id": "T002", "task_type__v": "approve", "status__v": "open__v"},
                ],
            }
        )

        tool = TasksListTool(mock_auth_manager, mock_http_client)
        result = await tool.execute()

        assert result.success
        assert result.data["count"] == 2
        assert result.data["status_filter"] == "open"

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/objects/tasks" in call_args.kwargs["path"]
        assert call_args.kwargs["params"]["status__v"] == "open__v"

    @pytest.mark.asyncio
    async def test_list_completed_tasks(self, mock_auth_manager, mock_http_client):
        """Test listing completed tasks."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [],
            }
        )

        tool = TasksListTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(status="completed", limit=50)

        assert result.success

        # Verify parameters
        call_args = mock_http_client.get.call_args
        assert call_args.kwargs["params"]["status__v"] == "completed__v"
        assert call_args.kwargs["params"]["limit"] == 50

    @pytest.mark.asyncio
    async def test_list_all_tasks(self, mock_auth_manager, mock_http_client):
        """Test listing all tasks regardless of status."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [],
            }
        )

        tool = TasksListTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(status="all")

        assert result.success

        # Verify no status filter when status='all'
        call_args = mock_http_client.get.call_args
        assert "status__v" not in call_args.kwargs["params"]


class TestTasksGetTool:
    """Tests for TasksGetTool."""

    @pytest.mark.asyncio
    async def test_get_task_success(self, mock_auth_manager, mock_http_client):
        """Test getting task details."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": {
                    "id": "T001",
                    "task_type__v": "review",
                    "status__v": "open__v",
                    "due_date__v": "2025-11-15",
                },
            }
        )

        tool = TasksGetTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(task_id="T001")

        assert result.success
        assert result.data["task_id"] == "T001"
        assert result.data["status"] == "open__v"
        assert result.data["due_date"] == "2025-11-15"

        # Verify correct endpoint
        call_args = mock_http_client.get.call_args
        assert "/objects/tasks/T001" in call_args.kwargs["path"]


class TestTasksExecuteActionTool:
    """Tests for TasksExecuteActionTool."""

    @pytest.mark.asyncio
    async def test_complete_task_success(self, mock_auth_manager, mock_http_client):
        """Test completing a task."""
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "id": "T001",
            }
        )

        tool = TasksExecuteActionTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            task_id="T001",
            action="complete",
            verdict="approved",
            comment="Looks good",
        )

        assert result.success
        assert result.data["task_id"] == "T001"
        assert result.data["action"] == "complete"
        assert result.data["verdict"] == "approved"

        # Verify correct endpoint and data
        call_args = mock_http_client.post.call_args
        assert "/objects/tasks/T001/actions/complete" in call_args.kwargs["path"]
        assert call_args.kwargs["json"]["verdict__v"] == "approved"
        assert call_args.kwargs["json"]["comment__v"] == "Looks good"

    @pytest.mark.asyncio
    async def test_reassign_task_success(self, mock_auth_manager, mock_http_client):
        """Test reassigning a task."""
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "id": "T001",
            }
        )

        tool = TasksExecuteActionTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            task_id="T001",
            action="reassign",
            assignee_id=456,
            comment="Reassigning to specialist",
        )

        assert result.success

        # Verify assignee was included
        call_args = mock_http_client.post.call_args
        assert call_args.kwargs["json"]["assignee__v"] == 456

    @pytest.mark.asyncio
    async def test_task_action_without_optional_params(self, mock_auth_manager, mock_http_client):
        """Test task action with minimal parameters."""
        mock_http_client.post = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "id": "T001",
            }
        )

        tool = TasksExecuteActionTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(task_id="T001", action="cancel")

        assert result.success

        # Verify empty dict was sent
        call_args = mock_http_client.post.call_args
        assert call_args.kwargs["json"] == {}
