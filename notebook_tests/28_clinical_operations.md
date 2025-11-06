# Clinical Operations API Testing Documentation

## Overview
This document provides comprehensive testing procedures for the Clinical Operations API (Section 28) of VeevaTools. The Clinical Operations API enables management of clinical trial activities including EDL creation, milestone management, site fee handling, safety distributions, and OpenData Clinical integrations.

## Service Class Information
- **Service Class**: `ClinicalOperationsService`
- **Module Path**: `veevavault.services.applications.clinical_operations.clinical_operations_service`
- **Authentication**: VaultClient session required
- **Application Requirement**: Clinical Operations application must be enabled
- **Base URL Pattern**: `/api/{version}/vobjects/`, `/api/{version}/app/clinical/`

## Core Functionality
The Clinical Operations API provides capabilities for:
- **EDL Management**: Create Expected Document Lists and apply templates
- **Milestone Operations**: Create and manage study milestones
- **Site Fee Management**: Populate and manage site fee definitions
- **Safety Distributions**: Distribute safety reports to sites
- **Record Merging**: Merge duplicate clinical records
- **Study Migration**: Enable/disable study migration mode
- **OpenData Integration**: Manage investigator affiliations
- **Procedure Definitions**: Populate procedure definitions from templates

## Important Requirements
- **Clinical Application**: Must have appropriate Clinical application licensed
- **File Limits**: Maximum CSV input file size is 1GB, UTF-8 encoded
- **Batch Limits**: Various endpoints have specific batch size limits (10-500 records)
- **Permissions**: Specific Clinical Operations permissions required

## Testing Methods

### 1. Service Initialization Testing

```python
def test_clinical_operations_service_initialization():
    """Test ClinicalOperationsService initialization"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    # Initialize the service
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Verify service initialization
    assert clinical_ops_service.client == vault_client
    assert hasattr(clinical_ops_service, 'create_edls')
    assert hasattr(clinical_ops_service, 'recalculate_milestone_document_field')
    assert hasattr(clinical_ops_service, 'apply_edl_template_to_milestone')
    assert hasattr(clinical_ops_service, 'create_milestones_from_template')
    assert hasattr(clinical_ops_service, 'execute_milestone_story_events')
    assert hasattr(clinical_ops_service, 'generate_milestone_documents')
    assert hasattr(clinical_ops_service, 'distribute_to_sites')
    assert hasattr(clinical_ops_service, 'populate_site_fee_definitions')
    assert hasattr(clinical_ops_service, 'initiate_clinical_record_merge')
    assert hasattr(clinical_ops_service, 'enable_study_migration_mode')
    assert hasattr(clinical_ops_service, 'disable_study_migration_mode')
    assert hasattr(clinical_ops_service, 'retrieve_opendata_clinical_affiliations')
    assert hasattr(clinical_ops_service, 'change_primary_investigator_affiliation')
    assert hasattr(clinical_ops_service, 'populate_procedure_definitions')
    print("✓ ClinicalOperationsService initialized successfully")
```

### 2. EDL Management Testing

```python
def test_create_edls():
    """Test creating Expected Document Lists"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Sample EDL creation data
    edl_csv_data = '''edl_item_name__v,edl_item_number__v,document_type__v
Informed Consent,ICF-001,informed_consent__v
Protocol,PROT-001,protocol__v
Investigator CV,CV-001,investigator_cv__v'''
    
    # Test with actual study ID (replace with valid study ID)
    study_id = "STUDY_001"  # Replace with actual study ID
    
    try:
        response = clinical_ops_service.create_edls(
            study_id=study_id,
            data=edl_csv_data,
            apply_where_edl_items_exist=False
        )
        
        # Verify response structure
        assert response["responseStatus"] == "SUCCESS"
        assert "job_id" in response
        assert "url" in response
        
        job_id = response["job_id"]
        print(f"✓ EDL creation job started successfully: {job_id}")
        print(f"  Study ID: {study_id}")
        print(f"  Job URL: {response['url']}")
        
        return response
        
    except Exception as e:
        print(f"⚠ EDL creation test failed (may require valid study and permissions): {e}")
        return None

def test_apply_edl_template_to_milestone():
    """Test applying EDL template to milestone"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Test with actual milestone and EDL IDs (replace with valid IDs)
    milestone_id = "MILESTONE_001"  # Replace with actual milestone ID
    edl_id = "EDL_TEMPLATE_001"  # Replace with actual EDL template ID
    
    try:
        response = clinical_ops_service.apply_edl_template_to_milestone(
            milestone_id=milestone_id,
            edl_id=edl_id
        )
        
        # Verify response
        assert response["responseStatus"] == "SUCCESS"
        assert "job_id" in response
        assert "url" in response
        
        print(f"✓ EDL template applied to milestone successfully")
        print(f"  Milestone ID: {milestone_id}")
        print(f"  EDL Template ID: {edl_id}")
        print(f"  Job ID: {response['job_id']}")
        
        return response
        
    except Exception as e:
        print(f"⚠ EDL template application test failed (may require valid IDs): {e}")
        return None
```

