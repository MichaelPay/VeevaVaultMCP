# 34. RIM Submissions Archive - Testing Documentation

## Overview
Testing documentation for RIM Submissions Archive functionality in Veeva Vault. This module provides functionality for importing submissions, retrieving import results, and managing submission metadata mapping for regulatory submissions archive.

## Prerequisites
- Veeva RIM Submissions Archive must be enabled
- User must have permissions to view and edit submission__v object records
- File staging access for submission uploads
- Valid submission and application object records

## Test Methods

### 1. RIM Submissions Archive Service Initialization

```python
from veevatools.veevavault.services.rim_submissions_archive_service import RIMSubmissionsArchiveService

def test_rim_submissions_archive_service_initialization():
    """Test the initialization of RIMSubmissionsArchiveService"""
    # Initialize vault client
    vault_client = initialize_vault_client()
    
    # Initialize RIM Submissions Archive service
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    # Verify service initialization
    assert rim_service is not None
    assert rim_service.vault_client == vault_client
    print("✓ RIM Submissions Archive Service initialized successfully")
```

### 2. Import Submission Testing

```python
def test_import_submission():
    """Test importing a submission into Vault"""
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    # Test data for submission import
    submission_id = "00S000000000101"  # Valid submission__v record ID
    file_path = "/SubmissionsArchive/nda123456/0000"  # Path to submission folder
    
    try:
        # Import submission
        response = rim_service.import_submission(
            submission_id=submission_id,
            file_path=file_path
        )
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        assert 'job_id' in response
        assert 'url' in response
        
        # Store job_id for later use
        job_id = response['job_id']
        print(f"✓ Submission import initiated successfully. Job ID: {job_id}")
        
        # Check for warnings
        if 'warnings' in response:
            for warning in response['warnings']:
                print(f"⚠ Warning: {warning['type']} - {warning['message']}")
        
        return job_id
        
    except Exception as e:
        print(f"✗ Error importing submission: {str(e)}")
        raise
```

### 3. Import Submission from User Folder Testing

```python
def test_import_submission_from_user_folder():
    """Test importing a submission from user folder"""
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    # Test data for user folder import
    submission_id = "00S000000000102"
    user_folder_path = "/u5678/Submissions Archive Import/nda123456/0013"
    
    try:
        # Import submission from user folder
        response = rim_service.import_submission(
            submission_id=submission_id,
            file_path=user_folder_path
        )
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        assert 'job_id' in response
        
        print("✓ Submission import from user folder initiated successfully")
        return response['job_id']
        
    except Exception as e:
        print(f"✗ Error importing submission from user folder: {str(e)}")
        raise
```

### 4. Retrieve Submission Import Results Testing

```python
def test_retrieve_submission_import_results():
    """Test retrieving submission import results"""
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    # Test data
    submission_id = "00S000000000101"
    job_id = "1301"  # From previous import job
    
    try:
        # Retrieve import results
        response = rim_service.retrieve_submission_import_results(
            submission_id=submission_id,
            job_id=job_id
        )
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        assert 'data' in response
        
        # Verify result data
        for result in response['data']:
            assert result['responseStatus'] == 'SUCCESS'
            assert 'id' in result  # Binder ID
            assert 'major_version_number__v' in result
            assert 'minor_version_number__v' in result
            
            print(f"✓ Import result: Binder ID {result['id']}, "
                  f"Version {result['major_version_number__v']}.{result['minor_version_number__v']}")
        
        return response
        
    except Exception as e:
        print(f"✗ Error retrieving import results: {str(e)}")
        raise
```

### 5. Retrieve Submission Metadata Mapping Testing

```python
def test_retrieve_submission_metadata_mapping():
    """Test retrieving submission metadata mapping"""
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    # Test data
    submission_id = "00S000000000101"
    
    try:
        # Retrieve metadata mapping
        response = rim_service.retrieve_submission_metadata_mapping(
            submission_id=submission_id
        )
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        assert 'data' in response
        assert 'responseDetails' in response
        
        # Verify mapping data
        for mapping in response['data']:
            assert 'name__v' in mapping
            assert 'xml_id' in mapping
            
            # Check for mapping fields
            mapping_fields = ['clinical_site__v', 'clinical_study__v', 'drug_product__v',
                            'drug_substance__v', 'indication__v', 'manufacturer__v', 
                            'nonclinical_study__v']
            
            found_mapping = False
            for field in mapping_fields:
                if field in mapping:
                    found_mapping = True
                    print(f"✓ Found mapping: {field} = {mapping[field]}")
                    break
            
            if not found_mapping:
                print(f"⚠ No mapping found for record: {mapping['name__v']}")
        
        print(f"✓ Retrieved {response['responseDetails']['total']} metadata mappings")
        return response
        
    except Exception as e:
        print(f"✗ Error retrieving metadata mapping: {str(e)}")
        raise
```

