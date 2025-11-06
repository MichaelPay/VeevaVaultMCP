<!-- 
VaultAPIDocs Section: # SCIM
Original Line Number: 29738
Generated: August 30, 2025
Part 13 of 38
-->

# SCIM

System for Cross-domain Identity Management ([SCIM](http://www.simplecloud.info/)) is designed to make managing user identities in cloud-based applications and services easier. Vault API is based on SCIM 2.0.

All SCIM endpoints require a Vault session ID which can be used as Bearer tokens.

## Discovery Endpoints

### Retrieve SCIM Provider

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.com/api/v25.2/scim/v2/ServiceProviderConfig
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig"
    ],
    "documentationUri": "https://developer.veevavault.com",
    "patch": {
        "supported": false
    },
    "bulk": {
        "supported": false,
        "maxOperations": 0,
        "maxPayloadSize": 0
    },
    "filter": {
        "supported": false,
        "maxResults": 1000
    },
    "changePassword": {
        "supported": false
    },
    "sort": {
        "supported": true
    },
    "etag": {
        "supported": false
    },
    "authenticationSchemes": [
        {
            "name": "OAuth Bearer Token",
            "description": "Authentication scheme using the OAuth Bearer Token Standard",
            "type": "oauthbearertoken",
            "primary": true
        }
    ],
    "meta": {
        "resourceType": "ServiceProviderConfig",
        "location": "https://promomats-template.vaultdev.com/api/v25.2/scim/v2/ServiceProviderConfig"
    }
}
'''

Retrieve a JSON that describes the SCIM specification features available on the currently authenticated Vault.

GET `/api/{version}/scim/v2/ServiceProviderConfig`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

#### Response Details

The attributes returned in the JSON object are defined in Section 5 of [RFC7643](https://tools.ietf.org/html/rfc7643).

### Retrieve All SCIM Schema Information

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.com/api/v25.2/scim/v2/Schemas
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:api:messages:2.0:ListResponse"
    ],
    "totalResults": 6,
    "Resources": [
        {
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:Schema"
            ],
            "id": "urn:ietf:params:scim:schemas:core:2.0:User",
            "name": "User",
            "description": "User Account",
            "attributes": [
                {
                    "name": "active",
                    "type": "boolean",
                    "multiValued": false,
                    "description": "A Boolean value indicating the User's administrative status.",
                    "required": false,
                    "caseExact": true,
                    "mutability": "readWrite",
                    "returned": "default",
                    "uniqueness": "none"
                },
                {
                    "name": "displayName",
                    "type": "string",
                    "multiValued": false,
                    "description": "The name of the User, suitable for display to end-users. The name SHOULD be the full name of the User being described if known.",
                    "required": false,
                    "caseExact": false,
                    "mutability": "readOnly",
                    "returned": "default",
                    "uniqueness": "none"
                }
            ]
        }

    ]
}
'''

Retrieve information about all SCIM schema specifications supported by a Vault SCIM service provider.

GET `/api/{version}/scim/v2/Schemas`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

