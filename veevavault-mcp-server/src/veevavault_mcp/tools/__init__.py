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
]