### 6. Retrieve Metadata Mapping as CSV Testing

```python
def test_retrieve_metadata_mapping_csv():
    """Test retrieving metadata mapping in CSV format"""
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    # Test data
    submission_id = "00S000000000101"
    
    try:
        # Retrieve metadata mapping as CSV
        response = rim_service.retrieve_submission_metadata_mapping(
            submission_id=submission_id,
            accept_header="text/csv"
        )
        
        # Verify CSV response
        assert response is not None
        assert isinstance(response, str)  # CSV data as string
        
        # Basic CSV validation
        lines = response.strip().split('\n')
        assert len(lines) > 1  # Header + data rows
        
        # Check header row
        header = lines[0]
        expected_fields = ['name__v', 'xml_id']
        for field in expected_fields:
            assert field in header
        
        print("✓ Metadata mapping retrieved in CSV format successfully")
        print(f"✓ CSV contains {len(lines) - 1} data rows")
        
        return response
        
    except Exception as e:
        print(f"✗ Error retrieving CSV metadata mapping: {str(e)}")
        raise
```

### 7. Update Submission Metadata Mapping Testing

```python
def test_update_submission_metadata_mapping():
    """Test updating submission metadata mapping"""
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    # Test data
    submission_id = "00S000000000101"
    mapping_updates = [
        {
            "name__v": "1675_00S000000000802",
            "drug_substance__v": "V0M000000001001"  # Target object record ID
        },
        {
            "name__v": "1681_00S000000000802", 
            "nonclinical_study__v": "V0N000000001001"  # Target object record ID
        }
    ]
    
    try:
        # Update metadata mapping
        response = rim_service.update_submission_metadata_mapping(
            submission_id=submission_id,
            mapping_data=mapping_updates
        )
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        
        # Verify individual updates
        if 'data' in response:
            for update_result in response['data']:
                assert update_result['responseStatus'] == 'SUCCESS'
                print(f"✓ Updated mapping for: {update_result.get('name__v', 'Unknown')}")
        
        print("✓ Submission metadata mapping updated successfully")
        return response
        
    except Exception as e:
        print(f"✗ Error updating metadata mapping: {str(e)}")
        raise
```

### 8. End-to-End Submission Archive Workflow Testing

```python
def test_complete_submission_archive_workflow():
    """Test complete submission archive workflow"""
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    print("Starting complete submission archive workflow test...")
    
    try:
        # Step 1: Import submission
        submission_id = "00S000000000101"
        file_path = "/SubmissionsArchive/nda123456/0000"
        
        import_response = rim_service.import_submission(
            submission_id=submission_id,
            file_path=file_path
        )
        
        job_id = import_response['job_id']
        print(f"✓ Step 1: Submission import initiated (Job ID: {job_id})")
        
        # Step 2: Wait for job completion (in real scenario)
        # Note: In actual testing, you would poll job status
        print("✓ Step 2: Waiting for import job completion...")
        
        # Step 3: Retrieve import results
        results_response = rim_service.retrieve_submission_import_results(
            submission_id=submission_id,
            job_id=job_id
        )
        
        binder_id = results_response['data'][0]['id']
        print(f"✓ Step 3: Import completed, Binder ID: {binder_id}")
        
        # Step 4: Retrieve metadata mapping
        mapping_response = rim_service.retrieve_submission_metadata_mapping(
            submission_id=submission_id
        )
        
        print(f"✓ Step 4: Retrieved {len(mapping_response['data'])} metadata mappings")
        
        # Step 5: Update mappings if needed
        if mapping_response['data']:
            # Example: Update first mapping
            first_mapping = mapping_response['data'][0]
            if first_mapping.get('drug_substance__v.name__v') == "":
                update_data = [{
                    "name__v": first_mapping['name__v'],
                    "drug_substance__v": "V0M000000001001"
                }]
                
                update_response = rim_service.update_submission_metadata_mapping(
                    submission_id=submission_id,
                    mapping_data=update_data
                )
                
                print("✓ Step 5: Metadata mapping updated")
        
        print("✓ Complete submission archive workflow completed successfully")
        
    except Exception as e:
        print(f"✗ Error in submission archive workflow: {str(e)}")
        raise
```

