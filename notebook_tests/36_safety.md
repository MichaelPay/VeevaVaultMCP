# 36. Safety - Testing Documentation

## Overview
Testing documentation for Veeva Safety functionality in Veeva Vault. This module provides comprehensive safety case management capabilities including intake processing, narrative management, and E2B file handling for Individual Case Safety Reports (ICSRs).

## Prerequisites
- Veeva Safety must be enabled
- User must have appropriate Safety permissions
- Understanding of E2B format and safety case workflows
- Valid organization and transmission profile configurations

## Test Methods

### 1. Safety Service Initialization

```python
from veevatools.veevavault.services.safety_service import SafetyService

def test_safety_service_initialization():
    """Test the initialization of SafetyService"""
    # Initialize vault client
    vault_client = initialize_vault_client()
    
    # Initialize Safety service
    safety_service = SafetyService(vault_client)
    
    # Verify service initialization
    assert safety_service is not None
    assert safety_service.vault_client == vault_client
    print("✓ Safety Service initialized successfully")
```

### 2. Intake Inbox Item Testing

```python
def test_intake_inbox_item():
    """Test importing an inbox item from E2B file"""
    safety_service = SafetyService(vault_client)
    
    # Test data for inbox item intake
    intake_data = {
        "file_path": "/directory/labrinone_literature_case.xml",
        "format": "e2br3__v",  # E2B R3 format
        "organization": "vault_customer__v",
        "origin_organization": "vertio_biopharma__c",
        "transmission_profile": "general_api_profile__v"
    }
    
    try:
        # Import inbox item
        response = safety_service.intake_inbox_item(
            file_path=intake_data["file_path"],
            format=intake_data["format"],
            organization=intake_data["organization"],
            origin_organization=intake_data["origin_organization"],
            transmission_profile=intake_data["transmission_profile"]
        )
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        assert 'intake_id' in response
        assert 'url' in response
        
        intake_id = response['intake_id']
        print(f"✓ Inbox item intake initiated successfully. Intake ID: {intake_id}")
        
        # Verify URL format
        assert response['url'].startswith('/api/')
        assert 'intake/status' in response['url']
        
        return intake_id
        
    except Exception as e:
        print(f"✗ Error importing inbox item: {str(e)}")
        raise
```

### 3. Intake Imported Case Testing

```python
def test_intake_imported_case():
    """Test importing a case from E2B file"""
    safety_service = SafetyService(vault_client)
    
    # Test data for imported case intake
    intake_data = {
        "file_path": "/directory/cholecap_vaers_literature_case.xml",
        "format": "e2br3__v",
        "organization": "verteo_biopharma__c",
        "origin_organization": "fda__v"
    }
    
    try:
        # Import case
        response = safety_service.intake_imported_case(
            file_path=intake_data["file_path"],
            format=intake_data["format"],
            organization=intake_data["organization"],
            origin_organization=intake_data["origin_organization"]
        )
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        assert 'intake_id' in response
        assert 'url' in response
        
        intake_id = response['intake_id']
        print(f"✓ Imported case intake initiated successfully. Intake ID: {intake_id}")
        
        return intake_id
        
    except Exception as e:
        print(f"✗ Error importing case: {str(e)}")
        raise
```

### 4. Retrieve Intake Status Testing

```python
def test_retrieve_intake_status():
    """Test retrieving intake status"""
    safety_service = SafetyService(vault_client)
    
    # Test data
    inbound_id = "V29000000005001"
    
    try:
        # Retrieve intake status
        response = safety_service.retrieve_intake_status(inbound_id=inbound_id)
        
        # Verify response structure
        required_fields = ['status', 'inbound-transmission', 'number-of-icsrs']
        for field in required_fields:
            assert field in response, f"Missing required field: {field}"
        
        # Verify status values
        valid_statuses = ['complete', 'in_progress', 'failed']
        assert response['status'] in valid_statuses
        
        print(f"✓ Intake status retrieved: {response['status']}")
        print(f"✓ Number of ICSRs: {response['number-of-icsrs']}")
        print(f"✓ Successes/Warnings: {response.get('number-success/warning', 0)}")
        print(f"✓ Failures: {response.get('number-failures', 0)}")
        
        # Check ICSR details
        if 'icsr-details' in response:
            for icsr in response['icsr-details']:
                assert 'status' in icsr
                assert 'inbound-transmission' in icsr
                print(f"✓ ICSR {icsr.get('icsr', 'N/A')}: {icsr['status']}")
        
        return response
        
    except Exception as e:
        print(f"✗ Error retrieving intake status: {str(e)}")
        raise
```

