# VeevaVault MCP Server Architecture Design

## Executive Summary

This document presents a comprehensive architectural analysis for building a Model Context Protocol (MCP) server that enables LLMs to interact with Veeva Vault through the VeevaVaultMCP API wrapper library. Four distinct implementation variations are analyzed with their respective trade-offs, followed by a final recommendation.

**Recommendation**: **Variation 3: Resource-Oriented Approach** provides the optimal balance of usability, maintainability, and alignment with MCP best practices.

---

## Current State Analysis

### Codebase Statistics
- **115 service implementation files** across 26 service directories
- **81 Service classes** with 564+ public methods
- **600+ API endpoints** covering comprehensive Vault functionality
- **27 major service modules** including:
  - Documents (17 sub-services)
  - Objects (11 sub-services)
  - Binders (12 sub-services)
  - Workflows (3 sub-services)
  - Authentication
  - Queries (VQL)
  - Clinical Operations
  - Safety (E2B pharmacovigilance)
  - File Staging
  - Picklists
  - And 17 more specialized services

### Service Architecture Pattern
The codebase follows a **hierarchical service delegation pattern**:

```
VaultClient (client/vault_client.py)
    └── Main Service (e.g., DocumentService)
            └── Specialized Sub-Services (e.g., DocumentRetrievalService, DocumentCreationService)
                    └── Individual API Methods
```

**Example**: DocumentService delegates to 17 specialized services (fields, types, retrieval, creation, update, deletion, locks, renditions, attachments, annotations, relationships, exports, events, templates, signatures, tokens, roles).

---

## MCP Architecture Fundamentals

### Core MCP Concepts
1. **Tools**: Functions that LLMs can invoke to perform actions
2. **Resources**: Data/content that LLMs can read (documents, objects, etc.)
3. **Prompts**: Reusable prompt templates for common workflows
4. **Server**: Exposes tools, resources, and prompts via standard JSON-RPC protocol

### MCP Best Practices (2025)
1. **Single Responsibility**: Each MCP server should have one clear purpose
2. **Avoid Over-Tooling**: Don't map every API endpoint to a tool; group related tasks
3. **Security First**: Explicit user consent, OAuth2 resource indicators (RFC 8707)
4. **Logging & Observability**: Comprehensive logging for debugging
5. **Modularity**: Decouple components for independent scaling
6. **Containerization**: Docker packaging for consistency

---

## Implementation Variation 1: Flat High-Level Tool Approach

### Design Overview
Create a **minimal set of high-level tools** that represent **user intent** rather than individual API endpoints. Map common workflows to approximately 20-40 tools.

### Architecture

```
MCP Server
├── Authentication
│   ├── vault_authenticate
│   └── vault_logout
├── Document Operations
│   ├── vault_search_documents
│   ├── vault_get_document
│   ├── vault_create_document
│   ├── vault_update_document
│   ├── vault_delete_document
│   ├── vault_download_document
│   ├── vault_upload_document
│   └── vault_manage_document_lifecycle
├── Object Operations
│   ├── vault_query_objects
│   ├── vault_get_object_record
│   ├── vault_create_object_record
│   ├── vault_update_object_record
│   ├── vault_delete_object_record
│   └── vault_bulk_object_operations
├── Query Operations
│   ├── vault_execute_vql
│   └── vault_bulk_query
├── Workflow Operations
│   ├── vault_initiate_workflow
│   ├── vault_complete_task
│   └── vault_get_workflow_status
├── Metadata Operations
│   ├── vault_get_document_types
│   ├── vault_get_object_metadata
│   └── vault_get_picklists
└── Specialized Applications
    ├── vault_clinical_operations
    ├── vault_safety_case_intake
    └── vault_file_staging
```

### Tool Design Example

```python
@mcp.tool()
def vault_search_documents(
    query: str = None,
    document_type: str = None,
    status: str = None,
    created_after: str = None,
    limit: int = 100
) -> dict:
    """
    Search for documents in Veeva Vault.

    Args:
        query: Full-text search query
        document_type: Filter by document type
        status: Filter by lifecycle state (draft, approved, etc.)
        created_after: ISO date string
        limit: Maximum results to return

    Returns:
        List of matching documents with metadata
    """
    # Construct VQL query based on parameters
    # Call appropriate service methods
    # Return formatted results
```

