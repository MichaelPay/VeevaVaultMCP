"""
Group management tools for VeevaVault.
"""

from typing import Optional, List
from .base import BaseTool, ToolResult
from ..utils.errors import APIError


class ListGroupsTool(BaseTool):
    """List groups in Veeva Vault."""

    @property
    def name(self) -> str:
        return "vault_groups_list"

    @property
    def description(self) -> str:
        return """List groups in Veeva Vault.

Groups are used to organize users and manage permissions.
Returns group details including:
- Group name and label
- Description
- Members
- Active status"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "active_only": {
                    "type": "boolean",
                    "description": "Only return active groups",
                    "default": True,
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of groups to return",
                    "default": 100,
                    "minimum": 1,
                    "maximum": 1000,
                },
            },
            "required": [],
        }

    async def execute(self, active_only: bool = True, limit: int = 100) -> ToolResult:
        """
        Execute group list retrieval.

        Args:
            active_only: Only return active groups
            limit: Maximum number of groups

        Returns:
            ToolResult with group list
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path("/objects/groups")

            params = {"limit": limit}
            if active_only:
                params["active__v"] = "true"

            response = await self.http_client.get(
                path=path,
                headers=headers,
                params=params,
            )

            groups = response.get("data", [])

            self.logger.info("groups_listed", count=len(groups))

            return ToolResult(
                success=True,
                data={
                    "groups": groups,
                    "count": len(groups),
                },
                metadata={"active_only": active_only},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to list groups: {e.message}",
                metadata={"error_code": e.error_code},
            )


class GetGroupTool(BaseTool):
    """Get detailed information about a specific group."""

    @property
    def name(self) -> str:
        return "vault_group_get"

    @property
    def description(self) -> str:
        return """Get detailed information about a specific Veeva Vault group.

Returns:
- Group details (name, label, description)
- Group members list
- Permissions and roles
- Status and metadata"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The ID of the group to retrieve",
                },
            },
            "required": ["group_id"],
        }

    async def execute(self, group_id: int) -> ToolResult:
        """
        Execute group retrieval.

        Args:
            group_id: Group ID to retrieve

        Returns:
            ToolResult with group details
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/groups/{group_id}")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            group_data = response.get("data", {})

            self.logger.info(
                "group_retrieved",
                group_id=group_id,
                group_name=group_data.get("name__v"),
            )

            return ToolResult(
                success=True,
                data=group_data,
                metadata={"group_id": group_id},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get group {group_id}: {e.message}",
                metadata={"error_code": e.error_code, "group_id": group_id},
            )


class CreateGroupTool(BaseTool):
    """Create a new group in Veeva Vault."""

    @property
    def name(self) -> str:
        return "vault_group_create"

    @property
    def description(self) -> str:
        return """Create a new group in Veeva Vault.

Required:
- name: Group name (unique identifier)
- label: Display label for the group

Optional:
- description: Group description
- active: Whether group is active (default: true)
- members: List of user IDs to add to group"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Unique group name (API name)",
                },
                "label": {
                    "type": "string",
                    "description": "Display label for the group",
                },
                "description": {
                    "type": "string",
                    "description": "Group description",
                },
                "active": {
                    "type": "boolean",
                    "description": "Whether group is active",
                    "default": True,
                },
            },
            "required": ["name", "label"],
        }

    async def execute(
        self,
        name: str,
        label: str,
        description: Optional[str] = None,
        active: bool = True,
    ) -> ToolResult:
        """
        Execute group creation.

        Args:
            name: Group name (unique)
            label: Display label
            description: Description (optional)
            active: Active status (default: True)

        Returns:
            ToolResult with created group ID
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path("/objects/groups")

            group_data = {
                "name__v": name,
                "label__v": label,
                "active__v": active,
            }

            if description:
                group_data["description__v"] = description

            response = await self.http_client.post(
                path=path,
                headers=headers,
                json=group_data,
            )

            group_id = response.get("data", {}).get("id")

            self.logger.info(
                "group_created",
                group_id=group_id,
                group_name=name,
            )

            return ToolResult(
                success=True,
                data={
                    "group_id": group_id,
                    "name": name,
                    "label": label,
                },
                metadata={"group_id": group_id, "operation": "create"},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to create group: {e.message}",
                metadata={"error_code": e.error_code},
            )


class AddGroupMembersTool(BaseTool):
    """Add members to a Veeva Vault group."""

    @property
    def name(self) -> str:
        return "vault_group_add_members"

    @property
    def description(self) -> str:
        return """Add users to a Veeva Vault group.

Specify group ID and list of user IDs to add.
Users will be added as members with appropriate permissions."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The group ID",
                },
                "user_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "List of user IDs to add to the group",
                    "minItems": 1,
                },
            },
            "required": ["group_id", "user_ids"],
        }

    async def execute(self, group_id: int, user_ids: List[int]) -> ToolResult:
        """
        Execute adding members to group.

        Args:
            group_id: Group ID
            user_ids: List of user IDs to add

        Returns:
            ToolResult with operation result
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/groups/{group_id}/users")

            # Add each user
            added_users = []
            failed_users = []

            for user_id in user_ids:
                try:
                    await self.http_client.post(
                        path=path,
                        headers=headers,
                        json={"user_id__v": user_id},
                    )
                    added_users.append(user_id)
                except APIError as e:
                    failed_users.append({"user_id": user_id, "error": str(e)})

            self.logger.info(
                "group_members_added",
                group_id=group_id,
                added_count=len(added_users),
                failed_count=len(failed_users),
            )

            return ToolResult(
                success=len(failed_users) == 0,
                data={
                    "group_id": group_id,
                    "added_users": added_users,
                    "failed_users": failed_users,
                    "total_added": len(added_users),
                },
                metadata={
                    "group_id": group_id,
                    "operation": "add_members",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to add group members: {e.message}",
                metadata={"error_code": e.error_code, "group_id": group_id},
            )


class RemoveGroupMembersTool(BaseTool):
    """Remove members from a Veeva Vault group."""

    @property
    def name(self) -> str:
        return "vault_group_remove_members"

    @property
    def description(self) -> str:
        return """Remove users from a Veeva Vault group.

Specify group ID and list of user IDs to remove.
Users will be removed from the group membership."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "The group ID",
                },
                "user_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "List of user IDs to remove from the group",
                    "minItems": 1,
                },
            },
            "required": ["group_id", "user_ids"],
        }

    async def execute(self, group_id: int, user_ids: List[int]) -> ToolResult:
        """
        Execute removing members from group.

        Args:
            group_id: Group ID
            user_ids: List of user IDs to remove

        Returns:
            ToolResult with operation result
        """
        try:
            headers = await self._get_auth_headers()

            # Remove each user
            removed_users = []
            failed_users = []

            for user_id in user_ids:
                try:
                    path = self._build_api_path(f"/objects/groups/{group_id}/users/{user_id}")
                    await self.http_client.delete(
                        path=path,
                        headers=headers,
                    )
                    removed_users.append(user_id)
                except APIError as e:
                    failed_users.append({"user_id": user_id, "error": str(e)})

            self.logger.info(
                "group_members_removed",
                group_id=group_id,
                removed_count=len(removed_users),
                failed_count=len(failed_users),
            )

            return ToolResult(
                success=len(failed_users) == 0,
                data={
                    "group_id": group_id,
                    "removed_users": removed_users,
                    "failed_users": failed_users,
                    "total_removed": len(removed_users),
                },
                metadata={
                    "group_id": group_id,
                    "operation": "remove_members",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to remove group members: {e.message}",
                metadata={"error_code": e.error_code, "group_id": group_id},
            )
