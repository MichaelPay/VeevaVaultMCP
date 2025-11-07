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
)

# Object tools
from .objects import (
    ObjectsQueryTool,
    ObjectsGetTool,
    ObjectsCreateTool,
    ObjectsUpdateTool,
)

# VQL tools
from .vql import (
    VQLExecuteTool,
    VQLValidateTool,
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
    # Objects
    "ObjectsQueryTool",
    "ObjectsGetTool",
    "ObjectsCreateTool",
    "ObjectsUpdateTool",
    # VQL
    "VQLExecuteTool",
    "VQLValidateTool",
]
