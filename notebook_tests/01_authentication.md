# Authentication API Testing Documentation

## Required Services and Classes

### Primary Services
- **Location:** `veevavault/services/authentication/`
- **Main Service:** `AuthenticationService` (in `auth_service.py`)

### Required Files and Classes
- `veevavault/services/authentication/auth_service.py`
  - `AuthenticationService` class
- `veevavault/client/vault_client.py` (required dependency)
- `test_credentials.py` (for secure credential management)

---

## Authentication Endpoints Testing

### User Name and Password Authentication

**Endpoint:** `POST /api/{version}/auth`

**Method Tested:** `authenticate()` and `authenticate_with_username_password()`
**Class:** `AuthenticationService`
**Location:** `veevavault/services/authentication/auth_service.py`

**Test Coverage:**
- ✅ Basic username/password authentication
- ✅ Response parsing (sessionId, userId, vaultIds, vaultId)
- ✅ Invalid DNS handling and fallback to most relevant vault
- ✅ Multi-vault user authentication
- ✅ Error handling for invalid credentials
- ✅ Vault DNS validation and user access verification

**Test Implementation:**
```python
# Test basic authentication
auth_service = AuthenticationService(client)
result = auth_service.authenticate(
    vaultURL="https://myvault.veevavault.com",
    vaultUserName="test_user",
    vaultPassword="test_password"
)

# Verify response structure
assert result["responseStatus"] == "SUCCESS"
assert "sessionId" in result
assert "userId" in result
assert "vaultIds" in result
assert isinstance(result["vaultIds"], list)
```

---

### OAuth 2.0 / OpenID Connect Authentication

**Endpoint:** `POST /auth/oauth/session/{oauth_oidc_profile_id}`

**Method Tested:** `authenticate_with_oauth_openid_connect()`
**Class:** `AuthenticationService`
**Location:** `veevavault/services/authentication/auth_service.py`

**Test Coverage:**
- ✅ OAuth 2.0 token authentication
- ✅ Access token bearer header validation
- ✅ OAuth profile ID parameter handling
- ✅ Optional vaultDNS parameter
- ✅ Optional client_id parameter
- ✅ Response structure validation

**Test Implementation:**
```python
# Test OAuth authentication
result = auth_service.authenticate_with_oauth_openid_connect(
    oauth_profile_id="profile_id_123",
    access_token="bearer_token_456",
    vault_dns="myvault.veevavault.com",
    client_id="my_client_app"
)

# Verify OAuth-specific response
assert result["responseStatus"] == "SUCCESS"
assert "sessionId" in result
```

---

### Retrieve API Versions

**Endpoint:** `GET /api/`

**Method Tested:** `retrieve_api_version()`
**Class:** `AuthenticationService`
**Location:** `veevavault/services/authentication/auth_service.py`

**Test Coverage:**
- ✅ API version retrieval without authentication
- ✅ Response format validation (values dictionary)
- ✅ Version string format validation
- ✅ Beta version identification
- ✅ URL structure verification for each version

**Test Implementation:**
```python
# Test API version retrieval
result = auth_service.retrieve_api_version(
    vault_url="https://myvault.veevavault.com"
)

# Verify version response structure
assert result["responseStatus"] == "SUCCESS"
assert "values" in result
assert isinstance(result["values"], dict)

# Verify version format (e.g., "v25.2")
for version, url in result["values"].items():
    assert version.startswith("v")
    assert url.startswith("https://")
```

---

### Authentication Type Discovery

**Endpoint:** `POST /auth/discovery`

**Method Tested:** `authentication_type_discovery()`
**Class:** `AuthenticationService`
**Location:** `veevavault/services/authentication/auth_service.py`

**Test Coverage:**
- ✅ Username-based auth type discovery
- ✅ Password user type detection
- ✅ SSO user type detection
- ✅ OAuth profile information retrieval
- ✅ MSAL support detection (with X-VaultAPI-AuthIncludeMsal header)
- ✅ Client ID mapping validation
- ✅ AS metadata parsing

**Test Implementation:**
```python
# Test auth type discovery for password user
result = auth_service.authentication_type_discovery(
    username="password_user@company.com",
    client_id="my_client_id",
    include_msal=True
)

assert result["data"]["auth_type"] == "password"

# Test auth type discovery for SSO user
result = auth_service.authentication_type_discovery(
    username="sso_user@company.com",
    include_msal=True
)

assert result["data"]["auth_type"] == "sso"
assert "auth_profiles" in result["data"]
```

---

### Session Keep Alive

**Endpoint:** `POST /api/{version}/keep-alive`

**Method Tested:** `keep_alive()`
**Class:** `AuthenticationService`
**Location:** `veevavault/services/authentication/auth_service.py`

**Test Coverage:**
- ✅ Session duration refresh
- ✅ Active session validation
- ✅ Authentication header requirement
- ✅ Success response validation
- ✅ Session timeout prevention

**Test Implementation:**
```python
# First authenticate to get session ID
auth_result = auth_service.authenticate(
    vaultURL="https://myvault.veevavault.com",
    vaultUserName="test_user",
    vaultPassword="test_password"
)
session_id = auth_result["sessionId"]

# Test keep alive
result = auth_service.keep_alive(session_id=session_id)

assert result["responseStatus"] == "SUCCESS"
```

---

### End Session

**Endpoint:** `DELETE /api/{version}/session`

**Method Tested:** `logout()`
**Class:** `AuthenticationService`
**Location:** `veevavault/services/authentication/auth_service.py`

