# User Stories: QA (Quality Assurance) Specialist

**Persona:** Tier 1 - High-Volume Daily User
**Frequency:** Multiple times per day (15-40 quality event operations daily)
**Primary Goals:** Manage deviations, CAPAs, complaints, change controls, investigations, audits

---

## Scenario 1: Deviation Investigation and Documentation

**Context:** Quality deviation detected in manufacturing requiring investigation.

### User Story 1.1: Create Deviation Record
```
As a QA Specialist
I want to create a deviation record when a quality event occurs
So that I can initiate investigation and track resolution
```

**Acceptance Criteria:**
- Creates deviation object record with unique ID
- Captures location, process, product affected
- Assigns severity level (critical, major, minor)
- Links to related batch records or equipment
- Triggers automatic notifications to stakeholders
- Starts deviation clock for timeline compliance

**MCP Tool Interaction:**
```
User: "Create critical deviation for Batch 12345 - Out of specification result"
LLM calls: objects_create(
    object="deviation__c",
    fields={
        title__c: "OOS Result Batch 12345",
        severity__c: "Critical",
        batch_number__c: "12345",
        product__c: "Product X",
        location__c: "Building 3",
        detection_date__c: "2025-11-06"
    }
)
```

### User Story 1.2: Assign Investigation Team
```
As a QA Specialist
I want to assign investigation tasks to subject matter experts
So that root cause analysis can begin immediately
```

**Acceptance Criteria:**
- Can assign multiple investigators
- Creates workflow tasks for each team member
- Sets investigation deadline based on severity
- Provides investigation template/checklist
- Tracks task completion status

**MCP Tool Interaction:**
```
User: "Assign deviation DEV-12345 investigation to John (QA), Mary (Manufacturing), Bob (QC)"
LLM calls: workflows_create_tasks(
    object_id="DEV-12345",
    object_type="deviation__c",
    assignees=["john.smith", "mary.jones", "bob.wilson"],
    task_type="investigation",
    due_date="2025-11-13"
)
```

---

## Scenario 2: Root Cause Analysis Documentation

**Context:** Investigation team completing root cause analysis for deviation.

### User Story 2.1: Document Investigation Findings
```
As a QA Specialist
I want to record investigation findings and root cause
So that I have complete documentation for regulators
```

**Acceptance Criteria:**
- Updates deviation record with investigation results
- Documents immediate cause and root cause
- Captures supporting evidence (documents, photos, data)
- Links to affected SOPs or procedures
- Records investigation team conclusions

**MCP Tool Interaction:**
```
User: "Update deviation DEV-12345 with root cause: equipment calibration drift"
LLM calls: objects_update(
    object="deviation__c",
    record_id="DEV-12345",
    fields={
        root_cause__c: "Equipment calibration drift",
        immediate_cause__c: "Skipped weekly calibration check",
        investigation_complete__c: true,
        investigation_date__c: "2025-11-10"
    }
)
```

### User Story 2.2: Link Supporting Evidence
```
As a QA Specialist
I want to attach all investigation evidence to the deviation
So that I have complete traceability
```

**Acceptance Criteria:**
- Can upload multiple evidence documents
- Supports photos, test data, emails, reports
- Documents are version-controlled
- Can link existing Vault documents
- Evidence is indexed for quick retrieval

**MCP Tool Interaction:**
```
User: "Attach calibration records and test data to deviation DEV-12345"
LLM calls: objects_add_attachments(
    object="deviation__c",
    record_id="DEV-12345",
    files=["calibration_record.pdf", "test_data.xlsx"],
    description="Investigation evidence"
)
```

---

## Scenario 3: CAPA (Corrective and Preventive Action) Management

**Context:** Deviation requires CAPA to prevent recurrence.

### User Story 3.1: Initiate CAPA from Deviation
```
As a QA Specialist
I want to create a CAPA linked to a deviation
So that I ensure corrective actions are implemented
```

**Acceptance Criteria:**
- Creates CAPA object linked to parent deviation
- Inherits product, location, root cause from deviation
- Assigns CAPA owner and due date
- Creates workflow for CAPA execution
- Tracks effectiveness check requirement

**MCP Tool Interaction:**
```
User: "Create CAPA for deviation DEV-12345 to implement weekly calibration checks"
LLM calls: objects_create(
    object="capa__c",
    fields={
        title__c: "Implement weekly equipment calibration checks",
        parent_deviation__c: "DEV-12345",
        capa_owner__c: "john.smith",
        due_date__c: "2025-12-06",
        action_type__c: "Corrective"
    }
)
```

