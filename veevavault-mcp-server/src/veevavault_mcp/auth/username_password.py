"""
Username/password authentication manager for Veeva Vault.
"""

from typing import Optional
from datetime import datetime, timedelta
import structlog

from .manager import AuthenticationManager
from .models import VaultSession
from ..config import Config, AuthMode
from ..utils.errors import AuthenticationError, ConfigurationError
from ..utils.http import VaultHTTPClient

logger = structlog.get_logger(__name__)


class UsernamePasswordAuthManager(AuthenticationManager):
    """
    Authentication manager for username/password mode.

    Uses Veeva Vault username/password authentication to create sessions.
    Sessions are long-lived and don't typically expire.
    """

    # Veeva Vault API version
    API_VERSION = "v25.2"

    def __init__(self, config: Config):
        """
        Initialize username/password authentication manager.

        Args:
            config: Server configuration

        Raises:
            ConfigurationError: If username/password are not configured
        """
        super().__init__(config)

        # Validate configuration
        if config.auth_mode != AuthMode.USERNAME_PASSWORD:
            raise ConfigurationError(
                message=f"Invalid auth_mode for UsernamePasswordAuthManager: {config.auth_mode}",
                context={"expected": "username_password", "actual": config.auth_mode.value},
            )

        if not config.username or not config.password:
            raise ConfigurationError(
                message="Username and password are required for username_password auth mode",
                context={"has_username": bool(config.username), "has_password": bool(config.password)},
            )

        self.username = config.username
        self.password = config.password
        self.vault_url = config.url

        # HTTP client will be created when needed
        self._http_client: Optional[VaultHTTPClient] = None

    async def _get_http_client(self) -> VaultHTTPClient:
        """Get or create HTTP client."""
        if self._http_client is None:
            self._http_client = VaultHTTPClient(
                base_url=self.vault_url,
                timeout=30,
                max_retries=3,
            )
            await self._http_client.__aenter__()
        return self._http_client

    async def authenticate(self) -> VaultSession:
        """
        Authenticate with Veeva Vault using username/password.

        Makes POST request to /api/{version}/auth endpoint.

        Returns:
            VaultSession with session details

        Raises:
            AuthenticationError: If authentication fails
        """
        self.logger.info(
            "authenticating",
            username=self.username,
            vault_url=self.vault_url,
        )

        try:
            http_client = await self._get_http_client()

            # Make authentication request
            auth_data = {
                "username": self.username,
                "password": self.password,
            }

            response = await http_client.post(
                path=f"/api/{self.API_VERSION}/auth",
                json=auth_data,
            )

            # Extract session information
            session_id = response.get("sessionId")
            if not session_id:
                raise AuthenticationError(
                    message="Authentication response missing sessionId",
                    context={"response": response},
                )

            user_id = response.get("userId")
            vault_ids = response.get("vaultIds", [])

            # Get first vault (primary vault)
            if not vault_ids:
                raise AuthenticationError(
                    message="No vaults available for user",
                    context={"user_id": user_id},
                )

            primary_vault = vault_ids[0]
            vault_id = primary_vault.get("id")
            vault_name = primary_vault.get("name", "Unknown")

            # Create session object
            # Note: Veeva Vault sessions don't have explicit expiry
            # They remain valid until explicitly logged out or timeout (usually 24 hours)
            session = VaultSession(
                session_id=session_id,
                user_id=user_id,
                vault_id=vault_id,
                vault_name=vault_name,
                created_at=datetime.utcnow(),
                expires_at=None,  # No explicit expiry
                metadata={
                    "auth_mode": "username_password",
                    "vault_count": len(vault_ids),
                    "all_vaults": [{"id": v.get("id"), "name": v.get("name")} for v in vault_ids],
                },
            )

            self.logger.info(
                "authentication_successful",
                user_id=user_id,
                vault_id=vault_id,
                vault_name=vault_name,
            )

            return session

        except AuthenticationError:
            raise
        except Exception as e:
            self.logger.error(
                "authentication_failed",
                error=str(e),
                error_type=type(e).__name__,
            )
            raise AuthenticationError(
                message=f"Authentication failed: {str(e)}",
                context={"username": self.username, "error_type": type(e).__name__},
            )

    async def refresh_session(self) -> VaultSession:
        """
        Refresh session by creating a new one.

        For username/password mode, we don't have a refresh endpoint,
        so we just re-authenticate.

        Returns:
            New VaultSession

        Raises:
            AuthenticationError: If authentication fails
        """
        self.logger.info("refreshing_session", action="reauthenticating")
        return await self.authenticate()

    async def logout(self) -> None:
        """
        Logout from Veeva Vault.

        Invalidates the current session on the server.
        """
        if self._current_session is None:
            self.logger.info("logout_called_without_session")
            return

        try:
            http_client = await self._get_http_client()

            # Make logout request with session header
            headers = self.get_auth_headers()
            await http_client.post(
                path=f"/api/{self.API_VERSION}/auth",
                headers=headers,
            )

            self.logger.info("logout_successful", user_id=self._current_session.user_id)

        except Exception as e:
            self.logger.warning(
                "logout_failed",
                error=str(e),
                # Continue to invalidate local session even if server logout fails
            )

        finally:
            # Always invalidate local session
            await self.invalidate_session()

    async def close(self) -> None:
        """Close HTTP client and cleanup resources."""
        if self._http_client:
            await self._http_client.__aexit__(None, None, None)
            self._http_client = None

        self.logger.info("auth_manager_closed")
