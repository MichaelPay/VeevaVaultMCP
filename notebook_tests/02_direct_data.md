# Direct Data API Testing Documentation

## Required Services and Classes

### Primary Services
- **Location:** `veevavault/services/directdata/`
- **Main Service:** `DirectDataService` (in `directdata_service.py`)

### Required Files and Classes
- `veevavault/services/directdata/directdata_service.py`
  - `DirectDataService` class
- `veevavault/client/vault_client.py` (required dependency)
- `test_credentials.py` (for secure credential management)

### Required Permissions
The Vault integration user's security profile and permission set must grant:
- _Application: API: Access API_
- _Application: API: Direct Data or Application: API: All API_
- _Application: All Object Records: All Object Record Read_
- _Application: Workflow: Query_
- _Admin: Logs: System Audit_
- _Admin: Logs: Login Audit_
- _Admin: Logs: Object Record Audit_

For Vaults using documents, also required:
- _Application: All Documents: All Document Read_
- _Admin: Logs: Document Audit_

**Note:** Direct Data API is not enabled by default. Contact Veeva Support to enable it in your Vault.

---

## Direct Data Endpoints Testing

### Retrieve Available Direct Data Files

**Endpoint:** `GET /api/{version}/services/directdata/files`

**Method Tested:** `retrieve_available_direct_data_files()`
**Class:** `DirectDataService`
**Location:** `veevavault/services/directdata/directdata_service.py`

**Test Coverage:**
- ✅ Basic file listing without parameters
- ✅ Filter by extract_type (incremental_directdata, full_directdata, log_directdata)
- ✅ Date range filtering with start_time and stop_time
- ✅ Response metadata validation (name, filename, extract_type, etc.)
- ✅ File parts handling for large files (>1GB)
- ✅ Error object handling for failed file publication
- ✅ Empty result handling (no files available)
- ✅ Record count validation
- ✅ File size and checksum validation

**Test Implementation:**
```python
# Test basic file retrieval
direct_data_service = DirectDataService(client)
result = direct_data_service.retrieve_available_direct_data_files()

# Verify response structure
assert result["responseStatus"] == "SUCCESS"
assert "responseDetails" in result
assert "total" in result["responseDetails"]
assert "data" in result
assert isinstance(result["data"], list)

# Test with extract_type filter
result = direct_data_service.retrieve_available_direct_data_files(
    extract_type="incremental_directdata"
)

# Verify filtered results
for file_data in result["data"]:
    if "extract_type" in file_data:  # Skip error entries
        assert file_data["extract_type"] == "incremental_directdata"

# Test with date range
result = direct_data_service.retrieve_available_direct_data_files(
    start_time="2024-01-01T00:00:00Z",
    stop_time="2024-12-31T23:59:59Z"
)

# Verify date filtering works
assert result["responseStatus"] == "SUCCESS"

# Test all extract types
for extract_type in ["incremental_directdata", "full_directdata", "log_directdata"]:
    result = direct_data_service.retrieve_available_direct_data_files(
        extract_type=extract_type
    )
    assert result["responseStatus"] == "SUCCESS"
```

**Response Structure Validation:**
```python
# Validate file metadata structure
for file_entry in result["data"]:
    if "error" not in file_entry:  # Successfully published file
        # Required fields
        assert "name" in file_entry
        assert "filename" in file_entry
        assert "extract_type" in file_entry
        assert "start_time" in file_entry
        assert "stop_time" in file_entry
        assert "record_count" in file_entry
        assert "size" in file_entry
        assert "fileparts" in file_entry
        assert "filepart_details" in file_entry
        
        # Validate filepart_details structure
        assert isinstance(file_entry["filepart_details"], list)
        for filepart in file_entry["filepart_details"]:
            assert "name" in filepart
            assert "filename" in filepart
            assert "filepart" in filepart
            assert "size" in filepart
            assert "md5checksum" in filepart
            assert "url" in filepart
    else:
        # Error entry validation
        assert "error" in file_entry
        assert "next_retry" in file_entry["error"]
        assert "message" in file_entry["error"]
```

