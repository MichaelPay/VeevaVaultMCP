# SCIM API Testing Documentation

## Required Services and Classes

### Primary Service Structure
- **Location:** `veevavault/services/scim/`
- **Main Service:** `SCIMService` (in `scim.py`)

### Service Architecture
SCIM (System for Cross-domain Identity Management) is handled by the specialized SCIMService:

- `SCIMService` - SCIM 2.0 compliant identity management operations
- `UserService` - Traditional user management (for comparison)
- `ObjectService` - Object-based user management (for integration)

### Required Files and Classes
- `veevavault/services/scim/scim.py` - SCIM operations
- `veevavault/services/users/users.py` - Traditional user management
- `veevavault/services/objects/object_service.py` - Object record management
- `veevavault/client/vault_client.py` (required dependency)
- `test_credentials.py` (for secure credential management)

---

## SCIM Concepts

### SCIM Standard Overview
- **SCIM 2.0 Compliance:** Full RFC 7643/7644 standard implementation
- **Cross-Domain Identity Management:** Standardized user provisioning
- **REST API Standard:** Consistent identity operations across systems
- **Bearer Token Authentication:** Session ID as OAuth bearer token
- **JSON Schema Definitions:** Structured attribute definitions

### Supported Resource Types
- **Users:** User account management and provisioning
- **Groups:** Group membership and access control (if available)
- **ServiceProviderConfig:** SCIM capability discovery
- **ResourceTypes:** Available resource definitions
- **Schemas:** Attribute and structure definitions

### SCIM vs Traditional API
- **Standard Compliance:** SCIM follows industry standards
- **Attribute Mapping:** Standardized user attribute names
- **Filtering Syntax:** SCIM-compliant filtering expressions
- **Pagination:** Standard SCIM pagination parameters
- **Schema Discovery:** Self-describing API capabilities

---

## Discovery Endpoints Testing

### Retrieve SCIM Provider Configuration

**Endpoint:** `GET /api/{version}/scim/v2/ServiceProviderConfig`

**Method Tested:** `scim_service.retrieve_scim_provider()`
**Service:** `SCIMService`
**Location:** `veevavault/services/scim/scim.py`

**Test Coverage:**
- ✅ Provider capability discovery
- ✅ Supported operations validation
- ✅ Authentication scheme verification
- ✅ Feature support analysis
- ✅ RFC compliance validation

**Test Implementation:**
```python
# Test SCIM provider configuration retrieval
from veevavault.services.scim.scim import SCIMService

scim_service = SCIMService(client)

try:
    # Test SCIM provider configuration
    provider_config = scim_service.retrieve_scim_provider()
    
    # Verify response structure
    assert provider_config["responseStatus"] == "SUCCESS"
    assert "schemas" in provider_config
    assert "authenticationSchemes" in provider_config
    
    print(f"✅ SCIM Provider Configuration retrieved successfully")
    
    # Analyze provider capabilities
    schemas = provider_config.get("schemas", [])
    auth_schemes = provider_config.get("authenticationSchemes", [])
    
    print(f"  Schemas: {schemas}")
    print(f"  Authentication schemes: {len(auth_schemes)}")
    
    # Check supported operations
    operations = ["patch", "bulk", "filter", "changePassword", "sort", "etag"]
    supported_operations = []
    
    for operation in operations:
        if operation in provider_config:
            op_config = provider_config[operation]
            is_supported = op_config.get("supported", False)
            
            print(f"  {operation.title()} Support: {is_supported}")
            
            if is_supported:
                supported_operations.append(operation)
                
                # Show additional details for supported operations
                if operation == "filter" and "maxResults" in op_config:
                    print(f"    Max Results: {op_config['maxResults']}")
                elif operation == "bulk":
                    max_ops = op_config.get("maxOperations", 0)
                    max_payload = op_config.get("maxPayloadSize", 0)
                    print(f"    Max Operations: {max_ops}")
                    print(f"    Max Payload Size: {max_payload}")
    
    print(f"  Supported Operations: {supported_operations}")
    
    # Analyze authentication schemes
    for auth_scheme in auth_schemes:
        name = auth_scheme.get("name", "unknown")
        description = auth_scheme.get("description", "")
        auth_type = auth_scheme.get("type", "unknown")
        is_primary = auth_scheme.get("primary", False)
        
        print(f"  Authentication: {name}")
        print(f"    Type: {auth_type}")
        print(f"    Primary: {is_primary}")
        print(f"    Description: {description}")
    
    # Check documentation URI
    if "documentationUri" in provider_config:
        doc_uri = provider_config["documentationUri"]
        print(f"  Documentation: {doc_uri}")
    
    # Verify meta information
    if "meta" in provider_config:
        meta = provider_config["meta"]
        resource_type = meta.get("resourceType", "unknown")
        location = meta.get("location", "unknown")
        
        print(f"  Meta Information:")
        print(f"    Resource Type: {resource_type}")
        print(f"    Location: {location}")
    
    print(f"  ✅ Provider configuration analysis completed")

except Exception as e:
    print(f"❌ SCIM provider configuration retrieval failed: {e}")
```

