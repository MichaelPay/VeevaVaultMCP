# User Stories: Safety/Pharmacovigilance Specialist

**Persona:** Tier 2 - Regular Specialized User
**Frequency:** Daily (5-15 safety case operations daily)
**Primary Goals:** E2B case intake, ICSR processing, regulatory reporting, safety signal detection

---

## Scenario 1: E2B R3 Case Intake

**Context:** Receiving adverse event case in E2B R3 XML format from clinical trial or spontaneous report.

### User Story 1.1: Intake E2B R3 File
```
As a Safety Specialist
I want to import E2B R3 XML file into safety system
So that adverse event is registered for processing
```

**Acceptance Criteria:**
- Parses E2B R3 XML and validates against ICH schema
- Creates safety case object with unique case ID
- Extracts patient, event, product, reporter information
- Identifies duplicate cases (same patient/event)
- Triggers auto-triage based on seriousness criteria

**MCP Tool Interaction:**
```
User: "Import E2B R3 file AE_12345.xml for Product X"
LLM calls: safety_intake_e2b_r3(
    file_path="AE_12345.xml",
    product="Product X",
    source="Clinical Trial ABC-301",
    check_duplicates=true
)
```

### User Story 1.2: Validate Case Data Quality
```
As a Safety Specialist
I want to validate completeness and quality of case data
So that I can identify missing critical information
```

**Acceptance Criteria:**
- Checks for required regulatory fields (patient ID, event term, outcome)
- Validates medical terminology (MedDRA coding)
- Identifies inconsistencies (dates, causality assessments)
- Flags cases with missing reportable elements
- Generates data quality score

**MCP Tool Interaction:**
```
User: "Validate safety case SAF-12345 for regulatory reporting"
LLM calls: safety_validate_case(
    case_id="SAF-12345",
    validation_type="regulatory_submission",
    check_meddra_coding=true
)
```

---

## Scenario 2: Case Triage and Assignment

**Context:** New cases need initial safety assessment and assignment.

### User Story 2.1: Auto-Triage Serious Cases
```
As a Safety Specialist
I want system to automatically identify serious adverse events
So that critical cases are prioritized immediately
```

**Acceptance Criteria:**
- Applies ICH seriousness criteria (death, life-threatening, hospitalization, etc.)
- Flags cases requiring expedited reporting (15-day vs. 30-day)
- Assigns priority level (urgent, high, medium, low)
- Routes to appropriate safety physician based on product/indication
- Triggers immediate notification for fatal or life-threatening cases

**MCP Tool Interaction:**
```
User: "Triage all new safety cases from last 24 hours"
LLM calls: safety_triage_cases(
    received_after="2025-11-05",
    apply_seriousness_criteria=true,
    auto_assign=true
)
```

### User Story 2.2: Assign Case to Safety Physician
```
As a Safety Specialist
I want to assign case to safety physician for medical review
So that causality assessment can be completed
```

**Acceptance Criteria:**
- Can assign to specific physician or use round-robin
- Creates workflow task for medical review
- Sets due date based on regulatory timeline
- Physician receives case notification with summary
- Tracks assignment in case audit trail

**MCP Tool Interaction:**
```
User: "Assign case SAF-12345 to Dr. Wilson for medical review, due in 3 days"
LLM calls: workflows_create_task(
    object_id="SAF-12345",
    object_type="safety_case__c",
    assignee="dr.wilson",
    task_type="medical_review",
    due_date="2025-11-09"
)
```

---

## Scenario 3: Medical Coding and Narrative Development

**Context:** Standardizing medical terms and creating case narratives.

### User Story 3.1: Code Adverse Events with MedDRA
```
As a Safety Specialist
I want to assign MedDRA preferred terms to adverse events
So that cases can be analyzed and reported consistently
```

**Acceptance Criteria:**
- Search MedDRA dictionary by term or code
- Assigns PT (Preferred Term) and hierarchical terms (SOC, HLGT, HLT, LLT)
- Supports multiple events per case
- Validates MedDRA version consistency
- Tracks coding history if terms are revised

**MCP Tool Interaction:**
```
User: "Code event 'severe headache' in case SAF-12345 with MedDRA"
LLM calls: safety_code_event(
    case_id="SAF-12345",
    event_description="severe headache",
    meddra_version="26.1",
    suggest_terms=true
)
```

### User Story 3.2: Generate Case Narrative
```
As a Safety Specialist
I want to generate structured case narrative from case data
So that I have comprehensive description for regulatory submission
```

**Acceptance Criteria:**
- Compiles patient demographics, medical history, events, outcomes
- Follows regulatory narrative format (ICH E2B)
- Includes causality assessment and dechallenge/rechallenge
- Supports multiple languages for global submissions
- Can customize narrative template by authority

**MCP Tool Interaction:**
```
User: "Generate FDA-format narrative for case SAF-12345"
LLM calls: safety_generate_narrative(
    case_id="SAF-12345",
    format="FDA_CIOMS",
    language="English",
    include_causality=true
)
```

---

## Scenario 4: Causality Assessment

**Context:** Safety physician assessing relationship between product and adverse event.

