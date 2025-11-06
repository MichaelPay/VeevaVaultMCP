# User Stories: Clinical Operations Manager

**Persona:** Tier 1 - High-Volume Daily User
**Frequency:** Multiple times per day (10-30 clinical document/milestone operations daily)
**Primary Goals:** Maintain inspection-ready eTMF, track study milestones, manage site documents, ensure GCP compliance

---

## Scenario 1: eTMF Setup for New Clinical Trial

**Context:** New Phase 3 trial starting, need to establish eTMF structure.

### User Story 1.1: Create eTMF Binder from Template
```
As a Clinical Operations Manager
I want to create an eTMF binder based on TMF Reference Model
So that I have correct structure for regulatory inspections
```

**Acceptance Criteria:**
- Creates binder with TMF Reference Model zones and sections
- Supports DIA TMF Reference Model v4 or v5
- Includes all required artifact placeholders
- Pre-populates study metadata (protocol number, sponsor, phase)
- Creates country/site sub-binders if multi-site trial

**MCP Tool Interaction:**
```
User: "Create eTMF for Study ABC-301, Phase 3, 50 sites across US and EU"
LLM calls: clinical_operations_create_etmf_binder(
    study_number="ABC-301",
    study_phase="Phase 3",
    tmf_model="DIA TMF RM v5",
    regions=["US", "EU"],
    site_count=50
)
```

### User Story 1.2: Set Up Site-Specific eTMF Sections
```
As a Clinical Operations Manager
I want to create site-level eTMF folders for each clinical site
So that I can organize site-specific essential documents
```

**Acceptance Criteria:**
- Creates site sub-binders for each site
- Includes site-specific sections (site selection, CVs, training, delegation logs)
- Links to master study documents
- Assigns site coordinators access to their site folders
- Tracks site documentation status separately

**MCP Tool Interaction:**
```
User: "Set up site eTMF folders for 10 US sites in Study ABC-301"
LLM calls: clinical_operations_create_site_folders(
    study_number="ABC-301",
    sites=[
        {site_number: "101", country: "US", pi: "Dr. Smith"},
        {site_number: "102", country: "US", pi: "Dr. Jones"},
        ...
    ]
)
```

---

## Scenario 2: Essential Document Collection

**Context:** Collecting and filing essential documents throughout trial lifecycle.

### User Story 2.1: Upload Site Essential Documents
```
As a Clinical Operations Manager
I want to upload essential documents to correct eTMF artifact locations
So that eTMF follows TMF Reference Model structure
```

**Acceptance Criteria:**
- Can specify TMF artifact code for document placement
- Validates document type matches artifact requirements
- Supports bulk upload of multiple documents
- Auto-detects document metadata from filename or OCR
- Triggers completeness checking

**MCP Tool Interaction:**
```
User: "Upload 5 investigator CVs to Zone 3 Section 3.1 for sites 101-105"
LLM calls: clinical_operations_upload_essential_documents(
    study_number="ABC-301",
    artifact_code="03.01.01",  # Investigator CV per TMF RM
    documents=[
        {file: "CV_Site101_DrSmith.pdf", site: "101"},
        {file: "CV_Site102_DrJones.pdf", site: "102"},
        ...
    ]
)
```

### User Story 2.2: Link Master Documents Across Sites
```
As a Clinical Operations Manager
I want to link master study documents to all site eTMFs
So that sites reference centrally controlled documents
```

**Acceptance Criteria:**
- Identifies documents applicable to all sites (protocol, ICF template, manuals)
- Creates references in each site eTMF pointing to master
- Updates all site references when master is revised
- Maintains version control and traceability
- Distinguishes between master and site-specific versions

**MCP Tool Interaction:**
```
User: "Link master protocol v3.0 to all 50 site eTMFs in Study ABC-301"
LLM calls: clinical_operations_link_master_document(
    study_number="ABC-301",
    document_id="DOC-PROTO-301-v3",
    artifact_code="02.01.01",  # Final protocol
    apply_to_all_sites=true
)
```

---

## Scenario 3: Study Milestone Tracking

**Context:** Tracking critical study milestones for regulatory timelines.

### User Story 3.1: Log Study Milestone
```
As a Clinical Operations Manager
I want to record study milestones as they occur
So that I maintain accurate regulatory timeline documentation
```

**Acceptance Criteria:**
- Records milestone type (FPI, LPO, FPFV, LPLV, DBL, etc.)
- Captures actual date and supporting documentation
- Compares to planned dates, highlights variances
- Triggers notifications to stakeholders
- Updates study status dashboard

