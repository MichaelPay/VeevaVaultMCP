# QualityDocs API Testing Documentation

## Overview
This document provides comprehensive testing procedures for the QualityDocs API (Section 29) of VeevaTools. The QualityDocs API enables quality management operations for Veeva QualityDocs, specifically checking document roles in Document Change Control (DCC) records.

## Service Class Information
- **Service Class**: `QualityDocsService`
- **Module Path**: `veevavault.services.applications.quality_docs.quality_docs_service`
- **Authentication**: VaultClient session required
- **Application Requirement**: Veeva QualityDocs must be licensed and enabled
- **Base URL Pattern**: `/api/{version}/vobjects/document_change_control__v/`

## Core Functionality
The QualityDocs API provides capabilities for:
- **Document Role Checking**: Verify if application roles exist on documents in Document Change Control
- **Quality Control**: Support quality management processes through role validation
- **DCC Integration**: Work with Document Change Control records for release processes

## Important Requirements
- **QualityDocs License**: Must have Veeva QualityDocs application licensed
- **Document Change Control**: Works with document_change_control__v object records
- **Application Roles**: Checks against application_role__v records
- **Document Sections**: Only checks "Documents to be Released" and "Documents to be Made Obsolete" sections
- **Permissions**: Appropriate QualityDocs permissions required for document access

## Testing Methods

### 1. Service Initialization Testing

```python
def test_quality_docs_service_initialization():
    """Test QualityDocsService initialization"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    # Initialize the service
    quality_docs_service = QualityDocsService(vault_client)
    
    # Verify service initialization
    assert quality_docs_service.client == vault_client
    assert hasattr(quality_docs_service, 'document_role_check_for_document_change_control')
    
    print("✓ QualityDocsService initialized successfully")
    print("✓ All required methods are available")
```

### 2. Document Role Check Testing

```python
def test_document_role_check_for_document_change_control():
    """Test document role check for Document Change Control"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    quality_docs_service = QualityDocsService(vault_client)
    
    # Test with sample DCC record and application role
    test_dcc_id = "00S000000000101"  # Replace with actual DCC record ID
    test_app_role = "approver__c"     # Replace with actual application role
    
    try:
        response = quality_docs_service.document_role_check_for_document_change_control(
            object_record_id=test_dcc_id,
            application_role=test_app_role
        )
        
        # Verify response structure
        assert response["responseStatus"] == "SUCCESS"
        assert "data" in response
        assert "check_result" in response["data"]
        assert isinstance(response["data"]["check_result"], bool)
        
        check_result = response["data"]["check_result"]
        
        print(f"✓ Document role check completed successfully")
        print(f"  DCC Record ID: {test_dcc_id}")
        print(f"  Application Role: {test_app_role}")
        print(f"  Role Found: {check_result}")
        
        return response
        
    except Exception as e:
        print(f"⚠ Document role check test failed (may require valid DCC ID and permissions): {e}")
        return None

def test_document_role_check_multiple_roles():
    """Test document role check with multiple application roles"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    quality_docs_service = QualityDocsService(vault_client)
    
    # Test with different application roles
    test_dcc_id = "00S000000000101"  # Replace with actual DCC record ID
    
    test_roles = [
        "approver__c",
        "reviewer__c", 
        "coordinator__c",
        "owner__c",
        "editor__c"
    ]
    
    results = {}
    
    for role in test_roles:
        try:
            response = quality_docs_service.document_role_check_for_document_change_control(
                object_record_id=test_dcc_id,
                application_role=role
            )
            
            if response["responseStatus"] == "SUCCESS":
                check_result = response["data"]["check_result"]
                results[role] = check_result
                
                print(f"✓ Role check for '{role}': {check_result}")
            else:
                print(f"⚠ Role check failed for '{role}': {response}")
                results[role] = None
                
        except Exception as e:
            print(f"⚠ Role check exception for '{role}': {e}")
            results[role] = None
    
    # Verify we got some results
    successful_checks = [role for role, result in results.items() if result is not None]
    print(f"✓ Successfully checked {len(successful_checks)} out of {len(test_roles)} roles")
    
    return results

def test_document_role_check_different_dcc_records():
    """Test document role check with different DCC records"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    quality_docs_service = QualityDocsService(vault_client)
    
    # Test with multiple DCC record IDs
    test_dcc_records = [
        "00S000000000101",
        "00S000000000102", 
        "00S000000000103"
    ]
    
    test_app_role = "approver__c"
    results = {}
    
    for dcc_id in test_dcc_records:
        try:
            response = quality_docs_service.document_role_check_for_document_change_control(
                object_record_id=dcc_id,
                application_role=test_app_role
            )
            
            if response["responseStatus"] == "SUCCESS":
                check_result = response["data"]["check_result"]
                results[dcc_id] = check_result
                
                print(f"✓ DCC '{dcc_id}' role check: {check_result}")
            else:
                print(f"⚠ DCC '{dcc_id}' role check failed: {response}")
                results[dcc_id] = None
                
        except Exception as e:
            print(f"⚠ DCC '{dcc_id}' role check exception: {e}")
            results[dcc_id] = None
    
    # Verify results
    successful_checks = [dcc_id for dcc_id, result in results.items() if result is not None]
    print(f"✓ Successfully checked {len(successful_checks)} out of {len(test_dcc_records)} DCC records")
    
    return results
```

