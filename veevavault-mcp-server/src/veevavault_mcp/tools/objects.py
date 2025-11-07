"""
Object management tools for VeevaVault.

Objects are custom Vault records like products, studies, quality events, etc.
"""

from typing import Optional
from .base import BaseTool, ToolResult
from ..utils.errors import APIError


class ObjectsQueryTool(BaseTool):
    """Query Vault object records using VQL."""

    @property
    def name(self) -> str:
        return "vault_objects_query"

    @property
    def description(self) -> str:
        return """Query Veeva Vault object records using VQL.

Objects are custom records like:
- Products (product__v)
- Studies (study__v)
- Quality Events (quality_event__c)
- Sites (site__v)
- Any custom objects

Use VQL to query by any field.
Essential for working with Vault data."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "object_name": {
                    "type": "string",
                    "description": "Object API name (e.g., 'product__v', 'quality_event__c')",
                },
                "vql": {
                    "type": "string",
                    "description": "Raw VQL query (if not provided, queries all records)",
                },
                "fields": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Fields to return (default: id, name__v)",
                },
                "where": {
                    "type": "string",
                    "description": "WHERE clause (without 'WHERE' keyword)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results per page (default: 100)",
                    "default": 100,
                },
                "auto_paginate": {
                    "type": "boolean",
                    "description": "Automatically fetch all pages (default: false)",
                    "default": False,
                },
            },
            "required": ["object_name"],
        }

    async def execute(
        self,
        object_name: str,
        vql: Optional[str] = None,
        fields: Optional[list[str]] = None,
        where: Optional[str] = None,
        limit: int = 100,
        auto_paginate: bool = False,
    ) -> ToolResult:
        """Execute object query."""
        try:
            headers = await self._get_auth_headers()

            # Build VQL query
            if vql:
                query = vql
            else:
                field_list = ", ".join(fields) if fields else "id, name__v"
                where_clause = f" WHERE {where}" if where else ""
                query = f"SELECT {field_list} FROM {object_name}{where_clause} LIMIT {limit}"

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
                data={"q": query},
            )

            # Collect all records
            records = response.get("data", [])

            # Parse pagination metadata
            pagesize = response.get("pagesize", limit)
            total = response.get("total", len(records))
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
                    records.extend(page_data)
                    pages_fetched += 1
                    next_page = page_response.get("next_page")

            self.logger.info(
                "objects_queried",
                object_name=object_name,
                count=len(records),
                total_available=total,
                pages_fetched=pages_fetched,
            )

            return ToolResult(
                success=True,
                data={
                    "object_name": object_name,
                    "records": records,
                    "count": len(records),
                    "total": total,
                    "query": query,
                    "pagination": {
                        "pagesize": pagesize,
                        "pages_fetched": pages_fetched,
                        "total_available": total,
                        "is_complete": auto_paginate or len(records) >= total,
                    },
                },
                metadata={
                    "object_name": object_name,
                    "auto_paginate": auto_paginate,
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to query {object_name}: {e.message}",
                metadata={"error_code": e.error_code, "object_name": object_name},
            )


class ObjectsGetTool(BaseTool):
    """Get a specific object record by ID."""

    @property
    def name(self) -> str:
        return "vault_objects_get"

    @property
    def description(self) -> str:
        return """Get detailed information for a specific Vault object record.

Returns complete record with all fields.

Use after objects_query to get full record details."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "object_name": {
                    "type": "string",
                    "description": "Object API name (e.g., 'product__v')",
                },
                "record_id": {
                    "type": "string",
                    "description": "The record ID (e.g., 'V0P000000001001')",
                },
            },
            "required": ["object_name", "record_id"],
        }

    async def execute(self, object_name: str, record_id: str) -> ToolResult:
        """Execute object record retrieval."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/{object_name}/{record_id}")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            record_data = response.get("data", {})

            self.logger.info(
                "object_retrieved",
                object_name=object_name,
                record_id=record_id,
            )

            return ToolResult(
                success=True,
                data=record_data,
                metadata={"object_name": object_name, "record_id": record_id},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get {object_name} record {record_id}: {e.message}",
                metadata={
                    "error_code": e.error_code,
                    "object_name": object_name,
                    "record_id": record_id,
                },
            )


class ObjectsCreateTool(BaseTool):
    """Create a new object record."""

    @property
    def name(self) -> str:
        return "vault_objects_create"

    @property
    def description(self) -> str:
        return """Create a new Veeva Vault object record.

Specify object type and field values.
Use metadata tools to discover required fields.

Common objects:
- product__v: Products
- study__v: Clinical studies
- quality_event__c: Quality events
- site__v: Clinical sites"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "object_name": {
                    "type": "string",
                    "description": "Object API name (e.g., 'product__v')",
                },
                "fields": {
                    "type": "object",
                    "description": "Field name/value pairs (use __v suffix for field names)",
                    "additionalProperties": True,
                },
            },
            "required": ["object_name", "fields"],
        }

    async def execute(self, object_name: str, fields: dict) -> ToolResult:
        """Execute object record creation."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/{object_name}")

            response = await self.http_client.post(
                path=path,
                headers=headers,
                json=fields,
            )

            record_id = response.get("data", {}).get("id")

            self.logger.info(
                "object_created",
                object_name=object_name,
                record_id=record_id,
            )

            return ToolResult(
                success=True,
                data={
                    "object_name": object_name,
                    "record_id": record_id,
                    "fields": fields,
                },
                metadata={
                    "object_name": object_name,
                    "record_id": record_id,
                    "operation": "create",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to create {object_name} record: {e.message}",
                metadata={"error_code": e.error_code, "object_name": object_name},
            )


class ObjectsUpdateTool(BaseTool):
    """Update an existing object record."""

    @property
    def name(self) -> str:
        return "vault_objects_update"

    @property
    def description(self) -> str:
        return """Update an existing Veeva Vault object record.

Provide object type, record ID, and fields to update.
Only specified fields will be updated."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "object_name": {
                    "type": "string",
                    "description": "Object API name (e.g., 'product__v')",
                },
                "record_id": {
                    "type": "string",
                    "description": "The record ID to update",
                },
                "fields": {
                    "type": "object",
                    "description": "Field name/value pairs to update",
                    "additionalProperties": True,
                },
            },
            "required": ["object_name", "record_id", "fields"],
        }

    async def execute(
        self, object_name: str, record_id: str, fields: dict
    ) -> ToolResult:
        """Execute object record update."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/{object_name}/{record_id}")

            response = await self.http_client.put(
                path=path,
                headers=headers,
                json=fields,
            )

            self.logger.info(
                "object_updated",
                object_name=object_name,
                record_id=record_id,
                fields_updated=list(fields.keys()),
            )

            return ToolResult(
                success=True,
                data={
                    "object_name": object_name,
                    "record_id": record_id,
                    "updated_fields": list(fields.keys()),
                },
                metadata={
                    "object_name": object_name,
                    "record_id": record_id,
                    "operation": "update",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to update {object_name} record {record_id}: {e.message}",
                metadata={
                    "error_code": e.error_code,
                    "object_name": object_name,
                    "record_id": record_id,
                },
            )
