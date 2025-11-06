# User Stories: Regulatory Affairs Specialist

**Persona:** Tier 1 - High-Volume Daily User
**Frequency:** Multiple times per day (5-20 submission-related operations daily)
**Primary Goals:** Compile compliant submissions, manage global registrations, track health authority interactions

---

## Scenario 1: NDA/BLA Submission Preparation

**Context:** Preparing New Drug Application submission to FDA with Module 1-5 structure.

### User Story 1.1: Query All Submission Documents
```
As a Regulatory Affairs Specialist
I want to find all documents required for a specific submission module
So that I can ensure completeness before packaging
```

**Acceptance Criteria:**
- Query documents by regulatory module (M1, M2, M3, M4, M5)
- Filter for approved status only
- Show latest major versions
- Identify missing required documents
- Export list for review with team

**MCP Tool Interaction:**
```
User: "Find all approved Module 2.5 documents for Product X NDA submission"
LLM calls: documents_query(
    regulatory_module__c="M2.5",
    product__c="Product X",
    lifecycle_state="approved__c",
    version="latest_major"
)
```

### User Story 1.2: Validate Document Versions
```
As a Regulatory Affairs Specialist
I want to verify all documents are at correct versions per submission requirements
So that I don't submit superseded or draft content
```

**Acceptance Criteria:**
- Check each document is latest approved major version
- Identify documents with newer versions available
- Show version history with approval dates
- Flag documents expiring soon (retest dates, stability data)

**MCP Tool Interaction:**
```
User: "Verify all documents in my submission package are latest approved versions"
LLM calls:
  - documents_query(document_ids=[...])
  - documents_get_versions(document_id=each) to compare
```

---

## Scenario 2: eCTD Binder Creation and Organization

**Context:** Creating electronic Common Technical Document structure for submission.

### User Story 2.1: Create eCTD Binder from Template
```
As a Regulatory Affairs Specialist
I want to create an eCTD binder with predefined module structure
So that I follow the required regulatory format
```

**Acceptance Criteria:**
- Template includes Module 1-5 hierarchy
- Regional variations supported (US, EU, Japan)
- Placeholder sections for all required components
- Metadata captures submission details (application number, type, sequence)

**MCP Tool Interaction:**
```
User: "Create eCTD binder for Product X NDA submission to FDA"
LLM calls: binders_create_from_template(
    template="eCTD_US_NDA",
    name="Product X NDA Submission",
    application_number__c="IND-123456",
    submission_type__c="NDA"
)
```

### User Story 2.2: Add Documents to eCTD Sections
```
As a Regulatory Affairs Specialist
I want to organize documents into appropriate eCTD sections
So that the submission follows the required structure
```

**Acceptance Criteria:**
- Can drag-drop or select documents to add to binder sections
- Documents maintain version references
- Can specify document order within sections
- Validates document types match section requirements

**MCP Tool Interaction:**
```
User: "Add these 15 clinical study reports to Module 5.3.5"
LLM calls: binders_add_documents(
    binder_id="BINDER-12345",
    section="M5.3.5",
    document_ids=[...],
    maintain_order=true
)
```

---

## Scenario 3: Health Authority Correspondence Tracking

**Context:** Managing letters, questions, and responses from FDA, EMA, PMDA, etc.

### User Story 3.1: Log Health Authority Letter
```
As a Regulatory Affairs Specialist
I want to create a record for a health authority letter received
So that I can track inquiries and response deadlines
```

**Acceptance Criteria:**
- Creates object record for correspondence
- Links to product and submission
- Captures authority, letter date, due date for response
- Uploads original letter document
- Triggers notification to responsible parties

**MCP Tool Interaction:**
```
User: "Log FDA information request letter dated 2025-11-01 with 30-day response deadline"
LLM calls:
  - objects_create(object="ha_correspondence__c", fields={
      authority__c: "FDA",
      letter_date__c: "2025-11-01",
      response_due__c: "2025-12-01",
      product__c: "Product X"
    })
  - documents_create(type="ha_letter__c", linked_object=created_id)
```

### User Story 3.2: Track Response Status
```
As a Regulatory Affairs Specialist
I want to monitor status of all open health authority correspondence
So that I ensure timely responses and avoid regulatory issues
```

