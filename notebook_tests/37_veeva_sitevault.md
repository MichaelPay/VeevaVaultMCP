# 37. Veeva SiteVault - Testing Documentation

## Overview
Testing documentation for Veeva SiteVault functionality in Veeva Vault. This module provides comprehensive clinical site management capabilities including user administration and eConsent functionality for clinical trial sites.

## Prerequisites
- Veeva SiteVault must be enabled
- User must have appropriate SiteVault administration permissions
- Understanding of clinical site hierarchy and user roles
- Valid organization, site, and study configurations

## Test Methods

### 1. SiteVault Service Initialization

```python
from veevatools.veevavault.services.sitevault_service import SiteVaultService

def test_sitevault_service_initialization():
    """Test the initialization of SiteVaultService"""
    # Initialize vault client
    vault_client = initialize_vault_client()
    
    # Initialize SiteVault service
    sitevault_service = SiteVaultService(vault_client)
    
    # Verify service initialization
    assert sitevault_service is not None
    assert sitevault_service.vault_client == vault_client
    print("✓ SiteVault Service initialized successfully")
```

### 2. Create User Testing

```python
def test_create_user():
    """Test creating a new user in SiteVault"""
    sitevault_service = SiteVaultService(vault_client)
    
    # Test data for user creation
    user_data = {
        "user": {
            "email": "jerry.cotter@company.com",
            "first_name": "Jerry",
            "last_name": "Cotter",
            "security_policy_id": "VeevaID",
            "person_type": "staff__v",
            "language": "en"
        },
        "person_type": "staff__v",
        "is_investigator": False,
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_admin__v"
            },
            "site_assignments": [
                {
                    "site_usn": "US-NC-0001",
                    "system_role_id": "regulatory__v"
                }
            ]
        }
    }
    
    try:
        # Create user
        response = sitevault_service.create_user(user_data)
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        assert 'data' in response
        assert 'response' in response['data']
        
        user_response = response['data']['response'][0]
        assert user_response['status'] == 'Success'
        assert user_response['email'] == user_data['user']['email']
        assert 'person_id' in user_response
        assert user_response['record_status'] == 'active__v'
        
        person_id = user_response['person_id']
        print(f"✓ User created successfully. Person ID: {person_id}")
        print(f"✓ Email: {user_response['email']}")
        print(f"✓ Status: {user_response['record_status']}")
        
        return person_id
        
    except Exception as e:
        print(f"✗ Error creating user: {str(e)}")
        raise
```

### 3. Create External User Testing

```python
def test_create_external_user():
    """Test creating an external user in SiteVault"""
    sitevault_service = SiteVaultService(vault_client)
    
    # Test data for external user creation
    external_user_data = {
        "user": {
            "email": "external.user@sponsor.com",
            "first_name": "External",
            "last_name": "User",
            "security_policy_id": "VeevaID",
            "person_type": "external__v",
            "language": "en"
        },
        "person_type": "external__v",
        "is_investigator": False,  # External users must be False
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_external__v"
            },
            "site_assignments": [
                {
                    "site_usn": "US-NC-0001",
                    "system_role_id": "external__v"
                }
            ],
            "study_assignments": [
                {
                    "id": "V48000000001001",
                    "study_role": "sponsor_cro__v"
                }
            ]
        }
    }
    
    try:
        # Create external user
        response = sitevault_service.create_user(external_user_data)
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        
        user_response = response['data']['response'][0]
        assert user_response['status'] == 'Success'
        assert user_response['email'] == external_user_data['user']['email']
        
        print(f"✓ External user created successfully")
        print(f"✓ Person ID: {user_response['person_id']}")
        
        return user_response['person_id']
        
    except Exception as e:
        print(f"✗ Error creating external user: {str(e)}")
        raise
```

### 4. Create Staff User with Add-ons Testing

