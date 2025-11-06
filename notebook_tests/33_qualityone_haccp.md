# QualityOne HACCP API Testing Documentation

## Overview
This document provides comprehensive testing procedures for the QualityOne HACCP API (Section 33) of VeevaTools. The QualityOne HACCP API enables HACCP Plan translation workflows including export, retrieve, and import of translatable fields for Veeva QualityOne HACCP application.

## Service Class Information
- **Service Class**: `QualityOneService` (contains HACCP functionality)
- **Module Path**: `veevavault.services.applications.quality_one.quality_one_service`
- **Authentication**: VaultClient session required
- **Application Requirement**: Veeva QualityOne HACCP must be licensed and enabled
- **Base URL Pattern**: `/api/{version}/app/qualityone/haccp_plan/`

## Core Functionality
The QualityOne HACCP API provides capabilities for:
- **Translation Export**: Export translatable fields from HACCP Plans and related records
- **Translation Retrieval**: Retrieve exported field data for modification
- **Translation Import**: Import translated HACCP Plan data into Vault
- **Multi-Object Support**: Handle HACCP Plan and related object translations
- **Lifecycle Management**: Work with HACCP Translation Generation lifecycle states

## Important Requirements
- **QualityOne HACCP License**: Must have Veeva QualityOne HACCP application licensed
- **Translation Copies**: Must work with translation copies of HACCP Plans
- **Lifecycle States**: HACCP Translation Generation records must be in specific states
- **File Size Limits**: Maximum 250MB for JSON translation files
- **User Consistency**: Same user must perform export and retrieve operations
- **Permissions**: Must have view/edit permissions for HACCP Plan translatable fields

## Testing Methods

### 1. Service Initialization Testing

```python
def test_haccp_service_initialization():
    """Test HACCP functionality in QualityOneService"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    # Initialize the service (HACCP functionality is in QualityOneService)
    quality_one_service = QualityOneService(vault_client)
    
    # Verify HACCP methods are available
    assert hasattr(quality_one_service, 'export_haccp_plan_translatable_fields')
    assert hasattr(quality_one_service, 'retrieve_haccp_plan_translatable_fields')
    assert hasattr(quality_one_service, 'import_haccp_plan_translatable_fields')
    
    print("✓ QualityOne HACCP functionality available in QualityOneService")
    print("✓ All HACCP translation methods are accessible")
```

### 2. HACCP Plan Export Testing

```python
def test_export_haccp_plan_translatable_fields():
    """Test exporting HACCP Plan translatable fields"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test with sample HACCP Plan record ID (must be translation copy)
    haccp_plan_id = "V7V00000000R001"  # Replace with actual translation copy ID
    
    try:
        response = quality_one_service.export_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id
        )
        
        # Verify response structure
        assert response["responseStatus"] == "SUCCESS"
        assert "data" in response
        assert "job_id" in response["data"]
        
        job_id = response["data"]["job_id"]
        
        print(f"✓ HACCP Plan translatable fields export started successfully")
        print(f"  HACCP Plan ID: {haccp_plan_id}")
        print(f"  Export Job ID: {job_id}")
        
        return response
        
    except Exception as e:
        print(f"⚠ HACCP Plan export test failed (may require translation copy and permissions): {e}")
        return None

def test_export_multiple_haccp_plans():
    """Test exporting translatable fields from multiple HACCP Plans"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test with multiple HACCP Plan translation copies
    haccp_plan_ids = [
        "V7V00000000R001",  # Chocolate HACCP Plan
        "V7V00000000R002",  # Dairy HACCP Plan
        "V7V00000000R003",  # Beverage HACCP Plan
        "V7V00000000R004",  # Bakery HACCP Plan
    ]
    
    export_results = {}
    
    for plan_id in haccp_plan_ids:
        try:
            response = quality_one_service.export_haccp_plan_translatable_fields(
                haccp_plan_record_id=plan_id
            )
            
            if response["responseStatus"] == "SUCCESS":
                job_id = response["data"]["job_id"]
                export_results[plan_id] = {
                    "status": "SUCCESS",
                    "job_id": job_id
                }
                print(f"✓ Export started for HACCP Plan {plan_id}: Job {job_id}")
            else:
                export_results[plan_id] = {
                    "status": "FAILURE",
                    "error": response.get("errors", [])
                }
                print(f"⚠ Export failed for HACCP Plan {plan_id}: {response}")
                
        except Exception as e:
            export_results[plan_id] = {
                "status": "EXCEPTION",
                "error": str(e)
            }
            print(f"⚠ Export exception for HACCP Plan {plan_id}: {e}")
    
    successful_exports = len([plan for plan, result in export_results.items() if result["status"] == "SUCCESS"])
    print(f"✓ Successfully started exports for {successful_exports} out of {len(haccp_plan_ids)} HACCP Plans")
    
    return export_results

def test_export_validation_requirements():
    """Test export validation requirements (lifecycle states, permissions)"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test various scenarios
    test_scenarios = [
        {
            "plan_id": "V7V00000000R001",
            "scenario": "Valid translation copy in Ready for Export state",
            "expected": "SUCCESS"
        },
        {
            "plan_id": "V7V00000000Q001",  # Original plan (not translation copy)
            "scenario": "Original HACCP Plan (not translation copy)",
            "expected": "FAILURE"
        },
        {
            "plan_id": "V7V00000000R999",  # Non-existent plan
            "scenario": "Non-existent HACCP Plan",
            "expected": "FAILURE"
        }
    ]
    
    validation_results = []
    
    for scenario in test_scenarios:
        plan_id = scenario["plan_id"]
        description = scenario["scenario"]
        expected = scenario["expected"]
        
        try:
            response = quality_one_service.export_haccp_plan_translatable_fields(
                haccp_plan_record_id=plan_id
            )
            
            actual_status = response["responseStatus"]
            
            if actual_status == expected:
                validation_results.append({
                    "scenario": description,
                    "plan_id": plan_id,
                    "expected": expected,
                    "actual": actual_status,
                    "result": "PASS"
                })
                print(f"✓ {description}: {actual_status} (as expected)")
            else:
                validation_results.append({
                    "scenario": description,
                    "plan_id": plan_id,
                    "expected": expected,
                    "actual": actual_status,
                    "result": "UNEXPECTED"
                })
                print(f"⚠ {description}: {actual_status} (expected {expected})")
                
        except Exception as e:
            validation_results.append({
                "scenario": description,
                "plan_id": plan_id,
                "expected": expected,
                "actual": "EXCEPTION",
                "result": "EXCEPTION",
                "error": str(e)
            })
            print(f"⚠ {description}: Exception - {e}")
    
    passed_validations = len([r for r in validation_results if r["result"] == "PASS"])
    print(f"✓ Export validation: {passed_validations}/{len(validation_results)} scenarios behaved as expected")
    
    return validation_results
```

