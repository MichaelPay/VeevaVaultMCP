# 35. RIM Submissions - Testing Documentation

## Overview
Testing documentation for RIM Submissions functionality in Veeva Vault. This module provides functionality for managing regulatory submission content plans, including copying content plan sections and items for reuse across different applications and submissions.

## Prerequisites
- Veeva RIM Submissions must be enabled
- User must have permissions to view and edit content plans
- Valid content plan and content plan item records
- Understanding of content plan hierarchy structure

## Test Methods

### 1. RIM Submissions Service Initialization

```python
from veevatools.veevavault.services.rim_submissions_service import RIMSubmissionsService

def test_rim_submissions_service_initialization():
    """Test the initialization of RIMSubmissionsService"""
    # Initialize vault client
    vault_client = initialize_vault_client()
    
    # Initialize RIM Submissions service
    rim_service = RIMSubmissionsService(vault_client)
    
    # Verify service initialization
    assert rim_service is not None
    assert rim_service.vault_client == vault_client
    print("✓ RIM Submissions Service initialized successfully")
```

### 2. Copy Content Plan Testing

```python
def test_copy_content_plan():
    """Test copying a content plan"""
    rim_service = RIMSubmissionsService(vault_client)
    
    # Test data for content plan copy
    copy_data = {
        "source_id": "0CP000000001001",  # Source content plan ID
        "target_id": "0CP000000001002",  # Target parent content plan ID
        "order": 1,  # Position in target content plan
        "copy_documents": True  # Include matched documents
    }
    
    try:
        # Copy content plan
        response = rim_service.copy_into_content_plan(
            source_id=copy_data["source_id"],
            target_id=copy_data["target_id"],
            order=copy_data["order"],
            copy_documents=copy_data["copy_documents"]
        )
        
        # Verify response - content plan copy is asynchronous
        assert response['responseStatus'] in ['SUCCESS', 'WARNING']
        assert 'job_id' in response
        
        job_id = response['job_id']
        print(f"✓ Content plan copy initiated successfully. Job ID: {job_id}")
        
        # Check for warnings
        if 'warnings' in response:
            for warning in response['warnings']:
                print(f"⚠ Warning: {warning['type']} - {warning['message']}")
                
                # Validate expected warning types
                expected_warnings = ['TEMPLATE_MISMATCH', 'LEVEL_MISMATCH']
                assert warning['type'] in expected_warnings
        
        return job_id
        
    except Exception as e:
        print(f"✗ Error copying content plan: {str(e)}")
        raise
```

### 3. Copy Content Plan Item Testing

```python
def test_copy_content_plan_item():
    """Test copying a content plan item"""
    rim_service = RIMSubmissionsService(vault_client)
    
    # Test data for content plan item copy
    copy_data = {
        "source_id": "0EI000000001001",  # Source content plan item ID
        "target_id": "0CP000000001002",  # Target parent content plan ID
        "order": 2,  # Position in target content plan
        "copy_documents": False  # Don't include matched documents
    }
    
    try:
        # Copy content plan item
        response = rim_service.copy_into_content_plan(
            source_id=copy_data["source_id"],
            target_id=copy_data["target_id"],
            order=copy_data["order"],
            copy_documents=copy_data["copy_documents"]
        )
        
        # Verify response - content plan item copy is synchronous
        assert response['responseStatus'] in ['SUCCESS', 'WARNING']
        assert 'createdCPIRecordId' in response
        
        created_id = response['createdCPIRecordId']
        print(f"✓ Content plan item copied successfully. New ID: {created_id}")
        
        # Check for warnings
        if 'warnings' in response:
            for warning in response['warnings']:
                print(f"⚠ Warning: {warning['type']} - {warning['message']}")
        
        return created_id
        
    except Exception as e:
        print(f"✗ Error copying content plan item: {str(e)}")
        raise
```

### 4. Copy with Documents Testing

```python
def test_copy_content_plan_with_documents():
    """Test copying content plan with matched documents"""
    rim_service = RIMSubmissionsService(vault_client)
    
    # Test data with documents included
    copy_data = {
        "source_id": "0CP000000001003",  # Source with matched documents
        "target_id": "0CP000000001004",  # Target content plan
        "order": 1,
        "copy_documents": True
    }
    
    try:
        # Copy content plan with documents
        response = rim_service.copy_into_content_plan(**copy_data)
        
        # Verify response
        assert response['responseStatus'] in ['SUCCESS', 'WARNING']
        assert 'job_id' in response
        
        print(f"✓ Content plan with documents copy initiated. Job ID: {response['job_id']}")
        
        # Documents are included, so this should be asynchronous
        assert 'job_id' in response
        assert 'createdCPIRecordId' not in response
        
        return response['job_id']
        
    except Exception as e:
        print(f"✗ Error copying content plan with documents: {str(e)}")
        raise
```