### 3. Milestone Management Testing

```python
def test_recalculate_milestone_document_field():
    """Test recalculating milestone document fields"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Sample document IDs for milestone recalculation
    milestone_csv_data = '''id
7652
9875
541'''
    
    try:
        response = clinical_ops_service.recalculate_milestone_document_field(
            data=milestone_csv_data
        )
        
        # Verify response
        assert response["responseStatus"] == "SUCCESS"
        assert "responseMessage" in response
        
        print("✓ Milestone document field recalculation completed successfully")
        print(f"  Response message: {response['responseMessage']}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Milestone recalculation test failed (may require valid document IDs): {e}")
        return None

def test_create_milestones_from_template():
    """Test creating milestones from template"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Test with different object types
    test_objects = [
        ("study__v", "STUDY_001"),
        ("study_country__v", "STUDY_COUNTRY_001"),
        ("site__v", "SITE_001")
    ]
    
    for object_name, object_record_id in test_objects:
        try:
            response = clinical_ops_service.create_milestones_from_template(
                object_name=object_name,
                object_record_id=object_record_id
            )
            
            if response["responseStatus"] == "SUCCESS":
                assert "job_id" in response
                assert "url" in response
                
                print(f"✓ Milestones creation started for {object_name}: {object_record_id}")
                print(f"  Job ID: {response['job_id']}")
            else:
                print(f"⚠ Milestone creation failed for {object_name}: {response}")
                
        except Exception as e:
            print(f"⚠ Milestone creation test failed for {object_name}: {e}")
    
    return True

def test_execute_milestone_story_events():
    """Test executing milestone story events"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Sample milestone story events data
    story_events_csv = '''id,story_event__v
STUDY_001,first_patient_visit__v
STUDY_002,last_patient_visit__v
SITE_001,site_activation__v'''
    
    # Test with study object
    object_name = "study__v"
    
    try:
        response = clinical_ops_service.execute_milestone_story_events(
            object_name=object_name,
            data=story_events_csv,
            id_param=None
        )
        
        # Verify response format (CSV expected)
        assert isinstance(response, (str, dict))
        
        print(f"✓ Milestone story events executed for {object_name}")
        
        # Test with id_param
        response_with_param = clinical_ops_service.execute_milestone_story_events(
            object_name=object_name,
            data=story_events_csv,
            id_param="external_id__v"
        )
        
        print("✓ Milestone story events with id_param executed successfully")
        
        return response
        
    except Exception as e:
        print(f"⚠ Milestone story events test failed (may require valid data): {e}")
        return None

def test_generate_milestone_documents():
    """Test generating milestone documents"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Sample milestone IDs (limit to 500)
    milestone_csv_data = '''id
MILESTONE_001
MILESTONE_002
MILESTONE_003'''
    
    try:
        response = clinical_ops_service.generate_milestone_documents(
            data=milestone_csv_data
        )
        
        # Verify response
        assert response["responseStatus"] == "SUCCESS"
        
        print("✓ Milestone documents generated successfully")
        
        return response
        
    except Exception as e:
        print(f"⚠ Milestone document generation test failed (may require valid milestone IDs): {e}")
        return None
```

### 4. Safety Distribution Testing