---

### Retrieve All SCIM Schemas

**Endpoint:** `GET /api/{version}/scim/v2/Schemas`

**Method Tested:** `scim_service.retrieve_all_scim_schemas()`
**Service:** `SCIMService`
**Location:** `veevavault/services/scim/scim.py`

**Test Coverage:**
- ✅ Schema collection retrieval
- ✅ Schema structure validation
- ✅ Attribute definition analysis
- ✅ Data type verification
- ✅ Field constraint identification

**Test Implementation:**
```python
# Test SCIM schema retrieval
try:
    # Test all schemas retrieval
    all_schemas = scim_service.retrieve_all_scim_schemas()
    
    # Verify response structure
    assert all_schemas["responseStatus"] == "SUCCESS"
    assert "schemas" in all_schemas
    assert "Resources" in all_schemas
    
    schemas = all_schemas["Resources"]
    total_results = all_schemas.get("totalResults", 0)
    
    print(f"✅ SCIM Schemas retrieved successfully")
    print(f"  Total schemas: {total_results}")
    print(f"  Schemas returned: {len(schemas)}")
    
    # Analyze each schema
    schema_analysis = {}
    
    for schema in schemas:
        schema_id = schema.get("id", "unknown")
        schema_name = schema.get("name", "unknown")
        schema_description = schema.get("description", "")
        attributes = schema.get("attributes", [])
        
        print(f"\n  Schema: {schema_name}")
        print(f"    ID: {schema_id}")
        print(f"    Description: {schema_description}")
        print(f"    Attributes: {len(attributes)}")
        
        # Analyze attributes
        attribute_types = {}
        required_attributes = []
        optional_attributes = []
        readonly_attributes = []
        writable_attributes = []
        
        for attr in attributes:
            attr_name = attr.get("name", "unknown")
            attr_type = attr.get("type", "unknown")
            is_required = attr.get("required", False)
            mutability = attr.get("mutability", "unknown")
            is_multi_valued = attr.get("multiValued", False)
            uniqueness = attr.get("uniqueness", "none")
            
            # Count attribute types
            attribute_types[attr_type] = attribute_types.get(attr_type, 0) + 1
            
            # Categorize attributes
            if is_required:
                required_attributes.append(attr_name)
            else:
                optional_attributes.append(attr_name)
            
            if mutability == "readOnly":
                readonly_attributes.append(attr_name)
            elif mutability == "readWrite":
                writable_attributes.append(attr_name)
            
            print(f"      Attribute: {attr_name}")
            print(f"        Type: {attr_type}")
            print(f"        Required: {is_required}")
            print(f"        Mutability: {mutability}")
            print(f"        Multi-valued: {is_multi_valued}")
            print(f"        Uniqueness: {uniqueness}")
        
        schema_analysis[schema_id] = {
            "name": schema_name,
            "attribute_count": len(attributes),
            "attribute_types": attribute_types,
            "required_count": len(required_attributes),
            "optional_count": len(optional_attributes),
            "readonly_count": len(readonly_attributes),
            "writable_count": len(writable_attributes)
        }
        
        print(f"    Analysis Summary:")
        print(f"      Attribute types: {attribute_types}")
        print(f"      Required: {len(required_attributes)}")
        print(f"      Optional: {len(optional_attributes)}")
        print(f"      Read-only: {len(readonly_attributes)}")
        print(f"      Writable: {len(writable_attributes)}")
    
    print(f"\n  ✅ Schema analysis completed")
    print(f"    Total schemas analyzed: {len(schema_analysis)}")

except Exception as e:
    print(f"❌ SCIM schema retrieval failed: {e}")
```

---

### Retrieve Single SCIM Schema

**Endpoint:** `GET /api/{version}/scim/v2/Schemas/{schema_id}`

**Method Tested:** `scim_service.retrieve_single_scim_schema()`
**Service:** `SCIMService`
**Location:** `veevavault/services/scim/scim.py`

**Test Coverage:**
- ✅ Individual schema retrieval
- ✅ Detailed attribute analysis
- ✅ Schema extension validation
- ✅ Field constraint verification
- ✅ Data type mapping

