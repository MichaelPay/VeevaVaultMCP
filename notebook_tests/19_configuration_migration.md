# 19. Configuration Migration API Testing

## Overview
This section covers testing for the Configuration Migration API, which provides functionality for managing Vault Package (VPK) exports, imports, validations, and deployments to migrate configuration changes between Vaults.

## Service Class Under Test
- **Location**: `veevatools.veevavault.services.configuration_migration.configuration_migration.ConfigurationMigrationService`
- **Primary Purpose**: Manage configuration migration operations including VPK package lifecycle
- **API Endpoints Covered**: 11 endpoints for package management, vault comparison, and configuration reporting

## Testing Categories

### 1. Package Export Operations
```python
# Test exporting a Vault Package (VPK) from an Outbound Package
# Tests POST /api/{version}/services/package

def test_export_package():
    """Test VPK package export functionality."""
    config_service = ConfigurationMigrationService(vault_client)
    
    # Test successful package export
    package_name = "Test_Outbound_Package"
    result = config_service.export_package(package_name)
    
    assert result is not None
    assert 'job_id' in result
    assert 'url' in result
    print(f"Export initiated for package: {package_name}")
    print(f"Job ID: {result.get('job_id')}")

def test_export_package_error_handling():
    """Test error handling for package export."""
    config_service = ConfigurationMigrationService(vault_client)
    
    # Test with invalid package name
    try:
        result = config_service.export_package("Invalid_Package_Name")
        assert result.get('responseStatus') == 'FAILURE'
    except Exception as e:
        print(f"Expected error for invalid package: {e}")
```

### 2. Package Import Operations
```python
# Test importing and validating a VPK package
# Tests PUT /api/{version}/services/package

def test_import_package_file_path():
    """Test VPK package import using file path."""
    config_service = ConfigurationMigrationService(vault_client)
    
    vpk_file_path = "path/to/test_package.vpk"
    # Note: Replace with actual VPK file path for real testing
    
    try:
        result = config_service.import_package(vpk_file_path)
        assert result is not None
        assert 'job_id' in result
        assert 'url' in result
        print(f"Import initiated for package: {vpk_file_path}")
    except FileNotFoundError:
        print("VPK file not found - ensure test package exists")

def test_import_package_file_object():
    """Test VPK package import using file object."""
    config_service = ConfigurationMigrationService(vault_client)
    
    # Test with file-like object (mock for testing)
    try:
        with open("test_package.vpk", "rb") as vpk_file:
            result = config_service.import_package(vpk_file)
            assert result is not None
            print("File object import successful")
    except FileNotFoundError:
        print("Test VPK file not available - test with actual package file")
```

### 3. Package Validation Operations
```python
# Test validation of VPK packages
# Tests POST /api/{version}/services/package/actions/validate

def test_validate_package():
    """Test VPK package validation without import."""
    config_service = ConfigurationMigrationService(vault_client)
    
    vpk_file_path = "path/to/test_package.vpk"
    
    try:
        result = config_service.validate_package(vpk_file_path)
        assert result is not None
        print("Package validation completed")
        
        # Check validation results
        if 'validation_results' in result:
            validation_data = result['validation_results']
            print(f"Validation status: {validation_data.get('status')}")
    except FileNotFoundError:
        print("VPK file not found for validation")

def test_validate_inbound_package():
    """Test validation of imported VPK package."""
    config_service = ConfigurationMigrationService(vault_client)
    
    # Use package ID from previous import operation
    package_id = "12345"  # Replace with actual package ID
    
    result = config_service.validate_inbound_package(package_id)
    assert result is not None
    print(f"Inbound package validation for ID: {package_id}")
    
    # Analyze validation results
    if 'validation_results' in result:
        print("Validation Results:")
        for component in result['validation_results'].get('components', []):
            print(f"  Component: {component.get('name')} - Status: {component.get('status')}")
```

