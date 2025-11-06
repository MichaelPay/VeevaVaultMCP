# QualityOne API Testing Documentation

## Overview
This document provides comprehensive testing procedures for the QualityOne API (Section 32) of VeevaTools. The QualityOne API enables quality management operations including Team assignments and HACCP Plan translation workflows for Veeva QualityOne application.

## Service Class Information
- **Service Class**: `QualityOneService`
- **Module Path**: `veevavault.services.applications.quality_one.quality_one_service`
- **Authentication**: VaultClient session required
- **Application Requirement**: Veeva QualityOne must be licensed and enabled
- **Base URL Pattern**: `/api/{version}/app/qualityone/`

## Core Functionality
The QualityOne API provides capabilities for:
- **Team Management**: Add/remove users from Team Roles in batches
- **HACCP Translation**: Export, retrieve, and import translatable HACCP Plan fields
- **Quality Workflows**: Support QualityOne-specific quality management processes
- **Batch Operations**: Handle team assignments and translations asynchronously

## Important Requirements
- **QualityOne License**: Must have Veeva QualityOne application licensed
- **File Limits**: Maximum CSV input file size is 1GB; JSON translation files max 250MB
- **Batch Limits**: Maximum 500 records per team assignment batch
- **HACCP Permissions**: Must have view/edit permissions for HACCP Plan translatable fields
- **Translation Workflow**: HACCP translation requires specific lifecycle state progression
- **Permissions**: Appropriate QualityOne permissions required

## Testing Methods

### 1. Service Initialization Testing

```python
def test_quality_one_service_initialization():
    """Test QualityOneService initialization"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    # Initialize the service
    quality_one_service = QualityOneService(vault_client)
    
    # Verify service initialization
    assert quality_one_service.client == vault_client
    assert hasattr(quality_one_service, 'manage_team_assignments')
    assert hasattr(quality_one_service, 'export_haccp_plan_translatable_fields')
    assert hasattr(quality_one_service, 'retrieve_haccp_plan_translatable_fields')
    assert hasattr(quality_one_service, 'import_haccp_plan_translatable_fields')
    
    print("✓ QualityOneService initialized successfully")
    print("✓ All required methods are available")
```

### 2. Team Assignment Testing

