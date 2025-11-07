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


class ObjectsBatchCreateTool(BaseTool):
    """Create multiple object records in a single API call."""

    @property
    def name(self) -> str:
        return "vault_objects_batch_create"

    @property
    def description(self) -> str:
        return """Create multiple Veeva Vault object records in a single operation.

Batch creation is 10-100x faster than creating records individually.
Use this for:
- Bulk data imports
- Mass record creation
- Data migration
- Efficient data loading

Supports partial success - returns detailed results for each record."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "object_name": {
                    "type": "string",
                    "description": "Object API name (e.g., 'product__v')",
                },
                "records": {
                    "type": "array",
                    "description": "Array of records to create (field name/value pairs)",
                    "items": {
                        "type": "object",
                        "additionalProperties": True,
                    },
                },
            },
            "required": ["object_name", "records"],
        }

    async def execute(self, object_name: str, records: list[dict]) -> ToolResult:
        """Execute batch object creation."""
        try:
            headers = await self._get_auth_headers()
            headers["Content-Type"] = "application/json"
            path = self._build_api_path(f"/objects/{object_name}")

            response = await self.http_client.post(
                path=path,
                headers=headers,
                json=records,
            )

            # Parse batch response
            results = response.get("data", [])
            success_count = sum(
                1 for r in results if r.get("responseStatus") == "SUCCESS"
            )
            failure_count = len(results) - success_count

            self.logger.info(
                "batch_objects_created",
                object_name=object_name,
                total=len(records),
                successes=success_count,
                failures=failure_count,
            )

            return ToolResult(
                success=failure_count == 0,
                data={
                    "object_name": object_name,
                    "total": len(records),
                    "successes": success_count,
                    "failures": failure_count,
                    "results": results,
                },
                metadata={
                    "object_name": object_name,
                    "operation": "batch_create",
                    "batch_size": len(records),
                    "success_rate": success_count / len(records) if records else 0,
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Batch {object_name} creation failed: {e.message}",
                metadata={
                    "error_code": e.error_code,
                    "object_name": object_name,
                    "batch_size": len(records),
                },
            )


class ObjectsBatchUpdateTool(BaseTool):
    """Update multiple object records in a single API call."""

    @property
    def name(self) -> str:
        return "vault_objects_batch_update"

    @property
    def description(self) -> str:
        return """Update multiple Veeva Vault object records in a single operation.

Batch updates are 10-100x faster than updating records individually.
Use this for:
- Bulk metadata changes
- Mass status updates
- Data synchronization
- Large-scale data management

Supports partial success - returns detailed results for each record."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "object_name": {
                    "type": "string",
                    "description": "Object API name (e.g., 'product__v')",
                },
                "updates": {
                    "type": "array",
                    "description": "Array of updates (must include id field)",
                    "items": {
                        "type": "object",
                        "additionalProperties": True,
                        "required": ["id"],
                    },
                },
            },
            "required": ["object_name", "updates"],
        }

    async def execute(self, object_name: str, updates: list[dict]) -> ToolResult:
        """Execute batch object update."""
        try:
            headers = await self._get_auth_headers()
            headers["Content-Type"] = "application/json"
            path = self._build_api_path(f"/objects/{object_name}")

            response = await self.http_client.put(
                path=path,
                headers=headers,
                json=updates,
            )

            # Parse batch response
            results = response.get("data", [])
            success_count = sum(
                1 for r in results if r.get("responseStatus") == "SUCCESS"
            )
            failure_count = len(results) - success_count

            self.logger.info(
                "batch_objects_updated",
                object_name=object_name,
                total=len(updates),
                successes=success_count,
                failures=failure_count,
            )

            return ToolResult(
                success=failure_count == 0,
                data={
                    "object_name": object_name,
                    "total": len(updates),
                    "successes": success_count,
                    "failures": failure_count,
                    "results": results,
                },
                metadata={
                    "object_name": object_name,
                    "operation": "batch_update",
                    "batch_size": len(updates),
                    "success_rate": success_count / len(updates) if updates else 0,
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Batch {object_name} update failed: {e.message}",
                metadata={
                    "error_code": e.error_code,
                    "object_name": object_name,
                    "batch_size": len(updates),
                },
            )


class ObjectsGetActionsTool(BaseTool):
    """Get available workflow actions for an object record."""

    @property
    def name(self) -> str:
        return "vault_objects_get_actions"

    @property
    def description(self) -> str:
        return """Get available workflow/lifecycle actions for an object record.

Returns list of actions that can be performed:
- Workflow state changes
- Lifecycle state transitions  
- User actions specific to object type

Use before executing actions to discover what's available."""

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
                    "description": "The record ID",
                },
            },
            "required": ["object_name", "record_id"],
        }

    async def execute(self, object_name: str, record_id: str) -> ToolResult:
        """Execute get actions."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/{object_name}/{record_id}/actions")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            actions = response.get("lifecycle_actions__v", [])

            self.logger.info(
                "object_actions_retrieved",
                object_name=object_name,
                record_id=record_id,
                action_count=len(actions),
            )

            return ToolResult(
                success=True,
                data={
                    "object_name": object_name,
                    "record_id": record_id,
                    "actions": actions,
                    "count": len(actions),
                },
                metadata={"object_name": object_name, "record_id": record_id},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get actions for {object_name} record {record_id}: {e.message}",
                metadata={
                    "error_code": e.error_code,
                    "object_name": object_name,
                    "record_id": record_id,
                },
            )


class ObjectsExecuteActionTool(BaseTool):
    """Execute a workflow action on an object record."""

    @property
    def name(self) -> str:
        return "vault_objects_execute_action"

    @property
    def description(self) -> str:
        return """Execute a workflow/lifecycle action on an object record.

Common actions:
- Change state (e.g., Draft → Active → Retired)
- Trigger approvals
- Update workflow status
- Object-specific actions

Use get_actions first to discover available actions."""

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
                    "description": "The record ID",
                },
                "action_name": {
                    "type": "string",
                    "description": "Action name (from get_actions response)",
                },
                "action_data": {
                    "type": "object",
                    "description": "Action-specific parameters (optional)",
                    "additionalProperties": True,
                },
            },
            "required": ["object_name", "record_id", "action_name"],
        }

    async def execute(
        self,
        object_name: str,
        record_id: str,
        action_name: str,
        action_data: Optional[dict] = None,
    ) -> ToolResult:
        """Execute workflow action."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(
                f"/objects/{object_name}/{record_id}/actions/{action_name}"
            )

            response = await self.http_client.post(
                path=path,
                headers=headers,
                json=action_data or {},
            )

            self.logger.info(
                "object_action_executed",
                object_name=object_name,
                record_id=record_id,
                action_name=action_name,
            )

            return ToolResult(
                success=True,
                data={
                    "object_name": object_name,
                    "record_id": record_id,
                    "action_name": action_name,
                    "result": response,
                },
                metadata={
                    "object_name": object_name,
                    "record_id": record_id,
                    "action_name": action_name,
                    "operation": "workflow_action",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to execute action {action_name} on {object_name} record {record_id}: {e.message}",
                metadata={
                    "error_code": e.error_code,
                    "object_name": object_name,
                    "record_id": record_id,
                    "action_name": action_name,
                },
            )
