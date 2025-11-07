"""
VeevaVault MCP Server
Main server implementation with MCP SDK integration.
"""

from typing import Optional, Sequence
import asyncio
import structlog
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .config import Config, AuthMode
from .auth.manager import AuthenticationManager
from .auth.username_password import UsernamePasswordAuthManager
from .utils.http import VaultHTTPClient
from .tools.base import BaseTool, ToolResult

# Import all tool classes
from .tools.users import (
    ListUsersTool,
    GetUserTool,
    CreateUserTool,
    UpdateUserTool,
)
from .tools.groups import (
    ListGroupsTool,
    GetGroupTool,
    CreateGroupTool,
    AddGroupMembersTool,
    RemoveGroupMembersTool,
)
from .tools.metadata import (
    GetMetadataTool,
    ListObjectTypesTool,
    GetPicklistValuesTool,
)
from .tools.audit import (
    QueryAuditTrailTool,
    GetDocumentAuditTool,
    GetUserActivityTool,
)
from .tools.documents import (
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
    DocumentsAttachmentsListTool,
    DocumentsAttachmentsUploadTool,
    DocumentsAttachmentsDownloadTool,
    DocumentsAttachmentsDeleteTool,
    DocumentsRenditionsListTool,
    DocumentsRenditionsGenerateTool,
    DocumentsRenditionsDownloadTool,
    DocumentsRenditionsDeleteTool,
)
from .tools.objects import (
    ObjectsQueryTool,
    ObjectsGetTool,
    ObjectsCreateTool,
    ObjectsUpdateTool,
    ObjectsBatchCreateTool,
    ObjectsBatchUpdateTool,
    ObjectsGetActionsTool,
    ObjectsExecuteActionTool,
)
from .tools.vql import (
    VQLExecuteTool,
    VQLValidateTool,
)
from .tools.file_staging import (
    FileStagingUploadTool,
    FileStagingListTool,
    FileStagingDownloadTool,
    FileStagingDeleteTool,
)
from .tools.workflows import (
    WorkflowsListTool,
    WorkflowsGetTool,
    DocumentsGetWorkflowDetailsTool,
)
from .tools.tasks import (
    TasksListTool,
    TasksGetTool,
    TasksExecuteActionTool,
)

logger = structlog.get_logger(__name__)