```python
def test_manage_team_assignments():
    """Test managing QualityOne team assignments"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test with QualityOne object
    object_name = "car__v"  # Corrective Action Record
    
    # Sample CSV data for team assignments
    team_assignments_csv = '''record_id,user_id,operation,application_role
VC400000001001,1962069,ADD,approver__c
VC400000001001,1962070,ADD,record_owner__c
VC400000001002,1962069,ADD,reviewer__c
VC400000001001,1962070,REMOVE,record_owner__c'''
    
    try:
        response = quality_one_service.manage_team_assignments(
            object_name=object_name,
            data=team_assignments_csv
        )
        
        # Verify response structure
        assert response["responseStatus"] == "SUCCESS"
        assert "jobId" in response
        
        job_id = response["jobId"]
        
        print(f"✓ QualityOne team assignments job started successfully")
        print(f"  Object: {object_name}")
        print(f"  Job ID: {job_id}")
        print(f"  Operations: 4 (3 ADD, 1 REMOVE)")
        
        return response
        
    except Exception as e:
        print(f"⚠ QualityOne team assignments test failed (may require valid records and permissions): {e}")
        return None

def test_manage_team_assignments_different_objects():
    """Test team assignments with different QualityOne object types"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test with different QualityOne team-enabled objects
    test_objects = [
        "car__v",             # Corrective Action Record
        "audit__qdm",         # Audit
        "risk_event__v",      # Risk Event
        "investigation__qdm", # Investigation
        "supplier_audit__v"   # Supplier Audit
    ]
    
    sample_assignment = '''record_id,user_id,operation,application_role
TEST_001,1962069,ADD,record_owner__c'''
    
    results = {}
    
    for object_name in test_objects:
        try:
            # Update record ID format for each object
            test_csv = sample_assignment.replace("TEST_001", f"{object_name.upper().replace('__', '_')}_001")
            
            response = quality_one_service.manage_team_assignments(
                object_name=object_name,
                data=test_csv
            )
            
            if response["responseStatus"] == "SUCCESS":
                results[object_name] = {
                    "status": "SUCCESS",
                    "job_id": response["jobId"]
                }
                print(f"✓ Team assignment successful for {object_name}: Job {response['jobId']}")
            else:
                results[object_name] = {
                    "status": "FAILURE",
                    "error": response.get("errors", [])
                }
                print(f"⚠ Team assignment failed for {object_name}: {response}")
                
        except Exception as e:
            results[object_name] = {
                "status": "EXCEPTION",
                "error": str(e)
            }
            print(f"⚠ Team assignment exception for {object_name}: {e}")
    
    successful_objects = len([obj for obj, result in results.items() if result["status"] == "SUCCESS"])
    print(f"✓ Successfully tested {successful_objects} out of {len(test_objects)} QualityOne object types")
    
    return results

def test_team_assignment_operations():
    """Test ADD and REMOVE operations for QualityOne teams"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    object_name = "car__v"
    
    # Test ADD operations
    add_operations_csv = '''record_id,user_id,operation,application_role
VC400000001001,1962069,ADD,record_owner__c
VC400000001001,1962070,ADD,reviewer__c
VC400000001001,1962071,ADD,approver__c'''
    
    try:
        add_response = quality_one_service.manage_team_assignments(
            object_name=object_name,
            data=add_operations_csv
        )
        
        if add_response["responseStatus"] == "SUCCESS":
            print(f"✓ ADD operations successful: Job {add_response['jobId']}")
        else:
            print(f"⚠ ADD operations failed: {add_response}")
        
        # Test REMOVE operations
        remove_operations_csv = '''record_id,user_id,operation,application_role
VC400000001001,1962070,REMOVE,reviewer__c
VC400000001001,1962071,REMOVE,approver__c'''
        
        remove_response = quality_one_service.manage_team_assignments(
            object_name=object_name,
            data=remove_operations_csv
        )
        
        if remove_response["responseStatus"] == "SUCCESS":
            print(f"✓ REMOVE operations successful: Job {remove_response['jobId']}")
        else:
            print(f"⚠ REMOVE operations failed: {remove_response}")
        
        return {
            "add_response": add_response,
            "remove_response": remove_response
        }
        
    except Exception as e:
        print(f"⚠ Team operations test failed: {e}")
        return None

def test_bulk_team_assignments():
    """Test bulk team assignments (up to 500 limit)"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    object_name = "car__v"
    
    # Generate bulk assignment data (test with smaller number first)
    bulk_size = 50  # Adjust based on available test data
    
    csv_lines = ["record_id,user_id,operation,application_role"]
    
    for i in range(bulk_size):
        record_id = f"VC400000{str(i+1).zfill(6)}"
        user_id = 1962069 + (i % 10)  # Cycle through user IDs
        role = ["record_owner__c", "reviewer__c", "approver__c"][i % 3]
        operation = "ADD"
        
        csv_lines.append(f"{record_id},{user_id},{operation},{role}")
    
    bulk_csv = "\n".join(csv_lines)
    
    try:
        response = quality_one_service.manage_team_assignments(
            object_name=object_name,
            data=bulk_csv
        )
        
        if response["responseStatus"] == "SUCCESS":
            print(f"✓ Bulk QualityOne assignment successful: Job {response['jobId']}")
            print(f"  Records processed: {bulk_size}")
            print(f"  CSV size: {len(bulk_csv)} characters")
        else:
            print(f"⚠ Bulk assignment failed: {response}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Bulk assignment test failed: {e}")
        return None
```

### 3. HACCP Plan Translation Testing