### User Story 3.2: Track CAPA Implementation
```
As a QA Specialist
I want to monitor all open CAPAs and their status
So that I ensure timely completion and prevent regulatory findings
```

**Acceptance Criteria:**
- Lists all open CAPAs
- Shows days until due or days overdue
- Displays completion percentage
- Highlights CAPAs requiring effectiveness checks
- Can filter by product, location, or priority

**MCP Tool Interaction:**
```
User: "Show me all overdue CAPAs for Building 3"
LLM calls: objects_query(
    object="capa__c",
    filter="location__c='Building 3' AND status__c='Open' AND due_date__c < TODAY",
    sort="due_date__c ASC"
)
```

---

## Scenario 4: Change Control Processing

**Context:** Proposed change to manufacturing process requires quality review.

### User Story 4.1: Review Change Control Request
```
As a QA Specialist
I want to review a change control for quality impact
So that I can approve or reject based on risk assessment
```

**Acceptance Criteria:**
- Retrieves change control record with full details
- Shows proposed change, justification, risk assessment
- Links to affected documents (SOPs, batch records)
- Provides quality review form/checklist
- Can approve, reject, or request more information

**MCP Tool Interaction:**
```
User: "Show me change control CHG-98765 for quality review"
LLM calls: objects_get(
    object="change_control__c",
    record_id="CHG-98765",
    include_related_documents=true
)
```

### User Story 4.2: Approve Change with Conditions
```
As a QA Specialist
I want to approve a change control with quality conditions
So that implementation includes necessary quality safeguards
```

**Acceptance Criteria:**
- Can approve with specific conditions/requirements
- Conditions are captured in audit trail
- Assigns tasks for condition fulfillment
- Links quality requirements to implementation plan
- Triggers notifications to change owner

**MCP Tool Interaction:**
```
User: "Approve change CHG-98765 with condition: additional operator training required"
LLM calls: workflows_complete_task(
    task_id="TASK-QA-123",
    decision="approve_with_conditions",
    conditions="Require operator training on new procedure before implementation",
    comments="Quality approved pending training completion"
)
```

---

## Scenario 5: Complaint Management

**Context:** Customer complaint received requiring quality investigation.

### User Story 5.1: Log Customer Complaint
```
As a QA Specialist
I want to create a complaint record from customer report
So that I can investigate and respond appropriately
```

**Acceptance Criteria:**
- Creates complaint object with unique ID
- Captures customer information, product, batch
- Records complaint description and severity
- Triggers automatic acknowledgment to customer
- Assigns for investigation based on complaint type
- Determines if reportable as adverse event

**MCP Tool Interaction:**
```
User: "Create complaint for Product X batch 67890 - patient reported tablet discoloration"
LLM calls: objects_create(
    object="complaint__c",
    fields={
        product__c: "Product X",
        batch_number__c: "67890",
        complaint_type__c: "Product defect",
        description__c: "Tablet discoloration reported by patient",
        severity__c: "Moderate",
        receipt_date__c: "2025-11-06"
    }
)
```

### User Story 5.2: Link Complaint to Safety Case
```
As a QA Specialist
I want to escalate a complaint to safety for adverse event reporting
So that we meet pharmacovigilance obligations
```

**Acceptance Criteria:**
- Can convert complaint to safety case
- Transfers all complaint data to safety system
- Maintains link between quality complaint and safety case
- Triggers safety team notification
- Tracks both quality and safety resolution

**MCP Tool Interaction:**
```
User: "Escalate complaint COMP-45678 to safety for adverse event reporting"
LLM calls: objects_create(
    object="safety_case__c",
    fields={
        source_complaint__c: "COMP-45678",
        product__c: "Product X",
        case_type__c: "Adverse Event",
        priority__c: "High"
    }
)
```

---

## Scenario 6: Internal Audit Preparation

**Context:** Preparing for scheduled internal GMP audit.

### User Story 6.1: Generate Audit Preparation Package
```
As a QA Specialist
I want to compile all quality records for an audit area
So that auditors have complete documentation access
```

**Acceptance Criteria:**
- Queries all relevant quality records by area/process
- Includes deviations, CAPAs, changes, complaints
- Shows only records in date range for audit
- Generates summary metrics (open vs. closed, trends)
- Exports package for auditor review

**MCP Tool Interaction:**
```
User: "Generate audit package for Manufacturing Area 3 covering January-October 2025"
LLM calls:
  - objects_query(object="deviation__c", filter="location__c='Area 3' AND date__c BETWEEN '2025-01-01' AND '2025-10-31'")
  - objects_query(object="capa__c", filter="location__c='Area 3' AND date__c BETWEEN '2025-01-01' AND '2025-10-31'")
  - objects_query(object="change_control__c", filter="location__c='Area 3' AND date__c BETWEEN '2025-01-01' AND '2025-10-31'")
  - Generate summary report
```

