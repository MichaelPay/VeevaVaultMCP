"""
VeevaVault MCP Server
Main server implementation (stub for now).
"""

from typing import Optional
from .config import Config


class VeevaVaultMCPServer:
    """
    Main MCP server implementation.
    Placeholder stub - will be implemented in Week 2.
    """

    def __init__(self, config: Optional[Config] = None):
        """Initialize the MCP server."""
        self.config = config or Config()
        self.config.validate_auth_config()

    async def start(self):
        """Start the MCP server."""
        raise NotImplementedError("Server implementation coming in Week 2")

    async def stop(self):
        """Stop the MCP server."""
        raise NotImplementedError("Server implementation coming in Week 2")
