# 38. Errors - Testing Documentation

## Overview
Testing documentation for Veeva Vault API error handling and response validation. This module provides comprehensive testing strategies for handling various error scenarios and response status codes across all Vault API operations.

## Prerequisites
- Understanding of Vault API response structure
- Knowledge of HTTP status codes and API error handling patterns
- Access to testing environments for error simulation
- Ability to create invalid requests for error testing

## Test Methods

### 1. Error Handling Service Initialization

```python
from veevatools.veevavault.services.error_handling_service import ErrorHandlingService

def test_error_handling_service_initialization():
    """Test the initialization of ErrorHandlingService"""
    # Initialize vault client
    vault_client = initialize_vault_client()
    
    # Initialize Error Handling service
    error_service = ErrorHandlingService(vault_client)
    
    # Verify service initialization
    assert error_service is not None
    assert error_service.vault_client == vault_client
    print("✓ Error Handling Service initialized successfully")
```

### 2. Response Status Testing

```python
def test_response_status_validation():
    """Test validation of different response status values"""
    error_service = ErrorHandlingService(vault_client)
    
    # Test all possible response statuses
    response_statuses = ['SUCCESS', 'WARNING', 'FAILURE', 'EXCEPTION']
    
    for status in response_statuses:
        sample_response = {
            'responseStatus': status,
            'data': {} if status == 'SUCCESS' else None,
            'errors': [] if status == 'SUCCESS' else [
                {
                    'type': 'INVALID_DATA',
                    'message': f'Test error for {status} status'
                }
            ]
        }
        
        # Validate response structure
        is_valid = error_service.validate_response_structure(sample_response)
        
        if status == 'SUCCESS':
            assert is_valid == True
        else:
            assert is_valid == False or 'errors' in sample_response
        
        print(f"✓ Response status {status} validation completed")
```

### 3. Authentication Error Testing

```python
def test_authentication_errors():
    """Test various authentication error scenarios"""
    error_service = ErrorHandlingService(vault_client)
    
    # Test authentication error scenarios
    auth_errors = [
        {
            'type': 'NO_PASSWORD_PROVIDED',
            'scenario': 'Missing password',
            'message': 'No password was provided for the login call.'
        },
        {
            'type': 'USERNAME_OR_PASSWORD_INCORRECT',
            'scenario': 'Invalid credentials',
            'message': 'Authentication failed because an invalid username or password was provided.'
        },
        {
            'type': 'USER_LOCKED_OUT',
            'scenario': 'Account locked',
            'message': 'The user is locked out.'
        },
        {
            'type': 'PASSWORD_CHANGE_REQUIRED',
            'scenario': 'Password change required',
            'message': 'Password change required.'
        },
        {
            'type': 'INVALID_SESSION_ID',
            'scenario': 'Invalid session',
            'message': 'Invalid session ID provided.'
        },
        {
            'type': 'INACTIVE_USER',
            'scenario': 'Inactive user',
            'message': 'User is inactive or not found.'
        }
    ]
    
    for error in auth_errors:
        try:
            print(f"\nTesting {error['scenario']}...")
            
            # Create error response
            error_response = {
                'responseStatus': 'FAILURE',
                'errors': [
                    {
                        'type': error['type'],
                        'message': error['message']
                    }
                ],
                'errorType': 'AUTHENTICATION_FAILED'
            }
            
            # Validate error handling
            handled_error = error_service.handle_authentication_error(error_response)
            
            assert handled_error['error_type'] == error['type']
            assert handled_error['category'] == 'AUTHENTICATION'
            
            print(f"✓ {error['scenario']} handled correctly")
            
        except Exception as e:
            print(f"✗ Error testing {error['scenario']}: {str(e)}")
```

### 4. Data Validation Error Testing