### Pros
✅ **Excellent LLM Usability**: Tools map to natural user intents ("search documents", "create record")
✅ **Minimal Tool Count**: ~30-40 tools are easy for LLMs to navigate and select
✅ **Follows MCP Best Practice**: Avoids over-tooling anti-pattern
✅ **Clear Abstraction**: Hides API complexity from LLM
✅ **Faster LLM Decision Making**: Fewer tools = faster tool selection
✅ **Better Documentation**: Each tool can have comprehensive docstrings

### Cons
❌ **Reduced Granularity**: May not expose all specialized endpoints
❌ **Parameter Complexity**: High-level tools may have many optional parameters
❌ **Workflow Assumptions**: May encode assumptions about how users work
❌ **Harder to Extend**: Adding new capabilities requires careful tool design
❌ **Potential Information Loss**: Abstracting 600+ endpoints to 30 tools loses details
❌ **Custom Logic Required**: Need to write wrapper logic for parameter mapping

### Implementation Complexity
**Medium**: Requires thoughtful design of high-level workflows and parameter mapping.

### Best For
- General-purpose Vault interactions
- Users who want simple, intuitive tool names
- Production deployments where LLM token efficiency matters

---

## Implementation Variation 2: Service-Grouped Tool Approach

### Design Overview
Create tools that **map directly to service classes**, with each main service becoming a namespace of related tools. Approximately 80-120 tools organized by service module.

### Architecture

```
MCP Server
├── documents.get_types
├── documents.get_fields
├── documents.retrieve_single
├── documents.retrieve_all_versions
├── documents.create_single
├── documents.create_multiple
├── documents.update_single
├── documents.delete_single
├── documents.lock
├── documents.unlock
├── documents.add_rendition
├── documents.export_to_package
├── objects.get_metadata
├── objects.get_all_objects
├── objects.create_record
├── objects.update_record
├── objects.delete_record
├── objects.query_records
├── objects.get_attachment
├── binders.create
├── binders.add_document
├── binders.retrieve_structure
├── queries.execute_vql
├── queries.bulk_query
├── workflows.initiate
├── workflows.get_tasks
├── auth.login
├── auth.logout
└── [... ~80-120 more tools]
```

### Tool Design Example

```python
@mcp.tool()
def documents_retrieve_single(
    document_id: str,
    version: str = "latest"
) -> dict:
    """
    Retrieve a single document by ID.

    Args:
        document_id: The document ID
        version: Version number or 'latest'

    Returns:
        Document metadata and content
    """
    service = get_document_service()
    return service.retrieval.retrieve_single_document(document_id, version)

@mcp.tool()
def documents_create_single(
    document_type: str,
    name: str,
    lifecycle: str,
    **fields
) -> dict:
    """
    Create a new document.

    Args:
        document_type: Document type API name
        name: Document name
        lifecycle: Lifecycle API name
        **fields: Additional field values

    Returns:
        Created document ID and metadata
    """
    service = get_document_service()
    return service.creation.create_single_document(
        document_type=document_type,
        name=name,
        lifecycle=lifecycle,
        **fields
    )
```

### Pros
✅ **Direct API Mapping**: One-to-one correspondence with existing service methods
✅ **Complete Coverage**: Exposes all 564+ methods as tools
✅ **Easy to Implement**: Minimal wrapper logic, mostly pass-through
✅ **Easy to Maintain**: Adding new API methods is straightforward
✅ **Granular Control**: LLM can access any specific endpoint
✅ **Developer Friendly**: Service names match codebase structure

### Cons
❌ **Too Many Tools**: 80-120+ tools overwhelm LLM tool selection
❌ **Violates MCP Best Practice**: Over-tooling anti-pattern
❌ **Poor LLM Performance**: More tools = slower decision making, higher token usage
❌ **Namespace Verbosity**: Tool names like `documents_retrieve_single_document_by_id_with_version` get long
❌ **Requires Domain Knowledge**: LLM needs to understand service architecture
❌ **Fragmented Workflows**: Multi-step tasks require multiple tool calls