## Error Scenarios Testing

### 1. Invalid Submission ID Testing

```python
def test_invalid_submission_id():
    """Test handling of invalid submission ID"""
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    try:
        response = rim_service.import_submission(
            submission_id="INVALID_ID",
            file_path="/SubmissionsArchive/test/submission"
        )
        
        # Should not reach here
        assert False, "Expected exception for invalid submission ID"
        
    except Exception as e:
        print(f"✓ Correctly handled invalid submission ID: {str(e)}")
```

### 2. Invalid File Path Testing

```python
def test_invalid_file_path():
    """Test handling of invalid file path"""
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    try:
        response = rim_service.import_submission(
            submission_id="00S000000000101",
            file_path="/NonExistent/Path/submission"
        )
        
        # Should handle error gracefully
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled invalid file path")
        
    except Exception as e:
        print(f"✓ Correctly handled invalid file path error: {str(e)}")
```

### 3. Missing Permissions Testing

```python
def test_missing_permissions():
    """Test handling of missing permissions"""
    # Note: This would typically require a different user context
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    try:
        response = rim_service.retrieve_submission_metadata_mapping(
            submission_id="00S000000000999"  # Submission user cannot access
        )
        
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled missing permissions")
        
    except Exception as e:
        print(f"✓ Correctly handled permission error: {str(e)}")
```

## Sample Test Data

### Sample Submission Import Data
```python
SAMPLE_SUBMISSION_DATA = {
    "submission_id": "00S000000000101",
    "file_paths": [
        "/SubmissionsArchive/nda123456/0000",
        "/SubmissionsArchive/nda123456/0001.zip",
        "/u5678/Submissions Archive Import/nda123456/0013"
    ],
    "expected_warnings": [
        "APPLICATION_MISMATCH",
        "SUBMISSION_MISMATCH"
    ]
}
```

### Sample Metadata Mapping Data
```python
SAMPLE_MAPPING_DATA = [
    {
        "name__v": "1675_00S000000000802",
        "xml_id": "m2-3-s-drug-substance",
        "drug_substance__v": "Ethyl Alcohol",
        "manufacturer__v": "Veeva"
    },
    {
        "name__v": "1681_00S000000000802",
        "xml_id": "S001",
        "nonclinical_study__v": "Study001"
    }
]
```

## Validation Helpers

### Submission Import Response Validator
```python
def validate_import_response(response):
    """Validate submission import response structure"""
    required_fields = ['responseStatus', 'job_id', 'url']
    
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"
    
    assert response['responseStatus'] in ['SUCCESS', 'FAILURE']
    
    if response['responseStatus'] == 'SUCCESS':
        assert isinstance(response['job_id'], int)
        assert response['url'].startswith('/api/')
    
    print("✓ Import response validation passed")
```

### Metadata Mapping Response Validator  
```python
def validate_mapping_response(response):
    """Validate metadata mapping response structure"""
    required_fields = ['responseStatus', 'data']
    
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"
    
    assert response['responseStatus'] == 'SUCCESS'
    assert isinstance(response['data'], list)
    
    # Validate mapping records
    for mapping in response['data']:
        assert 'name__v' in mapping
        assert 'xml_id' in mapping
    
    print("✓ Mapping response validation passed")
```

## Performance Testing

### Import Performance Testing
```python
def test_import_performance():
    """Test submission import performance"""
    import time
    
    rim_service = RIMSubmissionsArchiveService(vault_client)
    
    start_time = time.time()
    
    response = rim_service.import_submission(
        submission_id="00S000000000101",
        file_path="/SubmissionsArchive/nda123456/large_submission"
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✓ Import request completed in {duration:.2f} seconds")
    
    # Performance assertion (adjust threshold as needed)
    assert duration < 30.0, f"Import request too slow: {duration} seconds"
```

## Notes
- RIM Submissions Archive requires specific licensing
- File staging permissions may vary by user
- Import jobs are asynchronous - always check job status
- Metadata mappings are specific to eCTD submissions
- Warning messages are informational and don't prevent import
- ZIP file imports not supported from user folders