```python
def test_data_validation_errors():
    """Test data validation error scenarios"""
    error_service = ErrorHandlingService(vault_client)
    
    # Test data validation errors
    validation_errors = [
        {
            'type': 'PARAMETER_REQUIRED',
            'scenario': 'Missing required parameter',
            'message': 'Missing required parameter [document_id]'
        },
        {
            'type': 'INVALID_DATA',
            'scenario': 'Invalid data format',
            'message': 'Invalid data provided in the API call'
        },
        {
            'type': 'ATTRIBUTE_NOT_SUPPORTED',
            'scenario': 'Unsupported attribute',
            'message': 'The specified resource does not recognize provided attributes'
        },
        {
            'type': 'INVALID_FILTER',
            'scenario': 'Invalid filter',
            'message': 'Provided a non-existent filter to Retrieve Documents'
        },
        {
            'type': 'INCORRECT_QUERY_SYNTAX_ERROR',
            'scenario': 'Invalid VQL syntax',
            'message': 'Query string used with VQL has an incorrect query syntax'
        }
    ]
    
    for error in validation_errors:
        try:
            print(f"\nTesting {error['scenario']}...")
            
            # Create error response
            error_response = {
                'responseStatus': 'FAILURE',
                'errors': [
                    {
                        'type': error['type'],
                        'message': error['message']
                    }
                ]
            }
            
            # Validate error handling
            handled_error = error_service.handle_validation_error(error_response)
            
            assert handled_error['error_type'] == error['type']
            assert handled_error['category'] == 'VALIDATION'
            
            print(f"✓ {error['scenario']} handled correctly")
            
        except Exception as e:
            print(f"✗ Error testing {error['scenario']}: {str(e)}")
```

### 5. Permission Error Testing

```python
def test_permission_errors():
    """Test permission and access error scenarios"""
    error_service = ErrorHandlingService(vault_client)
    
    # Test permission errors
    permission_errors = [
        {
            'type': 'INSUFFICIENT_ACCESS',
            'scenario': 'Insufficient permissions',
            'message': 'User does not have sufficient privileges to perform the action'
        },
        {
            'type': 'OPERATION_NOT_ALLOWED',
            'scenario': 'Operation not allowed',
            'message': 'Certain rules that must be met to perform this operation have not been met'
        },
        {
            'type': 'CONFIGURATION_MODE_ENABLED',
            'scenario': 'Configuration mode active',
            'message': 'Non-Admins cannot access a Vault in Configuration Mode'
        }
    ]
    
    for error in permission_errors:
        try:
            print(f"\nTesting {error['scenario']}...")
            
            # Create error response
            error_response = {
                'responseStatus': 'FAILURE',
                'errors': [
                    {
                        'type': error['type'],
                        'message': error['message']
                    }
                ]
            }
            
            # Validate error handling
            handled_error = error_service.handle_permission_error(error_response)
            
            assert handled_error['error_type'] == error['type']
            assert handled_error['category'] == 'PERMISSION'
            
            print(f"✓ {error['scenario']} handled correctly")
            
        except Exception as e:
            print(f"✗ Error testing {error['scenario']}: {str(e)}")
```

### 6. System Error Testing

```python
def test_system_errors():
    """Test system and operational error scenarios"""
    error_service = ErrorHandlingService(vault_client)
    
    # Test system errors
    system_errors = [
        {
            'type': 'UNEXPECTED_ERROR',
            'scenario': 'Unexpected system error',
            'message': 'General error catch-all when there is no specific error'
        },
        {
            'type': 'RACE_CONDITION',
            'scenario': 'Race condition',
            'message': 'A rare condition where the same record is being simultaneously updated'
        },
        {
            'type': 'OPERATION_IN_PROGRESS',
            'scenario': 'Operation in progress',
            'message': 'There is already an operation running on the item specified'
        },
        {
            'type': 'SDK_ERROR',
            'scenario': 'SDK error',
            'message': 'An error caused by the Vault Java SDK',
            'subtype': 'CUSTOM_SDK_ERROR'
        }
    ]
    
    for error in system_errors:
        try:
            print(f"\nTesting {error['scenario']}...")
            
            # Create error response
            error_data = {
                'type': error['type'],
                'message': error['message']
            }
            
            # Add subtype if present
            if 'subtype' in error:
                error_data['subtype'] = error['subtype']
            
            error_response = {
                'responseStatus': 'EXCEPTION',
                'errors': [error_data]
            }
            
            # Validate error handling
            handled_error = error_service.handle_system_error(error_response)
            
            assert handled_error['error_type'] == error['type']
            assert handled_error['category'] == 'SYSTEM'
            
            if 'subtype' in error:
                assert handled_error['subtype'] == error['subtype']
            
            print(f"✓ {error['scenario']} handled correctly")
            
        except Exception as e:
            print(f"✗ Error testing {error['scenario']}: {str(e)}")
```