### Implementation Complexity
**Low**: Straightforward mapping from service methods to MCP tools.

### Best For
- Developer-focused use cases
- Scenarios requiring complete API access
- Internal tools where users understand the service architecture

---

## Implementation Variation 3: Resource-Oriented Approach

### Design Overview
Organize around **Vault resource types** (Documents, Objects, Binders, Users, etc.) with **CRUD + specialized operations** for each. Approximately 50-70 tools following RESTful patterns.

### Architecture

```
MCP Server
├── Authentication
│   ├── vault_auth
│   └── vault_logout
│
├── Documents Resource
│   ├── documents_query           # Search/list documents (VQL or filters)
│   ├── documents_get             # Retrieve single document
│   ├── documents_create          # Create new document
│   ├── documents_update          # Update existing document
│   ├── documents_delete          # Delete document
│   ├── documents_lock            # Lock for editing
│   ├── documents_unlock          # Unlock
│   ├── documents_upload_content  # Upload file content
│   ├── documents_download_content # Download file content
│   ├── documents_get_versions    # Get version history
│   ├── documents_add_rendition   # Add rendition (PDF, etc.)
│   ├── documents_manage_lifecycle # Change state/workflow
│   └── documents_get_metadata    # Get metadata/schema
│
├── Objects Resource
│   ├── objects_query             # VQL query on objects
│   ├── objects_get               # Get single record
│   ├── objects_create            # Create record
│   ├── objects_update            # Update record
│   ├── objects_delete            # Delete record
│   ├── objects_bulk_upsert       # Bulk operations
│   ├── objects_get_metadata      # Get object schema
│   └── objects_manage_attachments # Attachment operations
│
├── Binders Resource
│   ├── binders_query
│   ├── binders_get
│   ├── binders_create
│   ├── binders_update
│   ├── binders_delete
│   ├── binders_add_document
│   ├── binders_remove_document
│   └── binders_export
│
├── Users Resource
│   ├── users_query
│   ├── users_get
│   ├── users_create
│   ├── users_update
│   ├── users_disable
│   └── users_get_permissions
│
├── Workflows Resource
│   ├── workflows_query_tasks
│   ├── workflows_get_task
│   ├── workflows_complete_task
│   ├── workflows_initiate
│   └── workflows_reassign_task
│
├── VQL Resource
│   ├── vql_execute              # Execute arbitrary VQL
│   ├── vql_bulk_export          # Large query with pagination
│   └── vql_validate             # Validate VQL syntax
│
├── Metadata Resource
│   ├── metadata_get_document_types
│   ├── metadata_get_object_types
│   ├── metadata_get_picklists
│   ├── metadata_get_lifecycles
│   └── metadata_get_workflows
│
└── Specialized Resources
    ├── clinical_operations_*     # 8-10 clinical-specific tools
    ├── safety_*                  # 5-7 safety case tools
    ├── file_staging_*            # 5-7 file staging tools
    └── groups_*                  # 4-6 group management tools
```

### Tool Design Example