**Acceptance Criteria:**
- Query shows all open correspondence
- Displays days until response due
- Highlights overdue items
- Shows linked response documents
- Can filter by authority, product, or urgency

**MCP Tool Interaction:**
```
User: "Show me all open health authority letters with responses due in next 14 days"
LLM calls: objects_query(
    object="ha_correspondence__c",
    filter="status__c='open' AND response_due__c <= TODAY+14"
)
```

---

## Scenario 4: Global Product Registration Management

**Context:** Tracking product registrations across multiple countries and regions.

### User Story 4.1: Create Product Registration Record
```
As a Regulatory Affairs Specialist
I want to create a registration record for a new market
So that I can track approval status and lifecycle
```

**Acceptance Criteria:**
- Creates registration object linked to product
- Captures country/region, application type, submission date
- Links to submission documents
- Tracks milestones (submission, review, approval, launch)
- Manages expiration and renewal dates

**MCP Tool Interaction:**
```
User: "Create registration record for Product X in Germany"
LLM calls: objects_create(
    object="product_registration__c",
    fields={
        product__c: "Product X",
        country__c: "Germany",
        authority__c: "BfArM",
        submission_date__c: "2025-11-01"
    }
)
```

### User Story 4.2: Global Registration Dashboard
```
As a Regulatory Affairs Specialist
I want to see approval status across all markets for a product
So that I can report on global registration progress
```

**Acceptance Criteria:**
- Lists all registrations for a product
- Shows status (submitted, under review, approved, rejected)
- Displays approval dates and expiration dates
- Highlights upcoming renewals (within 6 months)
- Can export report for management

**MCP Tool Interaction:**
```
User: "Show me global registration status for Product X across all markets"
LLM calls: objects_query(
    object="product_registration__c",
    filter="product__c='Product X'",
    fields=["country__c", "status__c", "approval_date__c", "expiration__c"]
)
```

---

## Scenario 5: Commitments and Obligations Tracking

**Context:** Managing post-approval commitments made to health authorities.

### User Story 5.1: Log Regulatory Commitment
```
As a Regulatory Affairs Specialist
I want to record a commitment made to a health authority
So that I can ensure we fulfill all regulatory obligations
```

**Acceptance Criteria:**
- Creates commitment record linked to registration or correspondence
- Captures commitment description, authority, due date
- Assigns responsible parties
- Links supporting documents
- Sets up reminder notifications

**MCP Tool Interaction:**
```
User: "Create commitment to submit annual safety report to EMA by 2026-03-31"
LLM calls: objects_create(
    object="regulatory_commitment__c",
    fields={
        authority__c: "EMA",
        commitment_type__c: "Annual Safety Report",
        due_date__c: "2026-03-31",
        status__c: "Open"
    }
)
```

### User Story 5.2: Monitor Commitment Deadlines
```
As a Regulatory Affairs Specialist
I want to see all upcoming commitments and their status
So that I can prevent missed deadlines that could impact product approval
```

**Acceptance Criteria:**
- Lists all open commitments
- Sorts by due date (soonest first)
- Shows days remaining until due
- Indicates if deliverable is ready
- Can mark commitments as complete with supporting documents

**MCP Tool Interaction:**
```
User: "Show me all regulatory commitments due in next 60 days"
LLM calls: objects_query(
    object="regulatory_commitment__c",
    filter="status__c='Open' AND due_date__c <= TODAY+60",
    sort="due_date__c ASC"
)
```

---

## Scenario 6: Submission Package Export

**Context:** Final packaging of submission for electronic delivery to health authority.

### User Story 6.1: Export Submission in eCTD Format
```
As a Regulatory Affairs Specialist
I want to export my eCTD binder in regulatory authority format
So that I can submit via health authority portal
```

**Acceptance Criteria:**
- Exports in eCTD v3.2.2 or v4.0 format
- Includes all documents from binder
- Generates proper folder structure and XML backbone
- Validates against eCTD specifications
- Creates MD5 checksums for integrity verification

**MCP Tool Interaction:**
```
User: "Export eCTD binder BINDER-12345 in eCTD 3.2.2 format"
LLM calls: binders_export(
    binder_id="BINDER-12345",
    format="eCTD_v3.2.2",
    include_checksums=true,
    validate=true
)
```