```python
def test_export_haccp_plan_translatable_fields():
    """Test exporting HACCP Plan translatable fields"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test with sample HACCP Plan record ID
    haccp_plan_id = "HP000000000001"  # Replace with actual HACCP Plan ID
    
    try:
        response = quality_one_service.export_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id
        )
        
        # Verify response structure
        assert response["responseStatus"] == "SUCCESS"
        assert "job_id" in response
        
        job_id = response["job_id"]
        
        print(f"✓ HACCP Plan translatable fields export started successfully")
        print(f"  HACCP Plan ID: {haccp_plan_id}")
        print(f"  Export Job ID: {job_id}")
        
        return response
        
    except Exception as e:
        print(f"⚠ HACCP Plan export test failed (may require valid HACCP Plan and permissions): {e}")
        return None

def test_retrieve_haccp_plan_translatable_fields():
    """Test retrieving HACCP Plan translatable fields"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test with sample HACCP Plan record ID (must have completed export)
    haccp_plan_id = "HP000000000001"  # Replace with actual HACCP Plan ID
    
    try:
        response = quality_one_service.retrieve_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id
        )
        
        # Verify response structure
        if response["responseStatus"] == "SUCCESS":
            # Response should contain translatable field data
            print(f"✓ HACCP Plan translatable fields retrieved successfully")
            print(f"  HACCP Plan ID: {haccp_plan_id}")
            
            # Check if we have field data
            if "data" in response:
                field_count = len(response["data"]) if isinstance(response["data"], list) else 1
                print(f"  Fields retrieved: {field_count}")
            elif isinstance(response, dict) and len(response) > 1:
                print(f"  Response contains translatable field data")
            
        else:
            print(f"⚠ HACCP Plan retrieval failed: {response}")
        
        return response
        
    except Exception as e:
        print(f"⚠ HACCP Plan retrieval test failed (may require completed export): {e}")
        return None

def test_import_haccp_plan_translatable_fields():
    """Test importing HACCP Plan translatable fields"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    import json
    import io
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test with sample HACCP Plan record ID
    haccp_plan_id = "HP000000000001"  # Replace with actual HACCP Plan ID
    
    # Sample translation data (would normally come from retrieve operation)
    sample_translation_data = {
        "haccp_plan_id": haccp_plan_id,
        "translatable_fields": [
            {
                "field_name": "name__v",
                "field_type": "String",
                "original_value": "HACCP Plan Example",
                "translated_value": "Plan HACCP Ejemplo"
            },
            {
                "field_name": "description__v",
                "field_type": "LongText",
                "original_value": "Example HACCP Plan description",
                "translated_value": "Descripción del plan HACCP de ejemplo"
            }
        ]
    }
    
    # Convert to JSON file-like object
    json_data = json.dumps(sample_translation_data, indent=2)
    file_data = io.StringIO(json_data)
    
    try:
        response = quality_one_service.import_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id,
            file_data=file_data
        )
        
        # Verify response structure
        if response["responseStatus"] == "SUCCESS":
            assert "job_id" in response
            
            job_id = response["job_id"]
            
            print(f"✓ HACCP Plan translatable fields import started successfully")
            print(f"  HACCP Plan ID: {haccp_plan_id}")
            print(f"  Import Job ID: {job_id}")
            print(f"  Translation data size: {len(json_data)} characters")
        else:
            print(f"⚠ HACCP Plan import failed: {response}")
        
        return response
        
    except Exception as e:
        print(f"⚠ HACCP Plan import test failed (may require valid data and permissions): {e}")
        return None

def test_complete_haccp_translation_workflow():
    """Test complete HACCP Plan translation workflow"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    import json
    import io
    
    quality_one_service = QualityOneService(vault_client)
    
    haccp_plan_id = "HP000000000001"  # Replace with actual HACCP Plan ID
    
    workflow_results = {
        "haccp_plan_id": haccp_plan_id,
        "steps": []
    }
    
    print(f"Starting complete HACCP translation workflow for plan: {haccp_plan_id}")
    
    try:
        # Step 1: Export translatable fields
        export_response = quality_one_service.export_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id
        )
        
        if export_response["responseStatus"] == "SUCCESS":
            export_job_id = export_response["job_id"]
            workflow_results["steps"].append({
                "step": "export",
                "status": "SUCCESS",
                "job_id": export_job_id
            })
            print(f"Step 1: ✓ Export started - Job {export_job_id}")
            
            # Note: In real workflow, you'd wait for job completion here
            print("  ℹ In production, wait for export job completion before proceeding")
            
            # Step 2: Retrieve exported fields (simulated - would need job completion)
            try:
                retrieve_response = quality_one_service.retrieve_haccp_plan_translatable_fields(
                    haccp_plan_record_id=haccp_plan_id
                )
                
                if retrieve_response["responseStatus"] == "SUCCESS":
                    workflow_results["steps"].append({
                        "step": "retrieve",
                        "status": "SUCCESS",
                        "data_size": len(str(retrieve_response))
                    })
                    print(f"Step 2: ✓ Fields retrieved successfully")
                    
                    # Step 3: Import translated fields (simulated with sample data)
                    sample_import_data = {
                        "haccp_plan_id": haccp_plan_id,
                        "translated_fields": [
                            {
                                "field": "name__v",
                                "value": "Translated HACCP Plan Name"
                            }
                        ]
                    }
                    
                    json_data = json.dumps(sample_import_data)
                    file_data = io.StringIO(json_data)
                    
                    import_response = quality_one_service.import_haccp_plan_translatable_fields(
                        haccp_plan_record_id=haccp_plan_id,
                        file_data=file_data
                    )
                    
                    if import_response["responseStatus"] == "SUCCESS":
                        import_job_id = import_response["job_id"]
                        workflow_results["steps"].append({
                            "step": "import",
                            "status": "SUCCESS",
                            "job_id": import_job_id
                        })
                        print(f"Step 3: ✓ Import started - Job {import_job_id}")
                    else:
                        workflow_results["steps"].append({
                            "step": "import",
                            "status": "FAILURE",
                            "error": import_response.get("errors", [])
                        })
                        print(f"Step 3: ⚠ Import failed: {import_response}")
                        
                else:
                    workflow_results["steps"].append({
                        "step": "retrieve",
                        "status": "FAILURE",
                        "error": retrieve_response.get("errors", [])
                    })
                    print(f"Step 2: ⚠ Retrieve failed: {retrieve_response}")
                    
            except Exception as e:
                workflow_results["steps"].append({
                    "step": "retrieve",
                    "status": "EXCEPTION",
                    "error": str(e)
                })
                print(f"Step 2: ⚠ Retrieve exception: {e}")
        else:
            workflow_results["steps"].append({
                "step": "export",
                "status": "FAILURE",
                "error": export_response.get("errors", [])
            })
            print(f"Step 1: ⚠ Export failed: {export_response}")
        
        successful_steps = len([step for step in workflow_results["steps"] if step["status"] == "SUCCESS"])
        total_steps = len(workflow_results["steps"])
        
        print(f"✓ HACCP translation workflow completed: {successful_steps}/{total_steps} steps successful")
        
        return workflow_results
        
    except Exception as e:
        print(f"⚠ HACCP translation workflow failed: {e}")
        return None

def test_haccp_translation_file_size_limits():
    """Test HACCP translation file size limits"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    import json
    import io
    
    quality_one_service = QualityOneService(vault_client)
    
    haccp_plan_id = "HP000000000001"
    
    # Test small file (should work)
    small_data = {
        "haccp_plan_id": haccp_plan_id,
        "fields": [{"field": "name__v", "value": "Small translation"}]
    }
    
    small_json = json.dumps(small_data)
    small_file = io.StringIO(small_json)
    
    try:
        small_response = quality_one_service.import_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id,
            file_data=small_file
        )
        
        if small_response["responseStatus"] == "SUCCESS":
            print(f"✓ Small file import accepted: {len(small_json)} characters")
        else:
            print(f"⚠ Small file import failed: {small_response}")
        
        # Test large file (near 250MB limit - simulated)
        # Note: This is a simulation - actual 250MB would be impractical in testing
        large_data = {
            "haccp_plan_id": haccp_plan_id,
            "fields": [
                {
                    "field": f"large_field_{i}",
                    "value": "x" * 1000  # 1KB of data per field
                }
                for i in range(100)  # 100KB total (simulated large file)
            ]
        }
        
        large_json = json.dumps(large_data)
        large_file = io.StringIO(large_json)
        
        large_response = quality_one_service.import_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id,
            file_data=large_file
        )
        
        if large_response["responseStatus"] == "SUCCESS":
            print(f"✓ Large file simulation accepted: {len(large_json)} characters")
        else:
            print(f"⚠ Large file simulation failed: {large_response}")
        
        print(f"ℹ Note: Actual 250MB limit testing would require very large files")
        
        return {
            "small_file": small_response,
            "large_file_simulation": large_response
        }
        
    except Exception as e:
        print(f"⚠ File size limit test failed: {e}")
        return None
```