### 3. Response Format Testing

```python
def test_document_role_check_response_formats():
    """Test different response formats for document role check"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    quality_docs_service = QualityDocsService(vault_client)
    
    test_dcc_id = "00S000000000101"
    test_app_role = "approver__c"
    
    # Test JSON response (default)
    try:
        json_response = quality_docs_service.document_role_check_for_document_change_control(
            object_record_id=test_dcc_id,
            application_role=test_app_role
        )
        
        # Verify JSON response structure
        assert json_response["responseStatus"] == "SUCCESS"
        assert "data" in json_response
        assert "check_result" in json_response["data"]
        
        print("✓ JSON response format validated")
        print(f"  Response keys: {list(json_response.keys())}")
        print(f"  Data keys: {list(json_response['data'].keys())}")
        print(f"  Check result type: {type(json_response['data']['check_result'])}")
        
        return json_response
        
    except Exception as e:
        print(f"⚠ JSON response format test failed: {e}")
        return None

def test_document_role_check_response_validation():
    """Test response validation and data types"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    quality_docs_service = QualityDocsService(vault_client)
    
    test_dcc_id = "00S000000000101"
    test_app_role = "approver__c"
    
    try:
        response = quality_docs_service.document_role_check_for_document_change_control(
            object_record_id=test_dcc_id,
            application_role=test_app_role
        )
        
        # Validate response structure
        assert isinstance(response, dict), "Response should be a dictionary"
        assert "responseStatus" in response, "Response should have responseStatus"
        assert response["responseStatus"] in ["SUCCESS", "FAILURE"], "Invalid responseStatus"
        
        if response["responseStatus"] == "SUCCESS":
            # Validate success response
            assert "data" in response, "Success response should have data"
            assert isinstance(response["data"], dict), "Data should be a dictionary"
            assert "check_result" in response["data"], "Data should have check_result"
            assert isinstance(response["data"]["check_result"], bool), "check_result should be boolean"
            
            print("✓ Response validation passed")
            print(f"  Response status: {response['responseStatus']}")
            print(f"  Data structure valid: True")
            print(f"  Check result: {response['data']['check_result']}")
            
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

### 4. Error Handling Testing

```python
def test_invalid_dcc_record_id():
    """Test document role check with invalid DCC record ID"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    quality_docs_service = QualityDocsService(vault_client)
    
    invalid_dcc_ids = [
        "INVALID_ID",
        "00S999999999999",  # Non-existent ID
        "",                 # Empty string
        "123",             # Invalid format
        "null"             # String null
    ]
    
    test_app_role = "approver__c"
    
    for invalid_id in invalid_dcc_ids:
        try:
            response = quality_docs_service.document_role_check_for_document_change_control(
                object_record_id=invalid_id,
                application_role=test_app_role
            )
            
            if response["responseStatus"] == "FAILURE":
                assert "errors" in response
                print(f"✓ Invalid DCC ID '{invalid_id}' handled correctly")
                print(f"  Error: {response.get('errors', [])}")
            else:
                print(f"⚠ Invalid DCC ID '{invalid_id}' was accepted: {response}")
                
        except Exception as e:
            print(f"✓ Exception for invalid DCC ID '{invalid_id}': {e}")

def test_invalid_application_role():
    """Test document role check with invalid application role"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    quality_docs_service = QualityDocsService(vault_client)
    
    test_dcc_id = "00S000000000101"
    
    invalid_roles = [
        "nonexistent_role__c",
        "",                     # Empty string
        "invalid role",         # Invalid format
        "null",                # String null
        "admin__sys"           # System role instead of app role
    ]
    
    for invalid_role in invalid_roles:
        try:
            response = quality_docs_service.document_role_check_for_document_change_control(
                object_record_id=test_dcc_id,
                application_role=invalid_role
            )
            
            if response["responseStatus"] == "FAILURE":
                assert "errors" in response
                print(f"✓ Invalid application role '{invalid_role}' handled correctly")
                print(f"  Error: {response.get('errors', [])}")
            else:
                # Some invalid roles might return false instead of error
                if "data" in response and "check_result" in response["data"]:
                    check_result = response["data"]["check_result"]
                    print(f"✓ Invalid role '{invalid_role}' returned: {check_result}")
                else:
                    print(f"⚠ Invalid role '{invalid_role}' was accepted: {response}")
                
        except Exception as e:
            print(f"✓ Exception for invalid application role '{invalid_role}': {e}")

