# VeevaVault MCP Server - Updated Technical Plan

**Version:** 2.0 (Updated based on technical discussion)
**Date:** 2025-11-06
**Status:** Ready for Implementation

---

## 📋 Decisions Summary

Based on our discussion, here are the confirmed technical decisions:

1. ✅ **Deployment:** Docker initially, architected for Kubernetes migration
2. ✅ **Authentication:** Support both username/password AND OAuth2
3. ✅ **Caching:** In-memory initially, expandable to Valkey
4. ✅ **Monitoring:** Both structured logs AND Prometheus metrics
5. ⏸️ **CI/CD:** Deferred (focus on core implementation first)
6. ✅ **Development:** VS Code, Vault sandbox available

---

## Technology Stack (Updated)

### Core Technologies

**Unchanged from v1.0:**
- Python 3.11+
- MCP SDK from Anthropic
- Pydantic for validation
- Structlog for logging
- Tenacity for retries

### Updated Dependencies

```toml
# pyproject.toml

[project]
name = "veevavault-mcp-server"
version = "0.1.0"
requires-python = ">=3.11"

dependencies = [
    "mcp>=1.0.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "httpx>=0.25.0",
    "python-dotenv>=1.0.0",
    "structlog>=23.2.0",
    "tenacity>=8.2.0",
    "prometheus-client>=0.19.0",  # Metrics from day 1

    # Authentication
    "python-jose[cryptography]>=3.3.0",  # JWT handling for OAuth2
    "passlib>=1.7.4",  # Password hashing

    # Caching (optional, for Valkey expansion)
    "valkey>=5.0.0",  # Valkey Python client (Redis-compatible)
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "black>=23.12.0",
    "ruff>=0.1.9",
    "mypy>=1.7.0",
    "httpx[http2]>=0.25.0",  # For testing
]

valkey = [
    "valkey>=5.0.0",
    "valkey-py[hiredis]>=5.0.0"  # Performance boost with hiredis
]
```

---

## Updated Authentication Architecture

### Two Authentication Modes

We'll implement **both** authentication patterns with a configurable switch:

#### **Mode 1: Username/Password (Simple)**
- For: Personal use, small teams, development
- Credentials in environment variables
- Fast setup

#### **Mode 2: OAuth2 (Enterprise)**
- For: Multi-user deployments, compliance requirements
- JWT token validation
- User-specific Vault sessions

### Configuration

