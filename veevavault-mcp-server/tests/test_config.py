"""
Tests for configuration module.
"""

import pytest
from pydantic import ValidationError as PydanticValidationError

from veevavault_mcp.config import Config, AuthMode
from veevavault_mcp.utils.errors import ConfigurationError


class TestConfigUsernamePassword:
    """Tests for username/password authentication configuration."""

    def test_config_loads_from_env(self, config_username_password):
        """Test configuration loads correctly from environment variables."""
        assert config_username_password.auth_mode == AuthMode.USERNAME_PASSWORD
        assert config_username_password.url == "https://test-vault.veevavault.com"
        assert config_username_password.username == "test.user@example.com"
        assert config_username_password.password == "TestPassword123"
        assert config_username_password.enable_caching is True
        assert config_username_password.cache_backend == "memory"
        assert config_username_password.log_level == "DEBUG"

    def test_config_validates_auth_username_password(self, config_username_password):
        """Test authentication validation passes for username/password mode."""
        # Should not raise any exception
        config_username_password.validate_auth_config()

    def test_config_fails_without_username(self, monkeypatch):
        """Test configuration fails when username is missing."""
        monkeypatch.setenv("VAULT_AUTH_MODE", "username_password")
        monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
        monkeypatch.setenv("VAULT_PASSWORD", "TestPassword123")
        # Missing VAULT_USERNAME

        config = Config()
        with pytest.raises(ValueError, match="username and password are required"):
            config.validate_auth_config()

    def test_config_fails_without_password(self, monkeypatch):
        """Test configuration fails when password is missing."""
        monkeypatch.setenv("VAULT_AUTH_MODE", "username_password")
        monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
        monkeypatch.setenv("VAULT_USERNAME", "test.user@example.com")
        # Missing VAULT_PASSWORD

        config = Config()
        with pytest.raises(ValueError, match="username and password are required"):
            config.validate_auth_config()

    def test_config_summary_excludes_password(self, config_username_password):
        """Test configuration summary does not include password."""
        summary = config_username_password.summary()

        assert "password" not in summary
        assert summary["username"] == "test.user@example.com"
        assert summary["auth_mode"] == "username_password"
        assert summary["url"] == "https://test-vault.veevavault.com"


class TestConfigOAuth2:
    """Tests for OAuth2 authentication configuration."""

    def test_config_loads_oauth2_from_env(self, config_oauth2):
        """Test OAuth2 configuration loads correctly."""
        assert config_oauth2.auth_mode == AuthMode.OAUTH2
        assert config_oauth2.oauth2_token_url == "https://auth.example.com/oauth/token"
        assert config_oauth2.oauth2_jwks_url == "https://auth.example.com/.well-known/jwks.json"
        assert config_oauth2.oauth2_audience == "vault-mcp-server"
        assert config_oauth2.service_account_username == "service-bot@example.com"
        assert config_oauth2.service_account_password == "ServicePassword123"

    def test_config_validates_auth_oauth2(self, config_oauth2):
        """Test authentication validation passes for OAuth2 mode."""
        # Should not raise any exception
        config_oauth2.validate_auth_config()

    def test_config_fails_oauth2_missing_token_url(self, monkeypatch):
        """Test OAuth2 config fails when token URL is missing."""
        monkeypatch.setenv("VAULT_AUTH_MODE", "oauth2")
        monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
        monkeypatch.setenv("VAULT_OAUTH2_JWKS_URL", "https://auth.example.com/.well-known/jwks.json")
        monkeypatch.setenv("VAULT_SERVICE_ACCOUNT_USERNAME", "service-bot@example.com")
        monkeypatch.setenv("VAULT_SERVICE_ACCOUNT_PASSWORD", "ServicePassword123")
        # Missing VAULT_OAUTH2_TOKEN_URL

        config = Config()
        with pytest.raises(ValueError, match="oauth2_token_url"):
            config.validate_auth_config()

    def test_config_fails_oauth2_missing_jwks_url(self, monkeypatch):
        """Test OAuth2 config fails when JWKS URL is missing."""
        monkeypatch.setenv("VAULT_AUTH_MODE", "oauth2")
        monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
        monkeypatch.setenv("VAULT_OAUTH2_TOKEN_URL", "https://auth.example.com/oauth/token")
        monkeypatch.setenv("VAULT_SERVICE_ACCOUNT_USERNAME", "service-bot@example.com")
        monkeypatch.setenv("VAULT_SERVICE_ACCOUNT_PASSWORD", "ServicePassword123")
        # Missing VAULT_OAUTH2_JWKS_URL

        config = Config()
        with pytest.raises(ValueError, match="oauth2_jwks_url"):
            config.validate_auth_config()

    def test_config_fails_oauth2_missing_service_account(self, monkeypatch):
        """Test OAuth2 config fails when service account credentials are missing."""
        monkeypatch.setenv("VAULT_AUTH_MODE", "oauth2")
        monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
        monkeypatch.setenv("VAULT_OAUTH2_TOKEN_URL", "https://auth.example.com/oauth/token")
        monkeypatch.setenv("VAULT_OAUTH2_JWKS_URL", "https://auth.example.com/.well-known/jwks.json")
        # Missing service account credentials

        config = Config()
        with pytest.raises(ValueError, match="service_account_username"):
            config.validate_auth_config()