### Retrieve Single SCIM Schema Information

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.com/api/v25.2/scim/v2/Schemas/urn:ietf:params:scim:schemas:extension:veevavault:2.0:User
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:Schema"
    ],
    "id": "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
    "name": "VaultSCIMUser",
    "description": "Veeva Vault User",
    "attributes": [
        {
            "name": "createdBy",
            "type": "complex",
            "subAttributes": [
                {
                    "name": "$ref",
                    "type": "reference",
                    "multiValued": false,
                    "description": "The URI of the SCIM resource representing the User",
                    "required": true,
                    "caseExact": false,
                    "mutability": "readOnly",
                    "returned": "default",
                    "uniqueness": "none",
                    "referenceTypes": [
                        "User"
                    ]
                },
                {
                    "name": "value",
                    "type": "string",
                    "multiValued": false,
                    "description": "The id of the SCIM resource representing a User",
                    "required": true,
                    "caseExact": false,
                    "mutability": "readOnly",
                    "returned": "default",
                    "uniqueness": "none"
                }
            ],
            "multiValued": false,
            "description": "The user who has created this record.",
            "required": false,
            "caseExact": false,
            "mutability": "readOnly",
            "returned": "default",
            "uniqueness": "none"
        }
    ]
}
'''

Retrieve information about a single SCIM schema specification supported by a Vault SCIM service provider.

GET `/api/{version}/scim/v2/Schemas/{id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

#### URI Path Parameters

Name

Description

`id`

The ID of a specific schema. For example, `urn:ietf:params:scim:schemas:extension:veevavault:2.0:User`.

### Retrieve All SCIM Resource Types

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.com/api/v25.2/scim/v2/ResourceTypes
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:api:messages:2.0:ListResponse"
    ],
    "totalResults": 4,
    "Resources": [
        {
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:ResourceType"
            ],
            "id": "User",
            "name": "User",
            "description": "User Account",
            "endpoint": "/Users",
            "schema": "urn:ietf:params:scim:schemas:core:2.0:User",
            "schemaExtensions": [
                {
                    "schema": "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
                    "required": true
                },
                {
                    "schema": "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User",
                    "required": false
                }
            ],
            "meta": {
                "resourceType": "Resource Type",
                "location": "https://promomats-template.vaultdev.com/api/v25.2/scim/v2/ResourceTypes/User"
            }
        },
        {
            "schemas": [
                "urn:ietf:params:scim:schemas:core:2.0:ResourceType"
            ],
            "id": "SecurityProfile",
            "name": "SecurityProfile",
            "description": "Security Profile",
            "endpoint": "/SecurityProfiles",
            "schema": "urn:ietf:params:scim:schemas:extension:veevavault:2.0:SecurityProfile",
            "meta": {
                "resourceType": "Resource Type",
                "location": "https://promomats-template.vaultdev.com/api/v25.2/scim/v2/ResourceTypes/SecurityProfile"
            }
}
'''

Retrieve the types of SCIM resources available. Each resource type defines the endpoints, the core schema URI that defines the resource, and any supported schema extensions.

GET `/api/{version}/scim/v2/ResourceTypes`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

### Retrieve Single SCIM Resource Type

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.com/api/v25.2/scim/v2/ResourceTypes/SecurityProfile
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:ResourceType"
    ],
    "id": "SecurityProfile",
    "name": "SecurityProfile",
    "description": "Security Profile",
    "endpoint": "/SecurityProfiles",
    "schema": "urn:ietf:params:scim:schemas:extension:veevavault:2.0:SecurityProfile",
    "meta": {
        "resourceType": "Resource Type",
        "location": "https://promomats-template.vaultdev.com/api/v25.2/scim/v2/ResourceTypes/SecurityProfile"
    }
}
'''

Retrieve a single SCIM resource type. Defines the endpoints, the core schema URI which defines this resource, and any supported schema extensions.

GET `/api/{version}/scim/v2/ResourceTypes/{type}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

#### URI Path Parameters

Name

Description

`type`

A specific resource type. You can retrieve all available types from the [Retrieve All SCIM Resource Types](#SCIM_Retrieve_Resource_Types) endpoint, where the value for this parameter is the `id` value.

## Users

### Retrieve All Users with SCIM

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.com/api/v25.2/scim/v2/Users
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
        "urn:ietf:params:scim:schemas:core:2.0:User",
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
    ],
    "id": "100084",
    "meta": {
        "created": "2018-01-24T21:28:47.000Z",
        "lastModified": "2018-05-22T04:51:21.000Z",
        "resourceType": "User",
        "location": "https://veepharm.com/api/v25.2/scim/v2/Users/100084"
    },
    "active": true,
    "displayName": "Kimathi Gills",
    "emails": [
        {
            "value": "kg@veepharm.com",
            "type": "work"
        }
    ],
    "locale": "en_US",
    "name": {
        "familyName": "Gills",
        "givenName": "Kimathi"
    },
    "preferredLanguage": "en",
    "timezone": "America/Los_Angeles",
    "userName": "kimathi@veepharm.com",
    "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User": {
        "createdBy": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/Users/1",
            "value": "1"
        },
        "domainAdmin": false,
        "favoriteDocNewComment": false,
        "favoriteDocNewContent": false,
        "favoriteDocNewStatus": false,
        "lastLogin": "2018-01-26T19:13:20.000Z",
        "lastModifiedBy": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/Users/1",
            "value": "1"
        },
        "licenseType": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/LicenseTypes/full__v",
            "value": "full__v"
        },
        "lifecycle": "vault_membership_lifecycle__sys",
        "lifecycleState": "active_state__sys",
        "productAnnouncementEmails": false,
        "securityPolicy": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/SecurityPolicies/2525",
            "value": "2525"
        },
        "securityProfile": {
            "value": "business_admin__v",
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/SecurityProfiles/business_admin__v"
        },
        "systemAvailabilityEmails": false
    },
    "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
        "manager": "61603"
    }
}
'''

