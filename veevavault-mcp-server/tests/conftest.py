"""
Pytest configuration and shared fixtures for VeevaVault MCP Server tests.
"""

import os
from typing import Generator
import pytest
from unittest.mock import MagicMock, patch

from veevavault_mcp.config import Config, AuthMode


@pytest.fixture
def mock_env_username_password(monkeypatch) -> None:
    """Mock environment variables for username/password auth mode."""
    monkeypatch.setenv("VAULT_AUTH_MODE", "username_password")
    monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
    monkeypatch.setenv("VAULT_USERNAME", "test.user@example.com")
    monkeypatch.setenv("VAULT_PASSWORD", "TestPassword123")
    monkeypatch.setenv("VAULT_ENABLE_CACHING", "true")
    monkeypatch.setenv("VAULT_CACHE_BACKEND", "memory")
    monkeypatch.setenv("VAULT_LOG_LEVEL", "DEBUG")


@pytest.fixture
def mock_env_oauth2(monkeypatch) -> None:
    """Mock environment variables for OAuth2 auth mode."""
    monkeypatch.setenv("VAULT_AUTH_MODE", "oauth2")
    monkeypatch.setenv("VAULT_URL", "https://test-vault.veevavault.com")
    monkeypatch.setenv("VAULT_OAUTH2_TOKEN_URL", "https://auth.example.com/oauth/token")
    monkeypatch.setenv("VAULT_OAUTH2_JWKS_URL", "https://auth.example.com/.well-known/jwks.json")
    monkeypatch.setenv("VAULT_OAUTH2_AUDIENCE", "vault-mcp-server")
    monkeypatch.setenv("VAULT_SERVICE_ACCOUNT_USERNAME", "service-bot@example.com")
    monkeypatch.setenv("VAULT_SERVICE_ACCOUNT_PASSWORD", "ServicePassword123")


@pytest.fixture
def config_username_password(mock_env_username_password) -> Config:
    """Create Config instance with username/password auth."""
    return Config()


@pytest.fixture
def config_oauth2(mock_env_oauth2) -> Config:
    """Create Config instance with OAuth2 auth."""
    return Config()


@pytest.fixture
def mock_vault_session() -> Generator[MagicMock, None, None]:
    """Mock Vault API session."""
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance

        # Mock successful authentication response
        mock_instance.post.return_value.json.return_value = {
            "responseStatus": "SUCCESS",
            "sessionId": "test-session-id-12345",
            "userId": 12345,
            "vaultIds": [{"id": 1234, "name": "Test Vault"}]
        }

        yield mock_instance


@pytest.fixture
def mock_document_response() -> dict:
    """Mock Veeva Vault document API response."""
    return {
        "responseStatus": "SUCCESS",
        "responseDetails": {
            "pageOffset": 0,
            "pageSize": 50,
            "total": 1
        },
        "documents": [
            {
                "id": 123,
                "name__v": "Test Document",
                "title__v": "Test Document Title",
                "type__v": "protocol__c",
                "subtype__v": "clinical_study_protocol__c",
                "classification__v": "clinical__c",
                "lifecycle__v": "clinical_document_lifecycle__c",
                "status__v": "draft__c",
                "study_number__c": "ABC-123",
                "therapeutic_area__c": "Oncology",
                "version_created_by__v": 12345,
                "version_creation_date__v": "2025-11-01T10:00:00Z"
            }
        ]
    }


@pytest.fixture
def mock_object_response() -> dict:
    """Mock Veeva Vault object API response."""
    return {
        "responseStatus": "SUCCESS",
        "data": [
            {
                "id": "V0C000000001001",
                "name__v": "Test Quality Event",
                "status__v": "open__c",
                "event_type__c": "deviation__c",
                "severity__c": "major__c",
                "created_date__v": "2025-11-01T10:00:00Z",
                "created_by__v": 12345
            }
        ]
    }


@pytest.fixture
def mock_vql_response() -> dict:
    """Mock Veeva Vault VQL query response."""
    return {
        "responseStatus": "SUCCESS",
        "responseDetails": {
            "pagesize": 1000,
            "pageOffset": 0,
            "total": 2
        },
        "data": [
            {
                "id": 123,
                "name__v": "Document 1",
                "type__v": "protocol__c"
            },
            {
                "id": 124,
                "name__v": "Document 2",
                "type__v": "informed_consent__c"
            }
        ]
    }


@pytest.fixture(autouse=True)
def reset_env():
    """Reset environment variables after each test."""
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)
