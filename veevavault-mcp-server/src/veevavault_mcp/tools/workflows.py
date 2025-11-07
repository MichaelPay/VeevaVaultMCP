"""
Workflow management tools for Veeva Vault.

Workflows control document and object lifecycle transitions.
"""

from typing import Optional
from .base import BaseTool, ToolResult
from ..utils.errors import APIError


class WorkflowsListTool(BaseTool):
    """List all workflows in the vault."""

    @property
    def name(self) -> str:
        return "vault_workflows_list"

    @property
    def description(self) -> str:
        return """List all workflows available in the vault.

Workflows manage document and object lifecycle transitions.

Common workflows:
- Document Review & Approval
- Change Control
- Training Assignment
- Quality Event Investigation

Returns workflow IDs, names, types, and status."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "workflow_type": {
                    "type": "string",
                    "description": "Filter by workflow type (optional): 'atomic', 'standard'",
                },
                "active_only": {
                    "type": "boolean",
                    "description": "Only return active workflows (default: true)",
                    "default": True,
                },
            },
        }

    async def execute(
        self, workflow_type: Optional[str] = None, active_only: bool = True
    ) -> ToolResult:
        """List workflows."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path("/objects/workflows")

            # Build query parameters
            params = {}
            if active_only:
                params["status"] = "active__v"
            if workflow_type:
                params["type"] = workflow_type

            response = await self.http_client.get(
                path=path,
                headers=headers,
                params=params if params else None,
            )

            workflows = response.get("data", [])

            self.logger.info(
                "workflows_listed",
                workflow_count=len(workflows),
                active_only=active_only,
            )

            return ToolResult(
                success=True,
                data={
                    "workflows": workflows,
                    "count": len(workflows),
                    "active_only": active_only,
                },
                metadata={"workflow_count": len(workflows)},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to list workflows: {e.message}",
                metadata={"error_code": e.error_code},
            )


class WorkflowsGetTool(BaseTool):
    """Get detailed information about a specific workflow."""

    @property
    def name(self) -> str:
        return "vault_workflows_get"

    @property
    def description(self) -> str:
        return """Get detailed workflow information.

Returns:
- Workflow states and transitions
- Available user actions
- Role assignments
- Workflow configuration

Use this to understand workflow structure before triggering actions."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "workflow_id": {
                    "type": "string",
                    "description": "The workflow ID (e.g., 'doc_workflow__c')",
                },
            },
            "required": ["workflow_id"],
        }

    async def execute(self, workflow_id: str) -> ToolResult:
        """Get workflow details."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/workflows/{workflow_id}")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            workflow_data = response.get("data", {})

            self.logger.info(
                "workflow_retrieved",
                workflow_id=workflow_id,
            )

            return ToolResult(
                success=True,
                data={
                    "workflow_id": workflow_id,
                    "workflow": workflow_data,
                },
                metadata={"workflow_id": workflow_id},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get workflow {workflow_id}: {e.message}",
                metadata={"error_code": e.error_code, "workflow_id": workflow_id},
            )


class DocumentsGetWorkflowDetailsTool(BaseTool):
    """Get workflow details for a specific document."""

    @property
    def name(self) -> str:
        return "vault_documents_get_workflow_details"

    @property
    def description(self) -> str:
        return """Get current workflow state and available actions for a document.

Returns:
- Current workflow state
- Available user actions
- Task assignments
- Workflow history

Essential for understanding what actions can be performed on a document."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "integer",
                    "description": "The document ID",
                },
            },
            "required": ["document_id"],
        }

    async def execute(self, document_id: int) -> ToolResult:
        """Get document workflow details."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/documents/{document_id}/workflow")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            workflow_data = response.get("data", {})

            self.logger.info(
                "document_workflow_retrieved",
                document_id=document_id,
            )

            return ToolResult(
                success=True,
                data={
                    "document_id": document_id,
                    "workflow": workflow_data,
                    "current_state": workflow_data.get("state__v"),
                    "available_actions": workflow_data.get("available_actions", []),
                },
                metadata={
                    "document_id": document_id,
                    "operation": "get_workflow_details",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get workflow details for document {document_id}: {e.message}",
                metadata={"error_code": e.error_code, "document_id": document_id},
            )