### 4. Package Deployment Operations
```python
# Test deploying imported VPK packages
# Tests POST /api/{version}/vobject/vault_package__v/{package_id}/actions/deploy

def test_deploy_package():
    """Test VPK package deployment."""
    config_service = ConfigurationMigrationService(vault_client)
    
    # Use package ID from previous import operation
    package_id = "12345"  # Replace with actual package ID
    
    result = config_service.deploy_package(package_id)
    assert result is not None
    assert 'job_id' in result
    assert 'url' in result
    
    print(f"Deployment initiated for package ID: {package_id}")
    print(f"Job ID: {result.get('job_id')}")

def test_retrieve_package_deploy_results():
    """Test retrieving deployment results."""
    config_service = ConfigurationMigrationService(vault_client)
    
    package_id = "12345"  # Replace with actual deployed package ID
    
    result = config_service.retrieve_package_deploy_results(package_id)
    assert result is not None
    
    print(f"Deployment results for package ID: {package_id}")
    
    # Analyze deployment results
    if 'deployment_status' in result:
        print(f"Deployment Status: {result['deployment_status']}")
    
    if 'deployment_log' in result:
        print(f"Deployment Log URL: {result['deployment_log']}")
    
    if 'data_deployment_log' in result:
        print(f"Data Deployment Log URL: {result['data_deployment_log']}")
```

### 5. Package Dependencies Management
```python
# Test retrieving outbound package dependencies
# Tests GET /api/{version}/vobjects/outbound_package__v/{package_id}/dependencies

def test_retrieve_outbound_package_dependencies():
    """Test retrieving package dependencies."""
    config_service = ConfigurationMigrationService(vault_client)
    
    outbound_package_id = "54321"  # Replace with actual outbound package ID
    
    result = config_service.retrieve_outbound_package_dependencies(outbound_package_id)
    assert result is not None
    
    print(f"Dependencies for outbound package ID: {outbound_package_id}")
    
    # Analyze dependency information
    if 'total_dependencies' in result:
        print(f"Total Dependencies: {result['total_dependencies']}")
    
    if 'package_dependencies' in result:
        print("Package Dependencies:")
        for dep in result['package_dependencies']:
            print(f"  Component: {dep.get('component_name')} - Type: {dep.get('component_type')}")
```

### 6. Component Query Operations
```python
# Test querying component definitions
# Tests POST /api/{version}/query/components

def test_query_component_definitions():
    """Test VQL queries on component definitions."""
    config_service = ConfigurationMigrationService(vault_client)
    
    # Test query for document types
    vql_query = "SELECT id, name__v, mdl_definition__v FROM vault_component__v WHERE component_type__v = 'Doctype'"
    
    result = config_service.query_component_definitions(vql_query)
    assert result is not None
    
    print("Component Definition Query Results:")
    if 'data' in result:
        for component in result['data']:
            print(f"  ID: {component.get('id')} - Name: {component.get('name__v')}")

def test_query_package_components():
    """Test VQL queries on package components."""
    config_service = ConfigurationMigrationService(vault_client)
    
    # Test query for package components
    vql_query = "SELECT id, component_name__v, component_type__v FROM vault_package_component__v"
    
    result = config_service.query_component_definitions(vql_query)
    assert result is not None
    
    print("Package Component Query Results:")
    if 'data' in result:
        component_count = len(result['data'])
        print(f"Total Package Components: {component_count}")
```