### User Story 6.2: Identify Open Quality Issues
```
As a QA Specialist
I want to identify all open quality issues before an audit
So that I can address or explain them to auditors
```

**Acceptance Criteria:**
- Lists all open deviations, CAPAs, changes
- Highlights overdue items
- Shows aging of open items
- Links to status updates and action plans
- Generates auditor-ready summary

**MCP Tool Interaction:**
```
User: "Show me all open quality issues that will be visible in next week's audit"
LLM calls: objects_query(
    object=["deviation__c", "capa__c", "change_control__c"],
    filter="status__c IN ('Open', 'In Progress')",
    group_by="object_type"
)
```

---

## Scenario 7: External Audit Response

**Context:** FDA inspector requests specific quality records during inspection.

### User Story 7.1: Retrieve Records for Inspector
```
As a QA Specialist
I want to quickly find specific quality records requested by inspector
So that I can provide complete documentation promptly
```

**Acceptance Criteria:**
- Fast search by record ID, product, date, type
- Retrieves complete record with all attachments
- Includes full audit trail and electronic signatures
- Can export in PDF format for inspector
- Maintains tamper-evident format

**MCP Tool Interaction:**
```
User: "Retrieve deviation DEV-12345 with complete audit trail for FDA inspector"
LLM calls:
  - objects_get(object="deviation__c", record_id="DEV-12345", include_audit_trail=true)
  - objects_get_attachments(object="deviation__c", record_id="DEV-12345")
  - Export to PDF with signatures
```

### User Story 7.2: Generate Trend Analysis for Inspector
```
As a QA Specialist
I want to generate quality trend analysis for a specific area or product
So that I can demonstrate quality oversight to inspector
```

**Acceptance Criteria:**
- Queries quality events over time period
- Groups by type, severity, root cause
- Generates charts showing trends
- Includes CAPA effectiveness metrics
- Shows improvement over time

**MCP Tool Interaction:**
```
User: "Generate 2-year deviation trend analysis for Product X"
LLM calls: objects_query(
    object="deviation__c",
    filter="product__c='Product X' AND detection_date__c >= TODAY-730",
    aggregate={
        group_by: ["MONTH(detection_date__c)", "severity__c"],
        count: true
    }
)
```

---

## Scenario 8: Quality Metrics Reporting

**Context:** Monthly quality metrics report due to management.

### User Story 8.1: Generate Quality Dashboard
```
As a QA Specialist
I want to generate key quality metrics for the month
So that I can report quality performance to management
```

**Acceptance Criteria:**
- Counts deviations, CAPAs, complaints, changes for period
- Shows open vs. closed by type
- Calculates average closure times
- Highlights overdue items
- Exports to PowerPoint or PDF for presentation

**MCP Tool Interaction:**
```
User: "Generate October 2025 quality metrics dashboard"
LLM calls:
  - objects_query(object="deviation__c", filter="MONTH(detection_date__c)=10 AND YEAR(detection_date__c)=2025", aggregate=count)
  - objects_query(object="capa__c", filter="MONTH(created_date__c)=10 AND YEAR(created_date__c)=2025", aggregate=count)
  - Calculate metrics, generate dashboard
```

### User Story 8.2: Track CAPA Effectiveness
```
As a QA Specialist
I want to measure CAPA effectiveness
So that I can demonstrate continuous improvement
```

**Acceptance Criteria:**
- Identifies CAPAs that have completed effectiveness checks
- Shows percentage of effective vs. ineffective CAPAs
- Tracks repeat deviations (CAPA was ineffective)
- Highlights areas needing additional corrective action
- Trends effectiveness over time

**MCP Tool Interaction:**
```
User: "Show me CAPA effectiveness metrics for last 6 months"
LLM calls: objects_query(
    object="capa__c",
    filter="effectiveness_check_date__c >= TODAY-180",
    fields=["effectiveness_result__c", "parent_deviation__c"],
    aggregate={
        group_by: "effectiveness_result__c",
        count: true
    }
)
```

---

## Scenario 9: Lab Investigation Management

**Context:** Out-of-specification lab result requires investigation.

### User Story 9.1: Create Lab Investigation Record
```
As a QA Specialist
I want to create an investigation for an OOS result
So that I can determine if result is valid or due to lab error
```

**Acceptance Criteria:**
- Creates lab investigation object linked to test result
- Captures test method, analyst, sample details
- Assigns investigation according to OOS procedure
- Sets timeline for investigation (typically 48 hours initial)
- Triggers notifications to laboratory and QA management