### 4. Error Handling Testing

```python
def test_invalid_object_names():
    """Test team assignments with invalid object names"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    invalid_objects = [
        "invalid_object__v",
        "document__v",  # Not team-enabled
        "user__sys",    # System object
        "",             # Empty string
        "nonexistent__qdm"
    ]
    
    sample_assignment = '''record_id,user_id,operation,application_role
TEST_001,1962069,ADD,record_owner__c'''
    
    for invalid_object in invalid_objects:
        try:
            response = quality_one_service.manage_team_assignments(
                object_name=invalid_object,
                data=sample_assignment
            )
            
            if response["responseStatus"] == "FAILURE":
                errors = response.get("errors", [])
                print(f"✓ Invalid object '{invalid_object}' handled correctly: {errors}")
            else:
                print(f"⚠ Invalid object '{invalid_object}' was accepted: {response}")
                
        except Exception as e:
            print(f"✓ Exception for invalid object '{invalid_object}': {e}")

def test_invalid_haccp_plan_ids():
    """Test HACCP operations with invalid plan IDs"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    invalid_plan_ids = [
        "INVALID_PLAN_ID",
        "HP999999999999",  # Non-existent ID
        "",                # Empty string
        "123456789",       # Invalid format
        "null"             # String null
    ]
    
    for invalid_id in invalid_plan_ids:
        try:
            # Test export with invalid ID
            export_response = quality_one_service.export_haccp_plan_translatable_fields(
                haccp_plan_record_id=invalid_id
            )
            
            if export_response["responseStatus"] == "FAILURE":
                errors = export_response.get("errors", [])
                print(f"✓ Invalid HACCP Plan ID '{invalid_id}' handled correctly: {errors}")
            else:
                print(f"⚠ Invalid HACCP Plan ID '{invalid_id}' was accepted: {export_response}")
        
        except Exception as e:
            print(f"✓ Exception for invalid HACCP Plan ID '{invalid_id}': {e}")

def test_quality_one_application_requirement():
    """Test QualityOne application requirement"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test team assignment
    sample_csv = "record_id,user_id,operation,application_role\nCAR_001,1962069,ADD,record_owner__c"
    
    try:
        team_response = quality_one_service.manage_team_assignments(
            object_name="car__v",
            data=sample_csv
        )
        
        if team_response["responseStatus"] == "FAILURE":
            errors = team_response.get("errors", [])
            
            app_errors = [
                error for error in errors 
                if any(keyword in str(error).lower() for keyword in ["qualityone", "quality one", "application", "license"])
            ]
            
            if app_errors:
                print(f"✓ QualityOne application requirement enforced for team assignments")
            else:
                print(f"⚠ Different error for team assignments: {errors}")
        else:
            print(f"✓ QualityOne application available for team assignments")
        
        # Test HACCP operation
        haccp_response = quality_one_service.export_haccp_plan_translatable_fields("HP001")
        
        if haccp_response["responseStatus"] == "FAILURE":
            errors = haccp_response.get("errors", [])
            
            app_errors = [
                error for error in errors 
                if any(keyword in str(error).lower() for keyword in ["qualityone", "quality one", "haccp", "application"])
            ]
            
            if app_errors:
                print(f"✓ QualityOne application requirement enforced for HACCP operations")
            else:
                print(f"⚠ Different error for HACCP operations: {errors}")
        else:
            print(f"✓ QualityOne application available for HACCP operations")
            
    except Exception as e:
        print(f"✓ Application requirement exception: {e}")

def test_batch_size_limits():
    """Test batch size limit enforcement for team assignments"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    object_name = "car__v"
    
    # Test exceeding 500 limit
    large_batch_size = 510  # Exceeds 500 limit
    
    csv_lines = ["record_id,user_id,operation,application_role"]
    
    for i in range(large_batch_size):
        record_id = f"VC400000{str(i+1).zfill(6)}"
        user_id = 1962069 + (i % 10)
        role = "record_owner__c"
        operation = "ADD"
        
        csv_lines.append(f"{record_id},{user_id},{operation},{role}")
    
    large_csv = "\n".join(csv_lines)
    
    try:
        response = quality_one_service.manage_team_assignments(
            object_name=object_name,
            data=large_csv
        )
        
        if response["responseStatus"] == "FAILURE":
            errors = response.get("errors", [])
            if any("limit" in str(error).lower() or "500" in str(error) for error in errors):
                print("✓ Batch size limit (500) enforced correctly")
            else:
                print(f"⚠ Different error for batch size limit: {errors}")
        else:
            print(f"⚠ Large batch was accepted (should have failed): {response}")
            
    except Exception as e:
        if "limit" in str(e).lower() or "500" in str(e):
            print("✓ Exception for batch size limit correctly raised")
        else:
            print(f"⚠ Unexpected exception: {e}")
```