### 7. Vault Comparison Operations
```python
# Test comparing configurations between vaults
# Tests POST /api/{version}/objects/vault/actions/compare

def test_compare_vaults_differences():
    """Test vault comparison showing only differences."""
    config_service = ConfigurationMigrationService(vault_client)
    
    target_vault_id = "target_vault_123"  # Replace with actual target vault ID
    
    result = config_service.compare_vaults(
        vault_id=target_vault_id,
        results_type="differences",
        details_type="simple",
        include_doc_binder_templates=True,
        include_vault_settings=True
    )
    
    assert result is not None
    assert 'job_id' in result
    print(f"Vault comparison initiated with target vault: {target_vault_id}")

def test_compare_vaults_complete():
    """Test complete vault configuration comparison."""
    config_service = ConfigurationMigrationService(vault_client)
    
    target_vault_id = "target_vault_123"
    
    result = config_service.compare_vaults(
        vault_id=target_vault_id,
        results_type="complete",
        details_type="complex",
        component_types="Doclifecycle,Doctype,Workflow",
        generate_outbound_packages=True
    )
    
    assert result is not None
    print("Complete vault comparison with outbound package generation")

def test_compare_vaults_specific_components():
    """Test vault comparison for specific component types."""
    config_service = ConfigurationMigrationService(vault_client)
    
    target_vault_id = "target_vault_123"
    
    result = config_service.compare_vaults(
        vault_id=target_vault_id,
        results_type="differences",
        details_type="simple",
        component_types="Doctype,Object",
        include_doc_binder_templates=False,
        include_vault_settings=False
    )
    
    assert result is not None
    print("Vault comparison for specific component types completed")
```

### 8. Configuration Reporting
```python
# Test generating configuration reports
# Tests POST /api/{version}/objects/vault/actions/configreport

def test_generate_configuration_report_default():
    """Test generating default configuration report."""
    config_service = ConfigurationMigrationService(vault_client)
    
    result = config_service.generate_configuration_report()
    assert result is not None
    assert 'job_id' in result
    
    print("Configuration report generation initiated")
    print(f"Job ID: {result.get('job_id')}")

def test_generate_configuration_report_custom():
    """Test generating custom configuration report."""
    config_service = ConfigurationMigrationService(vault_client)
    
    result = config_service.generate_configuration_report(
        include_vault_settings=True,
        include_inactive_components=True,
        include_components_modified_since="2024-01-01",
        include_doc_binder_templates=False,
        suppress_empty_results=True,
        component_types="Doctype,Object,Workflow",
        output_format="Excel"
    )
    
    assert result is not None
    print("Custom configuration report with specific filters generated")

def test_generate_configuration_report_macro_enabled():
    """Test generating macro-enabled Excel report."""
    config_service = ConfigurationMigrationService(vault_client)
    
    result = config_service.generate_configuration_report(
        output_format="Excel_Macro_Enabled",
        include_inactive_components=False,
        suppress_empty_results=True
    )
    
    assert result is not None
    print("Macro-enabled Excel configuration report generated")
```

### 9. Configuration Mode Management
```python
# Test enabling and disabling configuration mode
# Tests POST /api/{version}/services/configuration_mode/actions/enable|disable

def test_enable_configuration_mode():
    """Test enabling configuration mode."""
    config_service = ConfigurationMigrationService(vault_client)
    
    result = config_service.enable_configuration_mode()
    assert result is not None
    
    if result.get('responseStatus') == 'SUCCESS':
        print("Configuration mode enabled successfully")
        print("Non-admin users are now locked out of the vault")
    else:
        print(f"Configuration mode enable failed: {result.get('errors')}")

def test_disable_configuration_mode():
    """Test disabling configuration mode."""
    config_service = ConfigurationMigrationService(vault_client)
    
    result = config_service.disable_configuration_mode()
    assert result is not None
    
    if result.get('responseStatus') == 'SUCCESS':
        print("Configuration mode disabled successfully")
        print("Non-admin users can now access the vault")
    else:
        print(f"Configuration mode disable failed: {result.get('errors')}")

def test_configuration_mode_permissions():
    """Test configuration mode with different user permissions."""
    config_service = ConfigurationMigrationService(vault_client)
    
    # Test enabling with appropriate permissions
    try:
        result = config_service.enable_configuration_mode()
        
        if result.get('responseStatus') == 'SUCCESS':
            print("Configuration mode enabled - user has appropriate permissions")
            
            # Disable it again
            disable_result = config_service.disable_configuration_mode()
            assert disable_result.get('responseStatus') == 'SUCCESS'
            
        else:
            print("User may not have configuration mode permissions")
            
    except Exception as e:
        print(f"Configuration mode operation failed: {e}")
```