```python
@mcp.tool()
def documents_query(
    vql: str = None,
    name_contains: str = None,
    document_type: str = None,
    lifecycle_state: str = None,
    created_by: str = None,
    created_after: str = None,
    modified_after: str = None,
    limit: int = 100,
    return_format: str = "summary"  # summary | full | ids_only
) -> dict:
    """
    Query documents in Vault using VQL or common filter parameters.

    Use this tool to search for documents, list documents, or find specific documents
    matching criteria. You can either provide a raw VQL query or use the filter parameters.

    Args:
        vql: Raw VQL query (takes precedence over filters if provided)
        name_contains: Filter by document name (partial match)
        document_type: Document type API name (e.g., 'general_document__c')
        lifecycle_state: Lifecycle state (e.g., 'draft__c', 'approved__c')
        created_by: User ID who created the document
        created_after: ISO date string (e.g., '2025-01-01')
        modified_after: ISO date string
        limit: Maximum results to return (default 100, max 1000)
        return_format: 'summary' (id, name, type), 'full' (all fields), 'ids_only'

    Returns:
        {
            "total": 42,
            "returned": 100,
            "documents": [
                {
                    "id": "DOC-12345",
                    "name": "Clinical Protocol",
                    "type": "protocol__c",
                    "state": "approved__c",
                    "version": "2.0",
                    ...
                }
            ]
        }
    """
    service = get_query_service()

    # Build VQL if not provided
    if not vql:
        vql = build_document_query(
            name_contains=name_contains,
            document_type=document_type,
            lifecycle_state=lifecycle_state,
            created_by=created_by,
            created_after=created_after,
            modified_after=modified_after,
            limit=limit
        )

    # Execute query
    results = service.query(vql)

    # Format based on return_format
    return format_document_results(results, return_format)


@mcp.tool()
def documents_create(
    name: str,
    type: str,
    lifecycle: str,
    classification: str = None,
    file_path: str = None,
    **custom_fields
) -> dict:
    """
    Create a new document in Vault.

    Args:
        name: Document name
        type: Document type API name
        lifecycle: Lifecycle API name
        classification: Document classification
        file_path: Optional path to file content to upload
        **custom_fields: Additional field values (field_name__c: value)

    Returns:
        {
            "id": "DOC-12345",
            "version": "0.1",
            "url": "https://vault.example.com/...",
            "status": "created"
        }
    """
    service = get_document_service()

    # Create document metadata
    result = service.creation.create_single_document(
        name=name,
        type=type,
        lifecycle=lifecycle,
        classification=classification,
        **custom_fields
    )

    # Upload content if file provided
    if file_path and result.get("id"):
        upload_result = service.update.upload_document_content(
            document_id=result["id"],
            file_path=file_path
        )
        result["content_uploaded"] = upload_result.get("responseStatus") == "SUCCESS"

    return result
```

### MCP Resources Definition

In addition to tools, define **MCP Resources** for browsing Vault content:

```python
@mcp.resource("vault://documents/{doc_id}")
def get_document_resource(uri: str) -> dict:
    """Retrieve document as an MCP resource"""
    doc_id = extract_id_from_uri(uri)
    service = get_document_service()
    return service.retrieval.retrieve_single_document(doc_id)

@mcp.resource("vault://objects/{object_name}/{record_id}")
def get_object_resource(uri: str) -> dict:
    """Retrieve object record as an MCP resource"""
    object_name, record_id = extract_from_uri(uri)
    service = get_object_service()
    return service.crud.retrieve_object_record(object_name, record_id)

# MCP Resource listing
@mcp.list_resources()
def list_vault_resources() -> list:
    """Return browsable Vault resources"""
    return [
        {"uri": "vault://documents/", "name": "Documents", "mimeType": "application/json"},
        {"uri": "vault://objects/", "name": "Objects", "mimeType": "application/json"},
        {"uri": "vault://binders/", "name": "Binders", "mimeType": "application/json"},
    ]
```

### Pros
✅ **RESTful Intuition**: Familiar CRUD pattern for resources
✅ **Balanced Tool Count**: 50-70 tools is manageable for LLMs
✅ **Resource Organization**: Clear conceptual model (Documents, Objects, etc.)
✅ **Aligns with MCP Best Practices**: Avoids over-tooling while maintaining coverage
✅ **Extensible**: Easy to add new resources without disrupting existing tools
✅ **Supports MCP Resources**: Natural mapping to MCP resource URIs
✅ **Developer & LLM Friendly**: Both humans and LLMs understand resource concepts
✅ **Consistent Naming**: Predictable pattern (resource_action)

### Cons
❌ **Some Specialization Lost**: Highly specialized endpoints might not fit cleanly
❌ **Workflow Complexity**: Multi-step workflows still require multiple tools
❌ **Parameter Overload**: Query/search tools may have many optional parameters
❌ **Requires Schema Knowledge**: LLM needs to know object types, field names

### Implementation Complexity
**Medium-High**: Requires careful resource modeling and intelligent parameter handling.

### Best For
- **Production MCP deployments** (RECOMMENDED)
- General-purpose Vault interaction
- Users familiar with REST APIs
- Scenarios where LLMs need to browse and interact with Vault content
- Balance between usability and completeness

---

## Implementation Variation 4: Hybrid Dynamic Context Approach

### Design Overview
Combine **high-level tools** for common operations with **dynamic tool generation** for specialized contexts. Start with ~30 core tools and dynamically expose additional tools based on conversation context.