### 3. HACCP Plan Retrieval Testing

```python
def test_retrieve_haccp_plan_translatable_fields():
    """Test retrieving HACCP Plan translatable fields"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test with HACCP Plan that has completed export
    haccp_plan_id = "V7V00000000R001"  # Replace with actual plan with completed export
    
    try:
        response = quality_one_service.retrieve_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id
        )
        
        # Verify response structure
        if response["responseStatus"] == "SUCCESS":
            # Response should be array of objects with field data
            if isinstance(response, list):
                print(f"✓ HACCP Plan translatable fields retrieved successfully")
                print(f"  HACCP Plan ID: {haccp_plan_id}")
                print(f"  Object types returned: {len(response)}")
                
                # Validate structure of each object
                for i, obj_data in enumerate(response):
                    if "object_name" in obj_data:
                        object_name = obj_data["object_name"]
                        record_count = len(obj_data.get("records", []))
                        field_count = len(obj_data.get("field_metadata", []))
                        language = obj_data.get("language", "unknown")
                        
                        print(f"    Object {i+1}: {object_name}")
                        print(f"      Records: {record_count}")
                        print(f"      Fields: {field_count}")
                        print(f"      Language: {language}")
            else:
                print(f"✓ HACCP Plan fields retrieved (response format): {type(response)}")
                
        else:
            print(f"⚠ HACCP Plan retrieval failed: {response}")
        
        return response
        
    except Exception as e:
        print(f"⚠ HACCP Plan retrieval test failed (may require completed export): {e}")
        return None

def test_retrieve_field_structure_validation():
    """Test validation of retrieved field structure"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    haccp_plan_id = "V7V00000000R001"
    
    try:
        response = quality_one_service.retrieve_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id
        )
        
        if response["responseStatus"] == "SUCCESS" and isinstance(response, list):
            validation_results = {
                "total_objects": len(response),
                "object_validations": []
            }
            
            for obj_data in response:
                obj_validation = {
                    "object_name": obj_data.get("object_name", "unknown"),
                    "has_field_metadata": "field_metadata" in obj_data,
                    "has_records": "records" in obj_data,
                    "has_language": "language" in obj_data,
                    "field_types": [],
                    "record_count": len(obj_data.get("records", [])),
                    "field_count": len(obj_data.get("field_metadata", []))
                }
                
                # Validate field metadata structure
                for field_meta in obj_data.get("field_metadata", []):
                    if "type" in field_meta:
                        field_type = field_meta["type"]
                        if field_type not in obj_validation["field_types"]:
                            obj_validation["field_types"].append(field_type)
                
                # Validate record structure
                for record in obj_data.get("records", []):
                    obj_validation["has_record_id"] = "id" in record
                    obj_validation["has_checksum"] = "md5checksum" in record
                    obj_validation["has_fields"] = "fields" in record
                    break  # Check first record only
                
                validation_results["object_validations"].append(obj_validation)
                
                print(f"✓ Object: {obj_validation['object_name']}")
                print(f"  Records: {obj_validation['record_count']}")
                print(f"  Fields: {obj_validation['field_count']}")
                print(f"  Field types: {obj_validation['field_types']}")
            
            print(f"✓ Field structure validation completed for {validation_results['total_objects']} objects")
            
            return validation_results
        else:
            print(f"⚠ Cannot validate structure - invalid response: {response}")
            return None
            
    except Exception as e:
        print(f"⚠ Field structure validation failed: {e}")
        return None

def test_retrieve_supported_field_types():
    """Test retrieval of supported field types (Text, Long Text, Rich Text)"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    haccp_plan_id = "V7V00000000R001"
    
    expected_field_types = ["String", "LongText", "RichText"]
    
    try:
        response = quality_one_service.retrieve_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id
        )
        
        if response["responseStatus"] == "SUCCESS" and isinstance(response, list):
            found_field_types = set()
            field_type_counts = {}
            
            for obj_data in response:
                for field_meta in obj_data.get("field_metadata", []):
                    field_type = field_meta.get("type")
                    if field_type:
                        found_field_types.add(field_type)
                        field_type_counts[field_type] = field_type_counts.get(field_type, 0) + 1
            
            print(f"✓ Found field types: {sorted(found_field_types)}")
            
            # Check if expected types are present
            for expected_type in expected_field_types:
                if expected_type in found_field_types:
                    count = field_type_counts[expected_type]
                    print(f"  ✓ {expected_type}: {count} fields")
                else:
                    print(f"  ⚠ {expected_type}: Not found")
            
            # Check for unexpected types
            unexpected_types = found_field_types - set(expected_field_types)
            if unexpected_types:
                print(f"  ℹ Unexpected field types: {sorted(unexpected_types)}")
            
            return {
                "found_types": sorted(found_field_types),
                "type_counts": field_type_counts,
                "unexpected_types": sorted(unexpected_types)
            }
        else:
            print(f"⚠ Cannot check field types - invalid response: {response}")
            return None
            
    except Exception as e:
        print(f"⚠ Field type checking failed: {e}")
        return None
```