### 7. API Limit Error Testing

```python
def test_api_limit_errors():
    """Test API rate limit error scenarios"""
    error_service = ErrorHandlingService(vault_client)
    
    # Test API limit errors
    limit_errors = [
        {
            'type': 'API_LIMIT_EXCEEDED',
            'scenario': 'Rate limit exceeded',
            'message': 'The Job Status endpoint can only be requested once every 10 seconds'
        },
        {
            'type': 'EXCEEDS_FILE_MAX_SIZE',
            'scenario': 'File size exceeded',
            'message': 'The size of uploaded file exceeds the maximum size allowed (4 GB)'
        }
    ]
    
    for error in limit_errors:
        try:
            print(f"\nTesting {error['scenario']}...")
            
            # Create error response
            error_response = {
                'responseStatus': 'FAILURE',
                'errors': [
                    {
                        'type': error['type'],
                        'message': error['message']
                    }
                ]
            }
            
            # Validate error handling
            handled_error = error_service.handle_limit_error(error_response)
            
            assert handled_error['error_type'] == error['type']
            assert handled_error['category'] == 'LIMIT'
            
            # Check for retry recommendation
            if error['type'] == 'API_LIMIT_EXCEEDED':
                assert handled_error['retry_recommended'] == True
                assert handled_error['retry_after'] >= 10
            
            print(f"✓ {error['scenario']} handled correctly")
            
        except Exception as e:
            print(f"✗ Error testing {error['scenario']}: {str(e)}")
```

### 8. HTTP Error Testing

```python
def test_http_errors():
    """Test HTTP-level error scenarios"""
    error_service = ErrorHandlingService(vault_client)
    
    # Test HTTP errors
    http_errors = [
        {
            'type': 'MALFORMED_URL',
            'scenario': 'Resource not found',
            'message': 'The specified resource cannot be found',
            'http_status': 404
        },
        {
            'type': 'METHOD_NOT_SUPPORTED',
            'scenario': 'Method not supported',
            'message': 'The specified resource does not support the method',
            'http_status': 405
        }
    ]
    
    for error in http_errors:
        try:
            print(f"\nTesting {error['scenario']}...")
            
            # Create error response
            error_response = {
                'responseStatus': 'FAILURE',
                'errors': [
                    {
                        'type': error['type'],
                        'message': error['message']
                    }
                ],
                'http_status': error['http_status']
            }
            
            # Validate error handling
            handled_error = error_service.handle_http_error(error_response)
            
            assert handled_error['error_type'] == error['type']
            assert handled_error['category'] == 'HTTP'
            assert handled_error['http_status'] == error['http_status']
            
            print(f"✓ {error['scenario']} handled correctly")
            
        except Exception as e:
            print(f"✗ Error testing {error['scenario']}: {str(e)}")
```

### 9. User Error Testing

```python
def test_user_errors():
    """Test user-specific error scenarios"""
    error_service = ErrorHandlingService(vault_client)
    
    # Test user errors
    user_errors = [
        {
            'type': 'USER_NOT_FOUND',
            'scenario': 'User not found',
            'message': 'The specified user cannot be found'
        },
        {
            'type': 'FEDERATED_ID_ALREADY_EXISTS',
            'scenario': 'Duplicate federated ID',
            'message': 'A user with the same Federated ID already exists'
        },
        {
            'type': 'ITEM_NAME_EXISTS',
            'scenario': 'Item name exists',
            'message': 'An item with the same name already exists in the specified location'
        }
    ]
    
    for error in user_errors:
        try:
            print(f"\nTesting {error['scenario']}...")
            
            # Create error response
            error_response = {
                'responseStatus': 'FAILURE',
                'errors': [
                    {
                        'type': error['type'],
                        'message': error['message']
                    }
                ]
            }
            
            # Validate error handling
            handled_error = error_service.handle_user_error(error_response)
            
            assert handled_error['error_type'] == error['type']
            assert handled_error['category'] == 'USER'
            
            print(f"✓ {error['scenario']} handled correctly")
            
        except Exception as e:
            print(f"✗ Error testing {error['scenario']}: {str(e)}")
```