### Architecture

```
MCP Server
├── Core Tools (Always Available - ~30 tools)
│   ├── vault_auth
│   ├── vault_execute_vql
│   ├── vault_search
│   ├── vault_get_resource
│   ├── vault_create_resource
│   ├── vault_update_resource
│   ├── vault_delete_resource
│   ├── vault_discover_tools
│   └── vault_load_context
│
├── Context-Specific Tools (Loaded Dynamically)
│   ├── Clinical Operations Context
│   │   ├── clinical_create_etmf_binder
│   │   ├── clinical_track_milestone
│   │   └── clinical_sync_opendata
│   │
│   ├── Safety Context
│   │   ├── safety_intake_e2b_r3
│   │   ├── safety_validate_case
│   │   └── safety_export_case
│   │
│   ├── Document Management Context
│   │   ├── doc_advanced_search
│   │   ├── doc_bulk_state_change
│   │   └── doc_version_compare
│   │
│   └── Admin Context
│       ├── admin_manage_users
│       ├── admin_configure_security
│       └── admin_audit_trail
│
└── Meta Tools
    ├── vault_list_available_contexts
    ├── vault_activate_context
    └── vault_get_tool_documentation
```

### Tool Design Example

```python
# Core high-level tool
@mcp.tool()
def vault_search(
    resource_type: str,  # "documents", "objects", "users", etc.
    query: str = None,
    filters: dict = None,
    limit: int = 100
) -> dict:
    """
    Universal search across Vault resources.

    Args:
        resource_type: Type of resource to search
        query: Search query string
        filters: Dictionary of filter criteria
        limit: Max results
    """
    # Route to appropriate service based on resource_type
    pass

# Context discovery tool
@mcp.tool()
def vault_discover_tools(
    resource_type: str = None,
    use_case: str = None
) -> dict:
    """
    Discover available specialized tools for a specific context.

    Args:
        resource_type: Filter by resource type (documents, clinical, safety)
        use_case: Describe your use case to get relevant tools

    Returns:
        List of available tools with descriptions and when to use them
    """
    available_contexts = {
        "clinical_operations": {
            "description": "Tools for clinical trial document management",
            "tools": ["clinical_create_etmf_binder", "clinical_track_milestone"],
            "use_cases": ["eTMF management", "clinical milestones", "OpenData Clinical sync"]
        },
        "safety": {
            "description": "Pharmacovigilance and safety case management",
            "tools": ["safety_intake_e2b_r3", "safety_validate_case"],
            "use_cases": ["E2B case intake", "adverse event reporting"]
        }
    }

    # Return relevant contexts
    return filter_contexts(available_contexts, resource_type, use_case)

# Dynamic context activation
@mcp.tool()
def vault_activate_context(context_name: str) -> dict:
    """
    Activate a specialized context to load additional tools.

    Args:
        context_name: Name of context (clinical_operations, safety, admin, etc.)

    Returns:
        List of newly available tools
    """
    # Dynamically register context-specific tools
    context_tools = load_context_tools(context_name)
    register_tools(context_tools)

    return {
        "context": context_name,
        "tools_loaded": len(context_tools),
        "available_tools": [t.name for t in context_tools]
    }
```

### Dynamic Tool Loading

```python
# Example: Clinical Operations context tools loaded dynamically
def load_clinical_context():
    @mcp.tool(context="clinical")
    def clinical_create_etmf_binder(
        study_id: str,
        country: str,
        tmf_section: str
    ) -> dict:
        """Create an eTMF binder for clinical trials."""
        service = get_clinical_operations_service()
        return service.create_etmf_binder(study_id, country, tmf_section)

    @mcp.tool(context="clinical")
    def clinical_track_milestone(
        study_id: str,
        milestone_type: str,
        status: str,
        completion_date: str = None
    ) -> dict:
        """Track clinical study milestones."""
        service = get_clinical_operations_service()
        return service.track_milestone(study_id, milestone_type, status, completion_date)
```