Retrieve all users with SCIM.

GET `/api/{version}/scim/v2/Users`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

#### Query Parameters

Name

Description

`filter`

Optional: Filter for a specific attribute value. Must be in the format `{attribute} eq "{value}"`. For example, to filter for a particular user name, `userName eq "john"`. Complex expressions are not supported, and `eq` is the only supported operator.

`attributes`

Optional: Include specified attributes only. Enter multiple values in a comma separated list. For example, to include only user name and email in the response, `attributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned.

`excludedAttributes`

Optional: Exclude specific attributes from the response. Enter multiple values in a comma separated list. For example, to exclude user name and email from the response, `excludedAttributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned and cannot be excluded.

`sortBy`

Optional: Specify an attribute or sub-attribute to order the response. For example, you can sort by the `displayName` attribute, or the `name.familyName` sub-attribute. If omitted, the response is sorted by `id`. Note that the following attributes are not supported:

-   `securityPolicy`
-   `securityProfile`
-   `locale`
-   `preferredLanguage`

`sortOrder`

Optional: Specify the order in which the `sortBy` parameter is applied. Allowed values are `ascending` or `descending`. If omitted, defaults to `ascending`.

`count`

Optional: Specify the number of query results per page, for example, `10`. Negative values are treated as `0`, and `0` returns no results except for `totalResults`. If omitted, defaults to `1000`.

`startIndex`

Optional: Specify the index of the first result. For example, `10` would omit the first 9 results and begin on result 10. Omission, negative values, and `0` is treated as `1`.

### Retrieve Single User with SCIM

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.com/api/v25.2/scim/v2/Users/61579?attributes=userName,emails
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
        "urn:ietf:params:scim:schemas:core:2.0:User"
    ],
    "id": "61579",
    "emails": [
        {
            "value": "mmurray@veepharm.com",
            "type": "work"
        }
    ],
    "userName": "mmurray@veepharm.com"
}
'''

Retrieve a specific user with SCIM.

GET `/api/{version}/scim/v2/Users/{id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

#### URI Path Parameters

Name

Description

`id`

The ID of a specific user.

#### Query Parameters

Name

Description

`filter`

Optional: Filter for a specific attribute value. Must be in the format `{attribute} eq "{value}"`. For example, to filter for a particular user name, `userName eq "john"`. Complex expressions are not supported, and `eq` is the only supported operator.

`attributes`

Optional: Include specified attributes only. Enter multiple values in a comma separated list. For example, to include only user name and email in the response, `attributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned.

`excludedAttributes`

Optional: Exclude specific attributes from the response. Enter multiple values in a comma separated list. For example, to exclude user name and email from the response, `excludedAttributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned and cannot be excluded.

### Retrieve Current User with SCIM

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.com/api/v25.2/scim/v2/Me?attributes=userName,emails,meta
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
        "urn:ietf:params:scim:schemas:core:2.0:User"
    ],
    "id": "61579",
    "meta": {
        "created": "2018-01-09T23:07:46.000Z",
        "lastModified": "2018-06-19T22:48:30.000Z",
        "resourceType": "User",
        "location": "https://veepharm.com/api/v25.2/scim/v2/Users/61579"
    },
    "emails": [
        {
            "value": "mmurray@veepharm.com",
            "type": "work"
        }
    ],
    "userName": "mmurray@veepharm.com"
}
'''

Retrieve the currently authenticated user with SCIM.

GET `/api/{version}/scim/v2/Me`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

#### Query Parameters

Name

Description

`attributes`

Optional: Include specified attributes only. Enter multiple values in a comma separated list. For example, to include only user name and email in the response, `attributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned.

`excludedAttributes`

Optional: Exclude specific attributes from the response. Enter multiple values in a comma separated list. For example, to exclude user name and email from the response, `excludedAttributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned and cannot be excluded.