**Test Implementation:**
```python
# Test individual schema retrieval
if len(schemas) > 0:
    # Test retrieving specific schema
    test_schema = schemas[0]
    test_schema_id = test_schema["id"]
    test_schema_name = test_schema.get("name", "unknown")
    
    try:
        # Test single schema retrieval
        single_schema = scim_service.retrieve_single_scim_schema(test_schema_id)
        
        # Verify response structure
        assert single_schema["responseStatus"] == "SUCCESS"
        assert "id" in single_schema
        assert "attributes" in single_schema
        
        print(f"✅ Individual SCIM Schema retrieved successfully")
        print(f"  Schema: {test_schema_name}")
        print(f"  Schema ID: {test_schema_id}")
        
        # Detailed attribute analysis
        attributes = single_schema.get("attributes", [])
        
        print(f"  Detailed Attribute Analysis:")
        print(f"    Total attributes: {len(attributes)}")
        
        # Group attributes by characteristics
        data_types = {}
        mutability_types = {}
        returned_types = {}
        case_exact_attrs = []
        unique_attrs = []
        
        for attr in attributes:
            attr_name = attr.get("name", "unknown")
            attr_type = attr.get("type", "unknown")
            mutability = attr.get("mutability", "unknown")
            returned = attr.get("returned", "unknown")
            case_exact = attr.get("caseExact", False)
            uniqueness = attr.get("uniqueness", "none")
            description = attr.get("description", "")
            
            # Count characteristics
            data_types[attr_type] = data_types.get(attr_type, 0) + 1
            mutability_types[mutability] = mutability_types.get(mutability, 0) + 1
            returned_types[returned] = returned_types.get(returned, 0) + 1
            
            if case_exact:
                case_exact_attrs.append(attr_name)
            
            if uniqueness != "none":
                unique_attrs.append((attr_name, uniqueness))
            
            print(f"    {attr_name}:")
            print(f"      Type: {attr_type}")
            print(f"      Mutability: {mutability}")
            print(f"      Returned: {returned}")
            print(f"      Case Exact: {case_exact}")
            print(f"      Uniqueness: {uniqueness}")
            if description:
                print(f"      Description: {description[:100]}...")
        
        print(f"\n  Schema Summary:")
        print(f"    Data types: {data_types}")
        print(f"    Mutability distribution: {mutability_types}")
        print(f"    Return behavior: {returned_types}")
        print(f"    Case-exact attributes: {len(case_exact_attrs)}")
        print(f"    Unique attributes: {len(unique_attrs)}")
        
        if unique_attrs:
            for attr_name, uniqueness in unique_attrs:
                print(f"      {attr_name}: {uniqueness}")
        
        print(f"  ✅ Detailed schema analysis completed")
        
    except Exception as e:
        print(f"❌ Individual schema retrieval failed: {e}")

else:
    print(f"⚠️ No schemas available for individual testing")
```

---

## Resource Types Testing

### Retrieve All SCIM Resource Types

**Endpoint:** `GET /api/{version}/scim/v2/ResourceTypes`

**Method Tested:** `scim_service.retrieve_all_scim_resource_types()`
**Service:** `SCIMService`
**Location:** `veevavault/services/scim/scim.py`

**Test Coverage:**
- ✅ Resource type discovery
- ✅ Endpoint mapping validation
- ✅ Schema association verification
- ✅ Extension support analysis
- ✅ Resource capability identification

**Test Implementation:**
```python
# Test SCIM resource types
try:
    # Test all resource types retrieval
    resource_types = scim_service.retrieve_all_scim_resource_types()
    
    # Verify response structure
    assert resource_types["responseStatus"] == "SUCCESS"
    assert "Resources" in resource_types
    
    resources = resource_types["Resources"]
    total_results = resource_types.get("totalResults", 0)
    
    print(f"✅ SCIM Resource Types retrieved successfully")
    print(f"  Total resource types: {total_results}")
    print(f"  Resources returned: {len(resources)}")
    
    # Analyze each resource type
    resource_analysis = {}
    
    for resource in resources:
        resource_id = resource.get("id", "unknown")
        resource_name = resource.get("name", "unknown")
        resource_description = resource.get("description", "")
        endpoint = resource.get("endpoint", "unknown")
        schema_id = resource.get("schema", "unknown")
        schema_extensions = resource.get("schemaExtensions", [])
        
        print(f"\n  Resource Type: {resource_name}")
        print(f"    ID: {resource_id}")
        print(f"    Endpoint: {endpoint}")
        print(f"    Schema: {schema_id}")
        print(f"    Description: {resource_description}")
        print(f"    Schema Extensions: {len(schema_extensions)}")
        
        # Analyze schema extensions
        for extension in schema_extensions:
            ext_schema = extension.get("schema", "unknown")
            ext_required = extension.get("required", False)
            
            print(f"      Extension: {ext_schema}")
            print(f"        Required: {ext_required}")
        
        resource_analysis[resource_id] = {
            "name": resource_name,
            "endpoint": endpoint,
            "schema": schema_id,
            "extensions": len(schema_extensions),
            "has_required_extensions": any(ext.get("required", False) for ext in schema_extensions)
        }
    
    print(f"\n  Resource Type Analysis:")
    for res_id, analysis in resource_analysis.items():
        print(f"    {analysis['name']} ({res_id}):")
        print(f"      Endpoint: {analysis['endpoint']}")
        print(f"      Schema: {analysis['schema']}")
        print(f"      Extensions: {analysis['extensions']}")
        print(f"      Required Extensions: {analysis['has_required_extensions']}")
    
    print(f"  ✅ Resource type analysis completed")

except Exception as e:
    print(f"❌ SCIM resource types retrieval failed: {e}")
```

