# Getting Started with VeevaVault MCP Server

This guide will walk you through setting up and using the VeevaVault MCP Server from scratch.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [First Run](#first-run)
5. [Using with Claude Desktop](#using-with-claude-desktop)
6. [Your First Queries](#your-first-queries)
7. [Common Use Cases](#common-use-cases)
8. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, ensure you have:

### Required
- **Python 3.11 or higher**: Check with `python3 --version`
- **Veeva Vault Account**: With API access enabled
- **Vault Credentials**: Username and password (or OAuth2 setup)
- **Git**: For cloning the repository

### Optional
- **Claude Desktop**: For LLM integration
- **Docker**: For containerized deployment
- **Valkey/Redis**: For distributed caching (production)

### Verify Your Vault Access

1. Log into your Veeva Vault instance at: `https://your-vault.veevavault.com`
2. Verify you can access the API documentation at: `https://your-vault.veevavault.com/api/`
3. Note your Vault URL - you'll need this for configuration

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/VeevaVaultMCP.git
cd VeevaVaultMCP/veevavault-mcp-server
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
# Install the package with development dependencies
pip install -e ".[dev]"
```

This installs:
- Core MCP server and dependencies
- Testing tools (pytest, coverage)
- Code quality tools (black, ruff, mypy)
- Documentation tools

### Step 4: Verify Installation

```bash
python -m veevavault_mcp --help
```

You should see usage information (or an error about missing configuration - that's expected).

---

## Configuration

### Step 1: Create Configuration File

```bash
# Copy the example configuration
cp .env.example .env
```

### Step 2: Edit Configuration

Open `.env` in your favorite text editor:

```bash
# Use nano, vim, or any editor
nano .env
```

### Step 3: Configure Authentication

**For Username/Password (Recommended for Getting Started):**

```bash
# Authentication Mode
VAULT_AUTH_MODE=username_password

# Vault Connection
VAULT_URL=https://your-vault.veevavault.com

# Username/Password Authentication
VAULT_USERNAME=your.username@company.com
VAULT_PASSWORD=YourPassword123
```

Replace:
- `your-vault.veevavault.com` with your actual Vault URL
- `your.username@company.com` with your Vault username
- `YourPassword123` with your Vault password

**For OAuth2 (Advanced):**

See [README.md](README.md#oauth2-authentication-enterprise) for OAuth2 configuration.

### Step 4: Configure Optional Settings

**Caching (Recommended):**
```bash
VAULT_ENABLE_CACHING=true
VAULT_CACHE_BACKEND=memory  # Use 'valkey' for production
VAULT_CACHE_TTL=300  # 5 minutes
```

**Logging:**
```bash
VAULT_LOG_LEVEL=INFO  # DEBUG for troubleshooting
VAULT_LOG_FORMAT=json
```

**Monitoring:**
```bash
VAULT_ENABLE_METRICS=true
VAULT_METRICS_PORT=9090
```

Save and close the file.

---

## First Run

### Step 1: Test Configuration

```bash
python -m veevavault_mcp
```

The server should start and you'll see log output similar to:

```json
{"event": "server_starting", "auth_mode": "username_password", "timestamp": "2025-11-07T..."}
{"event": "auth_initialized", "vault_url": "https://your-vault.veevavault.com"}
{"event": "tools_registered", "tool_count": 58}
{"event": "server_ready", "listening": "stdio"}
```

### Step 2: Verify Tools Are Loaded

The log should show `"tool_count": 58` indicating all tools are available.

### Step 3: Test Authentication

The server will authenticate with Vault on first tool use. If authentication fails, you'll see an error in the logs.

Press `Ctrl+C` to stop the server.

---

## Using with Claude Desktop

Claude Desktop can use the MCP server to interact with Veeva Vault.

### Step 1: Locate Claude Desktop Config

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Edit Configuration

Open the config file and add the VeevaVault MCP server:

```json
{
  "mcpServers": {
    "veevavault": {
      "command": "/full/path/to/venv/bin/python",
      "args": ["-m", "veevavault_mcp"],
      "env": {
        "VAULT_URL": "https://your-vault.veevavault.com",
        "VAULT_USERNAME": "your.username@company.com",
        "VAULT_PASSWORD": "YourPassword123",
        "VAULT_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Important:**
- Use the FULL path to your Python binary in the venv
- Find it with: `which python` (after activating venv)
- Example: `/Users/yourname/VeevaVaultMCP/veevavault-mcp-server/venv/bin/python`

### Step 3: Restart Claude Desktop

Quit and restart Claude Desktop completely.

### Step 4: Verify Connection

In Claude Desktop, type:

```
"Can you list the VeevaVault tools available?"
```

Claude should respond with a list of the 58 available tools.

---

## Your First Queries

Now that everything is set up, try these examples:

### Example 1: Query Documents

```
"Show me all documents in draft state"
```

Claude will use the `vault_documents_query` tool to search for draft documents.

### Example 2: Get Document Details

```
"Get details for document ID 12345"
```

Claude uses `vault_documents_get` to retrieve full document information.

### Example 3: List Workflows

```
"What workflows are available in the vault?"
```

Claude uses `vault_workflows_list` to show all active workflows.

### Example 4: Check Your Tasks

```
"Show me my pending tasks"
```

Claude uses `vault_tasks_list` to display your open tasks.

### Example 5: Execute VQL Query

```
"Execute this VQL: SELECT id, name__v, type__v FROM documents WHERE created_date__v >= '2025-01-01' LIMIT 10"
```

Claude uses `vault_vql_execute` to run the query and return results.

---

## Common Use Cases

### Document Management

**Find and Review Documents:**
```
"Find all protocol documents for Study ABC-123 that are pending my review"
```

**Create a Document:**
```
"Create a new clinical study report titled 'Phase 3 Results' for Product X in the base lifecycle"
```

**Update Document Metadata:**
```
"Update document 12345 to set the therapeutic area to 'Cardiology'"
```

**Approve a Document:**
```
"Get the workflow details for document 12345, then approve it with comment 'Ready for submission'"
```

### Task Management

**Review Task Queue:**
```
"Show me all my open tasks sorted by due date"
```

**Complete a Task:**
```
"Get details for task T-67890, then complete it with approval verdict and comment 'Document reviewed and approved'"
```

**Reassign a Task:**
```
"Reassign task T-67890 to user ID 54321"
```

### Quality Management

**Query Quality Events:**
```
"Find all open quality events created in the last 30 days"
```

**Create Quality Event:**
```
"Create a new quality event for manufacturing deviation in batch LOT-789"
```

### Data Analysis

**Advanced Queries:**
```
"Execute VQL to find all documents where lifecycle_state is 'Approved' and product contains 'Product X' from the last quarter"
```

**Audit Trail:**
```
"Show me all document deletions in the past 7 days"
```

### Batch Operations

**Bulk Updates:**
```
"Update all documents in Study ABC-123 to set the new study phase to 'Phase 3'"
```

**Batch Creation:**
```
"Create 20 training documents from this list with sequential names"
```

---

## Next Steps

### Learn More

- **Tool Reference**: See [TOOLS_REFERENCE.md](TOOLS_REFERENCE.md) for complete tool documentation
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- **Configuration**: See [README.md](README.md) for advanced configuration options

### Advanced Features

**Caching:**
- Set up Valkey/Redis for production caching
- Configure cache TTL based on data volatility
- Monitor cache hit rates via Prometheus metrics

**Monitoring:**
- Access Prometheus metrics at `http://localhost:9090/metrics`
- Set up Grafana dashboards for visualization
- Monitor tool usage, latency, and error rates

**Production Deployment:**
- Deploy with Docker: See [README.md](README.md#docker)
- Kubernetes deployment: See `docs/kubernetes/`
- Configure OAuth2 for enterprise authentication

### Best Practices

1. **Security:**
   - Never commit `.env` files to git
   - Use OAuth2 for production environments
   - Rotate credentials regularly
   - Enable audit logging

2. **Performance:**
   - Use batch operations for bulk changes
   - Enable caching for read-heavy workloads
   - Use `auto_paginate` carefully (can return thousands of records)
   - Leverage VQL for complex queries instead of multiple tool calls

3. **Error Handling:**
   - Check workflow state before executing actions
   - Review batch operation results for partial failures
   - Monitor logs for authentication issues
   - Use `vault_documents_get_actions` before executing document actions

4. **Development:**
   - Run tests before deploying: `pytest`
   - Check code coverage: `pytest --cov`
   - Lint code: `black src/ && ruff check src/`
   - Review logs in DEBUG mode during development

---

## Getting Help

### Resources

- **GitHub Issues**: https://github.com/yourusername/VeevaVaultMCP/issues
- **Documentation**: All docs in the repository root
- **Veeva Vault API**: https://developer.veevavault.com/api/

### Common Questions

**Q: "Tools not showing up in Claude Desktop"**
A: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#tools-not-available)

**Q: "Authentication failing"**
A: Verify credentials, check Vault URL, ensure API access is enabled

**Q: "Queries returning no results"**
A: Check VQL syntax, verify data exists, review filter parameters

**Q: "File upload not working"**
A: FileStagingUploadTool is not yet fully implemented (see tool description)

### Support Channels

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Search existing GitHub issues
3. Create a new issue with:
   - Your configuration (without passwords!)
   - Error messages from logs
   - Steps to reproduce
   - Expected vs actual behavior

---

## Quick Reference Card

```bash
# Start server
python -m veevavault_mcp

# Run tests
pytest

# Check code
black src/ tests/
ruff check src/ tests/

# View metrics
curl http://localhost:9090/metrics

# Activate venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Update dependencies
pip install -e ".[dev]"
```

---

**Congratulations!** You're now ready to use the VeevaVault MCP Server. Start with simple queries and explore the 58 available tools as you get comfortable.

For detailed tool documentation, see [TOOLS_REFERENCE.md](TOOLS_REFERENCE.md).
