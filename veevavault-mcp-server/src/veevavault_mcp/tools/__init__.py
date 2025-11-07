"""MCP Tools for VeevaVault operations."""

from .base import BaseTool, ToolResult

# User management tools
from .users import (
    ListUsersTool,
    GetUserTool,
    CreateUserTool,
    UpdateUserTool,
)

# Group management tools
from .groups import (
    ListGroupsTool,
    GetGroupTool,
    CreateGroupTool,
    AddGroupMembersTool,
    RemoveGroupMembersTool,
)

# Metadata tools
from .metadata import (
    GetMetadataTool,
    ListObjectTypesTool,
    GetPicklistValuesTool,
)

# Audit trail tools
from .audit import (
    QueryAuditTrailTool,
    GetDocumentAuditTool,
    GetUserActivityTool,
)

# Document tools
from .documents import (
    DocumentsQueryTool,
    DocumentsGetTool,
    DocumentsCreateTool,
    DocumentsUpdateTool,
    DocumentsDeleteTool,
    DocumentsLockTool,
    DocumentsUnlockTool,
    DocumentsDownloadFileTool,
    DocumentsDownloadVersionFileTool,
    DocumentsBatchCreateTool,
    DocumentsBatchUpdateTool,
    DocumentsGetActionsTool,
    DocumentsExecuteActionTool,
    DocumentsUploadFileTool,
    DocumentsCreateVersionTool,
)

# Object tools
from .objects import (
    ObjectsQueryTool,
    ObjectsGetTool,
    ObjectsCreateTool,
    ObjectsUpdateTool,
    ObjectsBatchCreateTool,
    ObjectsBatchUpdateTool,
    ObjectsGetActionsTool,
    ObjectsExecuteActionTool,
)

# VQL tools
from .vql import (
    VQLExecuteTool,
    VQLValidateTool,
)

# File staging tools
from .file_staging import (
    FileStagingUploadTool,
    FileStagingListTool,
    FileStagingDownloadTool,
    FileStagingDeleteTool,
)

__all__ = [
    # Base
    "BaseTool",
    "ToolResult",
    # User management
    "ListUsersTool",
    "GetUserTool",
    "CreateUserTool",
    "UpdateUserTool",
    # Group management
    "ListGroupsTool",
    "GetGroupTool",
    "CreateGroupTool",
    "AddGroupMembersTool",
    "RemoveGroupMembersTool",
    # Metadata
    "GetMetadataTool",
    "ListObjectTypesTool",
    "GetPicklistValuesTool",
    # Audit
    "QueryAuditTrailTool",
    "GetDocumentAuditTool",
    "GetUserActivityTool",
    # Documents
    "DocumentsQueryTool",
    "DocumentsGetTool",
    "DocumentsCreateTool",
    "DocumentsUpdateTool",
    "DocumentsDeleteTool",
    "DocumentsLockTool",
    "DocumentsUnlockTool",
    "DocumentsDownloadFileTool",
    "DocumentsDownloadVersionFileTool",
    "DocumentsBatchCreateTool",
    "DocumentsBatchUpdateTool",
    "DocumentsGetActionsTool",
    "DocumentsExecuteActionTool",
    "DocumentsUploadFileTool",
    "DocumentsCreateVersionTool",
    # Objects
    "ObjectsQueryTool",
    "ObjectsGetTool",
    "ObjectsCreateTool",
    "ObjectsUpdateTool",
    "ObjectsBatchCreateTool",
    "ObjectsBatchUpdateTool",
    "ObjectsGetActionsTool",
    "ObjectsExecuteActionTool",
    # VQL
    "VQLExecuteTool",
    "VQLValidateTool",
    # File Staging
    "FileStagingUploadTool",
    "FileStagingListTool",
    "FileStagingDownloadTool",
    "FileStagingDeleteTool",
]