### User Story 4.1: Record Causality Assessment
```
As a Safety Specialist
I want to document physician's causality assessment
So that product-event relationship is officially recorded
```

**Acceptance Criteria:**
- Captures causality category (related, probably related, possibly related, unlikely, unrelated)
- Records assessment method (WHO-UMC, Naranjo)
- Documents rationale for assessment
- Requires electronic signature from assessor
- Updates case status to "medically reviewed"

**MCP Tool Interaction:**
```
User: "Record causality for case SAF-12345 as 'Probably Related'"
LLM calls: safety_record_causality(
    case_id="SAF-12345",
    causality="probably_related",
    method="WHO-UMC",
    rationale="Temporal relationship, known ADR, no alternative causes",
    assessor="dr.wilson"
)
```

---

## Scenario 5: Regulatory Reporting Preparation

**Context:** Preparing expedited case reports for submission to health authorities.

### User Story 5.1: Export Case in E2B Format
```
As a Safety Specialist
I want to export case in E2B R3 format for submission
So that I can report to FDA, EMA, or other authorities
```

**Acceptance Criteria:**
- Exports valid E2B R3 XML file
- Includes all required regulatory elements
- Validates against ICH schema before export
- Generates transmission file for gateway submission
- Creates export log for compliance tracking

**MCP Tool Interaction:**
```
User: "Export case SAF-12345 in E2B R3 format for FDA submission"
LLM calls: safety_export_case(
    case_id="SAF-12345",
    export_format="E2B_R3",
    authority="FDA",
    validate=true
)
```

### User Story 5.2: Track Submission Status
```
As a Safety Specialist
I want to track submission status of reported cases
So that I ensure regulatory obligations are met
```

**Acceptance Criteria:**
- Shows submission date and authority
- Tracks acknowledgment receipt from authority
- Monitors regulatory clock (15-day, 30-day deadlines)
- Highlights overdue submissions
- Links submission confirmations and correspondence

**MCP Tool Interaction:**
```
User: "Show me all cases pending FDA submission in next 7 days"
LLM calls: objects_query(
    object="safety_case__c",
    filter="submission_due_date__c <= TODAY+7 AND submission_status__c='Pending'",
    sort="submission_due_date__c ASC"
)
```

---

## Scenario 6: Follow-Up Information Management

**Context:** Receiving additional information on previously reported cases.

### User Story 6.1: Record Follow-Up Information
```
As a Safety Specialist
I want to add follow-up information to existing case
So that case history is complete and current
```

**Acceptance Criteria:**
- Updates existing case record with new information
- Creates follow-up report if regulatory re-submission required
- Links follow-up documents to original case
- Triggers re-assessment if new information changes causality
- Maintains version history of case evolution

**MCP Tool Interaction:**
```
User: "Add follow-up info to case SAF-12345: patient recovered, no sequelae"
LLM calls: objects_update(
    object="safety_case__c",
    record_id="SAF-12345",
    fields={
        follow_up_received_date__c: "2025-11-06",
        outcome__c: "Recovered",
        follow_up_number__c: 1
    }
)
```

---

## Scenario 7: Safety Signal Detection

**Context:** Analyzing aggregate data to identify potential safety signals.

### User Story 7.1: Query Cases by Event Term
```
As a Safety Specialist
I want to find all cases for specific adverse event
So that I can assess frequency and characteristics
```

**Acceptance Criteria:**
- Queries by MedDRA PT, HLT, or SOC
- Filters by product, date range, geographic region
- Shows case count and event rate
- Can drill down to individual cases
- Exports case list for detailed review

**MCP Tool Interaction:**
```
User: "Find all cases of 'myocardial infarction' for Product X in last 12 months"
LLM calls: objects_query(
    object="safety_case__c",
    filter="product__c='Product X' AND meddra_pt__c='Myocardial infarction' AND received_date__c >= TODAY-365"
)
```

---

## Summary: Safety Specialist User Stories

**Total Scenarios:** 7
**Total User Stories:** 14

### Primary MCP Tools Required:
1. `safety_intake_e2b_r3` - Import adverse event cases (HIGH usage)
2. `safety_validate_case` - Data quality checks (HIGH usage)
3. `safety_triage_cases` - Auto-triage and prioritization (HIGH usage)
4. `safety_code_event` - MedDRA medical coding (HIGH usage)
5. `safety_generate_narrative` - Case narrative generation (HIGH usage)
6. `safety_record_causality` - Causality assessment (HIGH usage)
7. `safety_export_case` - E2B export for submission (HIGH usage)
8. `objects_update` - Case updates and follow-ups (MEDIUM usage)
9. `objects_query` - Case queries for signal detection (MEDIUM usage)
10. `workflows_create_task` - Assignment and routing (MEDIUM usage)

### Key Insights:
- Safety needs **highly specialized safety-specific tools** (7-10 dedicated safety tools)
- **E2B R2/R3 format** is industry standard (ICH regulatory requirement)
- **Time-critical** - expedited reporting deadlines (15-day serious, 7-day fatal)
- **MedDRA coding** is essential for global reporting
- **Regulatory compliance** drives all processes
- Values **specialized safety resource organization** (30-40 tools optimal, with dedicated safety context)
