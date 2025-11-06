# User Stories: Vault Administrator

**Persona:** Tier 1 - High-Volume Daily User
**Frequency:** Multiple times per day (20-50 administrative operations daily)
**Primary Goals:** User provisioning, system configuration, troubleshooting, bulk operations, reporting

---

## Scenario 1: User Provisioning and Access Management

**Context:** New employees joining, need Vault access with appropriate permissions.

### User Story 1.1: Create New User Account
```
As a Vault Administrator
I want to create a new user account with appropriate security profile
So that new employees can access Vault with correct permissions
```

**Acceptance Criteria:**
- Creates user via SCIM 2.0 API
- Assigns security profile based on role
- Sets user metadata (department, location, manager)
- Sends welcome email with login instructions
- Triggers provisioning in identity management system

**MCP Tool Interaction:**
```
User: "Create Vault account for John Smith, QA Specialist, assign QA_User security profile"
LLM calls: users_create(
    username="john.smith@company.com",
    first_name="John",
    last_name="Smith",
    email="john.smith@company.com",
    security_profile="QA_User",
    department="Quality Assurance",
    active=true
)
```

### User Story 1.2: Bulk User Creation from CSV
```
As a Vault Administrator
I want to create multiple users from CSV file
So that I can efficiently onboard large groups (acquisitions, new sites)
```

**Acceptance Criteria:**
- Parses CSV with user details
- Validates data before creating accounts
- Creates all users with specified security profiles
- Reports success vs. failure for each user
- Sends batch welcome emails

**MCP Tool Interaction:**
```
User: "Create 50 new users from CSV file new_users.csv"
LLM calls: users_bulk_create(
    source_file="new_users.csv",
    default_security_profile="External_User",
    send_welcome_email=true,
    dry_run=false
)
```

---

## Scenario 2: Security Profile and Permission Management

**Context:** Managing security profiles and group memberships for access control.

### User Story 2.1: Review User Permissions
```
As a Vault Administrator
I want to see all permissions for a specific user
So that I can troubleshoot access issues
```

**Acceptance Criteria:**
- Shows user's security profile and all permission sets
- Lists all groups user belongs to
- Displays effective permissions (cumulative from all sources)
- Identifies permission conflicts or issues
- Shows object-level and record-level security

**MCP Tool Interaction:**
```
User: "Show me all permissions for user john.smith@company.com"
LLM calls:
  - users_get(username="john.smith@company.com", include_security_profile=true)
  - groups_get_user_memberships(username="john.smith@company.com")
  - users_get_effective_permissions(username="john.smith@company.com")
```

### User Story 2.2: Add User to Group
```
As a Vault Administrator
I want to add a user to a security group
So that they inherit group permissions
```

**Acceptance Criteria:**
- Can add user to one or multiple groups
- Validates user has appropriate security profile for group
- Updates permissions immediately (no delay)
- Records group membership change in audit log
- Notifies user if permissions significantly change

**MCP Tool Interaction:**
```
User: "Add john.smith to QA_Reviewers group"
LLM calls: groups_add_members(
    group_id="QA_Reviewers",
    members=["john.smith@company.com"],
    notify_members=true
)
```

---

## Scenario 3: Metadata Configuration

**Context:** Configuring custom fields, picklists, and object schemas.

### User Story 3.1: Create Custom Object Field
```
As a Vault Administrator
I want to add a custom field to an object
So that users can capture additional data
```

**Acceptance Criteria:**
- Specifies field name, label, type (text, number, picklist, date, etc.)
- Sets field properties (required, editable, facetable, searchable)
- Defines validation rules if applicable
- Updates page layouts to display field
- Validates no naming conflicts

**MCP Tool Interaction:**
```
User: "Add custom field 'Risk Level' picklist to quality_event__c object"
LLM calls: metadata_create_field(
    object="quality_event__c",
    field_name="risk_level__c",
    field_type="picklist",
    picklist_name="risk_levels__c",
    required=true,
    label="Risk Level"
)
```

### User Story 3.2: Update Picklist Values
```
As a Vault Administrator
I want to add or update values in a picklist
So that users have current options for selection
```