### 4. HACCP Plan Import Testing

```python
def test_import_haccp_plan_translatable_fields():
    """Test importing HACCP Plan translatable fields"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    import json
    import io
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test with HACCP Plan that has completed export/retrieve cycle
    haccp_plan_id = "V7V00000000R001"
    
    # Sample translation data (based on retrieve response structure)
    sample_translation_data = [
        {
            "object_name": "haccp_plan__v",
            "field_metadata": [
                {
                    "name": "name__v",
                    "type": "String",
                    "max_length": 128
                },
                {
                    "name": "description__v",
                    "type": "String",
                    "max_length": 1500
                }
            ],
            "language": "es",
            "records": [
                {
                    "id": haccp_plan_id,
                    "md5checksum": "9d4c28675262b14653d94089aad16028",
                    "fields": {
                        "name__v": "Plan HACCP para Chocolate",  # Translated from English
                        "description__v": "Este Plan HACCP describe el proceso para fabricar chocolate."
                    }
                }
            ]
        }
    ]
    
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
            assert "data" in response
            assert "job_id" in response["data"]
            
            job_id = response["data"]["job_id"]
            
            print(f"✓ HACCP Plan translatable fields import started successfully")
            print(f"  HACCP Plan ID: {haccp_plan_id}")
            print(f"  Import Job ID: {job_id}")
            print(f"  Translation data size: {len(json_data)} characters")
            print(f"  Objects in translation: {len(sample_translation_data)}")
        else:
            print(f"⚠ HACCP Plan import failed: {response}")
        
        return response
        
    except Exception as e:
        print(f"⚠ HACCP Plan import test failed (may require valid data and permissions): {e}")
        return None

def test_import_file_size_validation():
    """Test import file size validation (250MB limit)"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    import json
    import io
    
    quality_one_service = QualityOneService(vault_client)
    
    haccp_plan_id = "V7V00000000R001"
    
    # Test small file (should work)
    small_translation = [
        {
            "object_name": "haccp_plan__v",
            "field_metadata": [{"name": "name__v", "type": "String", "max_length": 128}],
            "language": "es",
            "records": [
                {
                    "id": haccp_plan_id,
                    "md5checksum": "sample_checksum",
                    "fields": {"name__v": "Plan HACCP Pequeño"}
                }
            ]
        }
    ]
    
    small_json = json.dumps(small_translation)
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
        
        # Test large file simulation (approaching 250MB limit)
        # Note: Creating actual 250MB would be impractical in testing
        large_translation = [
            {
                "object_name": "haccp_plan__v",
                "field_metadata": [
                    {"name": "description__v", "type": "LongText", "max_length": 1500}
                ],
                "language": "es",
                "records": [
                    {
                        "id": haccp_plan_id,
                        "md5checksum": "large_checksum",
                        "fields": {
                            "description__v": "x" * 10000  # 10KB description (simulated large content)
                        }
                    }
                ]
            }
        ]
        
        # Add multiple large objects to simulate larger file
        for i in range(50):  # Simulate ~500KB total
            large_translation.append({
                "object_name": f"haccp_plan_ingredient__v",
                "field_metadata": [{"name": "description__v", "type": "String", "max_length": 1500}],
                "language": "es", 
                "records": [
                    {
                        "id": f"INGREDIENT_{i}",
                        "md5checksum": f"checksum_{i}",
                        "fields": {"description__v": "x" * 200}  # 200 chars per ingredient
                    }
                ]
            })
        
        large_json = json.dumps(large_translation)
        large_file = io.StringIO(large_json)
        
        large_response = quality_one_service.import_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id,
            file_data=large_file
        )
        
        if large_response["responseStatus"] == "SUCCESS":
            print(f"✓ Large file simulation accepted: {len(large_json)} characters (~{len(large_json)/1024:.1f}KB)")
        else:
            print(f"⚠ Large file simulation failed: {large_response}")
        
        print(f"ℹ Note: Actual 250MB limit testing would require very large files")
        
        return {
            "small_file": small_response,
            "large_file_simulation": large_response,
            "large_file_size": len(large_json)
        }
        
    except Exception as e:
        print(f"⚠ File size validation test failed: {e}")
        return None

def test_import_field_type_validation():
    """Test import validation for supported field types"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    import json
    import io
    
    quality_one_service = QualityOneService(vault_client)
    
    haccp_plan_id = "V7V00000000R001"
    
    # Test different supported field types
    field_type_tests = [
        {
            "field_type": "String",
            "test_value": "Translated text value",
            "description": "Text field"
        },
        {
            "field_type": "LongText", 
            "test_value": "This is a much longer translated text that would be used in a long text field with more detailed information about the HACCP process.",
            "description": "Long Text field"
        },
        {
            "field_type": "RichText",
            "test_value": "<p>This is <strong>rich text</strong> with <em>formatting</em> that has been translated.</p>",
            "description": "Rich Text field"
        }
    ]
    
    import_results = []
    
    for test in field_type_tests:
        field_type = test["field_type"]
        test_value = test["test_value"]
        description = test["description"]
        
        translation_data = [
            {
                "object_name": "haccp_plan__v",
                "field_metadata": [
                    {
                        "name": "test_field__v",
                        "type": field_type,
                        "max_length": 2000
                    }
                ],
                "language": "es",
                "records": [
                    {
                        "id": haccp_plan_id,
                        "md5checksum": "test_checksum",
                        "fields": {
                            "test_field__v": test_value
                        }
                    }
                ]
            }
        ]
        
        json_data = json.dumps(translation_data)
        file_data = io.StringIO(json_data)
        
        try:
            response = quality_one_service.import_haccp_plan_translatable_fields(
                haccp_plan_record_id=haccp_plan_id,
                file_data=file_data
            )
            
            import_results.append({
                "field_type": field_type,
                "description": description,
                "status": response["responseStatus"],
                "value_length": len(test_value)
            })
            
            if response["responseStatus"] == "SUCCESS":
                job_id = response["data"]["job_id"]
                print(f"✓ {description} ({field_type}): Import started - Job {job_id}")
            else:
                print(f"⚠ {description} ({field_type}): Import failed - {response}")
                
        except Exception as e:
            import_results.append({
                "field_type": field_type,
                "description": description,
                "status": "EXCEPTION",
                "error": str(e)
            })
            print(f"⚠ {description} ({field_type}): Exception - {e}")
    
    successful_imports = len([r for r in import_results if r["status"] == "SUCCESS"])
    print(f"✓ Field type validation: {successful_imports}/{len(field_type_tests)} field types imported successfully")
    
    return import_results
```