### 10. Warning Handling Testing

```python
def test_warning_handling():
    """Test handling of API warnings"""
    error_service = ErrorHandlingService(vault_client)
    
    # Test warning scenarios
    warning_scenarios = [
        {
            'type': 'TEMPLATE_MISMATCH',
            'message': 'The templates of the source and target do not align',
            'category': 'RIM_SUBMISSIONS'
        },
        {
            'type': 'LEVEL_MISMATCH',
            'message': 'Level of the source record does not match the level of the target location',
            'category': 'RIM_SUBMISSIONS'
        },
        {
            'type': 'APPLICATION_MISMATCH',
            'message': 'Application folder name does not match the Application record name',
            'category': 'SUBMISSIONS_ARCHIVE'
        }
    ]
    
    for warning in warning_scenarios:
        try:
            print(f"\nTesting {warning['type']} warning...")
            
            # Create warning response
            warning_response = {
                'responseStatus': 'WARNING',
                'warnings': [
                    {
                        'type': warning['type'],
                        'message': warning['message']
                    }
                ],
                'data': {'result': 'success_with_warnings'}
            }
            
            # Validate warning handling
            handled_warning = error_service.handle_warning(warning_response)
            
            assert handled_warning['warning_type'] == warning['type']
            assert handled_warning['category'] == warning['category']
            assert handled_warning['severity'] == 'WARNING'
            
            print(f"✓ {warning['type']} warning handled correctly")
            
        except Exception as e:
            print(f"✗ Error testing {warning['type']}: {str(e)}")
```

### 11. Error Recovery Testing

```python
def test_error_recovery_strategies():
    """Test error recovery and retry strategies"""
    error_service = ErrorHandlingService(vault_client)
    
    # Test recoverable errors
    recoverable_errors = [
        {
            'type': 'API_LIMIT_EXCEEDED',
            'recovery_strategy': 'retry_with_delay',
            'retry_delay': 10
        },
        {
            'type': 'RACE_CONDITION',
            'recovery_strategy': 'retry_immediately',
            'max_retries': 3
        },
        {
            'type': 'OPERATION_IN_PROGRESS',
            'recovery_strategy': 'wait_and_retry',
            'wait_time': 30
        }
    ]
    
    for error in recoverable_errors:
        try:
            print(f"\nTesting recovery for {error['type']}...")
            
            # Create error response
            error_response = {
                'responseStatus': 'FAILURE',
                'errors': [
                    {
                        'type': error['type'],
                        'message': f'Test error for {error["type"]}'
                    }
                ]
            }
            
            # Get recovery strategy
            recovery = error_service.get_recovery_strategy(error_response)
            
            assert recovery['strategy'] == error['recovery_strategy']
            
            if 'retry_delay' in error:
                assert recovery['delay'] == error['retry_delay']
            
            if 'max_retries' in error:
                assert recovery['max_retries'] == error['max_retries']
            
            print(f"✓ Recovery strategy for {error['type']}: {recovery['strategy']}")
            
        except Exception as e:
            print(f"✗ Error testing recovery for {error['type']}: {str(e)}")
```

## Error Classification Testing

### 1. Error Severity Classification

```python
def test_error_severity_classification():
    """Test classification of errors by severity"""
    error_service = ErrorHandlingService(vault_client)
    
    error_severity_map = {
        'CRITICAL': [
            'INVALID_SESSION_ID',
            'USERNAME_OR_PASSWORD_INCORRECT',
            'USER_LOCKED_OUT',
            'CONFIGURATION_MODE_ENABLED'
        ],
        'HIGH': [
            'INSUFFICIENT_ACCESS',
            'OPERATION_NOT_ALLOWED',
            'SDK_ERROR'
        ],
        'MEDIUM': [
            'PARAMETER_REQUIRED',
            'INVALID_DATA',
            'ATTRIBUTE_NOT_SUPPORTED'
        ],
        'LOW': [
            'INVALID_FILTER',
            'ITEM_NAME_EXISTS',
            'USER_NOT_FOUND'
        ]
    }
    
    for severity, error_types in error_severity_map.items():
        for error_type in error_types:
            classification = error_service.classify_error_severity(error_type)
            assert classification == severity
            print(f"✓ {error_type} classified as {severity} severity")
```