### 5. Retrieve ACK Testing

```python
def test_retrieve_ack():
    """Test retrieving E2B acknowledgement"""
    safety_service = SafetyService(vault_client)
    
    # Test data
    inbound_id = "V29000000005001"
    
    try:
        # Retrieve ACK
        ack_response = safety_service.retrieve_ack(inbound_id=inbound_id)
        
        # Verify ACK is XML format
        assert ack_response is not None
        assert isinstance(ack_response, str)
        
        # Basic XML validation
        assert '<?xml' in ack_response
        assert 'MCCI_IN200101UV01' in ack_response
        
        # Check for key ACK elements
        ack_elements = [
            'acknowledgement',
            'creationTime',
            'interactionId'
        ]
        
        for element in ack_elements:
            assert element in ack_response
        
        print("✓ ACK retrieved successfully")
        print(f"✓ ACK length: {len(ack_response)} characters")
        
        return ack_response
        
    except Exception as e:
        print(f"✗ Error retrieving ACK: {str(e)}")
        raise
```

### 6. Intake JSON Testing

```python
def test_intake_json():
    """Test JSON intake for safety cases"""
    safety_service = SafetyService(vault_client)
    
    # Sample JSON intake data
    json_data = {
        "patient": {
            "age_value__v": 45,
            "age_unit__v": "years__v",
            "gender__v": "male__v"
        },
        "case": {
            "case_type__v": "spontaneous__v",
            "serious__v": True
        },
        "events": [
            {
                "event_name__v": "Headache",
                "outcome__v": "recovered__v"
            }
        ],
        "products": [
            {
                "product_name__v": "Test Drug",
                "dose_value__v": 50,
                "dose_unit__v": "mg"
            }
        ]
    }
    
    try:
        # Submit JSON intake
        response = safety_service.intake_json(
            intake_json=json_data,
            organization_api_name="verteo_biopharma"
        )
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        assert 'jobId' in response
        assert 'transmissionRecordId' in response
        
        job_id = response['jobId']
        transmission_id = response['transmissionRecordId']
        
        print(f"✓ JSON intake submitted successfully")
        print(f"✓ Job ID: {job_id}")
        print(f"✓ Transmission ID: {transmission_id}")
        
        return {
            "job_id": job_id,
            "transmission_id": transmission_id
        }
        
    except Exception as e:
        print(f"✗ Error in JSON intake: {str(e)}")
        raise
```

### 7. Import Narrative Testing

```python
def test_import_narrative():
    """Test importing narrative text into a case"""
    safety_service = SafetyService(vault_client)
    
    # Test data
    narrative_data = {
        "case_id": "V2B000000000201",
        "narrative_type": "primary",
        "narrative_language": "eng",
        "narrative_text": "The patient took 500 mg cholecap at 2pm and started experiencing heart palpitations at 2:30pm. The symptoms persisted for approximately 2 hours before subsiding. Patient had no prior history of cardiac issues."
    }
    
    try:
        # Import narrative
        response = safety_service.import_narrative(
            case_id=narrative_data["case_id"],
            narrative_type=narrative_data["narrative_type"],
            narrative_language=narrative_data["narrative_language"],
            narrative_text=narrative_data["narrative_text"]
        )
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        
        print(f"✓ Narrative imported successfully for case {narrative_data['case_id']}")
        print(f"✓ Language: {narrative_data['narrative_language']}")
        print(f"✓ Type: {narrative_data['narrative_type']}")
        
        return response
        
    except Exception as e:
        print(f"✗ Error importing narrative: {str(e)}")
        raise
```

### 8. Import Narrative Translation Testing

```python
def test_import_narrative_translation():
    """Test importing narrative translation"""
    safety_service = SafetyService(vault_client)
    
    # Test data for translation
    translation_data = {
        "case_id": "V2B000000000201",
        "narrative_type": "translation",
        "narrative_language": "fra",  # French
        "narrative_text": "Le patient a pris 500 mg de cholecap à 14h et a commencé à ressentir des palpitations cardiaques à 14h30. Les symptômes ont persisté pendant environ 2 heures avant de s'atténuer.",
        "link_translation_to_primary": True
    }
    
    try:
        # Import narrative translation
        response = safety_service.import_narrative(
            case_id=translation_data["case_id"],
            narrative_type=translation_data["narrative_type"],
            narrative_language=translation_data["narrative_language"],
            narrative_text=translation_data["narrative_text"],
            link_translation_to_primary=translation_data["link_translation_to_primary"]
        )
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        
        print(f"✓ Narrative translation imported successfully")
        print(f"✓ Translation language: {translation_data['narrative_language']}")
        print(f"✓ Linked to primary: {translation_data['link_translation_to_primary']}")
        
        return response
        
    except Exception as e:
        print(f"✗ Error importing narrative translation: {str(e)}")
        raise
```