```python
# src/veevavault_mcp/config.py

from enum import Enum
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from typing import Optional


class AuthMode(str, Enum):
    """Authentication modes."""
    USERNAME_PASSWORD = "username_password"
    OAUTH2 = "oauth2"


class Config(BaseSettings):
    """Configuration for VeevaVault MCP Server."""

    # ==========================================
    # Authentication Configuration
    # ==========================================

    auth_mode: AuthMode = Field(
        default=AuthMode.USERNAME_PASSWORD,
        description="Authentication mode: username_password or oauth2"
    )

    # Username/Password Mode
    vault_url: str = Field(..., description="Veeva Vault URL")
    vault_username: Optional[str] = Field(
        default=None,
        description="Vault username (required for username_password mode)"
    )
    vault_password: Optional[str] = Field(
        default=None,
        description="Vault password (required for username_password mode)"
    )

    # OAuth2 Mode
    oauth2_token_url: Optional[str] = Field(
        default=None,
        description="OAuth2 token endpoint (required for oauth2 mode)"
    )
    oauth2_jwks_url: Optional[str] = Field(
        default=None,
        description="JWKS endpoint for token validation"
    )
    oauth2_audience: Optional[str] = Field(
        default=None,
        description="Expected audience in JWT tokens"
    )

    # Service Account (for OAuth2 mode - MCP server authenticates with Vault)
    service_account_username: Optional[str] = Field(
        default=None,
        description="Service account for OAuth2 mode"
    )
    service_account_password: Optional[str] = Field(
        default=None,
        description="Service account password"
    )

    # ==========================================
    # Caching Configuration
    # ==========================================

    enable_caching: bool = Field(
        default=True,
        description="Enable response caching"
    )
    cache_backend: str = Field(
        default="memory",
        description="Cache backend: 'memory' or 'valkey'"
    )
    cache_ttl: int = Field(
        default=300,
        description="Cache TTL in seconds"
    )

    # Valkey Configuration (optional)
    valkey_url: Optional[str] = Field(
        default=None,
        description="Valkey URL (e.g., valkey://localhost:6379)"
    )
    valkey_password: Optional[str] = Field(
        default=None,
        description="Valkey password"
    )
    valkey_db: int = Field(
        default=0,
        description="Valkey database number"
    )

    # ==========================================
    # Monitoring Configuration
    # ==========================================

    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    log_format: str = Field(
        default="json",
        description="Log format: json or console"
    )

    enable_metrics: bool = Field(
        default=True,
        description="Enable Prometheus metrics"
    )
    metrics_port: int = Field(
        default=9090,
        description="Metrics server port"
    )

    # ==========================================
    # Rate Limiting
    # ==========================================

    rate_limit_enabled: bool = Field(
        default=True,
        description="Enable rate limiting"
    )
    rate_limit_calls: int = Field(
        default=100,
        description="Max calls per minute per user"
    )

    # ==========================================
    # Kubernetes Readiness
    # ==========================================

    # These will be used later for Kubernetes deployment
    kubernetes_mode: bool = Field(
        default=False,
        description="Enable Kubernetes-specific features"
    )
    pod_name: Optional[str] = Field(
        default=None,
        description="Kubernetes pod name (auto-populated)"
    )
    pod_namespace: Optional[str] = Field(
        default=None,
        description="Kubernetes namespace"
    )

    @field_validator("vault_url")
    def validate_vault_url(cls, v):
        """Ensure vault_url has scheme."""
        if not v.startswith(("http://", "https://")):
            return f"https://{v}"
        return v

    def validate_auth_config(self):
        """Validate authentication configuration."""
        if self.auth_mode == AuthMode.USERNAME_PASSWORD:
            if not self.vault_username or not self.vault_password:
                raise ValueError(
                    "vault_username and vault_password required for username_password mode"
                )
        elif self.auth_mode == AuthMode.OAUTH2:
            if not all([
                self.oauth2_token_url,
                self.oauth2_jwks_url,
                self.service_account_username,
                self.service_account_password
            ]):
                raise ValueError(
                    "OAuth2 configuration incomplete. Need: "
                    "oauth2_token_url, oauth2_jwks_url, "
                    "service_account_username, service_account_password"
                )

    class Config:
        env_file = ".env"
        env_prefix = "VAULT_"
```

### Authentication Manager Implementation