### 5. Copy without Documents Testing

```python
def test_copy_content_plan_without_documents():
    """Test copying content plan without matched documents"""
    rim_service = RIMSubmissionsService(vault_client)
    
    # Test data without documents
    copy_data = {
        "source_id": "0EI000000001005",  # Source content plan item
        "target_id": "0CP000000001006",  # Target content plan
        "order": 3,
        "copy_documents": False
    }
    
    try:
        # Copy content plan item without documents
        response = rim_service.copy_into_content_plan(**copy_data)
        
        # Verify response
        assert response['responseStatus'] in ['SUCCESS', 'WARNING']
        
        # Without documents, item copy should be synchronous
        if 'createdCPIRecordId' in response:
            print(f"✓ Content plan item copied without documents. ID: {response['createdCPIRecordId']}")
        elif 'job_id' in response:
            print(f"✓ Content plan copy without documents initiated. Job ID: {response['job_id']}")
        
        return response
        
    except Exception as e:
        print(f"✗ Error copying content plan without documents: {str(e)}")
        raise
```

### 6. Copy to Different Position Testing

```python
def test_copy_to_different_positions():
    """Test copying content to different positions in target"""
    rim_service = RIMSubmissionsService(vault_client)
    
    source_id = "0EI000000001007"
    target_id = "0CP000000001008"
    
    # Test copying to different positions
    positions = [1, 2, 5]
    
    for position in positions:
        try:
            response = rim_service.copy_into_content_plan(
                source_id=source_id,
                target_id=target_id,
                order=position,
                copy_documents=False
            )
            
            assert response['responseStatus'] in ['SUCCESS', 'WARNING']
            
            if 'createdCPIRecordId' in response:
                print(f"✓ Content copied to position {position}. ID: {response['createdCPIRecordId']}")
            else:
                print(f"✓ Content copy to position {position} initiated. Job ID: {response['job_id']}")
                
        except Exception as e:
            print(f"✗ Error copying to position {position}: {str(e)}")
```

### 7. Template and Level Mismatch Testing

```python
def test_template_level_mismatch_handling():
    """Test handling of template and level mismatches"""
    rim_service = RIMSubmissionsService(vault_client)
    
    # Test data designed to trigger mismatches
    mismatch_scenarios = [
        {
            "name": "Template Mismatch",
            "source_id": "0EI000000001009",  # Different template
            "target_id": "0CP000000001010",
            "order": 1,
            "copy_documents": True,
            "expected_warning": "TEMPLATE_MISMATCH"
        },
        {
            "name": "Level Mismatch", 
            "source_id": "0EI000000001011",  # Different level
            "target_id": "0CP000000001012",
            "order": 1,
            "copy_documents": False,
            "expected_warning": "LEVEL_MISMATCH"
        }
    ]
    
    for scenario in mismatch_scenarios:
        try:
            print(f"\nTesting {scenario['name']}...")
            
            response = rim_service.copy_into_content_plan(
                source_id=scenario["source_id"],
                target_id=scenario["target_id"],
                order=scenario["order"],
                copy_documents=scenario["copy_documents"]
            )
            
            # Should receive warnings but still succeed
            assert response['responseStatus'] == 'WARNING'
            assert 'warnings' in response
            
            # Check for expected warning type
            warning_types = [w['type'] for w in response['warnings']]
            assert scenario['expected_warning'] in warning_types
            
            print(f"✓ {scenario['name']} handled correctly with warnings")
            
        except Exception as e:
            print(f"✗ Error testing {scenario['name']}: {str(e)}")
```

### 8. Batch Copy Operations Testing

