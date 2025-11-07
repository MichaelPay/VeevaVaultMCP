"""
VQL (Vault Query Language) execution tools.
"""

from typing import Optional
from .base import BaseTool, ToolResult
from ..utils.errors import APIError


class VQLExecuteTool(BaseTool):
    """Execute arbitrary VQL queries against Veeva Vault."""

    @property
    def name(self) -> str:
        return "vault_vql_execute"

    @property
    def description(self) -> str:
        return """Execute a VQL (Vault Query Language) query.

VQL is SQL-like query language for Vault data.

Examples:
- SELECT id, name__v FROM documents WHERE type__v = 'protocol__c'
- SELECT id, name__v, status__v FROM product__v WHERE active__v = true
- SELECT id, title__v FROM documents WHERE created_date__v >= '2025-01-01'

Power user feature for complex queries.
Use specific tools (documents_query, objects_query) for simple queries."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The VQL query to execute",
                },
                "limit": {
                    "type": "integer",
                    "description": "Override LIMIT in query (optional)",
                    "minimum": 1,
                    "maximum": 10000,
                },
            },
            "required": ["query"],
        }

    async def execute(self, query: str, limit: Optional[int] = None) -> ToolResult:
        """Execute VQL query."""
        try:
            headers = await self._get_auth_headers()

            # Optionally add/override LIMIT
            query_to_execute = query
            if limit:
                # Simple limit override - remove existing LIMIT if present
                import re

                query_to_execute = re.sub(
                    r"\s+LIMIT\s+\d+", "", query, flags=re.IGNORECASE
                )
                query_to_execute += f" LIMIT {limit}"

            # Execute query
            path = self._build_api_path("/query")
            params = {"q": query_to_execute}

            response = await self.http_client.get(
                path=path,
                headers=headers,
                params=params,
            )

            # Extract results
            data = response.get("data", [])
            response_details = response.get("responseDetails", {})

            self.logger.info(
                "vql_executed",
                query_length=len(query),
                result_count=len(data),
            )

            return ToolResult(
                success=True,
                data={
                    "results": data,
                    "count": len(data),
                    "query": query_to_execute,
                    "response_details": response_details,
                },
                metadata={
                    "result_count": len(data),
                    "query_type": "vql",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"VQL query failed: {e.message}",
                metadata={"error_code": e.error_code, "query": query},
            )


class VQLValidateTool(BaseTool):
    """Validate VQL query syntax without executing it."""

    @property
    def name(self) -> str:
        return "vault_vql_validate"

    @property
    def description(self) -> str:
        return """Validate VQL query syntax without executing.

Useful for:
- Checking query syntax before execution
- Learning VQL
- Debugging complex queries

Returns validation errors if syntax is incorrect."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The VQL query to validate",
                },
            },
            "required": ["query"],
        }

    async def execute(self, query: str) -> ToolResult:
        """Execute VQL validation."""
        try:
            headers = await self._get_auth_headers()

            # Vault API doesn't have a dedicated validate endpoint,
            # so we use LIMIT 0 to validate without returning results
            validation_query = query
            import re

            # Remove existing LIMIT
            validation_query = re.sub(
                r"\s+LIMIT\s+\d+", "", validation_query, flags=re.IGNORECASE
            )
            validation_query += " LIMIT 0"

            path = self._build_api_path("/query")
            params = {"q": validation_query}

            response = await self.http_client.get(
                path=path,
                headers=headers,
                params=params,
            )

            self.logger.info("vql_validated", query_length=len(query))

            return ToolResult(
                success=True,
                data={
                    "valid": True,
                    "query": query,
                    "message": "Query syntax is valid",
                },
                metadata={"validation": "passed"},
            )

        except APIError as e:
            # Validation failed - query has syntax errors
            self.logger.warning(
                "vql_validation_failed",
                query=query[:100],
                error=e.message,
            )

            return ToolResult(
                success=False,
                error=f"Query validation failed: {e.message}",
                data={
                    "valid": False,
                    "query": query,
                    "error": e.message,
                },
                metadata={"validation": "failed", "error_code": e.error_code},
            )
