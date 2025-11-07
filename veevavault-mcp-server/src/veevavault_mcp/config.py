"""Configuration management for VeevaVault MCP Server."""

from enum import Enum
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthMode(str, Enum):
    """Authentication modes supported by the server."""

    USERNAME_PASSWORD = "username_password"
    OAUTH2 = "oauth2"


class Config(BaseSettings):
    """
    Configuration for VeevaVault MCP Server.

    All settings can be provided via environment variables with VAULT_ prefix.
    Example: VAULT_URL, VAULT_USERNAME, etc.
    """

    model_config = SettingsConfigDict(
        env_prefix="VAULT_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        # Allow missing .env file
        env_ignore_empty=True,
    )

    # ==========================================
    # Authentication Configuration
    # ==========================================

    auth_mode: AuthMode = Field(
        default=AuthMode.USERNAME_PASSWORD,
        description="Authentication mode: username_password or oauth2",
    )

    # Vault Connection
    url: str = Field(..., description="Veeva Vault URL")

    # Username/Password Mode
    username: Optional[str] = Field(
        default=None, description="Vault username (required for username_password mode)"
    )
    password: Optional[str] = Field(
        default=None, description="Vault password (required for username_password mode)"
    )

    # OAuth2 Mode
    oauth2_token_url: Optional[str] = Field(
        default=None, description="OAuth2 token endpoint (required for oauth2 mode)"
    )
    oauth2_jwks_url: Optional[str] = Field(
        default=None, description="JWKS endpoint for token validation (required for oauth2 mode)"
    )
    oauth2_audience: Optional[str] = Field(
        default=None, description="Expected audience in JWT tokens"
    )

    # Service Account (for OAuth2 mode - MCP server authenticates with Vault)
    service_account_username: Optional[str] = Field(
        default=None, description="Service account username for OAuth2 mode"
    )
    service_account_password: Optional[str] = Field(
        default=None, description="Service account password for OAuth2 mode"
    )

    # ==========================================
    # Caching Configuration
    # ==========================================

    enable_caching: bool = Field(default=True, description="Enable response caching")
    cache_backend: str = Field(
        default="memory", description="Cache backend: 'memory' or 'valkey'"
    )
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds")

    # Valkey Configuration (optional)
    valkey_url: Optional[str] = Field(
        default=None, description="Valkey URL (e.g., valkey://localhost:6379)"
    )
    valkey_password: Optional[str] = Field(default=None, description="Valkey password")
    valkey_db: int = Field(default=0, description="Valkey database number")

    # ==========================================
    # Monitoring Configuration
    # ==========================================

    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or console")

    enable_metrics: bool = Field(
        default=True, description="Enable Prometheus metrics"
    )
    metrics_port: int = Field(default=9090, description="Metrics server port")

    # ==========================================
    # Rate Limiting
    # ==========================================

    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_calls: int = Field(
        default=100, description="Max calls per minute per user"
    )

    # ==========================================
    # Kubernetes Configuration (Optional)
    # ==========================================

    kubernetes_mode: bool = Field(
        default=False, description="Enable Kubernetes-specific features"
    )
    pod_name: Optional[str] = Field(
        default=None, description="Kubernetes pod name (auto-populated)"
    )
    pod_namespace: Optional[str] = Field(
        default=None, description="Kubernetes namespace"
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Ensure URL has proper scheme."""
        if not v:
            raise ValueError("url is required")
        if not v.startswith(("http://", "https://")):
            return f"https://{v}"
        return v

    @field_validator("auth_mode", mode="before")
    @classmethod
    def validate_auth_mode(cls, v: str) -> str:
        """Normalize auth_mode value."""
        if isinstance(v, str):
            v = v.lower()
        return v

    @field_validator("cache_backend")
    @classmethod
    def validate_cache_backend(cls, v: str) -> str:
        """Validate cache backend value."""
        if v not in ("memory", "valkey"):
            raise ValueError(f"Invalid cache_backend: {v}. Must be 'memory' or 'valkey'")
        return v

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Normalize and validate log level."""
        v = v.upper()
        valid_levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
        if v not in valid_levels:
            raise ValueError(
                f"Invalid log_level: {v}. Must be one of {valid_levels}"
            )
        return v

    @field_validator("log_format")
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        """Validate log format."""
        if v not in ("json", "console"):
            raise ValueError(f"Invalid log_format: {v}. Must be 'json' or 'console'")
        return v

    def validate_auth_config(self) -> None:
        """Validate authentication configuration based on auth_mode."""
        if self.auth_mode == AuthMode.USERNAME_PASSWORD:
            if not self.username or not self.password:
                raise ValueError(
                    "username and password are required for username_password mode"
                )
        elif self.auth_mode == AuthMode.OAUTH2:
            missing = []
            if not self.oauth2_token_url:
                missing.append("oauth2_token_url")
            if not self.oauth2_jwks_url:
                missing.append("oauth2_jwks_url")
            if not self.service_account_username:
                missing.append("service_account_username")
            if not self.service_account_password:
                missing.append("service_account_password")

            if missing:
                raise ValueError(
                    f"OAuth2 mode requires: {', '.join(missing)}"
                )

    def validate_cache_config(self) -> None:
        """Validate caching configuration."""
        if self.enable_caching and self.cache_backend == "valkey":
            if not self.valkey_url:
                raise ValueError(
                    "valkey_url is required when cache_backend='valkey'"
                )

    def validate_all(self) -> None:
        """Run all validation checks."""
        self.validate_auth_config()
        self.validate_cache_config()

    def summary(self) -> dict:
        """Return sanitized configuration summary (no passwords)."""
        return {
            "auth_mode": self.auth_mode.value,
            "url": self.url,
            "username": self.username if self.username else None,
            "enable_caching": self.enable_caching,
            "cache_backend": self.cache_backend,
            "cache_ttl": self.cache_ttl,
            "log_level": self.log_level,
            "log_format": self.log_format,
            "enable_metrics": self.enable_metrics,
            "metrics_port": self.metrics_port,
            "kubernetes_mode": self.kubernetes_mode,
        }
