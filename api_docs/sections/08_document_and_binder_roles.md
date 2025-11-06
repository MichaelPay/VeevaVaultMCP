<!-- 
VaultAPIDocs Section: # Document & Binder Roles
Original Line Number: 22121
Generated: August 30, 2025
Part 8 of 38
-->

# Document & Binder Roles

Documents and binders can have different roles available to them depending on their type and lifecycles. There are a set of standard roles that ship with Vault: `owner__v`, `viewer__v`, and `editor__v`. In addition, Admins can create custom roles defined per lifecycle. Learn more about roles in [Vault Help](https://platform.veevavault.help/en/lr/2662).

Through the Role APIs, you can:

-   Retrieve available roles on documents and binders
-   Determine who can be assigned to roles
-   Retrieve default users who are assigned automatically within the Vault UI
-   Retrieve who is currently assigned to a role
-   Add additional users and groups to a role
-   Remove users and groups from roles

All responses return user and group IDs. To determine user and group names and other data, use the [Users](#Users) or [Groups](#Vault_Groups_API_Reference) API.

For roles on object records, see [Object Roles](#Object_Roles).

## Document Roles

Retrieve and manage roles on documents. Learn about document roles in [Vault Help](https://platform.veevavault.help/en/lr/2662).

### Retrieve All Document Roles

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/245/roles
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Document roles retrieved",
    "errorCodes": null,
    "documentRoles": [
        {
            "name": "reviewer__v",
            "label": "Reviewer",
            "assignedUsers": [
                25496,
                26231
            ],
            "assignedGroups": [
                1,
                2
            ],
            "availableUsers": [
                25496,
                26231,
                28874
            ],
            "availableGroups": [
                1,
                2,
                3
            ],
            "defaultUsers": [
                25496,
                26231
            ],
            "defaultGroups": [
                1,
                2
            ]
        }
      ],
    "errorType": null
}
'''

Retrieve all available roles on a document and the users and groups assigned to them.

GET `/api/{version}/objects/documents/{doc_id}/roles`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

#### Response Details

On `SUCCESS`, the response lists all document roles and includes the following for each role:

Name

Description

`name`

The role name available to developers. For example, `reviewer__v`.

`label`

The UI-friendly role label available to Admins in the Vault UI. For example, `Reviewer`.

`assignedUsers`

List of the IDs of users assigned to this role

`assignedGroups`

List of the IDs of groups assigned to this role

`availableUsers`

List of the IDs of users available for this role

`availableGroups`

List of the IDs of groups available to this role

`defaultUsers`

List of the IDs of default users assigned to this role

`defaultGroups`

List of the IDs of default groups assigned to this role

### Retrieve Document Role

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/245/roles/reviewer__v
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Document role retrieved",
    "errorCodes": null,
    "documentRoles": [
        {
            "name": "reviewer__v",
            "label": "Reviewer",
            "assignedUsers": [
                25496,
                26231
            ],
            "assignedGroups": [
                1,
                2
            ],
            "availableUsers": [
                25496,
                26231,
                28874
            ],
            "availableGroups": [
                1,
                2,
                3
            ],
            "defaultUsers": [
                25496,
                26231
            ],
            "defaultGroups": [
                1,
                2
            ]
        }
    ],
    "errorType": null
}
'''

Retrieve a specific role on a document and the users and groups assigned to it.

GET `/api/{version}/objects/documents/{doc_id}/roles/{role_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

`{role_name}`

The name of the role to retrieve. For example, `owner__v`.

#### Response Details

On `SUCCESS`, the response lists the following for the specific role retrieved:

Name

Description

`name`

The role name available to developers. For example, `reviewer__v`.

`label`

The UI-friendly role label available to Admins in the Vault UI. For example, `Reviewer`.

`assignedUsers`

List of the IDs of users assigned to this role

`assignedGroups`

List of the IDs of groups assigned to this role

`availableUsers`

List of the IDs of users available for this role

`availableGroups`

List of the IDs of groups available to this role

`defaultUsers`

List of the IDs of default users assigned to this role

`defaultGroups`

List of the IDs of default groups assigned to this role

### Assign Users & Groups to Roles on a Single Document

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "consumer__v.users=35565,35571" \
-d "approver__v.users-45585,45594" \
https://myvault.veevavault.com/api/v25.2/objects/documents/245/roles
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Document roles updated",
  "updatedRoles": {
    "consumer__v": {
      "users": [
        19376,18234,19456
      ]
    },
    "legal__c": {
      "groups": [
        19365,18923
      ]
    }
  }
}
'''

Assign users and groups to roles on a single document.

POST `/api/{version}/objects/documents/{doc_id}/roles`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

#### Body Parameters

Name

Description

`{role__v}.users`optional

A string of comma-separated user id values for the new role. For example, `reviewer__v.users = "3003, 4005"`.

`{role__v}.groups`optional

A string of comma-separated group id values for the new group. For example, `reviewer__v.groups = "20, 21"`.

#### Response Details

The response includes IDs of the users and groups successfully assigned to each role on the document.

### Assign Users & Groups to Roles on Multiple Documents & Binders

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Document Roles\assign_document_roles.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/roles/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 771,
            "reviewer__v.groups": [
                3311303,
                4411606
            ],
            "reviewer__v.users": [
                12021,
                12022,
                12023,
                12124
            ]
        },
        {
            "responseStatus": "SUCCESS",
            "id": 772,
            "reviewer__v.groups": [
                3311303,
                4411606
            ],
            "reviewer__v.users": [
                12021,
                12022,
                12023,
                12124
            ]
        },
        {
           "responseStatus":"FAILURE",
           "id":"773",
           "errors":[
              {
                 "type":"INVALID_DATA",
                 "message":"Error message describing why the users and groups were not assigned to roles on this document.."
              }
           ]
        }
    ]
}
'''

Assign users and groups to roles on documents and binders in bulk.

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 1000.

Assigning users and groups to document roles is additive. For example, if groups 1, 2, and 3 are currently assigned to a particular role and you assign groups 3, 4, and 5 to the same role, the final list of groups assigned to the role will be 1, 2, 3, 4, and 5. Users and groups (IDs) in the input that are either invalid (not recognized) or cannot be assigned to a role due to permissions are ignored and not processed.

POST `/api/{version}/objects/documents/roles/batch`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

You can add parameters in the request body or upload them as a CSV file. When adding parameters in the request body, you can only assign one set of users and groups to one set of documents and binders (`docIds`). Use a CSV file to assign different sets of users and groups to different documents and binders by adding multiple rows to the `id` column.

Name

Description

`id`conditional

The document or binder ID. Required if uploading a CSV file.

`docIds`conditional

A list of document and binder IDs. Required instead of `id` when adding parameters to the request body.

`role__v.users`conditional

A string of comma-separated user `id` values for the new role.

`role__v.groups`optional

A string of comma-separated user `id` values for the new group.

For example,

`id`

`reviewer__v.users`

`reviewer__v.groups`

`approver__v.users`

`approver__v.groups`

771

“12021,12022”

“3311303,3311404”

22124

4411606

#### Response Details

The response includes the IDs of the users and groups successfully assigned each role.

### Remove Users & Groups from Roles on a Single Document

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/1234/roles/consumer__v.user/1008313
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "User/group deleted from document role",
  "updatedRoles": {
    "consumer__v": {
      "users": [
        1008313
      ]
    }
  }
}
'''

Remove users and groups from roles on a single document.

DELETE `/api/{version}/objects/documents/{doc_id}/roles/{role_name_and_user_or_group}/{id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The `id` value of the document from which to remove roles.

`{role_name_and_user_or_group}`

The name of the role from which to remove the user or group followed by either `user` or `group`. The format is `{role_name}.{user_or_group}`. For example, `consumer__v.user`.

`{id}`

The `id` value of the user or group to remove from the role.

#### Response Details

On `SUCCESS`, the response lists the `id` of the user or group removed from the document role. On `FAILURE`, the response returns an error message describing the reason for the failure. For example, a user or group may not be removed if the role assignment is system-managed.

### Remove Users & Groups from Roles on Multiple Documents & Binders

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: application/json" \
--data-binary @"C:\Vault\Document Roles\remove_document_roles.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/roles/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 5,
            "coordinator__v.users": [
                1008313
            ],
            "consumer__v.users": [
                1006595
            ]
        }
    ]
}
'''

Remove users and groups from roles on documents and binders in bulk.

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 1000.

DELETE `/api/{version}/objects/documents/roles/batch`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

You can add parameters in the request body or upload them as a CSV file. When adding parameters in the request body, you can only remove the same set of users and groups from the same set of documents and binders (`docIds`). Use a CSV file to remove different sets of users and groups from different documents or binders by adding multiple rows to the `id` column.

Name

Description

`id`conditional

The document or binder ID. Required if uploading a CSV file.

`docIds`conditional

A list of document and binder IDs. Required instead of `id` when adding parameters to the request body.

`role__v.users`optional

A string of comma-separated user `id` values to remove.

`role__v.groups`optional

A string of comma-separated group `id` values to remove.

For example,

`id`

`reviewer__v.users`

`reviewer__v.groups`

`approver__v.users`

`approver__v.groups`

771

“12021,12022”

“3311303,3311404”

22124

4411606

#### Response Details

On `SUCCESS`, the response lists the IDs of the users or groups removed from the provided document roles. On `FAILURE`, the response returns an error message describing the reason for the failure. For example, a user or group may not be removed if the role assignment is system-managed.

## Binder Roles

Retrieve and manage roles on binders. Learn about document roles in [Vault Help](https://platform.veevavault.help/en/lr/2662).

### Retrieve All Binder Roles

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/245/roles
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Roles retrieved",
    "errorCodes": null,
    "documentRoles": [
        {
            "name": "reviewer__v",
            "label": "Reviewer",
            "assignedUsers": [
                25496,
                26231
            ],
            "assignedGroups": [
                1,
                2
            ],
            "availableUsers": [
                25496,
                26231,
                28874
            ],
            "availableGroups": [
                1,
                2,
                3
            ],
            "defaultUsers": [
                25496,
                26231
            ],
            "defaultGroups": [
                1,
                2
            ]
        }
      ],
    "errorType": null
}
'''

Retrieve all available roles on a binder and the users and groups assigned to them.

GET `/api/{version}/objects/binders/{binder_id}/roles`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{binder_id}`

The binder `id` field value.

#### Response Details

On `SUCCESS`, the response lists all binder roles and includes the following for each role:

Name

Description

`name`

The role name available to developers. For example, `reviewer__v`.

`label`

The UI-friendly role label available to Admins in the Vault UI. For example, _Reviewer_.

`assignedUsers`

List of the IDs of users assigned to this role

`assignedGroups`

List of the IDs of groups assigned to this role

`availableUsers`

List of the IDs of users available for this role

`availableGroups`

List of the IDs of groups available to this role

`defaultUsers`

List of the IDs of default users assigned to this role

`defaultGroups`

List of the IDs of default groups assigned to this role

### Retrieve Binder Role

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/245/roles/reviewer__v
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Role retrieved",
    "errorCodes": null,
    "documentRoles": [
        {
            "name": "reviewer__v",
            "label": "Reviewer",
            "assignedUsers": [
                25496,
                26231
            ],
            "assignedGroups": [
                1,
                2
            ],
            "availableUsers": [
                25496,
                26231,
                28874
            ],
            "availableGroups": [
                1,
                2,
                3
            ],
            "defaultUsers": [
                25496,
                26231
            ],
            "defaultGroups": [
                1,
                2
            ]
        }
      ],
    "errorType": null
}
'''

Retrieve a specific role on a binder and the users and groups assigned to it.

GET `/api/{version}/objects/binders/{binder_id}/roles/{role_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{binder_id}`

The binder `id` field value.

`{role_name}`

The name of the role to retrieve. For example, `owner__v`.

#### Response Details

On `SUCCESS`, the response lists the following for the specific role retrieved:

Name

Description

`name`

The role name available to developers. For example, `reviewer__v`.

`label`

The UI-friendly role label available to Admins in the Vault UI. For example, _Reviewer_.

`assignedUsers`

List of the IDs of users assigned to this role

`assignedGroups`

List of the IDs of groups assigned to this role

`availableUsers`

List of the IDs of users available for this role

`availableGroups`

List of the IDs of groups available to this role

`defaultUsers`

List of the IDs of default users assigned to this role

`defaultGroups`

List of the IDs of default groups assigned to this role

### Assign Users & Groups to Roles on a Single Binder

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "consumer__v.users=35565,35571" \
-d "approver__v.users-45585,45594" \
https://myvault.veevavault.com/api/v25.2/objects/binders/245/roles
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Roles updated",
  "updatedRoles": {
    "consumer__v": {
      "users": [
        19376,18234,19456
      ]
    },
    "legal__c": {
      "groups": [
        19365,18923
      ]
    }
  }
}
'''

Assign users and groups to roles on a single binder.

POST `/api/{version}/objects/binders/{binder_id}/roles`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{binder_id}`

The binder `id` field value.

#### Body Parameters

Name

Description

`{role__v}.users`optional

A string of comma-separated user id values for the new role. For example, `reviewer__v.users = "3003, 4005"`.

`{role__v}.groups`optional

A string of comma-separated group id values for the new group. For example, `reviewer__v.groups = "20, 21"`.

#### Response Details

The response includes IDs of the users and groups successfully assigned to each role on the document.

### Remove Users & Groups from Roles on a Single Binder

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/1234/roles/consumer__v.user/1008313
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "User/group deleted from role",
  "updatedRoles": {
    "consumer__v": {
      "users": [
        1008313
      ]
    }
  }
}
'''

Remove users and groups from roles on a single binder.

DELETE `/api/{version}/objects/binders/{binder_id}/roles/{role_name_and_user_or_group}/{id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{binder_id}`

The `id` value of the binder from which to remove roles.

`{role_name_and_user_or_group}`

The name of the role from which to remove the user or group followed by either `user` or `group`. The format is `{role_name}.{user_or_group}`. For example, `consumer__v.user`.

`{id}`

The `id` value of the user or group to remove from the role.

#### Response Details

On `SUCCESS`, the response lists the `id` of the user or group removed from the binder role. On `FAILURE`, the response returns an error message describing the reason for the failure. For example, a user or group may not be removed if the role assignment is system-managed.
