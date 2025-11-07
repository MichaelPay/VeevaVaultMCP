# VeevaVault MCP Server - Technical Implementation Plan

**Version:** 1.0
**Date:** 2025-11-06
**Status:** Ready for Implementation

---

## Table of Contents

1. [Technology Stack](#technology-stack)
2. [Project Structure](#project-structure)
3. [MCP Server Architecture](#mcp-server-architecture)
4. [Tool Implementation Pattern](#tool-implementation-pattern)
5. [Resource Implementation Pattern](#resource-implementation-pattern)
6. [Authentication & Session Management](#authentication--session-management)
7. [Error Handling Strategy](#error-handling-strategy)
8. [Configuration Management](#configuration-management)
9. [Testing Strategy](#testing-strategy)
10. [Deployment Architecture](#deployment-architecture)
11. [Performance Optimization](#performance-optimization)
12. [Security Considerations](#security-considerations)
13. [Development Workflow](#development-workflow)
14. [Phase 1 Implementation Details](#phase-1-implementation-details)

---

## Technology Stack

### Core Technologies

**Programming Language:** Python 3.11+
- ✅ **Rationale:** VeevaVaultMCP library already in Python
- ✅ Excellent MCP SDK support
- ✅ Strong async/await support for performance
- ✅ Rich ecosystem for API development

**MCP Framework:** `mcp` Python SDK
```bash
pip install mcp
```
- Official Anthropic MCP SDK for Python
- Provides decorators for tools and resources
- Handles JSON-RPC protocol automatically
- Built-in validation and error handling

**Existing Library:** VeevaVaultMCP
- Already implements 600+ Vault API endpoints
- Located in `veevavault/` directory
- Will be used as the foundation for MCP tools

### Dependencies

```toml
# pyproject.toml

[project]
name = "veevavault-mcp-server"
version = "0.1.0"
description = "MCP Server for Veeva Vault API"
requires-python = ">=3.11"

dependencies = [
    "mcp>=1.0.0",              # MCP SDK
    "pydantic>=2.5.0",         # Data validation
    "httpx>=0.25.0",           # Async HTTP client
    "python-dotenv>=1.0.0",    # Environment config
    "structlog>=23.2.0",       # Structured logging
    "tenacity>=8.2.0",         # Retry logic
    "redis>=5.0.0",            # Optional: session caching
    "prometheus-client>=0.19.0" # Optional: metrics
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "black>=23.12.0",
    "ruff>=0.1.9",
    "mypy>=1.7.0"
]
```

### Additional Tools

- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD pipeline
- **Pre-commit** - Code quality hooks

---

## Project Structure

```
veevavault-mcp-server/
│
├── pyproject.toml              # Project metadata & dependencies
├── README.md                   # Project documentation
├── .env.example                # Example environment variables
├── .gitignore
├── Dockerfile
├── docker-compose.yml
│
├── src/
│   └── veevavault_mcp/
│       ├── __init__.py
│       ├── __main__.py         # Entry point
│       ├── server.py           # MCP server initialization
│       ├── config.py           # Configuration management
│       │
│       ├── auth/
│       │   ├── __init__.py
│       │   ├── manager.py      # Authentication manager
│       │   └── session.py      # Session management
│       │
│       ├── tools/              # MCP Tools organized by resource
│       │   ├── __init__.py
│       │   ├── base.py         # Base tool class
│       │   │
│       │   ├── documents/
│       │   │   ├── __init__.py
│       │   │   ├── query.py    # documents_query tool
│       │   │   ├── create.py   # documents_create tool
│       │   │   ├── get.py      # documents_get tool
│       │   │   ├── update.py   # documents_update tool
│       │   │   └── ...
│       │   │
│       │   ├── objects/
│       │   │   ├── __init__.py
│       │   │   ├── query.py
│       │   │   ├── create.py
│       │   │   └── ...
│       │   │
│       │   ├── vql/
│       │   │   ├── __init__.py
│       │   │   ├── execute.py
│       │   │   └── bulk_export.py
│       │   │
│       │   ├── workflows/
│       │   ├── binders/
│       │   ├── users/
│       │   └── ...
│       │
│       ├── resources/          # MCP Resources
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── documents.py    # vault://documents/* resources
│       │   ├── objects.py      # vault://objects/* resources
│       │   └── ...
│       │
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── formatting.py   # Response formatting
│       │   ├── validation.py   # Input validation
│       │   ├── query_builder.py # VQL query construction helpers
│       │   ├── errors.py       # Custom exceptions
│       │   └── cache.py        # Caching utilities
│       │
│       └── prompts/            # MCP Prompts (optional)
│           ├── __init__.py
│           └── executive.py    # Executive-level prompts
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── test_tools/
│   │   ├── test_documents.py
│   │   ├── test_objects.py
│   │   └── ...
│   ├── test_resources/
│   ├── test_auth/
│   └── integration/
│       └── test_vault_integration.py
│
├── docs/
│   ├── API.md                  # API documentation
│   ├── DEVELOPMENT.md          # Development guide
│   └── DEPLOYMENT.md           # Deployment guide
│
└── scripts/
    ├── setup_dev.sh            # Development environment setup
    ├── run_tests.sh            # Test runner
    └── build_docker.sh         # Docker build script
```

---

## MCP Server Architecture

### Server Initialization

```python
# src/veevavault_mcp/server.py

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
import structlog

from .config import Config
from .auth.manager import AuthenticationManager
from .tools import register_all_tools
from .resources import register_all_resources

logger = structlog.get_logger(__name__)


class VeevaVaultMCPServer:
    """Main MCP Server for Veeva Vault integration."""

    def __init__(self, config: Config):
        self.config = config
        self.server = Server("veevavault-mcp")
        self.auth_manager = AuthenticationManager(config)

    async def initialize(self):
        """Initialize server components."""
        logger.info("Initializing VeevaVault MCP Server")

        # Authenticate with Vault
        await self.auth_manager.authenticate()
        logger.info("Vault authentication successful")

        # Register tools
        register_all_tools(self.server, self.auth_manager)
        logger.info("Tools registered", count=len(self.server.list_tools()))

        # Register resources
        register_all_resources(self.server, self.auth_manager)
        logger.info("Resources registered")

    async def run(self):
        """Run the MCP server."""
        await self.initialize()

        # Run stdio server
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Entry point for MCP server."""
    config = Config.from_env()
    server = VeevaVaultMCPServer(config)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
```

### Configuration Management

```python
# src/veevavault_mcp/config.py

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from typing import Optional


class Config(BaseSettings):
    """Configuration for VeevaVault MCP Server."""

    # Vault Connection
    vault_url: str = Field(..., description="Veeva Vault URL")
    vault_username: str = Field(..., description="Vault username")
    vault_password: str = Field(..., description="Vault password")

    # Or OAuth2 (alternative to username/password)
    vault_client_id: Optional[str] = None
    vault_client_secret: Optional[str] = None

    # Server Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    enable_caching: bool = Field(default=True, description="Enable response caching")
    cache_ttl: int = Field(default=300, description="Cache TTL in seconds")

    # Rate Limiting
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    rate_limit_calls: int = Field(default=100, description="Max calls per minute")

    # Redis (optional for distributed caching)
    redis_url: Optional[str] = Field(default=None, description="Redis URL for caching")

    # Monitoring
    enable_metrics: bool = Field(default=False, description="Enable Prometheus metrics")
    metrics_port: int = Field(default=9090, description="Metrics server port")

    @field_validator("vault_url")
    def validate_vault_url(cls, v):
        """Ensure vault_url has scheme."""
        if not v.startswith(("http://", "https://")):
            return f"https://{v}"
        return v

    class Config:
        env_file = ".env"
        env_prefix = "VAULT_"  # All env vars start with VAULT_
```

---

## Tool Implementation Pattern

### Base Tool Class

```python
# src/veevavault_mcp/tools/base.py

from typing import Any, Dict, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, ValidationError
import structlog

from veevavault import VaultClient
from ..utils.errors import VaultMCPError, VaultAPIError
from ..auth.manager import AuthenticationManager

logger = structlog.get_logger(__name__)


class ToolParameters(BaseModel):
    """Base class for tool parameters with validation."""

    class Config:
        extra = "forbid"  # Reject unknown parameters


class BaseTool(ABC):
    """Base class for all MCP tools."""

    def __init__(self, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager

    def get_client(self) -> VaultClient:
        """Get authenticated Vault client."""
        return self.auth_manager.get_client()

    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool. Must be implemented by subclasses."""
        pass

    async def __call__(self, **kwargs) -> Dict[str, Any]:
        """Call the tool with validation and error handling."""
        try:
            # Validate parameters
            params = self.parameter_class(**kwargs)

            # Log execution
            logger.info(
                "Tool execution started",
                tool=self.__class__.__name__,
                params=params.dict()
            )

            # Execute
            result = await self.execute(**params.dict())

            # Log success
            logger.info(
                "Tool execution completed",
                tool=self.__class__.__name__
            )

            return result

        except ValidationError as e:
            logger.error("Parameter validation failed", error=str(e))
            raise VaultMCPError(
                f"Invalid parameters: {e.errors()}",
                error_type="validation_error"
            )

        except VaultAPIError as e:
            logger.error("Vault API error", error=str(e))
            raise VaultMCPError(
                f"Vault API error: {e.message}",
                error_type="vault_api_error",
                original_error=e
            )

        except Exception as e:
            logger.exception("Unexpected error in tool execution")
            raise VaultMCPError(
                f"Unexpected error: {str(e)}",
                error_type="internal_error"
            )

    @property
    @abstractmethod
    def parameter_class(self):
        """Return the Pydantic model for parameters."""
        pass
```

### Example Tool Implementation

```python
# src/veevavault_mcp/tools/documents/query.py

from typing import List, Optional, Dict, Any
from pydantic import Field
import structlog

from ..base import BaseTool, ToolParameters
from ...utils.query_builder import build_document_vql
from ...utils.formatting import format_document_results

logger = structlog.get_logger(__name__)


class DocumentsQueryParameters(ToolParameters):
    """Parameters for documents_query tool."""

    vql: Optional[str] = Field(
        default=None,
        description="Raw VQL query (takes precedence over filters)"
    )
    name_contains: Optional[str] = Field(
        default=None,
        description="Filter by document name (partial match)"
    )
    document_type: Optional[str] = Field(
        default=None,
        description="Document type API name (e.g., 'protocol__c')"
    )
    lifecycle_state: Optional[str] = Field(
        default=None,
        description="Lifecycle state (e.g., 'approved__c')"
    )
    created_by: Optional[str] = Field(
        default=None,
        description="User ID who created the document"
    )
    created_after: Optional[str] = Field(
        default=None,
        description="ISO date string (e.g., '2025-01-01')"
    )
    modified_after: Optional[str] = Field(
        default=None,
        description="ISO date string"
    )
    limit: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum results to return (1-1000)"
    )
    return_format: str = Field(
        default="summary",
        description="Response format: 'summary', 'full', or 'ids_only'"
    )


class DocumentsQueryTool(BaseTool):
    """
    Query documents in Vault using VQL or common filter parameters.

    Use this tool to search for documents, list documents, or find specific
    documents matching criteria. You can either provide a raw VQL query or
    use the filter parameters.
    """

    parameter_class = DocumentsQueryParameters

    async def execute(
        self,
        vql: Optional[str] = None,
        name_contains: Optional[str] = None,
        document_type: Optional[str] = None,
        lifecycle_state: Optional[str] = None,
        created_by: Optional[str] = None,
        created_after: Optional[str] = None,
        modified_after: Optional[str] = None,
        limit: int = 100,
        return_format: str = "summary"
    ) -> Dict[str, Any]:
        """Execute document query."""

        client = self.get_client()

        # Build VQL if not provided
        if not vql:
            vql = build_document_vql(
                name_contains=name_contains,
                document_type=document_type,
                lifecycle_state=lifecycle_state,
                created_by=created_by,
                created_after=created_after,
                modified_after=modified_after,
                limit=limit
            )

        logger.info("Executing VQL query", vql=vql[:100])

        # Execute query via VeevaVault library
        from veevavault.services.queries import QueryService
        query_service = QueryService(client)

        results = query_service.query(vql)

        # Format results based on return_format
        formatted = format_document_results(results, return_format)

        return {
            "total": results.get("responseDetails", {}).get("total", 0),
            "returned": len(results.get("data", [])),
            "documents": formatted,
            "vql": vql  # Return VQL for transparency
        }


# Tool registration
def register_documents_query_tool(server, auth_manager):
    """Register documents_query tool with MCP server."""
    tool = DocumentsQueryTool(auth_manager)

    @server.tool(
        name="documents_query",
        description=DocumentsQueryTool.__doc__
    )
    async def documents_query(**kwargs):
        return await tool(**kwargs)
```

### Tool Registration System

```python
# src/veevavault_mcp/tools/__init__.py

from mcp.server import Server
from ..auth.manager import AuthenticationManager

from .documents.query import register_documents_query_tool
from .documents.create import register_documents_create_tool
from .documents.get import register_documents_get_tool
# ... import all tool registration functions


def register_all_tools(server: Server, auth_manager: AuthenticationManager):
    """Register all MCP tools with the server."""

    # Documents tools
    register_documents_query_tool(server, auth_manager)
    register_documents_create_tool(server, auth_manager)
    register_documents_get_tool(server, auth_manager)
    # ... register all document tools

    # Objects tools
    # ... register all object tools

    # VQL tools
    # ... register all VQL tools

    # And so on for all resources
```

---

## Resource Implementation Pattern

### MCP Resources for Browsing Vault Content

```python
# src/veevavault_mcp/resources/documents.py

from typing import List
from mcp.types import Resource, ResourceTemplate
import structlog

from ..auth.manager import AuthenticationManager

logger = structlog.get_logger(__name__)


class DocumentsResource:
    """MCP Resources for Vault documents."""

    def __init__(self, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager

    def get_templates(self) -> List[ResourceTemplate]:
        """Return resource templates for documents."""
        return [
            ResourceTemplate(
                uriTemplate="vault://documents/{document_id}",
                name="Vault Document",
                description="Access a specific Vault document by ID",
                mimeType="application/json"
            ),
            ResourceTemplate(
                uriTemplate="vault://documents/{document_id}/content",
                name="Vault Document Content",
                description="Access document file content",
                mimeType="application/octet-stream"
            )
        ]

    async def read_resource(self, uri: str) -> Resource:
        """Read a document resource."""

        if uri.startswith("vault://documents/") and "/content" not in uri:
            # Get document metadata
            document_id = uri.split("/")[-1]
            return await self._get_document_metadata(document_id)

        elif "/content" in uri:
            # Get document content
            document_id = uri.split("/")[-2]
            return await self._get_document_content(document_id)

        else:
            raise ValueError(f"Unknown resource URI: {uri}")

    async def _get_document_metadata(self, document_id: str) -> Resource:
        """Get document metadata as resource."""
        client = self.auth_manager.get_client()

        from veevavault.services.documents import DocumentService
        doc_service = DocumentService(client)

        metadata = doc_service.retrieval.retrieve_single_document(document_id)

        return Resource(
            uri=f"vault://documents/{document_id}",
            name=metadata.get("name", document_id),
            description=f"Document {document_id}",
            mimeType="application/json",
            text=str(metadata)  # JSON serialized metadata
        )

    async def _get_document_content(self, document_id: str) -> Resource:
        """Get document file content as resource."""
        client = self.auth_manager.get_client()

        from veevavault.services.documents import DocumentService
        doc_service = DocumentService(client)

        content = doc_service.retrieval.download_document_content(document_id)

        return Resource(
            uri=f"vault://documents/{document_id}/content",
            name=f"{document_id}_content",
            description=f"Content of document {document_id}",
            mimeType="application/octet-stream",
            blob=content  # Binary content
        )


def register_documents_resources(server, auth_manager):
    """Register document resources with MCP server."""
    resource_handler = DocumentsResource(auth_manager)

    # Register resource templates
    for template in resource_handler.get_templates():
        server.add_resource_template(template)

    # Register resource reader
    @server.read_resource()
    async def read_document_resource(uri: str):
        if uri.startswith("vault://documents/"):
            return await resource_handler.read_resource(uri)
```

---

## Authentication & Session Management

```python
# src/veevavault_mcp/auth/manager.py

import asyncio
from typing import Optional
from datetime import datetime, timedelta
import structlog

from veevavault import VaultClient
from ..config import Config
from ..utils.cache import Cache

logger = structlog.get_logger(__name__)


class AuthenticationManager:
    """Manages Vault authentication and session lifecycle."""

    def __init__(self, config: Config):
        self.config = config
        self._client: Optional[VaultClient] = None
        self._session_expires_at: Optional[datetime] = None
        self._lock = asyncio.Lock()
        self._cache = Cache(ttl=config.cache_ttl) if config.enable_caching else None

    async def authenticate(self):
        """Authenticate with Vault and create client."""
        async with self._lock:
            logger.info("Authenticating with Vault", url=self.config.vault_url)

            self._client = VaultClient(
                vault_url=self.config.vault_url,
                vault_username=self.config.vault_username,
                vault_password=self.config.vault_password
            )

            # Authenticate
            from veevavault.services.authentication import AuthenticationService
            auth_service = AuthenticationService(self._client)

            result = auth_service.authenticate(if_return=True)

            # Set session expiration (Vault sessions typically last 12 hours)
            self._session_expires_at = datetime.now() + timedelta(hours=11)

            logger.info(
                "Authentication successful",
                session_id=result["sessionId"][:10] + "...",
                vault_id=result["vaultId"]
            )

    async def ensure_authenticated(self):
        """Ensure we have a valid authenticated session."""
        if self._client is None:
            await self.authenticate()
            return

        # Check if session is expiring soon (refresh if < 30 min left)
        if self._session_expires_at:
            time_left = self._session_expires_at - datetime.now()
            if time_left < timedelta(minutes=30):
                logger.info("Session expiring soon, re-authenticating")
                await self.authenticate()

    def get_client(self) -> VaultClient:
        """Get authenticated Vault client."""
        if self._client is None:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        return self._client

    async def logout(self):
        """Logout and invalidate session."""
        if self._client:
            async with self._lock:
                logger.info("Logging out from Vault")

                from veevavault.services.authentication import AuthenticationService
                auth_service = AuthenticationService(self._client)
                auth_service.logout()

                self._client = None
                self._session_expires_at = None
```

---

## Error Handling Strategy

```python
# src/veevavault_mcp/utils/errors.py

from typing import Optional, Dict, Any


class VaultMCPError(Exception):
    """Base exception for all MCP server errors."""

    def __init__(
        self,
        message: str,
        error_type: str = "internal_error",
        original_error: Optional[Exception] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.original_error = original_error
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response."""
        return {
            "error": self.error_type,
            "message": self.message,
            "details": self.details
        }


class VaultAPIError(VaultMCPError):
    """Vault API returned an error."""

    def __init__(self, message: str, response=None, **kwargs):
        super().__init__(message, error_type="vault_api_error", **kwargs)
        self.response = response


class VaultAuthenticationError(VaultAPIError):
    """Authentication failed."""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type="authentication_error", **kwargs)


class VaultValidationError(VaultMCPError):
    """Parameter validation failed."""

    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_type="validation_error", **kwargs)


class VaultRateLimitError(VaultMCPError):
    """Rate limit exceeded."""

    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, error_type="rate_limit_error", **kwargs)
        self.retry_after = retry_after
```

### Retry Logic with Tenacity

```python
# src/veevavault_mcp/utils/retry.py

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import structlog

from .errors import VaultRateLimitError

logger = structlog.get_logger(__name__)


def vault_retry(func):
    """Decorator for retrying Vault API calls with exponential backoff."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(VaultRateLimitError),
        before_sleep=lambda retry_state: logger.warning(
            "Retrying after rate limit",
            attempt=retry_state.attempt_number
        )
    )
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)

    return wrapper
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_tools/test_documents_query.py

import pytest
from unittest.mock import Mock, AsyncMock, patch

from veevavault_mcp.tools.documents.query import DocumentsQueryTool, DocumentsQueryParameters


@pytest.fixture
def mock_auth_manager():
    """Mock authentication manager."""
    manager = Mock()
    manager.get_client.return_value = Mock()
    return manager


@pytest.fixture
def documents_query_tool(mock_auth_manager):
    """Create DocumentsQueryTool instance."""
    return DocumentsQueryTool(mock_auth_manager)


class TestDocumentsQueryTool:
    """Tests for documents_query tool."""

    def test_parameter_validation_success(self):
        """Test valid parameters pass validation."""
        params = DocumentsQueryParameters(
            name_contains="protocol",
            document_type="protocol__c",
            limit=50
        )
        assert params.name_contains == "protocol"
        assert params.limit == 50

    def test_parameter_validation_limit_too_high(self):
        """Test limit validation fails for > 1000."""
        with pytest.raises(ValueError):
            DocumentsQueryParameters(limit=1500)

    @pytest.mark.asyncio
    async def test_execute_with_filters(self, documents_query_tool):
        """Test executing query with filter parameters."""
        with patch("veevavault.services.queries.QueryService") as mock_query_service:
            # Mock query response
            mock_query_service.return_value.query.return_value = {
                "responseStatus": "SUCCESS",
                "data": [
                    {"id": "DOC-001", "name": "Test Doc"}
                ],
                "responseDetails": {"total": 1}
            }

            result = await documents_query_tool.execute(
                name_contains="test",
                limit=10
            )

            assert result["total"] == 1
            assert len(result["documents"]) == 1
            assert "vql" in result

    @pytest.mark.asyncio
    async def test_execute_with_raw_vql(self, documents_query_tool):
        """Test executing with raw VQL."""
        with patch("veevavault.services.queries.QueryService") as mock_query_service:
            mock_query_service.return_value.query.return_value = {
                "responseStatus": "SUCCESS",
                "data": [],
                "responseDetails": {"total": 0}
            }

            vql = "SELECT id, name FROM documents WHERE status__v='approved__v'"
            result = await documents_query_tool.execute(vql=vql)

            assert result["vql"] == vql
            assert result["total"] == 0
```

### Integration Tests

```python
# tests/integration/test_vault_integration.py

import pytest
import os
from dotenv import load_dotenv

from veevavault_mcp.config import Config
from veevavault_mcp.auth.manager import AuthenticationManager
from veevavault_mcp.tools.documents.query import DocumentsQueryTool

# Load test environment
load_dotenv(".env.test")


@pytest.fixture(scope="module")
async def auth_manager():
    """Create authenticated session for integration tests."""
    config = Config(
        vault_url=os.getenv("TEST_VAULT_URL"),
        vault_username=os.getenv("TEST_VAULT_USERNAME"),
        vault_password=os.getenv("TEST_VAULT_PASSWORD")
    )

    manager = AuthenticationManager(config)
    await manager.authenticate()

    yield manager

    await manager.logout()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_documents_query_integration(auth_manager):
    """Integration test for documents_query against real Vault."""
    tool = DocumentsQueryTool(auth_manager)

    result = await tool.execute(
        document_type="general_document__c",
        limit=5
    )

    assert "documents" in result
    assert result["total"] >= 0
    assert len(result["documents"]) <= 5
```

---

## Deployment Architecture

### Docker Container

```dockerfile
# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir .

# Copy source code
COPY src/ ./src/

# Create non-root user
RUN useradd -m -u 1000 mcp && chown -R mcp:mcp /app
USER mcp

# Set environment
ENV PYTHONUNBUFFERED=1
ENV VAULT_LOG_LEVEL=INFO

# Run MCP server
CMD ["python", "-m", "veevavault_mcp"]
```

### Docker Compose

```yaml
# docker-compose.yml

version: '3.8'

services:
  veevavault-mcp:
    build: .
    container_name: veevavault-mcp
    environment:
      - VAULT_URL=${VAULT_URL}
      - VAULT_USERNAME=${VAULT_USERNAME}
      - VAULT_PASSWORD=${VAULT_PASSWORD}
      - VAULT_LOG_LEVEL=INFO
      - VAULT_ENABLE_CACHING=true
      - VAULT_CACHE_TTL=300
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - vault-network

  # Optional: Redis for distributed caching
  redis:
    image: redis:7-alpine
    container_name: vault-mcp-redis
    volumes:
      - redis-data:/data
    networks:
      - vault-network

volumes:
  redis-data:

networks:
  vault-network:
    driver: bridge
```

---

## Performance Optimization

### Caching Strategy

```python
# src/veevavault_mcp/utils/cache.py

from typing import Optional, Any
import hashlib
import json
from datetime import datetime, timedelta


class Cache:
    """Simple in-memory cache with TTL."""

    def __init__(self, ttl: int = 300):
        self.ttl = ttl  # seconds
        self._cache: dict = {}

    def _make_key(self, func_name: str, **kwargs) -> str:
        """Generate cache key from function name and parameters."""
        params_str = json.dumps(kwargs, sort_keys=True)
        return hashlib.md5(f"{func_name}:{params_str}".encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key in self._cache:
            value, expires_at = self._cache[key]
            if datetime.now() < expires_at:
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any):
        """Set cached value with TTL."""
        expires_at = datetime.now() + timedelta(seconds=self.ttl)
        self._cache[key] = (value, expires_at)

    def clear(self):
        """Clear all cached values."""
        self._cache.clear()


def cached(cache: Cache):
    """Decorator to cache function results."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = cache._make_key(func.__name__, **kwargs)

            # Check cache
            cached_result = cache.get(key)
            if cached_result is not None:
                return cached_result

            # Execute and cache
            result = await func(*args, **kwargs)
            cache.set(key, result)

            return result
        return wrapper
    return decorator
```

---

## Security Considerations

### Credential Management

```bash
# .env file (never commit!)

VAULT_URL=https://your-vault.veevavault.com
VAULT_USERNAME=your-username
VAULT_PASSWORD=your-password

# Or use OAuth2
VAULT_CLIENT_ID=your-client-id
VAULT_CLIENT_SECRET=your-client-secret

# Optionally use secrets manager
VAULT_USE_SECRETS_MANAGER=true
VAULT_SECRETS_PATH=/vault/credentials
```

### Audit Logging

```python
# All tool executions are logged with:
# - Tool name
# - Parameters (sanitized - no passwords)
# - Execution time
# - User context
# - Result status

logger.info(
    "Tool execution",
    tool="documents_query",
    params={"name_contains": "protocol", "limit": 10},
    duration_ms=245,
    result_count=5,
    user="john.smith@company.com"
)
```

---

## Development Workflow

### Setup Development Environment

```bash
# 1. Clone repository
git clone <repo-url>
cd veevavault-mcp-server

# 2. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Setup pre-commit hooks
pre-commit install

# 5. Copy environment template
cp .env.example .env
# Edit .env with your Vault credentials

# 6. Run tests
pytest

# 7. Run server locally
python -m veevavault_mcp
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/ci.yml

name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -e ".[dev]"

    - name: Run linting
      run: |
        ruff check .
        black --check .

    - name: Run type checking
      run: mypy src/

    - name: Run tests
      run: pytest --cov=veevavault_mcp --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

---

## Phase 1 Implementation Details

### Week 1-2: Foundation

**Tasks:**
1. ✅ Project structure setup
2. ✅ Configuration management
3. ✅ Authentication manager
4. ✅ Base tool class
5. ✅ Error handling framework
6. ✅ Unit test framework

**Deliverable:** Working MCP server that can authenticate with Vault

### Week 3: Documents Resource (Part 1)

**Tools to implement:**
1. `documents_query` - Search/filter documents
2. `documents_get` - Retrieve single document
3. `documents_create` - Create new document
4. `documents_update` - Update document metadata

**Deliverable:** Basic document operations working

### Week 4: Documents Resource (Part 2)

**Tools to implement:**
5. `documents_delete` - Delete document
6. `documents_upload_content` - Upload file content
7. `documents_download_content` - Download file
8. `documents_lock` / `documents_unlock` - Lock management
9. `documents_manage_lifecycle` - Lifecycle operations

**Deliverable:** Complete document resource

### Week 5: Objects & VQL Resources

**Objects tools:**
1. `objects_query` - Query object records
2. `objects_get` - Get single record
3. `objects_create` - Create record
4. `objects_update` - Update record
5. `objects_delete` - Delete record

**VQL tools:**
1. `vql_execute` - Execute VQL query
2. `vql_bulk_export` - Large dataset export

**Deliverable:** Phase 1 complete - 30 tools serving 60% of users

---

## Next Steps

1. **Review & Approve** - Review this technical plan
2. **Environment Setup** - Set up development environment
3. **Week 1 Start** - Begin foundation implementation
4. **Daily Standups** - Track progress against roadmap

**Questions to Discuss:**
- Preferred deployment: Docker vs. Kubernetes vs. serverless?
- Redis for caching: needed for MVP or later?
- Monitoring: Prometheus metrics from day 1 or later?
- CI/CD: GitHub Actions sufficient or need something else?

---

**STATUS:** Ready to begin implementation! 🚀
