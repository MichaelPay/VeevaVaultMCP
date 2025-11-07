"""
HTTP client utilities for Veeva Vault API.
"""

from typing import Any, Optional
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import structlog

from .errors import APIError, RateLimitError, TimeoutError

logger = structlog.get_logger(__name__)


class VaultHTTPClient:
    """
    HTTP client for Veeva Vault API with retry logic and error handling.
    """

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        """
        Initialize HTTP client.

        Args:
            base_url: Base URL for Veeva Vault (e.g., https://vault.veevavault.com)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logger.bind(base_url=base_url)

        # Create async HTTP client
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)),
        reraise=True,
    )
    async def request(
        self,
        method: str,
        path: str,
        headers: Optional[dict[str, str]] = None,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Make HTTP request to Vault API with retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API path (e.g., /api/v25.2/auth)
            headers: Optional HTTP headers
            json: Optional JSON body
            params: Optional query parameters
            data: Optional form data

        Returns:
            Parsed JSON response

        Raises:
            APIError: If API returns error response
            RateLimitError: If rate limit exceeded
            TimeoutError: If request times out
        """
        if self._client is None:
            raise RuntimeError("Client not initialized. Use 'async with' context manager.")

        url = path if path.startswith("http") else path
        request_headers = headers or {}

        self.logger.debug(
            "http_request",
            method=method,
            path=path,
            has_json=json is not None,
            has_data=data is not None,
        )

        try:
            response = await self._client.request(
                method=method,
                url=url,
                headers=request_headers,
                json=json,
                params=params,
                data=data,
            )

            # Log response
            self.logger.debug(
                "http_response",
                status_code=response.status_code,
                path=path,
            )

            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 60))
                raise RateLimitError(
                    message="API rate limit exceeded",
                    retry_after=retry_after,
                    context={"path": path, "method": method},
                )

            # Parse JSON response
            try:
                response_data = response.json()
            except Exception:
                response_data = {"response": response.text}

            # Handle error responses
            if response.status_code >= 400:
                error_message = self._extract_error_message(response_data)
                raise APIError(
                    message=error_message,
                    status_code=response.status_code,
                    response_data=response_data,
                    context={"path": path, "method": method},
                )

            # Check for Vault API error in successful HTTP response
            if isinstance(response_data, dict):
                response_status = response_data.get("responseStatus")
                if response_status == "FAILURE":
                    error_message = self._extract_error_message(response_data)
                    error_type = response_data.get("errors", [{}])[0].get("type", "API_ERROR")
                    raise APIError(
                        message=error_message,
                        error_code=error_type,
                        status_code=response.status_code,
                        response_data=response_data,
                        context={"path": path, "method": method},
                    )

            return response_data

        except httpx.TimeoutException as e:
            self.logger.error("http_timeout", path=path, error=str(e))
            raise TimeoutError(
                message=f"Request to {path} timed out",
                context={"path": path, "timeout": self.timeout},
            )

        except (httpx.ConnectError, httpx.NetworkError) as e:
            self.logger.error("http_network_error", path=path, error=str(e))
            raise APIError(
                message=f"Network error: {str(e)}",
                context={"path": path},
            )

    def _extract_error_message(self, response_data: dict) -> str:
        """Extract error message from Vault API response."""
        # Try to get error message from errors array
        if "errors" in response_data and response_data["errors"]:
            first_error = response_data["errors"][0]
            return first_error.get("message", "Unknown API error")

        # Try to get from responseMessage
        if "responseMessage" in response_data:
            return response_data["responseMessage"]

        # Fallback
        return "Unknown API error"

    async def get(self, path: str, **kwargs) -> dict[str, Any]:
        """Make GET request."""
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> dict[str, Any]:
        """Make POST request."""
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs) -> dict[str, Any]:
        """Make PUT request."""
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs) -> dict[str, Any]:
        """Make DELETE request."""
        return await self.request("DELETE", path, **kwargs)
