# VeevaVault MCP Server

Model Context Protocol (MCP) server for Veeva Vault API integration. Enables LLMs to interact with Veeva Vault for document management, regulatory compliance, quality management, and clinical trial operations.

## Overview

This MCP server provides resource-oriented tools for interacting with Veeva Vault v25.2 API:
- **Documents**: Query, create, update, lifecycle management
- **Objects**: CRUD operations on custom Vault objects
- **VQL**: Execute Vault Query Language queries
- **Workflows**: Manage approval workflows and tasks
- **Binders**: Create and organize document binders
- **Users & Groups**: User provisioning and access management

## Features

- **Dual Authentication**: Username/password or OAuth2 with JWT validation
- **Flexible Caching**: In-memory or Valkey (Redis-compatible) backends
- **Prometheus Metrics**: Built-in observability for tool usage and performance
- **Structured Logging**: JSON-formatted logs with structlog
- **Type Safety**: Full Pydantic validation for all configurations and parameters
- **Rate Limiting**: Automatic rate limit handling with retries
- **Docker Ready**: Container deployment with Kubernetes migration path

## Installation

### Prerequisites

- Python 3.11 or higher
- Veeva Vault account with API access
- (Optional) Valkey/Redis instance for distributed caching

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/VeevaVaultMCP.git
cd VeevaVaultMCP/veevavault-mcp-server
```

2. Create virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your Vault credentials
```

5. Run the server:
```bash
python -m veevavault_mcp
```

## Configuration

Configuration is managed via environment variables. See `.env.example` for all options.

### Username/Password Authentication (Default)

```bash
VAULT_AUTH_MODE=username_password
VAULT_URL=https://your-vault.veevavault.com
VAULT_USERNAME=your.username@company.com
VAULT_PASSWORD=YourPassword123
```

### OAuth2 Authentication (Enterprise)

```bash
VAULT_AUTH_MODE=oauth2
VAULT_URL=https://your-vault.veevavault.com
VAULT_OAUTH2_TOKEN_URL=https://auth.company.com/oauth/token
VAULT_OAUTH2_JWKS_URL=https://auth.company.com/.well-known/jwks.json
VAULT_OAUTH2_AUDIENCE=vault-mcp-server
VAULT_SERVICE_ACCOUNT_USERNAME=service-bot@company.com
VAULT_SERVICE_ACCOUNT_PASSWORD=ServicePassword123
```

### Caching Configuration

**In-Memory Cache (Default):**
```bash
VAULT_ENABLE_CACHING=true
VAULT_CACHE_BACKEND=memory
VAULT_CACHE_TTL=300
```

**Valkey/Redis Cache:**
```bash
VAULT_ENABLE_CACHING=true
VAULT_CACHE_BACKEND=valkey
VAULT_CACHE_TTL=300
VAULT_VALKEY_URL=valkey://localhost:6379
VAULT_VALKEY_DB=0
```

## Usage Examples

### With Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/config.json` on macOS):

```json
{
  "mcpServers": {
    "veevavault": {
      "command": "/path/to/venv/bin/python",
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

### Example Prompts

**Document Management:**
```
"Show me all clinical study reports pending my review"
"Create a new protocol document for Study ABC-123"
"Update the therapeutic area to 'Oncology' for all Study ABC-123 documents"
```

**Regulatory Affairs:**
```
"Create an eCTD binder for Product X NDA submission to FDA"
"Show me all open health authority correspondence due in next 30 days"
"Export submission BINDER-12345 in eCTD 3.2.2 format"
```

**Quality Management:**
```
"Log a new deviation for manufacturing batch LOT-456"
"Show me all open CAPAs with overdue actions"
"Create investigation report for deviation DEV-789"
```

**VQL Queries:**
```
"Query all documents where lifecycle state is 'Approved' and product is 'Product X'"
"Find all quality events created in the last 30 days"
```

## Development

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=veevavault_mcp --cov-report=html

# Specific test file
pytest tests/test_config.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type checking
mypy src/
```