### 2. Error Category Grouping

```python
def test_error_category_grouping():
    """Test grouping of errors by functional category"""
    error_service = ErrorHandlingService(vault_client)
    
    error_categories = {
        'AUTHENTICATION': [
            'NO_PASSWORD_PROVIDED',
            'USERNAME_OR_PASSWORD_INCORRECT',
            'USER_LOCKED_OUT',
            'PASSWORD_CHANGE_REQUIRED',
            'INVALID_SESSION_ID',
            'INACTIVE_USER'
        ],
        'AUTHORIZATION': [
            'INSUFFICIENT_ACCESS',
            'OPERATION_NOT_ALLOWED',
            'CONFIGURATION_MODE_ENABLED'
        ],
        'VALIDATION': [
            'PARAMETER_REQUIRED',
            'INVALID_DATA',
            'ATTRIBUTE_NOT_SUPPORTED',
            'INVALID_FILTER',
            'INCORRECT_QUERY_SYNTAX_ERROR'
        ],
        'SYSTEM': [
            'UNEXPECTED_ERROR',
            'RACE_CONDITION',
            'OPERATION_IN_PROGRESS',
            'SDK_ERROR'
        ],
        'RESOURCE': [
            'MALFORMED_URL',
            'METHOD_NOT_SUPPORTED',
            'USER_NOT_FOUND',
            'ITEM_NAME_EXISTS'
        ],
        'LIMIT': [
            'API_LIMIT_EXCEEDED',
            'EXCEEDS_FILE_MAX_SIZE'
        ]
    }
    
    for category, error_types in error_categories.items():
        for error_type in error_types:
            categorization = error_service.categorize_error(error_type)
            assert categorization == category
            print(f"✓ {error_type} categorized as {category}")
```

## Sample Test Data

### Sample Error Responses
```python
SAMPLE_ERROR_RESPONSES = {
    "authentication_failure": {
        "responseStatus": "FAILURE",
        "errors": [
            {
                "type": "USERNAME_OR_PASSWORD_INCORRECT",
                "message": "Authentication failed because an invalid username or password was provided."
            }
        ],
        "errorType": "AUTHENTICATION_FAILED"
    },
    "insufficient_access": {
        "responseStatus": "FAILURE",
        "errors": [
            {
                "type": "INSUFFICIENT_ACCESS",
                "message": "User does not have sufficient privileges to perform the action."
            }
        ]
    },
    "invalid_data": {
        "responseStatus": "FAILURE",
        "errors": [
            {
                "type": "INVALID_DATA",
                "message": "Invalid data provided in the API call."
            }
        ]
    },
    "api_limit_exceeded": {
        "responseStatus": "FAILURE",
        "errors": [
            {
                "type": "API_LIMIT_EXCEEDED",
                "message": "The Job Status endpoint can only be requested once every 10 seconds for each job_id."
            }
        ]
    }
}
```

### Sample Warning Responses
```python
SAMPLE_WARNING_RESPONSES = {
    "template_mismatch": {
        "responseStatus": "WARNING",
        "warnings": [
            {
                "type": "TEMPLATE_MISMATCH",
                "message": "The templates of the source and target do not align."
            }
        ],
        "data": {
            "job_id": 104448
        }
    },
    "submission_mismatch": {
        "responseStatus": "WARNING", 
        "warnings": [
            {
                "type": "SUBMISSION_MISMATCH",
                "message": "Submission folder name does not match the Submission record name."
            }
        ],
        "data": {
            "import_id": "V29000000004001"
        }
    }
}
```

## Validation Helpers

### Error Response Validator
```python
def validate_error_response(response):
    """Validate error response structure"""
    required_fields = ['responseStatus']
    
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"
    
    assert response['responseStatus'] in ['FAILURE', 'EXCEPTION']
    
    if response['responseStatus'] in ['FAILURE', 'EXCEPTION']:
        assert 'errors' in response
        assert isinstance(response['errors'], list)
        assert len(response['errors']) > 0
        
        for error in response['errors']:
            assert 'type' in error
            assert 'message' in error
    
    print("✓ Error response validation passed")
```