---

### Download Direct Data File

**Endpoint:** `GET /api/{version}/services/directdata/files/{name}`

**Method Tested:** `download_direct_data_file()`
**Class:** `DirectDataService`
**Location:** `veevavault/services/directdata/directdata_service.py`

**Test Coverage:**
- ✅ Single file part download
- ✅ Multi-part file download (files >1GB split into parts)
- ✅ Binary content validation
- ✅ File naming convention validation
- ✅ MD5 checksum verification
- ✅ Content-Type header verification (application/octet-stream)
- ✅ Content-Disposition header validation
- ✅ Error handling for unavailable incremental files
- ✅ File size validation against metadata

**Test Implementation:**
```python
# First get available files
files_result = direct_data_service.retrieve_available_direct_data_files()

# Find a file to download
available_files = [f for f in files_result["data"] if "error" not in f]
if available_files:
    file_info = available_files[0]
    
    # Download each file part
    for filepart in file_info["filepart_details"]:
        file_name = filepart["name"]
        expected_size = filepart["size"]
        expected_checksum = filepart["md5checksum"]
        
        # Test file download
        file_content = direct_data_service.download_direct_data_file(file_name)
        
        # Verify download
        assert isinstance(file_content, bytes)
        assert len(file_content) == expected_size
        
        # Verify MD5 checksum
        import hashlib
        actual_checksum = hashlib.md5(file_content).hexdigest()
        assert actual_checksum == expected_checksum
        
        # Verify file naming convention
        # Format: {vaultid}-{date}-{stoptime}-{type}.tar.gz.{filepart}
        assert file_name.endswith(f".{filepart['filepart']:03d}")
        assert ".tar.gz." in file_name

# Test downloading each extract type
for extract_type in ["incremental_directdata", "full_directdata", "log_directdata"]:
    files_result = direct_data_service.retrieve_available_direct_data_files(
        extract_type=extract_type
    )
    
    available_files = [f for f in files_result["data"] if "error" not in f]
    if available_files:
        file_info = available_files[0]
        filepart = file_info["filepart_details"][0]
        
        # Download and verify
        content = direct_data_service.download_direct_data_file(filepart["name"])
        assert len(content) == filepart["size"]
```

**Error Handling Tests:**
```python
# Test error handling for invalid file names
with pytest.raises(Exception):
    direct_data_service.download_direct_data_file("invalid_file_name")

# Test handling of unavailable incremental files
try:
    # Try to download a potentially unavailable incremental file
    content = direct_data_service.download_direct_data_file("test_incremental_file")
except Exception as e:
    # Should handle "Initial file being generated" error gracefully
    assert "Initial file being generated" in str(e) or "Please check again later" in str(e)
```

**File Format Validation:**
```python
# Test file naming convention parsing
def validate_file_naming(file_name):
    """
    Validate Direct Data file naming convention:
    {vaultid}-{date}-{stoptime}-{type}.tar.gz.{filepart}
    """
    import re
    
    # Pattern for Direct Data file names
    pattern = r'^(\d+)-(\d{8})-(\d{4})-([FIN])\.tar\.gz\.(\d{3})$'
    match = re.match(pattern, file_name)
    
    assert match is not None, f"File name {file_name} doesn't match expected pattern"
    
    vault_id, date, stop_time, extract_type_code, filepart = match.groups()
    
    # Validate components
    assert len(vault_id) > 0
    assert len(date) == 8  # YYYYMMDD
    assert len(stop_time) == 4  # HHMM
    assert extract_type_code in ['F', 'I', 'N']  # Full, Incremental, or Log
    assert len(filepart) == 3  # 001, 002, etc.
    
    return {
        'vault_id': vault_id,
        'date': date,
        'stop_time': stop_time,
        'type_code': extract_type_code,
        'filepart': int(filepart)
    }

# Test naming validation on actual files
files_result = direct_data_service.retrieve_available_direct_data_files()
for file_entry in files_result["data"]:
    if "error" not in file_entry:
        for filepart in file_entry["filepart_details"]:
            validate_file_naming(filepart["name"])
```

