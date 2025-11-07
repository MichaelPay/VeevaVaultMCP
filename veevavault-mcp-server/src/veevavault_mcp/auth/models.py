"""
Data models for authentication.
"""

from datetime import datetime, timedelta
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class VaultSession:
    """
    Represents an authenticated Veeva Vault session.

    Attributes:
        session_id: Vault session ID token
        user_id: Authenticated user's ID
        vault_id: Vault instance ID
        vault_name: Vault instance name
        created_at: When the session was created
        expires_at: When the session expires (None if no expiry)
        metadata: Additional session metadata
    """

    session_id: str
    user_id: int
    vault_id: int
    vault_name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    metadata: dict = field(default_factory=dict)

    def is_expired(self) -> bool:
        """Check if the session has expired."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() >= self.expires_at

    def time_until_expiry(self) -> Optional[timedelta]:
        """Get time remaining until session expires."""
        if self.expires_at is None:
            return None
        remaining = self.expires_at - datetime.utcnow()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)

    def should_refresh(self, threshold_seconds: int = 300) -> bool:
        """
        Check if session should be refreshed.

        Args:
            threshold_seconds: Refresh if expiry is within this many seconds

        Returns:
            True if session should be refreshed
        """
        if self.expires_at is None:
            return False

        time_left = self.time_until_expiry()
        if time_left is None:
            return False

        return time_left.total_seconds() <= threshold_seconds

    def to_dict(self) -> dict:
        """Convert session to dictionary for serialization."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "vault_id": self.vault_id,
            "vault_name": self.vault_name,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VaultSession":
        """Create VaultSession from dictionary."""
        return cls(
            session_id=data["session_id"],
            user_id=data["user_id"],
            vault_id=data["vault_id"],
            vault_name=data["vault_name"],
            created_at=datetime.fromisoformat(data["created_at"]),
            expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
            metadata=data.get("metadata", {}),
        )