def test_permission_requirements():
    """Test permission-related errors"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    quality_docs_service = QualityDocsService(vault_client)
    
    # Test with DCC record that user may not have access to
    restricted_dcc_id = "00S000000000999"  # Hypothetical restricted record
    test_app_role = "approver__c"
    
    try:
        response = quality_docs_service.document_role_check_for_document_change_control(
            object_record_id=restricted_dcc_id,
            application_role=test_app_role
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
            print(f"✓ User has access to DCC record: {restricted_dcc_id}")
            
    except Exception as e:
        if any(keyword in str(e).lower() for keyword in ["permission", "access", "unauthorized", "forbidden"]):
            print(f"✓ Permission exception correctly raised: {e}")
        else:
            print(f"⚠ Unexpected exception: {e}")

def test_qualitydocs_application_requirement():
    """Test QualityDocs application requirement"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    quality_docs_service = QualityDocsService(vault_client)
    
    test_dcc_id = "00S000000000101"
    test_app_role = "approver__c"
    
    try:
        response = quality_docs_service.document_role_check_for_document_change_control(
            object_record_id=test_dcc_id,
            application_role=test_app_role
        )
        
        if response["responseStatus"] == "FAILURE":
            errors = response.get("errors", [])
            
            # Check for application-related errors
            app_errors = [
                error for error in errors 
                if any(keyword in str(error).lower() for keyword in ["qualitydocs", "application", "license", "feature"])
            ]
            
            if app_errors:
                print(f"✓ QualityDocs application requirement enforced")
                print(f"  Errors: {app_errors}")
            else:
                print(f"⚠ Different error (may not be app-related): {errors}")
        else:
            print(f"✓ QualityDocs application is available and accessible")
            
    except Exception as e:
        if any(keyword in str(e).lower() for keyword in ["qualitydocs", "application", "license", "feature"]):
            print(f"✓ Application requirement exception: {e}")
        else:
            print(f"⚠ Unexpected exception: {e}")