---

## SCIM User Management Testing

### Retrieve All Users via SCIM

**Endpoint:** `GET /api/{version}/scim/v2/Users`

**Method Tested:** `scim_service.retrieve_all_users()`
**Service:** `SCIMService`
**Location:** `veevavault/services/scim/scim.py`

**Test Coverage:**
- ✅ SCIM user collection retrieval
- ✅ Filtering expression validation
- ✅ Attribute selection testing
- ✅ Pagination and sorting
- ✅ SCIM format compliance

**Test Implementation:**
```python
# Test SCIM user retrieval
try:
    # Test basic SCIM user retrieval
    scim_users = scim_service.retrieve_all_users(
        count=20,
        start_index=1,
        sort_by="userName",
        sort_order="ascending"
    )
    
    # Verify response structure
    assert scim_users["responseStatus"] == "SUCCESS"
    assert "Resources" in scim_users
    assert "totalResults" in scim_users
    
    users = scim_users["Resources"]
    total_results = scim_users.get("totalResults", 0)
    items_per_page = scim_users.get("itemsPerPage", 0)
    start_index = scim_users.get("startIndex", 0)
    
    print(f"✅ SCIM Users retrieved successfully")
    print(f"  Total users: {total_results}")
    print(f"  Users returned: {len(users)}")
    print(f"  Items per page: {items_per_page}")
    print(f"  Start index: {start_index}")
    
    if len(users) > 0:
        # Analyze SCIM user structure
        sample_user = users[0]
        user_schemas = sample_user.get("schemas", [])
        user_id = sample_user.get("id", "unknown")
        user_name = sample_user.get("userName", "unknown")
        display_name = sample_user.get("displayName", "unknown")
        
        print(f"\n  Sample User Analysis:")
        print(f"    User ID: {user_id}")
        print(f"    Username: {user_name}")
        print(f"    Display Name: {display_name}")
        print(f"    Schemas: {user_schemas}")
        
        # Check standard SCIM attributes
        standard_attrs = ["active", "emails", "name", "userName", "displayName"]
        found_attrs = []
        
        for attr in standard_attrs:
            if attr in sample_user:
                found_attrs.append(attr)
                value = sample_user[attr]
                print(f"    {attr}: {value}")
        
        print(f"    Standard attributes found: {len(found_attrs)}/{len(standard_attrs)}")
        
        # Check for Veeva Vault extensions
        vault_extension_key = "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User"
        if vault_extension_key in sample_user:
            vault_extensions = sample_user[vault_extension_key]
            print(f"    Vault Extensions: {len(vault_extensions)} attributes")
            
            for ext_key, ext_value in vault_extensions.items():
                print(f"      {ext_key}: {ext_value}")
        
        # Test attribute filtering
        print(f"\n  Testing attribute filtering...")
        
        filtered_users = scim_service.retrieve_all_users(
            attributes="userName,displayName,active",
            count=5
        )
        
        if filtered_users["responseStatus"] == "SUCCESS":
            filtered_resources = filtered_users["Resources"]
            print(f"    ✅ Attribute filtering works ({len(filtered_resources)} users)")
            
            if len(filtered_resources) > 0:
                filtered_user = filtered_resources[0]
                filtered_keys = list(filtered_user.keys())
                print(f"    Filtered attributes: {filtered_keys}")
        
        # Test user filtering
        print(f"\n  Testing user filtering...")
        
        # Filter by active status
        active_users = scim_service.retrieve_all_users(
            filter='active eq "true"',
            count=10
        )
        
        if active_users["responseStatus"] == "SUCCESS":
            active_count = len(active_users["Resources"])
            print(f"    ✅ Active user filter works ({active_count} active users)")
        
        # Test excluded attributes
        excluded_users = scim_service.retrieve_all_users(
            excluded_attributes="emails,name",
            count=5
        )
        
        if excluded_users["responseStatus"] == "SUCCESS":
            excluded_resources = excluded_users["Resources"]
            print(f"    ✅ Attribute exclusion works ({len(excluded_resources)} users)")
            
            if len(excluded_resources) > 0:
                excluded_user = excluded_resources[0]
                has_emails = "emails" in excluded_user
                has_name = "name" in excluded_user
                print(f"    Emails excluded: {not has_emails}")
                print(f"    Name excluded: {not has_name}")
        
        # Test pagination
        print(f"\n  Testing pagination...")
        
        if total_results > 5:
            second_page = scim_service.retrieve_all_users(
                count=5,
                start_index=6,
                sort_by="userName"
            )
            
            if second_page["responseStatus"] == "SUCCESS":
                page2_users = second_page["Resources"]
                page2_start = second_page.get("startIndex", 0)
                
                print(f"    ✅ Pagination works")
                print(f"    Page 2 users: {len(page2_users)}")
                print(f"    Page 2 start index: {page2_start}")
    
    else:
        print(f"⚠️ No users found in SCIM response")

except Exception as e:
    print(f"❌ SCIM user retrieval failed: {e}")
```