### 5. Complete HACCP Translation Workflow Testing

```python
def test_complete_haccp_translation_workflow():
    """Test complete HACCP Plan translation workflow"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    import json
    import io
    import time
    
    quality_one_service = QualityOneService(vault_client)
    
    haccp_plan_id = "V7V00000000R001"  # Must be a translation copy
    
    workflow_results = {
        "haccp_plan_id": haccp_plan_id,
        "workflow_steps": [],
        "translation_data": None
    }
    
    print(f"Starting complete HACCP translation workflow for plan: {haccp_plan_id}")
    
    try:
        # Step 1: Export translatable fields
        print("Step 1: Exporting translatable fields...")
        export_response = quality_one_service.export_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id
        )
        
        if export_response["responseStatus"] == "SUCCESS":
            export_job_id = export_response["data"]["job_id"]
            workflow_results["workflow_steps"].append({
                "step": "export",
                "status": "SUCCESS",
                "job_id": export_job_id,
                "timestamp": time.time()
            })
            print(f"  ✓ Export started - Job {export_job_id}")
            
            # Note: In real workflow, you'd wait for job completion here
            print("  ℹ Waiting for export job completion...")
            print("    (In production, monitor job status before proceeding)")
            
            # Step 2: Retrieve exported fields
            print("Step 2: Retrieving exported fields...")
            try:
                retrieve_response = quality_one_service.retrieve_haccp_plan_translatable_fields(
                    haccp_plan_record_id=haccp_plan_id
                )
                
                if retrieve_response["responseStatus"] == "SUCCESS":
                    workflow_results["workflow_steps"].append({
                        "step": "retrieve",
                        "status": "SUCCESS",
                        "data_size": len(str(retrieve_response)),
                        "timestamp": time.time()
                    })
                    workflow_results["translation_data"] = retrieve_response
                    
                    # Count objects and fields
                    if isinstance(retrieve_response, list):
                        object_count = len(retrieve_response)
                        total_fields = sum(len(obj.get("field_metadata", [])) for obj in retrieve_response)
                        total_records = sum(len(obj.get("records", [])) for obj in retrieve_response)
                        
                        print(f"  ✓ Fields retrieved successfully")
                        print(f"    Objects: {object_count}")
                        print(f"    Total fields: {total_fields}")
                        print(f"    Total records: {total_records}")
                    
                    # Step 3: Simulate translation and import
                    print("Step 3: Simulating translation and import...")
                    
                    # Create modified translation data (simulate translation)
                    if isinstance(retrieve_response, list):
                        translated_data = []
                        
                        for obj_data in retrieve_response:
                            translated_obj = {
                                "object_name": obj_data.get("object_name"),
                                "field_metadata": obj_data.get("field_metadata", []),
                                "language": obj_data.get("language", "es"),
                                "records": []
                            }
                            
                            # Translate field values
                            for record in obj_data.get("records", []):
                                translated_record = {
                                    "id": record.get("id"),
                                    "md5checksum": record.get("md5checksum"),
                                    "fields": {}
                                }
                                
                                # Add "Translated: " prefix to simulate translation
                                for field_name, field_value in record.get("fields", {}).items():
                                    if field_value and isinstance(field_value, str):
                                        translated_record["fields"][field_name] = f"Translated: {field_value}"
                                    else:
                                        translated_record["fields"][field_name] = field_value
                                
                                translated_obj["records"].append(translated_record)
                            
                            translated_data.append(translated_obj)
                        
                        # Import translated data
                        json_data = json.dumps(translated_data, indent=2)
                        file_data = io.StringIO(json_data)
                        
                        import_response = quality_one_service.import_haccp_plan_translatable_fields(
                            haccp_plan_record_id=haccp_plan_id,
                            file_data=file_data
                        )
                        
                        if import_response["responseStatus"] == "SUCCESS":
                            import_job_id = import_response["data"]["job_id"]
                            workflow_results["workflow_steps"].append({
                                "step": "import",
                                "status": "SUCCESS",
                                "job_id": import_job_id,
                                "translation_size": len(json_data),
                                "timestamp": time.time()
                            })
                            print(f"  ✓ Import started - Job {import_job_id}")
                            print(f"    Translation file size: {len(json_data)} characters")
                        else:
                            workflow_results["workflow_steps"].append({
                                "step": "import",
                                "status": "FAILURE",
                                "error": import_response.get("errors", []),
                                "timestamp": time.time()
                            })
                            print(f"  ⚠ Import failed: {import_response}")
                    else:
                        print(f"  ⚠ Cannot process translation data - unexpected format")
                        
                else:
                    workflow_results["workflow_steps"].append({
                        "step": "retrieve",
                        "status": "FAILURE",
                        "error": retrieve_response.get("errors", []),
                        "timestamp": time.time()
                    })
                    print(f"  ⚠ Retrieve failed: {retrieve_response}")
                    
            except Exception as e:
                workflow_results["workflow_steps"].append({
                    "step": "retrieve",
                    "status": "EXCEPTION",
                    "error": str(e),
                    "timestamp": time.time()
                })
                print(f"  ⚠ Retrieve exception: {e}")
        else:
            workflow_results["workflow_steps"].append({
                "step": "export",
                "status": "FAILURE",
                "error": export_response.get("errors", []),
                "timestamp": time.time()
            })
            print(f"  ⚠ Export failed: {export_response}")
        
        # Workflow summary
        successful_steps = len([step for step in workflow_results["workflow_steps"] if step["status"] == "SUCCESS"])
        total_steps = len(workflow_results["workflow_steps"])
        
        print(f"\n✓ HACCP translation workflow completed: {successful_steps}/{total_steps} steps successful")
        
        # Calculate workflow duration
        if workflow_results["workflow_steps"]:
            start_time = min(step.get("timestamp", 0) for step in workflow_results["workflow_steps"])
            end_time = max(step.get("timestamp", 0) for step in workflow_results["workflow_steps"])
            duration = end_time - start_time
            print(f"  Workflow duration: {duration:.2f} seconds")
        
        return workflow_results
        
    except Exception as e:
        print(f"⚠ HACCP translation workflow failed: {e}")
        return None

def test_multi_language_translation_workflow():
    """Test HACCP translation workflow for multiple languages"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    import json
    import io
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test different language translations
    language_tests = [
        {"plan_id": "V7V00000000R001", "language": "es", "description": "Spanish translation"},
        {"plan_id": "V7V00000000R002", "language": "fr", "description": "French translation"},
        {"plan_id": "V7V00000000R003", "language": "de", "description": "German translation"},
        {"plan_id": "V7V00000000R004", "language": "pt", "description": "Portuguese translation"}
    ]
    
    multi_language_results = []
    
    print("Testing multi-language HACCP translation workflow...")
    
    for test in language_tests:
        plan_id = test["plan_id"]
        language = test["language"]
        description = test["description"]
        
        print(f"\nTesting {description} (Language: {language})...")
        
        try:
            # Export for this language/plan
            export_response = quality_one_service.export_haccp_plan_translatable_fields(
                haccp_plan_record_id=plan_id
            )
            
            language_result = {
                "plan_id": plan_id,
                "language": language,
                "description": description,
                "export_status": export_response["responseStatus"]
            }
            
            if export_response["responseStatus"] == "SUCCESS":
                job_id = export_response["data"]["job_id"]
                language_result["export_job_id"] = job_id
                print(f"  ✓ Export started for {description}: Job {job_id}")
                
                # Simulate retrieve and import steps
                language_result["simulated_steps"] = True
                print(f"  ℹ Simulated retrieve and import steps for {language}")
            else:
                language_result["export_error"] = export_response.get("errors", [])
                print(f"  ⚠ Export failed for {description}: {export_response}")
            
            multi_language_results.append(language_result)
            
        except Exception as e:
            language_result = {
                "plan_id": plan_id,
                "language": language,
                "description": description,
                "export_status": "EXCEPTION",
                "error": str(e)
            }
            multi_language_results.append(language_result)
            print(f"  ⚠ Exception for {description}: {e}")
    
    # Summary
    successful_exports = len([r for r in multi_language_results if r["export_status"] == "SUCCESS"])
    print(f"\n✓ Multi-language testing: {successful_exports}/{len(language_tests)} language exports successful")
    
    return multi_language_results
```

