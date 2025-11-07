"""
User management tools for VeevaVault.
"""

from typing import Optional, List
from .base import BaseTool, ToolResult
from ..utils.errors import APIError


class ListUsersTool(BaseTool):
    """List users in Veeva Vault with filtering options."""

    @property
    def name(self) -> str:
        return "vault_users_list"

    @property
    def description(self) -> str:
        return """List users in Veeva Vault. Supports filtering by status, security profile, and other criteria.

Examples:
- List all active users
- Find users by security profile
- Search users by name or email"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["active", "inactive", "all"],
                    "description": "Filter by user status",
                    "default": "active",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of users to return",
                    "default": 100,
                    "minimum": 1,
                    "maximum": 1000,
                },
                "offset": {
                    "type": "integer",
                    "description": "Offset for pagination",
                    "default": 0,
                    "minimum": 0,
                },
            },
            "required": [],
        }

    async def execute(self, status: str = "active", limit: int = 100, offset: int = 0) -> ToolResult:
        """
        Execute user list retrieval.

        Args:
            status: Filter by status (active, inactive, all)
            limit: Maximum number of users to return
            offset: Offset for pagination

        Returns:
            ToolResult with user list
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path("/objects/users")

            # Build query parameters
            params = {
                "limit": limit,
                "offset": offset,
            }

            if status != "all":
                params["status__v"] = status + "__v"

            # Make API request
            response = await self.http_client.get(
                path=path,
                headers=headers,
                params=params,
            )

            # Extract users from response
            users = response.get("data", [])
            total = len(users)

            self.logger.info(
                "users_listed",
                count=total,
                status=status,
            )

            return ToolResult(
                success=True,
                data={
                    "users": users,
                    "count": total,
                    "limit": limit,
                    "offset": offset,
                },
                metadata={
                    "status_filter": status,
                    "total_returned": total,
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to list users: {e.message}",
                metadata={"error_code": e.error_code},
            )


class GetUserTool(BaseTool):
    """Get detailed information about a specific user."""

    @property
    def name(self) -> str:
        return "vault_user_get"

    @property
    def description(self) -> str:
        return """Get detailed information about a specific Veeva Vault user by ID.

Returns complete user profile including:
- User details (name, email, license)
- Security profiles and permissions
- Groups and roles
- Status and metadata"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "The ID of the user to retrieve",
                },
            },
            "required": ["user_id"],
        }

    async def execute(self, user_id: int) -> ToolResult:
        """
        Execute user retrieval.

        Args:
            user_id: User ID to retrieve

        Returns:
            ToolResult with user details
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/users/{user_id}")

            # Make API request
            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            # Extract user data
            user_data = response.get("data", {})

            self.logger.info(
                "user_retrieved",
                user_id=user_id,
                user_name=user_data.get("user_name__v"),
            )

            return ToolResult(
                success=True,
                data=user_data,
                metadata={
                    "user_id": user_id,
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to get user {user_id}: {e.message}",
                metadata={"error_code": e.error_code, "user_id": user_id},
            )


class CreateUserTool(BaseTool):
    """Create a new user in Veeva Vault."""

    @property
    def name(self) -> str:
        return "vault_user_create"

    @property
    def description(self) -> str:
        return """Create a new user in Veeva Vault.

Required fields:
- user_name: Username (email format)
- user_email: Email address
- user_first_name: First name
- user_last_name: Last name
- security_profile: Security profile ID or name
- license_type: License type (e.g., full_user__v)

Optional fields:
- user_title: Job title
- group_id: Initial group assignment
- user_language: Language preference"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "user_name": {
                    "type": "string",
                    "description": "Username (email format required)",
                },
                "user_email": {
                    "type": "string",
                    "description": "User email address",
                },
                "user_first_name": {
                    "type": "string",
                    "description": "User first name",
                },
                "user_last_name": {
                    "type": "string",
                    "description": "User last name",
                },
                "security_profile": {
                    "type": "string",
                    "description": "Security profile ID",
                },
                "license_type": {
                    "type": "string",
                    "description": "License type (e.g., full_user__v)",
                },
                "user_title": {
                    "type": "string",
                    "description": "Job title (optional)",
                },
                "group_id": {
                    "type": "integer",
                    "description": "Initial group assignment (optional)",
                },
                "user_language": {
                    "type": "string",
                    "description": "Language code (e.g., en, de, ja)",
                },
            },
            "required": [
                "user_name",
                "user_email",
                "user_first_name",
                "user_last_name",
                "security_profile",
                "license_type",
            ],
        }

    async def execute(
        self,
        user_name: str,
        user_email: str,
        user_first_name: str,
        user_last_name: str,
        security_profile: str,
        license_type: str,
        user_title: Optional[str] = None,
        group_id: Optional[int] = None,
        user_language: Optional[str] = None,
    ) -> ToolResult:
        """
        Execute user creation.

        Args:
            user_name: Username (email format)
            user_email: Email address
            user_first_name: First name
            user_last_name: Last name
            security_profile: Security profile ID
            license_type: License type
            user_title: Job title (optional)
            group_id: Group ID (optional)
            user_language: Language code (optional)

        Returns:
            ToolResult with created user ID
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path("/objects/users")

            # Build user data
            user_data = {
                "user_name__v": user_name,
                "user_email__v": user_email,
                "user_first_name__v": user_first_name,
                "user_last_name__v": user_last_name,
                "security_profile__v": security_profile,
                "license_type__v": license_type,
                "active__v": True,
            }

            # Add optional fields
            if user_title:
                user_data["user_title__v"] = user_title
            if group_id:
                user_data["group_id__v"] = group_id
            if user_language:
                user_data["user_language__v"] = user_language

            # Make API request
            response = await self.http_client.post(
                path=path,
                headers=headers,
                json=user_data,
            )

            # Extract created user ID
            user_id = response.get("data", {}).get("id")

            self.logger.info(
                "user_created",
                user_id=user_id,
                user_name=user_name,
            )

            return ToolResult(
                success=True,
                data={
                    "user_id": user_id,
                    "user_name": user_name,
                    "user_email": user_email,
                },
                metadata={
                    "user_id": user_id,
                    "operation": "create",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to create user: {e.message}",
                metadata={"error_code": e.error_code},
            )


class UpdateUserTool(BaseTool):
    """Update an existing user in Veeva Vault."""

    @property
    def name(self) -> str:
        return "vault_user_update"

    @property
    def description(self) -> str:
        return """Update an existing Veeva Vault user.

Can update:
- User profile (name, title, email)
- Security profile
- License type
- Status (active/inactive)
- Language preference
- Group assignments"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "ID of user to update",
                },
                "user_email": {
                    "type": "string",
                    "description": "New email address",
                },
                "user_first_name": {
                    "type": "string",
                    "description": "New first name",
                },
                "user_last_name": {
                    "type": "string",
                    "description": "New last name",
                },
                "user_title": {
                    "type": "string",
                    "description": "New job title",
                },
                "security_profile": {
                    "type": "string",
                    "description": "New security profile ID",
                },
                "license_type": {
                    "type": "string",
                    "description": "New license type",
                },
                "active": {
                    "type": "boolean",
                    "description": "Set user active/inactive status",
                },
                "user_language": {
                    "type": "string",
                    "description": "New language preference",
                },
            },
            "required": ["user_id"],
        }

    async def execute(
        self,
        user_id: int,
        user_email: Optional[str] = None,
        user_first_name: Optional[str] = None,
        user_last_name: Optional[str] = None,
        user_title: Optional[str] = None,
        security_profile: Optional[str] = None,
        license_type: Optional[str] = None,
        active: Optional[bool] = None,
        user_language: Optional[str] = None,
    ) -> ToolResult:
        """
        Execute user update.

        Args:
            user_id: User ID to update
            user_email: New email (optional)
            user_first_name: New first name (optional)
            user_last_name: New last name (optional)
            user_title: New title (optional)
            security_profile: New security profile (optional)
            license_type: New license type (optional)
            active: New active status (optional)
            user_language: New language (optional)

        Returns:
            ToolResult with update confirmation
        """
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/objects/users/{user_id}")

            # Build update data with only provided fields
            update_data = {}
            if user_email is not None:
                update_data["user_email__v"] = user_email
            if user_first_name is not None:
                update_data["user_first_name__v"] = user_first_name
            if user_last_name is not None:
                update_data["user_last_name__v"] = user_last_name
            if user_title is not None:
                update_data["user_title__v"] = user_title
            if security_profile is not None:
                update_data["security_profile__v"] = security_profile
            if license_type is not None:
                update_data["license_type__v"] = license_type
            if active is not None:
                update_data["active__v"] = active
            if user_language is not None:
                update_data["user_language__v"] = user_language

            if not update_data:
                return ToolResult(
                    success=False,
                    error="No fields provided for update",
                    metadata={"user_id": user_id},
                )

            # Make API request
            response = await self.http_client.put(
                path=path,
                headers=headers,
                json=update_data,
            )

            self.logger.info(
                "user_updated",
                user_id=user_id,
                fields_updated=list(update_data.keys()),
            )

            return ToolResult(
                success=True,
                data={
                    "user_id": user_id,
                    "updated_fields": list(update_data.keys()),
                },
                metadata={
                    "user_id": user_id,
                    "operation": "update",
                    "fields_updated": len(update_data),
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to update user {user_id}: {e.message}",
                metadata={"error_code": e.error_code, "user_id": user_id},
            )