```python
# src/veevavault_mcp/auth/manager.py

from abc import ABC, abstractmethod
from typing import Optional, Dict
from datetime import datetime, timedelta
import asyncio
import structlog

from veevavault import VaultClient
from ..config import Config, AuthMode

logger = structlog.get_logger(__name__)


class AuthenticationManager(ABC):
    """Base authentication manager."""

    @abstractmethod
    async def authenticate(self):
        """Authenticate with Vault."""
        pass

    @abstractmethod
    def get_client(self, user_context: Optional[str] = None) -> VaultClient:
        """Get authenticated Vault client."""
        pass


class UsernamePasswordAuthManager(AuthenticationManager):
    """
    Username/Password authentication.
    Single shared session for all users.
    """

    def __init__(self, config: Config):
        self.config = config
        self._client: Optional[VaultClient] = None
        self._session_expires_at: Optional[datetime] = None
        self._lock = asyncio.Lock()

    async def authenticate(self):
        """Authenticate with username/password."""
        async with self._lock:
            logger.info(
                "Authenticating with username/password",
                url=self.config.vault_url,
                username=self.config.vault_username
            )

            self._client = VaultClient(
                vault_url=self.config.vault_url,
                vault_username=self.config.vault_username,
                vault_password=self.config.vault_password
            )

            from veevavault.services.authentication import AuthenticationService
            auth_service = AuthenticationService(self._client)
            result = auth_service.authenticate(if_return=True)

            # Vault sessions typically last 12 hours, refresh at 11 hours
            self._session_expires_at = datetime.now() + timedelta(hours=11)

            logger.info(
                "Authentication successful",
                session_id=result["sessionId"][:10] + "...",
                mode="username_password"
            )

    async def ensure_authenticated(self):
        """Ensure session is still valid."""
        if self._client is None:
            await self.authenticate()
            return

        if self._session_expires_at:
            time_left = self._session_expires_at - datetime.now()
            if time_left < timedelta(minutes=30):
                logger.info("Session expiring soon, re-authenticating")
                await self.authenticate()

    def get_client(self, user_context: Optional[str] = None) -> VaultClient:
        """
        Get Vault client.

        Note: user_context ignored in this mode - everyone uses same client.
        """
        if self._client is None:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        if user_context:
            logger.warning(
                "Username/password mode - user context ignored",
                user_context=user_context,
                note="All operations logged as configured user"
            )

        return self._client


class OAuth2AuthManager(AuthenticationManager):
    """
    OAuth2 authentication with per-user sessions.
    Maintains separate Vault sessions for each user.
    """

    def __init__(self, config: Config):
        self.config = config
        self._service_client: Optional[VaultClient] = None
        self._user_sessions: Dict[str, 'UserSession'] = {}
        self._lock = asyncio.Lock()

    async def authenticate(self):
        """Authenticate service account with Vault."""
        async with self._lock:
            logger.info(
                "Authenticating service account",
                url=self.config.vault_url,
                service_account=self.config.service_account_username
            )

            self._service_client = VaultClient(
                vault_url=self.config.vault_url,
                vault_username=self.config.service_account_username,
                vault_password=self.config.service_account_password
            )

            from veevavault.services.authentication import AuthenticationService
            auth_service = AuthenticationService(self._service_client)
            auth_service.authenticate()

            logger.info(
                "Service account authenticated",
                mode="oauth2"
            )

    async def validate_user_token(self, token: str) -> Dict:
        """
        Validate OAuth2 JWT token and extract user info.

        Returns:
            {
                "user_id": "john.smith@company.com",
                "email": "john.smith@company.com",
                "name": "John Smith",
                "exp": 1699999999
            }
        """
        from jose import jwt, JWTError

        try:
            # Fetch JWKS (JSON Web Key Set) for validation
            # In production, cache this!
            jwks = await self._fetch_jwks()

            # Decode and validate token
            payload = jwt.decode(
                token,
                jwks,
                algorithms=["RS256"],
                audience=self.config.oauth2_audience
            )

            logger.info(
                "Token validated",
                user_id=payload.get("sub"),
                email=payload.get("email")
            )

            return {
                "user_id": payload.get("email") or payload.get("sub"),
                "email": payload.get("email"),
                "name": payload.get("name"),
                "exp": payload.get("exp")
            }

        except JWTError as e:
            logger.error("Token validation failed", error=str(e))
            raise ValueError(f"Invalid token: {e}")

    async def _fetch_jwks(self):
        """Fetch JWKS for token validation."""
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.get(self.config.oauth2_jwks_url)
            response.raise_for_status()
            return response.json()

    async def get_user_vault_session(self, user_id: str) -> VaultClient:
        """
        Get or create Vault session for specific user.

        Options for user-specific sessions:
        1. Service account with impersonation (if Vault supports)
        2. Per-user credentials (stored securely)
        3. Token exchange (OAuth token -> Vault session)
        """

        async with self._lock:
            # Check if we have cached session
            if user_id in self._user_sessions:
                session = self._user_sessions[user_id]
                if not session.is_expired():
                    return session.client

            # Create new user session
            # Option 1: Impersonation (if Vault supports it)
            try:
                client = await self._create_impersonated_session(user_id)
            except NotImplementedError:
                # Option 2: Fall back to service account
                # (all operations logged as service account)
                logger.warning(
                    "Impersonation not supported, using service account",
                    user_id=user_id
                )
                client = self._service_client

            # Cache session
            self._user_sessions[user_id] = UserSession(
                client=client,
                user_id=user_id,
                expires_at=datetime.now() + timedelta(hours=11)
            )

            return client

    async def _create_impersonated_session(self, user_id: str) -> VaultClient:
        """
        Create Vault session impersonating specific user.

        Note: This depends on Vault supporting impersonation.
        If not supported, raise NotImplementedError.
        """
        # TODO: Implement if Vault supports impersonation
        # For now, not supported
        raise NotImplementedError("Vault impersonation not yet implemented")

    def get_client(self, user_context: Optional[str] = None) -> VaultClient:
        """
        Get Vault client for specific user.

        Args:
            user_context: OAuth2 token or user_id
        """
        if not user_context:
            raise ValueError("user_context required in OAuth2 mode")

        # If user_context is a JWT token, validate and extract user_id
        if user_context.startswith("eyJ"):  # JWT tokens start with eyJ
            import asyncio
            user_info = asyncio.run(self.validate_user_token(user_context))
            user_id = user_info["user_id"]
        else:
            user_id = user_context

        # Get user-specific Vault session
        return asyncio.run(self.get_user_vault_session(user_id))


class UserSession:
    """Container for user Vault session."""

    def __init__(self, client: VaultClient, user_id: str, expires_at: datetime):
        self.client = client
        self.user_id = user_id
        self.expires_at = expires_at

    def is_expired(self) -> bool:
        """Check if session is expired or expiring soon."""
        time_left = self.expires_at - datetime.now()
        return time_left < timedelta(minutes=30)


# Factory function
def create_auth_manager(config: Config) -> AuthenticationManager:
    """Create appropriate authentication manager based on config."""
    if config.auth_mode == AuthMode.USERNAME_PASSWORD:
        return UsernamePasswordAuthManager(config)
    elif config.auth_mode == AuthMode.OAUTH2:
        return OAuth2AuthManager(config)
    else:
        raise ValueError(f"Unknown auth mode: {config.auth_mode}")
```