**Acceptance Criteria:**
- Can add new picklist values
- Can update labels for existing values
- Can inactivate (not delete) obsolete values
- Validates no duplicate values
- Records all changes in metadata audit log

**MCP Tool Interaction:**
```
User: "Add 'High' and 'Critical' values to risk_levels__c picklist"
LLM calls: picklists_create_values(
    picklist_name="risk_levels__c",
    values=[
        {name: "high__c", label: "High"},
        {name: "critical__c", label: "Critical"}
    ]
)
```

---

## Scenario 4: User Support and Troubleshooting

**Context:** User reports issue accessing documents or performing operation.

### User Story 4.1: Diagnose User Access Issue
```
As a Vault Administrator
I want to determine why a user cannot access a specific document
So that I can resolve the access issue
```

**Acceptance Criteria:**
- Retrieves document security settings
- Checks user's permissions for that document type
- Identifies if document lifecycle state restricts access
- Checks role-based access on the document
- Provides specific reason for access denial

**MCP Tool Interaction:**
```
User: "Why can't mary.jones access document DOC-12345?"
LLM calls:
  - documents_get(document_id="DOC-12345", include_security=true)
  - users_get_effective_permissions(username="mary.jones@company.com")
  - documents_check_user_access(document_id="DOC-12345", username="mary.jones@company.com")
```

### User Story 4.2: Query User Activity for Investigation
```
As a Vault Administrator
I want to see recent activity for a user
So that I can investigate reported issues or suspicious behavior
```

**Acceptance Criteria:**
- Lists user's recent logins and session times
- Shows documents accessed, created, modified
- Displays workflow actions and approvals
- Includes failed login attempts
- Can filter by date range and activity type

**MCP Tool Interaction:**
```
User: "Show me all activity for john.smith in last 7 days"
LLM calls: audit_trail_query(
    username="john.smith@company.com",
    start_date="2025-10-30",
    end_date="2025-11-06",
    include_logins=true,
    include_document_access=true
)
```

---

## Scenario 5: Bulk Data Operations

**Context:** Need to update large datasets or migrate content.

### User Story 5.1: Bulk Update Document Metadata
```
As a Vault Administrator
I want to update a field for thousands of documents
So that I can correct data quality issues efficiently
```

**Acceptance Criteria:**
- Can query documents to update via VQL
- Validates update before applying to all records
- Shows preview of changes
- Performs update in batches (API rate limiting)
- Reports success count and any failures

**MCP Tool Interaction:**
```
User: "Update therapeutic_area to 'Oncology' for all documents in Study ABC-123"
LLM calls:
  - vql_execute("SELECT id FROM documents WHERE study_number__c='ABC-123'")
  - documents_bulk_update(document_ids=[...], fields={"therapeutic_area__c": "Oncology"})
```

### User Story 5.2: Extract Data via Vault Loader
```
As a Vault Administrator
I want to extract object data with all fields and attachments
So that I can analyze data externally or migrate to another system
```

**Acceptance Criteria:**
- Extracts specified objects with all fields
- Includes related records (e.g., object with child records)
- Optionally includes attachments and renditions
- Exports to CSV format with proper encoding
- Provides download link when extraction completes

**MCP Tool Interaction:**
```
User: "Extract all deviation__c records from 2025 with attachments"
LLM calls: vault_loader_extract(
    objects=["deviation__c"],
    filter="YEAR(created_date__c)=2025",
    include_attachments=true,
    include_related=["capa__c"],
    email_notification=true
)
```

---

## Scenario 6: System Monitoring and Health Checks

**Context:** Proactive monitoring of Vault health and performance.

### User Story 6.1: Monitor API Usage
```
As a Vault Administrator
I want to see API usage statistics
So that I can identify integrations approaching rate limits
```

**Acceptance Criteria:**
- Shows API calls per hour/day by user or integration
- Highlights usage approaching daily or burst limits
- Identifies slowest or failing API calls
- Tracks API version usage (identify deprecated versions)
- Exports usage report for capacity planning