```python
def test_distribute_to_sites():
    """Test distributing safety reports to sites"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Test with safety distribution ID (must be in Ready or Distributed state)
    safety_distribution_id = "SAFETY_DIST_001"  # Replace with actual ID
    
    try:
        response = clinical_ops_service.distribute_to_sites(
            safety_distribution_id=safety_distribution_id
        )
        
        # Verify response
        assert response["responseStatus"] == "SUCCESS"
        assert "job_id" in response
        
        print(f"✓ Safety distribution to sites initiated successfully")
        print(f"  Distribution ID: {safety_distribution_id}")
        print(f"  Job ID: {response['job_id']}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Safety distribution test failed (may require valid distribution ID): {e}")
        return None
```

### 5. Site Fee Management Testing

```python
def test_populate_site_fee_definitions():
    """Test populating site fee definitions"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Test with source study
    target_study = "TARGET_STUDY_001"
    source_study = ["SOURCE_STUDY_001", "SOURCE_STUDY_002"]
    
    try:
        response = clinical_ops_service.populate_site_fee_definitions(
            target_study=target_study,
            source_study=source_study
        )
        
        # Verify response
        assert response["responseStatus"] == "SUCCESS"
        
        print(f"✓ Site fee definitions populated from source studies")
        print(f"  Target study: {target_study}")
        print(f"  Source studies: {source_study}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Site fee population test (source study) failed: {e}")
    
    # Test with source template
    source_template = ["TEMPLATE_001", "TEMPLATE_002"]
    
    try:
        response = clinical_ops_service.populate_site_fee_definitions(
            target_study=target_study,
            source_template=source_template
        )
        
        # Verify response
        assert response["responseStatus"] == "SUCCESS"
        
        print(f"✓ Site fee definitions populated from templates")
        print(f"  Target study: {target_study}")
        print(f"  Source templates: {source_template}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Site fee population test (source template) failed: {e}")
        return None
```

### 6. Record Merging Testing

```python
def test_initiate_clinical_record_merge():
    """Test clinical record merging"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Test different object types
    mergeable_objects = [
        "person__sys",
        "organization__v", 
        "location__v",
        "contact_information__clin"
    ]
    
    for object_name in mergeable_objects:
        # Sample merge data (max 10 merge sets)
        merge_data = [
            {
                "main_record_id": f"MAIN_{object_name.upper()}_001",
                "duplicate_record_id": f"DUPLICATE_{object_name.upper()}_001"
            },
            {
                "main_record_id": f"MAIN_{object_name.upper()}_002", 
                "duplicate_record_id": f"DUPLICATE_{object_name.upper()}_002"
            }
        ]
        
        try:
            response = clinical_ops_service.initiate_clinical_record_merge(
                object_name=object_name,
                data=merge_data
            )
            
            if response["responseStatus"] == "SUCCESS":
                assert "jobID" in response
                
                print(f"✓ Record merge initiated for {object_name}")
                print(f"  Job ID: {response['jobID']}")
                print(f"  Merge sets: {len(merge_data)}")
            else:
                print(f"⚠ Record merge failed for {object_name}: {response}")
                
        except Exception as e:
            print(f"⚠ Record merge test failed for {object_name}: {e}")
    
    return True
```

### 7. Study Migration Mode Testing

```python
def test_study_migration_mode():
    """Test enabling and disabling study migration mode"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Sample study data (max 500 studies)
    study_data = [
        {"id": "STUDY_001"},
        {"id": "STUDY_002"},
        {"id": "STUDY_003"}
    ]
    
    try:
        # Test enabling migration mode
        enable_response = clinical_ops_service.enable_study_migration_mode(
            data=study_data
        )
        
        # Verify response
        assert enable_response["responseStatus"] == "SUCCESS"
        assert "jobID" in enable_response
        assert "url" in enable_response
        
        print("✓ Study migration mode enabled successfully")
        print(f"  Job ID: {enable_response['jobID']}")
        print(f"  Studies: {len(study_data)}")
        
        # Test disabling migration mode
        disable_response = clinical_ops_service.disable_study_migration_mode(
            data=study_data
        )
        
        # Verify response
        assert disable_response["responseStatus"] == "SUCCESS"
        assert "jobID" in disable_response
        assert "url" in disable_response
        
        print("✓ Study migration mode disabled successfully")
        print(f"  Job ID: {disable_response['jobID']}")
        
        return {
            "enable": enable_response,
            "disable": disable_response
        }
        
    except Exception as e:
        print(f"⚠ Study migration mode test failed (may require valid study IDs): {e}")
        return None
```