```python
def test_create_staff_user_with_addons():
    """Test creating staff user with add-on permissions"""
    sitevault_service = SiteVaultService(vault_client)
    
    # Test data for staff user with add-ons
    staff_user_data = {
        "user": {
            "email": "site.coordinator@site.com",
            "first_name": "Site",
            "last_name": "Coordinator",
            "security_policy_id": "VeevaID",
            "person_type": "staff__v",
            "language": "en"
        },
        "person_type": "staff__v",
        "is_investigator": False,
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_full__v",
                "addons": ["org_patients__v"]
            },
            "site_assignments": [
                {
                    "site_usn": "US-NC-0001",
                    "system_role_id": "study_team__v",
                    "addons": ["site_budgets__v", "site_patients__v", "site_profiles__v"]
                }
            ],
            "study_assignments": [
                {
                    "id": "V48000000001001",
                    "study_role": "clinical_research_coordinator__v"
                }
            ]
        }
    }
    
    try:
        # Create staff user with add-ons
        response = sitevault_service.create_user(staff_user_data)
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        
        user_response = response['data']['response'][0]
        assert user_response['status'] == 'Success'
        
        print(f"✓ Staff user with add-ons created successfully")
        print(f"✓ Person ID: {user_response['person_id']}")
        print(f"✓ Organization add-ons: org_patients__v")
        print(f"✓ Site add-ons: site_budgets__v, site_patients__v, site_profiles__v")
        
        return user_response['person_id']
        
    except Exception as e:
        print(f"✗ Error creating staff user with add-ons: {str(e)}")
        raise
```

### 5. Create No-Login User Testing

```python
def test_create_no_login_user():
    """Test creating a user who doesn't require login"""
    sitevault_service = SiteVaultService(vault_client)
    
    # Test data for no-login user
    no_login_user_data = {
        "user": {
            "email": "no.login@site.com",
            "first_name": "No",
            "last_name": "Login",
            "security_policy_id": "noUser",
            "person_type": "staff__v",
            "language": "en"
        },
        "person_type": "staff__v",
        "is_investigator": False,
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_cant_login__v"
            },
            "site_assignments": [
                {
                    "site_usn": "US-NC-0001",
                    "system_role_id": "site_cant_login__v"
                }
            ]
        }
    }
    
    try:
        # Create no-login user
        response = sitevault_service.create_user(no_login_user_data)
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        
        user_response = response['data']['response'][0]
        assert user_response['status'] == 'Success'
        
        print(f"✓ No-login user created successfully")
        print(f"✓ Person ID: {user_response['person_id']}")
        print(f"✓ Security policy: noUser")
        
        return user_response['person_id']
        
    except Exception as e:
        print(f"✗ Error creating no-login user: {str(e)}")
        raise
```

### 6. Edit User Testing

```python
def test_edit_user():
    """Test editing an existing user in SiteVault"""
    sitevault_service = SiteVaultService(vault_client)
    
    # Test data for editing user
    person_id = "V0B000000001001"
    edit_data = {
        "is_investigator": False,
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_full__v",
                "addons": ["org_patients__v"]
            },
            "site_assignments": [
                {
                    "site_usn": "US-NC-0002",
                    "system_role_id": "study_team__v",
                    "addons": ["site_patients__v"]
                }
            ],
            "study_assignments": [
                {
                    "id": "V48000000001002",
                    "study_role": "data_coordinator__v"
                }
            ]
        }
    }
    
    try:
        # Edit user
        response = sitevault_service.edit_user(person_id, edit_data)
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        assert 'data' in response
        assert 'response' in response['data']
        
        user_response = response['data']['response']
        assert user_response['status'] == 'Success'
        assert user_response['person_id'] == person_id
        assert user_response['record_status'] == 'active__v'
        
        print(f"✓ User edited successfully")
        print(f"✓ Person ID: {user_response['person_id']}")
        print(f"✓ Email: {user_response['email']}")
        print(f"✓ Username: {user_response['username']}")
        
        return user_response
        
    except Exception as e:
        print(f"✗ Error editing user: {str(e)}")
        raise
```

### 7. Remove User Access Testing

```python
def test_remove_user_access():
    """Test removing user access by setting no_access roles"""
    sitevault_service = SiteVaultService(vault_client)
    
    # Test data for removing access
    person_id = "V0B000000001001"
    remove_access_data = {
        "is_investigator": False,
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_no_access__v"
            },
            "site_assignments": [
                {
                    "site_usn": "US-NC-0001",
                    "system_role_id": "no_access__v"
                }
            ]
        }
    }
    
    try:
        # Remove user access
        response = sitevault_service.edit_user(person_id, remove_access_data)
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        
        user_response = response['data']['response']
        assert user_response['status'] == 'Success'
        assert user_response['person_id'] == person_id
        
        print(f"✓ User access removed successfully")
        print(f"✓ Person ID: {user_response['person_id']}")
        print(f"✓ Organization role: org_no_access__v")
        print(f"✓ Site role: no_access__v")
        
        return user_response
        
    except Exception as e:
        print(f"✗ Error removing user access: {str(e)}")
        raise
```

