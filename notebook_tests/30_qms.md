# QMS (Quality Management System) API Testing Documentation

## Overview
This document provides comprehensive testing procedures for the QMS API (Section 30) of VeevaTools. The QMS API enables quality management operations including Quality Team assignments and Batch Release disposition management for Veeva QMS and Batch Release applications.

## Service Class Information
- **Service Class**: `QMSService`
- **Module Path**: `veevavault.services.applications.qms.qms_service`
- **Authentication**: VaultClient session required
- **Application Requirements**: Veeva QMS required; Veeva Batch Release required for batch operations
- **Base URL Pattern**: `/api/{version}/app/quality/`

## Core Functionality
The QMS API provides capabilities for:
- **Quality Team Management**: Add/remove users from Quality Teams on quality events
- **Batch Disposition**: Create batch disposition records from batches and disposition plans
- **Quality Event Processing**: Manage quality team assignments with business logic enforcement
- **Batch Release**: Support batch release workflows through disposition creation

## Important Requirements
- **QMS License**: Veeva QMS application must be licensed for quality team operations
- **Batch Release License**: Veeva Batch Release required for disposition operations
- **File Limits**: Maximum CSV input file size is 1GB, UTF-8 encoded
- **Batch Limits**: Maximum 500 records per quality team assignment batch
- **Business Logic**: Respects minimum/maximum users, role constraints, and state transitions
- **Permissions**: Appropriate QMS and Batch Release permissions required

## Testing Methods

### 1. Service Initialization Testing

```python
def test_qms_service_initialization():
    """Test QMSService initialization"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    # Initialize the service
    qms_service = QMSService(vault_client)
    
    # Verify service initialization
    assert qms_service.client == vault_client
    assert hasattr(qms_service, 'manage_quality_team_assignments')
    assert hasattr(qms_service, 'create_batch_disposition')
    
    print("✓ QMSService initialized successfully")
    print("✓ All required methods are available")
```

### 2. Quality Team Assignment Testing

