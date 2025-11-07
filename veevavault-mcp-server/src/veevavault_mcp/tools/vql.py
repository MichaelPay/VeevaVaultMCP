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
                "auto_paginate": {
                    "type": "boolean",
                    "description": "Automatically fetch all pages (default: false)",
                    "default": False,
                },
            },
            "required": ["query"],
        }

    async def execute(
        self, query: str, limit: Optional[int] = None, auto_paginate: bool = False
    ) -> ToolResult:
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

            # Execute query using POST (required by Vault API)
            path = self._build_api_path("/query")

            # Add Content-Type header for form-encoded data
            query_headers = {
                **headers,
                "Content-Type": "application/x-www-form-urlencoded",
            }

            response = await self.http_client.post(
                path=path,
                headers=query_headers,
                data={"q": query_to_execute},
            )

            # Extract results
            data = response.get("data", [])
            response_details = response.get("responseDetails", {})

            # Parse pagination metadata
            pagesize = response.get("pagesize", limit if limit else 100)
            total = response.get("total", len(data))
            next_page = response.get("next_page")

            # Auto-paginate if requested
            pages_fetched = 1
            if auto_paginate and next_page:
                while next_page:
                    page_response = await self.http_client.post(
                        path=next_page,
                        headers=query_headers,
                        data={},
                    )
                    page_data = page_response.get("data", [])
                    data.extend(page_data)
                    pages_fetched += 1
                    next_page = page_response.get("next_page")

            self.logger.info(
                "vql_executed",
                query_length=len(query),
                result_count=len(data),
                total_available=total,
                pages_fetched=pages_fetched,
            )

            return ToolResult(
                success=True,
                data={
                    "results": data,
                    "count": len(data),
                    "total": total,
                    "query": query_to_execute,
                    "response_details": response_details,
                    "pagination": {
                        "pagesize": pagesize,
                        "pages_fetched": pages_fetched,
                        "total_available": total,
                        "is_complete": auto_paginate or len(data) >= total,
                    },
                },
                metadata={
                    "result_count": len(data),
                    "query_type": "vql",
                    "auto_paginate": auto_paginate,
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

            # Execute validation query using POST (required by Vault API)
            path = self._build_api_path("/query")

            # Add Content-Type header for form-encoded data
            query_headers = {
                **headers,
                "Content-Type": "application/x-www-form-urlencoded",
            }

            response = await self.http_client.post(
                path=path,
                headers=query_headers,
                data={"q": validation_query},
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
