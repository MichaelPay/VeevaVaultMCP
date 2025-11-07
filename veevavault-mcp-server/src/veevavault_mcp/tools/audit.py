"""
Audit trail and compliance reporting tools for VeevaVault.
"""

from typing import Optional
from datetime import datetime, timedelta
from .base import BaseTool, ToolResult
from ..utils.errors import APIError


class QueryAuditTrailTool(BaseTool):
    """Query Vault audit trail for compliance and tracking."""

    @property
    def name(self) -> str:
        return "vault_audit_query"

    @property
    def description(self) -> str:
        return """Query Veeva Vault audit trail for compliance tracking.

Search audit trail by:
- Date range (start_date, end_date)
- Event type (login, document_access, data_change, etc.)
- User
- Object type

Returns detailed audit records including:
- Timestamp
- User who performed action
- Action type
- Object/record affected
- Previous/new values (for changes)"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "Start date (ISO format: YYYY-MM-DD)",
                },
                "end_date": {
                    "type": "string",
                    "description": "End date (ISO format: YYYY-MM-DD)",
                },
                "event_type": {
                    "type": "string",
                    "description": "Filter by event type (e.g., login, document_access, data_change)",
                },
                "user_id": {
                    "type": "integer",
                    "description": "Filter by user ID",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of records to return",
                    "default": 1000,
                    "minimum": 1,
                    "maximum": 10000,
                },
            },
            "required": ["start_date", "end_date"],
        }

    async def execute(
        self,
        start_date: str,
        end_date: str,
        event_type: Optional[str] = None,
        user_id: Optional[int] = None,
        limit: int = 1000,
    ) -> ToolResult:
        """
        Execute audit trail query.

        Args:
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            event_type: Event type filter (optional)
            user_id: User ID filter (optional)
            limit: Max records to return

        Returns:
            ToolResult with audit records
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path("/audittrail")

            # Build query parameters
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "limit": limit,
            }

            if event_type:
                params["event_type"] = event_type
            if user_id:
                params["user_id"] = user_id

            response = await self.http_client.get(
                path=path,
                headers=headers,
                params=params,
            )

            audit_records = response.get("data", [])

            self.logger.info(
                "audit_trail_queried",
                start_date=start_date,
                end_date=end_date,
                record_count=len(audit_records),
            )

            return ToolResult(
                success=True,
                data={
                    "audit_records": audit_records,
                    "count": len(audit_records),
                    "start_date": start_date,
                    "end_date": end_date,
                },
                metadata={
                    "start_date": start_date,
                    "end_date": end_date,
                    "record_count": len(audit_records),
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to query audit trail: {e.message}",
                metadata={"error_code": e.error_code},
            )


class GetDocumentAuditTool(BaseTool):
    """Get audit history for a specific document."""

    @property
    def name(self) -> str:
        return "vault_document_audit_get"

    @property
    def description(self) -> str:
        return """Get complete audit history for a specific Veeva Vault document.

Returns all audit events for a document including:
- Document creation
- Version updates
- Lifecycle state changes
- Metadata changes
- Access history
- Download history

Useful for compliance tracking and investigating document changes."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "integer",
                    "description": "The document ID",
                },
                "major_version": {
                    "type": "integer",
                    "description": "Major version number (optional, for version-specific audit)",
                },
                "minor_version": {
                    "type": "integer",
                    "description": "Minor version number (optional, for version-specific audit)",
                },
            },
            "required": ["document_id"],
        }

    async def execute(
        self,
        document_id: int,
        major_version: Optional[int] = None,
        minor_version: Optional[int] = None,
    ) -> ToolResult:
        """
        Execute document audit retrieval.

        Args:
            document_id: Document ID
            major_version: Major version (optional)
            minor_version: Minor version (optional)

        Returns:
            ToolResult with document audit history
        """
        try:
            headers = await self._get_auth_headers()

            # Build path based on version
            if major_version is not None and minor_version is not None:
                path = self._build_api_path(
                    f"/objects/documents/{document_id}/versions/{major_version}/{minor_version}/audittrail"
                )
            else:
                path = self._build_api_path(f"/objects/documents/{document_id}/audittrail")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            audit_records = response.get("data", [])

            self.logger.info(
                "document_audit_retrieved",
                document_id=document_id,
                record_count=len(audit_records),
            )

            return ToolResult(
                success=True,
                data={
                    "document_id": document_id,
                    "major_version": major_version,
                    "minor_version": minor_version,
                    "audit_records": audit_records,
                    "count": len(audit_records),
                },
                metadata={
                    "document_id": document_id,
                    "record_count": len(audit_records),
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get document audit: {e.message}",
                metadata={"error_code": e.error_code, "document_id": document_id},
            )


class GetUserActivityTool(BaseTool):
    """Get activity history for a specific user."""

    @property
    def name(self) -> str:
        return "vault_user_activity_get"

    @property
    def description(self) -> str:
        return """Get activity history for a specific Veeva Vault user.

Returns user's actions including:
- Login/logout events
- Document access and downloads
- Record creation/updates
- Permission changes
- Configuration changes

Useful for:
- Compliance audits
- Security investigations
- User activity monitoring"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The user ID",
                },
                "start_date": {
                    "type": "string",
                    "description": "Start date (ISO format: YYYY-MM-DD)",
                },
                "end_date": {
                    "type": "string",
                    "description": "End date (ISO format: YYYY-MM-DD)",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of activity records",
                    "default": 1000,
                },
            },
            "required": ["user_id", "start_date", "end_date"],
        }

    async def execute(
        self,
        user_id: int,
        start_date: str,
        end_date: str,
        limit: int = 1000,
    ) -> ToolResult:
        """
        Execute user activity retrieval.

        Args:
            user_id: User ID
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
            limit: Max records

        Returns:
            ToolResult with user activity records
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path("/audittrail")

            params = {
                "user_id": user_id,
                "start_date": start_date,
                "end_date": end_date,
                "limit": limit,
            }

            response = await self.http_client.get(
                path=path,
                headers=headers,
                params=params,
            )

            activity_records = response.get("data", [])

            # Group by activity type for summary
            activity_summary = {}
            for record in activity_records:
                event_type = record.get("event_type", "unknown")
                activity_summary[event_type] = activity_summary.get(event_type, 0) + 1

            self.logger.info(
                "user_activity_retrieved",
                user_id=user_id,
                record_count=len(activity_records),
            )

            return ToolResult(
                success=True,
                data={
                    "user_id": user_id,
                    "start_date": start_date,
                    "end_date": end_date,
                    "activity_records": activity_records,
                    "count": len(activity_records),
                    "activity_summary": activity_summary,
                },
                metadata={
                    "user_id": user_id,
                    "record_count": len(activity_records),
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get user activity: {e.message}",
                metadata={"error_code": e.error_code, "user_id": user_id},
            )