**MCP Tool Interaction:**
```
User: "Log First Patient In (FPI) for Study ABC-301 on 2025-11-06 at Site 101"
LLM calls: clinical_operations_track_milestone(
    study_number="ABC-301",
    milestone_type="First Patient In",
    actual_date="2025-11-06",
    site="101",
    supporting_document="Enrollment_Log_Site101.pdf"
)
```

### User Story 3.2: Milestone Dashboard
```
As a Clinical Operations Manager
I want to see all study milestones and their status
So that I can report progress to management and regulators
```

**Acceptance Criteria:**
- Lists all planned milestones with target and actual dates
- Shows upcoming milestones and days remaining
- Highlights missed milestone targets
- Visualizes study progress timeline
- Exports milestone report for regulatory submissions

**MCP Tool Interaction:**
```
User: "Show me milestone status for Study ABC-301"
LLM calls: clinical_operations_get_milestone_status(
    study_number="ABC-301",
    include_planned=true,
    include_actual=true
)
```

---

## Scenario 4: eTMF Inspection Readiness

**Context:** Preparing for regulatory inspection or sponsor audit of eTMF.

### User Story 4.1: eTMF Completeness Check
```
As a Clinical Operations Manager
I want to check eTMF completeness against expected artifacts
So that I can identify and address gaps before inspection
```

**Acceptance Criteria:**
- Compares eTMF content to TMF Reference Model requirements
- Identifies missing artifacts by zone/section
- Shows which artifacts are optional vs. expected vs. required
- Highlights artifacts not yet expected (future milestones)
- Generates gap analysis report

**MCP Tool Interaction:**
```
User: "Run eTMF completeness check for Study ABC-301"
LLM calls: clinical_operations_check_etmf_completeness(
    study_number="ABC-301",
    tmf_model="DIA TMF RM v5",
    as_of_date="2025-11-06"
)
```

### User Story 4.2: Generate Inspection Readiness Report
```
As a Clinical Operations Manager
I want to generate inspection readiness report for eTMF
So that I can demonstrate GCP compliance to inspectors
```

**Acceptance Criteria:**
- Shows eTMF completeness percentage
- Lists all QC findings and resolution status
- Verifies all documents have QC status
- Checks all signatures are valid
- Confirms audit trail integrity

**MCP Tool Interaction:**
```
User: "Generate inspection readiness report for Study ABC-301 eTMF"
LLM calls: clinical_operations_generate_inspection_report(
    study_number="ABC-301",
    include_completeness=true,
    include_qc_status=true,
    include_signatures=true,
    include_audit_trail=true
)
```

---

## Scenario 5: Site Activation and Close-Out

**Context:** Managing site lifecycle from activation through close-out.

### User Story 5.1: Track Site Activation Status
```
As a Clinical Operations Manager
I want to monitor site activation progress for all sites
So that I can ensure sites are ready to enroll patients
```

**Acceptance Criteria:**
- Lists all sites with activation status
- Shows completed vs. pending activation tasks
- Tracks regulatory submissions (IND, EC/IRB approvals)
- Monitors contract and budget approvals
- Highlights sites ready for activation vs. blocked

**MCP Tool Interaction:**
```
User: "Show me site activation status for all sites in Study ABC-301"
LLM calls: clinical_operations_get_site_activation_status(
    study_number="ABC-301",
    include_tasks=true,
    include_approvals=true
)
```

### User Story 5.2: Initiate Site Close-Out
```
As a Clinical Operations Manager
I want to initiate close-out process when site completes enrollment
So that I collect all final documents before site closure
```

**Acceptance Criteria:**
- Creates close-out checklist for site
- Assigns close-out tasks to site coordinator and monitor
- Tracks receipt of final documents (final logs, AE reports, etc.)
- Monitors shipment of study materials back to sponsor
- Marks site as closed when all tasks complete

**MCP Tool Interaction:**
```
User: "Initiate close-out for Site 101 in Study ABC-301"
LLM calls: clinical_operations_initiate_site_closeout(
    study_number="ABC-301",
    site_number="101",
    last_patient_date="2025-10-15",
    site_coordinator="jane.smith@cro.com"
)
```

---

## Scenario 6: Document QC and Review

**Context:** Quality control review of eTMF documents before filing.

### User Story 6.1: Assign Documents for QC
```
As a Clinical Operations Manager
I want to assign documents to QC reviewers
So that all eTMF content is quality-checked before filing
```

**Acceptance Criteria:**
- Can assign individual or batch of documents to QC reviewer
- Creates QC workflow task with checklist
- Sets QC due date based on document priority
- Tracks QC status (not started, in progress, complete)
- Notifies when QC is overdue

