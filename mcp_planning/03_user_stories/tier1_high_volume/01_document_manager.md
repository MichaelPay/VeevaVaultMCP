# User Stories: Document Manager / Content Coordinator

**Persona:** Tier 1 - High-Volume Daily User
**Frequency:** Multiple times per day (10-50 document operations daily)
**Primary Goals:** Efficient document lifecycle management, quick search/retrieval, batch operations

---

## Scenario 1: Morning Document Review and Triage

**Context:** Start of workday, need to review pending documents and prioritize tasks.

### User Story 1.1: Check Pending Reviews
```
As a Document Manager
I want to quickly see all documents waiting for my review
So that I can prioritize my workload for the day
```

**Acceptance Criteria:**
- Query returns documents in "pending_review" state assigned to me
- Results show document name, type, submitter, and days pending
- Results are sorted by priority/age
- Can filter by document type or therapeutic area

**MCP Tool Interaction:**
```
User: "Show me all documents pending my review"
LLM calls: documents_query(lifecycle_state="pending_review__c", assigned_to="current_user", limit=50)
```

### User Story 1.2: Identify Overdue Documents
```
As a Document Manager
I want to identify documents overdue for lifecycle actions
So that I can prevent bottlenecks and maintain compliance timelines
```

**Acceptance Criteria:**
- Query identifies documents past due date for current lifecycle state
- Shows days overdue and responsible parties
- Highlights critical documents (regulatory submissions, quality records)
- Can export list for escalation to management

**MCP Tool Interaction:**
```
User: "Find all documents overdue for approval by more than 3 days"
LLM calls: documents_query(lifecycle_state="in_approval__c", modified_before="3_days_ago", return_format="full")
```

---

## Scenario 2: Bulk Document Upload from Clinical Trial

**Context:** Received 25 clinical documents from a CRO that need to be uploaded and properly classified.

### User Story 2.1: Batch Upload with Metadata
```
As a Document Manager
I want to upload multiple documents at once with consistent metadata
So that I can efficiently process batches from external partners
```

**Acceptance Criteria:**
- Can specify metadata template for batch (document type, lifecycle, classification, study)
- Upload supports common formats (PDF, Word, Excel)
- Each document can have unique fields (title, protocol number) while sharing common metadata
- Receive confirmation of successful uploads with document IDs

**MCP Tool Interaction:**
```
User: "Upload these 25 clinical documents as protocol documents for Study ABC-123 in draft state"
LLM calls:
  - For each file: documents_create(name=extracted, type="protocol__c", lifecycle="clinical_doc_lifecycle__c",
                                    state="draft__c", study_number__c="ABC-123", file_path=path)
```

### User Story 2.2: Link Related Documents
```
As a Document Manager
I want to establish relationships between uploaded documents
So that users can easily navigate between related content
```

**Acceptance Criteria:**
- Can link documents as "supporting documents", "supersedes", "related to"
- Relationships are bidirectional (visible from both documents)
- Can link during upload or after creation
- Can bulk-link multiple documents to a parent document

**MCP Tool Interaction:**
```
User: "Link these 5 appendix documents to the main protocol DOC-12345 as supporting documents"
LLM calls: documents_add_relationships(source_doc="DOC-12345", target_docs=[...], relationship_type="supporting_document__c")
```

---

## Scenario 3: Document Lifecycle Progression

**Context:** Documents approved by reviewers need to be moved to next lifecycle state.

### User Story 3.1: Single Document State Change
```
As a Document Manager
I want to move a document to the next lifecycle state
So that it progresses through the approval workflow
```

**Acceptance Criteria:**
- Can specify target lifecycle state
- Validates state transition is allowed per lifecycle rules
- Can add comments/notes for state change
- Electronic signature captured if required
- Notifies stakeholders of state change

**MCP Tool Interaction:**
```
User: "Move document DOC-12345 from draft to in review state"
LLM calls: documents_manage_lifecycle(document_id="DOC-12345", action="change_state", target_state="in_review__c")
```

### User Story 3.2: Bulk State Change for Approved Documents
```
As a Document Manager
I want to move multiple documents to approved state at once
So that I can efficiently process weekly approval board decisions
```

**Acceptance Criteria:**
- Can select multiple documents for batch state change
- All documents must allow the target state transition
- Single electronic signature for entire batch (where allowed)
- Receive summary of successful vs. failed operations
- Failed documents show reason for failure

**MCP Tool Interaction:**
```
User: "Approve these 15 documents that passed the review board"
LLM calls: documents_bulk_manage_lifecycle(document_ids=[...], action="change_state", target_state="approved__c")
```

---

## Scenario 4: Ad-Hoc Document Search for Colleagues

**Context:** Colleague asks for documents meeting specific criteria.

### User Story 4.1: Full-Text Search
```
As a Document Manager
I want to search document content using keywords
So that I can quickly find documents even when I don't know exact titles
```

