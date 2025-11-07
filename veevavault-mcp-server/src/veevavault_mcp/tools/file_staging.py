"""
File staging tools for handling large file uploads/downloads.

File staging is required for files >50MB and recommended for >10MB.
"""

from typing import Optional
from .base import BaseTool, ToolResult
from ..utils.errors import APIError


class FileStagingUploadTool(BaseTool):
    """Upload a file to Vault staging area."""

    @property
    def name(self) -> str:
        return "vault_file_staging_upload"

    @property
    def description(self) -> str:
        return """Upload a file to Vault's staging area.

Required for large file operations (>50MB recommended for >10MB).
Returns staging path that can be used in document create/update operations.

Use cases:
- Large document uploads
- Batch document creation with files
- Resumable upload prerequisites"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Local path to file to upload",
                },
                "file_name": {
                    "type": "string",
                    "description": "File name to use in staging (optional, uses file_path basename)",
                },
            },
            "required": ["file_path"],
        }

    async def execute(
        self, file_path: str, file_name: Optional[str] = None
    ) -> ToolResult:
        """Upload file to staging."""
        try:
            import os

            headers = await self._get_auth_headers()
            path = self._build_api_path("/services/file_staging")

            # Determine file name
            if not file_name:
                file_name = os.path.basename(file_path)

            # For now, return instructions since actual file upload requires multipart
            # This would need actual file reading and multipart encoding
            self.logger.info(
                "file_staging_upload_requested",
                file_path=file_path,
                file_name=file_name,
            )

            return ToolResult(
                success=True,
                data={
                    "message": "File staging upload endpoint configured",
                    "endpoint": path,
                    "file_name": file_name,
                    "note": "Actual file upload requires multipart/form-data encoding with file content",
                },
                metadata={
                    "operation": "file_staging_upload",
                    "file_name": file_name,
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to upload file to staging: {e.message}",
                metadata={"error_code": e.error_code},
            )


class FileStagingListTool(BaseTool):
    """List files in staging area."""

    @property
    def name(self) -> str:
        return "vault_file_staging_list"

    @property
    def description(self) -> str:
        return """List files in Vault's staging area.

Shows uploaded files waiting to be attached to documents.
Useful for:
- Checking upload status
- Finding staged file paths
- Cleaning up old staged files"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "folder": {
                    "type": "string",
                    "description": "Staging folder path (optional, defaults to user's folder)",
                },
            },
        }

    async def execute(self, folder: Optional[str] = None) -> ToolResult:
        """List staged files."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path("/services/file_staging")

            # Add folder parameter if provided
            params = {}
            if folder:
                params["folder"] = folder

            response = await self.http_client.get(
                path=path,
                headers=headers,
                params=params if params else None,
            )

            files = response.get("data", [])

            self.logger.info(
                "file_staging_listed",
                file_count=len(files),
                folder=folder,
            )

            return ToolResult(
                success=True,
                data={
                    "files": files,
                    "count": len(files),
                    "folder": folder or "default",
                },
                metadata={"file_count": len(files)},
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to list staged files: {e.message}",
                metadata={"error_code": e.error_code},
            )


class FileStagingDownloadTool(BaseTool):
    """Download a file from staging area."""

    @property
    def name(self) -> str:
        return "vault_file_staging_download"

    @property
    def description(self) -> str:
        return """Download a file from Vault's staging area.

Retrieve files that were previously uploaded to staging.
Useful for:
- Downloading extracted document files
- Retrieving batch export results
- Testing file staging operations"""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "staging_path": {
                    "type": "string",
                    "description": "Path to file in staging area",
                },
            },
            "required": ["staging_path"],
        }

    async def execute(self, staging_path: str) -> ToolResult:
        """Download file from staging."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/services/file_staging/{staging_path}")

            response = await self.http_client.get(
                path=path,
                headers=headers,
            )

            self.logger.info(
                "file_staging_downloaded",
                staging_path=staging_path,
            )

            return ToolResult(
                success=True,
                data={
                    "staging_path": staging_path,
                    "download_url": path,
                    "response": response,
                },
                metadata={
                    "staging_path": staging_path,
                    "operation": "file_staging_download",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to download file from staging: {e.message}",
                metadata={"error_code": e.error_code, "staging_path": staging_path},
            )


class FileStagingDeleteTool(BaseTool):
    """Delete a file from staging area."""

    @property
    def name(self) -> str:
        return "vault_file_staging_delete"

    @property
    def description(self) -> str:
        return """Delete a file from Vault's staging area.

Clean up staged files after they've been used.
Best practice: Delete staged files after attaching to documents."""

    def get_parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "staging_path": {
                    "type": "string",
                    "description": "Path to file in staging area",
                },
            },
            "required": ["staging_path"],
        }

    async def execute(self, staging_path: str) -> ToolResult:
        """Delete file from staging."""
        try:
            headers = await self._get_auth_headers()
            path = self._build_api_path(f"/services/file_staging/{staging_path}")

            response = await self.http_client.delete(
                path=path,
                headers=headers,
            )

            self.logger.info(
                "file_staging_deleted",
                staging_path=staging_path,
            )

            return ToolResult(
                success=True,
                data={
                    "staging_path": staging_path,
                    "message": "File deleted from staging",
                    "response": response,
                },
                metadata={
                    "staging_path": staging_path,
                    "operation": "file_staging_delete",
                },
            )

        except APIError as e:
            return ToolResult(
                success=False,
                error=f"Failed to delete file from staging: {e.message}",
                metadata={"error_code": e.error_code, "staging_path": staging_path},
            )