### Update Current User with SCIM

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
https://veepharm.com/api/v25.2/scim/v2/Me?attributes=userName,name
'''

> Body

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
        "urn:ietf:params:scim:schemas:core:2.0:User"
    ],
    "name": {
                "familyName": "Murray",
                "givenName": "Megan"
    }
}
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
        "urn:ietf:params:scim:schemas:core:2.0:User"
    ],
    "id": "61579",
    "name": {
        "familyName": "Murray",
        "givenName": "Megan"
    },
    "userName": "mmurray@veepharm.com"
}
'''

Update the currently authenticated user with SCIM.

PUT `/api/{version}/scim/v2/Me`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

#### Query Parameters

Name

Description

`attributes`

Optional: Include specified attributes only. Enter multiple values in a comma separated list. For example, to include only user name and email in the response, `attributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned.

`excludedAttributes`

Optional: Exclude specific attributes from the response. Enter multiple values in a comma separated list. For example, to exclude user name and email from the response, `excludedAttributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned and cannot be excluded.

#### Body Parameters

The body of your request should be a JSON file with the information you want to update for your user. You can include any editable attribute. Invalid attributes are ignored. You can set single-valued attributes to blank using `null`, or an empty array `[]` for multi-valued attributes.

You can determine which of the core attributes are editable based on schemas. If the `mutability` is `readWrite`, the attribute is editable.

### Create User with SCIM

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/scim+json" \
--data-binary @"C:\Vault\Users\create_users_scim.json" \
https://veepharm.com/api/v25.2/scim/v2/Users
'''

> Body

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
        "urn:ietf:params:scim:schemas:core:2.0:User"
    ],
    "userName": "AbigailSmith@veepharm.com",
    "emails": [
        {
            "value": "abigail.smith@veepharm.com",
             "type": "work"
        }
    ],
    "name": {
                "familyName": "Smith",
                "givenName": "Abigail"
            },
    "preferredLanguage": "en",
    "locale": "en_US",
    "timezone": "America/Los_Angeles",
    "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User": {
    "securityProfile": {
                    "value": "system_admin__v"
                }
  }
}
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
        "urn:ietf:params:scim:schemas:core:2.0:User"
    ],
    "id": "114055",
    "meta": {
        "created": "2018-05-29T23:44:08.000Z",
        "lastModified": "2018-05-29T23:44:08.000Z",
        "resourceType": "User",
        "location": "https://veepharm.com/api/v25.2/scim/v2/Users/114055"
    },
    "active": true,
    "displayName": "Abigail Smith",
    "emails": [
        {
            "value": "abigail.smith@veepharm.com",
            "type": "work"
        }
    ],
    "locale": "en_US",
    "name": {
        "familyName": "Smith",
        "givenName": "Abigail"
    },
    "preferredLanguage": "en",
    "timezone": "America/Los_Angeles",
    "userName": "AbigailSmith@veepharm.com",
    "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User": {
        "createdBy": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/Users/61579",
            "value": "61579"
        },
        "extendedAttributes": [
            {
                "name": "is_asset_portal_user__sys",
                "value": "false"
            }
        ],
        "lastModifiedBy": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/Users/61579",
            "value": "61579"
        },
        "licenseType": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/LicenseTypes/full__v",
            "value": "full__v"
        },
        "lifecycle": "vault_membership_lifecycle__sys",
        "lifecycleState": "active_state__sys",
        "securityPolicy": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/SecurityPolicies/2525",
            "value": "2525"
        },
        "securityProfile": {
            "value": "system_admin__v",
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/SecurityProfiles/system_admin__v"
        }
    }
}
'''

Create a user with SCIM.

POST `/api/{version}/scim/v2/Users`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

`Content-Type`

`application/json` or `application/scim+json`

#### Body Parameters

The body of your request should be a JSON file with the required information for your new user. The following fields are required, but you can add any other editable field in the request. Note that an Admin may set additional fields as required in your Vault.

Name

Description

`schemas`required

A JSON array of the schemas required to create this user. These may differ depending on the fields you wish to set for this user.

`userName`required

The user name for the new user. Must be in the format `name@domain.com`, and the domain must match the Vault.

`emails`required

A JSON array with the email information for a user. The array must include the following sub-attributes:

-   `value`: The email address in the format `name@domain.com`.
-   `type`:The email type, which is `work`. Other types are not supported.
-   Note that the `primary` sub-attribute is ignored.

`name`required