### 8. Associate Existing User Testing

```python
def test_associate_existing_user():
    """Test associating person record with existing user account"""
    sitevault_service = SiteVaultService(vault_client)
    
    # Test data for associating existing user
    person_id = "V0B000000001002"
    associate_data = {
        "username": "existing.user@company.com",  # Existing user account
        "is_investigator": True,  # Can set as investigator
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_full__v"
            },
            "site_assignments": [
                {
                    "site_usn": "US-NC-0001",
                    "system_role_id": "regulatory__v"
                }
            ],
            "study_assignments": [
                {
                    "id": "V48000000001001",
                    "study_role": "principal_investigator__v"
                }
            ]
        }
    }
    
    try:
        # Associate existing user
        response = sitevault_service.edit_user(person_id, associate_data)
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        
        user_response = response['data']['response']
        assert user_response['status'] == 'Success'
        assert user_response['username'] == associate_data['username']
        
        print(f"✓ Existing user associated successfully")
        print(f"✓ Person ID: {user_response['person_id']}")
        print(f"✓ Username: {user_response['username']}")
        print(f"✓ Study role: principal_investigator__v")
        
        return user_response
        
    except Exception as e:
        print(f"✗ Error associating existing user: {str(e)}")
        raise
```

### 9. Retrieve eConsent Documents and Signatories Testing

```python
def test_retrieve_econsent_documents():
    """Test retrieving eConsent documents and signatories for participant"""
    sitevault_service = SiteVaultService(vault_client)
    
    # Test data
    participant_id = "V0X000000002001"
    
    try:
        # Retrieve eConsent documents
        response = sitevault_service.retrieve_econsent_documents(
            participant_id=participant_id
        )
        
        # Verify response structure
        assert isinstance(response, list)
        assert len(response) > 0
        
        participant_data = response[0]
        assert 'subject__v.id' in participant_data
        assert participant_data['subject__v.id'] == participant_id
        assert 'documents' in participant_data
        
        # Check document structure
        for document in participant_data['documents']:
            assert 'document.version_id__v' in document
            assert 'signatory__v' in document
            
            for signatory in document['signatory__v']:
                assert 'signatory__v.id' in signatory
        
        print(f"✓ eConsent documents retrieved successfully")
        print(f"✓ Participant ID: {participant_id}")
        print(f"✓ Number of documents: {len(participant_data['documents'])}")
        
        return response
        
    except Exception as e:
        print(f"✗ Error retrieving eConsent documents: {str(e)}")
        raise
```

### 10. Send eConsent Documents Testing

```python
def test_send_econsent_documents():
    """Test sending eConsent documents to signatories"""
    sitevault_service = SiteVaultService(vault_client)
    
    # Test data for sending eConsent
    send_data = {
        "documents.version_id__v": "40_1_0",
        "signatory__v.id": "V5A000000004002",
        "signatory__v.role__v": "participant__v",
        "subject__v.id": "V0X000000002001"
    }
    
    try:
        # Send eConsent documents
        response = sitevault_service.send_econsent_documents(
            document_version_id=send_data["documents.version_id__v"],
            signatory_id=send_data["signatory__v.id"],
            signatory_role=send_data["signatory__v.role__v"],
            subject_id=send_data["subject__v.id"]
        )
        
        # Verify response
        assert response['responseStatus'] == 'SUCCESS'
        assert response['responseMessage'] == 'Success'
        assert 'data' in response
        
        data_response = response['data'][0]
        assert data_response['status'] == 'SUCCESS'
        assert 'job id' in data_response['message']
        
        # Verify data structure
        response_data = data_response['data']
        assert response_data['subject__v.id'] == send_data['subject__v.id']
        assert len(response_data['documents']) > 0
        
        document = response_data['documents'][0]
        assert document['document.version_id__v'] == send_data['documents.version_id__v']
        
        signatory = document['signatory__v'][0]
        assert signatory['signatory__v.id'] == send_data['signatory__v.id']
        assert signatory['signatory__v.role__v'] == send_data['signatory__v.role__v']
        
        print(f"✓ eConsent documents sent successfully")
        print(f"✓ Subject ID: {send_data['subject__v.id']}")
        print(f"✓ Document version: {send_data['documents.version_id__v']}")
        print(f"✓ Signatory: {send_data['signatory__v.id']}")
        
        # Extract job ID for status tracking
        job_id_match = re.search(r'job id (\w+)', data_response['message'])
        if job_id_match:
            job_id = job_id_match.group(1)
            print(f"✓ Job ID: {job_id}")
            return job_id
        
        return response
        
    except Exception as e:
        print(f"✗ Error sending eConsent documents: {str(e)}")
        raise
```

