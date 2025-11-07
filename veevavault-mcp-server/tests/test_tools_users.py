"""
Tests for user management tools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from veevavault_mcp.tools.users import (
    ListUsersTool,
    GetUserTool,
    CreateUserTool,
    UpdateUserTool,
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


class TestListUsersTool:
    """Tests for ListUsersTool."""

    @pytest.mark.asyncio
    async def test_list_users_success(self, mock_auth_manager, mock_http_client):
        """Test successful user listing."""
        mock_http_client.get = AsyncMock(
            return_value={
                "responseStatus": "SUCCESS",
                "data": [
                    {"id": 1, "user_name__v": "user1@example.com"},
                    {"id": 2, "user_name__v": "user2@example.com"},
                ],
            }
        )

        tool = ListUsersTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(status="active", limit=100)

        assert result.success
        assert result.data["count"] == 2
        assert len(result.data["users"]) == 2
        assert result.data["users"][0]["user_name__v"] == "user1@example.com"

    @pytest.mark.asyncio
    async def test_list_users_with_pagination(self, mock_auth_manager, mock_http_client):
        """Test user listing with pagination."""
        mock_http_client.get = AsyncMock(return_value={"data": []})

        tool = ListUsersTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(status="all", limit=50, offset=100)

        assert result.success
        assert result.data["limit"] == 50
        assert result.data["offset"] == 100

        # Verify parameters were passed correctly
        call_args = mock_http_client.get.call_args
        assert call_args.kwargs["params"]["limit"] == 50
        assert call_args.kwargs["params"]["offset"] == 100


class TestGetUserTool:
    """Tests for GetUserTool."""

    @pytest.mark.asyncio
    async def test_get_user_success(self, mock_auth_manager, mock_http_client):
        """Test successful user retrieval."""
        mock_http_client.get = AsyncMock(
            return_value={
                "data": {
                    "id": 12345,
                    "user_name__v": "test.user@example.com",
                    "user_email__v": "test.user@example.com",
                    "user_first_name__v": "Test",
                    "user_last_name__v": "User",
                }
            }
        )

        tool = GetUserTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(user_id=12345)

        assert result.success
        assert result.data["user_name__v"] == "test.user@example.com"
        assert result.metadata["user_id"] == 12345

        # Verify API path
        call_args = mock_http_client.get.call_args
        assert "/objects/users/12345" in call_args.kwargs["path"]


class TestCreateUserTool:
    """Tests for CreateUserTool."""

    @pytest.mark.asyncio
    async def test_create_user_success(self, mock_auth_manager, mock_http_client):
        """Test successful user creation."""
        mock_http_client.post = AsyncMock(
            return_value={"data": {"id": 999}}
        )

        tool = CreateUserTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            user_name="new.user@example.com",
            user_email="new.user@example.com",
            user_first_name="New",
            user_last_name="User",
            security_profile="document_user__v",
            license_type="full_user__v",
        )

        assert result.success
        assert result.data["user_id"] == 999
        assert result.data["user_name"] == "new.user@example.com"

        # Verify request payload
        call_args = mock_http_client.post.call_args
        payload = call_args.kwargs["json"]
        assert payload["user_name__v"] == "new.user@example.com"
        assert payload["active__v"] is True

    @pytest.mark.asyncio
    async def test_create_user_with_optional_fields(self, mock_auth_manager, mock_http_client):
        """Test user creation with optional fields."""
        mock_http_client.post = AsyncMock(
            return_value={"data": {"id": 999}}
        )

        tool = CreateUserTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            user_name="new.user@example.com",
            user_email="new.user@example.com",
            user_first_name="New",
            user_last_name="User",
            security_profile="document_user__v",
            license_type="full_user__v",
            user_title="Manager",
            group_id=5,
            user_language="en",
        )

        assert result.success

        # Verify optional fields in payload
        payload = mock_http_client.post.call_args.kwargs["json"]
        assert payload["user_title__v"] == "Manager"
        assert payload["group_id__v"] == 5
        assert payload["user_language__v"] == "en"


class TestUpdateUserTool:
    """Tests for UpdateUserTool."""

    @pytest.mark.asyncio
    async def test_update_user_success(self, mock_auth_manager, mock_http_client):
        """Test successful user update."""
        mock_http_client.put = AsyncMock(return_value={"responseStatus": "SUCCESS"})

        tool = UpdateUserTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(
            user_id=12345,
            user_title="Senior Manager",
            active=False,
        )

        assert result.success
        assert result.data["user_id"] == 12345
        assert "user_title__v" in result.data["updated_fields"]

        # Verify only provided fields are in payload
        payload = mock_http_client.put.call_args.kwargs["json"]
        assert payload["user_title__v"] == "Senior Manager"
        assert payload["active__v"] is False
        assert "user_email__v" not in payload  # Not provided

    @pytest.mark.asyncio
    async def test_update_user_no_fields(self, mock_auth_manager, mock_http_client):
        """Test update with no fields fails."""
        tool = UpdateUserTool(mock_auth_manager, mock_http_client)
        result = await tool.execute(user_id=12345)

        assert not result.success
        assert "No fields provided" in result.error