A JSON object for the user’s first name (`givenName`) and last name (`familyName`).

`preferredLanguage`required

The language for the user. Value is the language abbreviation, for example, `en`.

`locale`required

The user’s locale, in the format language\_country. For example, `en_US`.

`timezone`required

The user’s timezone, for example, `America/Los_Angeles`.

`securityProfile`required

A JSON object with the user’s security profile, set with the `value` sub-attribute. For example, `"securityProfile": { "value": "system_admin__v"}`.

`securityPolicy`optional

A JSON object with the user’s security policy, set with the `value` sub-attribute. If omitted, defaults to `Basic`.

`licenseType`optional

A JSON object with the user’s license type, set with the `value` sub-attribute. If omitted, defaults to `full__v`.

#### Response Details

On `SUCCESS`, the response includes the full details of the newly created user.

### Update User with SCIM

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/scim+json" \
--data-binary @"C:\Vault\Users\update_user_scim.json" \
https://veepharm.com/api/v25.2/scim/v2/Users/56798
'''

> Body

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
        "urn:ietf:params:scim:schemas:core:2.0:User"
    ],
    "userName": "AbigailSmith@veepharm.com",
    "name": {
                "familyName": "Smith",
                "givenName": "Abigail"
            },
    "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User": {
    "securityProfile": {
                    "value": "system_admin__v"
                }
  }
}
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
        "urn:ietf:params:scim:schemas:core:2.0:User"
    ],
    "id": "93521",
    "meta": {
        "created": "2018-01-09T23:07:43.000Z",
        "lastModified": "2018-05-30T22:21:18.000Z",
        "resourceType": "User",
        "location": "https://veepharm.com/api/v25.2/scim/v2/Users/93521"
    },
    "active": true,
    "displayName": "Abigail Smith",
    "emails": [
        {
            "value": "abigail.smith@veepharm.com",
            "type": "work"
        }
    ],
    "locale": "en_US",
    "name": {
        "familyName": "Smith",
        "givenName": "Abigail"
    },
    "preferredLanguage": "en",
    "timezone": "America/Los_Angeles",
    "userName": "a.smithn@veepharm.com",
    "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User": {
        "createdBy": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/Users/1",
            "value": "1"
        },
        "domainAdmin": true,
        "favoriteDocNewComment": false,
        "favoriteDocNewContent": false,
        "favoriteDocNewStatus": false,
        "lastLogin": "2018-05-30T20:53:10.000Z",
        "lastModifiedBy": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/Users/61579",
            "value": "61579"
        },
        "licenseType": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/LicenseTypes/full__v",
            "value": "full__v"
        },
        "lifecycle": "vault_membership_lifecycle__sys",
        "lifecycleState": "active_state__sys",
        "productAnnouncementEmails": false,
        "securityPolicy": {
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/SecurityPolicies/2525",
            "value": "2525"
        },
        "securityProfile": {
            "value": "system_admin__v",
            "$ref": "https://veepharm.com/api/v25.2/scim/v2/SecurityProfiles/system_admin__v"
        },
        "systemAvailabilityEmails": false
    }
}
'''

Update fields values on a single user with SCIM.

PUT `/api/{version}/scim/v2/Users/{id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

`Content-Type`

`application/json` or `application/scim+json`

#### URI Path Parameters

Name

Description

`id`

The `id` of the user you wish to update.

#### Body Parameters

The body of your request should be a JSON file with the information you want to update for your user. You can include any editable attribute. Invalid attributes are ignored. You can set single-valued attributes to blank using `null`, or an empty array `[]` for multi-valued attributes.

You can determine which of the core attributes are editable based on schemas. If the `mutability` is `readWrite`, the attribute is editable.

#### Response Details

On `SUCCESS`, the reponse contains the new information for the updated user.

## Retrieve SCIM Resources

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.com/api/v25.2/scim/v2/SecurityProfiles
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:api:messages:2.0:ListResponse"
    ],
    "totalResults": 20,
    "Resources": [
        {
            "schemas": [
                "urn:ietf:params:scim:schemas:extension:veevavault:2.0:SecurityProfile"
            ],
            "id": "business_admin__v",
            "meta": {
                "created": "2018-02-09T09:41:14.000Z",
                "lastModified": "2018-02-09T09:41:14.000Z",
                "resourceType": "SecurityProfile",
                "location": "https://promomats-template.vaultdev.com/api/v25.2/scim/v2/SecurityProfiles/business_admin__v"
            },
            "active": true,
            "displayName": "Business Administrator"
        },
        {
            "schemas": [
                "urn:ietf:params:scim:schemas:extension:veevavault:2.0:SecurityProfile"
            ],
            "id": "document_user__v",
            "meta": {
                "created": "2018-02-09T09:41:14.000Z",
                "lastModified": "2018-02-09T09:41:14.000Z",
                "resourceType": "SecurityProfile",
                "location": "https://promomats-template.vaultdev.com/api/v25.2/scim/v2/SecurityProfiles/document_user__v"
            },
            "active": true,
            "displayName": "Document User"
        }
    ]

}
'''

Retrieve a single SCIM resource type. Defines the endpoints, the core schema URI which defines this resource, and any supported schema extensions.

GET `/api/{version}/scim/v2/{type}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