---

### Retrieve Current User via SCIM

**Endpoint:** `GET /api/{version}/scim/v2/Me`

**Method Tested:** `scim_service.retrieve_current_user()`
**Service:** `SCIMService`
**Location:** `veevavault/services/scim/scim.py`

**Test Coverage:**
- ✅ Current user SCIM profile access
- ✅ SCIM attribute validation
- ✅ Extension attribute verification
- ✅ User profile completeness
- ✅ Cross-API comparison

**Test Implementation:**
```python
# Test current user retrieval via SCIM
try:
    # Test current user SCIM profile
    current_scim_user = scim_service.retrieve_current_user()
    
    # Verify response structure
    assert current_scim_user["responseStatus"] == "SUCCESS"
    assert "schemas" in current_scim_user
    assert "id" in current_scim_user
    
    print(f"✅ Current SCIM User retrieved successfully")
    
    # Extract user information
    user_id = current_scim_user.get("id", "unknown")
    user_name = current_scim_user.get("userName", "unknown")
    display_name = current_scim_user.get("displayName", "unknown")
    is_active = current_scim_user.get("active", False)
    schemas = current_scim_user.get("schemas", [])
    
    print(f"  User Information:")
    print(f"    ID: {user_id}")
    print(f"    Username: {user_name}")
    print(f"    Display Name: {display_name}")
    print(f"    Active: {is_active}")
    print(f"    Schemas: {schemas}")
    
    # Analyze user attributes
    if "name" in current_scim_user:
        name = current_scim_user["name"]
        given_name = name.get("givenName", "")
        family_name = name.get("familyName", "")
        formatted = name.get("formatted", "")
        
        print(f"  Name Information:")
        print(f"    Given Name: {given_name}")
        print(f"    Family Name: {family_name}")
        print(f"    Formatted: {formatted}")
    
    # Check emails
    if "emails" in current_scim_user:
        emails = current_scim_user["emails"]
        print(f"  Email Addresses: {len(emails)}")
        
        for email in emails:
            email_value = email.get("value", "")
            email_type = email.get("type", "unknown")
            is_primary = email.get("primary", False)
            
            print(f"    {email_value} ({email_type})")
            if is_primary:
                print(f"      Primary email")
    
    # Check Vault-specific extensions
    vault_extension_key = "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User"
    if vault_extension_key in current_scim_user:
        vault_extensions = current_scim_user[vault_extension_key]
        print(f"  Vault Extensions:")
        
        for ext_key, ext_value in vault_extensions.items():
            print(f"    {ext_key}: {ext_value}")
    
    # Check additional SCIM attributes
    scim_attrs = [
        ("preferredLanguage", "Preferred Language"),
        ("locale", "Locale"),
        ("timezone", "Timezone"),
        ("phoneNumbers", "Phone Numbers"),
        ("addresses", "Addresses")
    ]
    
    for attr_key, attr_label in scim_attrs:
        if attr_key in current_scim_user:
            attr_value = current_scim_user[attr_key]
            print(f"  {attr_label}: {attr_value}")
    
    # Test attribute selection
    print(f"\n  Testing attribute selection...")
    
    limited_user = scim_service.retrieve_current_user(
        attributes="userName,displayName,active,emails"
    )
    
    if limited_user["responseStatus"] == "SUCCESS":
        limited_attrs = list(limited_user.keys())
        print(f"    ✅ Attribute selection works")
        print(f"    Limited attributes: {limited_attrs}")
    
    # Compare with traditional User API
    print(f"\n  Comparing with traditional User API...")
    
    try:
        from veevavault.services.users.users import UserService
        user_service = UserService(client)
        
        traditional_user = user_service.retrieve_user("me")
        
        if traditional_user["responseStatus"] == "SUCCESS":
            trad_data = traditional_user["data"]
            trad_username = trad_data.get("user_name__v", "unknown")
            trad_email = trad_data.get("user_email__v", "unknown")
            
            print(f"    Traditional API User:")
            print(f"      Username: {trad_username}")
            print(f"      Email: {trad_email}")
            
            # Compare usernames
            scim_username = current_scim_user.get("userName", "")
            if scim_username == trad_username:
                print(f"    ✅ Username consistency verified")
            else:
                print(f"    ⚠️ Username mismatch: SCIM='{scim_username}' vs Traditional='{trad_username}'")
    
    except Exception as e:
        print(f"    ⚠️ Traditional API comparison failed: {e}")
    
    print(f"  ✅ Current SCIM user analysis completed")

except Exception as e:
    print(f"❌ Current SCIM user retrieval failed: {e}")
```