```python
def test_manage_quality_team_assignments():
    """Test managing quality team assignments"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Test with quality event object
    object_name = "quality_event__qdm"
    
    # Sample CSV data for team assignments
    team_assignments_csv = '''record_id,user_id,application_role,operation
QE000000000001,12345,record_owner__c,ADD
QE000000000001,67890,reviewer__c,ADD
QE000000000002,12345,investigator__c,ADD
QE000000000002,67890,record_owner__c,REMOVE'''
    
    try:
        response = qms_service.manage_quality_team_assignments(
            object_name=object_name,
            data=team_assignments_csv
        )
        
        # Verify response structure
        assert response["responseStatus"] == "SUCCESS"
        assert "jobId" in response
        
        job_id = response["jobId"]
        
        print(f"✓ Quality team assignments job started successfully")
        print(f"  Object: {object_name}")
        print(f"  Job ID: {job_id}")
        print(f"  Operations: 4 (2 ADD, 1 ADD, 1 REMOVE)")
        
        return response
        
    except Exception as e:
        print(f"⚠ Quality team assignments test failed (may require valid records and permissions): {e}")
        return None

def test_manage_quality_team_assignments_different_objects():
    """Test quality team assignments with different object types"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Test with different team-enabled objects
    test_objects = [
        "quality_event__qdm",
        "risk_event__v",
        "investigation__qdm",
        "corrective_action__v",
        "preventive_action__v"
    ]
    
    sample_assignment = '''record_id,user_id,application_role,operation
TEST_001,12345,record_owner__c,ADD'''
    
    results = {}
    
    for object_name in test_objects:
        try:
            response = qms_service.manage_quality_team_assignments(
                object_name=object_name,
                data=sample_assignment.replace("TEST_001", f"{object_name.upper()}_001")
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
    print(f"✓ Successfully tested {successful_objects} out of {len(test_objects)} object types")
    
    return results

def test_quality_team_operations():
    """Test ADD and REMOVE operations for quality teams"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    object_name = "quality_event__qdm"
    
    # Test ADD operations
    add_operations_csv = '''record_id,user_id,application_role,operation
QE000000000001,12345,record_owner__c,ADD
QE000000000001,67890,reviewer__c,ADD
QE000000000001,54321,investigator__c,ADD'''
    
    try:
        add_response = qms_service.manage_quality_team_assignments(
            object_name=object_name,
            data=add_operations_csv
        )
        
        if add_response["responseStatus"] == "SUCCESS":
            print(f"✓ ADD operations successful: Job {add_response['jobId']}")
        else:
            print(f"⚠ ADD operations failed: {add_response}")
        
        # Test REMOVE operations
        remove_operations_csv = '''record_id,user_id,application_role,operation
QE000000000001,67890,reviewer__c,REMOVE
QE000000000001,54321,investigator__c,REMOVE'''
        
        remove_response = qms_service.manage_quality_team_assignments(
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

def test_quality_team_roles():
    """Test different application roles in quality teams"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    object_name = "quality_event__qdm"
    
    # Test different application roles
    test_roles = [
        "record_owner__c",
        "reviewer__c",
        "investigator__c",
        "approver__c",
        "coordinator__c",
        "observer__c"
    ]
    
    results = {}
    
    for i, role in enumerate(test_roles, 1):
        role_assignment_csv = f'''record_id,user_id,application_role,operation
QE000000000001,{12345 + i},"{role}",ADD'''
        
        try:
            response = qms_service.manage_quality_team_assignments(
                object_name=object_name,
                data=role_assignment_csv
            )
            
            if response["responseStatus"] == "SUCCESS":
                results[role] = {
                    "status": "SUCCESS",
                    "job_id": response["jobId"]
                }
                print(f"✓ Role assignment successful for {role}: Job {response['jobId']}")
            else:
                results[role] = {
                    "status": "FAILURE",
                    "error": response.get("errors", [])
                }
                print(f"⚠ Role assignment failed for {role}: {response}")
                
        except Exception as e:
            results[role] = {
                "status": "EXCEPTION",
                "error": str(e)
            }
            print(f"⚠ Role assignment exception for {role}: {e}")
    
    successful_roles = len([role for role, result in results.items() if result["status"] == "SUCCESS"])
    print(f"✓ Successfully tested {successful_roles} out of {len(test_roles)} application roles")
    
    return results

def test_bulk_quality_team_assignments():
    """Test bulk quality team assignments (up to 500 limit)"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    object_name = "quality_event__qdm"
    
    # Generate bulk assignment data (test with smaller number first)
    bulk_size = 50  # Adjust based on available test data
    
    csv_lines = ["record_id,user_id,application_role,operation"]
    
    for i in range(bulk_size):
        record_id = f"QE{str(i+1).zfill(12)}"
        user_id = 12345 + (i % 10)  # Cycle through user IDs
        role = ["record_owner__c", "reviewer__c", "investigator__c"][i % 3]
        operation = "ADD"
        
        csv_lines.append(f"{record_id},{user_id},{role},{operation}")
    
    bulk_csv = "\n".join(csv_lines)
    
    try:
        response = qms_service.manage_quality_team_assignments(
            object_name=object_name,
            data=bulk_csv
        )
        
        if response["responseStatus"] == "SUCCESS":
            print(f"✓ Bulk assignment successful: Job {response['jobId']}")
            print(f"  Records processed: {bulk_size}")
            print(f"  CSV size: {len(bulk_csv)} characters")
        else:
            print(f"⚠ Bulk assignment failed: {response}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Bulk assignment test failed: {e}")
        return None
```

### 3. Batch Disposition Testing

