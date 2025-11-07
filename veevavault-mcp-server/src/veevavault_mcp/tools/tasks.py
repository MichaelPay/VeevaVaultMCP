"""
Task management tools for Veeva Vault.

Tasks are assigned to users as part of workflow processes.
"""

from typing import Optional
from .base import BaseTool, ToolResult
from ..utils.errors import APIError


class TasksListTool(BaseTool):
    """List tasks assigned to the current user."""

    @property
    def name(self) -> str:
        return "vault_tasks_list"

    @property
    def description(self) -> str:
        return """List workflow tasks assigned to the current user.

Returns tasks from:
- Document review workflows
- Change control processes
- Quality event investigations
- Training assignments

Filter by status:
- open - Pending completion
- completed - Already done
- all - All tasks

Use this to see your task queue and pending work."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "Filter by status: 'open', 'completed', 'all' (default: 'open')",
                    "enum": ["open", "completed", "all"],
                    "default": "open",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of tasks to return (default: 100)",
                    "minimum": 1,
                    "maximum": 1000,
                    "default": 100,
                },
            },
        }

    async def execute(self, status: str = "open", limit: int = 100) -> ToolResult:
        """List tasks."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path("/objects/tasks")

            # Build query parameters
            params = {"limit": limit}
            if status != "all":
                params["status__v"] = f"{status}__v"

            response = await self.http_client.get(
                path=path,
                headers=headers,
                params=params,
            )

            tasks = response.get("data", [])

            self.logger.info(
                "tasks_listed",
                task_count=len(tasks),
                status=status,
            )

            return ToolResult(
                success=True,
                data={
                    "tasks": tasks,
                    "count": len(tasks),
                    "status_filter": status,
                },
                metadata={"task_count": len(tasks)},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to list tasks: {e.message}",
                metadata={"error_code": e.error_code},
            )


class TasksGetTool(BaseTool):
    """Get detailed information about a specific task."""

    @property
    def name(self) -> str:
        return "vault_tasks_get"

    @property
    def description(self) -> str:
        return """Get detailed task information.

Returns:
- Task type and description
- Related document/object
- Due date
- Assigned users
- Available actions
- Task instructions

Use cases:
- Review task requirements before completion
- Check task due dates for prioritization
- Understand task context and related documents
- Identify required fields for task completion

Example:
Get details for a document review task to see what verdict options
are available (approve/reject) and what comments are required."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The task ID",
                },
            },
            "required": ["task_id"],
        }

    async def execute(self, task_id: str) -> ToolResult:
        """Get task details."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/tasks/{task_id}")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            task_data = response.get("data", {})

            self.logger.info(
                "task_retrieved",
                task_id=task_id,
            )

            return ToolResult(
                success=True,
                data={
                    "task_id": task_id,
                    "task": task_data,
                    "status": task_data.get("status__v"),
                    "due_date": task_data.get("due_date__v"),
                },
                metadata={"task_id": task_id},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get task {task_id}: {e.message}",
                metadata={"error_code": e.error_code, "task_id": task_id},
            )


class TasksExecuteActionTool(BaseTool):
    """Execute an action on a task (complete, reassign, cancel)."""

    @property
    def name(self) -> str:
        return "vault_tasks_execute_action"

    @property
    def description(self) -> str:
        return """Execute an action on a workflow task.

Common actions:
- complete - Mark task as done (may require comments/verdict)
- reassign - Assign to another user
- cancel - Cancel the task
- delegate - Delegate to another user

Completing tasks advances workflows and triggers next steps.

Required data varies by action:
- complete: May need verdict (approve/reject), comments
- reassign: Requires new assignee user ID
- delegate: Requires delegate user ID

Examples:
- Complete a review task with approval: action="complete", verdict="approved", comment="Looks good"
- Reassign task to another user: action="reassign", assignee_id=12345
- Cancel an outdated task: action="cancel", comment="No longer needed"
"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The task ID",
                },
                "action": {
                    "type": "string",
                    "description": "Action to execute: 'complete', 'reassign', 'cancel', 'delegate'",
                },
                "verdict": {
                    "type": "string",
                    "description": "Task verdict for completion: 'approved', 'rejected' (optional)",
                },
                "comment": {
                    "type": "string",
                    "description": "Comment explaining the action (optional)",
                },
                "assignee_id": {
                    "type": "integer",
                    "description": "User ID for reassign/delegate actions (optional)",
                },
            },
            "required": ["task_id", "action"],
        }

    async def execute(
        self,
        task_id: str,
        action: str,
        verdict: Optional[str] = None,
        comment: Optional[str] = None,
        assignee_id: Optional[int] = None,
    ) -> ToolResult:
        """Execute task action."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/tasks/{task_id}/actions/{action}")

            # Build action data
            action_data = {}
            if verdict:
                action_data["verdict__v"] = verdict
            if comment:
                action_data["comment__v"] = comment
            if assignee_id:
                action_data["assignee__v"] = assignee_id

            response = await self.http_client.post(
                path=path,
                headers=headers,
                json=action_data if action_data else {},
            )

            self.logger.info(
                "task_action_executed",
                task_id=task_id,
                action=action,
            )

            return ToolResult(
                success=True,
                data={
                    "task_id": task_id,
                    "action": action,
                    "verdict": verdict,
                    "result": response,
                },
                metadata={
                    "task_id": task_id,
                    "action": action,
                    "operation": "task_action",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to execute action {action} on task {task_id}: {e.message}",
                metadata={"error_code": e.error_code, "task_id": task_id, "action": action},
            )