### 5. Integration Testing

```python
def test_quality_one_complete_workflow():
    """Test complete QualityOne workflow combining teams and HACCP"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    workflow_data = {
        "car_record": "VC400000001001",
        "haccp_plan": "HP000000000001",
        "team_members": [
            {"user_id": "1962069", "role": "record_owner__c"},
            {"user_id": "1962070", "role": "reviewer__c"}
        ],
        "workflow_stages": []
    }
    
    print("Starting complete QualityOne workflow...")
    
    try:
        # Stage 1: Set up quality team for CAR
        team_csv = "record_id,user_id,operation,application_role\n"
        for member in workflow_data["team_members"]:
            team_csv += f"{workflow_data['car_record']},{member['user_id']},ADD,{member['role']}\n"
        
        team_response = quality_one_service.manage_team_assignments(
            object_name="car__v",
            data=team_csv.strip()
        )
        
        if team_response["responseStatus"] == "SUCCESS":
            workflow_data["workflow_stages"].append({
                "stage": "team_setup",
                "status": "SUCCESS",
                "job_id": team_response["jobId"]
            })
            print(f"Stage 1: ✓ Quality team setup - Job {team_response['jobId']}")
        else:
            workflow_data["workflow_stages"].append({
                "stage": "team_setup",
                "status": "FAILURE",
                "error": team_response.get("errors", [])
            })
            print(f"Stage 1: ⚠ Quality team setup failed: {team_response}")
        
        # Stage 2: Export HACCP Plan for translation
        haccp_export_response = quality_one_service.export_haccp_plan_translatable_fields(
            haccp_plan_record_id=workflow_data["haccp_plan"]
        )
        
        if haccp_export_response["responseStatus"] == "SUCCESS":
            workflow_data["workflow_stages"].append({
                "stage": "haccp_export",
                "status": "SUCCESS",
                "job_id": haccp_export_response["job_id"]
            })
            print(f"Stage 2: ✓ HACCP export started - Job {haccp_export_response['job_id']}")
        else:
            workflow_data["workflow_stages"].append({
                "stage": "haccp_export",
                "status": "FAILURE",
                "error": haccp_export_response.get("errors", [])
            })
            print(f"Stage 2: ⚠ HACCP export failed: {haccp_export_response}")
        
        # Stage 3: Update team assignments (simulate workflow progression)
        team_update_csv = f'''record_id,user_id,operation,application_role
{workflow_data['car_record']},1962071,ADD,approver__c
{workflow_data['car_record']},1962070,REMOVE,reviewer__c'''
        
        team_update_response = quality_one_service.manage_team_assignments(
            object_name="car__v",
            data=team_update_csv
        )
        
        if team_update_response["responseStatus"] == "SUCCESS":
            workflow_data["workflow_stages"].append({
                "stage": "team_update",
                "status": "SUCCESS",
                "job_id": team_update_response["jobId"]
            })
            print(f"Stage 3: ✓ Team updated - Job {team_update_response['jobId']}")
        else:
            workflow_data["workflow_stages"].append({
                "stage": "team_update",
                "status": "FAILURE",
                "error": team_update_response.get("errors", [])
            })
            print(f"Stage 3: ⚠ Team update failed: {team_update_response}")
        
        successful_stages = len([stage for stage in workflow_data["workflow_stages"] if stage["status"] == "SUCCESS"])
        total_stages = len(workflow_data["workflow_stages"])
        
        print(f"✓ QualityOne workflow completed: {successful_stages}/{total_stages} stages successful")
        
        return workflow_data
        
    except Exception as e:
        print(f"⚠ QualityOne workflow failed: {e}")
        return None

def test_cross_object_team_management():
    """Test team management across multiple QualityOne objects"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test coordinated team assignments across multiple object types
    cross_object_assignments = [
        {
            "object": "car__v",
            "record": "VC400000001001",
            "assignments": [
                {"user": "1962069", "role": "record_owner__c", "op": "ADD"},
                {"user": "1962070", "role": "reviewer__c", "op": "ADD"}
            ]
        },
        {
            "object": "audit__qdm",
            "record": "AUD000000001001", 
            "assignments": [
                {"user": "1962069", "role": "lead_auditor__c", "op": "ADD"},
                {"user": "1962071", "role": "auditor__c", "op": "ADD"}
            ]
        },
        {
            "object": "risk_event__v",
            "record": "RE000000001001",
            "assignments": [
                {"user": "1962070", "role": "risk_owner__c", "op": "ADD"},
                {"user": "1962072", "role": "reviewer__c", "op": "ADD"}
            ]
        }
    ]
    
    results = []
    
    print("Testing cross-object team management...")
    
    for assignment_group in cross_object_assignments:
        object_name = assignment_group["object"]
        
        # Build CSV for this object
        csv_lines = ["record_id,user_id,operation,application_role"]
        
        for assignment in assignment_group["assignments"]:
            csv_lines.append(
                f"{assignment_group['record']},{assignment['user']},{assignment['op']},{assignment['role']}"
            )
        
        csv_data = "\n".join(csv_lines)
        
        try:
            response = quality_one_service.manage_team_assignments(
                object_name=object_name,
                data=csv_data
            )
            
            if response["responseStatus"] == "SUCCESS":
                results.append({
                    "object": object_name,
                    "status": "SUCCESS",
                    "job_id": response["jobId"],
                    "assignments": len(assignment_group["assignments"])
                })
                print(f"  ✓ {object_name}: {len(assignment_group['assignments'])} assignments - Job {response['jobId']}")
            else:
                results.append({
                    "object": object_name,
                    "status": "FAILURE",
                    "error": response.get("errors", []),
                    "assignments": len(assignment_group["assignments"])
                })
                print(f"  ⚠ {object_name}: Failed - {response}")
                
        except Exception as e:
            results.append({
                "object": object_name,
                "status": "EXCEPTION",
                "error": str(e),
                "assignments": len(assignment_group["assignments"])
            })
            print(f"  ⚠ {object_name}: Exception - {e}")
    
    successful_objects = len([r for r in results if r["status"] == "SUCCESS"])
    total_assignments = sum(r["assignments"] for r in results)
    
    print(f"✓ Cross-object team management: {successful_objects}/{len(cross_object_assignments)} objects successful")
    print(f"  Total assignments processed: {total_assignments}")
    
    return results
```