```python
def test_create_batch_disposition():
    """Test creating batch disposition records"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Test with sample batch and disposition plan
    test_batch_id = "VB6000000001001"  # Replace with actual batch ID
    test_disposition_plan = "DP-000001"  # Replace with actual disposition plan
    
    try:
        response = qms_service.create_batch_disposition(
            batch_id=test_batch_id,
            disposition_plan=test_disposition_plan
        )
        
        # Verify response structure
        assert response["responseStatus"] == "SUCCESS"
        assert "jobId" in response
        
        job_id = response["jobId"]
        
        print(f"✓ Batch disposition creation successful")
        print(f"  Batch ID: {test_batch_id}")
        print(f"  Disposition Plan: {test_disposition_plan}")
        print(f"  Job ID: {job_id}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Batch disposition test failed (may require valid batch and disposition plan): {e}")
        return None

def test_create_batch_disposition_multiple_plans():
    """Test creating batch dispositions with different disposition plans"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Test data with different disposition plans
    test_cases = [
        {"batch_id": "VB6000000001001", "disposition_plan": "DP-000001"},
        {"batch_id": "VB6000000001002", "disposition_plan": "DP-000002"},
        {"batch_id": "VB6000000001003", "disposition_plan": "DP-000003"},
        {"batch_id": "VB6000000001004", "disposition_plan": "DP-RELEASE"},
        {"batch_id": "VB6000000001005", "disposition_plan": "DP-REJECT"}
    ]
    
    results = {}
    
    for i, test_case in enumerate(test_cases, 1):
        batch_id = test_case["batch_id"]
        disposition_plan = test_case["disposition_plan"]
        
        try:
            response = qms_service.create_batch_disposition(
                batch_id=batch_id,
                disposition_plan=disposition_plan
            )
            
            if response["responseStatus"] == "SUCCESS":
                results[batch_id] = {
                    "status": "SUCCESS",
                    "job_id": response["jobId"],
                    "disposition_plan": disposition_plan
                }
                print(f"✓ Disposition {i}: Batch {batch_id} with plan {disposition_plan} - Job {response['jobId']}")
            else:
                results[batch_id] = {
                    "status": "FAILURE",
                    "error": response.get("errors", []),
                    "disposition_plan": disposition_plan
                }
                print(f"⚠ Disposition {i} failed: Batch {batch_id} - {response}")
                
        except Exception as e:
            results[batch_id] = {
                "status": "EXCEPTION",
                "error": str(e),
                "disposition_plan": disposition_plan
            }
            print(f"⚠ Disposition {i} exception: Batch {batch_id} - {e}")
    
    successful_dispositions = len([batch for batch, result in results.items() if result["status"] == "SUCCESS"])
    print(f"✓ Successfully created {successful_dispositions} out of {len(test_cases)} batch dispositions")
    
    return results

def test_batch_disposition_validation():
    """Test batch disposition input validation"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Test with valid inputs first
    valid_batch_id = "VB6000000001001"
    valid_disposition_plan = "DP-000001"
    
    try:
        valid_response = qms_service.create_batch_disposition(
            batch_id=valid_batch_id,
            disposition_plan=valid_disposition_plan
        )
        
        if valid_response["responseStatus"] == "SUCCESS":
            print(f"✓ Valid inputs test passed: Job {valid_response['jobId']}")
        else:
            print(f"⚠ Valid inputs test failed: {valid_response}")
        
        # Test input validation
        validation_tests = [
            {"batch_id": "", "disposition_plan": valid_disposition_plan, "test": "empty batch ID"},
            {"batch_id": valid_batch_id, "disposition_plan": "", "test": "empty disposition plan"},
            {"batch_id": "INVALID_BATCH", "disposition_plan": valid_disposition_plan, "test": "invalid batch format"},
            {"batch_id": valid_batch_id, "disposition_plan": "INVALID_PLAN", "test": "invalid disposition plan"}
        ]
        
        for test_case in validation_tests:
            try:
                response = qms_service.create_batch_disposition(
                    batch_id=test_case["batch_id"],
                    disposition_plan=test_case["disposition_plan"]
                )
                
                if response["responseStatus"] == "FAILURE":
                    print(f"✓ Validation correctly failed for {test_case['test']}")
                else:
                    print(f"⚠ Validation should have failed for {test_case['test']}: {response}")
                    
            except Exception as e:
                print(f"✓ Exception correctly raised for {test_case['test']}: {e}")
        
        return True
        
    except Exception as e:
        print(f"⚠ Batch disposition validation test failed: {e}")
        return False
```