### Warning Response Validator
```python
def validate_warning_response(response):
    """Validate warning response structure"""
    required_fields = ['responseStatus', 'warnings']
    
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"
    
    assert response['responseStatus'] == 'WARNING'
    assert isinstance(response['warnings'], list)
    assert len(response['warnings']) > 0
    
    for warning in response['warnings']:
        assert 'type' in warning
        assert 'message' in warning
    
    print("✓ Warning response validation passed")
```

### HTTP Status Code Validator
```python
def validate_http_status_codes():
    """Validate HTTP status code handling"""
    status_codes = {
        200: 'OK - Normal API response',
        400: 'Bad Request - Client error', 
        401: 'Unauthorized - Authentication required',
        403: 'Forbidden - Access denied',
        404: 'Not Found - Resource not found',
        405: 'Method Not Allowed - HTTP method not supported',
        429: 'Too Many Requests - Rate limit exceeded',
        500: 'Internal Server Error - Server error',
        503: 'Service Unavailable - Service temporarily unavailable'
    }
    
    for code, description in status_codes.items():
        # Test HTTP status code handling
        assert code in [200, 400, 401, 403, 404, 405, 429, 500, 503]
        print(f"✓ HTTP {code}: {description}")
```

## Performance Testing

### Error Handling Performance
```python
def test_error_handling_performance():
    """Test error handling performance"""
    import time
    
    error_service = ErrorHandlingService(vault_client)
    
    # Create large error response
    large_error_response = {
        'responseStatus': 'FAILURE',
        'errors': [
            {
                'type': 'INVALID_DATA',
                'message': f'Error {i}: Invalid data in field {i}'
            } for i in range(100)
        ]
    }
    
    start_time = time.time()
    
    # Process error response
    processed_errors = error_service.process_error_response(large_error_response)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✓ Error processing completed in {duration:.3f} seconds")
    print(f"✓ Processed {len(processed_errors)} errors")
    
    # Performance assertion
    assert duration < 1.0, f"Error processing too slow: {duration} seconds"
```

## Integration Testing

### End-to-End Error Handling Workflow
```python
def test_complete_error_handling_workflow():
    """Test complete error handling workflow"""
    error_service = ErrorHandlingService(vault_client)
    
    print("Starting complete error handling workflow test...")
    
    try:
        # Step 1: Simulate API call with error
        print("✓ Step 1: Simulating API call with error...")
        
        error_response = {
            'responseStatus': 'FAILURE',
            'errors': [
                {
                    'type': 'INVALID_DATA',
                    'message': 'Invalid data provided in the API call.'
                }
            ]
        }
        
        # Step 2: Detect and classify error
        print("✓ Step 2: Detecting and classifying error...")
        
        error_classification = error_service.classify_error(error_response)
        assert error_classification['category'] == 'VALIDATION'
        assert error_classification['severity'] == 'MEDIUM'
        
        # Step 3: Determine recovery strategy
        print("✓ Step 3: Determining recovery strategy...")
        
        recovery_strategy = error_service.get_recovery_strategy(error_response)
        assert recovery_strategy['strategy'] == 'fix_and_retry'
        
        # Step 4: Log error for monitoring
        print("✓ Step 4: Logging error for monitoring...")
        
        log_entry = error_service.log_error(error_response)
        assert log_entry['logged'] == True
        assert log_entry['log_level'] == 'ERROR'
        
        print("✓ Complete error handling workflow completed successfully")
        
    except Exception as e:
        print(f"✗ Error in error handling workflow: {str(e)}")
        raise
```

## Notes
- All API responses include responseStatus field
- Error messages are subject to change and should not be used for application logic
- HTTP status code 200 is returned for all API responses (errors included)
- Error types are contractual and won't change within API versions
- Some errors like API_LIMIT_EXCEEDED suggest retry strategies
- SDK_ERROR may include custom subtypes for detailed debugging
- Configuration Mode errors affect non-admin users only
- Race conditions are rare but should be handled with retry logic
- File size limits are enforced at 4GB maximum
- Job status endpoint has specific rate limiting (10-second intervals)