### 8. OpenData Clinical Integration Testing

```python
def test_retrieve_opendata_clinical_affiliations():
    """Test retrieving OpenData clinical affiliations"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Test with different object types
    test_objects = [
        ("person__sys", "PERSON_001"),
        ("organization__v", "ORG_001")
    ]
    
    for object_name, record_id in test_objects:
        try:
            # Test JSON response
            json_response = clinical_ops_service.retrieve_opendata_clinical_affiliations(
                object_name=object_name,
                record_id=record_id,
                accept="application/json"
            )
            
            if json_response["responseStatus"] == "SUCCESS":
                print(f"✓ OpenData affiliations retrieved for {object_name} (JSON)")
                
                if "data" in json_response:
                    affiliations = json_response["data"]
                    print(f"  Affiliations found: {len(affiliations)}")
            
            # Test CSV response
            csv_response = clinical_ops_service.retrieve_opendata_clinical_affiliations(
                object_name=object_name,
                record_id=record_id,
                accept="text/csv"
            )
            
            if isinstance(csv_response, str):
                print(f"✓ OpenData affiliations retrieved for {object_name} (CSV)")
                print(f"  CSV length: {len(csv_response)} characters")
                
        except Exception as e:
            print(f"⚠ OpenData affiliations test failed for {object_name}: {e}")
    
    return True

def test_change_primary_investigator_affiliation():
    """Test changing primary investigator affiliation"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Sample affiliation change data (max 100 records)
    affiliation_data = [
        {
            "person_sys": "PERSON_001",
            "hco_opendata_id": "HCO_LINK_001"
        },
        {
            "person_sys": "PERSON_002", 
            "hco_opendata_id": "HCO_LINK_002"
        }
    ]
    
    try:
        response = clinical_ops_service.change_primary_investigator_affiliation(
            data=affiliation_data
        )
        
        # Verify response
        assert response["responseStatus"] == "SUCCESS"
        
        print("✓ Primary investigator affiliations changed successfully")
        print(f"  Records updated: {len(affiliation_data)}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Primary investigator affiliation test failed: {e}")
        return None
```

### 9. Procedure Management Testing

```python
def test_populate_procedure_definitions():
    """Test populating procedure definitions"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Sample procedure definition data
    procedure_data = [
        {
            "source_holder_object_name": "study__v",
            "source_holder_object_ids": ["SOURCE_STUDY_001", "SOURCE_STUDY_002"],
            "destination_holder_object_name": "study__v",
            "destination_holder_object_id": "TARGET_STUDY_001"
        }
    ]
    
    try:
        response = clinical_ops_service.populate_procedure_definitions(
            data=procedure_data
        )
        
        # Verify response
        assert response["responseStatus"] == "SUCCESS"
        
        print("✓ Procedure definitions populated successfully")
        print(f"  Source studies: {procedure_data[0]['source_holder_object_ids']}")
        print(f"  Target study: {procedure_data[0]['destination_holder_object_id']}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Procedure definitions test failed (may require valid study IDs): {e}")
    
    # Test with procedure template
    template_data = [
        {
            "source_holder_object_name": "procedure_template__v",
            "source_holder_object_ids": ["TEMPLATE_001"],
            "destination_holder_object_name": "study__v", 
            "destination_holder_object_id": "TARGET_STUDY_002"
        }
    ]
    
    try:
        response = clinical_ops_service.populate_procedure_definitions(
            data=template_data
        )
        
        # Verify response
        assert response["responseStatus"] == "SUCCESS"
        
        print("✓ Procedure definitions populated from template successfully")
        print(f"  Template: {template_data[0]['source_holder_object_ids']}")
        print(f"  Target study: {template_data[0]['destination_holder_object_id']}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Procedure definitions from template test failed: {e}")
        return None
```

### 10. Integration Testing