---

## Updated Caching Architecture

### Dual-Backend Cache System

```python
# src/veevavault_mcp/utils/cache.py

from abc import ABC, abstractmethod
from typing import Optional, Any
import hashlib
import json
from datetime import datetime, timedelta
import structlog

logger = structlog.get_logger(__name__)


class CacheBackend(ABC):
    """Abstract cache backend."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int):
        """Set value in cache with TTL."""
        pass

    @abstractmethod
    async def delete(self, key: str):
        """Delete key from cache."""
        pass

    @abstractmethod
    async def clear(self):
        """Clear all cached values."""
        pass


class MemoryCacheBackend(CacheBackend):
    """In-memory cache backend (default)."""

    def __init__(self):
        self._cache: dict = {}
        logger.info("Using in-memory cache backend")

    async def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            value, expires_at = self._cache[key]
            if datetime.now() < expires_at:
                logger.debug("Cache hit", key=key[:20])
                return value
            else:
                del self._cache[key]
                logger.debug("Cache expired", key=key[:20])
        return None

    async def set(self, key: str, value: Any, ttl: int):
        expires_at = datetime.now() + timedelta(seconds=ttl)
        self._cache[key] = (value, expires_at)
        logger.debug("Cache set", key=key[:20], ttl=ttl)

    async def delete(self, key: str):
        if key in self._cache:
            del self._cache[key]

    async def clear(self):
        self._cache.clear()
        logger.info("Cache cleared")


class ValkeyCacheBackend(CacheBackend):
    """Valkey cache backend for distributed caching."""

    def __init__(self, valkey_url: str, password: Optional[str] = None, db: int = 0):
        import valkey

        self.client = valkey.from_url(
            valkey_url,
            password=password,
            db=db,
            decode_responses=True
        )
        logger.info(
            "Using Valkey cache backend",
            url=valkey_url,
            db=db
        )

    async def get(self, key: str) -> Optional[Any]:
        value = self.client.get(key)
        if value:
            logger.debug("Valkey cache hit", key=key[:20])
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: int):
        serialized = json.dumps(value)
        self.client.setex(key, ttl, serialized)
        logger.debug("Valkey cache set", key=key[:20], ttl=ttl)

    async def delete(self, key: str):
        self.client.delete(key)

    async def clear(self):
        self.client.flushdb()
        logger.warning("Valkey cache cleared (entire DB)")


class Cache:
    """Cache manager with pluggable backends."""

    def __init__(self, backend: CacheBackend, ttl: int = 300):
        self.backend = backend
        self.ttl = ttl

    def _make_key(self, func_name: str, **kwargs) -> str:
        """Generate cache key from function name and parameters."""
        # Sort kwargs for consistent keys
        params_str = json.dumps(kwargs, sort_keys=True)
        key = f"vault_mcp:{func_name}:{hashlib.md5(params_str.encode()).hexdigest()}"
        return key

    async def get(self, key: str) -> Optional[Any]:
        """Get cached value."""
        return await self.backend.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set cached value."""
        await self.backend.set(key, value, ttl or self.ttl)

    async def delete(self, key: str):
        """Delete cached value."""
        await self.backend.delete(key)

    async def clear(self):
        """Clear all cached values."""
        await self.backend.clear()


def create_cache(config) -> Cache:
    """Create cache with configured backend."""
    if not config.enable_caching:
        logger.info("Caching disabled")
        return None

    if config.cache_backend == "memory":
        backend = MemoryCacheBackend()
    elif config.cache_backend == "valkey":
        if not config.valkey_url:
            raise ValueError("valkey_url required for valkey backend")
        backend = ValkeyCacheBackend(
            valkey_url=config.valkey_url,
            password=config.valkey_password,
            db=config.valkey_db
        )
    else:
        raise ValueError(f"Unknown cache backend: {config.cache_backend}")

    return Cache(backend, ttl=config.cache_ttl)


def cached(cache: Optional[Cache]):
    """Decorator to cache function results."""
    def decorator(func):
        if cache is None:
            # Caching disabled, pass through
            return func

        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = cache._make_key(func.__name__, **kwargs)

            # Check cache
            cached_result = await cache.get(key)
            if cached_result is not None:
                return cached_result

            # Execute and cache
            result = await func(*args, **kwargs)
            await cache.set(key, result)

            return result
        return wrapper
    return decorator
```