### 11. Bulk eConsent Send Testing

```python
def test_bulk_econsent_send():
    """Test sending eConsent documents to multiple participants"""
    sitevault_service = SiteVaultService(vault_client)
    
    # Test data for bulk eConsent send
    bulk_send_data = [
        {
            "documents.version_id__v": "40_1_0",
            "signatory__v.id": "V5A000000004002",
            "signatory__v.role__v": "participant__v",
            "subject__v.id": "V0X000000002001"
        },
        {
            "documents.version_id__v": "40_1_0",
            "signatory__v.id": "V5A000000004003",
            "signatory__v.role__v": "participant__v",
            "subject__v.id": "V0X000000002002"
        },
        {
            "documents.version_id__v": "41_1_0",
            "signatory__v.id": "V5A000000004004",
            "signatory__v.role__v": "legal_guardian__v",
            "subject__v.id": "V0X000000002003"
        }
    ]
    
    job_ids = []
    
    for send_data in bulk_send_data:
        try:
            print(f"\nSending eConsent to subject {send_data['subject__v.id']}...")
            
            response = sitevault_service.send_econsent_documents(
                document_version_id=send_data["documents.version_id__v"],
                signatory_id=send_data["signatory__v.id"],
                signatory_role=send_data["signatory__v.role__v"],
                subject_id=send_data["subject__v.id"]
            )
            
            assert response['responseStatus'] == 'SUCCESS'
            
            data_response = response['data'][0]
            assert data_response['status'] == 'SUCCESS'
            
            # Extract job ID
            job_id_match = re.search(r'job id (\w+)', data_response['message'])
            if job_id_match:
                job_id = job_id_match.group(1)
                job_ids.append(job_id)
                print(f"✓ eConsent sent successfully. Job ID: {job_id}")
            
        except Exception as e:
            print(f"✗ Error sending eConsent to {send_data['subject__v.id']}: {str(e)}")
    
    print(f"\n✓ Bulk eConsent send completed. {len(job_ids)} documents sent")
    return job_ids
```

## Error Scenarios Testing

### 1. Invalid Email Format Testing

```python
def test_invalid_email_format():
    """Test handling of invalid email format"""
    sitevault_service = SiteVaultService(vault_client)
    
    invalid_user_data = {
        "user": {
            "email": "invalid-email-format",  # Invalid email
            "first_name": "Test",
            "last_name": "User",
            "security_policy_id": "VeevaID",
            "person_type": "staff__v"
        },
        "person_type": "staff__v",
        "is_investigator": False,
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_full__v"
            }
        }
    }
    
    try:
        response = sitevault_service.create_user(invalid_user_data)
        
        # Should handle error gracefully
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled invalid email format")
        
    except Exception as e:
        print(f"✓ Correctly handled invalid email error: {str(e)}")
```

### 2. Invalid Organization ID Testing

```python
def test_invalid_organization_id():
    """Test handling of invalid organization ID"""
    sitevault_service = SiteVaultService(vault_client)
    
    invalid_user_data = {
        "user": {
            "email": "test@company.com",
            "first_name": "Test",
            "last_name": "User",
            "security_policy_id": "VeevaID",
            "person_type": "staff__v"
        },
        "person_type": "staff__v",
        "is_investigator": False,
        "assignments": {
            "org_assignment": {
                "org_id": "INVALID_ORG_ID",  # Invalid organization
                "system_role_id": "org_full__v"
            }
        }
    }
    
    try:
        response = sitevault_service.create_user(invalid_user_data)
        
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled invalid organization ID")
        
    except Exception as e:
        print(f"✓ Correctly handled invalid organization error: {str(e)}")
```

### 3. Invalid Site USN Testing