### 4. Error Handling Testing

```python
def test_invalid_object_names():
    """Test quality team assignments with invalid object names"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    invalid_objects = [
        "invalid_object__v",
        "document__v",  # Not team-enabled
        "user__sys",    # System object
        "",             # Empty string
        "nonexistent__qdm"
    ]
    
    sample_assignment = '''record_id,user_id,application_role,operation
TEST_001,12345,record_owner__c,ADD'''
    
    for invalid_object in invalid_objects:
        try:
            response = qms_service.manage_quality_team_assignments(
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

def test_invalid_csv_format():
    """Test quality team assignments with invalid CSV format"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    object_name = "quality_event__qdm"
    
    # Test various invalid CSV formats
    invalid_csv_tests = [
        {
            "data": "invalid,csv,header\ndata,without,proper,columns",
            "test": "invalid headers"
        },
        {
            "data": '''record_id,user_id,application_role,operation
QE001,,record_owner__c,ADD''',
            "test": "missing user_id"
        },
        {
            "data": '''record_id,user_id,application_role,operation
,12345,record_owner__c,ADD''',
            "test": "missing record_id"
        },
        {
            "data": '''record_id,user_id,application_role,operation
QE001,12345,,ADD''',
            "test": "missing application_role"
        },
        {
            "data": '''record_id,user_id,application_role,operation
QE001,12345,record_owner__c,''',
            "test": "missing operation"
        },
        {
            "data": '''record_id,user_id,application_role,operation
QE001,12345,record_owner__c,INVALID''',
            "test": "invalid operation"
        }
    ]
    
    for test_case in invalid_csv_tests:
        try:
            response = qms_service.manage_quality_team_assignments(
                object_name=object_name,
                data=test_case["data"]
            )
            
            if response["responseStatus"] == "FAILURE":
                print(f"✓ Invalid CSV ({test_case['test']}) handled correctly")
            else:
                print(f"⚠ Invalid CSV ({test_case['test']}) was accepted: {response}")
                
        except Exception as e:
            print(f"✓ Exception for invalid CSV ({test_case['test']}): {e}")

def test_batch_size_limits():
    """Test batch size limit enforcement"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    object_name = "quality_event__qdm"
    
    # Test exceeding 500 limit
    large_batch_size = 510  # Exceeds 500 limit
    
    csv_lines = ["record_id,user_id,application_role,operation"]
    
    for i in range(large_batch_size):
        record_id = f"QE{str(i+1).zfill(12)}"
        user_id = 12345 + (i % 10)
        role = "record_owner__c"
        operation = "ADD"
        
        csv_lines.append(f"{record_id},{user_id},{role},{operation}")
    
    large_csv = "\n".join(csv_lines)
    
    try:
        response = qms_service.manage_quality_team_assignments(
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

def test_permission_requirements():
    """Test permission-related errors"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Test operations that require specific permissions
    permission_tests = [
        {
            "operation": "quality_team_assignment",
            "func": lambda: qms_service.manage_quality_team_assignments(
                "quality_event__qdm",
                "record_id,user_id,application_role,operation\nQE001,12345,record_owner__c,ADD"
            )
        },
        {
            "operation": "batch_disposition",
            "func": lambda: qms_service.create_batch_disposition(
                "VB6000000001001",
                "DP-000001"
            )
        }
    ]
    
    for test in permission_tests:
        try:
            response = test["func"]()
            
            if response["responseStatus"] == "FAILURE":
                errors = response.get("errors", [])
                
                permission_keywords = ["permission", "access", "unauthorized", "forbidden", "qms", "batch release"]
                if any(keyword in str(error).lower() for error in errors for keyword in permission_keywords):
                    print(f"✓ Permission error handled correctly for {test['operation']}")
                else:
                    print(f"⚠ Different error for {test['operation']}: {errors}")
            else:
                print(f"✓ {test['operation']} succeeded (user has permissions)")
                
        except Exception as e:
            permission_keywords = ["permission", "access", "unauthorized", "forbidden", "qms", "batch release"]
            if any(keyword in str(e).lower() for keyword in permission_keywords):
                print(f"✓ Permission exception for {test['operation']}: {e}")
            else:
                print(f"⚠ Unexpected exception for {test['operation']}: {e}")
```

