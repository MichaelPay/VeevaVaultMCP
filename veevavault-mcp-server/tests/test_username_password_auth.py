"""
Tests for username/password authentication manager.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from veevavault_mcp.auth.username_password import UsernamePasswordAuthManager
from veevavault_mcp.auth.models import VaultSession
from veevavault_mcp.config import Config, AuthMode
from veevavault_mcp.utils.errors import AuthenticationError, ConfigurationError


@pytest.fixture
def username_password_config(monkeypatch):
    """Create config for username/password auth."""
    monkeypatch.setenv("VAULT_AUTH_MODE", "username_password")
    monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
    monkeypatch.setenv("VAULT_USERNAME", "test.user@example.com")
    monkeypatch.setenv("VAULT_PASSWORD", "TestPassword123")
    return Config()


@pytest.fixture
def mock_auth_response():
    """Mock successful authentication response from Vault."""
    return {
        "responseStatus": "SUCCESS",
        "sessionId": "test-session-id-12345",
        "userId": 12345,
        "vaultIds": [
            {"id": 1234, "name": "Test Vault"},
            {"id": 5678, "name": "Second Vault"},
        ],
    }


@pytest.fixture
def mock_auth_failure_response():
    """Mock failed authentication response."""
    return {
        "responseStatus": "FAILURE",
        "errors": [
            {
                "type": "INVALID_LOGIN",
                "message": "Invalid username or password",
            }
        ],
    }


class TestUsernamePasswordAuthManager:
    """Tests for UsernamePasswordAuthManager."""

    def test_init_success(self, username_password_config):
        """Test successful initialization."""
        auth_manager = UsernamePasswordAuthManager(username_password_config)

        assert auth_manager.username == "test.user@example.com"
        assert auth_manager.password == "TestPassword123"
        assert auth_manager.vault_url == "https://test-vault.veevavault.com"
        assert auth_manager.config.auth_mode == AuthMode.USERNAME_PASSWORD

    def test_init_wrong_auth_mode(self, monkeypatch):
        """Test initialization fails with wrong auth mode."""
        monkeypatch.setenv("VAULT_AUTH_MODE", "oauth2")
        monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
        monkeypatch.setenv("VAULT_OAUTH2_TOKEN_URL", "https://auth.example.com/token")
        monkeypatch.setenv("VAULT_OAUTH2_JWKS_URL", "https://auth.example.com/jwks")
        monkeypatch.setenv("VAULT_SERVICE_ACCOUNT_USERNAME", "service@example.com")
        monkeypatch.setenv("VAULT_SERVICE_ACCOUNT_PASSWORD", "password")

        config = Config()

        with pytest.raises(ConfigurationError, match="Invalid auth_mode"):
            UsernamePasswordAuthManager(config)

    def test_init_missing_credentials(self, monkeypatch):
        """Test initialization fails without credentials."""
        monkeypatch.setenv("VAULT_AUTH_MODE", "username_password")
        monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
        monkeypatch.setenv("VAULT_USERNAME", "test.user@example.com")
        # Missing password

        config = Config()

        with pytest.raises(ConfigurationError, match="Username and password are required"):
            UsernamePasswordAuthManager(config)

    @pytest.mark.asyncio
    async def test_authenticate_success(self, username_password_config, mock_auth_response):
        """Test successful authentication."""
        auth_manager = UsernamePasswordAuthManager(username_password_config)

        # Mock HTTP client
        with patch("veevavault_mcp.auth.username_password.VaultHTTPClient") as mock_http_class:
            mock_http_instance = AsyncMock()
            mock_http_instance.post = AsyncMock(return_value=mock_auth_response)
            mock_http_instance.__aenter__ = AsyncMock(return_value=mock_http_instance)
            mock_http_class.return_value = mock_http_instance

            # Authenticate
            session = await auth_manager.authenticate()

            # Verify session
            assert isinstance(session, VaultSession)
            assert session.session_id == "test-session-id-12345"
            assert session.user_id == 12345
            assert session.vault_id == 1234
            assert session.vault_name == "Test Vault"
            assert session.expires_at is None  # No expiry for username/password mode
            assert session.metadata["auth_mode"] == "username_password"
            assert session.metadata["vault_count"] == 2

            # Verify HTTP call
            mock_http_instance.post.assert_called_once()
            call_args = mock_http_instance.post.call_args
            assert "/api/v25.2/auth" in call_args.kwargs["path"]
            assert call_args.kwargs["json"]["username"] == "test.user@example.com"
            assert call_args.kwargs["json"]["password"] == "TestPassword123"

    @pytest.mark.asyncio
    async def test_authenticate_failure(self, username_password_config, mock_auth_failure_response):
        """Test authentication failure."""
        auth_manager = UsernamePasswordAuthManager(username_password_config)

        # Mock HTTP client to raise APIError
        with patch("veevavault_mcp.auth.username_password.VaultHTTPClient") as mock_http_class:
            mock_http_instance = AsyncMock()

            # Simulate API error
            from veevavault_mcp.utils.errors import APIError
            mock_http_instance.post = AsyncMock(
                side_effect=APIError(
                    message="Invalid username or password",
                    error_code="INVALID_LOGIN",
                    response_data=mock_auth_failure_response,
                )
            )
            mock_http_instance.__aenter__ = AsyncMock(return_value=mock_http_instance)
            mock_http_class.return_value = mock_http_instance

            # Should raise AuthenticationError
            with pytest.raises(AuthenticationError, match="Authentication failed"):
                await auth_manager.authenticate()

    @pytest.mark.asyncio
    async def test_authenticate_missing_session_id(self, username_password_config):
        """Test authentication with missing session ID in response."""
        auth_manager = UsernamePasswordAuthManager(username_password_config)

        # Mock response without sessionId
        bad_response = {
            "responseStatus": "SUCCESS",
            "userId": 12345,
        }

        with patch("veevavault_mcp.auth.username_password.VaultHTTPClient") as mock_http_class:
            mock_http_instance = AsyncMock()
            mock_http_instance.post = AsyncMock(return_value=bad_response)
            mock_http_instance.__aenter__ = AsyncMock(return_value=mock_http_instance)
            mock_http_class.return_value = mock_http_instance

            with pytest.raises(AuthenticationError, match="missing sessionId"):
                await auth_manager.authenticate()

    @pytest.mark.asyncio
    async def test_authenticate_no_vaults(self, username_password_config):
        """Test authentication with no available vaults."""
        auth_manager = UsernamePasswordAuthManager(username_password_config)

        # Mock response with empty vaultIds
        bad_response = {
            "responseStatus": "SUCCESS",
            "sessionId": "test-session-123",
            "userId": 12345,
            "vaultIds": [],
        }

        with patch("veevavault_mcp.auth.username_password.VaultHTTPClient") as mock_http_class:
            mock_http_instance = AsyncMock()
            mock_http_instance.post = AsyncMock(return_value=bad_response)
            mock_http_instance.__aenter__ = AsyncMock(return_value=mock_http_instance)
            mock_http_class.return_value = mock_http_instance

            with pytest.raises(AuthenticationError, match="No vaults available"):
                await auth_manager.authenticate()

    @pytest.mark.asyncio
    async def test_get_session_creates_new(self, username_password_config, mock_auth_response):
        """Test get_session creates new session when none exists."""
        auth_manager = UsernamePasswordAuthManager(username_password_config)

        with patch("veevavault_mcp.auth.username_password.VaultHTTPClient") as mock_http_class:
            mock_http_instance = AsyncMock()
            mock_http_instance.post = AsyncMock(return_value=mock_auth_response)
            mock_http_instance.__aenter__ = AsyncMock(return_value=mock_http_instance)
            mock_http_class.return_value = mock_http_instance

            # Get session (should create new one)
            session = await auth_manager.get_session()

            assert session is not None
            assert session.session_id == "test-session-id-12345"
            assert auth_manager.is_authenticated()

    @pytest.mark.asyncio
    async def test_get_session_returns_existing(self, username_password_config, mock_auth_response):
        """Test get_session returns existing valid session."""
        auth_manager = UsernamePasswordAuthManager(username_password_config)

        with patch("veevavault_mcp.auth.username_password.VaultHTTPClient") as mock_http_class:
            mock_http_instance = AsyncMock()
            mock_http_instance.post = AsyncMock(return_value=mock_auth_response)
            mock_http_instance.__aenter__ = AsyncMock(return_value=mock_http_instance)
            mock_http_class.return_value = mock_http_instance

            # Create first session
            session1 = await auth_manager.get_session()

            # Get session again - should return same session without new API call
            mock_http_instance.post.reset_mock()
            session2 = await auth_manager.get_session()

            assert session1.session_id == session2.session_id
            # Should not have made another HTTP call
            mock_http_instance.post.assert_not_called()

    @pytest.mark.asyncio
    async def test_refresh_session(self, username_password_config, mock_auth_response):
        """Test refresh_session re-authenticates."""
        auth_manager = UsernamePasswordAuthManager(username_password_config)

        with patch("veevavault_mcp.auth.username_password.VaultHTTPClient") as mock_http_class:
            mock_http_instance = AsyncMock()
            mock_http_instance.post = AsyncMock(return_value=mock_auth_response)
            mock_http_instance.__aenter__ = AsyncMock(return_value=mock_http_instance)
            mock_http_class.return_value = mock_http_instance

            # Refresh session (re-authenticates)
            session = await auth_manager.refresh_session()

            assert session.session_id == "test-session-id-12345"
            mock_http_instance.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_auth_headers(self, username_password_config, mock_auth_response):
        """Test getting authentication headers."""
        auth_manager = UsernamePasswordAuthManager(username_password_config)

        with patch("veevavault_mcp.auth.username_password.VaultHTTPClient") as mock_http_class:
            mock_http_instance = AsyncMock()
            mock_http_instance.post = AsyncMock(return_value=mock_auth_response)
            mock_http_instance.__aenter__ = AsyncMock(return_value=mock_http_instance)
            mock_http_class.return_value = mock_http_instance

            # Authenticate
            session = await auth_manager.get_session()

            # Get headers
            headers = auth_manager.get_auth_headers()

            assert headers["Authorization"] == "test-session-id-12345"
            assert headers["Content-Type"] == "application/json"
            assert headers["Accept"] == "application/json"

    @pytest.mark.asyncio
    async def test_logout(self, username_password_config, mock_auth_response):
        """Test logout invalidates session."""
        auth_manager = UsernamePasswordAuthManager(username_password_config)

        with patch("veevavault_mcp.auth.username_password.VaultHTTPClient") as mock_http_class:
            mock_http_instance = AsyncMock()
            mock_http_instance.post = AsyncMock(return_value=mock_auth_response)
            mock_http_instance.__aenter__ = AsyncMock(return_value=mock_http_instance)
            mock_http_class.return_value = mock_http_instance

            # Authenticate
            await auth_manager.get_session()
            assert auth_manager.is_authenticated()

            # Logout
            await auth_manager.logout()

            # Session should be invalidated
            assert not auth_manager.is_authenticated()
            assert auth_manager.get_current_session() is None

    @pytest.mark.asyncio
    async def test_close(self, username_password_config):
        """Test closing auth manager."""
        auth_manager = UsernamePasswordAuthManager(username_password_config)

        with patch("veevavault_mcp.auth.username_password.VaultHTTPClient") as mock_http_class:
            mock_http_instance = AsyncMock()
            mock_http_instance.__aenter__ = AsyncMock(return_value=mock_http_instance)
            mock_http_instance.__aexit__ = AsyncMock()
            mock_http_class.return_value = mock_http_instance

            # Initialize HTTP client
            await auth_manager._get_http_client()

            # Close
            await auth_manager.close()

            # HTTP client should be closed
            mock_http_instance.__aexit__.assert_called_once()
