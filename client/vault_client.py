from urllib.parse import urlparse
import requests
from typing import Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)


class VaultClient:
    """
    Core client for interacting with the Veeva Vault API.
    This class handles basic API communication while delegating authentication to AuthenticationService.
    """

    def __init__(self):
        self.vaultURL = None
        self.vaultUserName = None
        self.vaultPassword = None
        self.vaultConnection = None
        self.sessionId = None
        self.vaultId = None
        self.vaultDNS = None
        self.APIheaders = None
        self.APIversionList = []
        self.LatestAPIversion = "v25.2"

        # Property alias for service classes that expect session_id vs sessionId
        self._session_id = None

    @property
    def session_id(self):
        """
        Getter for session_id property that returns sessionId
        """
        return self.sessionId

    @session_id.setter
    def session_id(self, value):
        """
        Setter for session_id property that updates both sessionId and _session_id
        """
        self.sessionId = value
        self._session_id = value

    def api_call(
        self,
        endpoint: str,
        method: str = "GET",
        data: Any = None,
        params: Dict = None,
        headers: Dict = None,
        files: Dict = None,
        json: Any = None,
        raw_response: bool = False,
        **kwargs,
    ) -> Union[Dict[str, Any], requests.Response]:
        """
        This function is used to make API calls to the Veeva Vault API. It is a wrapper around the requests library.

        Args:
            endpoint: API endpoint to call
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Dictionary, list of tuples, bytes, or file-like object to send in the body
            params: Dictionary or bytes to be sent in the query string
            headers: Dictionary of HTTP headers to send with the request
            files: Dictionary of file-like objects for multipart encoding upload
            json: JSON data to send in the body
            raw_response: Whether to return the raw response object instead of parsed JSON
            kwargs: Additional arguments for requests.request

        Returns:
            Either a JSON parsed dictionary or the raw response object if raw_response is True

        Raises:
            VaultAuthenticationError: For 401 authentication errors
            VaultPermissionError: For 403 permission errors
            VaultNotFoundError: For 404 not found errors
            VaultValidationError: For 400 validation errors
            VaultRateLimitError: For 429 rate limit errors
            VaultServerError: For 5xx server errors
            VaultAPIError: For other API errors
        """
        if headers is None:
            headers = {}

        # Add default headers if not already provided
        if "Accept" not in headers:
            headers["Accept"] = "application/json"
        if "Authorization" not in headers and self.sessionId:
            headers["Authorization"] = f"{self.sessionId}"

        # Construct the full URL - handle both absolute and relative paths
        if endpoint.startswith(("http://", "https://")):
            api_url = endpoint
        else:
            baseUrl = self.vaultURL.rstrip("/")
            # Make sure we don't have double slashes
            clean_endpoint = endpoint.lstrip("/")
            api_url = f"{baseUrl}/{clean_endpoint}"

        # Import exceptions here to avoid circular imports
        from veevavault.exceptions import (
            VaultAPIError,
            VaultAuthenticationError,
            VaultPermissionError,
            VaultNotFoundError,
            VaultValidationError,
            VaultRateLimitError,
            VaultServerError,
            VaultSessionError,
        )

        try:
            logger.debug(f"{method} {api_url}")
            response = requests.request(
                method=method,
                url=api_url,
                headers=headers,
                params=params,
                data=data,
                files=files,
                json=json,
                **kwargs,
            )

            # Check for specific HTTP status codes and raise appropriate exceptions
            if response.status_code == 401:
                error_msg = f"Authentication failed"
                try:
                    error_data = response.json()
                    if "errors" in error_data:
                        error_msg += f": {error_data['errors']}"
                except:
                    error_msg += f": {response.text}"
                logger.error(error_msg)
                raise VaultAuthenticationError(error_msg, response=response)

            elif response.status_code == 403:
                error_msg = f"Permission denied"
                try:
                    error_data = response.json()
                    if "errors" in error_data:
                        error_msg += f": {error_data['errors']}"
                except:
                    error_msg += f": {response.text}"
                logger.error(error_msg)
                raise VaultPermissionError(error_msg, response=response)

            elif response.status_code == 404:
                error_msg = f"Resource not found: {api_url}"
                logger.error(error_msg)
                raise VaultNotFoundError(error_msg, response=response)

            elif response.status_code == 400:
                error_msg = f"Validation error"
                try:
                    error_data = response.json()
                    if "errors" in error_data:
                        error_msg += f": {error_data['errors']}"
                except:
                    error_msg += f": {response.text}"
                logger.error(error_msg)
                raise VaultValidationError(error_msg, response=response)

            elif response.status_code == 429:
                error_msg = f"Rate limit exceeded"
                logger.error(error_msg)
                raise VaultRateLimitError(error_msg, response=response)

            elif response.status_code >= 500:
                error_msg = f"Server error: {response.status_code}"
                logger.error(error_msg)
                raise VaultServerError(error_msg, response=response)

            # For any other error status
            response.raise_for_status()

            # Check for INVALID_SESSION_ID in successful response
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict) and "errors" in response_data:
                        for error in response_data["errors"]:
                            if isinstance(error, dict) and error.get("type") == "INVALID_SESSION_ID":
                                error_msg = "Session ID is invalid or expired"
                                logger.error(error_msg)
                                raise VaultSessionError(error_msg, response=response)
                except (ValueError, AttributeError):
                    # Response is not JSON, continue
                    pass

            if raw_response:
                logger.debug(f"Response: {response.status_code}")
                return response

            logger.debug(f"Response: {response.status_code} - Success")
            return response.json()  # Return JSON response

        except requests.exceptions.HTTPError as http_err:
            # This catches any HTTP errors not handled above
            error_msg = f"HTTP error occurred: {http_err}"
            if hasattr(http_err, "response") and http_err.response is not None:
                try:
                    error_data = http_err.response.json()
                    error_msg += f" | Response: {error_data}"
                except:
                    error_msg += f" | Response: {http_err.response.text}"
            logger.error(error_msg)
            raise VaultAPIError(error_msg, response=http_err.response) from http_err

        except requests.exceptions.RequestException as req_err:
            # This catches connection errors, timeouts, etc.
            error_msg = f"Request error occurred: {req_err}"
            logger.error(error_msg)
            raise VaultAPIError(error_msg) from req_err

        except Exception as err:
            # This catches any other unexpected errors
            error_msg = f"Unexpected error occurred: {err}"
            logger.error(error_msg)
            raise VaultAPIError(error_msg) from err

    def authenticate(
        self,
        vaultURL=None,
        vaultUserName=None,
        vaultPassword=None,
        sessionId=None,
        vaultId=None,
        if_return=False,
        *args,
        **kwargs,
    ):
        """
        Authenticate with the Veeva Vault API.
        This method is a stub that delegates to AuthenticationService.
        It's maintained here for backward compatibility.

        Args:
            vaultURL: URL of the Vault instance
            vaultUserName: User name for authentication
            vaultPassword: Password for authentication
            sessionId: Existing session ID (optional)
            vaultId: Vault ID (optional)
            if_return: Whether to return authentication details

        Returns:
            dict: Authentication details if if_return is True, otherwise None
        """
        # This is a stub that will be implemented by the AuthenticationService
        # We have to import inline to avoid circular imports
        from veevavault.services.authentication import AuthenticationService

        auth_service = AuthenticationService(self)
        return auth_service.authenticate(
            vaultURL=vaultURL,
            vaultUserName=vaultUserName,
            vaultPassword=vaultPassword,
            sessionId=sessionId,
            vaultId=vaultId,
            if_return=if_return,
            *args,
            **kwargs,
        )

    def validate_session_user(
        self,
        exclude_vault_membership: bool = False,
        exclude_app_licensing: bool = False,
    ) -> Dict[str, Any]:
        """
        Given a valid session ID, this request returns information for the currently authenticated user.
        In case of an invalid session ID, it returns an INVALID_SESSION_ID error.

        Args:
            exclude_vault_membership: If set to true, vault_membership fields are omitted from the response
            exclude_app_licensing: If set to true, app_licensing fields are omitted from the response

        Returns:
            Information of the currently authenticated user or an error message for invalid session ID
        """
        url = f"{self.vaultURL}/api/{self.LatestAPIversion}/objects/users/me"

        headers = {"Accept": "application/json", "Authorization": self.sessionId}

        params = {
            "exclude_vault_membership": str(exclude_vault_membership).lower(),
            "exclude_app_licensing": str(exclude_app_licensing).lower(),
        }

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def session_keep_alive(self) -> Dict[str, Any]:
        """
        Given an active sessionId, keep the session active by refreshing the session duration.
        This is a stub method that delegates to AuthenticationService.keep_alive().

        Returns:
            dict: Response from the API call indicating the success status.
        """
        # Import inline to avoid circular imports
        from veevavault.services.authentication import AuthenticationService

        auth_service = AuthenticationService(self)
        return auth_service.keep_alive()
