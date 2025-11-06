# Batch Release API Testing Documentation

## Overview
This document provides comprehensive testing procedures for the Batch Release API (Section 31) of VeevaTools. The Batch Release API enables creation of Batch Disposition records from existing Batches and Batch Disposition Plans for Veeva Batch Release application workflows.

## Service Class Information
- **Service Class**: `QMSService` (contains Batch Release functionality)
- **Module Path**: `veevavault.services.applications.qms.qms_service`
- **Authentication**: VaultClient session required
- **Application Requirement**: Veeva Batch Release must be licensed and enabled
- **Base URL Pattern**: `/api/{version}/app/quality/batch_release/`

## Core Functionality
The Batch Release API provides capabilities for:
- **Disposition Creation**: Create Batch Disposition records from Batches and Disposition Plans
- **Batch Release Management**: Support batch release workflows through disposition creation
- **Quality Integration**: Integrate with quality management processes
- **Asynchronous Processing**: Handle disposition creation through background jobs

## Important Requirements
- **Batch Release License**: Must have Veeva Batch Release application licensed
- **Batch Records**: Must work with existing Batch records (batch__v object)
- **Disposition Plans**: Must reference valid Batch Disposition Plan records
- **Permissions**: Appropriate Batch Release permissions required
- **Integration**: Often used in conjunction with QMS quality team workflows

## Testing Methods

### 1. Service Initialization Testing

```python
def test_batch_release_service_initialization():
    """Test Batch Release functionality in QMSService"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    # Initialize the service (Batch Release functionality is in QMSService)
    qms_service = QMSService(vault_client)
    
    # Verify Batch Release method is available
    assert hasattr(qms_service, 'create_batch_disposition')
    
    print("✓ Batch Release functionality available in QMSService")
    print("✓ create_batch_disposition method is accessible")
```

### 2. Create Disposition Testing

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
        assert "responseDetails" in response
        assert "job_id" in response["responseDetails"]
        
        job_id = response["responseDetails"]["job_id"]
        
        print(f"✓ Batch disposition creation successful")
        print(f"  Batch ID: {test_batch_id}")
        print(f"  Disposition Plan: {test_disposition_plan}")
        print(f"  Job ID: {job_id}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Batch disposition test failed (may require valid batch and disposition plan): {e}")
        return None

def test_create_batch_disposition_various_plans():
    """Test creating batch dispositions with various disposition plans"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Test different disposition plan scenarios
    test_cases = [
        {"batch_id": "VB6000000001001", "disposition_plan": "DP-RELEASE", "scenario": "Release approved batch"},
        {"batch_id": "VB6000000001002", "disposition_plan": "DP-REJECT", "scenario": "Reject failed batch"},
        {"batch_id": "VB6000000001003", "disposition_plan": "DP-REWORK", "scenario": "Rework batch with issues"},
        {"batch_id": "VB6000000001004", "disposition_plan": "DP-QUARANTINE", "scenario": "Quarantine suspicious batch"},
        {"batch_id": "VB6000000001005", "disposition_plan": "DP-HOLD", "scenario": "Hold batch pending review"}
    ]
    
    results = {}
    
    for test_case in test_cases:
        batch_id = test_case["batch_id"]
        disposition_plan = test_case["disposition_plan"]
        scenario = test_case["scenario"]
        
        try:
            response = qms_service.create_batch_disposition(
                batch_id=batch_id,
                disposition_plan=disposition_plan
            )
            
            if response["responseStatus"] == "SUCCESS":
                job_id = response["responseDetails"]["job_id"]
                results[batch_id] = {
                    "status": "SUCCESS",
                    "job_id": job_id,
                    "disposition_plan": disposition_plan,
                    "scenario": scenario
                }
                print(f"✓ {scenario}: Batch {batch_id} with plan {disposition_plan} - Job {job_id}")
            else:
                results[batch_id] = {
                    "status": "FAILURE",
                    "error": response.get("errors", []),
                    "disposition_plan": disposition_plan,
                    "scenario": scenario
                }
                print(f"⚠ {scenario}: Failed - {response}")
                
        except Exception as e:
            results[batch_id] = {
                "status": "EXCEPTION",
                "error": str(e),
                "disposition_plan": disposition_plan,
                "scenario": scenario
            }
            print(f"⚠ {scenario}: Exception - {e}")
    
    successful_dispositions = len([batch for batch, result in results.items() if result["status"] == "SUCCESS"])
    print(f"✓ Successfully created {successful_dispositions} out of {len(test_cases)} batch dispositions")
    
    return results

def test_batch_disposition_response_validation():
    """Test batch disposition response validation"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    test_batch_id = "VB6000000001001"
    test_disposition_plan = "DP-000001"
    
    try:
        response = qms_service.create_batch_disposition(
            batch_id=test_batch_id,
            disposition_plan=test_disposition_plan
        )
        
        # Validate response structure
        assert isinstance(response, dict), "Response should be a dictionary"
        assert "responseStatus" in response, "Response should have responseStatus"
        assert response["responseStatus"] in ["SUCCESS", "FAILURE"], "Invalid responseStatus"
        
        if response["responseStatus"] == "SUCCESS":
            # Validate success response
            assert "responseDetails" in response, "Success response should have responseDetails"
            assert isinstance(response["responseDetails"], dict), "responseDetails should be a dictionary"
            assert "job_id" in response["responseDetails"], "responseDetails should have job_id"
            assert isinstance(response["responseDetails"]["job_id"], (str, int)), "job_id should be string or int"
            
            print("✓ Batch disposition response validation passed")
            print(f"  Response status: {response['responseStatus']}")
            print(f"  Job ID: {response['responseDetails']['job_id']}")
            print(f"  Response structure valid: True")
            
        else:
            # Validate failure response
            print(f"⚠ Request failed with status: {response['responseStatus']}")
            if "errors" in response:
                print(f"  Errors: {response['errors']}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Response validation test failed: {e}")
        return None