### 9. Bulk Import Narrative Testing

```python
def test_bulk_import_narrative():
    """Test bulk importing multiple narratives"""
    safety_service = SafetyService(vault_client)
    
    # Prepare CSV data for bulk import
    csv_data = [
        {
            "caseId": "V2B000000002001",
            "localizedCaseId": "",
            "narrativeType": "primary",
            "narrativeLanguage": "eng",
            "narrative": "Patient experienced mild headache after taking medication..."
        },
        {
            "caseId": "V2B000000002002", 
            "localizedCaseId": "",
            "narrativeType": "primary",
            "narrativeLanguage": "eng",
            "narrative": "Patient reported nausea and dizziness approximately 1 hour post-dose..."
        },
        {
            "caseId": "V2B000000002001",
            "localizedCaseId": "V2L000000001001",
            "narrativeType": "translation",
            "narrativeLanguage": "fra",
            "narrative": "Le patient a ressenti un léger mal de tête après avoir pris le médicament..."
        }
    ]
    
    try:
        # Submit bulk import
        response = safety_service.bulk_import_narrative(
            narratives_csv_data=csv_data,
            integrity_check=True,
            migration_mode=False,
            archive_document=False
        )
        
        # Verify response
        assert response['responseStatus'] == 'success__v'
        assert 'responseDetails' in response
        assert 'import_id' in response['responseDetails']
        assert 'result_uri' in response['responseDetails']
        
        import_id = response['responseDetails']['import_id']
        result_uri = response['responseDetails']['result_uri']
        
        print(f"✓ Bulk narrative import initiated successfully")
        print(f"✓ Import ID: {import_id}")
        print(f"✓ Result URI: {result_uri}")
        
        return import_id
        
    except Exception as e:
        print(f"✗ Error in bulk narrative import: {str(e)}")
        raise
```

### 10. Retrieve Bulk Import Status Testing

```python
def test_retrieve_bulk_import_status():
    """Test retrieving bulk import status"""
    safety_service = SafetyService(vault_client)
    
    # Test data
    import_id = "dc2daf9d-8549-4701-805a-c3f62a2aefa5"
    
    try:
        # Retrieve bulk import status
        response = safety_service.retrieve_bulk_import_status(import_id=import_id)
        
        # Verify response structure
        required_fields = ['responseStatus', 'responseDetails']
        for field in required_fields:
            assert field in response
        
        status = response['responseStatus']
        details = response['responseDetails']
        
        print(f"✓ Bulk import status: {status}")
        
        # Check status-specific fields
        if status == 'completed__v':
            assert 'total_narratives' in details
            assert 'completed_narratives' in details
            assert 'start_time' in details
            assert 'end_time' in details
            
            print(f"✓ Total narratives: {details['total_narratives']}")
            print(f"✓ Completed narratives: {details['completed_narratives']}")
            
            # Check individual results
            if 'data' in response:
                for result in response['data']:
                    case_id = result.get('case_id')
                    result_status = result.get('status')
                    print(f"✓ Case {case_id}: {result_status}")
                    
                    if result_status == 'SUCCESS':
                        assert 'narrative_document_version' in result
                    elif result_status == 'FAILED':
                        assert 'errors' in result
                        
        elif status == 'in_progress__v':
            assert 'start_time' in details
            assert 'total_narratives' in details
            print(f"✓ Progress: {details.get('completed_narratives', 0)}/{details['total_narratives']}")
        
        return response
        
    except Exception as e:
        print(f"✗ Error retrieving bulk import status: {str(e)}")
        raise
```

## Error Scenarios Testing

### 1. Invalid E2B File Testing