### User Story 6.2: Generate Submission Manifest
```
As a Regulatory Affairs Specialist
I want to generate a complete manifest of all submission contents
So that I can verify completeness and provide to authorities
```

**Acceptance Criteria:**
- Lists all documents with version, date, checksum
- Organized by eCTD module/section
- Includes document metadata
- Captures electronic signatures and approvals
- Exports in PDF and Excel formats

**MCP Tool Interaction:**
```
User: "Generate submission manifest for binder BINDER-12345"
LLM calls: binders_generate_manifest(
    binder_id="BINDER-12345",
    include_versions=true,
    include_signatures=true,
    export_format=["PDF", "Excel"]
)
```

---

## Scenario 7: Labeling and Product Information Management

**Context:** Managing approved product labeling across markets.

### User Story 7.1: Link Label to Registration
```
As a Regulatory Affairs Specialist
I want to associate approved product labels with registrations
So that I can track which label version is approved in each market
```

**Acceptance Criteria:**
- Can link label document to registration record
- Captures approval date from authority
- Tracks label effective date
- Links translations for each market
- Maintains history of label changes

**MCP Tool Interaction:**
```
User: "Link approved US label DOC-98765 to Product X US registration"
LLM calls: objects_update(
    object="product_registration__c",
    record_id="REG-123",
    fields={
        approved_label__c: "DOC-98765",
        label_approval_date__c: "2025-10-15"
    }
)
```

### User Story 7.2: Compare Labels Across Markets
```
As a Regulatory Affairs Specialist
I want to compare product labels for different markets
So that I can identify regional variations and ensure consistency
```

**Acceptance Criteria:**
- Retrieves approved labels for selected markets
- Shows side-by-side comparison
- Highlights differences in indications, contraindications, warnings
- Exports comparison report
- Links to underlying justifications for variations

**MCP Tool Interaction:**
```
User: "Compare approved labels for Product X in US, EU, and Japan"
LLM calls:
  - objects_query(object="product_registration__c", filter="product='Product X'")
  - For each: documents_get(document_id=approved_label__c)
  - documents_compare(doc_ids=[...])
```

---

## Scenario 8: Regulatory Intelligence and Updates

**Context:** Monitoring and responding to regulatory guidance changes.

### User Story 8.1: Track Guidance Documents
```
As a Regulatory Affairs Specialist
I want to maintain a library of regulatory guidance documents
So that I can ensure submissions comply with current requirements
```

**Acceptance Criteria:**
- Can categorize guidance by authority, topic, date
- Links guidance to affected products or submissions
- Tracks version history of guidance
- Sets alerts for guidance updates
- Links to internal assessments of impact

**MCP Tool Interaction:**
```
User: "Add new FDA guidance on gene therapy products"
LLM calls: documents_create(
    type="regulatory_guidance__c",
    name="FDA Guidance: Gene Therapy CMC",
    authority__c="FDA",
    effective_date__c="2025-11-01",
    category__c="CMC"
)
```

### User Story 8.2: Impact Assessment
```
As a Regulatory Affairs Specialist
I want to identify products affected by new regulatory guidance
So that I can initiate necessary updates or submissions
```

**Acceptance Criteria:**
- Query products by therapy area, indication, or classification
- Links new guidance to affected products
- Creates tasks for impact assessment
- Tracks required actions (label update, new study, variation)
- Generates report for management

**MCP Tool Interaction:**
```
User: "Find all gene therapy products that need review for new FDA CMC guidance"
LLM calls: objects_query(
    object="product__c",
    filter="therapy_area__c='Gene Therapy' AND regulatory_status__c='Approved'"
)
```

---

## Scenario 9: Variation and Supplement Management

**Context:** Managing post-approval changes requiring regulatory notifications.

### User Story 9.1: Initiate Variation Submission
```
As a Regulatory Affairs Specialist
I want to create a variation record for a post-approval change
So that I can track regulatory notifications across markets
```

**Acceptance Criteria:**
- Creates variation object linked to product and registration
- Captures variation type (Type IA, IB, II for EU; CBE, PAS for US)
- Links to change control or deviation driving the variation
- Associates supporting documents
- Tracks submission and approval timelines