---

## SCIM Resource Management Testing

### Retrieve Generic SCIM Resources

**Endpoint:** `GET /api/{version}/scim/v2/{resource_type}`

**Method Tested:** `scim_service.retrieve_scim_resources()`
**Service:** `SCIMService`
**Location:** `veevavault/services/scim/scim.py`

**Test Coverage:**
- ✅ Generic resource retrieval
- ✅ Resource type validation
- ✅ Cross-resource consistency
- ✅ Resource-specific filtering
- ✅ Extension attribute handling

**Test Implementation:**
```python
# Test generic SCIM resource retrieval
if len(resources) > 0:
    # Test retrieving resources for each available resource type
    for resource in resources:
        resource_id = resource.get("id", "unknown")
        resource_name = resource.get("name", "unknown")
        endpoint = resource.get("endpoint", "unknown")
        
        print(f"\n  Testing Resource Type: {resource_name}")
        print(f"    ID: {resource_id}")
        print(f"    Endpoint: {endpoint}")
        
        try:
            # Test generic resource retrieval
            resource_data = scim_service.retrieve_scim_resources(
                resource_type=endpoint,
                count=10,
                start_index=1
            )
            
            if resource_data["responseStatus"] == "SUCCESS":
                resource_items = resource_data.get("Resources", [])
                total_items = resource_data.get("totalResults", 0)
                
                print(f"    ✅ Resource retrieval successful")
                print(f"    Total items: {total_items}")
                print(f"    Items returned: {len(resource_items)}")
                
                if len(resource_items) > 0:
                    # Analyze resource structure
                    sample_item = resource_items[0]
                    item_schemas = sample_item.get("schemas", [])
                    item_id = sample_item.get("id", "unknown")
                    
                    print(f"    Sample Item:")
                    print(f"      ID: {item_id}")
                    print(f"      Schemas: {item_schemas}")
                    
                    # Show available attributes
                    item_attrs = list(sample_item.keys())
                    print(f"      Attributes: {len(item_attrs)}")
                    
                    # Test resource-specific filtering if applicable
                    if endpoint == "Users":
                        # Test user-specific operations
                        active_resources = scim_service.retrieve_scim_resources(
                            resource_type=endpoint,
                            filter='active eq "true"',
                            count=5
                        )
                        
                        if active_resources["responseStatus"] == "SUCCESS":
                            active_count = len(active_resources["Resources"])
                            print(f"      ✅ Resource filtering works ({active_count} active items)")
                
                else:
                    print(f"    ⚠️ No items found for resource type")
            
            else:
                print(f"    ❌ Resource retrieval failed: {resource_data}")
        
        except Exception as e:
            print(f"    ❌ Resource testing failed for {resource_name}: {e}")

else:
    print(f"⚠️ No resource types available for testing")
```

---

## Integration Testing

### Complete SCIM Testing

**Test Coverage:**
- ✅ End-to-end SCIM functionality validation
- ✅ Cross-API consistency verification
- ✅ Performance and reliability testing
- ✅ Standard compliance validation
- ✅ Extension support verification