### Pros
✅ **Best of Both Worlds**: Simple core + specialized power when needed
✅ **Optimized LLM Performance**: Only expose tools relevant to current task
✅ **Scalable**: Can add unlimited specialized contexts without overwhelming LLM
✅ **Intelligent Contextualization**: LLM learns to activate appropriate contexts
✅ **Reduced Token Usage**: Smaller active tool set at any given time
✅ **Future-Proof**: Easy to add new specialized domains
✅ **Discovery Mechanism**: LLMs can explore available capabilities

### Cons
❌ **Highest Complexity**: Requires dynamic tool registration and context management
❌ **State Management**: Must track active contexts per session
❌ **Learning Curve**: LLMs need to learn when to activate contexts
❌ **Potential Confusion**: Tool availability changes during conversation
❌ **Testing Complexity**: Must test all context combinations
❌ **MCP Specification Limits**: May require custom protocol extensions
❌ **Documentation Challenge**: Need to document both core and context tools

### Implementation Complexity
**High**: Requires sophisticated context management, dynamic registration, and careful UX design.

### Best For
- Advanced users who work across multiple Vault domains
- Large enterprises with diverse use cases
- Scenarios where different teams have very different needs
- Future-proofing for extensive API growth

---

## Comparative Analysis

| Criteria | Variation 1: Flat Tools | Variation 2: Service-Grouped | Variation 3: Resource-Oriented | Variation 4: Hybrid Dynamic |
|----------|-------------------------|------------------------------|-------------------------------|----------------------------|
| **Tool Count** | 30-40 | 80-120 | 50-70 | 30 core + dynamic |
| **LLM Usability** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐ Poor | ⭐⭐⭐⭐ Very Good | ⭐⭐⭐⭐ Very Good |
| **API Coverage** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Complete | ⭐⭐⭐⭐ Very Good | ⭐⭐⭐⭐⭐ Complete |
| **Maintainability** | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐ Good | ⭐⭐ Complex |
| **Implementation Effort** | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ Low | ⭐⭐⭐ Medium | ⭐ High |
| **MCP Best Practices** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐ Violates | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Very Good |
| **Extensibility** | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ Easy | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| **Developer Experience** | ⭐⭐⭐ Medium | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Medium |
| **Production Ready** | ⭐⭐⭐⭐ Good | ⭐⭐ Poor | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Medium |
| **Documentation Clarity** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Medium |
| **Specialized Use Cases** | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ Full Support | ⭐⭐⭐⭐ Very Good | ⭐⭐⭐⭐⭐ Full Support |

---

## Final Recommendation: Variation 3 - Resource-Oriented Approach

### Rationale

After comprehensive analysis, **Variation 3: Resource-Oriented Approach** is the recommended architecture for the following reasons:

#### 1. **Optimal Balance**
- **Tool Count (50-70)**: Sweet spot between Variation 1's minimalism and Variation 2's over-tooling
- Manageable for LLMs while providing comprehensive coverage
- Follows MCP best practice of avoiding over-tooling while maintaining granularity

#### 2. **Conceptual Clarity**
- Resources (Documents, Objects, Binders, Users) are **natural conceptual units** that both humans and LLMs understand intuitively
- RESTful CRUD pattern is **universally recognized** and well-documented
- Predictable naming: `resource_action` (e.g., `documents_query`, `objects_create`)

#### 3. **MCP Protocol Alignment**
- **Native MCP Resource Support**: Vault resources map directly to MCP Resources
- Enables browsing: `vault://documents/DOC-12345`, `vault://objects/product__c/REC-001`
- LLMs can read resources AND invoke tools on them

#### 4. **Production Readiness**
- ⭐⭐⭐⭐⭐ **Excellent production readiness score**
- Clear documentation path for each resource type
- Consistent error handling across resource operations
- Easy to monitor and debug (grouped by resource)

#### 5. **Extensibility**
- Adding new Vault resources (new object types, new applications) follows the same pattern
- Each resource is independent and can be extended without affecting others
- Natural fit for future Vault API additions

#### 6. **Developer Experience**
- Developers familiar with REST APIs immediately understand the structure
- Clear separation of concerns (each resource has its own module)
- Easy to test (test each resource independently)

#### 7. **Real-World Use Cases**
Most Vault workflows are resource-centric:
- "Find all clinical trial documents for Study XYZ"
- "Create a new product record"
- "Update the lifecycle state of this binder"
- "Query all safety cases from last month"