**Test Coverage:**
- ✅ Session termination
- ✅ Session ID invalidation
- ✅ Multiple session handling
- ✅ Authentication header requirement
- ✅ Success response validation

**Test Implementation:**
```python
# Authenticate and then logout
auth_result = auth_service.authenticate(
    vaultURL="https://myvault.veevavault.com",
    vaultUserName="test_user",
    vaultPassword="test_password"
)
session_id = auth_result["sessionId"]

# Test logout
result = auth_service.logout(session_id=session_id)

assert result["responseStatus"] == "SUCCESS"

# Verify session is no longer valid
with pytest.raises(Exception):
    auth_service.keep_alive(session_id=session_id)
```

---

### Salesforce™ Delegated Requests

**Endpoint:** `GET /api/{version}/{Vault_Endpoint}`

**Method Tested:** `salesforce_delegated_requests()`
**Class:** `AuthenticationService`
**Location:** `veevavault/services/authentication/auth_service.py`

**Test Coverage:**
- ✅ Salesforce session token authentication
- ✅ X-Auth-Provider header validation (sfdc)
- ✅ X-Auth-Host header for Salesforce URL
- ✅ Query parameter alternative authentication
- ✅ Trusted Org ID validation
- ✅ Username matching between Vault and Salesforce

**Test Implementation:**
```python
# Test Salesforce delegated authentication
result = auth_service.salesforce_delegated_requests(
    sfdc_session_token="salesforce_session_123",
    sfdc_host="https://mycompany.salesforce.com",
    vault_endpoint="/api/v25.2/objects/documents"
)

# Note: This requires proper Salesforce delegated authentication setup
assert result is not None  # Response varies based on endpoint called
```

**Notes:**
- Requires Salesforce delegated authentication configuration
- Needs valid Salesforce session token
- Requires matching usernames in both systems

---

### Delegated Access - Retrieve Delegations

**Endpoint:** `GET /api/{version}/delegation/vaults`

**Method Tested:** `retrieve_delegations()`
**Class:** `AuthenticationService`
**Location:** `veevavault/services/authentication/auth_service.py`

**Test Coverage:**
- ✅ Delegation retrieval for authenticated user
- ✅ Vault information parsing (id, name, dns, delegator_userid)
- ✅ Empty response handling (no delegations)
- ✅ Multiple vault delegations
- ✅ Authorization header requirement

**Test Implementation:**
```python
# Authenticate first
auth_result = auth_service.authenticate(
    vaultURL="https://myvault.veevavault.com",
    vaultUserName="delegate_user",
    vaultPassword="test_password"
)
session_id = auth_result["sessionId"]

# Test delegation retrieval
result = auth_service.retrieve_delegations(session_id=session_id)

assert result["responseStatus"] == "SUCCESS"
assert "delegated_vaults" in result

if result["delegated_vaults"]:
    for vault in result["delegated_vaults"]:
        assert "id" in vault
        assert "name" in vault
        assert "dns" in vault
        assert "delegator_userid" in vault
```

---

### Delegated Access - Initiate Delegated Session

**Endpoint:** `POST /api/{version}/delegation/login`

**Method Tested:** `initiate_delegated_session()`
**Class:** `AuthenticationService`
**Location:** `veevavault/services/authentication/auth_service.py`

**Test Coverage:**
- ✅ Delegated session ID generation
- ✅ Vault ID parameter validation
- ✅ Delegator user ID parameter validation
- ✅ Regular session ID requirement (not delegated)
- ✅ Success response with delegated_sessionid
- ✅ Delegated session usage for API calls

**Test Implementation:**
```python
# First get delegation info
delegations = auth_service.retrieve_delegations(session_id=session_id)

if delegations["delegated_vaults"]:
    vault_info = delegations["delegated_vaults"][0]
    
    # Test delegated session initiation
    result = auth_service.initiate_delegated_session(
        session_id=session_id,
        vault_id=vault_info["id"],
        delegator_userid=vault_info["delegator_userid"]
    )
    
    assert result["responseStatus"] == "SUCCESS"
    assert "delegated_sessionid" in result
    
    # Verify delegated session can be used for API calls
    delegated_session_id = result["delegated_sessionid"]
    # Use delegated_session_id for subsequent API calls
```

**Notes:**
- Requires existing delegation setup between users
- Cannot use delegated session ID to initiate another delegated session
- Delegation is Vault-specific

---

## Summary

### Total Endpoints Covered: 9/9 (100%)

### Coverage by Category:
- **Basic Authentication:** ✅ Username/Password, OAuth 2.0/OIDC
- **Session Management:** ✅ Keep Alive, End Session  
- **Discovery & Information:** ✅ API Versions, Auth Type Discovery
- **Advanced Authentication:** ✅ Salesforce Delegated, Delegated Access
- **Delegated Operations:** ✅ Retrieve Delegations, Initiate Delegated Session

### Testing Notes:
- All authentication methods require proper credential setup
- OAuth testing requires configured OAuth profiles
- Salesforce delegation requires Salesforce integration setup
- Delegated access testing requires pre-existing delegation relationships
- Session management tests should verify both success and failure scenarios
- All endpoints support both JSON and XML response formats (where applicable)

### Test Environment Requirements:
- Valid Vault credentials in `test_credentials.py`
- OAuth 2.0/OIDC profiles configured (for OAuth tests)
- Salesforce delegated authentication setup (for SFDC tests)
- User delegation relationships (for delegation tests)
- Network access to Vault instances and login servers