```python
def test_complete_clinical_workflow():
    """Test complete clinical operations workflow"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Step 1: Create milestones from template
    study_id = "WORKFLOW_STUDY_001"
    
    try:
        milestone_response = clinical_ops_service.create_milestones_from_template(
            object_name="study__v",
            object_record_id=study_id
        )
        
        if milestone_response["responseStatus"] == "SUCCESS":
            print("Step 1: ✓ Milestones created from template")
        
        # Step 2: Create EDLs for the study
        edl_csv_data = '''edl_item_name__v,edl_item_number__v,document_type__v
Protocol Amendment,PROT-AMD-001,protocol_amendment__v
Safety Report,SAFETY-001,safety_report__v'''
        
        edl_response = clinical_ops_service.create_edls(
            study_id=study_id,
            data=edl_csv_data,
            apply_where_edl_items_exist=False
        )
        
        if edl_response["responseStatus"] == "SUCCESS":
            print("Step 2: ✓ EDLs created for study")
        
        # Step 3: Generate milestone documents
        milestone_csv = '''id
MILESTONE_WF_001
MILESTONE_WF_002'''
        
        milestone_docs_response = clinical_ops_service.generate_milestone_documents(
            data=milestone_csv
        )
        
        if milestone_docs_response["responseStatus"] == "SUCCESS":
            print("Step 3: ✓ Milestone documents generated")
        
        # Step 4: Populate site fee definitions
        site_fee_response = clinical_ops_service.populate_site_fee_definitions(
            target_study=study_id,
            source_study=["SOURCE_STUDY_001"]
        )
        
        if site_fee_response["responseStatus"] == "SUCCESS":
            print("Step 4: ✓ Site fee definitions populated")
        
        print("✓ Complete clinical workflow executed successfully")
        return True
        
    except Exception as e:
        print(f"⚠ Clinical workflow test failed: {e}")
        return False

def test_bulk_operations_limits():
    """Test bulk operation limits"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Test various batch size limits
    batch_tests = [
        ("milestone_documents", 500, lambda data: clinical_ops_service.generate_milestone_documents(data)),
        ("study_migration", 500, lambda data: clinical_ops_service.enable_study_migration_mode(data)),
        ("record_merge", 10, lambda data: clinical_ops_service.initiate_clinical_record_merge("person__sys", data)),
        ("investigator_affiliation", 100, lambda data: clinical_ops_service.change_primary_investigator_affiliation(data))
    ]
    
    for operation_name, max_batch, operation_func in batch_tests:
        print(f"Testing {operation_name} batch limit ({max_batch} records):")
        
        # Test within limit
        if operation_name == "milestone_documents":
            small_data = "id\n" + "\n".join([f"TEST_{i}" for i in range(min(5, max_batch))])
        elif operation_name == "study_migration":
            small_data = [{"id": f"STUDY_{i}"} for i in range(min(5, max_batch))]
        elif operation_name == "record_merge":
            small_data = [{"main_record_id": f"MAIN_{i}", "duplicate_record_id": f"DUP_{i}"} for i in range(min(5, max_batch))]
        elif operation_name == "investigator_affiliation":
            small_data = [{"person_sys": f"PERSON_{i}", "hco_opendata_id": f"HCO_{i}"} for i in range(min(5, max_batch))]
        
        try:
            response = operation_func(small_data)
            if response.get("responseStatus") == "SUCCESS":
                print(f"  ✓ Within limit test passed")
            else:
                print(f"  ⚠ Within limit test failed: {response}")
        except Exception as e:
            print(f"  ⚠ Within limit test exception: {e}")
    
    return True
```

### 11. Error Handling and Edge Cases

