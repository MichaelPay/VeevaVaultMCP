<!-- 
VaultAPIDocs Section: # Veeva SiteVault
Original Line Number: 43744
Generated: August 30, 2025
Part 37 of 38
-->

# Veeva SiteVault

## Users

The Create and Edit APIs are defined to be as consistent as possible. Both Create and Edit accept the same JSON, which has several shapes depending on which data you are creating/editing. For more information on Veeva SiteVault User Administration, see [Veeva SiteVault Help](https://sites.veevavault.help/gr/sitevault/sv-administration/).

#### Guidelines

-   A Person record is referencing `person__sys`.
-   A User record is referencing `user__sys`.
-   A “user” object (create) or a “username” referencing an existing user (edit) must be specified. All other API references are consistent.
-   Only a single user per API call is supported.
-   APIs build on each other and appear in a nested format.
-   If a site, organization, or study is specified, you must complete all the site, organization, or study parameters. For example, if you edit a user with an existing add-on permission and do not include it in your call, the user will no longer have that add-on permission.
-   You must be in the organization context to add study assignments for other sites within the organization.
-   It is possible to make an existing Person/User active if Vault finds an existing Person/User who is currently inactive.
-   A person is made inactive in an organization when all access within that organization has been removed.

### Create User

Create a new user in Veeva SiteVault. Bulk creation of users is not supported. You must be in the organization context to add study assignments for other sites within the organization.

POST `/api/{version}/app/sitevault/useradmin/persons`

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
--data-binary @"users_create.json" \
https://myvault.veevavault.com/api/v25.2/app/sitevault/useradmin/persons
'''

> Example JSON Request Body

'''
[
    {
        "user": {
            "email": "jerry.cotter@company.com",
            "first_name": "Jerry",
            "last_name": "Cotter",
            "security_policy_id": "VeevaID",
            "person_type": "staff__v",
            "language":"en"
        },
        "person_type": "staff__v",
        "is_investigator": false,
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
]
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "response": [
           {
               "status": "Success",
               "email": "jerry.cotter@company.com",
               "person_id": "V0B000000001001",
               "record_status": "active__v"
           }
       ]
   }
}
'''

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json`

#### Body Parameters

In the body of the request, upload parameters as a JSON file. The following tables provide the required and most common optional parameters for creating a user.

##### User Creation

The following table lists the fields required to create a user.

Name

Description

`user`required

This is an _object_ definition of the User being created. This represents the `user__sys record` in the Vault.

`user.email`required

The user’s email.

`user.username`required

The username of the user being created, with the domain name. This is always required _unless security policy is VeevaID_.

`user.first_name`required

The user’s first name.

`user.last_name`required

The user’s last name.

`user.security_policy_id`required

The `name__v` value of the Security Policy for this user. The standard is VeevaID. However, Enterprise Veeva SiteVaults may utilize custom policies. When creating a Staff user who will not require an account to log in, set as `noUser`.

`user.person_type`required

Defines the type of the `person__sys` record. Select from `staff__v` or `external__v`.

`user.language`optional

The 2-letter system code for the user language. If omitted, defaults to `en` for English.

`is_investigator`required

Indicates if the user is an investigator. External users must be set as `false`.

##### Organization Assignment

The following table lists the fields required to include an organization assignment when creating a user.

Name

Description

`assignments`required

This _object_ defines the user’s permissions.

`assignments.org_assignment`required

This _object_ defines the user’s organization-level permissions. Required when creating a user. Content sent in this call will overwrite any existing organization assignments with the same organization ID.

`assignments.org_assignment.org_id`required

The ID of the organization.

`assignments.org_assignment.system_role_id`required

The system ID of the organization-level system role for the user. Select from `org_admin__v`, `org_full__v`, or `org_external__v`. When creating a Staff user who will not require an account to log in, set as `org_cant_login__v`.

`assignments.org_assignment.addons`optional

The system ID for the organization-level add-on permissions assigned to the user. Add-on permissions must be valid for the specified system role. Add-on permissions are not available for the Site Viewer or External User roles. Select `org_patients__v`. Do not include if not applicable.

##### Site Assignment

The following table lists the fields required to include a site assignment when creating a user.

Name

Description

`site_assignments`required

This _object_ defines the user’s site-level permissions.

`site_assignments.site_USN`required

The Universal Site Number (USN) assigned to the Site.

`site_assignments.system_role_id`required

The system ID for the user’s site-level system role. Select from `regulatory__v`, `study_team__v`, `site_viewer__v`, or `external__v`. When creating a Staff user who will not require an account to log in, set as `site_cant_login__v`\`.

`site_assignments.addons`optional

The system ID for the site-level add-on permissions assigned to the user. Add-on permissions must be valid for the specified system role. Add-on permissions are not available for the Site Viewer or External User roles. Select from `site_budgets__v`, `site_patients__v`, and `site_profiles__v`. Use a comma to separate when selecting multiple add-on permissions (ex. `["site_budgets__v", "site_patients__v"]`). Do not include if not applicable.

##### Study Assignment

The following table lists the fields required to include a study assignment when creating a user.

Name

Description

`study_assignments`required

This _object_ defines the user’s study-level permissions.

`study_assignments.id`required

The Study ID.

`study_assignments.study_role`required

The study-level role for the user. Select from `sponsor_cro__v` or `auditor_inspector__v` for external users. Select from `clinical_research_coordinator__v`, `data_coordinator__v`, `principal_investigator__v`, `regulatory_coordinator__v`, `research_nurse__v`, `subinvestigator__v`, `pharmacist__v`, or `other__v`, for site staff.

### Edit User

Edit an existing user in Veeva SiteVault. Bulk editing is not supported. You must be in the organization context to add study assignments for other sites within the organization.

PUT `/api/{version}/app/sitevault/useradmin/persons/{personId}`

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
--data-binary @"users_edit.json" \
https://myvault.veevavault.com/api/v25.2/app/sitevault/useradmin/persons/V0B000000001001
'''