```python
def test_invalid_site_usn():
    """Test handling of invalid site USN"""
    sitevault_service = SiteVaultService(vault_client)
    
    invalid_user_data = {
        "user": {
            "email": "test@company.com",
            "first_name": "Test",
            "last_name": "User",
            "security_policy_id": "VeevaID",
            "person_type": "staff__v"
        },
        "person_type": "staff__v",
        "is_investigator": False,
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_full__v"
            },
            "site_assignments": [
                {
                    "site_usn": "INVALID-SITE-USN",  # Invalid site USN
                    "system_role_id": "regulatory__v"
                }
            ]
        }
    }
    
    try:
        response = sitevault_service.create_user(invalid_user_data)
        
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly handled invalid site USN")
        
    except Exception as e:
        print(f"✓ Correctly handled invalid site USN error: {str(e)}")
```

### 4. External User as Investigator Testing

```python
def test_external_user_as_investigator():
    """Test validation that external users cannot be investigators"""
    sitevault_service = SiteVaultService(vault_client)
    
    invalid_user_data = {
        "user": {
            "email": "external@company.com",
            "first_name": "External",
            "last_name": "User",
            "security_policy_id": "VeevaID",
            "person_type": "external__v"
        },
        "person_type": "external__v",
        "is_investigator": True,  # Invalid for external users
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_external__v"
            }
        }
    }
    
    try:
        response = sitevault_service.create_user(invalid_user_data)
        
        assert response['responseStatus'] == 'FAILURE'
        print("✓ Correctly validated external user cannot be investigator")
        
    except Exception as e:
        print(f"✓ Correctly handled external user investigator error: {str(e)}")
```

### 5. Invalid Participant ID for eConsent Testing

```python
def test_invalid_participant_id_econsent():
    """Test handling of invalid participant ID for eConsent"""
    sitevault_service = SiteVaultService(vault_client)
    
    try:
        response = sitevault_service.retrieve_econsent_documents(
            participant_id="INVALID_PARTICIPANT_ID"
        )
        
        # Should handle error gracefully
        assert response == [] or 'error' in str(response).lower()
        print("✓ Correctly handled invalid participant ID")
        
    except Exception as e:
        print(f"✓ Correctly handled invalid participant ID error: {str(e)}")
```

## Sample Test Data

### Sample User Creation Data
```python
SAMPLE_USER_DATA = {
    "staff_user": {
        "user": {
            "email": "staff.user@site.com",
            "first_name": "Staff",
            "last_name": "User",
            "security_policy_id": "VeevaID",
            "person_type": "staff__v",
            "language": "en"
        },
        "person_type": "staff__v",
        "is_investigator": False,
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_full__v"
            },
            "site_assignments": [
                {
                    "site_usn": "US-NC-0001",
                    "system_role_id": "study_team__v",
                    "addons": ["site_patients__v"]
                }
            ]
        }
    },
    "external_user": {
        "user": {
            "email": "external@sponsor.com",
            "first_name": "External",
            "last_name": "User",
            "security_policy_id": "VeevaID",
            "person_type": "external__v",
            "language": "en"
        },
        "person_type": "external__v",
        "is_investigator": False,
        "assignments": {
            "org_assignment": {
                "org_id": "V42000000001001",
                "system_role_id": "org_external__v"
            },
            "study_assignments": [
                {
                    "id": "V48000000001001",
                    "study_role": "sponsor_cro__v"
                }
            ]
        }
    }
}
```

### Sample Role Mappings
```python
ROLE_MAPPINGS = {
    "organization_roles": [
        "org_admin__v",
        "org_full__v", 
        "org_external__v",
        "org_no_access__v",
        "org_cant_login__v"
    ],
    "site_roles": [
        "regulatory__v",
        "study_team__v",
        "site_viewer__v",
        "external__v",
        "no_access__v",
        "site_cant_login__v"
    ],
    "study_roles": {
        "external": ["sponsor_cro__v", "auditor_inspector__v"],
        "staff": [
            "clinical_research_coordinator__v",
            "data_coordinator__v",
            "principal_investigator__v",
            "regulatory_coordinator__v",
            "research_nurse__v",
            "subinvestigator__v",
            "pharmacist__v",
            "other__v"
        ]
    },
    "addons": {
        "organization": ["org_patients__v"],
        "site": ["site_budgets__v", "site_patients__v", "site_profiles__v"]
    }
}
```

### Sample eConsent Data
```python
SAMPLE_ECONSENT_DATA = {
    "participant": {
        "participant_id": "V0X000000002001",
        "document_version_id": "40_1_0",
        "signatory_id": "V5A000000004002",
        "signatory_role": "participant__v"
    },
    "guardian": {
        "participant_id": "V0X000000002002",
        "document_version_id": "41_1_0",
        "signatory_id": "V5A000000004003", 
        "signatory_role": "legal_guardian__v"
    }
}
```