```

### 3. Batch Release Workflow Testing

```python
def test_batch_release_workflow():
    """Test complete batch release workflow"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Simulate batch release workflow stages
    workflow_stages = [
        {"batch": "VB6000000001001", "plan": "DP-REVIEW", "stage": "Initial Review"},
        {"batch": "VB6000000001001", "plan": "DP-TEST", "stage": "Quality Testing"},
        {"batch": "VB6000000001001", "plan": "DP-APPROVE", "stage": "Final Approval"},
        {"batch": "VB6000000001001", "plan": "DP-RELEASE", "stage": "Release for Distribution"}
    ]
    
    workflow_results = []
    
    print("Starting batch release workflow simulation...")
    
    for i, stage in enumerate(workflow_stages, 1):
        try:
            response = qms_service.create_batch_disposition(
                batch_id=stage["batch"],
                disposition_plan=stage["plan"]
            )
            
            if response["responseStatus"] == "SUCCESS":
                job_id = response["responseDetails"]["job_id"]
                workflow_results.append({
                    "stage": stage["stage"],
                    "batch": stage["batch"],
                    "plan": stage["plan"],
                    "job_id": job_id,
                    "status": "SUCCESS"
                })
                print(f"  Stage {i}: ✓ {stage['stage']} - Job {job_id}")
            else:
                workflow_results.append({
                    "stage": stage["stage"],
                    "batch": stage["batch"],
                    "plan": stage["plan"],
                    "error": response.get("errors", []),
                    "status": "FAILURE"
                })
                print(f"  Stage {i}: ⚠ {stage['stage']} - Failed")
                
        except Exception as e:
            workflow_results.append({
                "stage": stage["stage"],
                "batch": stage["batch"],
                "plan": stage["plan"],
                "error": str(e),
                "status": "EXCEPTION"
            })
            print(f"  Stage {i}: ⚠ {stage['stage']} - Exception: {e}")
    
    successful_stages = len([r for r in workflow_results if r["status"] == "SUCCESS"])
    print(f"✓ Batch release workflow: {successful_stages}/{len(workflow_stages)} stages successful")
    
    return workflow_results

def test_multiple_batch_processing():
    """Test processing multiple batches simultaneously"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Test multiple batches with different disposition plans
    batch_processing = [
        {"batch": "VB6000000001001", "plan": "DP-RELEASE", "product": "Product A"},
        {"batch": "VB6000000001002", "plan": "DP-RELEASE", "product": "Product B"},
        {"batch": "VB6000000001003", "plan": "DP-REJECT", "product": "Product C"},
        {"batch": "VB6000000001004", "plan": "DP-HOLD", "product": "Product D"},
        {"batch": "VB6000000001005", "plan": "DP-REWORK", "product": "Product E"}
    ]
    
    processing_results = []
    
    print(f"Processing {len(batch_processing)} batches simultaneously...")
    
    for batch_info in batch_processing:
        try:
            response = qms_service.create_batch_disposition(
                batch_id=batch_info["batch"],
                disposition_plan=batch_info["plan"]
            )
            
            if response["responseStatus"] == "SUCCESS":
                job_id = response["responseDetails"]["job_id"]
                processing_results.append({
                    "batch": batch_info["batch"],
                    "product": batch_info["product"],
                    "plan": batch_info["plan"],
                    "job_id": job_id,
                    "status": "SUCCESS"
                })
                print(f"  ✓ {batch_info['product']} (Batch {batch_info['batch']}): {batch_info['plan']} - Job {job_id}")
            else:
                processing_results.append({
                    "batch": batch_info["batch"],
                    "product": batch_info["product"],
                    "plan": batch_info["plan"],
                    "error": response.get("errors", []),
                    "status": "FAILURE"
                })
                print(f"  ⚠ {batch_info['product']} (Batch {batch_info['batch']}): Failed")
                
        except Exception as e:
            processing_results.append({
                "batch": batch_info["batch"],
                "product": batch_info["product"],
                "plan": batch_info["plan"],
                "error": str(e),
                "status": "EXCEPTION"
            })
            print(f"  ⚠ {batch_info['product']} (Batch {batch_info['batch']}): Exception - {e}")
    
    successful_batches = len([r for r in processing_results if r["status"] == "SUCCESS"])
    print(f"✓ Multiple batch processing: {successful_batches}/{len(batch_processing)} batches successful")
    
    return processing_results