> Example JSON Request Body

'''
{
    "is_investigator": false,
    "assignments": {
        "org_assignment": {
            "org_id": "V42000000001001",
            "system_role_id": "org_no_access__v"
        },
        "site_assignments": [
            {
                "site_usn": "US-NC-0002",
                "system_role_id": "no_access__v"
            }
        ]
    }
}
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "response": {
            "status": "Success",
            "email": "jerry.cotter@company.com",
            "username": "jerry.cotter@company.com",
            "person_id": "V0B000000001001",
            "record_status": "active__v"
        }
    }
}
'''

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{personid}`

The ID of the `person__sys` to edit.

#### Body Parameters

In the body of the request, upload parameters as a JSON file. The following tables provide the required and most common optional parameters for editing a user.

##### Edit Existing User

The following table lists the fields required to edit an existing user.

Name

Description

`username`conditional

The username associated with the existing User account. Must include the domain name. Only required when editing a person record to associate with an existing user record.

`is_investigator`required

Indicates if the user is an investigator. External users must be noted as `false`.

##### Organization Assignment

The following table lists the fields required to include an organization assignment when editing a user.

Name

Description

`assignments`required

This _object_ defines the user’s permissions.

`assignments.org_assignment`required

This _object_ defines the user’s organization-level permissions. Not required when editing if the organization assignment isn’t changing. Content sent in this call will overwrite any existing orgAssignments with the same orgID.

`assignments.org_id`required

The ID of the organization.

`assignments.system_role_id`required

The system ID of the organization-level system role for the user. Select from `org_admin__v`, `org_full__v`, or `org_external__v`. When removing access to an organization, select `org_no_access__v`.

`assignments.addons`optional

The system ID for the organization-level add-on permissions assigned to the user. Add-on permissions must be valid for the specified system role. Add-on permissions are not available for the Site Viewer or External User roles. Select `org_patients__v`. Do not include if not applicable.

##### Site Assignment

The following table lists the fields required to include a site assignment when editing a user.

Name

Description

`site_assignments`required

This _object_ defines the user’s site-level permissions.

`site_assignments.site_USN`required

The Universal Site Number (USN) assigned to the Site.

`site_assignments.system_role_id`required

The system ID for the site-level system role for the user. Select from `regulatory__v`, `study_team__v`, `site_viewer__v`, or `external__v`. When removing access to a site, set to `no_access__v`.

`site_assignments.addons`required

The system ID for the site-level add-on permissions assigned to the user. Add-on permissions must be valid for the specified system role. Add-on permissions are not available for the Site Viewer or External User roles. Select from `site_budgets__v`, `site_patients__v`, and `site_profiles__v`. Use a comma to separate when selecting multiple add-on permissions (ex. `["site_budgets__v", "site_patients__v"]`). Do not include if not applicable.

##### Study Assignment

The following table lists the fields required to include a study assignment when editing a user.

Name

Description

`study_assignments`required

This _object_ defines the user’s study-level permissions.

`study_assignments.id`required

The Study ID.

`study_assignments.study_role`required

The study-level role for the user. Select from `sponsor_cro__v` or `auditor_inspector__v` for external users. Select from `clinical_research_coordinator__v`, `data_coordinator__v`, `principal_investigator__v`, `regulatory_coordinator__v`, `research_nurse__v`, `subinvestigator__v`, `pharmacist__v`, or `other__v`, for site staff.

## Veeva eConsent

Veeva eConsent enables study participants, signatories, and site staff to sign informed consent forms (ICFs) electronically, eliminating the need to print the forms and speeding up the consenting process. Participants and their signatories can review the forms at home on a familiar device, can read at their own pace, and can easily download and share the forms with their family and care team. Additionally, participants with accessibility requirements can zoom in and utilize screen readers. See the [Veeva eConsent](https://sites.veevavault.help/gr/econsent/overview/) help on the Veeva SiteVault Help website to learn more.

This API enables you to send eConsent forms to participants to review and complete in bulk.

### Retrieve Documents and Signatories

> Request

'''
curl --location --request GET 'https://myvault.veevavault.com/api/v25.2/app/sitevault/econsent/participant/V0X000000002001' \ --header 'Authorization: {SESSION_ID}'
'''

> Response

'''
[
   {
       "subject__v.id": "V0X000000002001",
       "documents": [
           {
               "document.version_id__v": "40_1_0",
               "signatory__v": [
                   {
                       "signatory__v.id": "V5A000000004002"
                   }
               ]
           }

       ]
   }
]
'''

Retrieve the valid blank ICFs and signatories for a participant.

GET `/api/{version}/app/sitevault/econsent/participant/{participant_id}`

#### URI Path Parameters

Name

Description

`participant_id`

The Veeva SiteVault ID of the participant. You can use the [`/query` interface](#Submit_Query) to query the _Participant_ (subject\_\_v) object for the participant ID.

#### Response Details

The response lists the valid blank ICFs and signatories for the participant. Valid blank ICFs are those that are not already sent or in a workflow.

### Send Documents to Signatories

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
-d "documents.version_id__v=40_1_0" \
-d "signatory__v.id=V5A000000004002" \
-d "signatory__v.role__v=participant__v" \
-d "subject__v.id=V0X000000002001" \
https://myvault.veevavault.com/api/v25.2/app/sitevault/econsent/send
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "data": [
        {
            "status": "SUCCESS",
            "message": "Send EConsent action began successfully with job id {job_id}",
            "data": {
                "subject__v.id": "V0X000000002001",
                "documents": [
                    {
                        "document.version_id__v": "40_1_0",
                        "signatory__v": [
                            {
                                "signatory__v.id": "V5A000000004002",
                                "signatory__v.role__v": "participant__v"
                            }
                        ]
                    }

                ]
            }
        }
    ]
}
'''

Send documents to signatories for signature.

POST `/api/{version}/app/sitevault/econsent/send`

#### Body Parameters

Name

Description

`documents.version_id__v`

The ID of the blank ICF.

`signatory__v.id`

The ID of the signatory.

`signatory__v.role__v`

The role of the signatory.

`subject__v.id`

The ID of the participant.

#### Response Details

The response lists the participant, the blank ICF, any signatories, and a job ID. You can use the [Retrieve Job Status](#Retrieve_Job_Status) endpoint to query the status of the request using the job ID.
