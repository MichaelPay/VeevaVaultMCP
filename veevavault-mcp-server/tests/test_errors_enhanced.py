"""
Tests for enhanced error handling.
"""

import pytest
from veevavault_mcp.utils.errors import (
    QuerySyntaxError,
    FieldNotFoundError,
    StateError,
    SessionExpiredError,
    NetworkError,
    create_error_from_response,
    RateLimitError,
    ValidationError,
    AuthorizationError,
    APIError,
)


class TestEnhancedErrorClasses:
    """Tests for enhanced error classes."""

    def test_query_syntax_error(self):
        """Test QuerySyntaxError creation."""
        error = QuerySyntaxError(message="Invalid VQL syntax")
        assert error.message == "Invalid VQL syntax"
        assert error.error_code == "MALFORMED_URL"
        assert "MALFORMED_URL" in str(error)
        assert isinstance(error, QuerySyntaxError)

    def test_field_not_found_error(self):
        """Test FieldNotFoundError creation."""
        error = FieldNotFoundError(message="Field does not exist")
        assert error.message == "Field does not exist"
        assert error.error_code == "ATTRIBUTE_NOT_SUPPORTED"

    def test_state_error(self):
        """Test StateError creation."""
        error = StateError(message="Cannot perform action in current state")
        assert error.message == "Cannot perform action in current state"
        assert error.error_code == "OPERATION_NOT_ALLOWED"

    def test_session_expired_error(self):
        """Test SessionExpiredError creation."""
        error = SessionExpiredError()
        assert error.message == "Session expired"
        assert error.error_code == "SESSION_EXPIRED"

    def test_network_error(self):
        """Test NetworkError creation."""
        error = NetworkError(message="Connection failed")
        assert error.message == "Connection failed"
        assert error.error_code == "NETWORK_ERROR"


class TestErrorMapping:
    """Tests for error mapping from API responses."""

    def test_map_query_syntax_error(self):
        """Test mapping MALFORMED_URL to QuerySyntaxError."""
        response = {
            "responseStatus": "FAILURE",
            "errors": [
                {"type": "MALFORMED_URL", "message": "Invalid query syntax"}
            ],
        }

        error = create_error_from_response(response)
        assert isinstance(error, QuerySyntaxError)
        assert error.message == "Invalid query syntax"
        assert error.error_code == "MALFORMED_URL"

    def test_map_field_not_found_error(self):
        """Test mapping ATTRIBUTE_NOT_SUPPORTED to FieldNotFoundError."""
        response = {
            "responseStatus": "FAILURE",
            "errors": [
                {"type": "ATTRIBUTE_NOT_SUPPORTED", "message": "Field not found"}
            ],
        }

        error = create_error_from_response(response)
        assert isinstance(error, FieldNotFoundError)
        assert error.message == "Field not found"

    def test_map_state_error(self):
        """Test mapping OPERATION_NOT_ALLOWED to StateError."""
        response = {
            "responseStatus": "FAILURE",
            "errors": [
                {"type": "OPERATION_NOT_ALLOWED", "message": "Invalid state"}
            ],
        }

        error = create_error_from_response(response)
        assert isinstance(error, StateError)

    def test_map_session_expired_error(self):
        """Test mapping INVALID_SESSION_ID to SessionExpiredError."""
        response = {
            "responseStatus": "FAILURE",
            "errors": [
                {"type": "INVALID_SESSION_ID", "message": "Session expired"}
            ],
        }

        error = create_error_from_response(response)
        assert isinstance(error, SessionExpiredError)

    def test_map_authorization_error(self):
        """Test mapping NO_PERMISSION to AuthorizationError."""
        response = {
            "responseStatus": "FAILURE",
            "errors": [
                {"type": "NO_PERMISSION", "message": "Access denied"}
            ],
        }

        error = create_error_from_response(response)
        assert isinstance(error, AuthorizationError)

    def test_map_validation_error(self):
        """Test mapping INVALID_DATA to ValidationError."""
        response = {
            "responseStatus": "FAILURE",
            "errors": [
                {"type": "INVALID_DATA", "message": "Invalid input"}
            ],
        }

        error = create_error_from_response(response)
        assert isinstance(error, ValidationError)

    def test_map_rate_limit_error(self):
        """Test mapping RATE_LIMIT_EXCEEDED to RateLimitError."""
        response = {
            "responseStatus": "FAILURE",
            "errors": [
                {"type": "RATE_LIMIT_EXCEEDED", "message": "Too many requests"}
            ],
            "retry_after": 60,
        }

        error = create_error_from_response(response)
        assert isinstance(error, RateLimitError)
        assert error.retry_after == 60

    def test_map_unknown_error_to_api_error(self):
        """Test mapping unknown error code to APIError."""
        response = {
            "responseStatus": "FAILURE",
            "errors": [
                {"type": "UNKNOWN_ERROR", "message": "Something went wrong"}
            ],
        }

        error = create_error_from_response(response, status_code=500)
        assert isinstance(error, APIError)
        assert error.message == "Something went wrong"
        assert error.status_code == 500

    def test_error_mapping_with_response_message(self):
        """Test error extraction from responseMessage."""
        response = {
            "responseStatus": "FAILURE",
            "responseMessage": "General error message",
            "errors": [],
        }

        error = create_error_from_response(response)
        assert error.message == "General error message"

    def test_error_mapping_with_context(self):
        """Test error includes context."""
        response = {
            "responseStatus": "FAILURE",
            "errors": [
                {"type": "INVALID_DATA", "message": "Bad request"}
            ],
        }

        error = create_error_from_response(response, status_code=400)
        assert error.context["response_status"] == "FAILURE"
        assert error.context["status_code"] == 400
        assert len(error.context["errors"]) == 1