### Project Structure

```
veevavault-mcp-server/
├── src/veevavault_mcp/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── server.py            # MCP server implementation
│   ├── auth/                # Authentication managers
│   │   ├── __init__.py
│   │   ├── manager.py       # Base auth manager
│   │   ├── username_password.py
│   │   └── oauth2.py
│   ├── tools/               # MCP tools by resource
│   │   ├── __init__.py
│   │   ├── base.py          # BaseTool abstract class
│   │   ├── documents.py     # Document tools
│   │   ├── objects.py       # Object CRUD tools
│   │   ├── vql.py           # VQL execution tools
│   │   ├── workflows.py     # Workflow tools
│   │   ├── binders.py       # Binder tools
│   │   └── users.py         # User/group tools
│   ├── resources/           # Resource models
│   │   ├── __init__.py
│   │   ├── document.py
│   │   ├── object.py
│   │   └── workflow.py
│   ├── utils/               # Utilities
│   │   ├── __init__.py
│   │   ├── errors.py        # Exception hierarchy
│   │   ├── cache.py         # Cache backends
│   │   ├── http.py          # HTTP client
│   │   └── rate_limit.py    # Rate limiter
│   └── monitoring/          # Observability
│       ├── __init__.py
│       ├── metrics.py       # Prometheus metrics
│       └── logging.py       # Structured logging
├── tests/                   # Test suite
├── docs/                    # Documentation
├── scripts/                 # Utility scripts
└── pyproject.toml          # Project configuration
```

## Monitoring

### Prometheus Metrics

The server exposes Prometheus metrics on port 9090 (configurable):

- `vault_mcp_tool_calls_total{tool_name}` - Total tool invocations
- `vault_mcp_tool_duration_seconds{tool_name}` - Tool execution time
- `vault_mcp_cache_hits_total{backend}` - Cache hit count
- `vault_mcp_cache_misses_total{backend}` - Cache miss count
- `vault_mcp_api_errors_total{error_type}` - API error count

Access metrics at: `http://localhost:9090/metrics`

### Logging

Structured JSON logs to stdout. Configure log level via `VAULT_LOG_LEVEL`:

```bash
VAULT_LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
VAULT_LOG_FORMAT=json  # json or console
```

## Deployment

### Docker

```bash
docker build -t veevavault-mcp-server .
docker run -d \
  -e VAULT_URL=https://your-vault.veevavault.com \
  -e VAULT_USERNAME=your.username@company.com \
  -e VAULT_PASSWORD=YourPassword123 \
  -p 9090:9090 \
  veevavault-mcp-server
```

### Kubernetes

See `docs/kubernetes/` for deployment manifests.

## Roadmap

### Phase 1 (Week 1-5) - Foundation
- ✅ Configuration and authentication
- ✅ Error handling and logging
- ✅ Caching and metrics
- 🚧 Core tools: Documents, Objects, VQL (30 tools)

### Phase 2 (Week 6-8) - Workflows
- Workflow and task management tools
- Binder creation and organization
- Signature and approval tools

### Phase 3 (Week 9-10) - Administration
- User and group management
- Metadata configuration
- Audit trail and compliance reporting

### Phase 4 (Week 11-12) - Polish
- Comprehensive testing (80%+ coverage)
- Performance optimization
- Documentation and examples

## License

MIT License - see LICENSE file for details

## Support

- GitHub Issues: https://github.com/yourusername/VeevaVaultMCP/issues
- Documentation: https://github.com/yourusername/VeevaVaultMCP/tree/main/docs
- Veeva Vault API Docs: https://developer.veevavault.com/api/

## Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## Acknowledgments

- Built with [MCP SDK](https://github.com/anthropics/mcp) by Anthropic
- Designed for [Veeva Vault](https://www.veeva.com/products/vault-platform/) v25.2 API