**Acceptance Criteria:**
- Searches document titles, descriptions, and content
- Supports Boolean operators (AND, OR, NOT)
- Can filter by document type, status, date range
- Returns relevance-ranked results
- Shows snippets of matching content

**MCP Tool Interaction:**
```
User: "Find all documents mentioning 'adverse events' created in last 6 months"
LLM calls: documents_query(full_text_search="adverse events", created_after="2024-06-01", limit=100)
```

### User Story 4.2: Find Latest Version of Document Series
```
As a Document Manager
I want to find the latest major version of a document
So that I ensure colleagues are working with current approved content
```

**Acceptance Criteria:**
- Query returns only latest major versions (e.g., 3.0, not 2.1)
- Can optionally include all minor versions of latest major
- Shows version history and change summary
- Indicates if document is in approved state

**MCP Tool Interaction:**
```
User: "Get the current approved version of the Quality Manual"
LLM calls: documents_query(name_contains="Quality Manual", lifecycle_state="approved__c", version="latest_major")
```

---

## Scenario 5: Document Export for External Submission

**Context:** Need to package documents for regulatory submission or partner delivery.

### User Story 5.1: Export Document Package
```
As a Document Manager
I want to export a set of documents with their attachments and renditions
So that I can deliver complete document packages to external parties
```

**Acceptance Criteria:**
- Can select multiple documents for export
- Exports include all renditions (PDF, source files)
- Exports include document metadata in structured format
- Can choose export format (ZIP, eCTD, folder structure)
- Maintains document relationships in export

**MCP Tool Interaction:**
```
User: "Export these 20 regulatory documents with all attachments as a ZIP file"
LLM calls: documents_export_package(document_ids=[...], include_renditions=true, include_attachments=true, format="zip")
```

### User Story 5.2: Export with Audit Trail
```
As a Document Manager
I want to export documents with their complete audit trail
So that I can demonstrate compliance for regulatory inspections
```

**Acceptance Criteria:**
- Export includes audit trail CSV for each document
- Audit trail shows all lifecycle changes, edits, views, signatures
- User names and timestamps are included
- Export is tamper-evident (checksums, signatures)

**MCP Tool Interaction:**
```
User: "Export document DOC-12345 with full audit trail for FDA inspection"
LLM calls:
  - documents_get(document_id="DOC-12345", include_audit_trail=true)
  - documents_download_content(document_id="DOC-12345")
```

---

## Scenario 6: Document Version Management

**Context:** Need to create new versions and manage version history.

### User Story 6.1: Create New Minor Version
```
As a Document Manager
I want to create a new minor version of a document for minor corrections
So that I can update content without re-approval
```

**Acceptance Criteria:**
- Creates new minor version (e.g., 2.0 → 2.1)
- Copies all metadata from previous version
- Previous version remains accessible
- Minor version follows lifecycle rules (may skip approval for minor changes)

**MCP Tool Interaction:**
```
User: "Create a minor version of DOC-12345 to fix typos"
LLM calls: documents_create_version(document_id="DOC-12345", version_type="minor", description="Typo corrections")
```

### User Story 6.2: Compare Document Versions
```
As a Document Manager
I want to see what changed between two document versions
So that I can understand the revision history
```

**Acceptance Criteria:**
- Shows side-by-side or diff view of two versions
- Highlights metadata changes
- Shows content differences for text documents
- Lists all fields that changed with old vs. new values

**MCP Tool Interaction:**
```
User: "Show me what changed between version 1.0 and 2.0 of DOC-12345"
LLM calls: documents_compare_versions(document_id="DOC-12345", version1="1.0", version2="2.0")
```

---

## Scenario 7: Document Lock Management

**Context:** Need to coordinate editing access to prevent conflicts.

### User Story 7.1: Lock Document for Editing
```
As a Document Manager
I want to lock a document while I'm editing it
So that others don't make conflicting changes
```

**Acceptance Criteria:**
- Locks document for exclusive editing access
- Other users see lock status and lock holder
- Lock expires after configurable timeout (e.g., 1 hour)
- Can manually unlock when editing complete

**MCP Tool Interaction:**
```
User: "Lock document DOC-12345 so I can edit it"
LLM calls: documents_lock(document_id="DOC-12345")
```

### User Story 7.2: Override Stale Lock
```
As a Document Manager
I want to force-unlock a document with a stale lock
So that work isn't blocked when someone forgets to unlock
```

**Acceptance Criteria:**
- Can see who has document locked and for how long
- Can override lock if I have appropriate permissions
- Previous lock holder is notified of override
- Audit trail records lock override

**MCP Tool Interaction:**
```
User: "Unlock document DOC-12345 that's been locked for 3 hours"
LLM calls: documents_unlock(document_id="DOC-12345", force=true, reason="Stale lock override")
```

---

## Scenario 8: Template-Based Document Creation

**Context:** Creating standardized documents from approved templates.