Variation 3's resource-oriented tools map naturally to these intents.

### Implementation Roadmap

#### Phase 1: Core Infrastructure (Week 1-2)
```
✓ MCP server initialization
✓ Authentication tools (vault_auth, vault_logout)
✓ VaultClient session management
✓ Error handling and logging infrastructure
✓ Base tool decorator system
```

#### Phase 2: Primary Resources (Week 3-5)
```
✓ Documents resource (12 tools)
  - documents_query, documents_get, documents_create, documents_update,
    documents_delete, documents_upload_content, documents_download_content,
    documents_lock, documents_unlock, documents_manage_lifecycle,
    documents_get_versions, documents_get_metadata

✓ Objects resource (8 tools)
  - objects_query, objects_get, objects_create, objects_update,
    objects_delete, objects_bulk_upsert, objects_get_metadata,
    objects_manage_attachments

✓ VQL resource (3 tools)
  - vql_execute, vql_bulk_export, vql_validate
```

#### Phase 3: Secondary Resources (Week 6-7)
```
✓ Binders resource (8 tools)
✓ Users resource (6 tools)
✓ Workflows resource (5 tools)
✓ Metadata resource (5 tools)
```

#### Phase 4: Specialized Resources (Week 8-9)
```
✓ Clinical Operations (10 tools)
✓ Safety (7 tools)
✓ File Staging (6 tools)
✓ Groups & Picklists (6 tools)
```

#### Phase 5: MCP Resources & Polish (Week 10)
```
✓ Implement MCP resource URIs
✓ Resource browsing/listing
✓ Comprehensive documentation
✓ Integration tests
✓ Performance optimization
```

### Technical Architecture

```
veeva-vault-mcp/
├── server.py                    # MCP server entry point
├── config.py                    # Configuration management
├── auth/
│   ├── __init__.py
│   └── tools.py                 # vault_auth, vault_logout
├── resources/
│   ├── __init__.py
│   ├── base.py                  # Base resource tool class
│   ├── documents.py             # Documents resource tools
│   ├── objects.py               # Objects resource tools
│   ├── binders.py               # Binders resource tools
│   ├── users.py                 # Users resource tools
│   ├── workflows.py             # Workflows resource tools
│   ├── vql.py                   # VQL resource tools
│   ├── metadata.py              # Metadata resource tools
│   └── specialized/
│       ├── clinical_operations.py
│       ├── safety.py
│       ├── file_staging.py
│       └── groups.py
├── mcp_resources/
│   ├── __init__.py
│   └── vault_resources.py      # MCP resource URIs
├── utils/
│   ├── __init__.py
│   ├── query_builder.py        # VQL query construction helpers
│   ├── formatting.py           # Response formatting
│   └── validation.py           # Input validation
├── tests/
│   ├── test_documents.py
│   ├── test_objects.py
│   └── ...
├── pyproject.toml
├── Dockerfile
└── README.md
```

### Example Tool Implementation