class TestConfigURLValidation:
    """Tests for URL validation."""

    def test_vault_url_adds_https_prefix(self, monkeypatch):
        """Test that URL gets https:// prefix if missing."""
        monkeypatch.setenv("VAULT_AUTH_MODE", "username_password")
        monkeypatch.setenv("VAULT_URL", "test-vault.veevavault.com")  # No scheme
        monkeypatch.setenv("VAULT_USERNAME", "test.user@example.com")
        monkeypatch.setenv("VAULT_PASSWORD", "TestPassword123")

        config = Config()
        assert config.url == "https://test-vault.veevavault.com"

    def test_vault_url_preserves_https(self, monkeypatch):
        """Test that URL preserves existing https:// prefix."""
        monkeypatch.setenv("VAULT_AUTH_MODE", "username_password")
        monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
        monkeypatch.setenv("VAULT_USERNAME", "test.user@example.com")
        monkeypatch.setenv("VAULT_PASSWORD", "TestPassword123")

        config = Config()
        assert config.url == "https://test-vault.veevavault.com"

    def test_vault_url_preserves_http(self, monkeypatch):
        """Test that URL preserves http:// prefix (for testing)."""
        monkeypatch.setenv("VAULT_AUTH_MODE", "username_password")
        monkeypatch.setenv("VAULT_URL", "http://localhost:8080")
        monkeypatch.setenv("VAULT_USERNAME", "test.user@example.com")
        monkeypatch.setenv("VAULT_PASSWORD", "TestPassword123")

        config = Config()
        assert config.url == "http://localhost:8080"


class TestConfigDefaults:
    """Tests for configuration default values."""

    def test_default_values(self, config_username_password):
        """Test that default values are set correctly."""
        assert config_username_password.enable_caching is True
        assert config_username_password.cache_backend == "memory"
        assert config_username_password.cache_ttl == 300
        assert config_username_password.log_level == "DEBUG"  # Set by fixture
        assert config_username_password.log_format == "json"
        assert config_username_password.enable_metrics is True
        assert config_username_password.metrics_port == 9090
        assert config_username_password.rate_limit_enabled is True
        assert config_username_password.rate_limit_calls == 100
        assert config_username_password.kubernetes_mode is False

    def test_auth_mode_default(self, monkeypatch):
        """Test that auth_mode defaults to username_password."""
        monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
        monkeypatch.setenv("VAULT_USERNAME", "test.user@example.com")
        monkeypatch.setenv("VAULT_PASSWORD", "TestPassword123")
        # VAULT_AUTH_MODE not set

        config = Config()
        assert config.auth_mode == AuthMode.USERNAME_PASSWORD
