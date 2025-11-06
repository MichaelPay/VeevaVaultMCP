"""
Custom exception classes for VeevaVaultMCP.

These exceptions provide more granular error handling and better error messages
for Vault API interactions.
"""


class VaultAPIError(Exception):
    """
    Base exception for all Vault API errors.

    Attributes:
        message (str): Human-readable error message
        response: The requests.Response object (if available)
        status_code (int): HTTP status code (if available)
        vault_errors (list): List of Vault-specific error details from response
    """

    def __init__(self, message, response=None):
        """
        Initialize VaultAPIError.

        Args:
            message (str): Error message
            response (requests.Response, optional): HTTP response object
        """
        super().__init__(message)
        self.message = message
        self.response = response
        self.status_code = response.status_code if response else None
        self.vault_errors = []

        # Try to extract Vault-specific errors from response
        if response is not None:
            try:
                response_data = response.json()
                if isinstance(response_data, dict):
                    # Check for errors array
                    if "errors" in response_data:
                        self.vault_errors = response_data["errors"]
                    # Check for single error
                    elif "error" in response_data:
                        self.vault_errors = [response_data["error"]]
            except (ValueError, AttributeError):
                # Response is not JSON or doesn't have json() method
                pass

    def __str__(self):
        """Return string representation of the error."""
        error_parts = [self.message]

        if self.status_code:
            error_parts.append(f"Status Code: {self.status_code}")

        if self.vault_errors:
            error_details = "; ".join(str(e) for e in self.vault_errors)
            error_parts.append(f"Vault Errors: {error_details}")

        return " | ".join(error_parts)


class VaultAuthenticationError(VaultAPIError):
    """Raised when authentication fails."""
    pass


class VaultNotFoundError(VaultAPIError):
    """Raised when a requested resource is not found (404)."""
    pass


class VaultPermissionError(VaultAPIError):
    """Raised when the user lacks permission for an operation (403)."""
    pass


class VaultValidationError(VaultAPIError):
    """Raised when request validation fails (400)."""
    pass


class VaultServerError(VaultAPIError):
    """Raised when the server encounters an error (5xx)."""
    pass


class VaultRateLimitError(VaultAPIError):
    """Raised when API rate limit is exceeded (429)."""
    pass


class VaultQueryError(VaultAPIError):
    """Raised when a VQL query fails or returns an error."""
    pass


class VaultSessionError(VaultAPIError):
    """Raised when session is invalid or expired."""
    pass