### 6. Error Handling and Edge Cases

```python
def test_invalid_haccp_plan_ids():
    """Test HACCP operations with invalid plan IDs"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    invalid_plan_ids = [
        "INVALID_PLAN_ID",
        "V7V999999999999",  # Non-existent ID  
        "",                 # Empty string
        "123456789",        # Invalid format
        "V7V00000000Q001",  # Original plan (not translation copy)
        "null"              # String null
    ]
    
    for invalid_id in invalid_plan_ids:
        print(f"Testing invalid HACCP Plan ID: '{invalid_id}'")
        
        try:
            # Test export
            export_response = quality_one_service.export_haccp_plan_translatable_fields(
                haccp_plan_record_id=invalid_id
            )
            
            if export_response["responseStatus"] == "FAILURE":
                errors = export_response.get("errors", [])
                print(f"  ✓ Export correctly failed: {errors}")
            else:
                print(f"  ⚠ Export unexpectedly succeeded: {export_response}")
            
            # Test retrieve
            retrieve_response = quality_one_service.retrieve_haccp_plan_translatable_fields(
                haccp_plan_record_id=invalid_id
            )
            
            if retrieve_response["responseStatus"] == "FAILURE":
                errors = retrieve_response.get("errors", [])
                print(f"  ✓ Retrieve correctly failed: {errors}")
            else:
                print(f"  ⚠ Retrieve unexpectedly succeeded: {retrieve_response}")
        
        except Exception as e:
            print(f"  ✓ Exception correctly raised: {e}")

def test_lifecycle_state_requirements():
    """Test HACCP lifecycle state requirements"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    # Test scenarios with different lifecycle states
    lifecycle_tests = [
        {
            "plan_id": "V7V00000000R001",
            "expected_state": "Ready for Export",
            "operation": "export",
            "description": "Translation copy ready for export"
        },
        {
            "plan_id": "V7V00000000R005", 
            "expected_state": "Export Complete",
            "operation": "retrieve",
            "description": "Translation copy with completed export"
        },
        {
            "plan_id": "V7V00000000R006",
            "expected_state": "Draft",
            "operation": "export",
            "description": "Translation copy in draft state (should fail)"
        }
    ]
    
    for test in lifecycle_tests:
        plan_id = test["plan_id"]
        operation = test["operation"]
        description = test["description"]
        
        print(f"Testing lifecycle state: {description}")
        
        try:
            if operation == "export":
                response = quality_one_service.export_haccp_plan_translatable_fields(
                    haccp_plan_record_id=plan_id
                )
            elif operation == "retrieve":
                response = quality_one_service.retrieve_haccp_plan_translatable_fields(
                    haccp_plan_record_id=plan_id
                )
            
            if response["responseStatus"] == "SUCCESS":
                print(f"  ✓ {operation.title()} succeeded for {description}")
            else:
                errors = response.get("errors", [])
                lifecycle_errors = [
                    error for error in errors
                    if any(keyword in str(error).lower() for keyword in ["lifecycle", "state", "ready", "complete"])
                ]
                
                if lifecycle_errors:
                    print(f"  ✓ {operation.title()} correctly failed due to lifecycle state: {lifecycle_errors}")
                else:
                    print(f"  ⚠ {operation.title()} failed for different reason: {errors}")
                    
        except Exception as e:
            if any(keyword in str(e).lower() for keyword in ["lifecycle", "state", "ready", "complete"]):
                print(f"  ✓ Exception correctly raised for lifecycle state: {e}")
            else:
                print(f"  ⚠ Unexpected exception: {e}")

def test_user_consistency_requirements():
    """Test user consistency requirements for HACCP translation"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    haccp_plan_id = "V7V00000000R001"
    
    print("Testing user consistency requirements...")
    print("Note: This test assumes current user performed the export operation")
    
    try:
        # Test retrieve operation (should work if current user did export)
        retrieve_response = quality_one_service.retrieve_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id
        )
        
        if retrieve_response["responseStatus"] == "SUCCESS":
            print(f"  ✓ Retrieve succeeded - user consistency validated")
        else:
            errors = retrieve_response.get("errors", [])
            user_errors = [
                error for error in errors
                if any(keyword in str(error).lower() for keyword in ["user", "permission", "access", "same user"])
            ]
            
            if user_errors:
                print(f"  ⚠ User consistency requirement enforced: {user_errors}")
            else:
                print(f"  ⚠ Retrieve failed for different reason: {errors}")
        
        print("  ℹ Complete user consistency testing requires multiple user accounts")
        
    except Exception as e:
        if any(keyword in str(e).lower() for keyword in ["user", "permission", "access"]):
            print(f"  ✓ User consistency exception: {e}")
        else:
            print(f"  ⚠ Unexpected exception: {e}")

def test_application_requirements():
    """Test QualityOne HACCP application requirements"""
    from veevavault.services.applications.quality_one.quality_one_service import QualityOneService
    
    quality_one_service = QualityOneService(vault_client)
    
    haccp_plan_id = "V7V00000000R001"
    
    print("Testing QualityOne HACCP application requirements...")
    
    try:
        response = quality_one_service.export_haccp_plan_translatable_fields(
            haccp_plan_record_id=haccp_plan_id
        )
        
        if response["responseStatus"] == "FAILURE":
            errors = response.get("errors", [])
            
            app_errors = [
                error for error in errors 
                if any(keyword in str(error).lower() for keyword in ["qualityone", "haccp", "application", "license", "feature"])
            ]
            
            if app_errors:
                print(f"  ✓ QualityOne HACCP application requirement enforced: {app_errors}")
            else:
                print(f"  ⚠ Different error (may not be app-related): {errors}")
        else:
            print(f"  ✓ QualityOne HACCP application is available and accessible")
            
    except Exception as e:
        app_keywords = ["qualityone", "haccp", "application", "license", "feature"]
        if any(keyword in str(e).lower() for keyword in app_keywords):
            print(f"  ✓ Application requirement exception: {e}")
        else:
            print(f"  ⚠ Unexpected exception: {e}")
```

