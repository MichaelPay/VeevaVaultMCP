# Troubleshooting Guide

Common issues and solutions for the VeevaVault MCP Server.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Authentication Problems](#authentication-problems)
- [Claude Desktop Integration](#claude-desktop-integration)
- [Tool Execution Errors](#tool-execution-errors)
- [Performance Issues](#performance-issues)
- [Network and Connectivity](#network-and-connectivity)
- [Configuration Problems](#configuration-problems)
- [Logging and Debugging](#logging-and-debugging)

---

## Installation Issues

### Python Version Error

**Problem:**
```
ERROR: This package requires Python 3.11 or higher
```

**Solution:**
```bash
# Check your Python version
python3 --version

# If < 3.11, install Python 3.11+
# macOS (using Homebrew):
brew install python@3.11

# Ubuntu/Debian:
sudo apt-get install python3.11

# Then create venv with specific version:
python3.11 -m venv venv
```

### Package Installation Fails

**Problem:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Then retry installation
pip install -e ".[dev]"

# If still failing, install without dev dependencies
pip install -e .
```

### Virtual Environment Issues

**Problem:**
```
Command 'python' not found OR packages not found
```

**Solution:**
```bash
# Ensure virtual environment is activated
# You should see (venv) in your prompt

# If not activated:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Verify activation
which python  # Should point to venv/bin/python
```

---

## Authentication Problems

### Invalid Credentials

**Problem:**
```
{"event": "auth_failed", "error": "Invalid username or password"}
```

**Solution:**
1. Verify credentials in `.env`:
   ```bash
   VAULT_USERNAME=your.username@company.com
   VAULT_PASSWORD=YourPassword123
   ```

2. Test login manually:
   - Visit `https://your-vault.veevavault.com`
   - Try logging in with same credentials
   - If login fails, reset password

3. Check for special characters:
   - If password contains `$`, `!`, `\`, wrap in single quotes
   - Example: `VAULT_PASSWORD='P@ssw0rd!123'`

### Session Expired

**Problem:**
```
{"event": "api_error", "error_code": "INVALID_SESSION_ID"}
```

**Solution:**
- Session auto-refresh is enabled by default
- If still occurring, restart the MCP server
- Check if account is locked or disabled in Vault

### OAuth2 Token Issues

**Problem:**
```
{"event": "oauth_token_error", "error": "Invalid token"}
```

**Solution:**
1. Verify OAuth2 configuration in `.env`:
   ```bash
   VAULT_AUTH_MODE=oauth2
   VAULT_OAUTH2_TOKEN_URL=https://auth.company.com/oauth/token
   VAULT_OAUTH2_JWKS_URL=https://auth.company.com/.well-known/jwks.json
   VAULT_OAUTH2_AUDIENCE=vault-mcp-server
   ```

2. Check service account credentials:
   ```bash
   VAULT_SERVICE_ACCOUNT_USERNAME=service-bot@company.com
   VAULT_SERVICE_ACCOUNT_PASSWORD=ServicePassword123
   ```

3. Verify JWKS URL is accessible:
   ```bash
   curl https://auth.company.com/.well-known/jwks.json
   ```

### API Access Disabled

**Problem:**
```
{"error": "API access is disabled for this account"}
```

**Solution:**
- Contact your Vault administrator
- Request API access be enabled for your account
- Verify your security profile includes API permissions

---

## Claude Desktop Integration

### Tools Not Available

**Problem:**
Claude says "I don't have access to VeevaVault tools"

**Solution:**

1. **Check Claude Desktop Config**:
   ```json
   {
     "mcpServers": {
       "veevavault": {
         "command": "/full/path/to/venv/bin/python",
         "args": ["-m", "veevavault_mcp"],
         "env": {
           "VAULT_URL": "https://your-vault.veevavault.com",
           "VAULT_USERNAME": "your.username@company.com",
           "VAULT_PASSWORD": "YourPassword123"
         }
       }
     }
   }
   ```

2. **Verify Python Path**:
   ```bash
   # Activate venv
   source venv/bin/activate

   # Get full path
   which python
   # Copy this EXACT path to config
   ```

3. **Check Config Location**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

4. **Restart Claude Desktop**:
   - Quit completely (not just close window)
   - Restart application
   - Wait 10-15 seconds for server to initialize

5. **Check Server Logs**:
   ```bash
   # Enable debug logging in Claude config
   "env": {
     "VAULT_LOG_LEVEL": "DEBUG",
     ...
   }
   ```

### Server Won't Start

**Problem:**
Claude Desktop shows error or server not responding

**Solution:**

1. **Test server manually**:
   ```bash
   # Activate venv
   source venv/bin/activate

   # Run server
   python -m veevavault_mcp

   # Should see startup logs
   # Press Ctrl+C to stop
   ```

2. **Check for errors**:
   - Look for Python errors
   - Verify `.env` exists and is configured
   - Check for port conflicts

3. **Verify dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

### Slow Response Times

**Problem:**
Tools take a long time to respond in Claude Desktop

**Solution:**

1. **Enable caching**:
   ```bash
   VAULT_ENABLE_CACHING=true
   VAULT_CACHE_BACKEND=memory
   VAULT_CACHE_TTL=300
   ```

2. **Check network latency**:
   ```bash
   # Test connection to Vault
   curl -w "Time: %{time_total}s\n" https://your-vault.veevavault.com/api/
   ```

3. **Reduce result sizes**:
   - Use smaller `limit` values in queries
   - Avoid `auto_paginate=true` for large datasets
   - Use specific filters instead of broad queries

---

## Tool Execution Errors

### Query Returns No Results

**Problem:**
```
{"success": true, "data": {"documents": [], "count": 0}}
```

**Solution:**

1. **Verify data exists**:
   - Log into Vault web UI
   - Check if documents matching criteria exist
   - Verify field names and values

2. **Check VQL syntax**:
   ```
   # Correct
   "name__v CONTAINS ('protocol')"

   # Incorrect
   "name__v LIKE '%protocol%'"  # LIKE not supported, use CONTAINS
   ```

3. **Case sensitivity**:
   - Field names are case-sensitive: `name__v` not `Name__v`
   - Values may be case-sensitive depending on field type

4. **Field naming**:
   - Standard fields end in `__v`: `name__v`, `type__v`
   - Custom fields end in `__c`: `custom_field__c`

### Workflow Action Failed

**Problem:**
```
{"error": "Action not available in current state"}
```

**Solution:**

1. **Check available actions first**:
   ```
   "Get available actions for document 12345"
   ```

2. **Verify document state**:
   ```
   "Get workflow details for document 12345"
   ```

3. **Check permissions**:
   - Ensure you have permission to perform the action
   - Some actions require specific roles

4. **Review required fields**:
   - Some actions need additional data (comments, verdicts)
   - Use `vault_documents_get_actions` to see requirements

### File Upload Not Working

**Problem:**
```
{"error": "File upload not yet implemented"}
```

**Solution:**
- `FileStagingUploadTool` is a placeholder
- Currently does NOT perform actual file uploads
- For file uploads:
  - Use Vault web UI
  - Or implement multipart/form-data handling
  - Or wait for future implementation

### Batch Operation Partial Failure

**Problem:**
```
{"success": false, "successes": 45, "failures": 5}
```

**Solution:**

1. **Review batch results**:
   ```json
   {
     "results": [
       {"responseStatus": "SUCCESS", "id": 123},
       {"responseStatus": "FAILURE", "errors": [{"message": "..."}]}
     ]
   }
   ```

2. **Common failure reasons**:
   - Required fields missing
   - Invalid field values
   - Duplicate names
   - Permission issues

3. **Retry failures**:
   - Extract failed records from results
   - Fix data issues
   - Retry with corrected data

---

## Performance Issues

### Queries Taking Too Long

**Problem:**
Queries take > 5 seconds to return results

**Solution:**

1. **Add indexes to frequently queried fields** (Vault admin task)

2. **Use specific filters**:
   ```
   # Slow - queries everything
   SELECT * FROM documents WHERE id > 0

   # Fast - specific filters
   SELECT id, name__v FROM documents
   WHERE type__v = 'protocol__c'
   AND created_date__v >= '2025-01-01'
   LIMIT 100
   ```

3. **Avoid auto-pagination on large datasets**:
   ```bash
   # This could take minutes
   auto_paginate=true on query returning 10,000 records

   # Better approach
   auto_paginate=false, limit=100
   # Then paginate manually if needed
   ```

4. **Enable caching**:
   ```bash
   VAULT_ENABLE_CACHING=true
   VAULT_CACHE_TTL=300  # 5 minutes
   ```

### Memory Usage High

**Problem:**
Server using excessive memory

**Solution:**

1. **Avoid fetching large result sets**:
   - Use pagination instead of auto_paginate
   - Reduce limit values
   - Filter data server-side with VQL

2. **Clear cache periodically**:
   - Restart server if using memory cache
   - Use Valkey/Redis for production (bounded memory)

3. **Monitor with metrics**:
   ```bash
   curl http://localhost:9090/metrics
   ```

### Rate Limiting

**Problem:**
```
{"error": "RATE_LIMIT_EXCEEDED"}
```

**Solution:**

1. **Reduce request frequency**:
   - Use batch operations instead of individual calls
   - Increase cache TTL to reduce API calls
   - Add delays between large operations

2. **Check Vault rate limits**:
   - Contact Vault admin for rate limit details
   - May need to request higher limits

3. **Enable rate limiting in config**:
   ```bash
   VAULT_RATE_LIMIT_ENABLED=true
   VAULT_RATE_LIMIT_CALLS=100  # Per window
   ```

---

## Network and Connectivity

### Connection Timeout

**Problem:**
```
{"error": "Connection timeout"}
```

**Solution:**

1. **Verify Vault URL**:
   ```bash
   # Should be reachable
   curl https://your-vault.veevavault.com/api/
   ```

2. **Check firewall/proxy**:
   - Ensure outbound HTTPS allowed
   - Configure proxy if needed:
     ```bash
     export HTTPS_PROXY=http://proxy.company.com:8080
     ```

3. **Test DNS resolution**:
   ```bash
   nslookup your-vault.veevavault.com
   ```

4. **Verify VPN if required**:
   - Some Vaults require VPN connection
   - Connect to VPN before starting server

### SSL Certificate Errors

**Problem:**
```
{"error": "SSL: CERTIFICATE_VERIFY_FAILED"}
```

**Solution:**

1. **Update CA certificates**:
   ```bash
   # macOS
   brew install ca-certificates

   # Ubuntu/Debian
   sudo apt-get install ca-certificates
   ```

2. **For corporate proxies with SSL inspection**:
   - Install corporate CA certificate
   - Or (NOT recommended for production):
     ```bash
     export PYTHONHTTPSVERIFY=0
     ```

### Connection Refused

**Problem:**
```
{"error": "Connection refused"}
```

**Solution:**

1. **Verify Vault is accessible**:
   - Log into Vault web UI
   - Check if Vault is under maintenance

2. **Check URL format**:
   ```bash
   # Correct
   VAULT_URL=https://your-vault.veevavault.com

   # Wrong (no trailing slash)
   VAULT_URL=https://your-vault.veevavault.com/

   # Wrong (includes /api)
   VAULT_URL=https://your-vault.veevavault.com/api
   ```

---

## Configuration Problems

### Environment Variables Not Loading

**Problem:**
Server not reading `.env` file

**Solution:**

1. **Verify .env location**:
   ```bash
   ls -la .env
   # Should be in project root
   ```

2. **Check file format**:
   ```bash
   # Correct
   VAULT_URL=https://your-vault.veevavault.com

   # Wrong (spaces)
   VAULT_URL = https://your-vault.veevavault.com

   # Wrong (quotes when not needed)
   VAULT_URL="https://your-vault.veevavault.com"
   ```

3. **Test loading**:
   ```python
   from veevavault_mcp.config import load_config
   config = load_config()
   print(config.vault_url)
   ```

### Cache Configuration Issues

**Problem:**
```
{"error": "Failed to connect to cache backend"}
```

**Solution:**

1. **For memory cache** (default):
   ```bash
   VAULT_CACHE_BACKEND=memory
   # No other config needed
   ```

2. **For Valkey/Redis**:
   ```bash
   # Verify Valkey is running
   redis-cli -h localhost -p 6379 ping
   # Should return PONG

   # Configure in .env
   VAULT_CACHE_BACKEND=valkey
   VAULT_VALKEY_URL=valkey://localhost:6379
   VAULT_VALKEY_DB=0
   ```

3. **Disable caching for testing**:
   ```bash
   VAULT_ENABLE_CACHING=false
   ```

---

## Logging and Debugging

### Enable Debug Logging

```bash
# In .env file
VAULT_LOG_LEVEL=DEBUG
VAULT_LOG_FORMAT=console  # Easier to read than json

# Or in Claude Desktop config
"env": {
  "VAULT_LOG_LEVEL": "DEBUG",
  "VAULT_LOG_FORMAT": "console"
}
```

### View Structured Logs

```bash
# Logs are JSON by default
# Pipe through jq for formatting
python -m veevavault_mcp 2>&1 | jq .

# Filter for errors only
python -m veevavault_mcp 2>&1 | jq 'select(.level=="ERROR")'

# Filter for specific tool
python -m veevavault_mcp 2>&1 | jq 'select(.tool_name=="vault_documents_query")'
```

### Common Log Messages

**Normal startup**:
```json
{"event": "server_starting", "auth_mode": "username_password"}
{"event": "auth_initialized", "vault_url": "https://..."}
{"event": "tools_registered", "tool_count": 58}
{"event": "server_ready"}
```

**Authentication success**:
```json
{"event": "session_created", "session_id": "..."}
```

**Tool execution**:
```json
{"event": "tool_called", "tool_name": "vault_documents_query"}
{"event": "tool_completed", "duration_seconds": 0.234}
```

**Errors to investigate**:
```json
{"level": "ERROR", "event": "auth_failed"}
{"level": "ERROR", "event": "api_error", "error_code": "..."}
{"level": "ERROR", "event": "tool_failed", "tool_name": "..."}
```

### Test Individual Tools

```python
# Create test script: test_tool.py
import asyncio
from veevavault_mcp.config import load_config
from veevavault_mcp.auth.username_password import UsernamePasswordAuthManager
from veevavault_mcp.utils.http import HTTPClient
from veevavault_mcp.tools.documents import DocumentsQueryTool

async def test():
    config = load_config()
    auth = UsernamePasswordAuthManager(config)
    http = HTTPClient(config, auth)

    tool = DocumentsQueryTool(auth, http)
    result = await tool.execute(limit=5)

    print(f"Success: {result.success}")
    print(f"Data: {result.data}")

asyncio.run(test())
```

Run it:
```bash
python test_tool.py
```

---

## Getting More Help

### Before Creating an Issue

1. **Check documentation**:
   - [README.md](README.md)
   - [GETTING_STARTED.md](GETTING_STARTED.md)
   - [TOOLS_REFERENCE.md](TOOLS_REFERENCE.md)

2. **Search existing issues**:
   - https://github.com/yourusername/VeevaVaultMCP/issues

3. **Gather information**:
   - Error messages from logs
   - Steps to reproduce
   - Configuration (sanitized - no passwords!)
   - Python version: `python --version`
   - Package version: `pip show veevavault-mcp`

### Creating a Good Issue

Include:

```markdown
## Description
Brief description of the problem

## Steps to Reproduce
1. Configure server with...
2. Run command...
3. See error...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: macOS 14.2
- Python: 3.11.5
- Package version: 1.0.0
- Vault version: v25.2

## Logs
```
<paste relevant log output here>
```

## Configuration (sanitized)
```bash
VAULT_URL=https://my-vault.veevavault.com
VAULT_AUTH_MODE=username_password
# (removed credentials)
```
```

### Community Support

- GitHub Issues: https://github.com/yourusername/VeevaVaultMCP/issues
- Documentation: All docs in repository root
- Veeva Vault API Docs: https://developer.veevavault.com/api/

---

## Quick Diagnostic Checklist

When something's not working, check:

- [ ] Virtual environment is activated
- [ ] Python 3.11+ installed: `python --version`
- [ ] Dependencies installed: `pip install -e ".[dev]"`
- [ ] .env file exists and configured
- [ ] Vault URL correct (no trailing slash)
- [ ] Credentials valid (test login in web UI)
- [ ] API access enabled for your account
- [ ] Network connectivity to Vault
- [ ] Claude Desktop config has full Python path
- [ ] Claude Desktop restarted after config changes
- [ ] Logs show server starting successfully
- [ ] Logs show 58 tools registered

If all above pass and still not working, check logs with DEBUG level and create an issue.