**MCP Tool Interaction:**
```
User: "Assign 25 site CVs for QC review to Mary"
LLM calls: clinical_operations_assign_qc(
    documents=[list of 25 doc IDs],
    qc_reviewer="mary.wilson",
    qc_type="Site Essential Document QC",
    due_date="2025-11-13"
)
```

### User Story 6.2: Complete QC Review
```
As a Clinical Operations Manager
I want to complete QC review and mark documents as QC'd
So that documents are approved for final eTMF filing
```

**Acceptance Criteria:**
- Can approve document with "QC Passed" status
- Can reject with QC findings requiring correction
- Records QC comments and issues found
- Updates document QC status and QC date
- Triggers re-filing workflow if document corrected

**MCP Tool Interaction:**
```
User: "Complete QC for document DOC-CV-101 - Approved"
LLM calls: workflows_complete_task(
    task_id="QC-TASK-123",
    decision="approved",
    qc_status="QC Passed",
    comments="All required elements present, signature valid"
)
```

---

## Scenario 7: CTMS Integration and Data Sync

**Context:** Synchronizing data between eTMF and Clinical Trial Management System.

### User Story 7.1: Sync Study Metadata from CTMS
```
As a Clinical Operations Manager
I want to sync study information from CTMS to eTMF
So that study metadata is consistent across systems
```

**Acceptance Criteria:**
- Pulls study details (sites, milestones, contacts) from CTMS
- Updates eTMF binder metadata automatically
- Identifies discrepancies between systems
- Can schedule automatic sync (daily, weekly)
- Logs all sync activities for audit trail

**MCP Tool Interaction:**
```
User: "Sync Study ABC-301 metadata from CTMS to eTMF"
LLM calls: clinical_operations_sync_ctms(
    study_number="ABC-301",
    sync_type="study_metadata",
    ctms_system="Veeva CTMS"
)
```

### User Story 7.2: Push Milestone Updates to CTMS
```
As a Clinical Operations Manager
I want to update CTMS when milestones are recorded in eTMF
So that both systems reflect current study status
```

**Acceptance Criteria:**
- Automatically updates CTMS when milestone logged in eTMF
- Bi-directional sync keeps systems aligned
- Handles conflicts (different dates in each system)
- Maintains data lineage and audit trail
- Can manually trigger sync if automatic fails

**MCP Tool Interaction:**
```
User: "Push FPI milestone for Study ABC-301 to CTMS"
LLM calls: clinical_operations_update_ctms_milestone(
    study_number="ABC-301",
    milestone="First Patient In",
    date="2025-11-06",
    site="101"
)
```

---

## Scenario 8: OpenData Clinical Integration

**Context:** Integrating with OpenData Clinical for EDC and regulatory data exchange.

### User Story 8.1: Retrieve Affiliation Data
```
As a Clinical Operations Manager
I want to retrieve investigator affiliations from OpenData Clinical
So that I have verified investigator credentials in eTMF
```

**Acceptance Criteria:**
- Queries OpenData Clinical for investigator information
- Retrieves CV, medical licenses, training records
- Imports into eTMF as source data verified documents
- Maintains link to OpenData Clinical for updates
- Flags when OpenData Clinical credentials expire

**MCP Tool Interaction:**
```
User: "Retrieve investigator affiliation for Dr. Smith from OpenData Clinical"
LLM calls: clinical_operations_get_opendata_affiliation(
    investigator_id="INV-12345",
    include_cv=true,
    include_licenses=true,
    include_training=true
)
```

### User Story 8.2: Change Primary Investigator
```
As a Clinical Operations Manager
I want to change the principal investigator for a site
So that eTMF reflects current site leadership
```

**Acceptance Criteria:**
- Updates PI assignment for site
- Retrieves new PI credentials from OpenData Clinical
- Archives previous PI documents
- Creates task to collect new PI documents (CV, license, etc.)
- Updates delegation log and signature authority

**MCP Tool Interaction:**
```
User: "Change PI for Site 101 from Dr. Smith to Dr. Johnson"
LLM calls: clinical_operations_change_pi(
    study_number="ABC-301",
    site_number="101",
    current_pi="Dr. Smith",
    new_pi="Dr. Johnson",
    effective_date="2025-11-06"
)
```

---

## Scenario 9: Protocol Deviation Tracking

**Context:** Recording and managing protocol deviations during study conduct.

### User Story 9.1: Log Protocol Deviation
```
As a Clinical Operations Manager
I want to record a protocol deviation when identified
So that I maintain complete safety and compliance documentation
```

**Acceptance Criteria:**
- Creates protocol deviation record linked to study
- Captures deviation type, site, subject (if applicable)
- Records deviation date and discovery date
- Classifies severity (minor, major, critical)
- Initiates review workflow for causality assessment
- Links to affected case report forms or source documents

