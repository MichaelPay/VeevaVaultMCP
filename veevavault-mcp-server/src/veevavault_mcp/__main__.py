"""
Entry point for running VeevaVault MCP Server as a module.

Usage:
    python -m veevavault_mcp
"""

import asyncio
from .server import main

if __name__ == "__main__":
    asyncio.run(main())