---

## Prometheus Metrics Implementation

```python
# src/veevavault_mcp/monitoring/metrics.py

from prometheus_client import Counter, Histogram, Gauge, start_http_server
import structlog
from functools import wraps
import time

logger = structlog.get_logger(__name__)

# Define metrics
tool_calls_total = Counter(
    'vault_mcp_tool_calls_total',
    'Total number of tool calls',
    ['tool_name', 'status']  # labels
)

tool_duration_seconds = Histogram(
    'vault_mcp_tool_duration_seconds',
    'Tool execution duration in seconds',
    ['tool_name']
)

active_sessions = Gauge(
    'vault_mcp_active_sessions',
    'Number of active Vault sessions'
)

cache_hits = Counter(
    'vault_mcp_cache_hits_total',
    'Total cache hits',
    ['tool_name']
)

cache_misses = Counter(
    'vault_mcp_cache_misses_total',
    'Total cache misses',
    ['tool_name']
)

vault_api_errors = Counter(
    'vault_mcp_vault_api_errors_total',
    'Total Vault API errors',
    ['error_type']
)


def metrics_enabled(config):
    """Check if metrics are enabled."""
    return config.enable_metrics


def start_metrics_server(config):
    """Start Prometheus metrics HTTP server."""
    if config.enable_metrics:
        start_http_server(config.metrics_port)
        logger.info(
            "Metrics server started",
            port=config.metrics_port,
            endpoint=f"http://0.0.0.0:{config.metrics_port}/metrics"
        )


def track_tool_execution(tool_name: str):
    """Decorator to track tool execution metrics."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Start timer
            start_time = time.time()

            try:
                # Execute tool
                result = await func(*args, **kwargs)

                # Record success
                tool_calls_total.labels(
                    tool_name=tool_name,
                    status="success"
                ).inc()

                return result

            except Exception as e:
                # Record failure
                tool_calls_total.labels(
                    tool_name=tool_name,
                    status="error"
                ).inc()

                # Track error type
                error_type = type(e).__name__
                vault_api_errors.labels(error_type=error_type).inc()

                raise

            finally:
                # Record duration
                duration = time.time() - start_time
                tool_duration_seconds.labels(tool_name=tool_name).observe(duration)

        return wrapper
    return decorator
```

---

## Docker Configuration (Updated)

### Dockerfile

```dockerfile
# Dockerfile

FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy source code
COPY src/ ./src/

# Create non-root user
RUN useradd -m -u 1000 mcp && chown -R mcp:mcp /app
USER mcp

# Environment
ENV PYTHONUNBUFFERED=1
ENV VAULT_LOG_LEVEL=INFO
ENV VAULT_LOG_FORMAT=json

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:9090/metrics')" || exit 1

# Expose metrics port
EXPOSE 9090

# Run MCP server
CMD ["python", "-m", "veevavault_mcp"]
```

### Docker Compose (Development)