### User Story 8.1: Create Document from Template
```
As a Document Manager
I want to create a new document from an approved template
So that I ensure consistency and save time on formatting
```

**Acceptance Criteria:**
- Can select from available templates for document type
- Template pre-fills metadata fields and content structure
- Can customize fields during creation
- Template formatting is preserved

**MCP Tool Interaction:**
```
User: "Create a new SOP using the standard SOP template"
LLM calls: documents_create_from_template(template_id="TMP-SOP-001", name="New SOP Title", type="sop__c", lifecycle="sop_lifecycle__c")
```

### User Story 8.2: List Available Templates
```
As a Document Manager
I want to see all available templates for a document type
So that I can choose the appropriate starting point
```

**Acceptance Criteria:**
- Lists templates filtered by document type
- Shows template name, description, last updated date
- Indicates required vs. optional metadata fields
- Can preview template before using

**MCP Tool Interaction:**
```
User: "Show me all available SOP templates"
LLM calls: documents_get_templates(document_type="sop__c")
```

---

## Scenario 9: Workflow Task Management

**Context:** Documents in workflows generate tasks for review and approval.

### User Story 9.1: View My Workflow Tasks
```
As a Document Manager
I want to see all workflow tasks assigned to me
So that I can prioritize and complete my responsibilities
```

**Acceptance Criteria:**
- Lists tasks grouped by workflow type
- Shows task due dates and priority
- Links to associated documents
- Indicates overdue tasks
- Can filter by task type, document type, or date range

**MCP Tool Interaction:**
```
User: "Show me all my pending workflow tasks"
LLM calls: workflows_query_tasks(assigned_to="current_user", status="pending")
```

### User Story 9.2: Complete Review Task
```
As a Document Manager
I want to complete a workflow review task with my decision
So that the document continues through the approval process
```

**Acceptance Criteria:**
- Can approve or reject with comments
- Can request changes with specific feedback
- Electronic signature captured
- Next workflow step is triggered automatically
- Document author is notified of decision

**MCP Tool Interaction:**
```
User: "Approve workflow task TASK-123 for document DOC-12345"
LLM calls: workflows_complete_task(task_id="TASK-123", decision="approve", comments="Looks good, approved")
```

---

## Scenario 10: Document Metadata Bulk Update

**Context:** Need to update metadata for multiple documents at once.

### User Story 10.1: Bulk Metadata Update
```
As a Document Manager
I want to update a specific field for multiple documents
So that I can efficiently correct or enhance metadata
```

**Acceptance Criteria:**
- Can select documents by query or list
- Can update one or more fields for all selected documents
- Validates field values before applying
- Shows preview of changes before committing
- Receives summary of successful vs. failed updates

**MCP Tool Interaction:**
```
User: "Update the therapeutic area to 'Oncology' for all documents in Study ABC-123"
LLM calls:
  - documents_query(study_number__c="ABC-123")
  - documents_bulk_update(document_ids=[...], fields={"therapeutic_area__c": "Oncology"})
```

### User Story 10.2: Bulk Classification Update
```
As a Document Manager
I want to reclassify multiple documents
So that they appear in correct document libraries
```

**Acceptance Criteria:**
- Can change classification field for multiple documents
- Validates classification is valid for document type
- Updates security/access based on new classification
- Audit trail records reclassification reason

**MCP Tool Interaction:**
```
User: "Reclassify these 10 documents from 'General' to 'Regulatory' classification"
LLM calls: documents_bulk_update(document_ids=[...], fields={"classification__v": "regulatory__c"}, reason="Regulatory impact identified")
```

---

## Summary: Document Manager User Stories

**Total Scenarios:** 10
**Total User Stories:** 20

### Primary MCP Tools Required:
1. `documents_query` - Search and retrieve documents (HIGH usage)
2. `documents_create` - Create new documents (HIGH usage)
3. `documents_update` - Update document metadata (HIGH usage)
4. `documents_upload_content` - Upload file content (HIGH usage)
5. `documents_manage_lifecycle` - Change lifecycle states (HIGH usage)
6. `documents_lock` / `documents_unlock` - Manage editing locks (MEDIUM usage)
7. `documents_get_versions` - Version history and comparison (MEDIUM usage)
8. `documents_export_package` - Export document packages (MEDIUM usage)
9. `documents_create_from_template` - Template-based creation (MEDIUM usage)
10. `workflows_query_tasks` - View workflow tasks (MEDIUM usage)
11. `workflows_complete_task` - Complete workflow steps (MEDIUM usage)
12. `documents_add_relationships` - Link related documents (LOW usage)
13. `documents_bulk_update` - Bulk metadata updates (LOW usage)

### Key Insights:
- Document Manager needs **fast, intuitive search** (most common operation)
- **Batch operations are critical** (processes 10-50 docs daily)
- **Lifecycle management** is core responsibility
- Needs **simple error recovery** for failed operations
- Values **speed over granularity** (prefers 20-30 high-level tools)