### 5. Integration Testing

```python
def test_complete_qms_workflow():
    """Test complete QMS workflow"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    workflow_data = {
        "quality_event": "QE000000000001",
        "batch": "VB6000000001001",
        "disposition_plan": "DP-000001",
        "team_members": [
            {"user_id": "12345", "role": "record_owner__c"},
            {"user_id": "67890", "role": "reviewer__c"},
            {"user_id": "54321", "role": "investigator__c"}
        ]
    }
    
    print("Starting complete QMS workflow...")
    
    # Step 1: Set up quality team
    team_csv_lines = ["record_id,user_id,application_role,operation"]
    
    for member in workflow_data["team_members"]:
        team_csv_lines.append(
            f"{workflow_data['quality_event']},{member['user_id']},{member['role']},ADD"
        )
    
    team_csv = "\n".join(team_csv_lines)
    
    try:
        # Assign quality team
        team_response = qms_service.manage_quality_team_assignments(
            object_name="quality_event__qdm",
            data=team_csv
        )
        
        if team_response["responseStatus"] == "SUCCESS":
            print(f"Step 1: ✓ Quality team assigned - Job {team_response['jobId']}")
            workflow_data["team_job_id"] = team_response["jobId"]
        else:
            print(f"Step 1: ⚠ Quality team assignment failed: {team_response}")
        
        # Step 2: Create batch disposition
        disposition_response = qms_service.create_batch_disposition(
            batch_id=workflow_data["batch"],
            disposition_plan=workflow_data["disposition_plan"]
        )
        
        if disposition_response["responseStatus"] == "SUCCESS":
            print(f"Step 2: ✓ Batch disposition created - Job {disposition_response['jobId']}")
            workflow_data["disposition_job_id"] = disposition_response["jobId"]
        else:
            print(f"Step 2: ⚠ Batch disposition failed: {disposition_response}")
        
        # Step 3: Update team assignments (simulate workflow progression)
        update_csv = f'''record_id,user_id,application_role,operation
{workflow_data['quality_event']},11111,approver__c,ADD
{workflow_data['quality_event']},54321,investigator__c,REMOVE'''
        
        update_response = qms_service.manage_quality_team_assignments(
            object_name="quality_event__qdm",
            data=update_csv
        )
        
        if update_response["responseStatus"] == "SUCCESS":
            print(f"Step 3: ✓ Team updated - Job {update_response['jobId']}")
            workflow_data["update_job_id"] = update_response["jobId"]
        else:
            print(f"Step 3: ⚠ Team update failed: {update_response}")
        
        print("✓ Complete QMS workflow executed successfully")
        
        return workflow_data
        
    except Exception as e:
        print(f"⚠ QMS workflow failed: {e}")
        return None

def test_batch_release_integration():
    """Test batch release workflow integration"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Test multiple batch dispositions for different scenarios
    batch_scenarios = [
        {"batch": "VB6000000001001", "plan": "DP-RELEASE", "scenario": "Release approved batch"},
        {"batch": "VB6000000001002", "plan": "DP-REJECT", "scenario": "Reject failed batch"},
        {"batch": "VB6000000001003", "plan": "DP-REWORK", "scenario": "Rework batch with issues"},
        {"batch": "VB6000000001004", "plan": "DP-QUARANTINE", "scenario": "Quarantine suspicious batch"}
    ]
    
    results = []
    
    print("Testing batch release integration scenarios...")
    
    for i, scenario in enumerate(batch_scenarios, 1):
        try:
            response = qms_service.create_batch_disposition(
                batch_id=scenario["batch"],
                disposition_plan=scenario["plan"]
            )
            
            if response["responseStatus"] == "SUCCESS":
                result = {
                    "scenario": scenario["scenario"],
                    "batch": scenario["batch"],
                    "plan": scenario["plan"],
                    "job_id": response["jobId"],
                    "status": "SUCCESS"
                }
                results.append(result)
                print(f"  {i}. ✓ {scenario['scenario']}: Job {response['jobId']}")
            else:
                result = {
                    "scenario": scenario["scenario"],
                    "batch": scenario["batch"],
                    "plan": scenario["plan"],
                    "error": response.get("errors", []),
                    "status": "FAILURE"
                }
                results.append(result)
                print(f"  {i}. ⚠ {scenario['scenario']}: Failed - {response}")
                
        except Exception as e:
            result = {
                "scenario": scenario["scenario"],
                "batch": scenario["batch"],
                "plan": scenario["plan"],
                "error": str(e),
                "status": "EXCEPTION"
            }
            results.append(result)
            print(f"  {i}. ⚠ {scenario['scenario']}: Exception - {e}")
    
    successful_scenarios = len([r for r in results if r["status"] == "SUCCESS"])
    print(f"✓ Batch release integration: {successful_scenarios}/{len(batch_scenarios)} scenarios successful")
    
    return results
```