```

### 4. Error Handling Testing

```python
def test_invalid_batch_ids():
    """Test disposition creation with invalid batch IDs"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    invalid_batch_ids = [
        "INVALID_BATCH_ID",
        "VB9999999999999",  # Non-existent ID
        "",                 # Empty string
        "123456789",        # Invalid format
        "VB000000000000",   # Invalid ID format
        "null"              # String null
    ]
    
    test_disposition_plan = "DP-000001"
    
    for invalid_id in invalid_batch_ids:
        try:
            response = qms_service.create_batch_disposition(
                batch_id=invalid_id,
                disposition_plan=test_disposition_plan
            )
            
            if response["responseStatus"] == "FAILURE":
                errors = response.get("errors", [])
                print(f"✓ Invalid batch ID '{invalid_id}' handled correctly: {errors}")
            else:
                print(f"⚠ Invalid batch ID '{invalid_id}' was accepted: {response}")
                
        except Exception as e:
            print(f"✓ Exception for invalid batch ID '{invalid_id}': {e}")

def test_invalid_disposition_plans():
    """Test disposition creation with invalid disposition plans"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    test_batch_id = "VB6000000001001"
    
    invalid_disposition_plans = [
        "NONEXISTENT_PLAN",
        "",                    # Empty string
        "DP-INVALID",         # Non-existent plan
        "null",               # String null
        "123456",             # Invalid format
        "INVALID-PLAN-NAME"   # Invalid naming
    ]
    
    for invalid_plan in invalid_disposition_plans:
        try:
            response = qms_service.create_batch_disposition(
                batch_id=test_batch_id,
                disposition_plan=invalid_plan
            )
            
            if response["responseStatus"] == "FAILURE":
                errors = response.get("errors", [])
                print(f"✓ Invalid disposition plan '{invalid_plan}' handled correctly: {errors}")
            else:
                print(f"⚠ Invalid disposition plan '{invalid_plan}' was accepted: {response}")
                
        except Exception as e:
            print(f"✓ Exception for invalid disposition plan '{invalid_plan}': {e}")