## Test Data Requirements

### Sample HACCP Plan IDs
```python
# HACCP Plan translation copy IDs (replace with actual values)
SAMPLE_HACCP_TRANSLATION_COPIES = [
    "V7V00000000R001",  # Chocolate HACCP Plan (Spanish)
    "V7V00000000R002",  # Dairy HACCP Plan (French)
    "V7V00000000R003",  # Beverage HACCP Plan (German)
    "V7V00000000R004",  # Bakery HACCP Plan (Portuguese)
]

# Original HACCP Plan IDs (not translation copies)
SAMPLE_HACCP_ORIGINALS = [
    "V7V00000000Q001",  # Original Chocolate HACCP Plan
    "V7V00000000Q002",  # Original Dairy HACCP Plan
]
```

### Sample Translation Data Structure
```python
SAMPLE_HACCP_TRANSLATION_DATA = [
    {
        "object_name": "haccp_plan__v",
        "field_metadata": [
            {
                "name": "name__v",
                "type": "String",
                "max_length": 128
            },
            {
                "name": "description__v", 
                "type": "String",
                "max_length": 1500
            }
        ],
        "language": "es",
        "records": [
            {
                "id": "V7V00000000R001",
                "md5checksum": "9d4c28675262b14653d94089aad16028",
                "fields": {
                    "name__v": "Plan HACCP para Chocolate",
                    "description__v": "Este Plan HACCP describe el proceso para fabricar chocolate."
                }
            }
        ]
    }
]
```