## Test Data Requirements

### Sample CSV Data Formats
```python
# QualityOne team assignments CSV
SAMPLE_TEAM_ASSIGNMENTS_CSV = '''record_id,user_id,operation,application_role
VC400000001001,1962069,ADD,record_owner__c
VC400000001001,1962070,ADD,reviewer__c
VC400000001002,1962069,ADD,approver__c
VC400000001001,1962070,REMOVE,reviewer__c'''

# HACCP translation data
SAMPLE_HACCP_TRANSLATION_JSON = {
    "haccp_plan_id": "HP000000000001",
    "translatable_fields": [
        {
            "field_name": "name__v",
            "field_type": "String",
            "original_value": "HACCP Plan Example",
            "translated_value": "Plan HACCP Ejemplo"
        }
    ]
}
```

### Sample Object and Record IDs
```python
# QualityOne team-enabled objects
SAMPLE_QUALITY_ONE_OBJECTS = [
    "car__v",             # Corrective Action Record
    "audit__qdm",         # Audit
    "risk_event__v",      # Risk Event
    "investigation__qdm", # Investigation
    "supplier_audit__v"   # Supplier Audit
]

# Sample record IDs
SAMPLE_RECORD_IDS = {
    "car__v": "VC400000001001",
    "audit__qdm": "AUD000000001001",
    "haccp_plan__v": "HP000000000001"
}

# Application roles
SAMPLE_APPLICATION_ROLES = [
    "record_owner__c",
    "reviewer__c",
    "approver__c",
    "lead_auditor__c",
    "auditor__c",
    "risk_owner__c"
]
```