### 10. Integration Testing
```python
# Test complete VPK lifecycle workflows

def test_complete_vpk_workflow():
    """Test complete VPK package workflow."""
    config_service = ConfigurationMigrationService(vault_client)
    
    print("=== Complete VPK Workflow Test ===")
    
    # Step 1: Export package
    package_name = "Test_Configuration_Package"
    export_result = config_service.export_package(package_name)
    assert export_result is not None
    print(f"1. Package export initiated: {export_result.get('job_id')}")
    
    # Step 2: Validate package (once available)
    vpk_file_path = "exported_package.vpk"  # Would be downloaded after export
    try:
        validation_result = config_service.validate_package(vpk_file_path)
        print("2. Package validation completed")
    except FileNotFoundError:
        print("2. Package validation skipped - file not available")
    
    # Step 3: Import package
    try:
        import_result = config_service.import_package(vpk_file_path)
        package_id = "imported_package_id"  # Would be from import result
        print(f"3. Package imported: {import_result.get('job_id')}")
        
        # Step 4: Validate imported package
        inbound_validation = config_service.validate_inbound_package(package_id)
        print("4. Inbound package validation completed")
        
        # Step 5: Deploy package
        deploy_result = config_service.deploy_package(package_id)
        print(f"5. Package deployment initiated: {deploy_result.get('job_id')}")
        
        # Step 6: Retrieve deployment results
        results = config_service.retrieve_package_deploy_results(package_id)
        print("6. Deployment results retrieved")
        
    except FileNotFoundError:
        print("3-6. Import/Deploy workflow skipped - package file not available")

def test_vault_comparison_and_report_workflow():
    """Test vault comparison and reporting workflow."""
    config_service = ConfigurationMigrationService(vault_client)
    
    print("=== Vault Comparison and Reporting Workflow ===")
    
    # Step 1: Compare vaults
    target_vault_id = "comparison_target_vault"
    comparison_result = config_service.compare_vaults(
        vault_id=target_vault_id,
        results_type="differences",
        generate_outbound_packages=True
    )
    print("1. Vault comparison initiated")
    
    # Step 2: Generate configuration report
    report_result = config_service.generate_configuration_report(
        include_inactive_components=False,
        output_format="Excel"
    )
    print("2. Configuration report generation initiated")
    
    # Step 3: Query component definitions
    component_query = "SELECT id, name__v FROM vault_component__v LIMIT 10"
    query_result = config_service.query_component_definitions(component_query)
    print(f"3. Component query completed - {len(query_result.get('data', []))} components")

def test_dependency_analysis_workflow():
    """Test package dependency analysis workflow."""
    config_service = ConfigurationMigrationService(vault_client)
    
    print("=== Dependency Analysis Workflow ===")
    
    # Step 1: Retrieve outbound package dependencies
    outbound_package_id = "test_outbound_package"
    dependencies_result = config_service.retrieve_outbound_package_dependencies(outbound_package_id)
    
    if dependencies_result.get('total_dependencies', 0) > 0:
        print(f"1. Found {dependencies_result['total_dependencies']} dependencies")
        
        # Step 2: Analyze dependency components
        for dep in dependencies_result.get('package_dependencies', []):
            component_type = dep.get('component_type')
            component_name = dep.get('component_name')
            print(f"   Dependency: {component_name} ({component_type})")
            
    else:
        print("1. No outstanding dependencies found")
    
    # Step 3: Query related components
    component_query = f"SELECT id, name__v, component_type__v FROM vault_component__v WHERE component_type__v IN ('Doctype', 'Object')"
    query_result = config_service.query_component_definitions(component_query)
    print(f"2. Related components query: {len(query_result.get('data', []))} results")
```

