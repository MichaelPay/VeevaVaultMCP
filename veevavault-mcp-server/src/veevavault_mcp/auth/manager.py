"""
Base authentication manager for VeevaVault MCP Server.
"""

from abc import ABC, abstractmethod
from typing import Optional
import structlog

from .models import VaultSession
from ..config import Config

logger = structlog.get_logger(__name__)


class AuthenticationManager(ABC):
    """
    Abstract base class for authentication managers.

    Handles authentication with Veeva Vault and session management.
    Subclasses implement specific authentication modes (username/password, OAuth2).
    """

    def __init__(self, config: Config):
        """
        Initialize authentication manager.

        Args:
            config: Server configuration
        """
        self.config = config
        self._current_session: Optional[VaultSession] = None
        self.logger = logger.bind(auth_mode=config.auth_mode.value)

    @abstractmethod
    async def authenticate(self) -> VaultSession:
        """
        Authenticate with Veeva Vault and create a new session.

        Returns:
            VaultSession object with session details

        Raises:
            AuthenticationError: If authentication fails
        """
        pass

    @abstractmethod
    async def refresh_session(self) -> VaultSession:
        """
        Refresh the current session.

        Returns:
            Refreshed VaultSession object

        Raises:
            AuthenticationError: If refresh fails
        """
        pass

    async def get_session(self) -> VaultSession:
        """
        Get current session, creating or refreshing as needed.

        Returns:
            Valid VaultSession object

        Raises:
            AuthenticationError: If authentication fails
        """
        # No session exists - create new one
        if self._current_session is None:
            self.logger.info("no_session_exists", action="creating_new")
            self._current_session = await self.authenticate()
            return self._current_session

        # Session expired - create new one
        if self._current_session.is_expired():
            self.logger.info("session_expired", action="creating_new")
            self._current_session = await self.authenticate()
            return self._current_session

        # Session should be refreshed - refresh it
        if self._current_session.should_refresh():
            self.logger.info("session_near_expiry", action="refreshing")
            try:
                self._current_session = await self.refresh_session()
            except Exception as e:
                # Refresh failed - create new session
                self.logger.warning(
                    "session_refresh_failed",
                    error=str(e),
                    action="creating_new"
                )
                self._current_session = await self.authenticate()
            return self._current_session

        # Session is valid
        return self._current_session

    def get_auth_headers(self, session: Optional[VaultSession] = None) -> dict[str, str]:
        """
        Get HTTP headers for authenticated requests.

        Args:
            session: VaultSession to use (uses current session if None)

        Returns:
            Dictionary of HTTP headers
        """
        if session is None:
            session = self._current_session

        if session is None:
            return {}

        return {
            "Authorization": session.session_id,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def invalidate_session(self) -> None:
        """Invalidate the current session."""
        self.logger.info("session_invalidated")
        self._current_session = None

    def is_authenticated(self) -> bool:
        """
        Check if there is a valid session.

        Returns:
            True if authenticated with valid session
        """
        if self._current_session is None:
            return False

        return not self._current_session.is_expired()

    def get_current_session(self) -> Optional[VaultSession]:
        """
        Get the current session without creating/refreshing.

        Returns:
            Current VaultSession or None
        """
        return self._current_session