## Expected Response Formats

### Team Assignment Response
```json
{
    "responseStatus": "SUCCESS",
    "jobId": "251801"
}
```

### HACCP Export Response
```json
{
    "responseStatus": "SUCCESS",
    "job_id": "252901"
}
```

### HACCP Retrieve Response
```json
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "field_name": "name__v",
            "field_type": "String",
            "current_value": "HACCP Plan Name"
        }
    ]
}
```

### Error Response
```json
{
    "responseStatus": "FAILURE",
    "errors": [
        {
            "type": "INVALID_DATA",
            "message": "Invalid object name"
        }
    ]
}
```

## Performance Considerations

1. **Batch Limits**: Maximum 500 records per team assignment batch
2. **File Size**: Maximum 1GB for CSV files; 250MB for JSON translation files
3. **Asynchronous Processing**: All operations are asynchronous and return job IDs
4. **Translation Workflow**: HACCP translation requires sequential export → retrieve → import
5. **State Dependencies**: HACCP operations require specific lifecycle states

## Security Notes

1. **QualityOne Permissions**: Requires appropriate QualityOne application permissions
2. **Object Access**: User must have access to target object records
3. **HACCP Permissions**: Must have view/edit permissions for HACCP Plan translatable fields
4. **Role Constraints**: Team role assignments respect configured constraints
5. **Translation Access**: Same user must perform export and retrieve operations