**MCP Tool Interaction:**
```
User: "Show me API usage for last 24 hours"
LLM calls: system_get_api_usage(
    time_period="last_24_hours",
    group_by="user",
    include_integration_points=true
)
```

### User Story 6.2: Check Background Job Status
```
As a Vault Administrator
I want to monitor status of background jobs
So that I can ensure bulk operations complete successfully
```

**Acceptance Criteria:**
- Lists all running and recent background jobs
- Shows job type (Vault Loader, bulk operations, scheduled exports)
- Displays progress percentage for running jobs
- Shows completion status and error logs for failed jobs
- Can cancel or retry failed jobs

**MCP Tool Interaction:**
```
User: "Show me status of all running Vault Loader jobs"
LLM calls: system_get_background_jobs(
    job_type="vault_loader",
    status=["running", "queued"],
    include_progress=true
)
```

---

## Scenario 7: Lifecycle and Workflow Configuration

**Context:** Configuring document/object lifecycles and workflows.

### User Story 7.1: View Lifecycle Configuration
```
As a Vault Administrator
I want to see all states and transitions for a lifecycle
So that I can understand or document workflow for users
```

**Acceptance Criteria:**
- Lists all lifecycle states with labels
- Shows allowed state transitions
- Displays entry actions, user actions, and automatic actions per state
- Identifies required fields per state
- Shows role requirements for state entry

**MCP Tool Interaction:**
```
User: "Show me lifecycle configuration for clinical_document_lifecycle__c"
LLM calls: metadata_get_lifecycle(
    lifecycle_name="clinical_document_lifecycle__c",
    include_states=true,
    include_transitions=true,
    include_actions=true
)
```

### User Story 7.2: Test Workflow Configuration
```
As a Vault Administrator
I want to test a workflow before deploying to production
So that I ensure it behaves as expected
```

**Acceptance Criteria:**
- Can run workflow in test mode
- Simulates workflow steps without committing
- Shows which users would be assigned tasks
- Displays notification emails that would be sent
- Validates all workflow steps are reachable

**MCP Tool Interaction:**
```
User: "Test workflow sop_approval_workflow__c with test document"
LLM calls: workflows_test(
    workflow_name="sop_approval_workflow__c",
    test_document_id="DOC-TEST-001",
    dry_run=true
)
```

---

## Scenario 8: Audit and Compliance Reporting

**Context:** Generating compliance reports for management or auditors.

### User Story 8.1: Generate User Access Report
```
As a Vault Administrator
I want to generate report of all user access rights
So that I can provide to auditors for access control review
```

**Acceptance Criteria:**
- Lists all active users with security profiles
- Shows group memberships for each user
- Indicates last login date (identify inactive accounts)
- Highlights users with admin or elevated permissions
- Exports to Excel for auditor review

**MCP Tool Interaction:**
```
User: "Generate user access report for all active users"
LLM calls: users_generate_access_report(
    include_inactive=false,
    include_groups=true,
    include_last_login=true,
    export_format="Excel"
)
```

### User Story 8.2: Part 11 Compliance Report
```
As a Vault Administrator
I want to generate 21 CFR Part 11 compliance report
So that I can demonstrate electronic signature compliance
```

**Acceptance Criteria:**
- Validates all electronic signature configurations
- Checks user authentication settings
- Verifies audit trail completeness
- Confirms record retention policies
- Identifies any compliance gaps

**MCP Tool Interaction:**
```
User: "Generate Part 11 compliance report for Q3 2025"
LLM calls: compliance_generate_part11_report(
    start_date="2025-07-01",
    end_date="2025-09-30",
    include_signature_verification=true,
    include_audit_trail_check=true
)
```

---

## Scenario 9: Data Migration and Vault Loader

**Context:** Loading data from external systems into Vault.

### User Story 9.1: Load Object Data from CSV
```
As a Vault Administrator
I want to load object records from CSV file
So that I can migrate data from legacy systems
```

**Acceptance Criteria:**
- Parses CSV with object field mappings
- Validates all data before loading
- Supports create and update operations
- Handles relationships between objects
- Reports detailed success/failure logs