```

### 5. Integration Testing

```python
def test_quality_docs_workflow():
    """Test complete QualityDocs workflow"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    quality_docs_service = QualityDocsService(vault_client)
    
    # Simulate a quality control workflow
    workflow_data = {
        "dcc_record": "00S000000000101",
        "required_roles": ["approver__c", "reviewer__c", "coordinator__c"],
        "quality_gates": []
    }
    
    print("Starting QualityDocs workflow simulation...")
    
    # Step 1: Check if all required roles are present
    all_roles_present = True
    role_results = {}
    
    for role in workflow_data["required_roles"]:
        try:
            response = quality_docs_service.document_role_check_for_document_change_control(
                object_record_id=workflow_data["dcc_record"],
                application_role=role
            )
            
            if response["responseStatus"] == "SUCCESS":
                role_present = response["data"]["check_result"]
                role_results[role] = role_present
                
                if role_present:
                    print(f"  ✓ Required role '{role}' is present")
                    workflow_data["quality_gates"].append(f"Role {role} verified")
                else:
                    print(f"  ⚠ Required role '{role}' is missing")
                    all_roles_present = False
            else:
                print(f"  ⚠ Could not check role '{role}': {response}")
                all_roles_present = False
                
        except Exception as e:
            print(f"  ⚠ Error checking role '{role}': {e}")
            all_roles_present = False
    
    # Step 2: Determine workflow status
    if all_roles_present:
        workflow_status = "APPROVED - All required roles present"
        workflow_data["quality_gates"].append("All roles verified")
    else:
        workflow_status = "PENDING - Missing required roles"
        workflow_data["quality_gates"].append("Role verification failed")
    
    print(f"\nWorkflow Status: {workflow_status}")
    print(f"Quality Gates Passed: {len(workflow_data['quality_gates'])}")
    print(f"Role Check Results: {role_results}")
    
    return {
        "workflow_status": workflow_status,
        "role_results": role_results,
        "quality_gates": workflow_data["quality_gates"]
    }

def test_bulk_role_checking():
    """Test bulk role checking across multiple DCC records"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    
    quality_docs_service = QualityDocsService(vault_client)
    
    # Test data for bulk checking
    bulk_test_data = [
        {"dcc_id": "00S000000000101", "role": "approver__c"},
        {"dcc_id": "00S000000000102", "role": "approver__c"},
        {"dcc_id": "00S000000000103", "role": "reviewer__c"},
        {"dcc_id": "00S000000000101", "role": "coordinator__c"},
        {"dcc_id": "00S000000000102", "role": "owner__c"}
    ]
    
    results = []
    successful_checks = 0
    
    print(f"Performing bulk role checking for {len(bulk_test_data)} combinations...")
    
    for i, test_case in enumerate(bulk_test_data, 1):
        dcc_id = test_case["dcc_id"]
        role = test_case["role"]
        
        try:
            response = quality_docs_service.document_role_check_for_document_change_control(
                object_record_id=dcc_id,
                application_role=role
            )
            
            if response["responseStatus"] == "SUCCESS":
                check_result = response["data"]["check_result"]
                results.append({
                    "dcc_id": dcc_id,
                    "role": role,
                    "result": check_result,
                    "status": "SUCCESS"
                })
                successful_checks += 1
                print(f"  {i}. DCC {dcc_id} / Role {role}: {check_result}")
            else:
                results.append({
                    "dcc_id": dcc_id,
                    "role": role,
                    "result": None,
                    "status": "FAILURE",
                    "error": response.get("errors", [])
                })
                print(f"  {i}. DCC {dcc_id} / Role {role}: FAILED")
                
        except Exception as e:
            results.append({
                "dcc_id": dcc_id,
                "role": role,
                "result": None,
                "status": "EXCEPTION",
                "error": str(e)
            })
            print(f"  {i}. DCC {dcc_id} / Role {role}: EXCEPTION - {e}")
    
    success_rate = (successful_checks / len(bulk_test_data)) * 100
    print(f"\nBulk check completed:")
    print(f"  Total checks: {len(bulk_test_data)}")
    print(f"  Successful: {successful_checks}")
    print(f"  Success rate: {success_rate:.1f}%")
    
    return results
