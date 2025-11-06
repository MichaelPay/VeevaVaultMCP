<!-- 
VaultAPIDocs Section: # Picklists
Original Line Number: 31486
Generated: August 30, 2025
Part 15 of 38
-->

# Picklists

Picklists allow users to select a value for a field from a range of predefined options. The API supports retrieving picklists and picklist values, creating and deleting picklist values, and updating picklist value labels and names. The API does not support creating, updating, or deleting the picklists themselves; this must be done in the Admin UI.

Learn about [managing picklists](https://platform.veevavault.help/en/lr/1269) in Vault Help, which includes [picklist limits](https://platform.veevavault.help/en/lr/1269#limits).

## Retrieve All Picklists

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/picklists
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "errorCodes": null,
    "picklists": [
        {
            "name": "issue_source__v",
            "label": "Source",
            "kind": "global",
            "systemManaged": false,
            "usedIn": [
                {
                    "objectName": "issue_escalation__v",
                    "propertyName": "issue_source__v"
                }
            ]
        },
        {
            "name": "third_party_service__v",
            "label": "Third Party Service?",
            "kind": "global",
            "systemManaged": false,
            "usedIn": [
                {
                    "objectName": "adverse_event_report__v",
                    "propertyName": "third_party_service__v"
                }
            ]
        },
        {
            "name": "exception_item_error_status__sys",
            "label": "User Exception Item Error Status",
            "kind": "global",
            "systemManaged": false,
            "usedIn": [
                {
                    "objectName": "exception_item__sys",
                    "propertyName": "error_status__sys"
                }
            ]
        },
        {
            "name": "audit_program_sig_type__sys",
            "label": "Audit Program Signature Type",
            "kind": "global",
            "systemManaged": false,
            "usedIn": [
                {
                    "objectName": "audit_program_sig__sys",
                    "propertyName": "signature_type__sys"
                }
            ]
        },
        {
            "name": "country_cda__v",
            "label": "Country",
            "kind": "global",
            "systemManaged": true,
            "usedIn": [
                {
                    "objectName": "country__v",
                    "propertyName": "country_cda__v"
                }
            ]
        },
        {
        "name": "email_template_type__v",
        "label": "Email Template Type",
        "kind": "global",
                "system": true,
            "usedIn": [
                {
                    "documentTypeName": "email_template__v",
                    "propertyName": "emailTemplateType_b"
                }
            ]
        },
        {
            "name": "license_type__v",
            "label": "License Type",
            "kind": "user",
            "system": true
        }
  ],
  "errorType": null
}
'''

Retrieve all picklists in the authenticated Vault which the authenticated user has access to view.

GET `/api/{version}/objects/picklists`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

Metadata Field

Description

`name`

Picklist name. This is used only in the API and displayed in the Admin UI.

`label`

Picklist label. This is used in the API and UI. Users see the label on document and object picklist fields.

`kind`

There are two kinds of picklists: `global` picklists apply to documents and objects; `user` picklists apply to Vault users.

`system`

If `true`, the picklist values cannot be added, edited, or removed. This attribute may not appear for all picklists.

`systemManaged`

Indicates if the picklist is system-managed. If `true`, picklist values cannot be added, picklist names cannot be modified, and picklist value names cannot be edited.

`usedIn`

The document type or object in which the picklist is defined.

`documentTypeName`

For document picklists, this is the document type name in which the picklist is defined.

`objectName`

For object picklists, this is the object name in which the picklist is defined.

`propertyName`

For document picklists, this is the document field name using the picklist. For object picklists, this is the object field name using the picklist.

## Retrieve Picklist Values

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/picklists/license_type__v
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Success",
  "picklistValues": [
    {
      "name": "full__v",
      "label": "Full User"
    },
    {
      "name": "read_only__v",
      "label": "Read-only User"
    },
    {
      "name": "external__v",
      "label": "External User"
    },
    {
      "name": "view_based__v",
      "label": "View-Based User"
    }
  ]
}
'''

> Request: System-Managed Dependencies

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/picklists/state_cda__v
'''

> Response: System-Managed Dependencies

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "picklistValues": [
        {
            "name": "ad-02__v",
            "label": "Canillo"
        },
        {
            "name": "ad-03__v",
            "label": "Encamp"
        },
        {
            "name": "ad-04__v",
            "label": "La Massana"
        }
    ],
"controllingPicklistName": "country_cda__v",
    "picklistDependencies": {
        "ad__v": [
            "ad-02__v",
            "ad-03__v",
            "ad-04__v",
            "ad-05__v",
            "ad-06__v",
            "ad-07__v",
            "ad-08__v"
        ],
        "ae__v": [
            "ae-aj__v",
            "ae-az__v",
            "ae-du__v",
            "ae-fu__v",
            "ae-rk__v",
            "ae-sh__v",
            "ae-uq__v"
        ]
   }
}
'''

Retrieve all available values configured on a picklist.

GET `/api/{version}/objects/picklists/{picklist_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{picklist_name}`

The picklist `name` field value (`license_type__v`, `product_family__c`, `region__c`, etc.)

#### Response Details