#### URI Path Parameters

Name

Description

`type`

The resource type to retrieve. You can retrieve all available types from the [Retrieve All SCIM Resource Types](#SCIM_Retrieve_Resource_Types) endpoint, where the value for this parameter is the `endpoint` value.

#### Query Parameters

Name

Description

`filter`

Optional: Filter for a specific attribute value. Must be in the format `{attribute} eq "{value}"`. For example, to filter for a particular user name, `userName eq "john"`. Complex expressions are not supported, and `eq` is the only supported operator.

`attributes`

Optional: Include specified attributes only. Enter multiple values in a comma separated list. For example, to include only user name and email in the response, `attributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned.

`excludedAttributes`

Optional: Exclude specific attributes from the response. Enter multiple values in a comma separated list. For example, to exclude user name and email from the response, `excludedAttributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned and cannot be excluded.

`sortBy`

Optional: Specify an attribute or sub-attribute to order the response. For example, you can sort by the `displayName` attribute, or the `name.familyName` sub-attribute. If omitted, the response is sorted by `id`. Note that the following attributes are not supported:

-   `securityPolicy`
-   `securityProfile`
-   `locale`
-   `preferredLanguage`

`sortOrder`

Optional: Specify the order in which the `sortBy` parameter is applied. Allowed values are `ascending` or `descending`. If omitted, defaults to `ascending`.

`count`

Optional: Specify the number of query results per page, for example, `10`. Negative values are treated as `0`, and `0` returns no results except for `totalResults`. If omitted, defaults to `1000`.

`startIndex`

Optional: Specify the index of the first result. For example, `10` would omit the first 9 results and begin on result 10. Omission, negative values, and `0` is treated as `1`.

## Retrieve Single SCIM Resource

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.com/api/v25.2/scim/v2/SecurityProfiles/business_admin__v
'''

> Response

'''
{
    "schemas": [
        "urn:ietf:params:scim:schemas:extension:veevavault:2.0:SecurityProfile"
    ],
    "id": "business_admin__v",
    "meta": {
        "created": "2018-02-09T09:41:14.000Z",
        "lastModified": "2018-02-09T09:41:14.000Z",
        "resourceType": "SecurityProfile",
        "location": "https://veepharm.com/api/v25.2/scim/v2/SecurityProfiles/business_admin__v"
    },
    "active": true,
    "displayName": "Business Administrator"
}
'''

Retrieve a single SCIM resource.

GET `/api/{version}/scim/v2/{type}/{id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/scim+json`

#### URI Path Parameters

Name

Description

`type`

The resource type to retrieve. You can retrieve all available types from the [Retrieve All SCIM Resource Types](#SCIM_Retrieve_Resource_Types) endpoint, where the value for this parameter is the `endpoint` value.

`id`

The ID of the resource to retrieve. You can retrieve all resource IDs from a particular resource type with the [Retrieve SCIM Resources](#SCIM_Retrieve_Resource_Type_Info) endpoint. For example, `business_admin__v`.

#### Query Parameters

Name

Description

`attributes`

Optional: Include specified attributes only. Enter multiple values in a comma separated list. For example, to include only user name and email in the response, `attributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned.

`excludedAttributes`

Optional: Exclude specific attributes from the response. Enter multiple values in a comma separated list. For example, to exclude user name and email from the response, `excludedAttributes=userName,emails`. Note that the `schemas` and `id` attributes are always returned and cannot be excluded.