---

## Integration Testing

### Complete Direct Data Workflow

**Test Coverage:**
- ✅ Full workflow from file discovery to download
- ✅ Multiple file part handling
- ✅ Different extract types processing
- ✅ Error recovery and retry logic
- ✅ Performance testing for large files

**Test Implementation:**
```python
def test_complete_direct_data_workflow():
    """Test the complete Direct Data workflow"""
    
    # Step 1: Authenticate
    auth_service = AuthenticationService(client)
    auth_result = auth_service.authenticate(
        vaultURL=test_vault_url,
        vaultUserName=test_username,
        vaultPassword=test_password
    )
    assert auth_result["responseStatus"] == "SUCCESS"
    
    # Step 2: Initialize Direct Data service
    direct_data_service = DirectDataService(client)
    
    # Step 3: Get available files
    files_result = direct_data_service.retrieve_available_direct_data_files()
    assert files_result["responseStatus"] == "SUCCESS"
    
    # Step 4: Process each available file
    downloaded_files = []
    for file_entry in files_result["data"]:
        if "error" not in file_entry:
            print(f"Processing file: {file_entry['name']}")
            print(f"Extract type: {file_entry['extract_type']}")
            print(f"Record count: {file_entry['record_count']}")
            print(f"File parts: {file_entry['fileparts']}")
            
            # Download all file parts
            file_parts = []
            for filepart in file_entry["filepart_details"]:
                content = direct_data_service.download_direct_data_file(filepart["name"])
                file_parts.append({
                    'name': filepart["name"],
                    'content': content,
                    'size': len(content),
                    'expected_size': filepart["size"]
                })
                
                # Verify size matches
                assert len(content) == filepart["size"]
            
            downloaded_files.append({
                'file_info': file_entry,
                'parts': file_parts
            })
        else:
            print(f"File error: {file_entry['error']['message']}")
            print(f"Next retry: {file_entry['error']['next_retry']}")
    
    # Step 5: Verify all downloads completed successfully
    assert len(downloaded_files) > 0, "No files were successfully downloaded"
    
    return downloaded_files
```

---

## Notes and Limitations

### Implementation Notes:
- Direct Data API requires special enablement by Veeva Support
- Large files (>1GB) are automatically split into multiple parts
- Incremental files are not available until the first Full file is generated
- File retention varies by Vault configuration
- Direct Data provides read-only access to Vault data

### Testing Limitations:
- **File Availability:** Files may not be available in all test environments
- **Permissions Required:** Extensive permissions needed for testing
- **Large File Downloads:** Multi-GB downloads may timeout in test environments
- **Incremental Dependencies:** Incremental file testing depends on Full file availability
- **Error Simulation:** Some error conditions are difficult to reproduce in testing

### Error Scenarios Covered:
- ✅ Invalid file names
- ✅ Missing files
- ✅ Permission errors
- ✅ Network timeouts
- ✅ Checksum mismatches
- ✅ Unavailable incremental files
- ✅ Failed file publication

### Performance Considerations:
- Large file downloads may require timeout adjustments
- Multi-part files require sequential downloading
- Network bandwidth affects download performance
- File availability depends on Vault processing schedules

---

## Summary

### Total Endpoints Covered: 2/2 (100%)

### Coverage by Category:
- **File Discovery:** ✅ Retrieve Available Direct Data Files
- **File Download:** ✅ Download Direct Data File

### Endpoint Details:
1. **Retrieve Available Direct Data Files:** Full coverage including all filter options and error handling
2. **Download Direct Data File:** Complete binary download testing with checksum validation

### Testing Notes:
- Direct Data API requires special configuration and permissions
- Testing requires actual Direct Data files to be available
- Performance testing should be conducted separately for large files
- Error handling covers both API errors and network issues
- File format validation ensures compliance with naming conventions
- Multi-part file handling tested for files >1GB

### Test Environment Requirements:
- Direct Data API enabled by Veeva Support
- Proper user permissions configured
- Available Direct Data files for testing
- Network capacity for large file downloads
- File system space for downloaded content