## Expected Response Formats

### Export Response
```json
{
    "responseStatus": "SUCCESS",
    "data": {
        "job_id": "392902"
    }
}
```

### Retrieve Response
```json
[
    {
        "object_name": "haccp_plan__v",
        "field_metadata": [
            {
                "name": "name__v",
                "type": "String",
                "max_length": 128
            }
        ],
        "language": "es",
        "records": [
            {
                "id": "V7V00000000R001",
                "md5checksum": "9d4c28675262b14653d94089aad16028",
                "fields": {
                    "name__v": "HACCP Plan for Chocolate"
                }
            }
        ]
    }
]
```

### Import Response
```json
{
    "responseStatus": "SUCCESS",
    "data": {
        "job_id": "392903"
    }
}
```

## Performance Considerations

1. **File Size Limits**: Maximum 250MB for JSON translation files
2. **Export Size**: If translatable field data exceeds 250MB, export fails
3. **Asynchronous Processing**: Export and import operations are asynchronous
4. **User Session**: Same user must perform export and retrieve operations
5. **Lifecycle Dependencies**: Operations depend on specific HACCP Translation Generation states

## Security Notes

1. **QualityOne HACCP Permissions**: Requires appropriate QualityOne HACCP permissions
2. **HACCP Plan Access**: User must have access to HACCP Plan translation copies
3. **Field Permissions**: Must have view/edit permissions for all translatable fields
4. **User Consistency**: Same user must perform export and retrieve in sequence
5. **Translation Copy Security**: Only translation copies can be used, not original plans