**MCP Tool Interaction:**
```
User: "Create OOS investigation for assay result 87% (spec: 95-105%) for Batch 54321"
LLM calls: objects_create(
    object="lab_investigation__c",
    fields={
        investigation_type__c: "OOS",
        test_method__c: "Assay HPLC",
        result_value__c: 87.0,
        specification__c: "95.0-105.0",
        batch_number__c: "54321",
        product__c: "Product Y"
    }
)
```

### User Story 9.2: Document Investigation Conclusion
```
As a QA Specialist
I want to record whether OOS result is confirmed or invalidated
So that I can determine impact on batch release
```

**Acceptance Criteria:**
- Records investigation conclusion (confirmed vs. lab error)
- If confirmed, links to deviation and CAPA
- If lab error, documents root cause and preventive action
- Determines batch disposition (release, reject, retest)
- Captures QA approval of conclusion

**MCP Tool Interaction:**
```
User: "Close lab investigation LAB-99999 as lab error - contaminated glassware"
LLM calls: objects_update(
    object="lab_investigation__c",
    record_id="LAB-99999",
    fields={
        conclusion__c: "Lab Error - Invalid Result",
        root_cause__c: "Contaminated glassware",
        batch_impact__c: "None - retest passed",
        status__c: "Closed"
    }
)
```

---

## Scenario 10: Supplier Quality Management

**Context:** Monitoring and managing supplier quality performance.

### User Story 10.1: Log Supplier Deviation
```
As a QA Specialist
I want to create a supplier deviation when material is out of specification
So that I can track supplier performance and trigger corrective actions
```

**Acceptance Criteria:**
- Creates supplier deviation linked to purchase order and material
- Captures supplier name, material, specification failure
- Initiates supplier notification and CAPA request
- Tracks supplier response and corrective actions
- Impacts supplier quality rating

**MCP Tool Interaction:**
```
User: "Create supplier deviation for Supplier ABC - raw material moisture content OOS"
LLM calls: objects_create(
    object="supplier_deviation__c",
    fields={
        supplier__c: "Supplier ABC",
        material__c: "API Ingredient 123",
        deviation_type__c: "OOS",
        specification_failed__c: "Moisture content",
        severity__c: "Major"
    }
)
```

### User Story 10.2: Supplier Quality Scorecard
```
As a QA Specialist
I want to generate a quality scorecard for a supplier
So that I can evaluate supplier performance and risk
```

**Acceptance Criteria:**
- Aggregates supplier deviations, rejections, late deliveries
- Calculates quality metrics (defect rate, on-time delivery)
- Shows trends over time (improving vs. declining)
- Compares to other suppliers
- Supports supplier qualification and re-evaluation

**MCP Tool Interaction:**
```
User: "Generate quality scorecard for Supplier ABC covering last 12 months"
LLM calls: objects_query(
    object="supplier_deviation__c",
    filter="supplier__c='Supplier ABC' AND date__c >= TODAY-365",
    aggregate={
        count: true,
        group_by: ["severity__c", "QUARTER(date__c)"]
    }
)
```

---

## Summary: QA Specialist User Stories

**Total Scenarios:** 10
**Total User Stories:** 20

### Primary MCP Tools Required:
1. `objects_create` - Create quality records (deviations, CAPAs, complaints, investigations) (HIGH usage)
2. `objects_update` - Update quality records with investigation findings, closures (HIGH usage)
3. `objects_query` - Monitor open quality issues, generate metrics, find records (HIGH usage)
4. `objects_get` - Retrieve complete quality records for review (HIGH usage)
5. `workflows_create_tasks` - Assign investigations and reviews (HIGH usage)
6. `workflows_complete_task` - Approve/reject change controls, complete reviews (HIGH usage)
7. `objects_add_attachments` - Link investigation evidence, supporting documents (MEDIUM usage)
8. `objects_get_audit_trail` - Provide compliance documentation for audits (MEDIUM usage)
9. `objects_query_aggregate` - Generate quality metrics and trends (MEDIUM usage)
10. `objects_link` - Link CAPAs to deviations, complaints to safety cases (MEDIUM usage)

### Key Insights:
- QA needs **robust object management** (creates/updates 15-40 quality records daily)
- **Workflow integration is critical** (investigations, approvals, task assignments)
- **Traceability and linking** between quality events (deviation→CAPA→effectiveness)
- **Time-sensitive processes** (24-hour deviation responses, 48-hour OOS investigations)
- **Audit readiness** requires instant access to complete records with audit trails
- **Metrics and reporting** are frequent activities for management and regulators
- Values **resource-oriented object tools** with workflow support (50-70 tools optimal)