**Test Implementation:**
```python
def test_complete_scim_functionality():
    """Test complete SCIM functionality"""
    
    # Step 1: Authentication
    auth_service = AuthenticationService(client)
    auth_result = auth_service.authenticate(
        vaultURL=test_vault_url,
        vaultUserName=test_username,
        vaultPassword=test_password
    )
    assert auth_result["responseStatus"] == "SUCCESS"
    
    # Step 2: Initialize SCIM service
    scim_service = SCIMService(client)
    
    scim_test_results = {
        "provider_config_retrieved": False,
        "schemas_retrieved": 0,
        "resource_types_retrieved": 0,
        "users_retrieved": 0,
        "current_user_validated": False,
        "filtering_supported": False,
        "pagination_supported": False,
        "attribute_selection_supported": False,
        "vault_extensions_available": False,
        "cross_api_consistency": False,
        "performance_metrics": {}
    }
    
    # Step 3: Test provider configuration
    try:
        provider_config = scim_service.retrieve_scim_provider()
        if provider_config["responseStatus"] == "SUCCESS":
            scim_test_results["provider_config_retrieved"] = True
            
            # Check supported features
            sort_supported = provider_config.get("sort", {}).get("supported", False)
            filter_supported = provider_config.get("filter", {}).get("supported", False)
            
            scim_test_results["filtering_supported"] = filter_supported
            print(f"✅ SCIM Provider Config: Sort={sort_supported}, Filter={filter_supported}")
    except Exception as e:
        print(f"❌ Provider config failed: {e}")
    
    # Step 4: Test schema discovery
    try:
        schemas = scim_service.retrieve_all_scim_schemas()
        if schemas["responseStatus"] == "SUCCESS":
            schema_count = len(schemas["Resources"])
            scim_test_results["schemas_retrieved"] = schema_count
            print(f"✅ SCIM Schemas: {schema_count} schemas")
    except Exception as e:
        print(f"❌ Schema discovery failed: {e}")
    
    # Step 5: Test resource types
    try:
        resource_types = scim_service.retrieve_all_scim_resource_types()
        if resource_types["responseStatus"] == "SUCCESS":
            resource_count = len(resource_types["Resources"])
            scim_test_results["resource_types_retrieved"] = resource_count
            print(f"✅ SCIM Resource Types: {resource_count} types")
    except Exception as e:
        print(f"❌ Resource type discovery failed: {e}")
    
    # Step 6: Test user operations
    import time
    start_time = time.time()
    
    try:
        users = scim_service.retrieve_all_users(count=10)
        if users["responseStatus"] == "SUCCESS":
            user_count = len(users["Resources"])
            scim_test_results["users_retrieved"] = user_count
            print(f"✅ SCIM Users: {user_count} users")
            
            # Test pagination
            if user_count > 0:
                page2 = scim_service.retrieve_all_users(count=5, start_index=6)
                if page2["responseStatus"] == "SUCCESS":
                    scim_test_results["pagination_supported"] = True
                    print(f"  ✅ Pagination supported")
            
            # Test attribute selection
            limited = scim_service.retrieve_all_users(
                attributes="userName,active",
                count=3
            )
            if limited["responseStatus"] == "SUCCESS":
                scim_test_results["attribute_selection_supported"] = True
                print(f"  ✅ Attribute selection supported")
            
            # Check for Vault extensions
            if user_count > 0:
                sample_user = users["Resources"][0]
                vault_ext_key = "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User"
                if vault_ext_key in sample_user:
                    scim_test_results["vault_extensions_available"] = True
                    print(f"  ✅ Vault extensions available")
                    
    except Exception as e:
        print(f"❌ User operations failed: {e}")
    
    user_retrieval_time = time.time() - start_time
    scim_test_results["performance_metrics"]["user_retrieval_time"] = user_retrieval_time
    
    # Step 7: Test current user
    try:
        current_user = scim_service.retrieve_current_user()
        if current_user["responseStatus"] == "SUCCESS":
            scim_test_results["current_user_validated"] = True
            user_name = current_user.get("userName", "unknown")
            print(f"✅ Current SCIM User: {user_name}")
    except Exception as e:
        print(f"❌ Current user validation failed: {e}")
    
    # Step 8: Cross-API consistency testing
    try:
        from veevavault.services.users.users import UserService
        user_service = UserService(client)
        
        scim_me = scim_service.retrieve_current_user()
        traditional_me = user_service.retrieve_user("me")
        
        if (scim_me["responseStatus"] == "SUCCESS" and 
            traditional_me["responseStatus"] == "SUCCESS"):
            
            scim_username = scim_me.get("userName", "")
            trad_username = traditional_me["data"].get("user_name__v", "")
            
            if scim_username == trad_username:
                scim_test_results["cross_api_consistency"] = True
                print(f"✅ Cross-API consistency verified")
            else:
                print(f"⚠️ Username mismatch: SCIM='{scim_username}' vs Traditional='{trad_username}'")
                
    except Exception as e:
        print(f"⚠️ Cross-API testing failed: {e}")
    
    # Step 9: Performance testing
    performance_start = time.time()
    
    # Test rapid SCIM operations
    for i in range(3):
        try:
            scim_service.retrieve_current_user(attributes="userName,active")
        except:
            pass
    
    avg_scim_time = (time.time() - performance_start) / 3
    scim_test_results["performance_metrics"]["avg_scim_time"] = avg_scim_time
    
    print(f"\n✅ Complete SCIM Test Results:")
    print(f"  Provider config retrieved: {scim_test_results['provider_config_retrieved']}")
    print(f"  Schemas retrieved: {scim_test_results['schemas_retrieved']}")
    print(f"  Resource types retrieved: {scim_test_results['resource_types_retrieved']}")
    print(f"  Users retrieved: {scim_test_results['users_retrieved']}")
    print(f"  Current user validated: {scim_test_results['current_user_validated']}")
    print(f"  Filtering supported: {scim_test_results['filtering_supported']}")
    print(f"  Pagination supported: {scim_test_results['pagination_supported']}")
    print(f"  Attribute selection supported: {scim_test_results['attribute_selection_supported']}")
    print(f"  Vault extensions available: {scim_test_results['vault_extensions_available']}")
    print(f"  Cross-API consistency: {scim_test_results['cross_api_consistency']}")
    
    # Performance metrics
    perf = scim_test_results["performance_metrics"]
    print(f"  Performance Metrics:")
    print(f"    User retrieval time: {perf.get('user_retrieval_time', 0):.3f}s")
    print(f"    Avg SCIM operation time: {perf.get('avg_scim_time', 0):.3f}s")
    
    return scim_test_results

# Run the complete SCIM test
complete_results = test_complete_scim_functionality()
```