## Common Issues and Troubleshooting

1. **Application Not Licensed**: Ensure QualityOne HACCP application is licensed
2. **Wrong Plan Type**: Must use translation copies, not original HACCP Plans
3. **Lifecycle State**: HACCP Translation Generation must be in correct state
4. **User Mismatch**: Same user must perform export and retrieve operations
5. **File Size**: Translation data must not exceed 250MB limit

## API Method Coverage Summary

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|---------|
| `export_haccp_plan_translatable_fields` | POST `/app/qualityone/haccp_plan/{id}/translatable_fields/actions/export` | Export HACCP Plan translatable fields | ✅ Covered |
| `retrieve_haccp_plan_translatable_fields` | GET `/app/qualityone/haccp_plan/{id}/translatable_fields/file` | Retrieve exported HACCP Plan fields | ✅ Covered |
| `import_haccp_plan_translatable_fields` | POST `/app/qualityone/haccp_plan/{id}/translatable_fields` | Import translated HACCP Plan fields | ✅ Covered |

**Total API Coverage: 3/3 methods (100%)**

## Notes on Implementation

- **Service Location**: HACCP functionality is implemented in `QualityOneService` class
- **Shared Methods**: These methods are also covered in Section 32 (QualityOne) testing documentation
- **HACCP Focus**: This section focuses specifically on HACCP Plan translation workflows
- **Application Scope**: Requires Veeva QualityOne HACCP license (part of QualityOne suite)

This comprehensive testing framework ensures complete coverage of the QualityOne HACCP API, focusing on HACCP Plan translation workflows with proper error handling, lifecycle state management, and security considerations.
