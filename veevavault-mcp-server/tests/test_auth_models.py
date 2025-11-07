"""
Tests for authentication models.
"""

import pytest
from datetime import datetime, timedelta

from veevavault_mcp.auth.models import VaultSession


class TestVaultSession:
    """Tests for VaultSession model."""

    def test_session_creation(self):
        """Test creating a VaultSession."""
        session = VaultSession(
            session_id="test-session-123",
            user_id=12345,
            vault_id=5678,
            vault_name="Test Vault",
        )

        assert session.session_id == "test-session-123"
        assert session.user_id == 12345
        assert session.vault_id == 5678
        assert session.vault_name == "Test Vault"
        assert session.created_at is not None
        assert session.expires_at is None
        assert session.metadata == {}

    def test_session_with_expiry(self):
        """Test session with expiration time."""
        expires_at = datetime.utcnow() + timedelta(hours=1)
        session = VaultSession(
            session_id="test-session-123",
            user_id=12345,
            vault_id=5678,
            vault_name="Test Vault",
            expires_at=expires_at,
        )

        assert not session.is_expired()
        assert session.time_until_expiry().total_seconds() > 3500  # ~1 hour

    def test_session_expired(self):
        """Test checking if session is expired."""
        # Create session that expired 1 hour ago
        expires_at = datetime.utcnow() - timedelta(hours=1)
        session = VaultSession(
            session_id="test-session-123",
            user_id=12345,
            vault_id=5678,
            vault_name="Test Vault",
            expires_at=expires_at,
        )

        assert session.is_expired()
        assert session.time_until_expiry() == timedelta(0)

    def test_session_no_expiry(self):
        """Test session without expiration."""
        session = VaultSession(
            session_id="test-session-123",
            user_id=12345,
            vault_id=5678,
            vault_name="Test Vault",
            expires_at=None,
        )

        assert not session.is_expired()
        assert session.time_until_expiry() is None
        assert not session.should_refresh()

    def test_session_should_refresh(self):
        """Test checking if session should be refreshed."""
        # Session expires in 2 minutes
        expires_at = datetime.utcnow() + timedelta(minutes=2)
        session = VaultSession(
            session_id="test-session-123",
            user_id=12345,
            vault_id=5678,
            vault_name="Test Vault",
            expires_at=expires_at,
        )

        # Should refresh if threshold is 5 minutes (300 seconds)
        assert session.should_refresh(threshold_seconds=300)
        # Should not refresh if threshold is 1 minute (60 seconds)
        assert not session.should_refresh(threshold_seconds=60)

    def test_session_to_dict(self):
        """Test converting session to dictionary."""
        created_at = datetime.utcnow()
        expires_at = created_at + timedelta(hours=1)

        session = VaultSession(
            session_id="test-session-123",
            user_id=12345,
            vault_id=5678,
            vault_name="Test Vault",
            created_at=created_at,
            expires_at=expires_at,
            metadata={"key": "value"},
        )

        session_dict = session.to_dict()

        assert session_dict["session_id"] == "test-session-123"
        assert session_dict["user_id"] == 12345
        assert session_dict["vault_id"] == 5678
        assert session_dict["vault_name"] == "Test Vault"
        assert session_dict["created_at"] == created_at.isoformat()
        assert session_dict["expires_at"] == expires_at.isoformat()
        assert session_dict["metadata"] == {"key": "value"}

    def test_session_from_dict(self):
        """Test creating session from dictionary."""
        created_at = datetime.utcnow()
        expires_at = created_at + timedelta(hours=1)

        session_dict = {
            "session_id": "test-session-123",
            "user_id": 12345,
            "vault_id": 5678,
            "vault_name": "Test Vault",
            "created_at": created_at.isoformat(),
            "expires_at": expires_at.isoformat(),
            "metadata": {"key": "value"},
        }

        session = VaultSession.from_dict(session_dict)

        assert session.session_id == "test-session-123"
        assert session.user_id == 12345
        assert session.vault_id == 5678
        assert session.vault_name == "Test Vault"
        assert session.metadata == {"key": "value"}

    def test_session_from_dict_no_expiry(self):
        """Test creating session from dict without expiry."""
        created_at = datetime.utcnow()

        session_dict = {
            "session_id": "test-session-123",
            "user_id": 12345,
            "vault_id": 5678,
            "vault_name": "Test Vault",
            "created_at": created_at.isoformat(),
            "expires_at": None,
        }

        session = VaultSession.from_dict(session_dict)

        assert session.expires_at is None
        assert not session.is_expired()

    def test_session_roundtrip(self):
        """Test converting session to dict and back."""
        original = VaultSession(
            session_id="test-session-123",
            user_id=12345,
            vault_id=5678,
            vault_name="Test Vault",
            metadata={"auth_mode": "username_password"},
        )

        session_dict = original.to_dict()
        restored = VaultSession.from_dict(session_dict)

        assert restored.session_id == original.session_id
        assert restored.user_id == original.user_id
        assert restored.vault_id == original.vault_id
        assert restored.vault_name == original.vault_name
        assert restored.metadata == original.metadata