On `SUCCESS`, the response returns the available values on a picklist in ascending order, designated by the picklist value’s `order` attribute. Retrieve the `order` of the picklist values with the [Retrieve Component Record (XML/JSON)](#Retrieve_Component_Record) endpoint on the `Picklist` component.

If the picklist is system-managed and has dependencies, the response also returns the `controllingPicklistName` and lists all `picklistDependencies`. Learn more about [managing picklist dependencies in Vault Help](https://platform.veevavault.help/en/lr/772652).

The response includes the following information for each picklist value:

Name

Description

`name`

The picklist value name. This is used only in the API and displayed in the Admin UI.

`label`

The picklist value label. This is used in the API and UI. Users see the label when selecting picklist values.

## Create Picklist Values

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "value_1=North America" \
-d "value_2=Central America" \
-d "value_3=South America" \
https://myvault.veevavault.com/api/v25.2/objects/picklists/regions__c
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Created picklist value(s).",
  "picklistValues": [
    {
      "name": "north_america__c",
      "label": "North America"
    },
    {
      "name": "central_america__c",
      "label": "Central America"
    },
    {
      "name": "south_america__c",
      "label": "South America"
    }
  ]
}
'''

Add new values to a picklist. Learn about [picklist limits in Vault Help](https://platform.veevavault.help/en/lr/1269#limits).

POST `/api/{version}/objects/picklists/{picklist_name}`

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

`{picklist_name}`

The picklist `name` field value (`license_type__v`, `product_family__c`, `region__c`, etc.)

#### Body Parameters

In the body of the request, use `value_1`, `value_2`, etc., set to alphanumeric values. Enter each new picklist value `label` as they will be displayed in the UI.

You do not need to enter a `name` value, instead, Vault uses the `label` to create the picklist value `name`.

You cannot specify picklist order on creation. New picklist values are added in the order they are submitted, after any existing values in the picklist. To re-order picklist values, use the Vault UI or [Vault Toolbox](/mdl/#Reorder_Picklist_Values_Vault_Toolbox).

#### Response Details

Metadata Field

Description

`name`

The picklist value name. This is used to reference this value in the API, and displayed to Vault Admins in the UI.

`label`

The picklist value label. Users see this label when selecting picklist values. Maximum 128 characters.

## Update Picklist Value Label

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "north_america__c=North America/United States" \
https://myvault.veevavault.com/api/v25.2/objects/picklists/regions__c
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Updated picklist value(s).",
  "picklistValues": [
    {
      "name": "north_america__c",
      "label": "North America/United States"
    }
  ]
}
'''

Change a picklist value `label` (only). To change a picklist value `name`, see the [next section](#Update_Picklist_Value_Name) below.

Use caution when editing picklist labels or names. When these attributes are changed, they affect all existing document and object metadata that refer to the picklist. For users in the UI who are accustomed to seeing a particular selection, the changes may cause confusion. This may also break existing integrations that access picklist values via the API.

PUT `/api/{version}/objects/picklists/{picklist_name}`

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

`{picklist_name}`

The picklist `name` field value (`license_type__v`, `product_family__c`, `region__c`, etc.)

#### Request Details

To change an existing picklist value `label`, use its picklist value `name` set to a new label. The picklist value `name` will remain unchanged. For example, to change the label of the existing `"north_america__c=North America"`, enter `"north_america__c=North America/United States"`. You may include one or more picklist values in the request.

#### Response Details

As shown above, only the picklist value `label` has changed. The picklist value `name` remains the same. The new label will be automatically updated on all documents and objects in which it is used. In the UI, users will see the new label when selecting values for the picklist. In the UI, Admins will see the new name in **Business Admin > Picklists > {Picklist}**.

## Update Picklist Value

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "name=north_america_united_states" \
https://myvault.veevavault.com/api/v25.2/objects/picklists/regions__c/north_america__c
'''

> Response

'''
{
  "responseStatus": "SUCCESS"
}
'''

Change a picklist value `name` or `status`. To change a picklist value `label`, see [Update Picklist Value Label](#Update_Picklist_Value_Label).

Use caution when editing picklist value names. When you change a picklist value name, it may affect existing document and object metadata that refer to the picklist. This may also break existing integrations that access picklist values via the API.

PUT `/api/{version}/objects/picklists/{picklist_name}/{picklist_value_name}`

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

`{picklist_name}`

The picklist `name` field value (`license_type__v`, `product_family__c`, `region__c`, etc.)

`{picklist_value_name}`

The picklist value `name` field value (`north_america__c`, `south_america__c`, etc.)

#### Body Parameters

At least one of the following parameters is required:

Name

Description

`name`conditional

The new name for a picklist value. This does not affect the label. Vault adds `__c` after processing. Special characters and double underscores `__` are not allowed.

`status`conditional

The new status for a picklist value. Valid values are `active` or `inactive`.

#### Response Details

Only the picklist value `name` is changed. The picklist value `label` remains the same. In the UI, Admins will see the new name in **Business Admin > Picklists > {Picklist}**.

## Inactivate Picklist Value

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/picklists/regions__c/north_america_united_states__c
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Inactivated picklist value.",
  "name": "north_america_united_states__c"
}
'''

Inactivate a value from a picklist. This does not affect picklist values that are already in use.

DELETE `/api/{version}/objects/picklists/{picklist_name}/{picklist_value_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{picklist_name}`

The picklist `name` field value (`license_type__v`, `product_family__c`, `region__c`, etc.)

`{picklist_value_name}`

The picklist value `name` field value (`north_america__c`, `south_america__c`, etc.)