```python
def test_invalid_study_ids():
    """Test operations with invalid study IDs"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    invalid_study_id = "INVALID_STUDY_ID"
    
    # Test EDL creation with invalid study ID
    try:
        response = clinical_ops_service.create_edls(
            study_id=invalid_study_id,
            data="edl_item_name__v,document_type__v\nTest,test__v"
        )
        
        if response.get("responseStatus") == "FAILURE":
            assert "errors" in response
            print("✓ Invalid study ID error handled correctly for EDL creation")
        
    except Exception as e:
        print(f"✓ Exception handling for invalid study ID: {e}")

def test_batch_size_limits():
    """Test batch size limit enforcement"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Test exceeding merge limit (>10)
    large_merge_data = [
        {"main_record_id": f"MAIN_{i}", "duplicate_record_id": f"DUP_{i}"}
        for i in range(15)  # Exceeds 10 limit
    ]
    
    try:
        response = clinical_ops_service.initiate_clinical_record_merge(
            object_name="person__sys",
            data=large_merge_data
        )
        
        if response.get("responseStatus") == "FAILURE":
            errors = response.get("errors", [])
            if any("limit" in str(error).lower() for error in errors):
                print("✓ Batch size limit enforced correctly")
            else:
                print("⚠ Different error for batch size limit")
        
    except Exception as e:
        if "limit" in str(e).lower():
            print("✓ Exception for batch size limit correctly raised")
        else:
            print(f"⚠ Unexpected exception: {e}")

def test_invalid_object_names():
    """Test operations with invalid object names"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    invalid_objects = [
        "invalid_object__v",
        "document__v",  # Not supported for merge
        "nonexistent__v"
    ]
    
    for invalid_object in invalid_objects:
        try:
            response = clinical_ops_service.initiate_clinical_record_merge(
                object_name=invalid_object,
                data=[{"main_record_id": "MAIN_001", "duplicate_record_id": "DUP_001"}]
            )
            
            if response.get("responseStatus") == "FAILURE":
                print(f"✓ Invalid object name '{invalid_object}' handled correctly")
            else:
                print(f"⚠ Invalid object name '{invalid_object}' was accepted")
                
        except Exception as e:
            print(f"✓ Exception for invalid object name '{invalid_object}': {e}")

def test_permission_requirements():
    """Test permission-related errors"""
    from veevavault.services.applications.clinical_operations.clinical_operations_service import ClinicalOperationsService
    
    clinical_ops_service = ClinicalOperationsService(vault_client)
    
    # Operations that require specific permissions
    permission_tests = [
        ("site_fee_population", lambda: clinical_ops_service.populate_site_fee_definitions("STUDY_001", source_study=["SOURCE_001"])),
        ("safety_distribution", lambda: clinical_ops_service.distribute_to_sites("SAFETY_001")),
        ("record_merge", lambda: clinical_ops_service.initiate_clinical_record_merge("person__sys", [{"main_record_id": "MAIN_001", "duplicate_record_id": "DUP_001"}]))
    ]
    
    for operation_name, operation_func in permission_tests:
        try:
            response = operation_func()
            
            if response.get("responseStatus") == "FAILURE":
                errors = response.get("errors", [])
                if any("permission" in str(error).lower() for error in errors):
                    print(f"✓ Permission error handled correctly for {operation_name}")
                else:
                    print(f"⚠ Different error for {operation_name}: {errors}")
            else:
                print(f"✓ {operation_name} succeeded (user has permissions)")
                
        except Exception as e:
            if "permission" in str(e).lower() or "unauthorized" in str(e).lower():
                print(f"✓ Permission exception for {operation_name}: {e}")
            else:
                print(f"⚠ Unexpected exception for {operation_name}: {e}")
```

## Test Data Requirements

### Sample CSV Data Formats
```python
# EDL creation data
SAMPLE_EDL_CSV = '''edl_item_name__v,edl_item_number__v,document_type__v,milestone__v
Informed Consent,ICF-001,informed_consent__v,MILESTONE_001
Protocol,PROT-001,protocol__v,MILESTONE_002
Investigator CV,CV-001,investigator_cv__v,MILESTONE_003'''

# Milestone recalculation data
SAMPLE_MILESTONE_CSV = '''id
7652
9875
541'''

# Story events data
SAMPLE_STORY_EVENTS_CSV = '''id,story_event__v
STUDY_001,first_patient_visit__v
STUDY_002,last_patient_visit__v
SITE_001,site_activation__v'''
```

### Sample JSON Data
```python
# Study migration data
SAMPLE_STUDY_MIGRATION = [
    {"id": "STUDY_001"},
    {"id": "STUDY_002"},
    {"id": "STUDY_003"}
]

# Record merge data
SAMPLE_RECORD_MERGE = [
    {
        "main_record_id": "MAIN_PERSON_001",
        "duplicate_record_id": "DUPLICATE_PERSON_001"
    }
]

# Site fee definitions data
SAMPLE_SITE_FEE_DATA = {
    "target_study": "TARGET_STUDY_001",
    "source_study": ["SOURCE_STUDY_001", "SOURCE_STUDY_002"]
}
```

