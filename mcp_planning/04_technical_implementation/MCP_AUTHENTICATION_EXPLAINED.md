# MCP Authentication: Real-World Scenarios & Architecture

**Document Version:** 1.0
**Date:** 2025-11-06
**Purpose:** Explain how authentication works in MCP servers with practical examples

---

## Table of Contents

1. [MCP Authentication Overview](#mcp-authentication-overview)
2. [Real-World Scenario 1: Single User Claude Desktop](#scenario-1-single-user-claude-desktop)
3. [Real-World Scenario 2: Multi-User Enterprise Deployment](#scenario-2-multi-user-enterprise-deployment)
4. [Real-World Scenario 3: LLM-as-Service Integration](#scenario-3-llm-as-service-integration)
5. [Real-World Scenario 4: Shared Team Server](#scenario-4-shared-team-server)
6. [Authentication Flow Diagrams](#authentication-flow-diagrams)
7. [Security Considerations](#security-considerations)
8. [Implementation Patterns](#implementation-patterns)

---

## MCP Authentication Overview

### **Two Layers of Authentication**

When building an MCP server for Veeva Vault, you're dealing with **two separate authentication concerns**:

1. **MCP Protocol Authentication** (Optional)
   - Between **Host** (Claude Desktop, IDE, etc.) and **MCP Server**
   - Ensures only authorized clients can connect to your MCP server
   - New in MCP 2025 spec: OAuth2 with RFC 8707 Resource Indicators

2. **Vault API Authentication** (Required)
   - Between **MCP Server** and **Veeva Vault**
   - Your MCP server needs credentials to call Vault APIs
   - This is what we're primarily concerned with

### **Key Question: Whose credentials does the MCP server use?**

This is where it gets interesting, and the answer depends on your deployment model.

---

## Scenario 1: Single User Claude Desktop

### **Setup:**
- Individual user running Claude Desktop on their laptop
- MCP server running locally (Docker container on localhost)
- User wants to interact with Vault through Claude

### **Authentication Flow:**

```
User's Laptop
│
├── Claude Desktop (Host)
│   └── Connects to → MCP Server (localhost:3000)
│
└── MCP Server (Docker)
    ├── Configured with user's Vault credentials
    └── Connects to → Veeva Vault
```

### **How It Works:**

**Step 1: User Configuration**
User creates a config file for Claude Desktop:
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "veevavault": {
      "command": "docker",
      "args": ["run", "-i", "--rm",
               "-e", "VAULT_URL=https://company.veevavault.com",
               "-e", "VAULT_USERNAME=john.smith@company.com",
               "-e", "VAULT_PASSWORD=JohnsPassword123",
               "veevavault-mcp:latest"]
    }
  }
}
```

**Step 2: MCP Server Starts**
- Claude Desktop launches the Docker container when first needed
- MCP server reads `VAULT_USERNAME` and `VAULT_PASSWORD` from environment
- Authenticates with Vault using **John's credentials**
- Keeps session alive

**Step 3: User Interaction**
```
User: "Show me all documents I created this week"

Claude Desktop:
  → Calls MCP tool: documents_query(created_by="john.smith@company.com", created_after="2025-11-01")

MCP Server:
  → Uses John's authenticated session
  → Calls Vault API: GET /api/v25.2/query?q=SELECT...
  → Returns John's documents (respects Vault permissions)

Claude Desktop:
  → Shows results to user
```

### **Key Points:**

✅ **Personal credentials** - Each user uses their own Vault login
✅ **Vault security respected** - User only sees what they have permission to see
✅ **Audit trail** - Vault logs show "john.smith@company.com" performed actions
✅ **Simple setup** - User controls their own credentials
✅ **No MCP auth needed** - Server only accessible on localhost

### **Real-World Example:**

**Sarah (Regulatory Affairs Specialist)** wants to use Claude to help compile her NDA submission:

```
Sarah: "Find all approved Module 2.5 documents for Product X"

Claude (via MCP):
  - Authenticates as sarah.jones@pharma.com
  - Queries Vault with Sarah's permissions
  - Returns only documents Sarah can access
  - Sarah's manager can't see her Vault activity (privacy)
```

---

## Scenario 2: Multi-User Enterprise Deployment

### **Setup:**
- Company deploys MCP server centrally (Kubernetes cluster)
- Multiple users across the organization
- Each user should interact with Vault using **their own identity**

### **Authentication Flow:**

```
User Laptops
│
├── Sarah's Claude Desktop → MCP Server (https://mcp.company.com)
├── John's Claude Desktop → MCP Server (https://mcp.company.com)
└── Mary's Claude Desktop → MCP Server (https://mcp.company.com)
                               │
                               ├── Authenticates Sarah as sarah.jones@pharma.com
                               ├── Authenticates John as john.smith@pharma.com
                               └── Authenticates Mary as mary.wilson@pharma.com
                                    │
                                    └── All connect to → Veeva Vault
```

### **How It Works:**

**Architecture Pattern: OAuth2 Token Exchange**

**Step 1: User Authentication with MCP Server**
```json
// Sarah's claude_desktop_config.json
{
  "mcpServers": {
    "veevavault": {
      "url": "https://mcp.company.com",
      "auth": {
        "type": "oauth2",
        "tokenUrl": "https://auth.company.com/token",
        "clientId": "claude-desktop-sarah",
        "scopes": ["vault:read", "vault:write"]
      }
    }
  }
}
```

**Step 2: Token Exchange Flow**
1. Claude Desktop gets OAuth token for Sarah
2. Sends token to MCP server with tool call
3. MCP server validates token (verifies it's really Sarah)
4. MCP server exchanges Sarah's token for Vault credentials
5. MCP server calls Vault API as Sarah

**Step 3: Session Management**
```python
# In MCP Server

class MultiUserAuthenticationManager:
    def __init__(self):
        # Map: user_id -> VaultClient session
        self._sessions = {}

    async def get_client_for_user(self, user_token: str) -> VaultClient:
        """Get Vault client for specific user."""

        # Validate OAuth token
        user_info = await validate_token(user_token)
        user_id = user_info["user_id"]  # e.g., "sarah.jones@pharma.com"

        # Check if we have cached session
        if user_id in self._sessions:
            session = self._sessions[user_id]
            if not session.is_expired():
                return session.client

        # Create new Vault session for this user
        vault_client = VaultClient()

        # Option A: Use service account with impersonation
        await vault_client.authenticate_as_service()
        await vault_client.impersonate(user_id)

        # Option B: Exchange OAuth token for Vault session
        vault_session = await exchange_token_for_vault_session(user_token)
        vault_client.set_session(vault_session)

        # Cache session
        self._sessions[user_id] = Session(vault_client, expires_in=3600)

        return vault_client
```

**Step 4: Tool Execution with User Context**
```python
@server.tool(name="documents_query")
async def documents_query(user_token: str, **params):
    """
    Query documents.

    user_token: Passed automatically by MCP protocol (from Claude Desktop)
    """

    # Get Vault client for this specific user
    client = await auth_manager.get_client_for_user(user_token)

    # Execute query as that user
    results = await query_documents(client, **params)

    return results
```

### **Real-World Example:**

**Scenario: QA Team Collaboration**

Sarah (QA Manager) and John (QA Specialist) both use Claude:

```
Sarah: "Show me all open deviations assigned to my team"
Claude:
  - Authenticates as Sarah
  - Vault returns ALL deviations (Sarah is manager, has broad access)
  - Shows 50 deviations

John: "Show me all open deviations assigned to my team"
Claude:
  - Authenticates as John
  - Vault returns only John's assigned deviations (John is specialist, limited access)
  - Shows 5 deviations

KEY: Same MCP server, same tool, different results based on user identity!
```

### **Key Points:**

✅ **User identity preserved** - Each user's Vault actions logged under their account
✅ **Vault permissions respected** - Users see only what they're authorized to see
✅ **Centralized server** - Company maintains one MCP server for all users
✅ **Audit compliance** - Clear trail of who did what
✅ **Requires MCP auth** - OAuth2 to identify users connecting to MCP server

---

## Scenario 3: LLM-as-Service Integration

### **Setup:**
- Company builds internal "Ask Vault" chatbot
- Web application where users log in
- Backend LLM service uses MCP to query Vault
- Need to maintain user identity through the chain

### **Authentication Flow:**

```
User Browser
│
└── Web App (https://askvault.company.com)
    │ User logs in with SSO
    │
    └── Backend Service
        │
        └── LLM API (Claude API)
            │
            └── MCP Server (internal)
                │
                └── Veeva Vault
```

### **How It Works:**

**Step 1: User Logs Into Web App**
```javascript
// User logs in via Okta/Azure AD
const userSession = await oktaAuth.login(username, password);
const userToken = userSession.accessToken;  // JWT token
```

**Step 2: Web App Calls Backend**
```javascript
// Frontend sends user token with request
fetch('/api/ask', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${userToken}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    question: "Show me my pending review tasks"
  })
})
```

**Step 3: Backend Calls Claude API with User Context**
```python
# Backend service

async def handle_question(question: str, user_token: str):
    """Handle user question via Claude."""

    # Validate user
    user_info = await validate_jwt(user_token)
    user_email = user_info["email"]

    # Call Claude API with MCP
    response = await anthropic.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{
            "role": "user",
            "content": question
        }],
        tools=mcp_tools,  # MCP tools exposed to Claude
        metadata={
            "user_id": user_email  # Pass user context
        }
    )

    return response
```

**Step 4: MCP Server Receives Call with User Context**
```python
# MCP Server

@server.tool(name="workflows_get_tasks")
async def get_my_tasks(user_id: str):  # user_id from metadata
    """Get tasks for the authenticated user."""

    # Get Vault client for this user
    vault_client = await auth_manager.get_client_for_user(user_id)

    # Query workflows as that user
    from veevavault.services.workflows import WorkflowService
    workflow_service = WorkflowService(vault_client)

    tasks = workflow_service.get_tasks_assigned_to(user_id)

    return tasks
```

### **Real-World Example:**

**Scenario: Mobile App for Field Users**

Pharma sales reps using mobile app to access medical information:

```
Sales Rep on iPad:
  "What's the approved dosing for Product X in pediatric patients?"

Mobile App:
  → User authenticated via corporate SSO
  → Sends question to backend with user token

Backend:
  → Calls Claude API via MCP
  → Passes "sales_rep_jane@pharma.com" as user context

MCP Server:
  → Authenticates with Vault as Jane
  → Queries medical information documents
  → Returns only approved, sales-appropriate content
  → (Jane can't see unpublished clinical data - permissions enforced!)

Mobile App:
  → Displays approved dosing information
```

### **Key Points:**

✅ **Chain of trust** - User identity passed through web app → backend → LLM → MCP → Vault
✅ **Token exchange** - Each layer validates and transforms tokens
✅ **Stateless** - No session storage needed (JWT tokens contain identity)
✅ **Scalable** - Can handle thousands of concurrent users

---

## Scenario 4: Shared Team Server

### **Setup:**
- Small team shares a single "team bot" account
- MCP server uses **service account** credentials
- All actions logged as service account (not individual users)
- Simpler but less secure

### **Authentication Flow:**

```
Team Members
│
├── Sarah's Claude Desktop → MCP Server (team-bot@company.com credentials)
├── John's Claude Desktop → MCP Server (team-bot@company.com credentials)
└── Mary's Claude Desktop → MCP Server (team-bot@company.com credentials)
                              │
                              └── All calls to Vault appear as "team-bot@company.com"
```

### **How It Works:**

**Configuration:**
```bash
# Shared credentials for team
VAULT_USERNAME=team-bot@company.com
VAULT_PASSWORD=SharedTeamPassword123

# Everyone uses same config
```

**Tool Execution:**
```python
# MCP Server - single shared session

class SharedAuthenticationManager:
    def __init__(self):
        # One client for everyone
        self._client = None

    async def authenticate(self):
        """Authenticate as shared service account."""
        self._client = VaultClient(
            vault_username="team-bot@company.com",
            vault_password="SharedTeamPassword123"
        )
        await self._client.authenticate()

    def get_client(self) -> VaultClient:
        """Everyone gets same client."""
        return self._client
```

### **Real-World Example:**

**Scenario: QA Team Shared Bot**

Small QA team (5 people) sharing a bot for quick queries:

```
Anyone on team:
  "Show me all open CAPAs for Building 3"

Claude:
  → Uses team-bot@company.com credentials
  → Queries Vault
  → Returns ALL CAPAs (service account has broad access)
  → Vault audit log shows: "team-bot@company.com queried CAPAs"

Problem: Can't tell if it was Sarah, John, or Mary who actually asked!
```

### **Key Points:**

⚠️ **Shared credentials** - Everyone uses same Vault account
⚠️ **No individual accountability** - Can't tell who performed actions
⚠️ **Broader permissions** - Service account typically has elevated access
✅ **Simple setup** - No complex token exchange needed
✅ **Good for small teams** - Works for trusted 3-5 person teams
❌ **Not audit-compliant** - FDA inspectors want individual accountability

---

## Authentication Flow Diagrams

### **Flow 1: Personal Desktop (Scenario 1)**

```
┌─────────────────┐
│  User's Laptop  │
│                 │
│  ┌───────────┐  │
│  │  Claude   │  │
│  │  Desktop  │  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │    MCP    │  │ ← Uses john.smith credentials
│  │   Server  │  │
│  └─────┬─────┘  │
└────────┼────────┘
         │
         │ Vault API call
         │ (as john.smith)
         ▼
┌─────────────────┐
│  Veeva Vault    │
│                 │
│  Audit Log:     │
│  john.smith     │
│  queried docs   │
└─────────────────┘
```

### **Flow 2: Enterprise Multi-User (Scenario 2)**

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Sarah's  │  │  John's  │  │  Mary's  │
│  Claude  │  │  Claude  │  │  Claude  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
     │ OAuth       │ OAuth       │ OAuth
     │ Token       │ Token       │ Token
     │ (Sarah)     │ (John)      │ (Mary)
     │             │             │
     └─────────────┼─────────────┘
                   │
                   ▼
            ┌─────────────┐
            │  MCP Server │
            │  (Central)  │
            └──────┬──────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
    VaultClient VaultClient VaultClient
    (as Sarah) (as John)   (as Mary)
        │          │          │
        └──────────┼──────────┘
                   │
                   ▼
            ┌─────────────┐
            │Veeva Vault  │
            │             │
            │ Audit Log:  │
            │ sarah.jones │
            │ john.smith  │
            │ mary.wilson │
            └─────────────┘
```

### **Flow 3: Web App Integration (Scenario 3)**

```
┌──────────────────────────────────────────────────┐
│                  User Browser                     │
│                                                   │
│  User logs in → Gets JWT token                   │
└─────────────────────┬────────────────────────────┘
                      │
                      │ HTTPS request
                      │ Authorization: Bearer <JWT>
                      ▼
┌──────────────────────────────────────────────────┐
│              Web App Backend                      │
│                                                   │
│  1. Validate JWT                                 │
│  2. Extract user_email from JWT                  │
│  3. Call Claude API with user context            │
└─────────────────────┬────────────────────────────┘
                      │
                      │ Claude API call
                      │ + MCP tools
                      │ + metadata: {user_email}
                      ▼
┌──────────────────────────────────────────────────┐
│              Claude API (Anthropic)               │
│                                                   │
│  Invokes MCP tools with user_email              │
└─────────────────────┬────────────────────────────┘
                      │
                      │ MCP tool call
                      │ + user_email parameter
                      ▼
┌──────────────────────────────────────────────────┐
│                 MCP Server                        │
│                                                   │
│  1. Get Vault credentials for user_email         │
│  2. Create/reuse Vault session for that user     │
│  3. Execute Vault API call                       │
└─────────────────────┬────────────────────────────┘
                      │
                      │ Vault API
                      │ (as user_email)
                      ▼
┌──────────────────────────────────────────────────┐
│                Veeva Vault                        │
│                                                   │
│  Audit Log: user_email@company.com               │
└──────────────────────────────────────────────────┘
```

---

## Security Considerations

### **1. Credential Storage**

**❌ NEVER do this:**
```python
# Hardcoded credentials in code
VAULT_USERNAME = "admin@company.com"
VAULT_PASSWORD = "MyPassword123"
```

**✅ DO this:**
```python
# Environment variables
VAULT_USERNAME = os.getenv("VAULT_USERNAME")
VAULT_PASSWORD = os.getenv("VAULT_PASSWORD")

# Or secrets manager
secrets = await get_secrets_from_vault("/vault/veeva-credentials")
VAULT_USERNAME = secrets["username"]
```

### **2. Session Management**

**Best Practices:**
- ✅ Refresh sessions before expiry (don't let them expire during operations)
- ✅ Invalidate sessions on user logout
- ✅ Use separate sessions per user (multi-user scenarios)
- ✅ Log all authentication events

### **3. Token Security**

**For OAuth2 tokens:**
- ✅ Validate tokens on every request
- ✅ Check token expiration
- ✅ Verify token signature (JWT)
- ✅ Use short-lived tokens (15-60 minutes)
- ✅ Implement token refresh flow

### **4. Audit Trail**

**Always log:**
- Who authenticated (user identity)
- When they authenticated
- What actions they performed
- Any authentication failures

```python
logger.info(
    "User authenticated",
    user_id="sarah.jones@pharma.com",
    session_id="abc123...",
    timestamp="2025-11-06T10:30:00Z",
    ip_address="10.0.1.45"
)
```

---

## Implementation Patterns

### **Pattern 1: Single User (Personal Desktop)**

**Best for:**
- Individual users
- Local development
- Simple use cases

**Implementation:**
```python
class PersonalAuthManager:
    async def authenticate(self):
        """Authenticate as configured user."""
        self.client = VaultClient(
            vault_url=config.vault_url,
            vault_username=config.vault_username,
            vault_password=config.vault_password
        )
        await self.client.authenticate()

    def get_client(self) -> VaultClient:
        return self.client  # Everyone gets same client
```

### **Pattern 2: Multi-User with User Context**

**Best for:**
- Enterprise deployments
- Compliance requirements
- Audit trail needed

**Implementation:**
```python
class MultiUserAuthManager:
    def __init__(self):
        self.sessions = {}  # user_id -> VaultSession

    async def get_client_for_user(self, user_id: str) -> VaultClient:
        """Get Vault client for specific user."""

        if user_id not in self.sessions:
            # Create new session for this user
            client = VaultClient()

            # Option A: Service account with impersonation
            await client.authenticate_as_service(
                service_account="mcp-service@company.com"
            )
            await client.impersonate_user(user_id)

            # Option B: User-specific credentials (from secrets manager)
            user_creds = await get_user_credentials(user_id)
            await client.authenticate(
                username=user_creds["username"],
                password=user_creds["password"]
            )

            self.sessions[user_id] = Session(client)

        return self.sessions[user_id].client
```

### **Pattern 3: Service Account (Shared)**

**Best for:**
- Small teams
- Internal automation
- Non-compliance-critical workflows

**Implementation:**
```python
class ServiceAccountAuthManager:
    async def authenticate(self):
        """Authenticate as service account."""
        self.client = VaultClient(
            vault_url=config.vault_url,
            vault_username="service-bot@company.com",
            vault_password=config.service_password
        )
        await self.client.authenticate()

        logger.warning(
            "Using shared service account",
            note="Individual user actions won't be traceable"
        )

    def get_client(self) -> VaultClient:
        return self.client
```

---

## Summary: Which Authentication Pattern to Use?

### **Decision Matrix:**

| Use Case | Pattern | Pros | Cons |
|----------|---------|------|------|
| **Personal use (Claude Desktop)** | Single User | Simple, fast setup | No sharing |
| **Small team (3-5 people)** | Service Account | Easy management | No individual audit trail |
| **Enterprise (10+ users)** | Multi-User OAuth | Full accountability | Complex setup |
| **Web app integration** | Multi-User with JWT | Scalable, secure | Requires token exchange |
| **Automation/CI-CD** | Service Account | No user interaction | Elevated permissions needed |

### **Your VeevaVault MCP Server:**

Based on your requirements (Docker now, Kubernetes later), I recommend implementing:

1. **Phase 1 (MVP):** Pattern 1 or 3 (Personal or Service Account)
   - Quick to implement
   - Good for initial testing and small teams

2. **Phase 2 (Enterprise):** Pattern 2 (Multi-User OAuth)
   - Add when deploying to Kubernetes
   - Full user accountability
   - Compliance-ready

We'll build the architecture to support both from the start, so you can switch patterns without rewriting code!

---

**Ready to implement?** Let me know if you want me to update the technical plan with these authentication patterns!