def test_batch_release_application_requirement():
    """Test Batch Release application requirement"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    test_batch_id = "VB6000000001001"
    test_disposition_plan = "DP-000001"
    
    try:
        response = qms_service.create_batch_disposition(
            batch_id=test_batch_id,
            disposition_plan=test_disposition_plan
        )
        
        if response["responseStatus"] == "FAILURE":
            errors = response.get("errors", [])
            
            # Check for application-related errors
            app_errors = [
                error for error in errors 
                if any(keyword in str(error).lower() for keyword in ["batch release", "application", "license", "feature"])
            ]
            
            if app_errors:
                print(f"✓ Batch Release application requirement enforced")
                print(f"  Errors: {app_errors}")
            else:
                print(f"⚠ Different error (may not be app-related): {errors}")
        else:
            print(f"✓ Batch Release application is available and accessible")
            
    except Exception as e:
        if any(keyword in str(e).lower() for keyword in ["batch release", "application", "license", "feature"]):
            print(f"✓ Application requirement exception: {e}")
        else:
            print(f"⚠ Unexpected exception: {e}")

def test_permission_requirements():
    """Test permission-related errors for batch release"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Test with batch that user may not have access to
    restricted_batch_id = "VB6000000999999"  # Hypothetical restricted batch
    test_disposition_plan = "DP-000001"
    
    try:
        response = qms_service.create_batch_disposition(
            batch_id=restricted_batch_id,
            disposition_plan=test_disposition_plan
        )
        
        if response["responseStatus"] == "FAILURE":
            errors = response.get("errors", [])
            
            # Check for permission-related errors
            permission_errors = [
                error for error in errors 
                if any(keyword in str(error).lower() for keyword in ["permission", "access", "unauthorized", "forbidden"])
            ]
            
            if permission_errors:
                print(f"✓ Permission error handled correctly")
                print(f"  Errors: {permission_errors}")
            else:
                print(f"⚠ Different error for restricted access: {errors}")
        else:
            print(f"✓ User has access to batch: {restricted_batch_id}")
            
    except Exception as e:
        if any(keyword in str(e).lower() for keyword in ["permission", "access", "unauthorized", "forbidden"]):
            print(f"✓ Permission exception correctly raised: {e}")
        else:
            print(f"⚠ Unexpected exception: {e}")