### 11. Error Handling and Edge Cases
```python
def test_error_handling():
    """Test various error conditions."""
    config_service = ConfigurationMigrationService(vault_client)
    
    # Test invalid package export
    try:
        result = config_service.export_package("NonExistent_Package")
        assert result.get('responseStatus') == 'FAILURE'
        print("Invalid package export handled correctly")
    except Exception as e:
        print(f"Export error handling: {e}")
    
    # Test invalid package deployment
    try:
        result = config_service.deploy_package("invalid_package_id")
        assert result.get('responseStatus') == 'FAILURE'
        print("Invalid package deployment handled correctly")
    except Exception as e:
        print(f"Deploy error handling: {e}")
    
    # Test invalid VQL query
    try:
        result = config_service.query_component_definitions("INVALID VQL SYNTAX")
        assert result.get('responseStatus') == 'FAILURE'
        print("Invalid VQL query handled correctly")
    except Exception as e:
        print(f"VQL error handling: {e}")
    
    # Test invalid vault comparison
    try:
        result = config_service.compare_vaults("invalid_vault_id")
        assert result.get('responseStatus') == 'FAILURE'
        print("Invalid vault comparison handled correctly")
    except Exception as e:
        print(f"Vault comparison error handling: {e}")

def test_permission_checks():
    """Test permission requirements for various operations."""
    config_service = ConfigurationMigrationService(vault_client)
    
    operations_to_test = [
        ("Configuration Mode Enable", lambda: config_service.enable_configuration_mode()),
        ("Configuration Report", lambda: config_service.generate_configuration_report()),
        ("Vault Comparison", lambda: config_service.compare_vaults("test_vault_id")),
        ("Package Export", lambda: config_service.export_package("test_package")),
    ]
    
    for operation_name, operation_func in operations_to_test:
        try:
            result = operation_func()
            if result.get('responseStatus') == 'SUCCESS':
                print(f"{operation_name}: User has required permissions")
            else:
                print(f"{operation_name}: Permission check - {result.get('errors', ['Unknown error'])[0]}")
        except Exception as e:
            print(f"{operation_name}: Exception - {e}")
```

## Service Integration Points

### Related Services
- **Object Services**: For managing vault_package__v and outbound_package__v objects
- **Job Services**: For monitoring asynchronous package operations
- **Document Services**: For document and binder template configurations
- **Security Services**: For managing configuration mode and access controls

### Authentication Requirements
- **Basic Operations**: Standard API access permissions
- **Configuration Mode**: Vault Owner or System Admin permissions
- **Configuration Reports**: Vault Configuration Report permission
- **Cross-Vault Operations**: Cross-domain user access required

### Asynchronous Operations
Most configuration migration operations are asynchronous and return job IDs:
- Package export, import, and deployment
- Vault comparison operations
- Configuration report generation
- Package validation (for complex packages)

## Best Practices for Testing

1. **Test File Management**: Ensure test VPK files are available and properly formatted
2. **Job Monitoring**: Implement job status checking for asynchronous operations
3. **Permission Testing**: Test operations with different user permission levels
4. **Error Scenarios**: Test invalid inputs and insufficient permissions
5. **Cleanup**: Properly manage test packages and configuration changes
6. **Cross-Vault Testing**: Use separate test vaults for comparison operations
7. **Backup Considerations**: Test in non-production environments due to configuration changes

## Notes
- Configuration Migration operations can significantly impact vault functionality
- Test in dedicated development/test environments only
- VPK files contain sensitive configuration data - handle securely
- Configuration Mode locks out non-admin users - use carefully in testing
- Some operations require specific vault configurations and permissions
- Deployment operations may have dependencies that need to be resolved first