## Validation Helpers

### User Creation Response Validator
```python
def validate_user_creation_response(response):
    """Validate user creation response structure"""
    required_fields = ['responseStatus', 'data']
    
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"
    
    assert response['responseStatus'] == 'SUCCESS'
    assert 'response' in response['data']
    
    user_response = response['data']['response'][0]
    user_required_fields = ['status', 'email', 'person_id', 'record_status']
    
    for field in user_required_fields:
        assert field in user_response, f"Missing user response field: {field}"
    
    assert user_response['status'] == 'Success'
    assert user_response['record_status'] == 'active__v'
    
    print("✓ User creation response validation passed")
```

### eConsent Response Validator
```python
def validate_econsent_response(response):
    """Validate eConsent operation response structure"""
    required_fields = ['responseStatus', 'responseMessage', 'data']
    
    for field in required_fields:
        assert field in response, f"Missing required field: {field}"
    
    assert response['responseStatus'] == 'SUCCESS'
    assert response['responseMessage'] == 'Success'
    
    data_response = response['data'][0]
    assert data_response['status'] == 'SUCCESS'
    assert 'job id' in data_response['message']
    
    print("✓ eConsent response validation passed")
```

## Performance Testing

### User Creation Performance Testing
```python
def test_user_creation_performance():
    """Test user creation performance"""
    import time
    
    sitevault_service = SiteVaultService(vault_client)
    
    start_time = time.time()
    
    # Create basic user
    user_data = SAMPLE_USER_DATA["staff_user"]
    response = sitevault_service.create_user(user_data)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✓ User creation completed in {duration:.2f} seconds")
    
    # Performance assertion (adjust threshold as needed)
    assert duration < 10.0, f"User creation too slow: {duration} seconds"
```

## Integration Testing

### Complete SiteVault User Lifecycle Testing
```python
def test_complete_user_lifecycle():
    """Test complete user lifecycle from creation to removal"""
    sitevault_service = SiteVaultService(vault_client)
    
    print("Starting complete user lifecycle test...")
    
    try:
        # Step 1: Create user
        print("✓ Step 1: Creating user...")
        
        user_data = SAMPLE_USER_DATA["staff_user"]
        create_response = sitevault_service.create_user(user_data)
        
        person_id = create_response['data']['response'][0]['person_id']
        print(f"✓ User created. Person ID: {person_id}")
        
        # Step 2: Edit user to add permissions
        print("✓ Step 2: Adding permissions...")
        
        edit_data = {
            "is_investigator": False,
            "assignments": {
                "org_assignment": {
                    "org_id": "V42000000001001",
                    "system_role_id": "org_admin__v",
                    "addons": ["org_patients__v"]
                },
                "site_assignments": [
                    {
                        "site_usn": "US-NC-0001",
                        "system_role_id": "study_team__v",
                        "addons": ["site_budgets__v", "site_patients__v"]
                    }
                ]
            }
        }
        
        edit_response = sitevault_service.edit_user(person_id, edit_data)
        print("✓ User permissions updated")
        
        # Step 3: Remove access
        print("✓ Step 3: Removing access...")
        
        remove_data = {
            "is_investigator": False,
            "assignments": {
                "org_assignment": {
                    "org_id": "V42000000001001",
                    "system_role_id": "org_no_access__v"
                },
                "site_assignments": [
                    {
                        "site_usn": "US-NC-0001",
                        "system_role_id": "no_access__v"
                    }
                ]
            }
        }
        
        remove_response = sitevault_service.edit_user(person_id, remove_data)
        print("✓ User access removed")
        
        print("✓ Complete user lifecycle completed successfully")
        
        return {
            "create": create_response,
            "edit": edit_response,
            "remove": remove_response
        }
        
    except Exception as e:
        print(f"✗ Error in user lifecycle: {str(e)}")
        raise
```

## Notes
- SiteVault requires specific licensing and permissions
- Only single user operations supported (no bulk create/edit)
- External users cannot be investigators
- Add-on permissions must be valid for the assigned system role
- Person records become inactive when all organization access is removed
- Must be in organization context for cross-site study assignments
- eConsent operations are asynchronous - track with job IDs
- Site USN format must follow proper conventions
- Security policies vary by SiteVault configuration
- Username must include domain name for non-VeevaID policies