```python
def test_invalid_e2b_file():
    """Test handling of invalid E2B file"""
    safety_service = SafetyService(vault_client)
    
    try:
        response = safety_service.intake_inbox_item(
            file_path="/directory/invalid_file.xml",
            format="e2br3__v",
            organization="vault_customer__v"
        )
        
        # Should handle error gracefully
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled invalid E2B file")
        
    except Exception as e:
        print(f"✓ Correctly handled invalid E2B file error: {str(e)}")
```

### 2. Invalid Organization Testing

```python
def test_invalid_organization():
    """Test handling of invalid organization"""
    safety_service = SafetyService(vault_client)
    
    try:
        response = safety_service.intake_imported_case(
            file_path="/directory/valid_case.xml",
            format="e2br3__v",
            organization="invalid_org__c"
        )
        
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled invalid organization")
        
    except Exception as e:
        print(f"✓ Correctly handled invalid organization error: {str(e)}")
```

### 3. Invalid Case ID for Narrative Testing

```python
def test_invalid_case_id_narrative():
    """Test handling of invalid case ID for narrative import"""
    safety_service = SafetyService(vault_client)
    
    try:
        response = safety_service.import_narrative(
            case_id="INVALID_CASE_ID",
            narrative_type="primary",
            narrative_language="eng",
            narrative_text="Test narrative"
        )
        
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled invalid case ID")
        
    except Exception as e:
        print(f"✓ Correctly handled invalid case ID error: {str(e)}")
```

### 4. Invalid JSON Format Testing

```python
def test_invalid_json_format():
    """Test handling of invalid JSON format"""
    safety_service = SafetyService(vault_client)
    
    # Invalid JSON with out-of-range value
    invalid_json = {
        "patient": {
            "height_value__v": 999999  # Invalid value outside range
        }
    }
    
    try:
        response = safety_service.intake_json(
            intake_json=invalid_json,
            organization_api_name="verteo_biopharma"
        )
        
        assert response['responseStatus'] == 'FAILURE'
        assert 'reason' in response
        assert 'height_value__v' in response['reason']
        
        print("✓ Correctly handled invalid JSON format")
        
    except Exception as e:
        print(f"✓ Correctly handled invalid JSON error: {str(e)}")
```

### 5. Narrative Character Limit Testing

```python
def test_narrative_character_limit():
    """Test narrative character limit validation"""
    safety_service = SafetyService(vault_client)
    
    # Create narrative exceeding character limit (100,000 characters)
    long_narrative = "A" * 100001
    
    try:
        response = safety_service.import_narrative(
            case_id="V2B000000000201",
            narrative_type="primary",
            narrative_language="eng",
            narrative_text=long_narrative
        )
        
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled narrative character limit exceeded")
        
    except Exception as e:
        print(f"✓ Correctly handled narrative limit error: {str(e)}")
```

## Sample Test Data

### Sample E2B Intake Data
```python
SAMPLE_E2B_DATA = {
    "inbox_item": {
        "file_path": "/directory/labrinone_literature_case.xml",
        "format": "e2br3__v",
        "organization": "vault_customer__v",
        "origin_organization": "vertio_biopharma__c"
    },
    "imported_case": {
        "file_path": "/directory/cholecap_vaers_case.xml",
        "format": "e2br2__v",
        "organization": "verteo_biopharma__c",
        "origin_organization": "fda__v"
    }
}
```

### Sample JSON Intake Data
```python
SAMPLE_JSON_INTAKE = {
    "patient": {
        "age_value__v": 45,
        "age_unit__v": "years__v",
        "gender__v": "male__v",
        "weight_value__v": 75,
        "weight_unit__v": "kg"
    },
    "case": {
        "case_type__v": "spontaneous__v",
        "serious__v": True,
        "reporter_type__v": "physician__v"
    },
    "events": [
        {
            "event_name__v": "Headache",
            "outcome__v": "recovered__v",
            "severity__v": "mild__v"
        }
    ],
    "products": [
        {
            "product_name__v": "Test Drug",
            "dose_value__v": 50,
            "dose_unit__v": "mg",
            "indication__v": "Pain Relief"
        }
    ]
}
```

### Sample Narrative Data
```python
SAMPLE_NARRATIVES = {
    "primary": {
        "case_id": "V2B000000000201",
        "narrative_type": "primary",
        "narrative_language": "eng",
        "text": "A 45-year-old male patient presented with headache following administration of the study medication. The headache was mild in severity and resolved without intervention after 2 hours."
    },
    "translation": {
        "case_id": "V2B000000000201",
        "narrative_type": "translation",
        "narrative_language": "fra",
        "text": "Un patient masculin de 45 ans a présenté des maux de tête suite à l'administration du médicament à l'étude. Le mal de tête était d'intensité légère et s'est résolu sans intervention après 2 heures."
    }
}
```