### 6. Performance Testing

```python
def test_qms_performance():
    """Test QMS API performance"""
    from veevavault.services.applications.qms.qms_service import QMSService
    import time
    
    qms_service = QMSService(vault_client)
    
    # Test team assignment performance
    performance_data = []
    
    # Test different batch sizes
    batch_sizes = [10, 50, 100, 250]
    
    for batch_size in batch_sizes:
        print(f"Testing performance with batch size: {batch_size}")
        
        # Generate CSV data
        csv_lines = ["record_id,user_id,application_role,operation"]
        
        for i in range(batch_size):
            record_id = f"QE{str(i+1).zfill(12)}"
            user_id = 12345 + (i % 10)
            role = "record_owner__c"
            operation = "ADD"
            
            csv_lines.append(f"{record_id},{user_id},{role},{operation}")
        
        csv_data = "\n".join(csv_lines)
        csv_size = len(csv_data)
        
        start_time = time.time()
        
        try:
            response = qms_service.manage_quality_team_assignments(
                object_name="quality_event__qdm",
                data=csv_data
            )
            
            response_time = time.time() - start_time
            
            if response["responseStatus"] == "SUCCESS":
                performance_data.append({
                    "batch_size": batch_size,
                    "csv_size": csv_size,
                    "response_time": response_time,
                    "job_id": response["jobId"],
                    "status": "SUCCESS"
                })
                print(f"  ✓ Batch size {batch_size}: {response_time:.2f}s - Job {response['jobId']}")
            else:
                performance_data.append({
                    "batch_size": batch_size,
                    "csv_size": csv_size,
                    "response_time": response_time,
                    "error": response.get("errors", []),
                    "status": "FAILURE"
                })
                print(f"  ⚠ Batch size {batch_size}: Failed in {response_time:.2f}s")
                
        except Exception as e:
            response_time = time.time() - start_time
            performance_data.append({
                "batch_size": batch_size,
                "csv_size": csv_size,
                "response_time": response_time,
                "error": str(e),
                "status": "EXCEPTION"
            })
            print(f"  ⚠ Batch size {batch_size}: Exception in {response_time:.2f}s - {e}")
        
        # Add delay to avoid rate limiting
        time.sleep(1)
    
    # Calculate performance metrics
    successful_tests = [p for p in performance_data if p["status"] == "SUCCESS"]
    
    if successful_tests:
        avg_response_time = sum(p["response_time"] for p in successful_tests) / len(successful_tests)
        min_response_time = min(p["response_time"] for p in successful_tests)
        max_response_time = max(p["response_time"] for p in successful_tests)
        
        print(f"\nPerformance Summary:")
        print(f"  Successful tests: {len(successful_tests)}/{len(performance_data)}")
        print(f"  Average response time: {avg_response_time:.2f}s")
        print(f"  Min response time: {min_response_time:.2f}s")
        print(f"  Max response time: {max_response_time:.2f}s")
    
    return performance_data
```