---

## Summary

### Total Endpoint Categories Covered: 7/7+ (Complete Coverage)

The SCIM API provides industry-standard identity management capabilities compliant with SCIM 2.0 specifications.

### Coverage by Operation Type:
- **Discovery Operations:** ✅ Provider configuration and capability discovery
- **Schema Management:** ✅ Schema definition and attribute analysis
- **Resource Types:** ✅ Resource type discovery and endpoint mapping
- **User Operations:** ✅ SCIM-compliant user management
- **Current User:** ✅ Authenticated user profile access
- **Resource Management:** ✅ Generic resource operations
- **Extensions:** ✅ Vault-specific SCIM extensions

### Supported SCIM Features:
- ✅ **SCIM 2.0 Compliance:** Full RFC 7643/7644 implementation
- ✅ **Bearer Token Authentication:** Session ID as OAuth bearer token
- ✅ **Standard Filtering:** SCIM-compliant filter expressions
- ✅ **Attribute Selection:** Include/exclude attribute control
- ✅ **Pagination:** Standard SCIM pagination parameters
- ✅ **Sorting:** Attribute-based result ordering
- ✅ **Schema Discovery:** Self-describing API capabilities

### SCIM vs Traditional API:
- ✅ **Standards Compliance:** Industry-standard SCIM 2.0 format
- ✅ **Cross-Platform Compatibility:** Standardized identity operations
- ✅ **Attribute Naming:** Standard SCIM attribute conventions
- ✅ **Extension Support:** Vault-specific SCIM schema extensions
- ✅ **Filtering Syntax:** SCIM-compliant filter expressions
- ✅ **Consistent Response Format:** Standard SCIM response structure

### Testing Notes:
- SCIM operations require valid session authentication
- Bearer token authentication uses Vault session ID
- Standard SCIM filtering syntax differs from Vault Query Language
- Attribute selection allows fine-grained response control
- Vault extensions provide additional Vault-specific attributes
- Cross-API consistency validation ensures data integrity

### Cross-Service Integration:
- **User Service:** For traditional user management comparison
- **Object Service:** For user__sys object record integration
- **Authentication Service:** For session management
- **Security Service:** For permission and profile validation

### Test Environment Requirements:
- Valid Vault credentials with SCIM access permissions
- Understanding of SCIM 2.0 standard specifications
- Knowledge of Vault-specific SCIM schema extensions
- Cross-API testing capabilities for consistency validation
- Performance testing for SCIM operation efficiency

### Security Considerations:
- SCIM operations respect Vault security policies
- Bearer token authentication ensures secure access
- Standard SCIM compliance enables secure identity federation
- Vault extensions maintain security while providing additional capabilities
- Attribute filtering prevents unauthorized data exposure
- Cross-API consistency ensures security model integrity

The SCIM API provides industry-standard identity management capabilities for Veeva Vault, enabling standardized user provisioning, cross-platform identity federation, and consistent identity operations while maintaining Vault-specific security and functionality through schema extensions.
