# Logging in VeevaVaultMCP

VeevaVaultMCP uses Python's built-in `logging` module to provide detailed information about API calls, errors, and operations.

## Quick Start

By default, logging is not configured. To enable logging in your application:

```python
import logging
from veevavault import VaultClient, AuthenticationService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Use the library as normal
client = VaultClient()
auth = AuthenticationService(client)
# ... your code ...
```

## Log Levels

VeevaVaultMCP uses the following log levels:

- **DEBUG**: Detailed information about API calls (request URLs, response status codes)
- **INFO**: General informational messages (query pagination, operation status)
- **WARNING**: Warning messages (pagination issues, non-critical errors)
- **ERROR**: Error messages (failed API calls, authentication errors)

## Configuration Examples

### Basic Console Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### File Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='vault_api.log',
    filemode='a'
)
```

### Advanced Configuration with Handlers

```python
import logging

# Create logger
logger = logging.getLogger('veevavault')
logger.setLevel(logging.DEBUG)

# Create console handler with INFO level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create file handler with DEBUG level
fh = logging.FileHandler('vault_api_debug.log')
fh.setLevel(logging.DEBUG)

# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)
```

### Disable Logging

If you want to disable all logging from VeevaVaultMCP:

```python
import logging

logging.getLogger('veevavault').setLevel(logging.CRITICAL + 1)
```

### Filter Specific Modules

You can control logging for specific modules:

```python
import logging

# Enable DEBUG for query service only
logging.getLogger('veevavault.services.queries').setLevel(logging.DEBUG)

# Set INFO for all other modules
logging.getLogger('veevavault').setLevel(logging.INFO)
```

## Logged Information

### VaultClient
- **DEBUG**: Request method and URL for each API call
- **DEBUG**: Response status code for successful calls
- **ERROR**: Detailed error messages with response content

### QueryService
- **DEBUG**: Number of records returned from successful queries
- **INFO**: Pagination information (PAGESIZE detection)
- **WARNING**: Incomplete pagination warnings
- **ERROR**: Query failures with error details

### All Services
- **ERROR**: Any exceptions raised during API calls

## Exception Handling

VeevaVaultMCP provides custom exceptions that include detailed error information:

```python
from veevavault import VaultClient, DocumentService
from veevavault.exceptions import (
    VaultAPIError,
    VaultAuthenticationError,
    VaultPermissionError,
    VaultNotFoundError,
    VaultValidationError,
    VaultRateLimitError,
    VaultServerError,
    VaultQueryError,
    VaultSessionError,
)

try:
    client = VaultClient()
    # ... your code ...
except VaultAuthenticationError as e:
    print(f"Authentication failed: {e}")
    print(f"Status code: {e.status_code}")
    print(f"Vault errors: {e.vault_errors}")
except VaultPermissionError as e:
    print(f"Permission denied: {e}")
except VaultNotFoundError as e:
    print(f"Resource not found: {e}")
except VaultAPIError as e:
    print(f"API error: {e}")
```

## Best Practices

1. **Development**: Use `DEBUG` level to see all API calls and responses
2. **Production**: Use `INFO` or `WARNING` level to reduce log volume
3. **Debugging**: Enable `DEBUG` for specific modules you're troubleshooting
4. **Security**: Avoid logging sensitive information (passwords, session IDs) by using INFO level or higher
5. **Performance**: Use file handlers instead of console handlers in production
6. **Rotation**: Use `RotatingFileHandler` or `TimedRotatingFileHandler` for log rotation

## Example: Production Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

# Create rotating file handler
handler = RotatingFileHandler(
    'vault_api.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)

# Set format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

# Configure logger
logger = logging.getLogger('veevavault')
logger.setLevel(logging.INFO)
logger.addHandler(handler)
```

## Troubleshooting

### No logs appearing

If you're not seeing any logs, ensure you've configured the logging module:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Too many logs

Reduce the log level to WARNING or ERROR:

```python
import logging
logging.getLogger('veevavault').setLevel(logging.WARNING)
```

### Logs from other libraries

To see only VeevaVaultMCP logs:

```python
import logging

# Disable all other loggers
logging.basicConfig(level=logging.CRITICAL)

# Enable VeevaVaultMCP logger
logging.getLogger('veevavault').setLevel(logging.INFO)
```