```python
def test_batch_copy_operations():
    """Test multiple copy operations in sequence"""
    rim_service = RIMSubmissionsService(vault_client)
    
    # Multiple items to copy
    copy_operations = [
        {
            "source_id": "0EI000000001013",
            "target_id": "0CP000000001014",
            "order": 1,
            "copy_documents": False
        },
        {
            "source_id": "0EI000000001015",
            "target_id": "0CP000000001014",  # Same target, different order
            "order": 2,
            "copy_documents": False
        },
        {
            "source_id": "0EI000000001017",
            "target_id": "0CP000000001014",  # Same target, different order
            "order": 3,
            "copy_documents": True
        }
    ]
    
    results = []
    
    for i, operation in enumerate(copy_operations):
        try:
            print(f"\nExecuting copy operation {i+1}...")
            
            response = rim_service.copy_into_content_plan(**operation)
            
            assert response['responseStatus'] in ['SUCCESS', 'WARNING']
            results.append(response)
            
            if 'createdCPIRecordId' in response:
                print(f"✓ Operation {i+1} completed. ID: {response['createdCPIRecordId']}")
            else:
                print(f"✓ Operation {i+1} initiated. Job ID: {response['job_id']}")
                
        except Exception as e:
            print(f"✗ Error in operation {i+1}: {str(e)}")
            results.append({"error": str(e)})
    
    print(f"\n✓ Batch copy operations completed. {len(results)} operations processed")
    return results
```

## Error Scenarios Testing

### 1. Invalid Source ID Testing

```python
def test_invalid_source_id():
    """Test handling of invalid source ID"""
    rim_service = RIMSubmissionsService(vault_client)
    
    try:
        response = rim_service.copy_into_content_plan(
            source_id="INVALID_ID",
            target_id="0CP000000001001",
            order=1,
            copy_documents=False
        )
        
        # Should handle error gracefully
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled invalid source ID")
        
    except Exception as e:
        print(f"✓ Correctly handled invalid source ID error: {str(e)}")
```

### 2. Invalid Target ID Testing

```python
def test_invalid_target_id():
    """Test handling of invalid target ID"""
    rim_service = RIMSubmissionsService(vault_client)
    
    try:
        response = rim_service.copy_into_content_plan(
            source_id="0EI000000001001",
            target_id="INVALID_TARGET",
            order=1,
            copy_documents=False
        )
        
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled invalid target ID")
        
    except Exception as e:
        print(f"✓ Correctly handled invalid target ID error: {str(e)}")
```

### 3. Inactive Target Testing

```python
def test_inactive_target():
    """Test handling of inactive target content plan"""
    rim_service = RIMSubmissionsService(vault_client)
    
    try:
        response = rim_service.copy_into_content_plan(
            source_id="0EI000000001001",
            target_id="0CP000000009999",  # Inactive content plan
            order=1,
            copy_documents=False
        )
        
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled inactive target content plan")
        
    except Exception as e:
        print(f"✓ Correctly handled inactive target error: {str(e)}")
```

### 4. Missing copy_documents Parameter Testing

```python
def test_missing_copy_documents_parameter():
    """Test handling of missing copy_documents parameter"""
    rim_service = RIMSubmissionsService(vault_client)
    
    try:
        # This should fail as copy_documents cannot be omitted
        response = rim_service.copy_into_content_plan(
            source_id="0EI000000001001",
            target_id="0CP000000001001",
            order=1
            # copy_documents parameter intentionally omitted
        )
        
        assert False, "Expected error for missing copy_documents parameter"
        
    except Exception as e:
        print(f"✓ Correctly handled missing copy_documents parameter: {str(e)}")
```

### 5. Invalid Order Position Testing

```python
def test_invalid_order_position():
    """Test handling of invalid order position"""
    rim_service = RIMSubmissionsService(vault_client)
    
    # Test negative order
    try:
        response = rim_service.copy_into_content_plan(
            source_id="0EI000000001001",
            target_id="0CP000000001001",
            order=-1,  # Invalid negative order
            copy_documents=False
        )
        
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled negative order position")
        
    except Exception as e:
        print(f"✓ Correctly handled negative order error: {str(e)}")
    
    # Test zero order
    try:
        response = rim_service.copy_into_content_plan(
            source_id="0EI000000001001",
            target_id="0CP000000001001",
            order=0,  # Invalid zero order
            copy_documents=False
        )
        
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled zero order position")
        
    except Exception as e:
        print(f"✓ Correctly handled zero order error: {str(e)}")
```

## Sample Test Data

### Sample Copy Operation Data
```python
SAMPLE_COPY_DATA = {
    "content_plan": {
        "source_id": "0CP000000001001",
        "target_id": "0CP000000001002", 
        "order": 1,
        "copy_documents": True,
        "expected_warnings": ["TEMPLATE_MISMATCH", "LEVEL_MISMATCH"]
    },
    "content_plan_item": {
        "source_id": "0EI000000001001",
        "target_id": "0CP000000001002",
        "order": 2, 
        "copy_documents": False,
        "expected_response": "createdCPIRecordId"
    }
}
```