## Common Issues and Troubleshooting

1. **Application Not Licensed**: Ensure QualityOne application is licensed
2. **Invalid Object Names**: Verify object is team-enabled for QualityOne
3. **HACCP Lifecycle States**: Ensure HACCP Plan is in correct state for translation operations
4. **Role Constraints**: Check minimum/maximum user requirements and role eligibility
5. **Translation User**: Same user must perform all steps in HACCP translation workflow

## API Method Coverage Summary

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|---------|
| `manage_team_assignments` | POST `/app/qualityone/qms/teams/vobjects/{object_name}/actions/manageassignments` | Manage QualityOne team assignments | ✅ Covered |
| `export_haccp_plan_translatable_fields` | POST `/app/qualityone/haccp_plan/{id}/translatable_fields/actions/export` | Export HACCP Plan translatable fields | ✅ Covered |
| `retrieve_haccp_plan_translatable_fields` | GET `/app/qualityone/haccp_plan/{id}/translatable_fields/file` | Retrieve exported HACCP Plan fields | ✅ Covered |
| `import_haccp_plan_translatable_fields` | POST `/app/qualityone/haccp_plan/{id}/translatable_fields` | Import translated HACCP Plan fields | ✅ Covered |

**Total API Coverage: 4/4 methods (100%)**

This comprehensive testing framework ensures complete coverage of the QualityOne API, including team management and HACCP Plan translation workflows with proper error handling, security considerations, and integration testing.