**MCP Tool Interaction:**
```
User: "Log protocol deviation for Study ABC-301 Site 101 - inclusion criteria violation"
LLM calls: objects_create(
    object="protocol_deviation__c",
    fields={
        study_number__c: "ABC-301",
        site_number__c: "101",
        deviation_type__c: "Inclusion/Exclusion Criteria",
        severity__c: "Major",
        deviation_date__c: "2025-11-05",
        discovery_date__c: "2025-11-06"
    }
)
```

### User Story 9.2: Protocol Deviation Summary Report
```
As a Clinical Operations Manager
I want to generate protocol deviation summary for study reporting
So that I can include in CSR and regulatory submissions
```

**Acceptance Criteria:**
- Lists all protocol deviations by type and severity
- Shows frequency by site (identifies problem sites)
- Includes CAPA status for significant deviations
- Summarizes impact on study integrity
- Exports for Clinical Study Report

**MCP Tool Interaction:**
```
User: "Generate protocol deviation summary for Study ABC-301"
LLM calls: objects_query(
    object="protocol_deviation__c",
    filter="study_number__c='ABC-301'",
    aggregate={
        group_by: ["deviation_type__c", "severity__c"],
        count: true
    }
)
```

---

## Scenario 10: Study Migration and Archival

**Context:** Enabling study migration mode for data transfer or archiving completed study.

### User Story 10.1: Enable Study Migration Mode
```
As a Clinical Operations Manager
I want to enable migration mode for a study
So that I can export complete eTMF to another system or archive
```

**Acceptance Criteria:**
- Enables migration mode for study
- Allows full data extraction including metadata
- Maintains document relationships and structure
- Preserves audit trail and electronic signatures
- Creates migration log for compliance

**MCP Tool Interaction:**
```
User: "Enable migration mode for Study ABC-301 for archival"
LLM calls: clinical_operations_enable_migration_mode(
    study_number="ABC-301",
    migration_type="archival",
    reason="Study completed, preparing for long-term archive"
)
```

### User Story 10.2: Export Complete eTMF
```
As a Clinical Operations Manager
I want to export complete eTMF for completed study
So that I can transfer to long-term archive system
```

**Acceptance Criteria:**
- Exports all eTMF documents with folder structure
- Includes all metadata, annotations, QC status
- Preserves document relationships and versioning
- Exports audit trail for entire eTMF
- Creates export manifest and validation report
- Format suitable for regulatory inspection (eCTD structure)

**MCP Tool Interaction:**
```
User: "Export complete eTMF for Study ABC-301 for archival"
LLM calls: clinical_operations_export_etmf(
    study_number="ABC-301",
    include_audit_trail=true,
    include_metadata=true,
    export_format="eCTD",
    generate_manifest=true
)
```

---

## Summary: Clinical Operations Manager User Stories

**Total Scenarios:** 10
**Total User Stories:** 20

### Primary MCP Tools Required:
1. `clinical_operations_create_etmf_binder` - Set up eTMF structure (HIGH usage)
2. `clinical_operations_upload_essential_documents` - File documents to eTMF (HIGH usage)
3. `clinical_operations_track_milestone` - Record study milestones (HIGH usage)
4. `clinical_operations_check_etmf_completeness` - Inspection readiness (HIGH usage)
5. `clinical_operations_assign_qc` - QC workflow management (HIGH usage)
6. `clinical_operations_sync_ctms` - CTMS integration (MEDIUM usage)
7. `clinical_operations_get_opendata_affiliation` - OpenData Clinical integration (MEDIUM usage)
8. `clinical_operations_change_pi` - Site management (MEDIUM usage)
9. `clinical_operations_enable_migration_mode` - Study lifecycle management (LOW usage)
10. `clinical_operations_export_etmf` - Archival and transfer (LOW usage)
11. `binders_add_documents` - Organize eTMF content (HIGH usage)
12. `binders_get_structure` - Navigate eTMF hierarchy (MEDIUM usage)
13. `objects_create` - Protocol deviations, site records (MEDIUM usage)
14. `objects_query` - Reporting and monitoring (MEDIUM usage)
15. `workflows_complete_task` - QC reviews, approvals (MEDIUM usage)

### Key Insights:
- Clinical Ops needs **specialized eTMF/clinical tools** (10-15 clinical-specific tools)
- **TMF Reference Model compliance** is non-negotiable (regulatory requirement)
- **Multi-system integration** critical (CTMS, OpenData Clinical, EDC)
- **Inspection readiness** drives most activities
- **Site-level organization** requires hierarchical document management
- **QC workflows** are core to eTMF quality
- Values **clinical-specific resource organization** (40-60 tools optimal)