class VeevaVaultMCPServer:
    """
    Main MCP server implementation for Veeva Vault.

    Provides tools for LLMs to interact with Veeva Vault API including:
    - User and group management
    - Document operations
    - Object CRUD
    - VQL queries
    - Metadata discovery
    - Audit trail queries
    """

    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the MCP server.

        Args:
            config: Server configuration (loads from env if not provided)
        """
        self.config = config or Config()
        self.config.validate_auth_config()

        # MCP server instance
        self.mcp_server = Server("veevavault-mcp-server")

        # Core components
        self.auth_manager: Optional[AuthenticationManager] = None
        self.http_client: Optional[VaultHTTPClient] = None

        # Tool registry
        self.tools: dict[str, BaseTool] = {}

        # Logger
        self.logger = logger.bind(
            server="veevavault-mcp",
            vault_url=self.config.url,
            auth_mode=self.config.auth_mode.value,
        )

    async def initialize(self) -> None:
        """Initialize server components."""
        self.logger.info("server_initializing")

        # Initialize authentication manager
        if self.config.auth_mode == AuthMode.USERNAME_PASSWORD:
            self.auth_manager = UsernamePasswordAuthManager(self.config)
        else:
            raise NotImplementedError("OAuth2 authentication not yet implemented")

        # Initialize HTTP client
        self.http_client = VaultHTTPClient(
            base_url=self.config.url,
            timeout=30,
            max_retries=3,
        )
        await self.http_client.__aenter__()

        # Register all tools
        self._register_tools()

        # Set up MCP handlers
        self._setup_handlers()

        self.logger.info("server_initialized", tool_count=len(self.tools))

    def _register_tools(self) -> None:
        """Register all available tools with the server."""
        self.logger.info("registering_tools")

        # User management tools
        self._register_tool(ListUsersTool)
        self._register_tool(GetUserTool)
        self._register_tool(CreateUserTool)
        self._register_tool(UpdateUserTool)

        # Group management tools
        self._register_tool(ListGroupsTool)
        self._register_tool(GetGroupTool)
        self._register_tool(CreateGroupTool)
        self._register_tool(AddGroupMembersTool)
        self._register_tool(RemoveGroupMembersTool)

        # Metadata tools
        self._register_tool(GetMetadataTool)
        self._register_tool(ListObjectTypesTool)
        self._register_tool(GetPicklistValuesTool)

        # Audit trail tools
        self._register_tool(QueryAuditTrailTool)
        self._register_tool(GetDocumentAuditTool)
        self._register_tool(GetUserActivityTool)

        # Document tools
        self._register_tool(DocumentsQueryTool)
        self._register_tool(DocumentsGetTool)
        self._register_tool(DocumentsCreateTool)
        self._register_tool(DocumentsUpdateTool)
        self._register_tool(DocumentsDeleteTool)
        self._register_tool(DocumentsLockTool)
        self._register_tool(DocumentsUnlockTool)
        self._register_tool(DocumentsDownloadFileTool)
        self._register_tool(DocumentsDownloadVersionFileTool)
        self._register_tool(DocumentsBatchCreateTool)
        self._register_tool(DocumentsBatchUpdateTool)
        self._register_tool(DocumentsGetActionsTool)
        self._register_tool(DocumentsExecuteActionTool)
        self._register_tool(DocumentsUploadFileTool)
        self._register_tool(DocumentsCreateVersionTool)
        self._register_tool(DocumentsAttachmentsListTool)
        self._register_tool(DocumentsAttachmentsUploadTool)
        self._register_tool(DocumentsAttachmentsDownloadTool)
        self._register_tool(DocumentsAttachmentsDeleteTool)
        self._register_tool(DocumentsRenditionsListTool)
        self._register_tool(DocumentsRenditionsGenerateTool)
        self._register_tool(DocumentsRenditionsDownloadTool)
        self._register_tool(DocumentsRenditionsDeleteTool)

        # Object tools
        self._register_tool(ObjectsQueryTool)
        self._register_tool(ObjectsGetTool)
        self._register_tool(ObjectsCreateTool)
        self._register_tool(ObjectsUpdateTool)
        self._register_tool(ObjectsBatchCreateTool)
        self._register_tool(ObjectsBatchUpdateTool)
        self._register_tool(ObjectsGetActionsTool)
        self._register_tool(ObjectsExecuteActionTool)

        # VQL tools
        self._register_tool(VQLExecuteTool)
        self._register_tool(VQLValidateTool)

        # File staging tools
        self._register_tool(FileStagingUploadTool)
        self._register_tool(FileStagingListTool)
        self._register_tool(FileStagingDownloadTool)
        self._register_tool(FileStagingDeleteTool)

        # Workflow tools
        self._register_tool(WorkflowsListTool)
        self._register_tool(WorkflowsGetTool)
        self._register_tool(DocumentsGetWorkflowDetailsTool)

        # Task tools
        self._register_tool(TasksListTool)
        self._register_tool(TasksGetTool)
        self._register_tool(TasksExecuteActionTool)

        self.logger.info("tools_registered", count=len(self.tools))

    def _register_tool(self, tool_class: type[BaseTool]) -> None:
        """
        Register a single tool with the server.

        Args:
            tool_class: Tool class to instantiate and register
        """
        tool_instance = tool_class(self.auth_manager, self.http_client)
        self.tools[tool_instance.name] = tool_instance

        self.logger.debug(
            "tool_registered",
            name=tool_instance.name,
            description=tool_instance.description[:50] + "...",
        )

    def _setup_handlers(self) -> None:
        """Set up MCP protocol handlers."""

        @self.mcp_server.list_tools()
        async def list_tools() -> list[Tool]:
            """List all available tools."""
            self.logger.info("list_tools_called")

            tools = []
            for tool_name, tool_instance in self.tools.items():
                tools.append(
                    Tool(
                        name=tool_name,
                        description=tool_instance.description,
                        inputSchema=tool_instance.get_parameters_schema(),
                    )
                )

            return tools

        @self.mcp_server.call_tool()
        async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
            """
            Execute a tool with given arguments.

            Args:
                name: Tool name
                arguments: Tool arguments

            Returns:
                Tool execution results
            """
            self.logger.info("tool_called", tool=name, args_count=len(arguments))

            # Get tool instance
            tool = self.tools.get(name)
            if not tool:
                error_msg = f"Unknown tool: {name}"
                self.logger.error("tool_not_found", tool=name)
                return [TextContent(type="text", text=f"Error: {error_msg}")]

            try:
                # Execute tool
                result: ToolResult = await tool.run(**arguments)

                # Format result
                if result.success:
                    # Success - return data as formatted text
                    import json
                    result_text = json.dumps(result.data, indent=2)

                    self.logger.info(
                        "tool_executed_successfully",
                        tool=name,
                        duration=result.metadata.get("duration_seconds"),
                    )

                    return [TextContent(type="text", text=result_text)]
                else:
                    # Error - return error message
                    error_text = f"Error: {result.error}"
                    if result.metadata:
                        error_text += f"\nMetadata: {result.metadata}"

                    self.logger.warning(
                        "tool_execution_failed",
                        tool=name,
                        error=result.error,
                    )

                    return [TextContent(type="text", text=error_text)]

            except Exception as e:
                error_msg = f"Tool execution failed: {str(e)}"
                self.logger.error(
                    "tool_execution_exception",
                    tool=name,
                    error=str(e),
                    error_type=type(e).__name__,
                )
                return [TextContent(type="text", text=f"Error: {error_msg}")]

    async def run(self) -> None:
        """
        Run the MCP server.

        This starts the server and handles stdio communication.
        """
        self.logger.info("server_starting")

        try:
            # Initialize server components
            await self.initialize()

            # Run server with stdio transport
            async with stdio_server() as (read_stream, write_stream):
                self.logger.info("server_running", transport="stdio")

                await self.mcp_server.run(
                    read_stream,
                    write_stream,
                    self.mcp_server.create_initialization_options(),
                )

        except Exception as e:
            self.logger.error(
                "server_error",
                error=str(e),
                error_type=type(e).__name__,
            )
            raise
        finally:
            await self.cleanup()

    async def cleanup(self) -> None:
        """Clean up server resources."""
        self.logger.info("server_cleanup_starting")

        try:
            # Close HTTP client
            if self.http_client:
                await self.http_client.__aexit__(None, None, None)

            # Close auth manager
            if self.auth_manager and hasattr(self.auth_manager, 'close'):
                await self.auth_manager.close()

            self.logger.info("server_cleanup_complete")

        except Exception as e:
            self.logger.error(
                "cleanup_error",
                error=str(e),
                error_type=type(e).__name__,
            )


async def main():
    """Main entry point for the MCP server."""
    # Set up logging
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Create and run server
    server = VeevaVaultMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
