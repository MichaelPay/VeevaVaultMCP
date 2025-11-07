# VeevaVault MCP Tools Reference

Complete reference for all 58 tools available in the VeevaVault MCP Server.

## Quick Navigation

- [Document Tools](#document-tools) (20 tools)
- [Object Tools](#object-tools) (8 tools)
- [Workflow Tools](#workflow-tools) (3 tools)
- [Task Tools](#task-tools) (3 tools)
- [VQL Tools](#vql-tools) (2 tools)
- [User Management](#user-management) (4 tools)
- [Group Management](#group-management) (5 tools)
- [Metadata Tools](#metadata-tools) (3 tools)
- [Audit Trail](#audit-trail) (3 tools)
- [File Staging](#file-staging) (4 tools)

---

## Document Tools

Comprehensive document lifecycle management in Veeva Vault.

### vault_documents_query
**Query and search documents using VQL or filters.**

Use for:
- Finding documents by name, type, or status
- Discovering documents matching criteria
- Building document lists

Parameters:
- `vql` (string, optional): Raw VQL query
- `name_contains` (string, optional): Partial name match
- `document_type` (string, optional): Document type (e.g., 'protocol__c')
- `lifecycle_state` (string, optional): State (e.g., 'draft__c', 'approved__c')
- `status` (string, optional): Document status
- `limit` (integer, default 100): Results per page
- `auto_paginate` (boolean, default false): Fetch all pages ⚠️ May return thousands

Example:
```
"Find all clinical study reports in approved state"
"Show me protocol documents for Study ABC-123"
```

### vault_documents_get
**Get complete details for a specific document by ID.**

Returns document metadata, lifecycle state, version, and all custom fields.

Parameters:
- `document_id` (integer, required): Document ID
- `major_version` (integer, optional): Major version number
- `minor_version` (integer, optional): Minor version number

Example:
```
"Get details for document 12345"
"Show me version 2.0 of document 12345"
```

### vault_documents_create
**Create a new document in Veeva Vault.**

Parameters:
- `name` (string, required): Document name (unique identifier)
- `type` (string, required): Document type
- `lifecycle` (string, required): Lifecycle to use
- `title` (string, required): Document title
- `subtype` (string, optional): Document subtype
- `classification` (string, optional): Classification
- `product` (string, optional): Product name or ID
- `study` (string, optional): Study number or ID

Example:
```
"Create a new protocol document titled 'Phase 3 Safety Study' for Product X"
```

### vault_documents_update
**Update metadata for an existing document.**

Can update title, description, product, study, classification, and custom fields. Document must be in an editable state.

Parameters:
- `document_id` (integer, required): Document to update
- `title` (string, optional): New title
- `description` (string, optional): New description
- `product` (string, optional): Product name/ID
- `study` (string, optional): Study number/ID
- `classification` (string, optional): New classification

Example:
```
"Update document 12345 to set therapeutic area to Oncology"
```

### vault_documents_delete
**Permanently delete a document from Vault.**

⚠️ WARNING: This permanently deletes the document! Document must be in a state that allows deletion.

Parameters:
- `document_id` (integer, required): Document to delete

### vault_documents_lock
**Lock a document for editing.**

Prevents other users from editing while you work on it. Must unlock when done or document remains locked to you.

Parameters:
- `document_id` (integer, required): Document to lock

### vault_documents_unlock
**Unlock a document after editing.**

Allows other users to edit the document again.

Parameters:
- `document_id` (integer, required): Document to unlock

### vault_documents_download_file
**Download the source file from a document.**

Returns file metadata and download information for the latest version.

Parameters:
- `document_id` (integer, required): Document ID
- `save_path` (string, optional): Local path to save file

Example:
```
"Download the file for document 12345"
```

### vault_documents_download_version_file
**Download file from a specific document version.**

Useful for accessing historical versions of documents.

Parameters:
- `document_id` (integer, required): Document ID
- `major_version` (integer, required): Major version
- `minor_version` (integer, required): Minor version

### vault_documents_batch_create
**Create multiple documents in a single operation.**

Batch creation is 10-100x faster than creating documents individually. Supports partial success.

Parameters:
- `documents` (array, required): Array of document objects with name, type, lifecycle, title

Example:
```
"Create 50 training documents from this CSV file"
```

### vault_documents_batch_update
**Update multiple documents in a single operation.**

Batch updates are 10-100x faster than individual updates. Supports partial success.

Parameters:
- `updates` (array, required): Array of updates with id and fields to change

### vault_documents_get_actions
**Get available workflow/lifecycle actions for a document.**

Returns list of actions that can be performed: workflow state changes, lifecycle transitions, user actions (Approve, Reject, etc.).

Parameters:
- `document_id` (integer, required): Document ID

Example:
```
"What actions can I take on document 12345?"
```

### vault_documents_execute_action
**Execute a workflow/lifecycle action on a document.**

Common actions: Change state (Draft → Review → Approved), Assign reviewers, Add signatures, Update workflow.

Parameters:
- `document_id` (integer, required): Document ID
- `action_name` (string, required): Action from get_actions
- `action_data` (object, optional): Action parameters

Example:
```
"Approve document 12345 with comment 'Looks good'"
```

### vault_documents_upload_file
**Create a document with file upload.**

For large files (>50MB), use file staging first.

Parameters:
- `name` (string, required): Document name
- `type` (string, required): Document type
- `lifecycle` (string, required): Lifecycle
- `title` (string, required): Title
- `file_path` (string, optional): Local file path
- `staging_path` (string, optional): Staging area path
- `metadata` (object, optional): Additional fields

### vault_documents_create_version
**Create a new version of an existing document.**

Critical for compliance workflows - maintains document history.

Parameters:
- `document_id` (integer, required): Document ID
- `staging_path` (string, optional): New version file
- `metadata` (object, optional): Version-specific updates

Example:
```
"Create version 2.0 of document 12345 with updated content"
```

### vault_documents_attachments_list
**List all attachments for a document.**

Returns attachment metadata including file names, sizes, and IDs.

Parameters:
- `document_id` (integer, required): Document ID

### vault_documents_attachments_upload
**Upload an attachment file to a document.**

For large files (>50MB), upload to staging first and provide staging_path.

Parameters:
- `document_id` (integer, required): Document ID
- `staging_path` (string, optional): Staged file path
- `description` (string, optional): Attachment description

### vault_documents_attachments_download
**Download a specific attachment from a document.**

Parameters:
- `document_id` (integer, required): Document ID
- `attachment_id` (string, required): Attachment ID

### vault_documents_attachments_delete
**Delete a specific attachment from a document.**

⚠️ This operation cannot be undone.

Parameters:
- `document_id` (integer, required): Document ID
- `attachment_id` (string, required): Attachment ID to delete

### vault_documents_renditions_list
**List all renditions (alternative formats) for a document.**

Renditions include PDF versions, viewable formats, thumbnails.

Parameters:
- `document_id` (integer, required): Document ID
- `doc_version` (string, optional): Specific version (e.g., '1.0')

### vault_documents_renditions_generate
**Generate a specific rendition type for a document.**

Common types: pdf, thumbnail, viewable. Generation is asynchronous.

Parameters:
- `document_id` (integer, required): Document ID
- `rendition_type` (string, required): 'pdf', 'thumbnail', or 'viewable'
- `doc_version` (string, optional): Specific version

### vault_documents_renditions_download
**Download a specific rendition file.**

Parameters:
- `document_id` (integer, required): Document ID
- `rendition_type` (string, required): Rendition type
- `doc_version` (string, optional): Specific version

### vault_documents_renditions_delete
**Delete a specific rendition.**

Renditions can be regenerated if needed.

Parameters:
- `document_id` (integer, required): Document ID
- `rendition_type` (string, required): Rendition to delete
- `doc_version` (string, optional): Specific version

---

## Object Tools

CRUD operations on custom Vault objects (products, studies, quality events, sites, etc.).

### vault_objects_query
**Query Vault object records using VQL.**

Objects are custom records like products, studies, quality events, sites.

Parameters:
- `object_name` (string, required): Object API name (e.g., 'product__v', 'quality_event__c')
- `vql` (string, optional): Raw VQL query
- `fields` (array, optional): Fields to return (default: id, name__v)
- `where` (string, optional): WHERE clause without 'WHERE' keyword
- `limit` (integer, default 100): Results per page
- `auto_paginate` (boolean, default false): Fetch all pages ⚠️

Example:
```
"Query all active products"
"Find quality events created in the last 30 days"
```

### vault_objects_get
**Get detailed information about a specific object record.**

Parameters:
- `object_name` (string, required): Object type
- `object_id` (integer, required): Record ID

Example:
```
"Get details for product 12345"
```

### vault_objects_create
**Create a new object record.**

Parameters:
- `object_name` (string, required): Object type
- `data` (object, required): Field values to set

Example:
```
"Create a new quality event for batch LOT-456"
```

### vault_objects_update
**Update an existing object record.**

Parameters:
- `object_name` (string, required): Object type
- `object_id` (integer, required): Record ID
- `data` (object, required): Fields to update

### vault_objects_batch_create
**Create multiple object records in one operation.**

10-100x faster than individual creates. Supports partial success.

Parameters:
- `object_name` (string, required): Object type
- `records` (array, required): Array of record data

### vault_objects_batch_update
**Update multiple object records in one operation.**

10-100x faster than individual updates. Supports partial success.

Parameters:
- `object_name` (string, required): Object type
- `updates` (array, required): Array of updates with id and fields

### vault_objects_get_actions
**Get available workflow actions for an object record.**

Parameters:
- `object_name` (string, required): Object type
- `object_id` (integer, required): Record ID

### vault_objects_execute_action
**Execute a workflow action on an object record.**

Parameters:
- `object_name` (string, required): Object type
- `object_id` (integer, required): Record ID
- `action_name` (string, required): Action to execute
- `action_data` (object, optional): Action parameters

---

## Workflow Tools

Manage document and object lifecycle workflows.

### vault_workflows_list
**List all workflows available in the vault.**

Returns workflow IDs, names, types, and status. Common workflows include Document Review & Approval, Change Control, Training Assignment.

Parameters:
- `workflow_type` (string, optional): Filter by 'atomic' or 'standard'
- `active_only` (boolean, default true): Only return active workflows

Example:
```
"Show me all active workflows"
```

### vault_workflows_get
**Get detailed workflow information.**

Returns workflow states, transitions, available actions, role assignments, and configuration.

Parameters:
- `workflow_id` (string, required): Workflow ID (e.g., 'doc_workflow__c')

Example:
```
"Get details for document review workflow to see all possible states"
```

### vault_documents_get_workflow_details
**Get current workflow state and available actions for a document.**

Returns current state, available actions, task assignments, and workflow history.

Parameters:
- `document_id` (integer, required): Document ID

Example:
```
"Check if document 12345 can be approved"
"Show me workflow details for document 12345 to see what verdict options are available"
```

---

## Task Tools

Manage user tasks and workflow completions.

### vault_tasks_list
**List tasks assigned to the current user.**

Returns all workflow tasks in the user's queue.

Parameters:
- `status` (string, optional): Filter by status: 'open', 'completed', 'all' (default: 'open')
- `limit` (integer, default 100): Results per page

Example:
```
"Show me all my pending tasks"
"List completed tasks from this week"
```

### vault_tasks_get
**Get detailed task information.**

Returns task type, description, related document/object, due date, assigned users, available actions, and instructions.

Parameters:
- `task_id` (string, required): Task ID

Example:
```
"Get details for task T-12345 to see what verdict options are available"
```

### vault_tasks_execute_action
**Execute an action on a workflow task.**

Common actions: complete (mark done), reassign (assign to another user), cancel, delegate.

Parameters:
- `task_id` (string, required): Task ID
- `action` (string, required): Action to execute
- `verdict` (string, optional): Verdict for completion (approve/reject)
- `comment` (string, optional): Comment text
- `assignee_id` (integer, optional): User ID for reassign/delegate

Examples:
```
"Complete review task T-12345 with approval and comment 'Looks good'"
"Reassign task T-12345 to user 67890"
"Cancel task T-12345 with comment 'No longer needed'"
```

---

## VQL Tools

Execute Vault Query Language queries for advanced data retrieval.

### vault_vql_execute
**Execute a VQL (Vault Query Language) query.**

VQL is SQL-like query language for Vault data. Power user feature for complex queries.

Parameters:
- `query` (string, required): VQL query to execute
- `limit` (integer, optional): Override LIMIT in query
- `auto_paginate` (boolean, default false): Fetch all pages ⚠️
- `describe_query` (boolean, default false): Include query metadata
- `record_properties` (boolean, default false): Include field metadata
- `enable_facets` (boolean, default false): Enable faceted search

Examples:
```
"Execute: SELECT id, name__v FROM documents WHERE type__v = 'protocol__c'"
"SELECT id, title__v FROM documents WHERE created_date__v >= '2025-01-01'"
"SELECT id, name__v, status__v FROM product__v WHERE active__v = true"
```

### vault_vql_validate
**Validate a VQL query without executing it.**

Checks query syntax and returns validation results.

Parameters:
- `query` (string, required): VQL query to validate

---

## User Management

Manage Vault users and user accounts.

### vault_users_list
**List users in Veeva Vault with filtering.**

Parameters:
- `status` (string, default 'active'): Filter by 'active', 'inactive', or 'all'
- `limit` (integer, default 100): Maximum users to return
- `offset` (integer, default 0): Pagination offset

Example:
```
"List all active users"
"Find users by security profile"
```

### vault_users_get
**Get detailed information about a specific user.**

Parameters:
- `user_id` (integer, required): User ID

### vault_users_create
**Create a new user account.**

Parameters:
- `username` (string, required): Username/email
- `security_profile` (string, required): Security profile ID
- `first_name` (string, required): First name
- `last_name` (string, required): Last name
- Additional user fields as needed

### vault_users_update
**Update an existing user account.**

Parameters:
- `user_id` (integer, required): User ID
- User fields to update

---

## Group Management

Manage user groups and group memberships.

### vault_groups_list
**List all groups in the vault.**

Parameters:
- `limit` (integer, default 100): Maximum groups to return

### vault_groups_get
**Get detailed information about a specific group.**

Parameters:
- `group_id` (integer, required): Group ID

### vault_groups_create
**Create a new group.**

Parameters:
- `name` (string, required): Group name
- `description` (string, optional): Group description

### vault_groups_add_members
**Add users to a group.**

Parameters:
- `group_id` (integer, required): Group ID
- `user_ids` (array, required): Array of user IDs to add

### vault_groups_remove_members
**Remove users from a group.**

Parameters:
- `group_id` (integer, required): Group ID
- `user_ids` (array, required): Array of user IDs to remove

---

## Metadata Tools

Retrieve Vault configuration and metadata.

### vault_metadata_get
**Get metadata configuration for Vault objects.**

Retrieves object schemas, field definitions, and picklists.

Parameters:
- `object_type` (string, required): Object type (e.g., 'documents', 'product__v')

Example:
```
"Get document metadata schema"
"Show me all fields for quality_event__c object"
```

### vault_metadata_list_objects
**List all object types available in Vault.**

Returns all standard and custom object types.

### vault_metadata_get_picklist_values
**Get picklist values for a field.**

Parameters:
- `object_type` (string, required): Object type
- `field_name` (string, required): Field name

Example:
```
"Get picklist values for document classification field"
```

---

## Audit Trail

Compliance and audit trail reporting.

### vault_audit_trail_query
**Query audit trail logs.**

Returns audit records for compliance and investigation.

Parameters:
- `start_date` (string, required): Start date (YYYY-MM-DD)
- `end_date` (string, optional): End date
- `user_id` (integer, optional): Filter by user
- `limit` (integer, default 100): Results per page

Example:
```
"Show me all document deletions in the last 30 days"
```

### vault_audit_trail_document
**Get audit history for a specific document.**

Returns complete audit trail for a document.

Parameters:
- `document_id` (integer, required): Document ID

### vault_audit_trail_user_activity
**Get activity log for a specific user.**

Returns all actions performed by a user.

Parameters:
- `user_id` (integer, required): User ID
- `start_date` (string, required): Start date
- `end_date` (string, optional): End date

---

## File Staging

Manage file staging area for large file uploads/downloads.

### vault_file_staging_upload
**Upload a file to Vault's staging area.**

⚠️ **IMPLEMENTATION STATUS**: This tool is currently a placeholder and does not perform actual file uploads. Requires multipart/form-data implementation.

Parameters:
- `file_path` (string, required): Local file path
- `file_name` (string, optional): File name in staging

### vault_file_staging_list
**List files in Vault's staging area.**

Returns files waiting to be attached to documents.

Parameters:
- `folder` (string, optional): Staging folder path

### vault_file_staging_download
**Download a file from staging area.**

Parameters:
- `staging_path` (string, required): Path to file in staging

### vault_file_staging_delete
**Delete a file from staging area.**

Best practice: Delete staged files after attaching to documents.

Parameters:
- `staging_path` (string, required): Path to file in staging

---

## Common Workflow Patterns

### Document Approval Workflow
1. Query documents: `vault_documents_query` with appropriate filters
2. Get workflow details: `vault_documents_get_workflow_details`
3. Check available actions: `vault_documents_get_actions`
4. Execute approval: `vault_documents_execute_action`

### Task Completion Workflow
1. List tasks: `vault_tasks_list` (status: 'open')
2. Get task details: `vault_tasks_get`
3. Complete task: `vault_tasks_execute_action` (action: 'complete')

### Document Creation with File
1. (For large files) Upload to staging: `vault_file_staging_upload`
2. Create document: `vault_documents_upload_file` with staging_path
3. Execute workflow action if needed: `vault_documents_execute_action`

### Batch Data Operations
1. Query records: `vault_objects_query` or `vault_documents_query`
2. Prepare batch data
3. Execute batch operation: `vault_documents_batch_update` or `vault_objects_batch_update`
4. Review results for any failures

---

## Tool Naming Conventions

All tools follow the pattern: `vault_{resource}_{action}`

- **vault_** - Prefix for all Vault tools
- **{resource}** - Resource type (documents, objects, users, workflows, tasks, etc.)
- **{action}** - Action to perform (query, get, create, update, delete, list, execute, etc.)

Special cases:
- Batch operations: `vault_{resource}_batch_{action}`
- Nested resources: `vault_documents_attachments_{action}`
- Workflow-related: `vault_documents_get_workflow_details`

---

## Need Help?

- **Getting Started**: See [GETTING_STARTED.md](GETTING_STARTED.md)
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Configuration**: See [README.md](README.md#configuration)
- **API Documentation**: https://developer.veevavault.com/api/