**MCP Tool Interaction:**
```
User: "Load 1000 product records from products.csv"
LLM calls: vault_loader_load(
    object="product__c",
    source_file="products.csv",
    operation="create",
    migration_mode=false,
    email_notification=true
)
```

### User Story 9.2: Monitor Load Job Progress
```
As a Vault Administrator
I want to track progress of data load job in real-time
So that I can estimate completion time and catch errors early
```

**Acceptance Criteria:**
- Shows records processed vs. total
- Displays current processing rate (records/minute)
- Estimates time to completion
- Shows error count and previews failures
- Can download partial results before completion

**MCP Tool Interaction:**
```
User: "Show me progress of Vault Loader job JOB-12345"
LLM calls: vault_loader_get_job_status(
    job_id="JOB-12345",
    include_progress=true,
    include_errors=true
)
```

---

## Scenario 10: Sandbox and Validation Environment Management

**Context:** Managing sandbox environments for testing and validation.

### User Story 10.1: Refresh Sandbox from Production
```
As a Vault Administrator
I want to refresh sandbox with production data
So that testers have current data for validation
```

**Acceptance Criteria:**
- Copies production metadata to sandbox
- Optionally copies recent documents/records (last N days)
- Masks or removes sensitive data (PII, PHI)
- Resets sandbox user passwords
- Notifies team when sandbox refresh complete

**MCP Tool Interaction:**
```
User: "Refresh sandbox with last 90 days of production data"
LLM calls: sandbox_refresh(
    source="production",
    include_data_days=90,
    mask_sensitive_data=true,
    reset_passwords=true
)
```

### User Story 10.2: Deploy Configuration from Sandbox to Production
```
As a Vault Administrator
I want to deploy validated configuration changes from sandbox to production
So that I can safely release new features
```

**Acceptance Criteria:**
- Exports configuration package from sandbox
- Validates package before deployment
- Can preview changes before applying
- Deploys with rollback capability
- Records deployment in change log

**MCP Tool Interaction:**
```
User: "Deploy configuration package PKG-v2.1 from sandbox to production"
LLM calls: sandbox_deploy(
    package_id="PKG-v2.1",
    source_env="sandbox",
    target_env="production",
    validation_mode=true,
    allow_rollback=true
)
```

---

## Summary: Vault Administrator User Stories

**Total Scenarios:** 10
**Total User Stories:** 20

### Primary MCP Tools Required:
1. `users_create` / `users_bulk_create` - User provisioning (HIGH usage)
2. `users_get` / `users_get_effective_permissions` - Access troubleshooting (HIGH usage)
3. `groups_add_members` / `groups_remove_members` - Group management (HIGH usage)
4. `metadata_create_field` / `metadata_update` - Configuration (HIGH usage)
5. `picklists_create_values` / `picklists_update` - Picklist management (HIGH usage)
6. `vql_execute` - Data queries for analysis and troubleshooting (HIGH usage)
7. `vault_loader_extract` / `vault_loader_load` - Bulk data operations (HIGH usage)
8. `documents_bulk_update` / `objects_bulk_update` - Mass updates (MEDIUM usage)
9. `audit_trail_query` - Compliance and investigation (MEDIUM usage)
10. `system_get_api_usage` / `system_get_background_jobs` - Monitoring (MEDIUM usage)
11. `metadata_get_lifecycle` / `metadata_get_workflow` - Configuration review (MEDIUM usage)
12. `users_generate_access_report` - Compliance reporting (MEDIUM usage)
13. `sandbox_refresh` / `sandbox_deploy` - Environment management (LOW usage)

### Key Insights:
- Vault Admin needs **complete API access** across all services (values 80-120 tools)
- **Bulk operations** are critical (manage thousands of users, documents, records)
- **Troubleshooting** requires deep visibility into permissions, audit trails, system state
- **Metadata management** is frequent configuration task
- **VQL proficiency** essential for data analysis and cleanup
- **Monitoring and reporting** prevent issues and demonstrate compliance
- Values **service-grouped organization** for comprehensive access (prefers Variation 2 or Variation 3 with advanced mode)