```yaml
# docker-compose.yml

version: '3.8'

services:
  veevavault-mcp:
    build: .
    container_name: veevavault-mcp
    environment:
      # Authentication
      - VAULT_AUTH_MODE=username_password
      - VAULT_URL=${VAULT_URL}
      - VAULT_USERNAME=${VAULT_USERNAME}
      - VAULT_PASSWORD=${VAULT_PASSWORD}

      # Caching
      - VAULT_ENABLE_CACHING=true
      - VAULT_CACHE_BACKEND=memory
      - VAULT_CACHE_TTL=300

      # Monitoring
      - VAULT_LOG_LEVEL=INFO
      - VAULT_LOG_FORMAT=json
      - VAULT_ENABLE_METRICS=true
      - VAULT_METRICS_PORT=9090

      # Rate Limiting
      - VAULT_RATE_LIMIT_ENABLED=true
      - VAULT_RATE_LIMIT_CALLS=100
    ports:
      - "9090:9090"  # Metrics
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - vault-network

  # Optional: Valkey for distributed caching (future)
  valkey:
    image: valkey/valkey:7.2-alpine
    container_name: vault-mcp-valkey
    command: valkey-server --save 60 1 --loglevel warning
    volumes:
      - valkey-data:/data
    networks:
      - vault-network
    profiles:
      - with-valkey  # Only start when explicitly requested

volumes:
  valkey-data:

networks:
  vault-network:
    driver: bridge
```

### Usage

```bash
# Development (memory cache only)
docker-compose up

# With Valkey (distributed cache)
docker-compose --profile with-valkey up

# Then update .env:
# VAULT_CACHE_BACKEND=valkey
# VAULT_VALKEY_URL=valkey://valkey:6379
```

---

## Kubernetes Readiness (Architecture)

While we're starting with Docker, here's how the architecture supports Kubernetes migration:

### ConfigMap for Configuration

```yaml
# kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: veevavault-mcp-config
data:
  VAULT_URL: "https://company.veevavault.com"
  VAULT_AUTH_MODE: "oauth2"
  VAULT_CACHE_BACKEND: "valkey"
  VAULT_VALKEY_URL: "valkey://valkey-service:6379"
  VAULT_ENABLE_METRICS: "true"
  VAULT_METRICS_PORT: "9090"
```

### Secret for Credentials

```yaml
# kubernetes/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: veevavault-mcp-secrets
type: Opaque
stringData:
  VAULT_SERVICE_ACCOUNT_USERNAME: "service-bot@company.com"
  VAULT_SERVICE_ACCOUNT_PASSWORD: "SecurePassword123"
  VAULT_VALKEY_PASSWORD: "ValKeyPassword"
```

### Deployment

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: veevavault-mcp
spec:
  replicas: 3  # Multiple pods for high availability
  selector:
    matchLabels:
      app: veevavault-mcp
  template:
    metadata:
      labels:
        app: veevavault-mcp
    spec:
      containers:
      - name: mcp-server
        image: company-registry/veevavault-mcp:latest
        ports:
        - containerPort: 9090
          name: metrics
        envFrom:
        - configMapRef:
            name: veevavault-mcp-config
        - secretRef:
            name: veevavault-mcp-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /metrics
            port: 9090
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /metrics
            port: 9090
          initialDelaySeconds: 5
          periodSeconds: 5
```

---

## Environment Configuration Examples

### Development (.env.dev)

```bash
# Authentication
VAULT_AUTH_MODE=username_password
VAULT_URL=https://sandbox.veevavault.com
VAULT_USERNAME=your.username@company.com
VAULT_PASSWORD=YourPassword123

# Caching
VAULT_ENABLE_CACHING=true
VAULT_CACHE_BACKEND=memory
VAULT_CACHE_TTL=300

# Monitoring
VAULT_LOG_LEVEL=DEBUG
VAULT_LOG_FORMAT=console
VAULT_ENABLE_METRICS=true
VAULT_METRICS_PORT=9090

# Rate Limiting
VAULT_RATE_LIMIT_ENABLED=false  # Disabled for dev
```

### Production (.env.prod)

```bash
# Authentication
VAULT_AUTH_MODE=oauth2
VAULT_URL=https://production.veevavault.com
VAULT_OAUTH2_TOKEN_URL=https://auth.company.com/oauth/token
VAULT_OAUTH2_JWKS_URL=https://auth.company.com/.well-known/jwks.json
VAULT_OAUTH2_AUDIENCE=vault-mcp-server
VAULT_SERVICE_ACCOUNT_USERNAME=service-bot@company.com
VAULT_SERVICE_ACCOUNT_PASSWORD=${SERVICE_PASSWORD}  # From secrets manager