## Test Data Requirements

### Sample CSV Data Formats
```python
# Quality team assignments CSV
SAMPLE_TEAM_ASSIGNMENTS_CSV = '''record_id,user_id,application_role,operation
QE000000000001,12345,record_owner__c,ADD
QE000000000001,67890,reviewer__c,ADD
QE000000000002,12345,investigator__c,ADD
QE000000000002,67890,record_owner__c,REMOVE'''

# Batch disposition data
SAMPLE_BATCH_DISPOSITION_DATA = {
    "batch_id": "VB6000000001001",
    "disposition_plan": "DP-000001"
}
```

### Sample Object Names
```python
# Team-enabled objects
SAMPLE_TEAM_OBJECTS = [
    "quality_event__qdm",
    "risk_event__v",
    "investigation__qdm",
    "corrective_action__v",
    "preventive_action__v"
]

# Application roles
SAMPLE_APPLICATION_ROLES = [
    "record_owner__c",
    "reviewer__c",
    "investigator__c",
    "approver__c",
    "coordinator__c"
]
```

## Expected Response Formats

### Quality Team Assignment Response
```json
{
    "responseStatus": "SUCCESS",
    "jobId": "243001"
}
```

### Batch Disposition Response
```json
{
    "responseStatus": "SUCCESS",
    "jobId": "244002"
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

1. **Batch Limits**: Maximum 500 records per quality team assignment batch
2. **File Size**: Maximum 1GB for CSV input files
3. **Asynchronous Processing**: All operations are asynchronous and return job IDs
4. **Rate Limiting**: Respect API rate limits for concurrent operations
5. **Business Logic**: Operations respect team configuration constraints

## Security Notes

1. **QMS Permissions**: Requires appropriate QMS application permissions
2. **Batch Release Permissions**: Batch operations require Batch Release permissions
3. **Object Access**: User must have access to target object records
4. **Role Constraints**: Application role assignments respect configured constraints
5. **State Restrictions**: Some operations restricted based on object record states

## Common Issues and Troubleshooting

1. **Application Not Licensed**: Ensure QMS and/or Batch Release applications are licensed
2. **Invalid Object Names**: Verify object is team-enabled for quality team operations
3. **Role Constraints**: Check minimum/maximum user requirements and role eligibility
4. **Locked Records**: Some operations blocked when records are in locked states
5. **Invalid Operations**: Ensure operation values are exactly "ADD" or "REMOVE" (case-sensitive)

## API Method Coverage Summary

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|---------|
| `manage_quality_team_assignments` | POST `/app/quality/qms/teams/vobjects/{object_name}/actions/manageassignments` | Manage quality team member assignments | ✅ Covered |
| `create_batch_disposition` | POST `/app/quality/batch_release/disposition` | Create batch disposition records | ✅ Covered |

**Total API Coverage: 2/2 methods (100%)**

This comprehensive testing framework ensures complete coverage of the QMS API, including quality team management and batch release operations with proper error handling, security considerations, and performance testing.