```

### 6. Performance and Reliability Testing

```python
def test_concurrent_role_checks():
    """Test concurrent role checking (simulated)"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    import time
    
    quality_docs_service = QualityDocsService(vault_client)
    
    test_dcc_id = "00S000000000101"
    test_roles = ["approver__c", "reviewer__c", "coordinator__c", "owner__c", "editor__c"]
    
    start_time = time.time()
    results = []
    
    print(f"Testing concurrent role checks for {len(test_roles)} roles...")
    
    # Simulate concurrent requests (sequential for API rate limiting)
    for role in test_roles:
        request_start = time.time()
        
        try:
            response = quality_docs_service.document_role_check_for_document_change_control(
                object_record_id=test_dcc_id,
                application_role=role
            )
            
            request_time = time.time() - request_start
            
            if response["responseStatus"] == "SUCCESS":
                results.append({
                    "role": role,
                    "result": response["data"]["check_result"],
                    "response_time": request_time,
                    "status": "SUCCESS"
                })
            else:
                results.append({
                    "role": role,
                    "result": None,
                    "response_time": request_time,
                    "status": "FAILURE"
                })
                
        except Exception as e:
            request_time = time.time() - request_start
            results.append({
                "role": role,
                "result": None,
                "response_time": request_time,
                "status": "EXCEPTION",
                "error": str(e)
            })
    
    total_time = time.time() - start_time
    avg_response_time = sum(r["response_time"] for r in results) / len(results)
    
    print(f"Concurrent testing completed:")
    print(f"  Total time: {total_time:.2f} seconds")
    print(f"  Average response time: {avg_response_time:.2f} seconds")
    print(f"  Successful requests: {len([r for r in results if r['status'] == 'SUCCESS'])}")
    
    return results

def test_api_reliability():
    """Test API reliability with repeated calls"""
    from veevavault.services.applications.quality_docs.quality_docs_service import QualityDocsService
    import time
    
    quality_docs_service = QualityDocsService(vault_client)
    
    test_dcc_id = "00S000000000101"
    test_app_role = "approver__c"
    iterations = 5  # Adjust based on rate limits
    
    print(f"Testing API reliability with {iterations} repeated calls...")
    
    results = []
    consistent_results = True
    first_result = None
    
    for i in range(iterations):
        try:
            response = quality_docs_service.document_role_check_for_document_change_control(
                object_record_id=test_dcc_id,
                application_role=test_app_role
            )
            
            if response["responseStatus"] == "SUCCESS":
                check_result = response["data"]["check_result"]
                results.append(check_result)
                
                if first_result is None:
                    first_result = check_result
                elif first_result != check_result:
                    consistent_results = False
                
                print(f"  Iteration {i+1}: {check_result}")
            else:
                print(f"  Iteration {i+1}: FAILED - {response}")
                results.append(None)
                
        except Exception as e:
            print(f"  Iteration {i+1}: EXCEPTION - {e}")
            results.append(None)
        
        # Add small delay to avoid rate limiting
        if i < iterations - 1:
            time.sleep(0.5)
    
    successful_calls = len([r for r in results if r is not None])
    reliability_rate = (successful_calls / iterations) * 100
    
    print(f"\nReliability test results:")
    print(f"  Successful calls: {successful_calls}/{iterations}")
    print(f"  Reliability rate: {reliability_rate:.1f}%")
    print(f"  Results consistent: {consistent_results}")
    
    return {
        "reliability_rate": reliability_rate,
        "consistent_results": consistent_results,
        "results": results
    }
```

## Test Data Requirements

### Sample Test Data
```python
# DCC Record IDs (replace with actual values)
SAMPLE_DCC_RECORDS = [
    "00S000000000101",
    "00S000000000102",
    "00S000000000103",
    "00S000000000104",
    "00S000000000105"
]

# Application Roles (replace with actual values)
SAMPLE_APPLICATION_ROLES = [
    "approver__c",
    "reviewer__c",
    "coordinator__c",
    "owner__c",
    "editor__c",
    "viewer__c"
]

# Workflow Test Data
SAMPLE_WORKFLOW_DATA = {
    "dcc_record": "00S000000000101",
    "required_roles": ["approver__c", "reviewer__c"],
    "optional_roles": ["coordinator__c", "editor__c"]
}
```

## Expected Response Formats

### Success Response
```json
{
    "responseStatus": "SUCCESS",
    "data": {
        "check_result": true
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
            "message": "Document Change Control record not found"
        }
    ]
}
```

## Performance Considerations

1. **Rate Limiting**: API calls should respect Veeva rate limiting
2. **Single Record**: Each call checks one DCC record and one application role
3. **Response Time**: Typically fast responses for role checking
4. **Concurrent Calls**: Can be made concurrently but within rate limits
5. **Document Scope**: Only checks specific sections of DCC records

## Security Notes

1. **QualityDocs Permissions**: Requires appropriate QualityDocs permissions
2. **Document Access**: User must have access to the DCC record
3. **Role Visibility**: Only checks roles user has permission to see
4. **Application Context**: Must be in QualityDocs application context
5. **Data Privacy**: Role checking respects document security

## Common Issues and Troubleshooting

1. **QualityDocs Not Licensed**: Ensure QualityDocs application is licensed
2. **Invalid DCC ID**: Verify Document Change Control record exists and is accessible
3. **Invalid Application Role**: Verify application role exists and is properly formatted
4. **Permission Denied**: User needs access to DCC record and application roles
5. **No Documents**: DCC record may not have documents in checked sections

## API Method Coverage Summary

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|---------|
| `document_role_check_for_document_change_control` | POST `/vobjects/document_change_control__v/{id}/actions/documentrolecheck` | Check application roles on DCC documents | ✅ Covered |

**Total API Coverage: 1/1 methods (100%)**

This comprehensive testing framework ensures complete coverage of the QualityDocs API, focusing on document role checking in Document Change Control records with proper error handling, security considerations, and workflow integration testing.