# Caching
VAULT_ENABLE_CACHING=true
VAULT_CACHE_BACKEND=valkey
VAULT_CACHE_TTL=300
VAULT_VALKEY_URL=valkey://valkey-cluster:6379
VAULT_VALKEY_PASSWORD=${VALKEY_PASSWORD}  # From secrets manager

# Monitoring
VAULT_LOG_LEVEL=INFO
VAULT_LOG_FORMAT=json
VAULT_ENABLE_METRICS=true
VAULT_METRICS_PORT=9090

# Rate Limiting
VAULT_RATE_LIMIT_ENABLED=true
VAULT_RATE_LIMIT_CALLS=100

# Kubernetes
VAULT_KUBERNETES_MODE=true
```

---

## Development Setup (VS Code)

### VS Code Extensions

Recommended extensions:
- Python (microsoft.python)
- Pylance (microsoft.pylance)
- Docker (microsoft.docker)
- YAML (redhat.vscode-yaml)
- Even Better TOML (tamasfe.even-better-toml)

### VS Code Settings (.vscode/settings.json)

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[python]": {
    "editor.rulers": [88]
  }
}
```

### VS Code Launch Configuration (.vscode/launch.json)

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: MCP Server",
      "type": "python",
      "request": "launch",
      "module": "veevavault_mcp",
      "justMyCode": false,
      "env": {
        "VAULT_URL": "https://sandbox.veevavault.com",
        "VAULT_USERNAME": "your.username@company.com",
        "VAULT_PASSWORD": "YourPassword123",
        "VAULT_LOG_LEVEL": "DEBUG"
      }
    },
    {
      "name": "Python: Run Tests",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v", "--cov=veevavault_mcp"],
      "justMyCode": false
    }
  ]
}
```

---

## Updated Phase 1 Timeline

### Week 1: Foundation ✅
**Days 1-2: Project Setup**
- Create project structure
- Set up pyproject.toml with dependencies
- Configure VS Code
- Initialize Git repository

**Days 3-5: Configuration & Auth**
- Implement Config class with dual auth modes
- Implement UsernamePasswordAuthManager
- Implement OAuth2AuthManager (skeleton)
- Add metrics initialization

**Deliverable:** Server can authenticate in both modes

### Week 2: Core Infrastructure ✅
**Days 1-3: Caching & Monitoring**
- Implement MemoryCacheBackend
- Implement ValkeyCacheBackend
- Set up Prometheus metrics
- Configure structured logging

**Days 4-5: Base Tool System**
- Implement BaseTool class
- Add parameter validation
- Add error handling
- Write unit tests

**Deliverable:** Complete infrastructure ready for tools

### Week 3: Documents Tools (Part 1) 📝
**Days 1-2:** `documents_query`
**Day 3:** `documents_get`
**Days 4-5:** `documents_create`, `documents_update`

**Deliverable:** Basic document CRUD

### Week 4: Documents Tools (Part 2) 📝
**Days 1-2:** `documents_delete`, upload/download
**Days 3-4:** Lock management, lifecycle
**Day 5:** Integration testing

**Deliverable:** Complete documents resource

### Week 5: Objects & VQL 📝
**Days 1-3:** Objects tools (5 tools)
**Days 4-5:** VQL tools (2 tools)

**Deliverable:** Phase 1 complete - 30 tools

---

## Summary of Updates

### ✅ Decisions Implemented:

1. **Dual Authentication** - Both username/password and OAuth2
2. **Flexible Caching** - Memory by default, Valkey expansion ready
3. **Metrics from Day 1** - Prometheus metrics built-in
4. **Kubernetes-Ready** - Architecture supports K8s migration
5. **Valkey over Redis** - Using Valkey (Redis fork)

### 🎯 Ready to Start:

- ✅ Technical architecture finalized
- ✅ Dependencies defined
- ✅ VS Code setup documented
- ✅ Docker configuration ready
- ✅ Authentication patterns implemented
- ✅ Monitoring infrastructure designed

### 📅 Next Steps:

1. **Set up development environment** (VS Code + venv)
2. **Create project structure** (folders + files)
3. **Start Week 1: Foundation** (Config + Auth)
4. **Daily progress tracking**

**Ready to begin implementation?** 🚀
