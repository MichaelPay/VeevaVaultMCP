"""
VeevaVault MCP Server

Model Context Protocol (MCP) server for Veeva Vault API integration.
Enables LLMs to interact with Veeva Vault through standardized MCP tools.
"""

__version__ = "0.1.0"
__author__ = "VeevaVault MCP Team"
__license__ = "MIT"

from .config import Config, AuthMode
from .server import VeevaVaultMCPServer

__all__ = [
    "Config",
    "AuthMode",
    "VeevaVaultMCPServer",
    "__version__",
]