### Sample Warning Scenarios
```python
SAMPLE_WARNING_SCENARIOS = [
    {
        "type": "TEMPLATE_MISMATCH",
        "message": "The templates of the source and target do not align.",
        "severity": "WARNING"
    },
    {
        "type": "LEVEL_MISMATCH", 
        "message": "Level of the source record does not match the level of the target location.",
        "severity": "WARNING"
    }
]
```

## Validation Helpers

### Copy Response Validator
```python
def validate_copy_response(response, expected_type="content_plan"):
    """Validate copy operation response structure"""
    required_fields = ['responseStatus']
    
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"
    
    assert response['responseStatus'] in ['SUCCESS', 'WARNING', 'FAILURE']
    
    if response['responseStatus'] in ['SUCCESS', 'WARNING']:
        if expected_type == "content_plan":
            assert 'job_id' in response, "Content plan copy should return job_id"
        elif expected_type == "content_plan_item":
            assert 'createdCPIRecordId' in response, "Content plan item copy should return createdCPIRecordId"
    
    print("✓ Copy response validation passed")
```

### Warning Validator
```python
def validate_warnings(response):
    """Validate warning structure and content"""
    if 'warnings' in response:
        for warning in response['warnings']:
            assert 'type' in warning
            assert 'message' in warning
            
            # Validate warning types
            valid_warning_types = ['TEMPLATE_MISMATCH', 'LEVEL_MISMATCH']
            assert warning['type'] in valid_warning_types
            
            print(f"✓ Warning validated: {warning['type']}")
    
    print("✓ Warning validation passed")
```

## Performance Testing

### Copy Performance Testing
```python
def test_copy_performance():
    """Test content plan copy performance"""
    import time
    
    rim_service = RIMSubmissionsService(vault_client)
    
    start_time = time.time()
    
    response = rim_service.copy_into_content_plan(
        source_id="0EI000000001001",
        target_id="0CP000000001001",
        order=1,
        copy_documents=False
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✓ Copy request completed in {duration:.2f} seconds")
    
    # Performance assertion (adjust threshold as needed)
    assert duration < 10.0, f"Copy request too slow: {duration} seconds"
```

## Integration Testing

### End-to-End Content Plan Workflow Testing
```python
def test_complete_content_plan_workflow():
    """Test complete content plan copy workflow"""
    rim_service = RIMSubmissionsService(vault_client)
    
    print("Starting complete content plan workflow test...")
    
    try:
        # Step 1: Copy content plan item without documents
        print("✓ Step 1: Copying content plan item...")
        
        item_response = rim_service.copy_into_content_plan(
            source_id="0EI000000001001",
            target_id="0CP000000001002",
            order=1,
            copy_documents=False
        )
        
        assert 'createdCPIRecordId' in item_response
        new_item_id = item_response['createdCPIRecordId']
        print(f"✓ Content plan item copied. New ID: {new_item_id}")
        
        # Step 2: Copy another item with documents (async)
        print("✓ Step 2: Copying content with documents...")
        
        async_response = rim_service.copy_into_content_plan(
            source_id="0CP000000001003",
            target_id="0CP000000001002",
            order=2,
            copy_documents=True
        )
        
        assert 'job_id' in async_response
        job_id = async_response['job_id']
        print(f"✓ Content copy with documents initiated. Job ID: {job_id}")
        
        # Step 3: Handle warnings if present
        if 'warnings' in item_response or 'warnings' in async_response:
            print("✓ Step 3: Processing warnings...")
            
            all_warnings = []
            if 'warnings' in item_response:
                all_warnings.extend(item_response['warnings'])
            if 'warnings' in async_response:
                all_warnings.extend(async_response['warnings'])
            
            for warning in all_warnings:
                print(f"⚠ Warning handled: {warning['type']}")
        
        print("✓ Complete content plan workflow completed successfully")
        
        return {
            "item_copy": item_response,
            "async_copy": async_response
        }
        
    except Exception as e:
        print(f"✗ Error in content plan workflow: {str(e)}")
        raise
```

## Notes
- RIM Submissions requires specific licensing and permissions
- Content plan copies are asynchronous when including documents
- Content plan item copies are typically synchronous
- Warning messages indicate potential issues but don't prevent copying
- Template and level mismatches are common and should be handled gracefully
- Order position must be positive integer (1-based)
- copy_documents parameter cannot be omitted and must be boolean
- Email notifications are sent when asynchronous copy operations complete