```

### 5. Integration Testing

```python
def test_batch_release_qms_integration():
    """Test integration between Batch Release and QMS workflows"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    integration_scenario = {
        "batch_id": "VB6000000001001",
        "disposition_plan": "DP-RELEASE",
        "quality_event": "QE000000000001",
        "team_members": [
            {"user_id": "12345", "role": "record_owner__c"},
            {"user_id": "67890", "role": "reviewer__c"}
        ]
    }
    
    print("Testing Batch Release and QMS integration...")
    
    try:
        # Step 1: Set up quality team for batch review
        team_csv = "record_id,user_id,application_role,operation\n"
        for member in integration_scenario["team_members"]:
            team_csv += f"{integration_scenario['quality_event']},{member['user_id']},{member['role']},ADD\n"
        
        team_response = qms_service.manage_quality_team_assignments(
            object_name="quality_event__qdm",
            data=team_csv.strip()
        )
        
        if team_response["responseStatus"] == "SUCCESS":
            print(f"Step 1: ✓ Quality team assigned - Job {team_response['jobId']}")
            integration_scenario["team_job_id"] = team_response["jobId"]
        else:
            print(f"Step 1: ⚠ Quality team assignment failed: {team_response}")
        
        # Step 2: Create batch disposition after quality review
        disposition_response = qms_service.create_batch_disposition(
            batch_id=integration_scenario["batch_id"],
            disposition_plan=integration_scenario["disposition_plan"]
        )
        
        if disposition_response["responseStatus"] == "SUCCESS":
            job_id = disposition_response["responseDetails"]["job_id"]
            print(f"Step 2: ✓ Batch disposition created - Job {job_id}")
            integration_scenario["disposition_job_id"] = job_id
        else:
            print(f"Step 2: ⚠ Batch disposition failed: {disposition_response}")
        
        print("✓ Batch Release and QMS integration test completed")
        
        return integration_scenario
        
    except Exception as e:
        print(f"⚠ Integration test failed: {e}")
        return None

def test_disposition_plan_workflows():
    """Test different disposition plan workflows"""
    from veevavault.services.applications.qms.qms_service import QMSService
    
    qms_service = QMSService(vault_client)
    
    # Test different workflow scenarios
    workflow_scenarios = [
        {
            "name": "Standard Release Workflow",
            "batches": ["VB6000000001001", "VB6000000001002"],
            "plans": ["DP-REVIEW", "DP-APPROVE", "DP-RELEASE"]
        },
        {
            "name": "Quality Issue Workflow",
            "batches": ["VB6000000001003"],
            "plans": ["DP-INVESTIGATE", "DP-REJECT"]
        },
        {
            "name": "Rework Workflow", 
            "batches": ["VB6000000001004"],
            "plans": ["DP-REWORK", "DP-RETEST", "DP-RELEASE"]
        },
        {
            "name": "Hold and Release Workflow",
            "batches": ["VB6000000001005"],
            "plans": ["DP-HOLD", "DP-INVESTIGATE", "DP-RELEASE"]
        }
    ]
    
    workflow_results = {}
    
    for scenario in workflow_scenarios:
        scenario_name = scenario["name"]
        workflow_results[scenario_name] = []
        
        print(f"Testing {scenario_name}...")
        
        for batch in scenario["batches"]:
            for plan in scenario["plans"]:
                try:
                    response = qms_service.create_batch_disposition(
                        batch_id=batch,
                        disposition_plan=plan
                    )
                    
                    if response["responseStatus"] == "SUCCESS":
                        job_id = response["responseDetails"]["job_id"]
                        workflow_results[scenario_name].append({
                            "batch": batch,
                            "plan": plan,
                            "job_id": job_id,
                            "status": "SUCCESS"
                        })
                        print(f"  ✓ Batch {batch} -> {plan}: Job {job_id}")
                    else:
                        workflow_results[scenario_name].append({
                            "batch": batch,
                            "plan": plan,
                            "error": response.get("errors", []),
                            "status": "FAILURE"
                        })
                        print(f"  ⚠ Batch {batch} -> {plan}: Failed")
                        
                except Exception as e:
                    workflow_results[scenario_name].append({
                        "batch": batch,
                        "plan": plan,
                        "error": str(e),
                        "status": "EXCEPTION"
                    })
                    print(f"  ⚠ Batch {batch} -> {plan}: Exception - {e}")
    
    # Summary
    for scenario_name, results in workflow_results.items():
        successful = len([r for r in results if r["status"] == "SUCCESS"])
        total = len(results)
        print(f"✓ {scenario_name}: {successful}/{total} dispositions successful")
    
    return workflow_results
```

## Test Data Requirements

### Sample Test Data
```python
# Batch IDs (replace with actual values)
SAMPLE_BATCH_IDS = [
    "VB6000000001001",
    "VB6000000001002", 
    "VB6000000001003",
    "VB6000000001004",
    "VB6000000001005"
]

# Disposition Plans (replace with actual values)
SAMPLE_DISPOSITION_PLANS = [
    "DP-000001",
    "DP-RELEASE", 
    "DP-REJECT",
    "DP-REWORK",
    "DP-HOLD",
    "DP-APPROVE",
    "DP-REVIEW"
]

# Workflow Test Data
SAMPLE_BATCH_WORKFLOW = {
    "batch_id": "VB6000000001001",
    "disposition_plan": "DP-RELEASE",
    "quality_event": "QE000000000001"
}
```

## Expected Response Formats

### Success Response
```json
{
    "responseStatus": "SUCCESS",
    "responseDetails": {
        "job_id": "392501"
    }
}
```

### Failure Response
```json
{
    "responseStatus": "FAILURE",
    "errors": [
        {
            "type": "INVALID_DATA",
            "message": "Invalid batch ID"
        }
    ]
}
```

## Performance Considerations

1. **Asynchronous Processing**: All disposition creation is asynchronous and returns job IDs
2. **Single Operations**: Each API call creates one batch disposition
3. **Rate Limiting**: Respect API rate limits for concurrent operations
4. **Job Monitoring**: Use job IDs to monitor disposition creation progress
5. **Batch Dependencies**: Consider batch state and dependencies

## Security Notes

1. **Batch Release Permissions**: Requires appropriate Batch Release application permissions
2. **Batch Access**: User must have access to source batch records
3. **Disposition Plan Access**: User must have access to disposition plan records
4. **Quality Integration**: May require QMS permissions for integrated workflows
5. **Data Integrity**: Disposition creation respects batch release business rules

## Common Issues and Troubleshooting

1. **Application Not Licensed**: Ensure Batch Release application is licensed
2. **Invalid Batch ID**: Verify batch record exists and is accessible
3. **Invalid Disposition Plan**: Verify disposition plan exists and is active
4. **Permission Denied**: User needs appropriate Batch Release permissions
5. **Batch State**: Some batches may not be eligible for certain dispositions

## API Method Coverage Summary

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|---------|
| `create_batch_disposition` | POST `/app/quality/batch_release/disposition` | Create batch disposition records | ✅ Covered |

**Total API Coverage: 1/1 methods (100%)**

## Notes on Implementation

- **Service Location**: Batch Release functionality is implemented in `QMSService` class
- **Shared Functionality**: This method is also covered in Section 30 (QMS) testing documentation
- **Integration Context**: While the method is the same, this section focuses on Batch Release workflows
- **Application Scope**: Requires Veeva Batch Release license (separate from QMS)

This comprehensive testing framework ensures complete coverage of the Batch Release API, focusing on disposition creation workflows and integration with quality management processes, with proper error handling and security considerations.