```python
# resources/documents.py

from typing import Optional, Dict, Any, List
from veevavault import VaultClient
from veevavault.services.documents import DocumentService
from ..utils.query_builder import build_document_vql
from ..utils.formatting import format_document_response
import logging

logger = logging.getLogger(__name__)


class DocumentsResource:
    """Documents resource tools for MCP server."""

    def __init__(self, vault_client: VaultClient):
        self.client = vault_client
        self.service = DocumentService(vault_client)

    def query(
        self,
        vql: Optional[str] = None,
        name_contains: Optional[str] = None,
        document_type: Optional[str] = None,
        lifecycle_state: Optional[str] = None,
        created_by: Optional[str] = None,
        created_after: Optional[str] = None,
        modified_after: Optional[str] = None,
        limit: int = 100,
        return_format: str = "summary"
    ) -> Dict[str, Any]:
        """
        Query documents in Vault.

        Tool Name: documents_query
        """
        try:
            # Build VQL if not provided
            if not vql:
                vql = build_document_vql(
                    name_contains=name_contains,
                    document_type=document_type,
                    lifecycle_state=lifecycle_state,
                    created_by=created_by,
                    created_after=created_after,
                    modified_after=modified_after,
                    limit=limit
                )

            logger.info(f"Executing document query: {vql[:100]}...")

            # Execute via query service
            from veevavault.services.queries import QueryService
            query_service = QueryService(self.client)
            results = query_service.query(vql)

            # Format response
            return format_document_response(results, return_format)

        except Exception as e:
            logger.error(f"Document query failed: {str(e)}")
            raise

    def get(
        self,
        document_id: str,
        version: str = "latest",
        include_renditions: bool = False,
        include_relationships: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieve a single document by ID.

        Tool Name: documents_get
        """
        try:
            logger.info(f"Retrieving document {document_id} version {version}")

            result = self.service.retrieval.retrieve_single_document(
                document_id=document_id,
                version=version
            )

            # Optionally include additional data
            if include_renditions:
                renditions = self.service.renditions.retrieve_document_renditions(document_id)
                result["renditions"] = renditions

            if include_relationships:
                relationships = self.service.relationships.retrieve_document_relationships(document_id)
                result["relationships"] = relationships

            return result

        except Exception as e:
            logger.error(f"Failed to retrieve document {document_id}: {str(e)}")
            raise

    # ... additional methods for create, update, delete, etc.
```

### Security Considerations

1. **Authentication**
   - OAuth2 with Resource Indicators (RFC 8707)
   - Session management with automatic refresh
   - Secure credential storage (environment variables, secrets manager)

2. **Authorization**
   - Explicit user consent for all tool invocations (MCP requirement)
   - Respect Vault permission model
   - Audit logging for all operations

3. **Data Privacy**
   - No credential logging
   - Sanitize responses to remove sensitive data
   - Support for field-level security rules

4. **Rate Limiting**
   - Implement client-side rate limiting
   - Respect Vault API rate limits
   - Backoff and retry logic

### Deployment

**Containerized Deployment (Recommended)**

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install poetry && poetry install --no-dev

COPY . .

ENV VAULT_URL=""
ENV VAULT_USERNAME=""
ENV VAULT_PASSWORD=""

CMD ["python", "-m", "veeva_vault_mcp.server"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  veeva-vault-mcp:
    build: .
    environment:
      - VAULT_URL=${VAULT_URL}
      - VAULT_USERNAME=${VAULT_USERNAME}
      - VAULT_PASSWORD=${VAULT_PASSWORD}
      - LOG_LEVEL=INFO
    ports:
      - "3000:3000"
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

---

## Alternative Recommendation: Variation 1 for Simplicity

If **implementation speed and LLM usability** are the absolute highest priorities, **Variation 1: Flat High-Level Tool Approach** is a strong alternative:

### When to Choose Variation 1
- ✅ Need to launch quickly (2-3 weeks vs 8-10 weeks)
- ✅ Prioritize LLM token efficiency above all
- ✅ Target general-purpose use cases only
- ✅ Small team with limited resources
- ✅ Willing to sacrifice some API coverage for simplicity

### When Variation 1 Falls Short
- ❌ Need comprehensive API coverage
- ❌ Users require specialized endpoints (clinical, safety, etc.)
- ❌ Plan to expose Vault content as browsable resources
- ❌ Expect significant future API expansion

---

## Conclusion

**Variation 3: Resource-Oriented Approach** represents the optimal balance of:
- ⭐ MCP best practices adherence
- ⭐ LLM usability and performance
- ⭐ Comprehensive API coverage
- ⭐ Production readiness
- ⭐ Long-term maintainability
- ⭐ Developer experience

This architecture provides a **solid foundation** for enabling LLMs to interact naturally with Veeva Vault while remaining **extensible, maintainable, and aligned with industry best practices**.

### Next Steps

1. **Approve Architecture**: Review and approve Variation 3 design
2. **Environment Setup**: Configure development environment, MCP SDK
3. **Implement Phase 1**: Core infrastructure and authentication
4. **Iterate Through Phases 2-5**: Build resources incrementally
5. **Testing & Documentation**: Comprehensive tests and user guides
6. **Deployment**: Containerized production deployment

---

**Document Version**: 1.0
**Date**: 2025-11-06
**Author**: Claude Code Architecture Team
**Status**: Ready for Review