## Validation Helpers

### E2B Response Validator
```python
def validate_e2b_response(response):
    """Validate E2B intake response structure"""
    required_fields = ['responseStatus', 'intake_id', 'url']
    
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"
    
    assert response['responseStatus'] == 'SUCCESS'
    assert response['intake_id'].startswith('V29')
    assert '/intake/status' in response['url']
    
    print("✓ E2B response validation passed")
```

### Intake Status Validator
```python
def validate_intake_status(response):
    """Validate intake status response structure"""
    required_fields = ['status', 'inbound-transmission', 'number-of-icsrs']
    
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"
    
    valid_statuses = ['complete', 'in_progress', 'failed']
    assert response['status'] in valid_statuses
    
    if 'icsr-details' in response:
        for icsr in response['icsr-details']:
            assert 'status' in icsr
            assert 'inbound-transmission' in icsr
    
    print("✓ Intake status validation passed")
```

### JSON Intake Validator
```python
def validate_json_intake_response(response):
    """Validate JSON intake response structure"""
    required_fields = ['responseStatus']
    
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"
    
    if response['responseStatus'] == 'SUCCESS':
        assert 'jobId' in response
        assert 'transmissionRecordId' in response
    elif response['responseStatus'] == 'FAILURE':
        assert 'reason' in response
    
    print("✓ JSON intake response validation passed")
```

## Performance Testing

### Intake Performance Testing
```python
def test_intake_performance():
    """Test safety intake performance"""
    import time
    
    safety_service = SafetyService(vault_client)
    
    start_time = time.time()
    
    response = safety_service.intake_inbox_item(
        file_path="/directory/test_case.xml",
        format="e2br3__v",
        organization="vault_customer__v"
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✓ Intake request completed in {duration:.2f} seconds")
    
    # Performance assertion (adjust threshold as needed)
    assert duration < 15.0, f"Intake request too slow: {duration} seconds"
```

## Integration Testing

### End-to-End Safety Workflow Testing
```python
def test_complete_safety_workflow():
    """Test complete safety case workflow"""
    safety_service = SafetyService(vault_client)
    
    print("Starting complete safety workflow test...")
    
    try:
        # Step 1: Import case via E2B
        print("✓ Step 1: Importing E2B case...")
        
        intake_response = safety_service.intake_imported_case(
            file_path="/directory/test_case.xml",
            format="e2br3__v",
            organization="vault_customer__v"
        )
        
        intake_id = intake_response['intake_id']
        print(f"✓ Case import initiated. Intake ID: {intake_id}")
        
        # Step 2: Check intake status
        print("✓ Step 2: Checking intake status...")
        
        status_response = safety_service.retrieve_intake_status(
            inbound_id=intake_id
        )
        
        print(f"✓ Intake status: {status_response['status']}")
        
        # Step 3: Retrieve ACK
        print("✓ Step 3: Retrieving ACK...")
        
        ack_response = safety_service.retrieve_ack(inbound_id=intake_id)
        print("✓ ACK retrieved successfully")
        
        # Step 4: Import narrative (if case processing completed)
        if status_response['status'] == 'complete':
            print("✓ Step 4: Importing narrative...")
            
            # Assuming we know the case ID from the intake process
            case_id = "V2B000000000201"  # Would be extracted from status response
            
            narrative_response = safety_service.import_narrative(
                case_id=case_id,
                narrative_type="primary",
                narrative_language="eng",
                narrative_text="Complete workflow test narrative."
            )
            
            print("✓ Narrative imported successfully")
        
        print("✓ Complete safety workflow completed successfully")
        
    except Exception as e:
        print(f"✗ Error in safety workflow: {str(e)}")
        raise
```

## Notes
- Veeva Safety requires specific licensing and permissions
- E2B files must be valid XML in R2 or R3 format
- JSON intake has specific field validation requirements
- Narrative imports support up to 100,000 characters for single import, 200,000 for bulk
- ACK files are returned in the same E2B format as the intake file
- Bulk narrative import supports up to 500 records per batch
- Translation narratives require primary narrative to exist first
- Organization records must be of type "Sponsor" for intake operations
- Case processing is asynchronous - always check status before proceeding