**MCP Tool Interaction:**
```
User: "Create Type II variation for manufacturing site change for Product X EU registration"
LLM calls: objects_create(
    object="variation__c",
    fields={
        product__c: "Product X",
        registration__c: "REG-EU-123",
        variation_type__c: "Type II",
        description__c: "Manufacturing site change",
        submission_date__c: "2025-11-15"
    }
)
```

### User Story 9.2: Track Multi-Market Variations
```
As a Regulatory Affairs Specialist
I want to see status of the same change across all markets
So that I can coordinate global implementation
```

**Acceptance Criteria:**
- Groups related variations by change (e.g., all site changes)
- Shows submission and approval status per market
- Highlights markets where submission is pending
- Tracks implementation dates (when change goes live)
- Links to common supporting documentation

**MCP Tool Interaction:**
```
User: "Show me status of manufacturing site change across all markets"
LLM calls: objects_query(
    object="variation__c",
    filter="change_id__c='CHG-12345'",
    group_by="country__c"
)
```

---

## Scenario 10: Audit Trail for Regulatory Submissions

**Context:** Providing audit trail for regulatory inspections.

### User Story 10.1: Generate Submission Audit Trail
```
As a Regulatory Affairs Specialist
I want to generate complete audit trail for a submission
So that I can demonstrate compliance during regulatory inspections
```

**Acceptance Criteria:**
- Includes all document lifecycle events (creation, approval, changes)
- Shows all electronic signatures with signer credentials
- Captures all binder modifications (documents added/removed)
- Lists all users who accessed submission documents
- Exports in tamper-evident format with checksums

**MCP Tool Interaction:**
```
User: "Generate audit trail report for NDA submission BINDER-12345"
LLM calls:
  - binders_get(binder_id="BINDER-12345", include_audit_trail=true)
  - For each document: documents_get(doc_id, include_audit_trail=true)
  - audit_trail_export(submission_id="BINDER-12345", format="PDF")
```

### User Story 10.2: Verify Electronic Signature Compliance
```
As a Regulatory Affairs Specialist
I want to verify all submissions have proper electronic signatures
So that I ensure 21 CFR Part 11 compliance
```

**Acceptance Criteria:**
- Lists all documents requiring signatures per lifecycle
- Verifies each signature has proper user credentials
- Confirms signature meaning is recorded (e.g., "Approved by")
- Checks signature timestamps are within valid dates
- Identifies any missing or invalid signatures

**MCP Tool Interaction:**
```
User: "Verify all documents in submission BINDER-12345 have valid electronic signatures"
LLM calls:
  - binders_get_documents(binder_id="BINDER-12345")
  - For each: documents_verify_signatures(doc_id)
  - Generate compliance report
```

---

## Summary: Regulatory Affairs Specialist User Stories

**Total Scenarios:** 10
**Total User Stories:** 20

### Primary MCP Tools Required:
1. `documents_query` - Find submission documents (HIGH usage)
2. `documents_get_versions` - Verify document versions (HIGH usage)
3. `binders_create_from_template` - Create eCTD structures (HIGH usage)
4. `binders_add_documents` - Organize submission content (HIGH usage)
5. `binders_export` - Export submissions in eCTD format (HIGH usage)
6. `objects_create` - Track registrations, correspondence, commitments (HIGH usage)
7. `objects_query` - Monitor regulatory activities (HIGH usage)
8. `objects_update` - Update registration and tracking records (MEDIUM usage)
9. `documents_compare` - Compare labels across markets (MEDIUM usage)
10. `binders_generate_manifest` - Submission documentation (MEDIUM usage)
11. `audit_trail_export` - Compliance reporting (MEDIUM usage)
12. `documents_verify_signatures` - Part 11 compliance (MEDIUM usage)

### Key Insights:
- Regulatory Affairs needs **hierarchical binder organization** (eCTD structure)
- **Version control is mission-critical** (wrong version = submission failure)
- Requires **multi-object tracking** (registrations, correspondence, commitments, variations)
- **Audit trail and compliance** features are non-negotiable
- **Global coordination** across markets is common workflow
- Values **structured, resource-oriented tools** (40-60 tools optimal)