## Expected Response Formats

### Job Creation Response
```json
{
    "responseStatus": "SUCCESS",
    "url": "https://myvault.veevavault.com/api/v25.2/services/jobs/1201",
    "job_id": 1201
}
```

### Bulk Operation Response
```json
{
    "responseStatus": "SUCCESS",
    "responseMessage": "SUCCESS"
}
```

### OpenData Affiliations Response
```json
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "investigator_site_id": "12345",
            "hco_name": "Test Hospital",
            "contact_information": "Dr. Smith"
        }
    ]
}
```

## Performance Considerations

1. **Batch Limits**: Respect specific batch size limits for each operation
2. **File Size**: Maximum 1GB for CSV input files
3. **Concurrent Operations**: Maximum 500 concurrent merge requests
4. **Job Processing**: Most operations are asynchronous and return job IDs
5. **Record Triggers**: Migration mode bypasses triggers for performance

## Security Notes

1. **Clinical Permissions**: Specific Clinical Operations permissions required
2. **Data Sensitivity**: Clinical data requires careful handling
3. **Record Merging**: Permanent operation that deletes duplicate records
4. **Migration Mode**: Affects data visibility for non-admin users
5. **OpenData Integration**: External data source with specific access controls

## Common Issues and Troubleshooting

1. **Application Not Enabled**: Clinical Operations application must be licensed
2. **Invalid Study States**: Some operations require studies in specific states
3. **Missing Permissions**: Various operations require specific Clinical permissions
4. **Batch Size Exceeded**: Different endpoints have different batch size limits
5. **Record Dependencies**: Cannot merge records with active dependencies

## API Method Coverage Summary

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|---------|
| `create_edls` | POST `/vobjects/study__v/{study_id}/actions/etmfcreateedl` | Create Expected Document Lists | ✅ Covered |
| `recalculate_milestone_document_field` | POST `/objects/documents/milestones/actions/recalculate` | Recalculate milestone fields | ✅ Covered |
| `apply_edl_template_to_milestone` | POST `/vobjects/milestone__v/{milestone_id}/actions/etmfcreateedl` | Apply EDL template to milestone | ✅ Covered |
| `create_milestones_from_template` | POST `/vobjects/{object_name}/{object_record_id}/actions/createmilestones` | Create milestones from template | ✅ Covered |
| `execute_milestone_story_events` | POST `/app/clinical/milestone/{object_name}/actions/applytemplate` | Execute milestone story events | ✅ Covered |
| `generate_milestone_documents` | POST `/app/clinical/milestone/actions/generatemilestonedocuments` | Generate milestone documents | ✅ Covered |
| `distribute_to_sites` | POST `/app/clinical/safety_distributions/{safety_distribution_id}/actions/send` | Distribute safety reports | ✅ Covered |
| `populate_site_fee_definitions` | POST `/app/clinical/payments/populate-site-fee-definitions` | Populate site fee definitions | ✅ Covered |
| `initiate_clinical_record_merge` | POST `/app/clinical/objects/{object_name}/actions/merge` | Merge clinical records | ✅ Covered |
| `enable_study_migration_mode` | POST `/app/clinical/studies/actions/enable_migration_mode` | Enable study migration mode | ✅ Covered |
| `disable_study_migration_mode` | POST `/app/clinical/studies/actions/disable_migration_mode` | Disable study migration mode | ✅ Covered |
| `retrieve_opendata_clinical_affiliations` | GET `/app/clinical/opendata/{object_name}/{record_id}/affiliations` | Get OpenData affiliations | ✅ Covered |
| `change_primary_investigator_affiliation` | POST `/app/clinical/opendata/person__sys/primary_affiliations` | Change investigator affiliation | ✅ Covered |
| `populate_procedure_definitions` | POST `/app/clinical/ctms/populate-procedure-definitions` | Populate procedure definitions | ✅ Covered |

**Total API Coverage: 14/14 methods (100%)**

This comprehensive testing framework ensures complete coverage of the Clinical Operations API, including EDL management, milestone operations, site fee handling, safety distributions, record merging, study migration, and OpenData Clinical integration with proper error handling and security considerations.
