"""
Metadata configuration tools for VeevaVault.
"""

from typing import Optional
from .base import BaseTool, ToolResult
from ..utils.errors import APIError


class GetMetadataTool(BaseTool):
    """Get metadata configuration for Vault objects."""

    @property
    def name(self) -> str:
        return "vault_metadata_get"

    @property
    def description(self) -> str:
        return """Get metadata configuration for Veeva Vault objects.

Retrieve object schemas, field definitions, and picklists.
Useful for understanding Vault configuration and available fields.

Examples:
- Get document metadata schema
- Get custom object field definitions
- Retrieve picklist values"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "object_type": {
                    "type": "string",
                    "description": "Object type (e.g., documents, users, custom_object__c)",
                },
            },
            "required": ["object_type"],
        }

    async def execute(self, object_type: str) -> ToolResult:
        """
        Execute metadata retrieval.

        Args:
            object_type: Vault object type

        Returns:
            ToolResult with metadata schema
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/metadata/vobjects/{object_type}")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            metadata = response.get("object", {})
            fields = metadata.get("fields", [])

            self.logger.info(
                "metadata_retrieved",
                object_type=object_type,
                field_count=len(fields),
            )

            return ToolResult(
                success=True,
                data={
                    "object_type": object_type,
                    "metadata": metadata,
                    "fields": fields,
                    "field_count": len(fields),
                },
                metadata={
                    "object_type": object_type,
                    "field_count": len(fields),
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get metadata for {object_type}: {e.message}",
                metadata={"error_code": e.error_code, "object_type": object_type},
            )


class ListObjectTypesTool(BaseTool):
    """List all object types available in Vault."""

    @property
    def name(self) -> str:
        return "vault_metadata_list_objects"

    @property
    def description(self) -> str:
        return """List all object types available in Veeva Vault.

Returns both standard and custom objects with their metadata.
Useful for discovering available Vault objects and their configurations."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {},
            "required": [],
        }

    async def execute(self) -> ToolResult:
        """
        Execute object types list retrieval.

        Returns:
            ToolResult with object types list
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path("/metadata/vobjects")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            objects = response.get("objects", [])

            self.logger.info("object_types_listed", count=len(objects))

            return ToolResult(
                success=True,
                data={
                    "objects": objects,
                    "count": len(objects),
                },
                metadata={"object_count": len(objects)},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to list object types: {e.message}",
                metadata={"error_code": e.error_code},
            )


class GetPicklistValuesTool(BaseTool):
    """Get picklist values for a specific field."""

    @property
    def name(self) -> str:
        return "vault_metadata_get_picklist"

    @property
    def description(self) -> str:
        return """Get picklist values for a specific Vault field.

Returns all available values for a picklist field,
including active/inactive status and display labels.

Useful for validating values before creating/updating records."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "object_type": {
                    "type": "string",
                    "description": "Object type containing the picklist field",
                },
                "field_name": {
                    "type": "string",
                    "description": "Name of the picklist field",
                },
            },
            "required": ["object_type", "field_name"],
        }

    async def execute(self, object_type: str, field_name: str) -> ToolResult:
        """
        Execute picklist values retrieval.

        Args:
            object_type: Vault object type
            field_name: Field name

        Returns:
            ToolResult with picklist values
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(
                f"/metadata/vobjects/{object_type}/picklists/{field_name}"
            )

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            picklist_values = response.get("picklistValues", [])

            self.logger.info(
                "picklist_retrieved",
                object_type=object_type,
                field_name=field_name,
                value_count=len(picklist_values),
            )

            return ToolResult(
                success=True,
                data={
                    "object_type": object_type,
                    "field_name": field_name,
                    "values": picklist_values,
                    "value_count": len(picklist_values),
                },
                metadata={
                    "object_type": object_type,
                    "field_name": field_name,
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get picklist values: {e.message}",
                metadata={
                    "error_code": e.error_code,
                    "object_type": object_type,
                    "field_name": field_name,
                },
            )
