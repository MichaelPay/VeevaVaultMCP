<!-- 
VaultAPIDocs Section: # Documents
Original Line Number: 2369
Generated: August 30, 2025
Part 5 of 38
-->

# Documents

Vault is a highly configurable system designed to reflect the business model of documents. Each Vault can have different document types, document fields, etc. The Document Metadata APIs allow you to query the Vault to understand what document-based metadata is available to use. Learn about [Documents & Binders](https://platform.veevavault.help/en/lr/21581) in Vault Help.

## Retrieve Document Fields

### Retrieve All Document Fields

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/properties
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "properties": [
       {
           "name": "id",
           "type": "id",
           "required": true,
           "maxLength": 20,
           "minValue": 0,
           "maxValue": 9223372036854775807,
           "repeating": false,
           "systemAttribute": true,
           "editable": false,
           "setOnCreateOnly": true,
           "disabled": false,
           "hidden": true,
           "queryable": true,
           "facetable": false
       },
       {
           "name": "name__v",
           "scope": "DocumentVersion",
           "type": "String",
           "required": true,
           "maxLength": 100,
           "repeating": false,
           "systemAttribute": true,
           "editable": true,
           "setOnCreateOnly": false,
           "disabled": false,
           "label": "Name",
           "section": "generalProperties",
           "sectionPosition": 0,
           "hidden": false,
           "queryable": true,
           "shared": false,
           "helpContent": "Displayed throughout application for the document, including in Library, Reporting, Notifications and Workflows.",
           "definedInType": "type",
           "definedIn": "base_document__v",
           "noCopy": false,
           "secureRelationship": false,
           "facetable": false
       },
       {
           "name": "template_document__v",
           "scope": "DocumentVersion",
           "type": "Boolean",
           "required": false,
           "repeating": false,
           "systemAttribute": true,
           "editable": false,
           "setOnCreateOnly": false,
           "disabled": false,
           "defaultValue": "false",
           "label": "Template Document",
           "section": "generalProperties",
           "sectionPosition": 1001,
           "hidden": true,
           "queryable": true,
           "shared": false,
           "definedInType": "type",
           "definedIn": "base_document__v",
           "noCopy": false,
           "secureRelationship": false,
           "facetable": true
       }
    ]
}
'''

Retrieve all standard and custom document fields and field properties.

GET `/api/{version}/metadata/objects/documents/properties`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

The response lists all standard and custom document fields and field metadata. Note the following field metadata:

Metadata Field

Description

`required`

When `true`, the field value must be set when creating new documents.

`editable`

When `true`, the field value can be defined by the currently authenticated user. When `false`, the field value is read-only or system-managed, or the current user does not have adequate permissions to edit this field.

`setOnCreateOnly`

When `true`, the field value can only be set once (when creating new documents).

`hidden`

Boolean indicating field availability to the UI. When `true`, the field is never available to nor visible in the UI. When `false`, the field is always available to the UI but visibility to users is subject to field-level security overrides. If field-level security is configured to hide a field for the currently authenticated API user, the field is not returned in this API response.

`queryable`

When `true`, field values can be retrieved using [VQL](/vql/#introduction_to_vault_queries). If field-level security is configured to hide the field from the user running this API, the field is not queryable by that user and will not appear in the API response.

`noCopy`

When `true`, field values are not copied when using the **Make a Copy** action.

`facetable`

When `true`, the field is available for use as a faceted filter in the Vault UI. Learn more about [faceted filters in Vault Help](https://platform.veevavault.help/en/lr/1616).

### Retrieve Common Document Fields

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "docIds=101,102,103" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/properties/find_common
'''

> Response

'''
    {
      "name": "submission_date__c",
      "scope": "DocumentVersion",
      "type": "Date",
      "required": false,
      "repeating": false,
      "systemAttribute": false,
      "editable": true,
      "setOnCreateOnly": false,
      "disabled": false,
      "label": "Submission Date",
      "section": "submissionDetails",
      "sectionPosition": 3,
      "hidden": false,
      "queryable": true,
      "shared": true,
      "usedIn": [
        {
          "key": "promotional_piece__c",
          "type": "type"
        },
        {
          "key": "compliance_package__v",
          "type": "type"
        },
        {
          "key": "claim__c",
          "type": "type"
        }
      ]
    }
    {
      "name": "withdrawal_effective_date__c",
      "scope": "DocumentVersion",
      "type": "Date",
      "required": false,
      "repeating": false,
      "systemAttribute": false,
      "editable": true,
      "setOnCreateOnly": false,
      "disabled": false,
      "label": "Withdrawal Effective Date",
      "section": "pieceDetails",
      "sectionPosition": 17,
      "hidden": false,
      "queryable": true,
      "shared": false,
      "definedInType": "type",
      "definedIn": "promotional_piece__c"
    }
'''

Retrieve all document fields and field properties which are common to (shared by) a specified set of documents. This allows you to determine which document fields are eligible for bulk update.

Learn about [Shared Fields](https://platform.veevavault.help/en/lr/4884) in Vault Help.

POST `/api/{version}/metadata/objects/documents/properties/find_common`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Name

Description

`docIds`required

Input a comma-separated list of document `id` field values.

#### Response Details

The response includes all fields shared by the three documents (`docIds=101,102,103`).

Vault allows you to reuse fields across multiple document types by creating shared fields, which exist outside the context of a document type. You can create shared fields or convert existing fields into shared fields in the Vault Admin application. If a shared field is only used in one document type, you can also convert it to a non-shared field. All document fields, except for `noCopy`, include the Boolean `shared` document field. A value of `true` indicates which the field is shared and the following additional fields are included:

Note the following field metadata:

Metadata Field

Description

`shared`

When true, this field is a shared field.

`usedIn` (`key`)

When `shared` is `true`, this lists the document types/subtypes/classifications which share the field.

`usedIn` (`type`)

When `shared` is `true`, this indicates if the shared field is defined at the document type, subtype, or classification level.

`noCopy`

When `true`, field values are not copied when using the **Make a Copy** action.

### Review Results
- **Location:** `veevavault/services/documents/fields_service.py`
- **Functions:** `retrieve_all_document_fields`, `retrieve_common_document_fields`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Retrieve Document Types

Document type refers both to the structure of hierarchical fields (Type > Subtype > Classification) that determines the relevant document fields, rendition types, and other settings for a document, and to the highest level in that hierarchy. Learn about [Configuring Document Types in Vault Help](https://platform.veevavault.help/en/lr/618).

### Retrieve All Document Types

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/types
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "types": [
        {
            "label": "Base Document",
            "value": "https://etmf-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/base_document__v"
        },
        {
            "label": "Centralized Testing",
            "value": "https://etmf-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/centralized_testing__c"
        },
        {
            "label": "Central Trial Documents",
            "value": "https://etmf-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/central_trial_documents__c"
        },
        {
            "label": "Country Master File",
            "value": "https://etmf-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/country_master_file__v"
        },
        {
            "label": "Data Management",
            "value": "https://etmf-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/data_management__c"
        },
        {
            "label": "Final CRF",
            "value": "https://etmf-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/final_crf__v"
        },
        {
            "label": "IP and Trial Supplies",
            "value": "https://etmf-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/ip_and_trial_supplies__c"
        },
    ],
    "lock": "https://etmf-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/lock"
}
'''

Retrieve all document types. These are the top-level of the document hierarchy (Type > Subtype > Classification).

GET `/api/{version}/metadata/objects/documents/types`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

The response lists all document types configured in the Vault. These vary by Vault application and configuration.

-   Standard types end in `__v`.
-   Some Vaults include sample types `__c`.
-   Admins can configure custom types `__c`.

The response includes the following information:

Metadata Field

Description

`types`

List of all standard and custom document types in your Vault.  
These are the top-level of the document hierarchy (Type > Subtype > Classification).

`label`

Label of each document type as seen in the API and UI.

`value`

URL to retrieve the metadata associated with each document type.

`lock`

URL to retrieve the document lock metadata (document check-out).

The `label` is displayed in the UI. These can be applied to documents and binders.

### Retrieve Document Type

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "name": "promotional_piece__c",
  "label": "Promotional Piece",
  "properties": [
    {
      "name": "id",
      "type": "id",
      "required": true,
      "maxLength": 20,
      "minValue": 0,
      "maxValue": 9223372036854775807,
      "repeating": false,
      "systemAttribute": true,
      "editable": false,
      "setOnCreateOnly": true,
      "disabled": false,
      "hidden": true,
      "queryable": true,
      "facetable": false
    }
  ],
  "renditions": [
    "viewable_rendition__v",
    "production_proof__c",
    "distribution_package__c",
    "imported_rendition__c",
    "veeva_distribution_package__c"
  ],
  "relationshipTypes": [
    {
      "label": "CrossLink Latest Bindings",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    },
    {
      "label": "CrossLink Latest Steady State Bindings",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    },
    {
      "label": "Linked Documents",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    },
    {
      "label": "Based on",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    }
  ],
  "templates": [
    {
      "label": "ANSM Submission",
      "name": "ansm_submission__c",
      "kind": "binder",
      "definedIn": "promotional_piece__c",
      "definedInType": "type"
    }
  ],
  "availableLifecycles": [
    {
      "name": "promotional_piece__c",
      "label": "Promotional Piece"
    }
  ],
  "subtypes": [
    {
      "label": "Advertisement",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/advertisement__c"
    },
    {
      "label": "Direct Mail",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/direct_mail__c"
    },
    {
      "label": "Formulary Announcement",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/formulary_announcement__c"
    },
    {
      "label": "Internal Communication",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/internal_communication__c"
    },
    {
      "label": "Managed Markets Program",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/managed_markets_program__c"
    },
    {
      "label": "Healthcare Practitioner Resources",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/healthcare_practitioner_resources__c"
    },
    {
      "label": "Convention Item",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/convention_item__c"
    }
  ]
}
'''

Retrieve all metadata from a document type, including all of its subtypes (when available).

GET `/api/{version}/metadata/objects/documents/types/{type}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{type}`

The document type. See [Retrieve Document Types](#Retrieve_Document_Types).

#### Response Details

The response includes all metadata for the document specified type. If the type contains subtypes in the document type hierarchy, the list of subtypes and the URLs pointing to their metadata will be included in the response. The list of document fields defined for the specified type are also included in the response.

Each document type may include some or all of the following fields:

Metadata Field

Description

`name`

Name of the document type. Used primarily in the API.

`label`

Label of the document type as seen in the API and UI.

`renditions`

List of all rendition types available for the document type.

`relationshipTypes`

List of all relationship types available for the document type.

`properties`

List of all the document fields associated to the document type.

`processes`

List of all processes available for the document type (when configured).

`etmfDepartment`

In eTMF Vaults only. List of all eTMF departments available for the document type (when configured).

`referenceModels`

In eTMF Vaults only. List of all reference models available for the document type.

`defaultWorkflows`

List of all workflows available for the document type.

`availableLifecycles`

List of all lifecycles available for the document type.

`templates`

List of all templates available for the document type (when configured).

`subtypes`

List of all standard and custom document subtypes available for the document type.

### Retrieve Document Subtype

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/advertisement__c
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "name": "advertisement__c",
  "label": "Advertisement",
  "properties": [
    {
      "name": "id",
      "type": "id",
      "required": true,
      "maxLength": 20,
      "minValue": 0,
      "maxValue": 9223372036854775807,
      "repeating": false,
      "systemAttribute": true,
      "editable": false,
      "setOnCreateOnly": true,
      "disabled": false,
      "hidden": true,
      "queryable": true
    },
    {
      "name": "name__v",
      "scope": "DocumentVersion",
      "type": "String",
      "required": true,
      "maxLength": 100,
      "repeating": false,
      "systemAttribute": true,
      "editable": true,
      "setOnCreateOnly": false,
      "disabled": false,
      "label": "Name",
      "section": "generalProperties",
      "sectionPosition": 1,
      "hidden": false,
      "queryable": true,
      "shared": false,
      "helpContent": "The document name.",
      "definedInType": "type",
      "definedIn": "base_document__v"
    },
    {
      "name": "product__v",
      "scope": "DocumentVersion",
      "type": "ObjectReference",
      "required": true,
      "repeating": true,
      "systemAttribute": true,
      "editable": true,
      "setOnCreateOnly": false,
      "disabled": false,
      "objectType": "product__v",
      "label": "Product",
      "section": "productInformation",
      "sectionPosition": 1,
      "hidden": false,
      "queryable": true,
      "shared": false,
      "definedInType": "type",
      "definedIn": "base_document__v",
      "relationshipType": "reference",
      "relationshipName": "document_product__vr"
    },
  ],
  "classifications": [
    {
      "label": "Print",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/advertisement__c/classifications/print__c"
    },
    {
      "label": "Television",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/advertisement__c/classifications/television__c"
    },
    {
      "label": "Web",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/advertisement__c/classifications/web__c"
    }
  ],
  "relationshipTypes": [
    {
      "label": "Linked Documents",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    },
    {
      "label": "Based on",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    },
    {
      "label": "Related Claims",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    },
    {
      "label": "Supporting Documents",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    },
  ],
  "templates": [
    {
      "label": "ANSM Submission",
      "name": "ansm_submission__c",
      "kind": "binder",
      "definedIn": "promotional_piece__c",
      "definedInType": "type"
    }
  ],
  "availableLifecycles": [
    {
      "name": "promotional_piece__c",
      "label": "Promotional Piece"
    }
  ]
}
'''

Retrieve all metadata from a document subtype, including all of its classifications (when available).

GET `/api/{version}/metadata/objects/documents/types/{type}/subtypes/{subtype}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{type}`

The document type. See [Retrieve Document Types](#Retrieve_Document_Types).

`{subtype}`

The document subtype. See [Retrieve Document Type](#Retrieve_Document_Type).

#### Response Details

The response may contain the following details, depending on the configuration of your Vault:

Name

Description

`name`

Name of the document subtype.

`label`

UI label for the document subtype.

`properties`

List of all the document fields associated to the document subtype.

`classifications`

This will not appear if the subtype has no classifications.

`templates`

List of all templates available for the document subtype. This will not appear if the subtype has no templates.

`availableLifecycles`

List of all lifecycles available for the document subtype.

`renditions`

List of all rendition types available for the document subtype. This will not appear if the subtype has no renditions configured.

### Retrieve Document Classification

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/subtypes/advertisement__c/classifications/print__c
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "name": "advertisement__c",
  "label": "Advertisement",
  "properties": [
    {
      "name": "id",
      "type": "id",
      "required": true,
      "maxLength": 20,
      "minValue": 0,
      "maxValue": 9223372036854775807,
      "repeating": false,
      "systemAttribute": true,
      "editable": false,
      "setOnCreateOnly": true,
      "disabled": false,
      "hidden": true,
      "queryable": true
    },
    {
      "name": "name__v",
      "scope": "DocumentVersion",
      "type": "String",
      "required": true,
      "maxLength": 100,
      "repeating": false,
      "systemAttribute": true,
      "editable": true,
      "setOnCreateOnly": false,
      "disabled": false,
      "label": "Name",
      "section": "generalProperties",
      "sectionPosition": 1,
      "hidden": false,
      "queryable": true,
      "shared": false,
      "helpContent": "The document name.",
      "definedInType": "type",
      "definedIn": "base_document__v"
    },
    {
      "name": "product__v",
      "scope": "DocumentVersion",
      "type": "ObjectReference",
      "required": true,
      "repeating": true,
      "systemAttribute": true,
      "editable": true,
      "setOnCreateOnly": false,
      "disabled": false,
      "objectType": "product__v",
      "label": "Product",
      "section": "productInformation",
      "sectionPosition": 1,
      "hidden": false,
      "queryable": true,
      "shared": false,
      "definedInType": "type",
      "definedIn": "base_document__v",
      "relationshipType": "reference",
      "relationshipName": "document_product__vr"
    },
  ],
  "relationshipTypes": [
    {
      "label": "Linked Documents",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    },
    {
      "label": "Based on",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    },
    {
      "label": "Related Claims",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    },
    {
      "label": "Supporting Documents",
      "value": "https://promomats-veevapharm.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional_piece__c/relationships"
    },
  ],
  "templates": [
    {
      "label": "ANSM Submission",
      "name": "ansm_submission__c",
      "kind": "binder",
      "definedIn": "promotional_piece__c",
      "definedInType": "type"
    }
  ],
  "availableLifecycles": [
    {
      "name": "promotional_piece__c",
      "label": "Promotional Piece"
    }
  ]
}
'''

Retrieve all metadata from a document classification.

GET `/api/{version}/metadata/objects/documents/types/{type}/subtypes/{subtype}/classifications/{classification}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{type}`

The document type. See [Retrieve Document Types](#Retrieve_Document_Types).

`{subtype}`

The document type. See [Retrieve Document Type](#Retrieve_Document_Type).

`{classification}`

The document classification. See [Retrieve Document Subtype](#Retrieve_Document_Subtype)

#### Response Details

The response may contain the following details, depending on the configuration of your Vault:

Name

Description

`name`

Name of the document subtype.

`label`

UI label for the document subtype.

`properties`

List of all the document fields associated to the document classification.

`templates`

List of all templates available for the document classification. This will not appear if the classification has no templates.

`availableLifecycles`

List of all lifecycles available for the document classification.

`renditions`

List of all rendition types available for the document classification. This will not appear if the classification has no renditions configured.

### Review Results
- **Location:** `veevavault/services/documents/types_service.py`
- **Functions:** `retrieve_all_document_types`, `retrieve_document_type`, `retrieve_document_subtype`, `retrieve_document_classification`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Retrieve Documents

The following rules govern document retrieval:

-   Vault only returns documents to which the logged in user has access to, even if more documents exist.
-   Vault only returns the latest version of each document. To return every version of a document, use the `versionscope=all` query parameter.
-   Vault returns a maximum of 200 documents per page. You can lower this number using the `limit` query parameter.

#### Identifying Binders

The document pseudo-field `binder__v` indicates whether the returned document is a document or a binder. The value of `true` means it is a binder, `false` or absence of this field means it is a document. If it is a binder, the binder sections are not listed as part of the response and must be determined using the [Retrieve Binder API](#Retrieve_Binder) with the `depth=all` query parameter.

#### Identifying CrossLink Documents

A document pseudo-field `crosslink__v` indicates whether the returned document is a regular document (`false`) or a CrossLink document (`true`).

### Retrieve All Documents

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "size": 69,
  "start": 0,
  "limit": 200,
  "documents": [
    {
      "document": {
        "id": 105,
        "version_id": "105_0_1",
        "binder__v": false,
        "coordinator__v": {
          "groups": [],
          "users": []
        },
        "owner__v": {
          "groups": [],
          "users": [
            25524
          ]
        },
        "approver__v": {
          "groups": [],
          "users": []
        },
        "reviewer__v": {
          "groups": [],
          "users": []
        },
        "viewer__v": {
          "groups": [],
          "users": []
        },
        "editor__v": {
          "groups": [],
          "users": []
        },
        "format__v": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "version_creation_date__v": "2016-03-23T22:03:04.094Z",
        "major_version_number__v": 0,
        "annotations_links__v": 0,
        "annotations_all__v": 2,
        "status__v": "Draft",
        "language__v": [
          "English"
        ],
        "suppress_rendition__v": "false",
        "filename__v": "cholecap_presentation_q316.pptx",
        "product__v": [
          "00P000000000101"
        ],
        "version_created_by__v": 25524,
        "country__v": [],
        "annotations_anchors__v": 0,
        "document_number__v": "PP-WD--0014",
        "minor_version_number__v": 1,
        "lifecycle__v": "Promotional Piece",
        "subtype__v": "Advertisement",
        "annotations_notes__v": 2,
        "allow_pdf_download__v": [
          "00W000000000201"
        ],
        "classification__v": "Other Electronic",
        "name__v": "CholeCap Presentation",
        "locked__v": false,
        "pages__v": 29,
        "restrict_fragments_by_product__v": true,
        "type__v": "Promotional Piece",
        "size__v": 623694,
        "md5checksum__v": "0405da0c29698e4249c2a0eca8f6642a",
        "annotations_unresolved__v": 2,
        "last_modified_by__v": 25524,
        "document_creation_date__v": "2016-03-23T22:03:04.094Z",
        "annotations_resolved__v": 0,
        "annotations_lines__v": 0,
        "version_modified_date__v": "2016-03-23T22:04:16.000Z",
        "created_by__v": 25524,
        "media__c": [
          "Print"
        ]
      }
    }
  ]
}
'''

Retrieve the latest version of documents and binders to which you have access.

GET `/api/{version}/objects/documents`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

You can optionally include one of the following parameters to filter the results:

Name

Description

`named_filter=My Documents`

Retrieves only documents for which you are the owner or which you have checked out.

`named_filter=Favorites`

Retrieves only documents which you have marked as favorites in the library.

`named_filter=Recent Documents`

Retrieves only documents which you have recently accessed.

`named_filter=Cart`

Retrieves only documents in your cart.

`scope=contents`

Searches only within the document content.

`scope=all`

Searches both within the document content and searchable document fields.

`versionscope=all`

Retrieves all document versions, rather than only the latest version.

`search={keyword}`

Search for documents based on a {keyword} in searchable document fields.

`limit`

Limit the number of documents to display. By default, Vault displays up to 200 documents per page.

`sort`

Return documents in a specific order by specifying a document field and either ascending (`ASC`) or descending (`DESC`) order. For example, `sort = name__v DESC`. The default is `sort = id ASC`. See [VQL documentation](/vql/#Query_Syntax_Structure) for more information.

`start`

The starting record number. The default is 0.

#### Response Details

On `SUCCESS`, Vault lists all documents and binders along with their fields and field values. If `binder__v = true`, the object is a binder. The document metadata returned will vary based on your Vault configuration. CrossLink documents are supported.

### Retrieve Document

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/450
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "document": {
        "id": 450,
        "binder__v": false,
        "allow_download_embedded_viewer__v": true,
        "reviewer__v": {
            "users": [
                25519,
                25516
            ],
            "groups": [
                1358979070034
            ]
        },
        "viewer__v": {
            "users": [
                25519,
                25516,
                25597
            ],
            "groups": [
                1358979070034
            ]
        },
        "distribution_contacts__v": {
            "users": [],
            "groups": []
        },
        "consumer__v": {
            "users": [],
            "groups": []
        },
        "approver__v": {
            "users": [
                25516
            ],
            "groups": []
        },
        "editor__v": {
            "users": [
                25519,
                25516
            ],
            "groups": []
        },
        "owner__v": {
            "users": [
                46916
            ],
            "groups": []
        },
        "coordinator__v": {
            "users": [],
            "groups": []
        },
        "crosslink__v": false,
        "lifecycle__v": "General Lifecycle",
        "version_created_by__v": 46916,
        "language__v": [
            "English"
        ],
        "minor_version_number__v": 1,
        "created_by__v": 46916,
        "annotations_lines__v": 0,
        "version_creation_date__v": "2015-03-12T16:24:33.539Z",
        "country__v": [],
        "md5checksum__v": "94e18bdbcf695c905a5968429e0c5204",
        "restrict_fragments_by_product__v": true,
        "annotations_notes__v": 0,
        "version_modified_date__v": "2015-03-12T16:24:54.000Z",
        "pages__v": 1,
        "major_version_number__v": 1,
        "annotations_anchors__v": 0,
        "product__v": [
            "1357662840293"
        ],
        "export_filename__v": "451Chole",
        "annotations_resolved__v": 0,
        "type__v": "Reference Document",
        "size__v": 11599,
        "description__v": "This is my document.",
        "status__v": "Draft",
        "annotations_unresolved__v": 0,
        "document_creation_date__v": "2015-02-25T01:26:55.845Z",
        "locked__v": false,
        "format__v": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "annotations_links__v": 0,
        "document_number__v": "REF-0201",
        "annotations_all__v": 0,
        "last_modified_by__v": 46916,
        "name__v": "CholeCap Information",
        "subtype__v": "Prescribing Information"
    },
    "renditions":
        {
        "viewable_rendition__v": "https://myvault.veevavault.com/api/v25.2/objects/documents/450/renditions/viewable_rendition__v",
        "veeva_distribution_package__c": "https://myvault.veevavault.com/api/v25.2/objects/documents/450/renditions/veeva_distribution_package__c"
    },
    "versions": [
        {
            "number": "0.1",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/450/versions/0/1"
        },
        {
            "number": "1.0",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/450/versions/1/0"
        },
        {
            "number": "1.1",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/450/versions/1/1"
        }
    ],
    "attachments": [
        {
            "id": 547,
            "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/450/attachments/547"
        }
    ]
}
'''

Retrieve all metadata from a document.

GET `/api/{version}/objects/documents/{doc_id}`

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

The boolean field `binder__v` indicates whether the returned document is a regular document (`true`) or a binder (`false`). The absence of this field means it is a document. Binder node structures are not listed as part of the response; they must be determined through the Binder API.

The boolean field `crosslink__v` indicates whether the returned document is a regular document (`true`) or a CrossLink document (`false`).

### Retrieve Document Versions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "versions": [
        {
            "number": "0.1",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/0/1"
        },
        {
            "number": "0.2",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/0/2"
        },
        {
            "number": "1.0",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/1/0"
        },
        {
            "number": "1.1",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/1/1"
        },
        {
            "number": "2.0",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/0"
        },
        {
            "number": "2.1",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/1"
        },
        {
            "number": "2.2",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/2"
        },
        {
            "number": "2.3",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/3"
        }
    ],
    "renditions":
        {
        "viewable_rendition__v": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions/viewable_rendition__v",
        "veeva_distribution_package__c": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions/veeva_distribution_package__c"
    }
}
'''

Retrieve all versions of a document.

GET `/api/{version}/objects/documents/{doc_id}/versions`

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

On `SUCCESS`, Vault returns a list of all available versions of the specified document. In the example response, document `id:534` has 8 different versions. Version 2.0 is the **latest steady state version**. Version 2.3 is the **latest version**. This document also has two different renditions: The `viewable_rendition__v` and a `veeva_distribution_package__c` rendition.

### Retrieve Document Version

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/3
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "document": {
        "id": 534,
        "allow_download_embedded_viewer__v": true,
        "reviewer__v": {
            "users": [
                46916,
                45589
            ],
            "groups": [
                1359484520721
            ]
        },
        "crosslink__v": false,
        "lifecycle__v": "General Lifecycle",
        "version_created_by__v": 46916,
        "language__v": [
            "English"
        ],
        "minor_version_number__v": 3,
        "created_by__v": 46916,
        "annotations_lines__v": 0,
        "version_creation_date__v": "2015-03-13T16:24:33.539Z",
        "country__v": [],
        "md5checksum__v": "94e18bdbcf695c905a5989629e0c5204",
        "restrict_fragments_by_product__v": true,
        "annotations_notes__v": 0,
        "version_modified_date__v": "2015-03-13T16:24:54.000Z",
        "pages__v": 1,
        "major_version_number__v": 2,
        "annotations_anchors__v": 0,
        "product__v": [
            "1357662840293"
        ],
        "export_filename__v": "WD",
        "annotations_resolved__v": 0,
        "type__v": "Reference Document",
        "size__v": 11518,
        "description__v": "",
        "status__v": "Draft",
        "annotations_unresolved__v": 0,
        "document_creation_date__v": "2015-02-25T01:26:55.845Z",
        "locked__v": false,
        "format__v": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "annotations_links__v": 0,
        "document_number__v": "REF-0059",
        "annotations_all__v": 0,
        "last_modified_by__v": 46916,
        "name__v": "WonderDrug Information",
        "binder__v": false,
        "subtype__v": "Prescribing Information"
    },
    "renditions": [
        {
        "viewable_rendition__v": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions/viewable_rendition__v",
        "veeva_distribution_package__c": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions/veeva_distribution_package__c"
        }
    ],
    "versions": [
        {
            "number": "2.3",
            "value": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/3"
        }
    ],
    "attachments": [
        {
            "id": 547,
            "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/attachments/547"
        },
        {
            "id": 561,
            "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/attachments/561"
        }
    ]
}
'''

Retrieve all fields and values configured on a document version.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

#### Response Details

On `SUCCESS`, Vault returns all fields and values for the specified version of the document. The example response shows information for document `id:534` version 2.3.

### Retrieve Document Version Text

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/201/versions/2/1/text
'''

> Response

'''
HIGHLIGHTS OF PRESCRIBING INFORMATION
----------------------WARNINGS AND PRECAUTIONS-----------------------­
These highlights do not include all the information needed to use
Skeletal muscle effects (e.g., myopathy and rhabdomyolysis): Risks increase CHOLECAP safely and effectively. See full prescribing information for
when higher doses are used concomitantly with cyclosporine, fibrates, and CHOLECAP.
'''

Retrieve the plain text of a specific document version.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/text`

#### Headers

Name

Description

`Accept`optional

`text/plain` (default). The format of the response will always be `text/plain` regardless of the value provided for the `Accept` header.

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

#### Response Details

On `SUCCESS`, Vault returns the plain text of the source file from the document.

On `FAILURE`, the response returns an error message describing the reason for the failure. For example, if the specified document is not found, no text is found, or the document is password-protected.

### Download Document File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/file?lockDocument=false > file
'''

> Response

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment;filename="CholeCap-Presentation.pptx"
'''

GET `/api/{version}/objects/documents/{doc_id}/file`

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

#### Query Parameters

Name

Description

`lockDocument`

Set to `true` to Check Out this document before retrieval. If omitted, defaults to `false`.

#### Response Details

On `SUCCESS`, Vault retrieves the latest version of the source file from the document. The HTTP Response Header `Content-Type` is set to `application/octet-stream`. The HTTP Response Header `Content-Disposition` contains a filename component which can be used when naming the local file. Note that for most downloads (larger file sizes), the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Download Document Version File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/3/file > file
'''

> Response

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment;filename="CholeCap-Presentation.pptx"
'''

Download the file of a specific document version.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/file`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

#### Response Details

On `SUCCESS`, Vault retrieves the specified version of the source file from the document. The HTTP Response Header `Content-Type` is set to `application/octet-stream`. The HTTP Response Header `Content-Disposition` contains a filename component which can be used when naming the local file.

### Download Document Version Thumbnail File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/3/thumbnail > thumbnail.png
'''

Download the thumbnail image file of a specific document version.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/thumbnail`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

#### Response Details

On `SUCCESS`, Vault returns the thumbnail image for the specified version of the document. The HTTP Response Header `Content-Type` is set to `image/png`.

### Review Results
- **Location:** `veevavault/services/documents/retrieval_service.py`
- **Functions:** `retrieve_all_documents`, `retrieve_document`, `retrieve_document_versions`, `retrieve_document_version`, `retrieve_document_version_text`, `download_document_file`, `download_document_version_file`, `download_document_version_thumbnail`
- **Updates Made:**
    - Added the `retrieve_document_version_text` function.
- **State:** Compliant with API documentation.

## Create Documents

### Create Single Document

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=@gludacta-document-01.docx" \
-F "name__v=Gludacta Document" \
-F "type__v=Promotional Piece" \
-F "subtype__v=Advertisement" \
-F "classification__v=Web" \
-F "lifecycle__v=Promotional Piece" \
-F "major_version_number__v=0" \
-F "minor_version_number__v=1" \
-F "product__v=0PR0303" \
-F "external_id__v=GLU-DOC-0773" \
https://myvault.veevavault.com/api/v25.2/objects/documents
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "successfully created document",
    "id": 773
}
'''

Create a single document.

The API supports all security settings.

POST `/api/{version}/objects/documents`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

`X-VaultAPI-MigrationMode`

When set to `true`, you can use the `status__v` field to create documents in any lifecycle state. Additionally, you can manually set the name, document number, and version number. Vault also bypasses entry criteria, entry actions, and event actions. You must have the _Document Migration_ permission to use this header. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### Body Parameters

There are multiple ways to create a document.

##### Create Document from Uploaded File

Most documents in your Vault are created from uploaded source files, such as a file from your computer. Learn about [Supported File Formats](https://platform.veevavault.help/en/lr/25210) in Vault Help. Once uploaded with values assigned to document fields, Vault generates the viewable rendition, e.g., “mydocument.docx.pdf”. Learn about [Viewable Renditions](https://platform.veevavault.help/en/lr/3815) in Vault Help.

Name

Description

`file`conditional

The filepath of the source document. The maximum allowed file size is 4GB. Only required when creating a document from an uploaded file. If omitted, creates a placeholder.

`name__v`required

The name of the new document.

`type__v`required

The name or label of the document type to assign to the new document.

`subtype__v`optional

The name or label of the document subtype (if one exists on the document type).

`classification__v`optional

The name or label of the document classification (if one exists on the document subtype).

`lifecycle__v`required

The name or label of the document lifecycle to assign to the new document.

`major_version_number__v`optional

The major version number to assign to the new document.

`minor_version_number__v`optional

The minor version number to assign to the new document.

##### Create Document from Template

When you create the new document, Vault copies the template file and uses that copy as the source file for the new document. This process bypasses the content upload process and allows for more consistent document creation. Document templates are associated with a specific document type, like documents themselves. Learn about [Document Templates](https://platform.veevavault.help/en/lr/5509) in Vault Help.

Name

Description

`fromTemplate`conditional

The name of the template to apply. Only required when creating a document from a template.

`name__v`required

The name of the new document.

`type__v`required

The name or label of the document type to assign to the new document.

`subtype__v`optional

The name or label of the document subtype (if applicable).

`classification__v`optional

The name or label of the document classification (if one exists on the document subtype).

`lifecycle__v`required

The name or label of the document lifecycle to assign to the new document.

`major_version_number__v`optional

The major version number to assign to the new document.

`minor_version_number__v`optional

The minor version number to assign to the new document.

**Optional Parameters in PromoMats**

In PromoMats Vaults, you can also optionally set the following parameters. Learn more about [PromoMats Standard Metrics in Vault Help](https://commercial.veevavault.help/en/lr/58143).

Name

Description

`global_content_type__v`optional

The name of the global content type to assign to the new document. If excluded, Vault creates the document with the default global content type, or as “Not Specified” if no default exists.

`content_creation_currency__v`optional

The `id` of the content creation currency type. If excluded, Vault creates the document with the default content creation currency, or as “Not Specified” if no default exists.

`content_creation_cost__v`optional

The `id` of the content creation cost. If excluded, Vault creates the document with the default content creation cost, or as “Not Specified” if no default exists.

##### Create Content Placeholder Document

Creating a content placeholder document is just like creating a document from an uploaded file, but the `file` parameter is not included in the request. Learn about [Content Placeholders](https://platform.veevavault.help/en/lr/15087) in Vault Help. Admin may set other standard or custom document fields to required in your Vault.

Name

Description

`name__v`required

The name of the new document.

`type__v`required

The name or label of the document type to assign to the new document.

`subtype__v`optional

The name or label of the document subtype (if one exists on the document type).

`classification__v`optional

The name or label of the document classification (if one exists on the document subtype).

`lifecycle__v`required

The name or label of the document lifecycle to assign to the new document.

`major_version_number__v`optional

The major version number to assign to the new document.

`minor_version_number__v`optional

The minor version number to assign to the new document.

##### Create Unclassified Document

Unclassified documents are documents which have a source file, but no document type. Learn about [Unclassified Documents](https://platform.veevavault.help/en/lr/15020) in Vault Help.

Name

Description

`file`conditional

The filepath of the source document. The maximum allowed file size is 4GB. Only required when creating a document from an uploaded file.

`type__v`required

Set the document type to `Unclassified` or `Undefined` (`undefined__v`).\*

`lifecycle__v`required

Set the document lifecycle to `Inbox` or `Unclassified` (`unclassified__v`).\*

In eTMF Vaults, you can also (optionally) set the following fields:

-   `product__v`
-   `study__v`
-   `study_country__v`
-   `site__v`

Any other fields included in the input will be ignored. The document `name__v` will default to the name of the uploaded file.

\* Prior to 21R1.3 (API v21.2), the `Unclassified` (`undefined__v`) document type and `Inbox` (`unclassified__v`) lifecycle were known as the `Undefined` document type and `Unclassified` lifecycle. Relabeling the `Undefined` document type and `Unclassified` lifecycle may impact the functionality of custom integrations that use the old labels. Check your integrations before updating this label. We recommend that customers experiencing errors change the labels back to their original values until this issue is resolved.

##### Create CrossLink Document

When creating a CrossLink document, you must include all document fields that are required for the specified document type/subtype/classification and no file is uploaded. You must also specify the Vault ID and document ID for the source document which will be bound to the new CrossLink document. Learn about [CrossLinks](https://platform.veevavault.help/en/lr/23143) in Vault Help.

Name

Description

`name__v`required

The name of the new CrossLink document.

`type__v`required

The label of the document type to assign to the new CrossLink document.

`subtype__v`optional

The label of the document subtype (if one exists on the document type).

`classification__v`optional

The label of the document classification (if one exists on the document subtype).

`lifecycle__v`required

The label of the document lifecycle to assign to the new CrossLink document.

`major_version_number__v`optional

The major version number to assign to the new CrossLink document

`minor_version_number__v`optional

The minor version number to assign to the new CrossLink document.

`source_vault_id__v`conditional

The Vault `id` field value of the Vault containing the source document that will be bound to the new CrossLink document. Only required when creating a CrossLink document. [Learn more](#Domain_Information).

`source_document_id__v`conditional

The document `id` field value of the source document that will be bound to the new CrossLink document. Only required when creating a CrossLink document.

`source_binding_rule__v`optional

Possible values are `Latest version`, `Latest Steady State version`, or `Specific Document version`. These define which version of the source document will be bound to the CrossLink document. If not specified, this defaults to the `Latest Steady State version`.

`bound_source_major_version__v`optional

When the `source_binding_rule__v` is set to `Specific Document version`, you must specify the major version number of the source document to bind to the CrossLink document.

`bound_source_minor_version__v`optional

When the `source_binding_rule__v` is set to `Specific Document version`, you must specify the minor version number of the source document to bind to the CrossLink document.

#### Response Details

On `SUCCESS`, the document is created and assigned a system-managed document `id` field value. The generated document `id` may not be in sequential order.

### Create Multiple Documents

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"filename" \
https://myvault.veevavault.com/api/v25.2/objects/documents/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 771,
            "external_id__v": "ALT-DOC-0771"
        },
        {
            "responseStatus": "SUCCESS",
            "id": 772,
            "external_id__v": "CHO-DOC-0772"
        },
        {
            "responseStatus": "SUCCESS",
            "id": 773,
            "external_id__v": "GLU-DOC-0773"
        },
        {
            "responseStatus": "FAILURE",
            "errors": [
                {
                    "type": "INVALID_DATA",
                    "message": "Error message describing why this document was not created."
                }
            ]
        }
    ]
}
'''

This endpoint allows you to create multiple documents at once with a CSV input file.

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

Note that this API does not support adding multi-value relationship fields by name. To add multi-value fields, you must first retrieve the ID values and add them to the relationship field.

The API supports all security settings except document lifecycle role defaults. You must create documents through the UI if your documents require document lifecycle role defaults. Learn more about [document lifecycle role defaults in Vault Help](https://platform.veevavault.help/en/lr/6572).

POST `/api/{version}/objects/documents/batch`

#### Headers

Name

Description

`Content-Type`

`text/csv`

`Accept`

`application/json` (default) or `text/csv`

`X-VaultAPI-MigrationMode`

When set to `true`, Vault allows you to create documents in any lifecycle state using the `status__v` field, and to manually set the name, document number, and version number. Vault also bypasses entry criteria, entry actions, and event actions. You must have the _Document Migration_ permission to use this header. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### Body Parameters

Prepare a CSV input file. There are multiple ways to create documents in bulk. The following shows the required standard fields needed to create documents, but an Admin may set other standard or custom document fields as required in your Vault. To find which fields are required, [retrieve document fields](#Retrieve_All_Document_Fields). You can also optionally include any editable document field.

##### Create Documents from Uploaded Files

You must first upload the document source files to your Vault’s [file staging](/docs/#ftp).

Name

Description

`file`conditional

The filepath of the source document. The maximum allowed file size is 500GB. Only required when creating a document from an uploaded file.

`name__v`required

The name of the new document.

`type__v`required

The name or label of the document type to assign to the new document.

`subtype__v`optional

The name or label of the document subtype (if one exists on the document type).

`classification__v`optional

The name or label of the document classification (if one exists on the document subtype).

`lifecycle__v`required

The name or label of the document lifecycle to assign to the new document.

`major_version_number__v`optional

The major version number to assign to the new document

`minor_version_number__v`optional

The minor version number to assign to the new document.

`suppressRendition`optional

Set to `true` to suppress generation of viewable renditions. The default is `false`.

`product__v`optional

Example: This is an example object reference field. To assign value for this field type, include either the document field name `product__v` or the document field name plus the name field on the object `product__v.name__v`.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-create-documents-from-uploaded-files-sample-csv-input.csv)

##### Create Documents from Templates

When you create a new document from a template, Vault copies the template file in your Vault and uses that copy as the source file for the new document.

Name

Description

`fromTemplate`conditional

The template to apply to the document. Only required when creating a document from a template.

`name__v`required

The name of the new document.

`type__v`required

The name or label of the document type to assign to the new document.

`subtype__v`optional

The name or label of the document subtype (if one exists on the document type).

`classification__v`optional

The name or label of the document classification (if one exists on the document subtype).

`lifecycle__v`required

The name or label of the document lifecycle to assign to the new document.

`major_version_number__v`optional

The major version number to assign to the new document

`minor_version_number__v`optional

The minor version number to assign to the new document.

`product__v`optional

Example: This is an example object reference field. To assign value for this field type, include either the document field name `product__v` or the document field name plus the name field on the object `product__v.name__v`.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-create-documents-from-document-template-sample-csv-input.csv)

##### Create Content Placeholder Documents

Vault allows you to create content placeholders when the associated file is not yet available. You can add the source document at a later date.

Name

Description

`file`required

Include this column in your input, but leave the values blank.

`name__v`required

The name of the new document.

`type__v`required

The name or label of the document type to assign to the new document.

`subtype__v`optional

The name or label of the document subtype (if one exists on the document type).

`classification__v`optional

The name or label of the document classification (if one exists on the document subtype).

`lifecycle__v`required

The name or label of the document lifecycle to assign to the new document.

`major_version_number__v`optional

The major version number to assign to the new document

`minor_version_number__v`optional

The minor version number to assign to the new document.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-create-content-placeholder-documents-sample-csv-input.csv)

##### Create Unclassified Documents

Unclassified documents are documents which have a source file, but no document type. The following fields are required, but you can include any editable document field.

Name

Description

`file`required

The filepath of the source document. The maximum allowed file size is 500GB.

`name__v`optional

The name of the new document.

`type__v`required

Set the document type to `Unclassified` or `Undefined` (`undefined__v`).\*

`lifecycle__v`required

Set the document lifecycle to `Inbox` or `Unclassified` (`unclassified__v`).\*

\* Prior to 21R1.3 (API v21.2), the `Unclassified` (`undefined__v`) document type and `Inbox` (`unclassified__v`) lifecycle were known as the `Undefined` document type and `Unclassified` lifecycle. Relabeling the `Undefined` document type and `Unclassified` lifecycle may impact the functionality of custom integrations that use the old labels. Check your integrations before updating this label. We recommend that customers experiencing errors change the labels back to their original values until this issue is resolved.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-create-unclassified-documents-sample-csv-input.csv)

#### Response Details

On `SUCCESS`, the documents are created and assigned a system-managed document `id` field value. The generated document `id` may not be in sequential order.

### Review Results
- **Location:** `veevavault/services/documents/creation_service.py`
- **Functions:** `create_single_document`, `create_multiple_documents`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Update Documents

### Update Single Document

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "language__v=English" \
-d "product__v=1357662840171" \
-d "audience__vs=consumer__vs" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534
'''

> Response

'''
{
"responseStatus": "SUCCESS",
"id": 534
}
'''

Update editable field values on the latest version of a single document. To update past document versions, see [Update Document Version](#Update_Document_Version). Note that this endpoint does not allow you to update the `archive__v` field. To archive a document, or to update multiple documents at once, see [Update Multiple Documents](#Update_Documents).

PUT `/api/{version}/objects/documents/{doc_id}`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

`X-VaultAPI-MigrationMode`

When set to `true`, Vault allows you to change the document number. All other Document Migration Mode overrides available at document creation are ignored, but do not generate an error message. You must have the _Document Migration_ permission to use this header. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

#### Body Parameters

In the body of the request, add any editable field values that you wish to update. To find these fields, [Retrieve Document Fields](#Retrieve_All_Document_Fields) configured on documents. Editable fields will have `editable:true`. To remove existing field values, include the field name and set its value to null.

### Update Multiple Documents

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"filename" \
https://myvault.veevavault.com/api/v25.2/objects/documents/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 771,
            "external_id__v": "ALT-DOC-0771"
        },
        {
            "responseStatus": "SUCCESS",
            "id": 772,
            "external_id__v": "CHO-DOC-0772"
        },
        {
            "responseStatus": "SUCCESS",
            "id": 773,
            "external_id__v": "GLU-DOC-0773"
        }
    ]
}
'''

Bulk update editable field values on multiple documents. You can only update the latest version of each document. To update past document versions, see [Update Document Version](#Update_Document_Version).

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 1,000.

PUT `/api/{version}/objects/documents/batch`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `text/csv`

`X-VaultAPI-MigrationMode`

When set to `true`, Vault allows you to change the document number. All other Document Migration Mode overrides available at document creation are ignored, but do not generate an error message. You must have the _Document Migration_ permission to use this header. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### Body Parameters

You can use Name-Value pairs in the body of your request or upload a CSV file. `id` is the only required field, and you can update values of any editable document field. To find these fields, [Retrieve Document Fields](#Retrieve_All_Document_Fields) configured on documents. Editable fields will have `editable:true`. To remove existing field values, include the field name and set its value to null.

The following table includes required fields, and some optional document fields you may want to update:

Name

Description

`id`conditional

The ID of the document to update. Only required when uploading a CSV file.

`docIds`conditional

Comma-separated list of the IDs of documents to update. Only required when entering key-value pairs in the body of your request.

`archive__v`optional

To archive a document, set to `true`. To unarchive a document, set to `false`. The default is `false`. Document archive is not available in all Vaults. [Learn more in Vault Help.](https://platform.veevavault.help/en/lr/34126)

`template_doctype__v`optional

If you need to create a controlled document template from this document, enter a value for the _Template Document Type_ field. To retrieve a list of all possible field values for this field, [Retrieve the Object Collection](#Retrieve_Object_Record_Collection) for `doc_type_detail__v`. Learn more about [controlled document template creation in Vault Help](https://platform.veevavault.help/en/lr/46025).

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-update-documents-sample-csv-input.csv)

### Reclassify Single Document

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "reclassify=true" \
-d "type__v=Promotional Piece" \
-d "subtype__v=Advertisement" \
-d "classification__v=Web" \
-d "lifecycle__v=Promotional Piece" \
https://myvault.veevavault.com/api/v25.2/objects/documents/775
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "id": 775
}
'''

Reclassify allows you to change the document type of an existing document or assign a document type to an unclassified document. This endpoint is analogous to the _Reclassify_ action in the Vault UI.

A document “type” is the combination of the `type__v`, `subtype__v`, and `classification__v` fields on a document. When you reclassify, Vault may add or remove certain fields on the document. Add these new fields and values to the body of this request. If a new required field is missing, the error response will list the name of the required field. To reclassify more than one document, use the [Reclassify Multiple Documents](#Reclassify_Multiple_Documents) endpoint.

Not all documents are eligible for reclassification. For example, you can only reclassify the latest version of a document and you cannot reclassify a checked out document. Learn more about [reclassifying documents in Vault Help](https://platform.veevavault.help/en/lr/2271).

PUT `/api/{version}/objects/documents/{doc_id}`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

`X-VaultAPI-MigrationMode`

When set to `true`, Vault allows you to manually set the document number and to update documents to any lifecycle state using the `status__v` field. All other Document Migration Mode overrides available at document creation are ignored, but do not generate an error message. You must have the _Document Migration_ permission to use this header. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

#### Body Parameters

You can also add or remove values for any other editable document field. Note that additional fields may be required depending on the document type, subtype, and classification being assigned to the document. Use the [Document Metadata API](#Retrieve_All_Document_Fields) to retrieve required and editable fields in your Vault. If a required field is missing, the error response will list the name of the required field.

Name

Description

`type__v`required

The name of the document type.

`subtype__v`optional

The name of the document subtype (if one exists on the type).

`classification__v`optional

The name of the document classification (if one exists on the subtype).

`lifecycle__v`required

The name of the document lifecycle.

`reclassify`required

Set to `true`. Without this, a standard document update action is performed.

`document_number__v`optional

The document number for the reclassified document. If omitted, the document retains the existing document number. You must set both the `reclassify` parameter and the `X-VaultAPI_MigrationMode` header to `true` to change the document number, and you can only include this parameter when you also change the document lifecycle or type, subtype, or classification.

`status__v`optional

Specifies the document lifecycle state for the reclassified document. If omitted, the document retains the existing state. You must set both the `reclassify` parameter and the `X-VaultAPI_MigrationMode` header to `true` to change the state, and you can only include this parameter when you also change the document lifecycle or type, subtype, or classification.

### Reclassify Multiple Documents

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Documents\reclassify_documents.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/batch/actions/reclassify
'''

> Response

'''
responseStatus,id,errors,warnings
SUCCESS,44,
SUCCESS,46,
'''

Reclassify documents in bulk. Reclassify allows you to change the document type of existing documents or assign document types to unclassified documents.

A document “type” is the combination of the `type__v`, `subtype__v`, and `classification__v` fields on a document. When you reclassify, Vault may add or remove certain fields on the document.

Not all documents are eligible for reclassification. For example, you can only reclassify the latest version of a document and you cannot reclassify a checked out document. Learn more about [reclassifying documents in Vault Help](https://platform.veevavault.help/en/lr/2271).

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

PUT `/api/{version}/objects/documents/batch/actions/reclassify`

#### Headers

Name

Description

`Content-Type`

`text/csv`

`Accept`

`application/json` (default) or `text/csv`

`X-VaultAPI-MigrationMode`

When set to `true`, Vault allows you to manually set the document number and to update documents to any lifecycle state using the `status__v` field. All other Document Migration Mode overrides available at document creation are ignored, but do not generate an error message. You must have the _Document Migration_ permission to use this header. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### Body Parameters

Upload parameters as a CSV file. You can also add or remove values for any other editable document field. Note that additional fields may be required depending on the document type, subtype, and classification being assigned to the document. Use the [Document Metadata API](#Retrieve_All_Document_Fields) to retrieve required and editable fields in your Vault. If a required field is missing, the error response will list the name of the required field.

Name

Description

`id`required

The ID of the document to reclassify.

`lifecycle__v`required

The name of the document lifecycle.

`type__v`required

The name of the document type.

`subtype__v`optional

The name of the document subtype (if one exists on the type).

`classification__v`optional

The name of the document classification (if one exists on the subtype).

`document_number__v`optional

The document number for the reclassified document. If omitted, the document retains the existing document number. You must set both the `reclassify` parameter and the `X-VaultAPI_MigrationMode` header to `true` to change the document number, and you can only include this parameter when you also change the document lifecycle or type, subtype, or classification.

`status__v`optional

Specifies the document lifecycle state for the reclassified document. If omitted, the document retains the existing state. You must set both the `reclassify` parameter and the `X-VaultAPI_MigrationMode` header to `true` to change the state, and you can only include this parameter when you also change the document lifecycle or type, subtype, or classification.

#### Response Details

On `SUCCESS`, Vault returns the IDs of the reclassified documents.

### Update Document Version

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "language__v=English" \
-d "product__v=1357662840171" \
-d "audience__c=consumer__c" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/0
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": 534
}
'''

Update editable field values on a specific version of a document. See also [Update Document](#Update_Document) above.

PUT `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

`X-VaultAPI-MigrationMode`

When set to `true`, Vault allows you to manually set the document number. All other Document Migration Mode overrides available at document creation are ignored, but do not generate an error message. You must have the _Document Migration_ permission to use this header. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

#### Response Details

On `SUCCESS`, Vault updates field values for the specified version of the document and returns the ID of the updated document.

### Create Multiple Document Versions

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"filename" \
https://myvault.veevavault.com/api/v25.2/objects/documents/versions/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 771,
            "external_id__v": "ALT-DOC-0771",
            "major_version_number__v": 0,
            "minor_version_number__v": 2
        },
        {
            "responseStatus": "SUCCESS",
            "id": 772,
            "external_id__v": "CHO-DOC-0772",
            "major_version_number__v": 0,
            "minor_version_number__v": 2
        },
        {
            "responseStatus": "SUCCESS",
            "id": 773,
            "external_id__v": "GLU-DOC-0773",
            "major_version_number__v": 1,
            "minor_version_number__v": 0
        },
        {
            "responseStatus": "FAILURE",
            "errors": [
                {
                    "type": "INVALID_DATA",
                    "message": "Error message describing why this document version was not added."
                }
            ]
        }
    ]
}
'''

Create or add document versions in bulk.

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

POST `/api/{version}/objects/documents/versions/batch`

#### Headers

Name

Description

`Content-Type`

`text/csv`

`Accept`

`application/json` (default) or `text/csv`

`X-VaultAPI-MigrationMode`

Must be set to `true`. Vault allows you to manually set the name and version number and to create documents in any lifecycle state using the `status__v` field, but does not allow you to change the document number. Vault also bypasses entry criteria, entry actions, and event actions. You must have the _Document Migration_ permission to use this header. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### Body Parameters

Name

Description

`file`required

The filepath of your source file. The maximum allowed file size is 500GB.

`id`conditional

The system-assigned document ID of the document to add the versions to. Not required if providing a unique field identifier (`idParam`) such as `external_id__v`.

`external_id__v`conditional

Instead of `id`, you can use this user-defined document external ID.

`name__v`required

Enter a name for the new document. This may be the same name as the existing document/version or a different name.

`type__v`required

Enter the name or label of the document type to assign to the new document.

`subtype__v`optional

Enter the name or label of the document subtype (if one exists on the document type).

`classification__v`optional

Enter the name or label of the document classification (if one exists on the document subtype).

`lifecycle__v`required

Enter the name or label of the document lifecycle to assign to the new document. This may be the same lifecycle as the existing document/version or a different lifecycle.

`major_version_number__v`required

Enter the major version number to assign to the new document version. This must be a version that does not yet exist on the document being updated.

`minor_version_number__v`required

Enter the minor version number to assign to the new document. This must be a version that does not yet exist on the document being updated.

`status__v`required

Enter the name or label of the status for the new document, e.g., Draft, In Review, Approved, etc.

`product__v`optional

Example: This is an example object reference field. To assign value for this field type, include either the document field name `product__v` or the document field name plus the name field on the object `product__v.name__v`.

#### Query Parameters

Name

Description

`idParam`

If you’re identifying documents in your input by a unique field, add `idParam={fieldname}` to the request endpoint. You can use any object field which has `unique` set to `true` in the object metadata, with the exception of picklists. For example, `idParam=external_id__v`.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-add-document-versions-sample-csv-input.csv)

**Note**: In PromoMats Vaults with Automated Claims Linking enabled, when a reference document is updated with the Create Multiple Document Versions API, the associated claim record is updated to reference the new version and remains in the approved state, and the reference is not removed.

### Create Single Document Version

> Request: Copy file from current version

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "createDraft=latestContent" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534
'''

> Request: Upload a new file & Suppress rendition

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=CholeCap-Presentation.pptx" \
-F "createDraft=uploadedContent" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534?suppressRendition=true
'''

> Request: Upload new version

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=CholeCap-Presentation.pptx" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "New draft successfully created.",
  "major_version_number__v": 0,
  "minor_version_number__v": 2
}
'''

> Response: Upload new version

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Document successfully checked in.",
  "errorCodes": null,
  "errorType": null
}
'''

Add a new draft version of an existing document. You can choose to either use the existing source file or a new source file. These actions increase the target document’s minor version number. This is analogous to using the _Create Draft_ action in the UI.

Not all documents are eligible for draft creation, however, this endpoint does support creating a new draft version of a checked-out document. [See below](#upload_new_version) for details. Learn more about [creating new draft versions in Vault Help](https://platform.veevavault.help/en/lr/1560).

POST `/api/{version}/objects/documents/{doc_id}`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

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

`createDraft`conditional

Choose one of the two available values:  
  
`latestContent`: Create a new draft version from the existing document in the Vault. This does not require uploading a file. This option is only available if both the source file and rendition are each 4 GB or less. This is analogous to the **Copy file from current version** option in the _Create Draft_ UI.  
  
`uploadedContent`: Create a new draft version by uploading the document source file. This requires uploading a new source file with an additional `file` body parameter. The maximum allowed file size is 4GB. This is analogous to the **Upload a new file** option in the _Create Draft_ UI.  
  
This parameter is only required to create a new draft version from an existing document or by uploading a source file. To create a new version for a placeholder document, you must omit this parameter.

`file`conditional

The filepath of the source document. This parameter is only required in the following scenarios:

-   If `createDraft=uploadedContent`, use this parameter to include the new document source file.
-   If your target document is a placeholder, use this parameter to upload a source file and create a new draft version of the document.
-   If your target document is currently checked out, use this parameter to upload a new version of the document source file.

`description__v`optional

Add a _Version Description_ for the new draft version. Other users may view this description in the document’s _Version History_. Maximum 1,500 characters.

#### Query Parameters

Name

Description

`suppressRendition`

Set to `true` to suppress automatic generation of the viewable rendition. If omitted, defaults to `false`.

##### Upload New Version

When _Enable Upload New Version_ is enabled by an Admin, you can upload a new version of a checked out document if you already have an updated version of the document source file available. This is analogous to using the _Upload New Version_ action in the UI. To achieve this, omit the `createDraft` parameter and include the `file` parameter when sending a request to this endpoint. If the document has not yet been checked out in the UI, you can send a request to [Create Document Lock](#Create_Document_Lock) to check it out. Learn more about [versioning documents in Vault Help](https://platform.veevavault.help/en/lr/162).

#### Response Details

On `SUCCESS`, Vault creates a new draft version and the response includes the document’s `major_version_number__v` and `minor_version_number__v`. When you create a new draft version, Vault automatically increments the minor version number.

When uploading a new version of a checked out document, on `SUCCESS`, Vault creates a new draft version and the response includes a message saying the document has been checked in on your behalf.

### Review Results
- **Location:** `veevavault/services/documents/update_service.py`
- **Functions:** `update_single_document`, `update_multiple_documents`, `reclassify_single_document`, `reclassify_multiple_documents`, `update_document_version`, `create_multiple_document_versions`, `create_single_document_version`
- **Updates Made:**
    - Corrected the `Content-Type` header and data format for `update_single_document`.
- **State:** Compliant with API documentation.

## Delete Documents

After deleting documents, the API allows you to retrieve their IDs for up to 30 days. The deleted files themselves are removed from the server and can only be retrieved by Vault Support. Note that you cannot delete checked out documents unless you have the _Power Delete_ permission. Learn more about Power Delete in [Vault Help](https://platform.veevavault.help/en/lr/3292).

### Delete Single Document

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": 534
}
'''

Delete all versions of a document, including all source files and viewable renditions.

DELETE `/api/{version}/objects/documents/{document_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`document_id`

The system-assigned document ID of the document to delete.

### Delete Multiple Documents

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Documents\delete_documents.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 771,
            "external_id__v": "ALT-DOC-0771"
        },
        {
            "responseStatus": "SUCCESS",
            "id": 772,
            "external_id__v": "CHO-DOC-0772"
        },
        {
            "responseStatus": "SUCCESS",
            "id": 773,
            "external_id__v": "GLU-DOC-0773"
        },
        {
            "responseStatus": "FAILURE",
            "errors": [
                {
                    "type": "INVALID_DATA",
                    "message": "Error message describing why this document was not deleted."
                }
            ]
        }
    ]
}
'''

Delete all versions of multiple documents, including all source files and viewable renditions.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

DELETE `/api/{version}/objects/documents/batch`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/json`

`Accept`

`application/json` (default) or `text/csv`

#### Body Parameters

Create a CSV or JSON input file. Choose one of the following two ways to identify documents for deletion:

Name

Description

`id`conditional

The system-assigned document ID of the document to delete. Not required if providing a unique field identifier (`idParam`) such as `external_id__v`.

`external_id__v`conditional

Instead of `id`, you can use this user-defined document external ID.

#### Query Parameters

Name

Description

`idParam`

If you’re identifying documents in your input by a unique field, add `idParam={fieldname}` to the request endpoint. You can use any object field which has `unique` set to `true` in the object metadata, with the exception of picklists. For example, `idParam=external_id__v`.

### Delete Single Document Version

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/0/2
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": 534
}
'''

Delete a specific version of a document, including the version’s source file and viewable rendition. Other versions of the document remain unchanged. See also [Delete Document](#Delete_Document).

DELETE `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `text/csv`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

### Delete Multiple Document Versions

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Documents\delete_document_versions.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/versions/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 771,
            "external_id__v": "ALT-DOC-0771",
            "major_version_number__v": 0,
            "minor_version_number__v": 2
        },
        {
            "responseStatus": "SUCCESS",
            "id": 772,
            "external_id__v": "CHO-DOC-0772",
            "major_version_number__v": 0,
            "minor_version_number__v": 2
        },
        {
            "responseStatus": "SUCCESS",
            "id": 773,
            "external_id__v": "GLU-DOC-0773",
            "major_version_number__v": 1,
            "minor_version_number__v": 0
        },
        {
            "responseStatus": "FAILURE",
            "errors": [
                {
                    "type": "INVALID_DATA",
                    "message": "Error message describing why this document version was not deleted."
                }
            ]
        }
    ]
}
'''

Delete a specific version of multiple documents, including the version’s source file and viewable rendition.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

DELETE `/api/{version}/objects/documents/versions/batch`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/json`

`Accept`

`application/json` (default) or `text/csv`

#### Body Parameters

Create a CSV or JSON input file.

Name

Description

`id`conditional

The system-assigned document ID of the document to delete. Not required if providing a unique field identifier (`idParam`) such as `external_id__v`.

`external_id__v`conditional

Instead of `id`, you can use this user-defined document external ID.

`major_version_number__v`required

Major version number of the document version to remove.

`minor_version_number__v`required

Minor version number of the document version to remove.

#### Query Parameters

Name

Description

`idParam`

If you’re identifying documents in your input by a unique field, add `idParam={fieldname}` to the request endpoint. You can use any object field which has `unique` set to `true` in the object metadata, with the exception of picklists. For example, `idParam=external_id__v`.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-delete-document-versions-sample-csv-input.csv)

### Retrieve Deleted Document IDs

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/deletions/documents
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": "OK",
   "responseDetails": {
       "total": 3,
       "size": 3,
       "limit": 1000,
       "offset": 0
   },
   "data": [
       {
           "id": 23,
           "major_version_number__v": 0,
           "minor_version_number__v": 1,
           "date_deleted": "2021-02-26T23:46:49Z",
           "global_id__sys": "10000760_23",
           "global_version_id__sys": "10000760_23_39",
           "external_id__v": null,
           "deletion_type": "version_change__sys"
       },
       {
           "id": 7,
           "major_version_number__v": 0,
           "minor_version_number__v": 16,
           "date_deleted": "2021-02-26T23:55:22Z",
           "global_id__sys": "10000760_7",
           "global_version_id__sys": "10000760_7_22",
           "external_id__v": null,
           "deletion_type": "document_version__sys"
       },
       {
           "id": 10,
           "major_version_number__v": "",
           "minor_version_number__v": "",
           "date_deleted": "2021-02-26T23:55:45Z",
           "global_id__sys": "10000760_10",
           "global_version_id__sys": null,
           "external_id__v": null,
           "deletion_type": "document__sys"
       }
   ]
}
'''

Retrieve IDs of documents deleted within the past 30 days.

After documents and document versions are deleted, their IDs remain available for retrieval for 30 days. After that, they cannot be retrieved. This request supports optional parameters to narrow the results to a specific date and time range within the past 30 days.

To completely restore a document deleted within the last 30 days, contact Veeva support.

GET `/api/{version}/objects/deletions/documents`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml` or `text/csv`

#### Query Parameters

You can modify the request by using one or both of the following parameters:

Name

Description

`start_date`

Specify a date (no more than 30 days past) after which Vault will look for deleted documents. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2016 would use `2016-01-15T07:00:00Z`

`end_date`

Specify a date (no more than 30 days past) before which Vault will look for deleted documents. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2016 would use `2016-01-15T07:00:00Z`

Dates and times are in UTC. If the time is not specified, it will default to midnight (T00:00:00Z) on the specified date.

#### Response Details

Name

Description

`total`

The total number of deleted documents and document versions.

`id`

The ID of the deleted document or version. If the same document has multiple deleted versions, the same ID may appear twice.

`major_version_number__v`

The major version of the deleted version. If all versions of the document were deleted (for example, using the _Delete_ user action in the Vault UI), this value is blank (`""`).

`minor_version_number__v`

The minor version of the deleted version. If all versions of the document were deleted (for example, using the _Delete_ user action in the Vault UI), this value is blank (`""`).

`date_deleted`

The date and time this document or version was deleted.

`global_id__sys`

The global ID of the deleted document or version.

`global_version_id__sys`

The global version ID of the deleted document or version. If all versions of the document were deleted (for example, using the _Delete_ user action in the Vault UI), this value is `null`.

`external_id__v`

The external ID of the deleted document or version. May be `null` if no external ID was set for this document.

`deletion_type`

Describes how this document or version was deleted.

-   `document__sys`: this document was deleted in full, including all versions. For example, this document was deleted with the _Delete_ user action in the Vault UI.
-   `document_version__sys`: this document version was deleted. For example, this document version was deleted with [Delete Single Document Version](#Delete_Document_Version) API.
-   `version_change__sys`: this document version no longer exists, as it became a new major version through the _Set new major version_ entry action.

### Review Results
- **Location:** `veevavault/services/documents/deletion_service.py`
- **Functions:** `delete_single_document`, `delete_multiple_documents`, `delete_single_document_version`, `delete_multiple_document_versions`, `retrieve_deleted_document_ids`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Document Locks

A document “lock” is analogous to “checking out a document” but without the file attached in the response for download. To download the document file after locking it, use the [Download Document File](#Download_Document_File) endpoint.

Learn about [Document Checkout (Locks)](https://platform.veevavault.help/en/lr/162) in Vault Help.

### Retrieve Document Lock Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/lock
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "name": "lock",
    "properties": [
        {
            "name": "locked_by__v",
            "scope": "Lock",
            "type": "ObjectReference",
            "required": true,
            "systemAttribute": true,
            "editable": false,
            "setOnCreateOnly": false,
            "disabled": false,
            "objectType": "User",
            "label": "Locked By",
            "hidden": false
        },
        {
            "name": "locked_date__v",
            "scope": "Lock",
            "type": "DateTime",
            "required": true,
            "systemAttribute": true,
            "editable": false,
            "setOnCreateOnly": false,
            "disabled": false,
            "objectType": "DateTime",
            "label": "Locked Date",
            "hidden": false
        }
    ]
}
'''

GET `/api/{version}/metadata/objects/documents/lock`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

Metadata Field

Description

`name`

The “name” of the field used in the API. These include `locked_by__v`, `locked_date__v`, etc.

`label`

The “label” of the field used in the UI. These include “Locked By”, “Locked Date”, etc.

`type`

The “type” of field. These include “ObjectReference”, “DateTime”, etc.

`scope`

The “scope” of the field. This value is “Lock” for all fields.

`required`

Indicates if the field is required.

`systemAttribute`

Boolean (true/false) field which indicates if the field is a standard (system-managed) field, i.e., not editable by the user.

`editable`

Boolean (true/false) field which indicates if the field can be set or changed by the user, i.e., not system-managed.

`setOnCreateOnly`

Boolean (true/false) field which indicates if the field can only be set during creation of a new document.

`objectType`

When the field `type` is “ObjectReference”, this field indicates the object which is being referenced.

### Create Document Lock

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/lock
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Document successfully checked out."
}
'''

A document lock is analogous to checking out a document but without the file attached in the response for download.

POST `/api/{version}/objects/documents/{doc_id}/lock`

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

On `SUCCESS`, Vault locks the document and other users are not allowed to lock (check-out) the document.

### Retrieve Document Lock

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/lock
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "lock": {
        "locked_by__v": 46916,
        "locked_date__v": "2015-03-20T23:47:11.000Z"
    }
}
'''

GET `/api/{version}/objects/documents/{doc_id}/lock`

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

If the document is locked (checked out), the response includes the user `id` field value of the person who checked it out and the date and time. If the document is not locked, the lock fields shown above will not be returned.

### Delete Document Lock

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/lock
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Undo check out successful."
}
'''

Deleting a document lock is analogous to undoing check out of a document. The authenticated user must have _Edit Document_ permission in the document lifecycle state security settings as well as one of the following:

-   _Document Owner_ role on the document
-   _All Documents: All Document Actions_ permission
-   _Document: Cancel Checkout_ permission

DELETE `/api/{version}/objects/documents/{doc_id}/lock`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

#### Response Details

On `SUCCESS`, Vault unlocks the document, allowing other users to lock/check out the document.

### Undo Collaborative Authoring Checkout

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: application/json" \
--data "id
7652
3
8" \
https://myvault.veevavault.com/api/v25.2/objects/documents/batch/lock
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "responseStatus": "EXCEPTION",
           "responseMessage": "Document not found 19523/7652",
           "id": 7652
       },
       {
           "responseStatus": "FAILURE",
           "responseMessage": "Cannot use office365__sys undo check out for a document checked out to basic__sys",
           "id": 3
       },
       {
           "responseStatus": "SUCCESS",
           "responseMessage": "Undo check out successful",
           "id": 8
       }
   ]
}
'''

Undo Collaborative Authoring checkout on up to 500 documents at once. Learn more about [Collaborative Authoring in Vault Help](https://platform.veevavault.help/en/lr/56842).

To undo basic checkout, see [Delete Document Lock](#Delete_Document_Lock).

DELETE `/api/{version}/objects/documents/batch/lock`

#### Headers

Name

Description

`Accept`

`application/json` or `text/csv`

`Content-Type`

`text/csv`

#### Body Parameters

Upload parameters as a CSV file.

Name

Description

`id`required

The `id` of the document to undo checkout. Maximum 500 documents per request.

#### Response Details

On `SUCCESS`, Vault returns a `responseStatus` and `responseMessage` for each `id` in the request body. Partial success is allowed, meaning some documents in the batch may succeed while others fail. For any failed documents, the response includes a reason for the failure.

### Review Results
- **Location:** `veevavault/services/documents/locks_service.py`
- **Functions:** `retrieve_document_lock_metadata`, `create_document_lock`, `retrieve_document_lock`, `delete_document_lock`, `undo_collaborative_authoring_checkout`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Document Renditions

Learn about [Document Renditions](https://platform.veevavault.help/en/lr/1403) in Vault Help.

Note that requests to retrieve renditions might return an `UNEXPECTED_ERROR`. If this occurs, retry the request after a few seconds.

### Retrieve Document Renditions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "renditionTypes": [
        "viewable_rendition__v",
        "imported_rendition__c",
        "veeva_distribution_package__c"
    ],
    "renditions": {
        "viewable_rendition__v": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions/viewable_rendition__v",
        "veeva_distribution_package__c": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions/veeva_distribution_package__c"
    }
}
'''

GET `/api/{version}/objects/documents/{doc_id}/renditions`

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

Metadata Field

Description

`renditionTypes[n]`

List of all rendition types configured for the specified document.

`renditions[n]`

List of renditions available for the specified document and the endpoint URL to retrieve them.

### Retrieve Document Version Renditions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/0/renditions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "renditionTypes": [
        "viewable_rendition__v",
        "imported_rendition__c",
        "veeva_distribution_package__c"
    ],
    "renditions": {
        "viewable_rendition__v": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/0/renditions/viewable_rendition__v",
        "veeva_distribution_package__c": "https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/0/renditions/veeva_distribution_package__c"
    }
}
'''

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/renditions`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

### Download Document Rendition File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions/viewable_rendition__v > file
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Download a rendition file from the latest version of a document.

GET `/api/{version}/objects/documents/{doc_id}/renditions/{rendition_type}`

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

`{rendition_type}`

The document rendition type.

#### Query Parameters

Name

Description

`steadyState`

Set to `true` to download a rendition (file) from the latest steady state version (1.0, 2.0, etc.) of a document.

`protectedRendition`

If your Vault is configured to use protected renditions, set to `false` to download the non-protected rendition. If omitted, defaults to `true`. You must have the _Download Non-Protected Rendition_ permission to download non-protected renditions.

#### Response Details

On `SUCCESS`, Vault retrieves the file associated with the given renditions type for the document. The HTTP Response Header `Content-Type` is set to `application/octet-stream`.

### Download Document Version Rendition File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/0/renditions/viewable_rendition__v > file
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Download a rendition for a specified version of a document.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/renditions/{rendition_type}`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

`{rendition_type}`

The document rendition type.

#### Query Parameters

Name

Description

`protectedRendition`

If your Vault is configured to use protected renditions, set to `false` to download the non-protected rendition. If omitted, defaults to `true`. You must have the _Download Non-Protected Rendition_ permission to download non-protected renditions.

#### Response Details

On `SUCCESS`, Vault retrieves the file associated with the given renditions type for the specified document version. The HTTP Response Header `Content-Type` is set to `application/octet-stream`.

### Add Multiple Document Renditions

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"filename" \
https://myvault.veevavault.com/api/v25.2/objects/documents/renditions/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 771,
            "external_id__v": "ALT-DOC-0771",
            "major_version_number__v": 0,
            "minor_version_number__v": 2,
            "rendition_type__c": "imported_rendition__c"
        },
        {
            "responseStatus": "SUCCESS",
            "id": 772,
            "external_id__v": "CHO-DOC-0772",
            "major_version_number__v": 0,
            "minor_version_number__v": 2,
            "rendition_type__c": "imported_rendition__c"
        },
        {
            "responseStatus": "SUCCESS",
            "id": 773,
            "external_id__v": "GLU-DOC-0773",
            "major_version_number__v": 1,
            "minor_version_number__v": 0,
            "rendition_type__c": "imported_rendition__c"
        },
        {
            "responseStatus": "FAILURE",
            "errors": [
                {
                    "type": "INVALID_DATA",
                    "message": "Error message describing why this document rendition was not added."
                }
            ]
        }
    ]
}
'''

Add document renditions in bulk. You must first load the renditions to [file staging](/docs/#FTP).

-   If the `largeSizeAsset` query parameter is not set to `true`, you must include the `X-VaultAPI-MigrationMode` header.
-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

POST `/api/{version}/objects/documents/renditions/batch`

#### Headers

Name

Description

`Content-Type`

`text/csv`

`Accept`

`application/json` (default) or `text/csv`

`X-VaultAPI-MigrationMode`

Must be set to `true` when importing any rendition type other than `large_size_asset__v`. You must have the _Document Migration_ permission to use this header. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### Body Parameters

Name

Description

`file`required

The filepath of the rendition on file staging.

`id`conditional

The system-assigned document ID of the document to add renditions to. Not required if providing a unique field identifier (`idParam`) such as `external_id__v`.

`external_id__v`conditional

Instead of `id`, you can use this user-defined document external ID.

`rendition_type__v`required

Document rendition type to assign to the new rendition. Only one rendition of each type may exist on each document.

`major_version_number__v`required

Major version number to assign to the new document rendition.

`minor_version_number__v`required

Minor version number to assign to the new document rendition.

#### Query Parameters

Name

Description

`idParam`

If you’re identifying documents in your input by a unique field, add `idParam={fieldname}` to the request endpoint. You can use any object field which has `unique` set to `true` in the object metadata, with the exception of picklists. For example, `idParam=external_id__v`.

`largeSizeAsset`

If set to `true`, indicates that the renditions to add are of the Large Size Asset (`large_size_asset__v`) rendition type. Vault applies [Document Migration Mode](https://platform.veevavault.help/en/lr/54028) limitations to renditions created with the request, but _Document Migration_ permission is not required and your Vault need not be in Migration Mode to use the parameter. Note that the request results in an error if the CSV contains any rendition type other than `large_size_asset__v`.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-add-document-renditions-sample-csv-input.csv)

### Add Single Document Rendition

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=CholeCap-Document.pdf" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions/imported_rendition__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

POST `/api/{version}/objects/documents/{doc_id}/renditions/{rendition_type}`

#### Headers

Name

Description

`Content-Type`

`application/json` or `multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

`{rendition_type}`

The document rendition type.

#### File Upload

To upload the file, use the multi-part attachment with the file component `"file={file_name}"`. The maximum allowed file size is 4GB.

#### Response Details

On `SUCCESS`, Vault associates the uploaded file with the given rendition type for the specified document.

### Upload Document Version Rendition

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=CholeCap-Document.pdf" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions/imported_rendition__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

POST `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/renditions/{rendition_type}`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

`{rendition_type}`

The document rendition type.

#### File Upload

To upload the file, use the multi-part attachment with the file component `"file={file_name}"`. The maximum allowed file size is 4GB.

#### Response Details

On `SUCCESS`, Vault associates the uploaded file with the given rendition type for the document with the specified version number.

### Update Multiple Document Renditions

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Documents\update_document_renditions.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/batch/actions/rerender
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 1,
            "major_version_number__v": "0",
            "minor_version_number__v": "1"
        },
        {
            "responseStatus": "SUCCESS",
            "id": 2,
            "major_version_number__v": "0",
            "minor_version_number__v": "1"
        }
    ]
}
'''

Update or re-render document renditions in bulk.

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

POST `/api/{version}/objects/documents/batch/actions/rerender`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `text/csv`

#### Body Parameters

Upload parameters as a CSV file.

Name

Description

`id`required

The system-assigned ID of the document.

`major_version_number__v`required

The major version number of the existing document.

`minor_version_number__v`required

The minor version number of the existing document.

#### Response Details

On `SUCCESS`, Vault returns whether each document rendition was successfully re-rendered.

### Replace Document Rendition

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=CholeCap-Document.pdf" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions/imported_rendition__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

PUT `/api/{version}/objects/documents/{doc_id}/renditions/{rendition_type}`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

`{rendition_type}`

The document rendition type.

#### File Upload

To upload the file, use the multi-part attachment with the file component `"file={file_name}"`. The maximum allowed file size is 4GB.

#### Response Details

On `SUCCESS`, Vault replaces the rendition of the given type from the latest version of the document.

### Replace Document Version Rendition

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=CholeCap-Document.pdf" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/0/renditions/imported_rendition__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

PUT `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/renditions/{rendition_type}`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

`{rendition_type}`

The document rendition type.

#### File Upload

To upload the file, use the multi-part attachment with the file component `"file={file_name}"`. The maximum allowed file size is 4GB.

#### Response Details

On `SUCCESS`, Vault replaces the rendition of the given type for the specified version of the document.

### Delete Multiple Document Renditions

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Documents\delete_document_renditions.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/renditions/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 771,
            "external_id__v": "ALT-DOC-0771",
            "major_version_number__v": 0,
            "minor_version_number__v": 2,
            "rendition_type__c": "imported_rendition__c"
        },
        {
            "responseStatus": "SUCCESS",
            "id": 772,
            "external_id__v": "CHO-DOC-0772",
            "major_version_number__v": 0,
            "minor_version_number__v": 2,
            "rendition_type__c": "imported_rendition__c"
        },
        {
            "responseStatus": "SUCCESS",
            "id": 773,
            "external_id__v": "GLU-DOC-0773",
            "major_version_number__v": 1,
            "minor_version_number__v": 0,
            "rendition_type__c": "imported_rendition__c"
        },
        {
            "responseStatus": "FAILURE",
            "errors": [
                {
                    "type": "INVALID_DATA",
                    "message": "Error message describing why this document rendition was not added."
                }
            ]
        }
    ]
}
'''

Delete document renditions in bulk.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

DELETE `/api/{version}/objects/documents/renditions/batch`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/json`

`Accept`

`application/json` (default) or `text/csv`

#### Body Parameters

Create a CSV or JSON input file.

Name

Description

`id`conditional

The system-assigned document ID of the document to delete. Not required if providing a unique field identifier (`idParam`) such as `external_id__v`.

`external_id__v`conditional

Instead of `id`, you can use this user-defined document external ID.

`rendition_type__v`required

Rendition type to delete from the document.

`major_version_number__v`required

Major version number of the document rendition to remove.

`minor_version_number__v`required

Minor version number of the document rendition to remove.

#### Query Parameters

Name

Description

`idParam`

If you’re identifying documents in your input by a unique field, add `idParam={fieldname}` to the request endpoint. You can use any object field which has `unique` set to `true` in the object metadata, with the exception of picklists. For example, `idParam=external_id__v`.

### Delete Single Document Rendition

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/renditions/imported_rendition__vs
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Delete a single document rendition. On `SUCCESS`, Vault deletes the rendition of specified type from the latest document version.

DELETE `/api/{version}/objects/documents/{document_id}/renditions/{rendition_type}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{document_id}` - The document `id` field value.

`{rendition_type}` - The document rendition type.

### Delete Document Version Rendition

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/0/renditions/imported_rendition__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

DELETE `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/renditions/{rendition_type}`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

`{rendition_type}`

The document rendition type.

On `SUCCESS`, Vault deletes the rendition of the given type from the specified version of the document.

### Review Results
- **Location:** `veevavault/services/documents/renditions_service.py`
- **Functions:** `retrieve_document_renditions`, `retrieve_document_version_renditions`, `download_document_rendition_file`, `download_document_version_rendition_file`, `add_multiple_document_renditions`, `add_single_document_rendition`, `upload_document_version_rendition`, `update_multiple_document_renditions`, `replace_document_rendition`, `replace_document_version_rendition`, `delete_multiple_document_renditions`, `delete_single_document_rendition`, `delete_document_version_rendition`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Document Attachments

Learn about [Document Attachments](https://platform.veevavault.help/en/lr/24287) in Vault Help.

### Review Results
- **Location:** `veevavault/services/documents/attachments_service.py`
- **Functions:** `determine_if_document_has_attachments`, `retrieve_document_attachments`, `retrieve_document_version_attachments`, `retrieve_document_attachment_versions`, `retrieve_document_version_attachment_versions`, `retrieve_document_version_attachment_version_metadata`, `retrieve_document_attachment_metadata`, `retrieve_document_attachment_version_metadata`, `retrieve_deleted_document_attachments`, `download_document_attachment`, `download_document_attachment_version`, `download_document_version_attachment_version`, `download_all_document_attachments`, `download_all_document_version_attachments`, `delete_single_document_attachment`, `delete_single_document_attachment_version`, `delete_multiple_document_attachments`, `create_document_attachment`, `create_multiple_document_attachments`, `restore_document_attachment_version`, `update_document_attachment_description`, `update_multiple_document_attachment_descriptions`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Determine if a Document has Attachments

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565
'''

> Response

'''
{
    "attachments": [
        {
            "id": 566,
            "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566"
        },
        {
            "id": 567,
            "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/567"
        }
    ]
}
'''

GET `/api/{version}/objects/documents/{doc_id}`

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

Shown above, document `id` 565 has two different attachments: `id` 566 and `id` 567. Note that this endpoint does not retrieve the number of versions of each attachment nor the attachment metadata. The “attachments” attribute is displayed in the response for documents in which attachments have been enabled on the document type (even if the document has no attachments).

### Retrieve Document Attachments

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "id": 566,
            "filename__v": "Site Area Map.png",
            "format__v": "image/png",
            "size__v": 109828,
            "md5checksum__v": "78b36d9602530e12051429e62558d581",
            "version__v": 2,
            "created_by__v": 46916,
            "created_date__v": "2015-01-14T00:35:01.775Z",
            "versions": [
                {
                    "version__v": 1,
                    "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/1"
                },
                {
                    "version__v": 2,
                    "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/2"
                }
            ]
        },
        {
            "id": 567,
            "filename__v": "Site Facilities Contacts.docx",
            "format__v": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "size__v": 11483,
            "md5checksum__v": "bddd2e18f40dd09ab4939ddd2acefeac",
            "version__v": 3,
            "created_by__v": 46916,
            "created_date__v": "2015-01-14T00:35:12.320Z",
            "versions": [
                {
                    "version__v": 1,
                    "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/567/versions/1"
                },
                {
                    "version__v": 2,
                    "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/567/versions/2"
                },
                {
                    "version__v": 3,
                    "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/567/versions/3"
                }
            ]
        }
    ]
}
'''

GET `/api/{version}/objects/documents/{doc_id}/attachments`

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

Shown above, document `id` 565 has two different attachments. Attachment `id` 566 is an image file with two versions. Attachment `id` 567 is a Word™ document with three versions. Unlike “regular” document versioning, attachment versioning uses integer numbers beginning with 1 and incrementing sequentially (1, 2, 3,…). There is no concept of major or minor version numbers with attachments.

### Retrieve Document Version Attachments

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/attachments
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "id": 39,
            "filename__v": "New",
            "format__v": "application/x-tika-ooxml",
            "size__v": 55762,
            "md5checksum__v": "c5e7eaafc39af8ba42081a213a68f781",
            "version__v": 1,
            "created_by__v": 61603,
            "created_date__v": "2017-10-30T17:03:29.878Z",
            "versions": [
                {
                    "version__v": 1,
                    "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/attachments/39/versions/1"
                }
            ]
        }
    ]
}
'''

Retrieve attachments on a specific version of a document.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/attachments`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

### Retrieve Document Attachment Versions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "version__v": 1,
            "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/1"
        },
        {
            "version__v": 2,
            "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/2"
        }
    ]
}
'''

GET `/api/{version}/objects/documents/{doc_id}/attachments/{attachment_id}/versions`

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

`{attachment_id}`

The attachment `id` field value.

#### Response Details

Unlike documents, attachment versions use integer values starting with version 1 and incrementing sequentially (2, 3, 4,…). Attachments do not use major or minor version numbers.

### Retrieve Document Version Attachment Versions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/attachments/39/versions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "version__v": 1,
            "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/attachments/2901/versions/1"
        }
    ]
}
'''

Retrieve all versions of an attachment on a specific document version.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/attachments/{attachment_id}/versions`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

`{attachment_id}`

The `id` of the document attachment to retrieve.

#### Response Details

On `SUCCESS`, the response lists the attachment versions on the specified document version along with the `url` to retrieve the metadata for each attachment version.

### Retrieve Document Version Attachment Version Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/attachments/39/versions/1
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "id": 39,
            "filename__v": "New",
            "format__v": "application/x-tika-ooxml",
            "size__v": 55762,
            "md5checksum__v": "c5e7eaafc39af8ba42081a213a68f781",
            "version__v": 1,
            "created_by__v": 61603,
            "created_date__v": "2017-10-30T17:03:29.878Z"
        }
    ]
}
'''

Retrieve a specific version of an attachment on a document version.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/attachments/{attachment_id}/versions/{attachment_version}`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

`{attachment_id}`

The `id` of the document attachment to retrieve.

`{attachment_version}`

Optional: The version of the attachment to retrieve. If omitted, the endpoint retrieves all versions of the specified attachment.

#### Response Details

On `SUCCESS`, the response contains the following metadata for the specified attachment version on the document version:

Field Name

Description

`id`

ID of the attachment. This is set by the system.

`version__v`

Version of the attachment. Attachment versioning uses integer numbers beginning with 1 and incrementing sequentially (1, 2, 3,…). There is no concept of major or minor version numbers with attachments.

`filename__v`

File name of the attachment.

`description__v`

Optional description added to the attachment. The response excludes this attribute if the attachment has no description.

`format__v`

File format of the attachment.

`size__v`

File size of the attachment.

`md5checksum__v`

MD5 checksum value calculated for the attachment. To avoid creating identical versions, Vault assigns each a checksum value.

`version__v`

Version of the attachment. Attachment versioning uses integer numbers beginning with 1 and incrementing sequentially (1, 2, 3,…). There is no concept of major or minor version numbers with attachments.

`created_by__v`

User ID of the person who created the attachment.

`created_date__v`

Date the attachment was created.

### Retrieve Document Attachment Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "id": 566,
            "filename__v": "Site Area Map.png",
            "format__v": "image/png",
            "size__v": 109828,
            "md5checksum__v": "78b36d9602530e12051429e62558d581",
            "version__v": 2,
            "created_by__v": 46916,
            "created_date__v": "2015-01-14T00:35:01.775Z",
            "versions": [
                {
                    "version__v": 1,
                    "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/1"
                },
                {
                    "version__v": 2,
                    "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/2"
                }
            ]
        }
    ]
}
'''

GET `/api/{version}/objects/documents/{doc_id}/attachments/{attachment_id}`

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

`{attachment_id}`

The attachment `id` field value.

#### Response Details

The `md5checksum__v` field is calculated on the latest version of the attachment. If an attachment is added which has the same MD5 checksum value as an existing attachment on a given document, the new attachment is not added.

Vault Document Attachments include the following fields (metadata):

Field Name

Description

`id`

ID of the attachment. This is set by the system.

`version__v`

Version of the attachment. Attachment versioning uses integer numbers beginning with 1 and incrementing sequentially (1, 2, 3,…). There is no concept of major or minor version numbers with attachments.

`filename__v`

File name of the attachment.

`description__v`

Optional description added to the attachment. You can add descriptions up to 1000 characters in length.

`format__v`

File format of the attachment. You can add any type of file as an attachment.

`size__v`

File size of the attachment. You can add up to 50 attachments to a document; each must be under 2GB.

`md5checksum__v`

MD5 checksum value calculated for the attachment. To avoid creating identical versions, Vault assigns each a checksum value. When you add an attachment with the same file name and checksum value, Vault ignores the new file and does not version the existing attachment.

`created_by__v`

User ID of the person who created the attachment.

`created_date__v`

Date the attachment was created.

`versions[n]`

List of links to earlier versions of the attachment.

### Retrieve Document Attachment Version Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/2
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "id": 566,
            "filename__v": "Site Area Map.png",
            "format__v": "image/png",
            "size__v": 109828,
            "md5checksum__v": "78b36d9602530e12051429e62558d581",
            "version__v": 2,
            "created_by__v": 46916,
            "created_date__v": "2015-01-14T00:35:01.775Z"
        }
    ]
}
'''

GET `/api/{version}/objects/documents/{doc_id}/attachments/{attachment_id}/versions/{attachment_version}`

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

`{attachment_id}`

The attachment `id` field value.

`{attachment_version}`

The attachment `version__v` field value.

### Retrieve Deleted Document Attachments

> Request

'''
curl --location 'https://myvault.veevavault.com/api/v25.2/objects/deletions/documents/attachments' \
--header 'Accept: application/json' \
--header 'Authorization: {SESSION_ID}' \
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": "OK",
   "responseDetails": {
       "total": 2,
       "size": 2,
       "limit": 1000,
       "offset": 0
   },
   "data": [
       {
           "id": 301,
           "version": "",
           "date_deleted": "2025-05-17T01:54:27Z",
           "external_id__v": null,
           "global_id__sys": "19523_148",
           "global_version_id__sys": null,
           "deletion_type": "attachment__sys"
       },
       {
           "id": 302,
           "version": "",
           "date_deleted": "2025-05-17T01:54:31Z",
           "external_id__v": null,
           "global_id__sys": "19523_148",
           "global_version_id__sys": null,
           "deletion_type": "attachment__sys"
       }
   ]
}
'''

Retrieve IDs of document attachments deleted within the past 30 days. Learn more about [document attachments in Vault Help](https://platform.veevavault.help/en/lr/58613).

After document attachments and attachment versions are deleted, their IDs remain available for retrieval for 30 days. After that, they cannot be retrieved.

GET `/api/{version}/objects/deletions/documents/attachments`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`start_date`

Specify a date (no more than 30 days past) after which Vault will look for deleted document attachments. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2016 would use `2016-01-15T07:00:00Z`. Dates and times are in UTC. If the time is not specified, it will default to midnight (T00:00:00Z) on the specified date.

`end_date`

Specify a date (no more than 30 days past) before which Vault will look for deleted document attachments. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2016 would use `2016-01-15T07:00:00Z`. Dates and times are in UTC. If the time is not specified, it will default to midnight (T00:00:00Z) on the specified date.

`limit`

Paginate the results by specifying the maximum number of deleted attachments to display per page in the response. This can be any value between `0` and `5000`. If omitted, defaults to `1000`.

#### Response Details

Name

Description

`total`

The total number of deleted document attachments or attachment versions.

`id`

The ID of this deleted document attachment or attachment version.

`version`

The version of this deleted document attachment. If all versions of the attachment were deleted, this value is blank (`""`). Unlike documents, document attachments do not have minor versions. Learn more about [attachment versioning in Vault Help](https://platform.veevavault.help/en/lr/58613/#versioning).

`date_deleted`

The date and time this document attachment or attachment version was deleted.

`external_id__v`

The external ID of this deleted document attachment or attachment version. May be `null` if no external ID was set for this document attachment.

`global_id__sys`

The global ID of this deleted document attachment or attachment version.

`global_version_id__sys`

The global version ID of this deleted document attachment or attachment version. If all versions of the document were deleted, this value is `null`.

`deletion_type`

Describes how this document attachment or attachment version was deleted.

-   `attachment__sys`: this document attachment was deleted in full, including all versions. For example, this document attachment was deleted with the Delete user action in the Vault UI, or with Vault API.
-   `attachment_version__sys`: this document attachment version was deleted. For example, this document attachment version was deleted with the [Delete Single Document Attachment Version](#Delete_Document_Attachment_Version) API.

### Download Document Attachment

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/567/file
'''

> Response

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment;filename="file.pdf"
'''

Downloads the latest version of the specified attachment from the document.

GET `/api/{version}/objects/documents/{doc_id}/attachments/{attachment_id}/file`

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

`{attachment_id}`

The attachment `id` field value.

#### Response Details

On `SUCCESS`, Vault retrieves the latest version of the attachment from the document. The file name is the same as the attachment file name.

The HTTP Response Header `Content-Type` is set to the MIME type of the file. For example, if the attachment is a PNG image, the `Content-Type`is image/png. If we cannot detect the MIME file type, Content-Type is set to application/octet-stream. The HTTP Response Header `Content-Disposition` contains a filename attribute which can be used when naming the local file. When retrieving attachments with very small file size, the HTTP Response Header `Content-Length` is set to the size of the attachment. Note that for most attachment downloads (larger file sizes), the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Download Document Attachment Version

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/567/versions/1/file
'''

> Response

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment;filename="file.pdf"
'''

Downloads the specified version of the attachment from the document.

GET `/api/{version}/objects/documents/{doc_id}/attachments/{attachment_id}/versions/{attachment_version}/file`

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

`{attachment_id}`

The attachment `id` field value.

`{attachment_version}`

The attachment `version__v` field value.

#### Response Details

On `SUCCESS`, Vault retrieves the specified version of the attachment from the document. The file name is the same as the attachment file name.

The HTTP Response Header Content-Type is set to the MIME type of the file. For example, if the attachment is a PNG image, the Content-Type is image/png. If we cannot detect the MIME file type, Content-Type is set to application/octet-stream. The HTTP Response Header `Content-Disposition` contains a filename attribute which can be used when naming the local file. When downloading attachments with very small file size, the HTTP Response Header `Content-Length` is set to the size of the attachment. Note that for most attachment downloads (larger file sizes), the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Download Document Version Attachment Version

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/56/versions/0/1/attachments/14/versions/3/file
'''

> Response

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment;filename="file.pdf"
'''

Downloads the specified attachment version from the specified document version.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/attachments/{attachment_id}/versions/{attachment_version}/file`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

`{attachment_id}`

The `id` field value of the attachment.

`{attachment_version}`

The version of the attachment.

#### Response Details

On `SUCCESS`, Vault retrieves the specified attachment version from the specified document version. The file name is the same as the attachment file name.

The HTTP Response Header `Content-Type` is set to the MIME type of the file. For example, if the attachment is a PNG image, the `Content-Type`is image/png. If we cannot detect the MIME file type, Content-Type is set to application/octet-stream. The HTTP Response Header `Content-Disposition` contains a filename attribute which can be used when naming the local file. When retrieving attachments with very small file size, the HTTP Response Header `Content-Length` is set to the size of the attachment. Note that for most attachment downloads (larger file sizes), the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Download All Document Attachments

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/file
'''

> Response

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment;filename="Document VV-02839 (v0.1) - attachments.zip"
'''

Downloads the latest version of all attachments from the document.

GET `/api/{version}/objects/documents/{doc_id}/attachments/file`

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

On `SUCCESS`, Vault retrieves the latest version of all attachments from the document. The attachments are packaged in a ZIP file with the file name: Document {document number} (v. {major version}.{minor version}) - attachments.zip.

The HTTP Response Header Content-Type is set to `application/zip`. The HTTP Response Header `Content-Disposition` contains a filename attribute which can be used when naming the local file. When downloading attachments with very small file size, the HTTP Response Header `Content-Length` is set to the size of the attachment. Note that for most attachment downloads (larger file sizes), the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Download All Document Version Attachments

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/56/versions/0/1/attachments/file
'''

> Response

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment;filename="file.pdf"
'''

Downloads the latest version of all attachments from the specified version of the document.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/attachments/file`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

#### Response Details

On `SUCCESS`, Vault retrieves the latest version of all attachments from the specified version of the document. The file name is the same as the attachment file name.

The HTTP Response Header `Content-Type` is set to the MIME type of the file. For example, if the attachment is a PNG image, the `Content-Type`is image/png. If we cannot detect the MIME file type, Content-Type is set to application/octet-stream. The HTTP Response Header `Content-Disposition` contains a filename attribute which can be used when naming the local file. When retrieving attachments with very small file size, the HTTP Response Header `Content-Length` is set to the size of the attachment. Note that for most attachment downloads (larger file sizes), the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Delete Single Document Attachment

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/567
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Deletes the specified attachment and all of its versions.

DELETE `/api/{version}/objects/documents/{doc_id}/attachments/{attachment_id}`

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

`{attachment_id}`

The attachment `id` field value.

#### Response Details

On `SUCCESS`, Vault deletes the specific attachment and all its versions.

### Delete Single Document Attachment Version

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/567/versions/3
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Deletes the specified version of the specified attachment.

DELETE `/api/{version}/objects/documents/{doc_id}/attachments/{attachment_id}/versions/{attachment_version}`

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

`{attachment_id}`

The attachment `id` field value.

`{attachment_version}`

The attachment `version__v` field value.

### Delete Multiple Document Attachments

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Documents\delete_attachments.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/attachments/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 26
        }
    ]
}
'''

Delete multiple document attachments in bulk with a JSON or CSV input file. This works for version-specific attachments and attachments at the document level.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

DELETE `/api/{version}/objects/documents/attachments/batch`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `text/csv` or `application/xml`

#### Body Parameters

Prepare a CSV or JSON input file.

Name

Description

`id`conditional

The attachment ID to delete. Not required if providing a unique field identifier (`idParam`) such as `external_id__v`.

`external_id__v`optional

Identify documents by their external ID instead of regular `id`. You must also add the `idParam=external_id__v` query parameter.

`document_id__v`optional

The source document `id` value.

#### Query Parameters

Name

Description

`idParam`

If you’re identifying attachments in your input by external id, add `idParam=external_id__v` to the request endpoint.

#### Response Details

On `SUCCESS`, the response returns the `id` of all successfully deleted attachments. You can only delete the latest version of an attachment.

### Create Document Attachment

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=my_attachment_file.png" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data":
    {
        "id": "567",
        "version__v": 3
    }
}
'''

Create an attachment on the latest version of a document. If the attachment already exists, Vault uploads the attachment as a new version of the existing attachment. Learn more about [attachment versioning in Vault Help](https://platform.veevavault.help/en/lr/24287#version-specific).

To create a version-specific attachment, or to create multiple attachments at once, use the [bulk API](#Create_Multiple_Attachments).

POST `/api/{version}/objects/documents/{doc_id}/attachments`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

#### File Upload

To upload the file, use the multi-part attachment with the file component `"file={file_name}"`. The maximum allowed file size is 2GB.

#### Response Details

On `SUCCESS`, the response will contain the attachment ID and version of the newly added attachment. Document attachments are automatically bound to all versions of a document. The following attribute values are determined based on the file in the request: `filename__v`, `format__v`, `size__v`.

### Create Multiple Document Attachments

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Documents\create_attachments.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/attachments/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 39,
            "version": 1
        }
    ]
}
'''

Create multiple document attachments in bulk with a JSON or CSV input file. You must first load the attachments to [file staging](/docs/#FTP). This works for version-specific attachments and attachments at the document level. If the attachment already exists, Vault uploads the attachment as a new version of the existing attachment. Learn more about [attachment versioning in Vault Help](https://platform.veevavault.help/en/lr/24287#version-specific).

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

POST `/api/{version}/objects/documents/attachments/batch`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `text/csv` or `application/xml`

#### Body Parameters

Prepare a CSV or JSON input file.

Name

Description

`document_id__v`required

The document ID to add this attachment.

`filename__v`required

The name for the new attachment. This name must include the file extension, for example, `MyAttachment.pdf`. If an attachment with this name already exists, this attachment is added as a new version.

`file`required

The filepath of the attachment on file staging.

`description__v`optional

Description of the attachment. Maximum 1000 characters.

`major_version_number__v`optional

The major version of the source document.

`minor_version_number__v`optional

The minor version of the source document.

`external_id__v`optional

Set an external ID value on the attachment.

[![Download Input File](../../images/download-json-orange.svg)](../../docs/sample-files/bulk-create-document-attachments.json)

#### Response Details

On `SUCCESS`, returns the ID and version of new attachments. Attachments created unsuccessfully are reported with an error message.

### Restore Document Attachment Version

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/567/versions/2?restore=true
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data":
    {
        "id": "567",
        "version__v": 3
    }
}
'''

POST `/api/{version}/objects/documents/{doc_id}/attachments/{attachment_id}/versions/{attachment_version}?restore=true`

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

`{attachment_id}`

The attachment `id` field value.

`{attachment_version}`

The attachment `version__v` field value.

#### Query Parameters

Name

Description

`restore`

The parameter `restore` must be set to `true`.

#### Response Details

On `SUCCESS`, Vault restores the specific version of an existing attachment to make it the latest version. The response will contain the attachment ID and version of the restored attachment.

### Update Document Attachment Description

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "description__v=This is my description for this attachment." \
https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Update an attachment on the latest version of a document. To update a version-specific attachment, or to update multiple attachments at once, use the [bulk API](#Update_Multiple_Attachments).

PUT `/api/{version}/objects/documents/{doc_id}/attachments/{attachment_id}`

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

`{attachment_id}`

The attachment `id` field value.

#### Body Parameters

Name

Description

`description__v`required

This is the only editable field. The maximum character length is 1000.

### Update Multiple Document Attachment Descriptions

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Documents\update_attachments.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/attachments/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 38,
            "version": 2
        }
    ]
}
'''

Update multiple document attachments in bulk with a JSON or CSV input file. This works for version-specific attachments and attachments at the document level. You can only update the latest version of an attachment.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

PUT `/api/{version}/objects/documents/attachments/batch`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `text/csv` or `application/xml`

#### Body Parameters

Prepare a CSV or JSON input file.

Name

Description

`id`conditional

The attachment ID to update. Not required if providing a unique field identifier (`idParam`) such as `external_id__v`.

`external_id__v`conditional

Identify attachments by their external ID instead of regular `id`. You must also add the `idParam=external_id__v` query parameter.

`description__v`required

Description of the attachment. Maximum 1,000 characters.

[![Download Input File](../../images/download-json-orange.svg)](../../docs/sample-files/bulk-update-multiple-document-attachment-descriptions.json)

#### Query Parameters

Name

Description

`idParam`

If you’re identifying attachments in your input by external id, add `idParam=external_id__v` to the request endpoint.

#### Response Details

On `SUCCESS`, the response gives the `id` and `version` of all successfully updated attachments.

## Document Annotations

Learn about [Document Annotations](https://platform.veevavault.help/en/lr/9777) in Vault Help.

### Review Results
- **Location:** `veevavault/services/documents/annotations_service.py`
- **Functions:** `retrieve_annotation_type_metadata`, `retrieve_annotation_placemark_type_metadata`, `retrieve_annotation_reference_type_metadata`, `create_multiple_annotations`, `add_annotation_replies`, `update_annotations`, `read_annotations_by_document_version_and_type`, `read_annotations_by_id`, `read_replies_of_parent_annotation`, `delete_annotations`, `export_document_annotations_to_pdf`, `export_document_version_annotations_to_pdf`, `import_document_annotations_from_pdf`, `import_document_version_annotations_from_pdf`, `retrieve_video_annotations`
- **Updates Made:**
    - Aligned function names with the API documentation.
    - Added the missing `retrieve_video_annotations` function.
- **State:** Compliant with API documentation.

### Retrieve Annotation Type Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/annotations/types/note__sys' \
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "name": "note__sys",
        "allows_replies": true,
        "allowed_placemark_types": [
            "arrow__sys",
            "ellipse__sys",
            "page_level__sys",
            "rectangle__sys",
            "sticky__sys",
            "text__sys"
        ],
        "allowed_reference_types": [],
        "fields": [
            {
                "name": "created_by_delegate_user__sys",
                "type": "String",
                "system_managed": true,
                "value_set": []
            },
            {
                "name": "created_by_user__sys",
                "type": "String",
                "system_managed": true,
                "value_set": []
            },
            {
                "name": "created_date_time__sys",
                "type": "DateTime",
                "system_managed": true,
                "value_set": []
            },
            {
                "name": "document_version_id__sys",
                "type": "String",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "external_id__sys",
                "type": "String",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "id__sys",
                "type": "String",
                "system_managed": true,
                "value_set": []
            },
            {
                "name": "modified_by_user__sys",
                "type": "String",
                "system_managed": true,
                "value_set": []
            },
            {
                "name": "modified_date_time__sys",
                "type": "DateTime",
                "system_managed": true,
                "value_set": []
            },
            {
                "name": "persistent_id__sys",
                "type": "String",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "title__sys",
                "type": "String",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "color__sys",
                "type": "String",
                "system_managed": false,
                "value_set": [
                    "yellow_light__sys",
                    "green_dark__sys",
                    "green_light__sys",
                    "orange_dark__sys",
                    "orange_light__sys",
                    "pink_dark__sys",
                    "pink_light__sys",
                    "purple_dark__sys",
                    "purple_light__sys",
                    "red_dark__sys",
                    "red_light__sys",
                    "yellow_dark__sys"
                ]
            },
            {
                "name": "comment__sys",
                "type": "String",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "original_source_document_version_id__sys",
                "type": "String",
                "system_managed": true,
                "value_set": []
            },
            {
                "name": "reply_count__sys",
                "type": "Number",
                "system_managed": true,
                "value_set": []
            },
            {
                "name": "state__sys",
                "type": "String",
                "system_managed": false,
                "value_set": [
                    "open__sys",
                    "resolved__sys"
                ]
            },
            {
                "name": "tag_names__sys",
                "type": "String list",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "type__sys",
                "type": "String",
                "system_managed": false,
                "value_set": [
                    "note__sys"
                ]
            }
        ]
    }
}
'''

Retrieves the metadata of an annotation type, including metadata and value sets for all supported fields on the annotation type. Learn more about [annotation types in the Vault Java SDK documentation](/sdk/#Annotation_Types).

GET `/api/{version}/metadata/objects/documents/annotations/types/{annotation_type}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{annotation_type}`required

The name of the annotation type. Valid annotation types include:

-   `note__sys`
-   `line__sys`
-   `document_link__sys`
-   `permalink_link__sys`
-   `anchor__sys`
-   `reply__sys`
-   `external_link__sys`

The following annotation types are only valid in Medical and PromoMats Vaults:

-   `suggested_link__sys`
-   `approved_link__sys`
-   `auto_link__sys`
-   `keyword_link__sys`

#### Response Details

On `SUCCESS`, the response includes a list of metadata information for the specified annotation type. Each response may include some or all of the following fields depending on type:

Field

Description

`allows_replies`

if `true`, this annotation type allows replies.

`allowed_placemark_types`

A list of placemark types this annotation type allows. Learn more about [placemark types in the Vault Java SDK documentation](/sdk/#Annotation_Placemarks).

`allowed_reference_types`

A list of reference types that this annotation type allows. Learn more about [reference types in the Vault Java SDK documentation](/sdk/#Annotation_References).

`fields`

A list of fields configured on the annotation type. For more details about annotation fields, see [Read Annotations by Document Version and Type](#Read_Annotations_by_Document_Version_and_Type).

### Retrieve Annotation Placemark Type Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/annotations/placemarks/types/arrow__sys \
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "name": "arrow__sys",
        "fields": [
            {
                "name": "coordinates__sys",
                "type": "Number list",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "height__sys",
                "type": "Number",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "width__sys",
                "type": "Number",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "x_coordinate__sys",
                "type": "Number",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "y_coordinate__sys",
                "type": "Number",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "page_number__sys",
                "type": "Number",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "style__sys",
                "type": "String",
                "system_managed": false,
                "value_set": [
                    "arrow_down_left__sys",
                    "arrow_down_right__sys",
                    "arrow_left_down__sys",
                    "arrow_left_up__sys",
                    "arrow_right_down__sys",
                    "arrow_right_up__sys",
                    "arrow_up_left__sys",
                    "arrow_up_right__sys"
                ]
            },
            {
                "name": "type__sys",
                "type": "String",
                "system_managed": false,
                "value_set": [
                    "arrow__sys"
                ]
            }
        ]
    }
}
'''

Retrieves the metadata of a specified annotation placemark type. Learn more about [placemark types in the Vault Java SDK documentation](/sdk/#Annotation_Placemarks).

GET `/api/{version}/metadata/objects/documents/annotations/placemarks/types/{placemark_type}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{placemark_type}`required

The name of the placemark type. For example, `sticky__sys`. Learn more about [placemark types in the Vault Java SDK documentation](/sdk/#Annotation_Placemarks).

#### Response Details

On `SUCCESS`, the response includes a list of metadata information for the specified placemark type. Each response may include some or all of the following fields depending on type:

Field

Description

`coordinates__sys`

A list of all coordinates for the placemark.

`height__sys`

The height of the selection, measured in pixels at 72 DPI.

`width__sys`

The width of the selection, measured in pixels at 72 DPI.

`x_coordinate__sys`

The X coordinate of the position of the top-left of the selection, measured in pixels at 72 DPI.

`y_coordinate__sys`

The Y coordinate of the position of the top-left of the selection, measured in pixels at 72 DPI.

`page_number__sys`

The document page number where the annotation appears. Page numbers start at 1.

`style__sys`

The style of the placemark. For example, `sticky_icon__sys`.

`reply_parent__sys`

Reply-type annotations only. The ID of the parent annotation.

`reply_position_index__sys`

The position of a reply in a series of replies to a parent annotation. Positions start at 1.

`text_start_index__sys`

Annotations placed on text selections only. The index of the first selected word on a page.

`text_end_index__sys`

Annotations placed on text selections only. The index of the last selected word on a page.

### Retrieve Annotation Reference Type Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/annotations/references/types/document__sys \
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "name": "document__sys",
        "fields": [
            {
                "name": "annotation__sys",
                "type": "String",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "document_version_id__sys",
                "type": "String",
                "system_managed": false,
                "value_set": []
            },
            {
                "name": "type__sys",
                "type": "String",
                "system_managed": true,
                "value_set": [
                    "document__sys"
                ]
            }
        ]
    }
}
'''

Retrieves the metadata of a specified annotation reference type. Learn more about [reference types in the Vault Java SDK documentation](/sdk/#Annotation_References).

GET `/api/{version}/metadata/objects/documents/annotations/references/types/{reference_type}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{reference_type}`required

The name of the reference type. For example, `permalink__sys`. Learn more about [reference types in the Vault Java SDK documentation](/sdk/#Annotation_References).

#### Response Details

On `SUCCESS`, the response includes a list of annotations of the specified type(s) for the document version. Each Annotation object may include some or all of the following fields depending on type:

Field

Description

`annotation__sys`

Document-type references only. The ID of the referenced anchor annotation, or null for references to an entire document.

`document_version_id__sys`

Document-type references only. The ID and version number of the referenced document in the format `{documentId}_{majorVersion}_{minorVersion}`. For example, `138_2_1`.

`permalink__sys`

Permalink-type references only. The ID of the referenced permalink.

`url__sys`

External-type references only. The URL of the external reference. Allows up to 32,000 characters.

### Create Multiple Annotations

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '[
   {
       "type__sys": "note__sys",
       "document_version_id__sys": "1001_0_1",
       "external_id__sys": "12345",
       "color__sys": "orange_dark__sys",
       "comment__sys": "hello world",
       "placemark": {
           "type__sys": "sticky__sys",
           "page_number__sys": 1,
           "x_coordinate__sys": 50.5,
           "y_coordinate__sys": 25.5
       }
   },
   {
       "type__sys": "document_link__sys",
       "document_version_id__sys": "1001_0_1",
       "placemark": {
           "type__sys": "text__sys",
           "page_number__sys": 1,
           "text_start_index__sys": 10,
           "text_end_index__sys": 15
       },
       "references": [
           {
               "type__sys": "document__sys",
               "document_version_id__sys": "301_0_4",
               "annotation__sys": "104"
           },
           {
               "type__sys": "document__sys",
               "document_version_id__sys": "601_0_1"
           }
       ]
   }
]'
https://myvault.veevavault.com/api/v25.2/objects/documents/annotations/batch \
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "document_version_id__sys": "1001_0_1",
            "global_version_id__sys": "119899_1001_36",
            "id__sys": "141"
        },
        {
            "responseStatus": "SUCCESS",
            "document_version_id__sys": "1001_0_1",
            "global_version_id__sys": "119899_1001_36",
            "id__sys": "142"
        }
    ]
}
'''

Create up to 500 annotations.

POST `/api/{version}/objects/documents/annotations/batch`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `text/csv`

`Content-Type`

`application/json`

#### Body Parameters

Prepare a JSON-formatted list of annotation objects, each containing a list of annotation properties and their values. For more details about annotation fields, see [Read Annotations by Document Version and Type](#Read_Annotations_by_Document_Version_and_Type).

#### Response Details

On `SUCCESS`, the response includes a `responseStatus` indicating whether each annotation object in the request body was successfully created. For successfully created annotations, the response also includes the following:

Field

Description

`document_version_id__sys`

The ID and version number of the document where the annotation appears in the format `{documentId}_{majorVersion}_{minorVersion}`. For example, `138_2_1`.

`global_version_id__sys`

The Vault ID, document ID, and document version ID in the format `{vaultId}_{documentId}_{docVersionId}`. For example, `123456_2_1`.

`id`

The annotation ID.

### Add Annotation Replies

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '[
   {
       "document_version_id__sys": "1_0_1",
       "type__sys": "reply__sys",
       "comment__sys": "first reply from the api",
       "placemark": {
           "type__sys": "reply__sys",
           "reply_parent__sys": "54"
       }
   },
   {
       "document_version_id__sys": "1_0_1",
       "type__sys": "reply__sys",
       "color__sys": "green_light__sys",
       "comment__sys": "first reply from the api",
       "placemark": {
           "type__sys": "reply__sys",
           "reply_parent__sys": "55"
       }
   },
   {
       "document_version_id__sys": "1_0_1",
       "type__sys": "reply__sys",
       "comment__sys": "second reply from the api",
       "placemark": {
           "type__sys": "reply__sys",
           "reply_parent__sys": "54"
       }
   }
]'
https://myvault.veevavault.com/api/v25.2/objects/documents/annotations/replies/batch \
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "document_version_id__sys": "1_0_1",
            "global_version_id__sys": "123456_1_1",
            "id__sys": "60"
        },
        {
            "responseStatus": "SUCCESS",
            "document_version_id__sys": "1_0_1",
            "global_version_id__sys": "123456_1_1",
            "id__sys": "62"
        },
        {
            "responseStatus": "SUCCESS",
            "document_version_id__sys": "1_0_1",
            "global_version_id__sys": "123456_1_1",
            "id__sys": "61"
        }
    ]
}
'''

Create up to 500 annotation replies.

POST `/api/{version}/objects/documents/annotations/replies/batch`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `text/csv`

`Content-Type`

`application/json`

#### Body Parameters

Prepare a JSON-formatted list of annotation reply objects. Each object must contain the `id__sys`, `document_version_id__sys`, and the annotation field(s) to be set, and a `placemark` object containing the following:

Placemark Field

Description

`type__sys`required

The annotation type. This must always be `reply__sys`.

`reply_parent__sys`required

The ID of the parent annotation.

#### Response Details

On SUCCESS, the response includes the document version ID, global version ID, and ID and version of each successfully created reply. See [Create Annotations](#Create_Multiple_Annotations) for details. Replies that were not added successfully are reported with an error message.

### Update Annotations

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '[
   {
       "id__sys": "58",
       "document_version_id__sys": "1_0_1",
       "comment__sys": "Updated comment from api"
   },
   {
       "id__sys": "54",
       "document_version_id__sys": "1_0_1",
       "color__sys": "yellow_light__sys"
   }
]'
https://myvault.veevavault.com/api/v25.2/objects/documents/annotations/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "document_version_id__sys": "1_0_1",
            "global_version_id__sys": "123456_1_1",
            "id__sys": "58"
        },
        {
            "responseStatus": "SUCCESS",
            "document_version_id__sys": "1_0_1",
            "global_version_id__sys": "123456_1_1",
            "id__sys": "54"
        }
    ]
}
'''

Update up to 500 existing annotations.

PUT `/api/{version}/objects/documents/annotations/batch`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `text/csv`

`Content-Type`

`application/json`

#### Body Parameters

Prepare a JSON-formatted list of annotation objects. Each object must contain the `id__sys`, `document_version_id__sys`, and the annotation field(s) to be updated. For more details about annotation fields, see [Read Annotations by Document Version and Type](#Read_Annotations_by_Document_Version_and_Type).

You can only update an annotation ID (`id__sys`) once per request. If you provide duplicate annotation IDs, the bulk update fails any duplicate annotations.

#### Response Details

On `SUCCESS`, the response includes the document version ID, global version ID, and ID and version of updated annotations. See [Create Annotations](#Create_Multiple_Annotations) for details. Annotations that did not update successfully are reported with an error message.

### Read Annotations by Document Version and Type

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/502/versions/0/1/annotations?annotation_types=document_link__sys,note__sys
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "document_version_id__sys": "502_0_1",
            "modified_by_user__sys": "133999",
            "references": [],
            "id__sys": "129",
            "placemark": {
                "y_coordinate__sys": 627.82,
                "coordinates__sys": [
                    72.024,
                    627.82,
                    108.489,
                    627.82,
                    72.024,
                    616.78,
                    108.489,
                    616.78
                ],
                "text_start_index__sys": 5,
                "text_end_index__sys": 5,
                "type__sys": "text__sys",
                "height__sys": 11.04,
                "width__sys": 36.465,
                "x_coordinate__sys": 72.024,
                "page_number__sys": 1,
                "style__sys": "text_highlight__sys"
            },
            "created_by_user__sys": "133999",
            "comment__sys": "Fix kerning",
            "created_date_time__sys": "2024-09-12T23:37:55.000Z",
            "modified_date_time__sys": "2024-09-12T23:37:55.000Z",
            "persistent_id__sys": "119899_129",
            "title__sys": "Patients",
            "type__sys": "note__sys",
            "tag_names__sys": [
                "Typography"
            ],
            "state__sys": "open__sys",
            "reply_count__sys": 0,
            "color__sys": "yellow_light__sys"
        },
        {
            "document_version_id__sys": "502_0_1",
            "modified_by_user__sys": "133999",
            "references": [
                {
                    "document_version_id__sys": "301_0_3",
                    "type__sys": "document__sys",
                    "annotation__sys": "56"
                }
            ],
            "id__sys": "143",
            "external_id__sys": "12345",
            "placemark": {
                "y_coordinate__sys": 717.82,
                "coordinates__sys": [
                    124.188,
                    717.82,
                    177.622,
                    717.82,
                    124.188,
                    706.78,
                    177.622,
                    706.78,
                    72.024,
                    695.38,
                    101.479,
                    695.38,
                    72.024,
                    684.34,
                    101.479,
                    684.34,
                    72.024,
                    672.82,
                    111.348,
                    672.82,
                    72.024,
                    661.78,
                    111.348,
                    661.78,
                    72.024,
                    650.38,
                    120.975,
                    650.38,
                    72.024,
                    639.34,
                    120.975,
                    639.34,
                    72.024,
                    627.82,
                    108.489,
                    627.82,
                    72.024,
                    616.78,
                    108.489,
                    616.78
                ],
                "text_start_index__sys": 1,
                "text_end_index__sys": 5,
                "type__sys": "text__sys",
                "height__sys": 101.04,
                "width__sys": 105.598,
                "x_coordinate__sys": 72.024,
                "page_number__sys": 1,
                "style__sys": "text_link__sys"
            },
            "created_by_user__sys": "133999",
            "comment__sys": "",
            "created_date_time__sys": "2024-09-13T23:04:25.000Z",
            "modified_date_time__sys": "2024-09-13T23:04:25.000Z",
            "persistent_id__sys": "119899_143",
            "title__sys": "Information Insulin Diabetes Indications Patients",
            "type__sys": "document_link__sys",
            "state__sys": "open__sys",
            "color__sys": "blue_dark__sys"
        }
    ],
    "responseDetails": {
        "offset": 0,
        "limit": 500,
        "size": 2,
        "total": 2
    }
}
'''

Retrieve annotations from a specific document version. You can retrieve all annotations or choose to retrieve only certain annotation types.

You must have _View Content_ permission on the specified document version.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`required

The document `id` field value.

`{major_version}`required

The document `major_version_number__v` field value.

`{minor_version}`required

The document `minor_version_number__v` field value.

#### Query Parameters

Name

Description

`offset`optional

This parameter is used to paginate the results. It specifies the amount of offset from the first record returned. Vault returns 200 records per page by default. If you are viewing the first 200 results (page 1) and want to see the next page, set this to `offset=201`.

`limit`optional

Paginate the results by specifying the maximum number of records per page in the response. This can be any value between `1` and `500`. If omitted, defaults to `500`. Values greater than `500` are ignored.

`pagination_id`optional

A unique identifier used to load requests with paginated results. For example, `b688a6f4-d0c4-4f72-9eb4-ceba01136466`.

`annotation_types`optional

The type(s) of annotations to retrieve. For example, `note__sys,anchor__sys`. If omitted, Vault returns all annotation types except replies. Valid annotation types include:

-   `note__sys`
-   `line__sys`
-   `document_link__sys`
-   `permalink_link__sys`
-   `anchor__sys`
-   `reply__sys`
-   `external_link__sys`

The following annotation types are only valid in Medical and PromoMats Vaults:

-   `suggested_link__sys`
-   `approved_link__sys`
-   `auto_link__sys`
-   `keyword_link__sys`

#### Response Details

On `SUCCESS`, the response includes a list of annotations of the specified type(s) for the document version. Each Annotation object may include some or all of the following fields depending on type:

Annotation Field

Description

`document_version_id__sys`

The ID and version number of the document where the annotation appears in the format `{documentId}_{majorVersion}_{minorVersion}`. For example, `138_2_1`.

`modified_by_user__sys`

The ID of the user who last modified the annotation. If no last modified information exists, this defaults to the value of `created_by_user__sys`.

`id__sys`

The annotation ID.

`placemark`

A list of fields whose values define where on a document an annotation appears. See [below](#Placemarks) for details.

`references`

A list of annotation references. See [below](#Annotation_References) for details.

`created_by_user__sys`

The ID of the user who created the annotation.

`created_by_delegate_user__sys`

The ID of the delegate user who created the annotation, if applicable.

`comment__sys`

The annotation comment text. Allows up to 32,000 characters. Not all annotation types allow comments.

`created_date_time__sys`

The date and time when the annotation was created.

`modified_date_time__sys`

The date and time when the annotation was last modified. If no last modified information exists, this defaults to the value of `created_date_time__sys`.

`persistent_id__sys`

The persistent ID. This ID remains the same across all document versions when brought forward. Some older annotations may not have a persistent ID. You can generate one by updating or bringing forward the annotation.

`external_id__sys`

The external ID. This field is optional and can be any non-empty string with a maximum of 250 characters. If no value is set, the field is excluded from the response.

`linked_object__sys`

The name of the primary linked object for the annotation. Not all annotation types support linked objects.

`linked_records__sys`

The ID(s) of the object record or records the annotation is linked to. Not all annotation types support linked records.

`title__sys`

The title of the annotation. Allows up to 1,500 characters. For annotations with text placemarks, this must be set to the selected text.

`type__sys`

The name of the annotation type. For example, `note__sys`.

`state__sys`

The name of the state of the annotation, either `open__sys` or `resolved__sys`. Not all annotation types support states.

`reply_count__sys`

For annotation types that support replies, the number of replies to this annotation.

`color__sys`

The name of the annotation color. Some annotation types allow users to select from a variety of colors, while others are always the same color.

`tag_names__sys`

A list of the names of each tag associated with each annotation. Not all annotation types support tags.

`anchor_name__sys`

Anchor annotations only: The name of the anchor. Allows up to 140 characters.

`match_text_variation__sys`

PromoMats Vaults with Suggested Links enabled only: The ID of the `matched_text_variation__sys` object record linked to the `annotation_keywords__sys` record associated with the annotation.

`offset`

The `offset` value specified in the request.

`limit`

The `limit` value specified in the request.

`size`

The number of records displayed on the current page.

`total`

The total number of annotations found.

`next_page`

The pagination URL to navigate to the next page of results. Only included if the number of results exceeds the number defined by a request’s limit.

`previous_page`

The pagination URL to navigate to the previous page of results. Only included if the request included an offset, or after navigating to the next\_page URL.

#### Placemarks

A placemark defines where on a document an annotation appears. For example, a text selection, a page number, or the coordinates of an area selection.

Placemark coordinates are listed in the style of PDF quad points and are measured in pixels from the bottom-left of the page at 72 DPI. There will be 8\*n coordinates, where n is the number of rectangles that make up the placemark. Annotation placemarks include the following fields:

Placemark Field

Description

`coordinates__sys`

A list of all coordinates for the placemark. Text placemarks must set the `title__sys` field to the selected text in addition to specifying coordinates.

`y_coordinate__sys`

The Y coordinate of the position of the top-left of the selection, measured in pixels at 72 DPI.

`x_coordinate__sys`

The X coordinate of the position of the top-left of the selection, measured in pixels at 72 DPI.

`text_start_index__sys`

Annotations placed on text selections only. The index of the first selected word on a page.

`text_end_index__sys`

Annotations placed on text selections only. The index of the last selected word on a page.

`type__sys`

The placemark type. For example, `text__sys`.

`height__sys`

The height of the selection, measured in pixels at 72 DPI.

`width__sys`

The width of the selection, measured in pixels at 72 DPI.

`page_number__sys`

The document page number where the annotation appears. Page numbers start at 1.

`style__sys`

The style of the placemark. For example, `sticky_icon__sys`.

`reply_parent__sys`

Reply-type annotations only. The ID of the parent annotation.

`reply_position_index__sys`

The position of a reply in a series of replies to a parent annotation. Positions start at 1.

#### References

A reference is a way for an annotation to refer to an external entity. This can be a document, an anchor annotation on a document, an external URL, or a permalink.

Annotation references include the following fields:

Reference Field

Description

`document_version_id__sys`

Document-type references only. The ID and version number of the referenced document in the format `{documentId}_{majorVersion}_{minorVersion}`. For example, `138_2_1.`

`permalink__sys`

Permalink-type references only. The ID of the referenced permalink.

`url__sys`

External-type references only. The URL of the external reference. Allows up to 32,000 characters.

`type__sys`

The reference type:`document__sys`, `external__sys`, or `permalink__sys`.

`annotation__sys`

Document-type references only. The ID of the referenced anchor annotation, or null for references to an entire document.

### Read Annotations by ID

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/301/versions/0/4/annotations/134
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "document_version_id__sys": "301_0_4",
            "modified_by_user__sys": "133999",
            "references": [],
            "id__sys": "134",
            "external_id__sys": "12345",
            "placemark": {
                "type__sys": "sticky__sys",
                "y_coordinate__sys": 25.5,
                "x_coordinate__sys": 50.5,
                "page_number__sys": 1,
                "style__sys": "sticky_icon__sys"
            },
            "created_by_user__sys": "133999",
            "comment__sys": "Remove this.",
            "created_date_time__sys": "2024-09-13T21:57:00.000Z",
            "modified_date_time__sys": "2024-09-13T21:57:00.000Z",
            "persistent_id__sys": "119899_134",
            "title__sys": "",
            "type__sys": "note__sys",
            "state__sys": "open__sys",
            "reply_count__sys": 0,
            "color__sys": "orange_dark__sys"
        }
    ]
}
'''

Retrieve a specific annotation by the annotation ID. You must have _View Content_ permission on the document version containing the specified ID.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations/{annotation_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`required

The document `id` field value.

`{major_version}`required

The document `major_version_number__v` field value.

`{minor_version}`required

The document `minor_version_number__v` field value.

`{annotation_id}`required

The annotation ID, which can be retrieved with [Read Annotations by Document Version and Type](#Read_Annotations_by_Document_Version_and_Type).

#### Response Details

On `SUCCESS`, the response includes all fields and values for the specified annotation. For more details about annotation fields, see [Read Annotations by Document Version and Type](#Read_Annotations_by_Document_Version_and_Type).

### Read Replies of Parent Annotation

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/102/versions/0/2/annotations/40/replies
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "document_version_id__sys": "102_0_2",
            "modified_by_user__sys": "133999",
            "type__sys": "reply__sys",
            "id__sys": "41",
            "tag_names__sys": [
                "IMG"
            ],
            "state__sys": "open__sys",
            "placemark": {
                "reply_position_index__sys": 1,
                "type__sys": "reply__sys",
                "reply_parent__sys": "40"
            },
            "created_by_user__sys": "133999",
            "comment__sys": "I think this image is fine.",
            "created_date_time__sys": "2024-02-07T00:37:36.000Z",
            "modified_date_time__sys": "2024-02-07T00:37:36.000Z",
            "color__sys": "red_dark__sys"
        }
    ],
    "responseDetails": {
        "offset": 0,
        "limit": 500,
        "size": 1,
        "total": 1
    }
}
'''

Given a parent annotation ID, retrieves all replies to the annotation. You must have _View Content_ permission on the document version containing the specified parent annotation ID.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations/{annotation_id}/replies`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`required

The document `id` field value.

`{major_version}`required

The document `major_version_number__v` field value.

`{minor_version}`required

The document `minor_version_number__v` field value.

`{annotation_id}`required

The parent annotation ID, which can be retrieved with [Read Annotations by Document Version and Type](#Read_Annotations_by_Document_Version_and_Type).

#### Response Details

On `SUCCESS`, the response lists all fields and values for all replies to the specified annotation. For more details about annotation fields, see [Read Annotations by Document Version and Type](#Read_Annotations_by_Document_Version_and_Type).

### Delete Annotations

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
--data-binary @"C:\Vault\Documents\delete_annotations.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/annotations/batch
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "responseStatus": "SUCCESS",
           "document_version_id__sys": "1_0_1",
           "id__sys": "58",
           "global_version_id__sys": "119899_1_1"
       }
   ]
}
'''

Delete multiple annotations. The authenticated user must have the appropriate permissions to delete annotations. Learn more about permissions required to [delete annotations](https://platform.veevavault.help/en/lr/9777/#deleting-annotations) and [delete brought forward annotations](https://platform.veevavault.help/en/lr/18648/#permissions) in Vault Help.

DELETE`/api/{version}/objects/documents/annotations/batch`

#### Headers

Name

Description

`Content-Type`

`text/csv` or `application/json`

`Accept`

`application/json` (default), `text/csv`, or `application/xml`

#### Body Parameters

Upload parameters as a JSON or CSV file. You can delete up to 500 annotations per batch.

Name

Description

`id__sys`required

The ID of the annotation to delete.

`document_version_id__sys`required

The ID and version number of the document where the annotation appears in the format `{documentId}_{majorVersion}_{minorVersion}`. For example, `138_2_1`.

### Export Document Annotations to PDF

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/14/annotations/file
'''

Export the latest version of any document, along with its annotations, as an annotated PDF. This is equivalent to the _Export Annotations_ action in the Vault document viewer UI. You can then view annotations, reply to existing annotations, and create new annotations in a [supported PDF editor](https://platform.veevavault.help/en/lr/23833#supported-pdf-editors). When finished, you can import your new notes and replies to Vault using the [Import Document Annotations from PDF](#Upload_Document_Annotations) endpoint.

You must have _View Content_ permission on the latest document version and a security profile that grants the _Document: Download Rendition_ permission to export annotations.

GET `/api/{version}/objects/documents/{doc_id}/annotations/file`

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

#### Response

On `SUCCESS`, Vault retrieves the specified version document rendition and its associated annotations in PDF format.

-   The HTTP Response Header `Content-Type` is set to `application/pdf`.
-   The HTTP Response Header `Content-Disposition` contains a `filename` component which is used as the default name for the local file.

### Export Document Version Annotations to PDF

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/14/versions/2/1/annotations/file
'''

Export a specific version of any document, along with its annotations, as an annotated PDF. This is equivalent to the _Export Annotations_ action in the Vault document viewer UI. You can then view annotations, reply to existing annotations, and create new annotations in a [supported PDF editor](https://platform.veevavault.help/en/lr/23833#supported-pdf-editors). When finished, you can import your new notes and replies to Vault using the [Import Document Version Annotations from PDF](#Upload_Document_Version_Annotations) endpoint.

You must have _View Content_ permission on the specified document version and a security profile that grants the _Document: Download Rendition_ permission to export annotations.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations/file`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

#### Response

On `SUCCESS`, Vault retrieves the specified version document rendition and its associated annotations in PDF format.

-   The HTTP Response Header `Content-Type` is set to `application/pdf`.
-   The HTTP Response Header `Content-Disposition` contains a `filename` component which is used as the default name for the local file.

### Import Document Annotations from PDF

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=document2016.pdf" \
https://myvault.veevavault.com/api/v25.2/objects/documents/548/annotations/file
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "OK",
    "replies": 0,
    "failures": 0,
    "new": 0
}
'''

Load annotations from a PDF to Vault. This is equivalent to the _Import Annotations_ action in the Vault document viewer UI. The file must be a PDF created by exporting annotations for the latest version of the same document through either the _Export Annotations_ action in the Vault UI or the [Export Document Annotations as PDF](#Retrieve_Document_Annotations) endpoint and edited in a [supported PDF editor](https://platform.veevavault.help/en/lr/23833#supported-pdf-editors). You must have a role on the document that includes the _Annotate_ permission.

POST `/api/{version}/objects/documents/{doc_id}/annotations/file`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

#### File Upload

To upload the file, use the multi-part attachment with the file component `"file={file_name}"`. The maximum allowed file size is 4GB. Vault truncates annotations that exceed the following character limits:

-   **Note annotations**: _Subject_ (in Header) limited to 32,000 characters
-   **Note, Line, and Reply annotations**: _Comment_ limited to 32,000 characters

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

#### Response Details

On `SUCCESS`, Vault uploads the file and its annotations.

### Import Document Version Annotations from PDF

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=document2016.pdf" \
https://myvault.veevavault.com/api/v25.2/objects/documents/548/versions/2/1/annotations/file
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "OK",
    "replies": 0,
    "failures": 0,
    "new": 0
}
'''

Load annotations from a PDF to Vault. This is equivalent to the _Import Annotations_ action in the Vault document viewer UI. The file must be a PDF created by exporting annotations for the specified version of the same document through either the _Export Annotations_ action in the Vault UI or the [Export Document Version Annotations as PDF](#Retrieve_Document_Version_Annotations) endpoint. You must have a role on the document that includes the _Annotate_ permission.

POST `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/annotations/file`

#### File Upload

To upload the file, use the multi-part attachment with the file component `"file={file_name}"`. The maximum allowed file size is 4GB. Vault truncates annotations that exceed the following character limits:

-   **Note annotations**: _Subject_ (in Header) limited to 32,000 characters
-   **Note, Line, and Reply annotations**: _Comment_ limited to 32,000 characters

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value.

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

#### Response Details

On `SUCCESS`, Vault uploads the file and its annotations.

### Retrieve Video Annotations

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/14/versions/2/1/export-video-annotations
'''

> Response

'''
* Name: Cholecap Presentation
* Number: VV-00040
* Version: 2
* Status: draft
* Download timestamp: 1/4/18 11:32:02 AM PST

-------------------------------
Time signature: 00:01:35
Note ID: 1515092438330
Author: Lateef Gills
Timestamp: 1/4/18 11:00:38 AM PST
Version of origin: 2
Status: Open
Comment: Slide 3 displays here

Reply author: Teresa Ibanez
Reply timestamp: 1/4/18 12:31:05 PM PST
Reply comment: Thanks!

## END
'''

Retrieve annotations on any version of a document with a video file as its viewable rendition. You must have the _View Content_ permission on the specified document version to retrieve video annotations.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/export-video-annotations`

#### Headers

This `Accept` header only changes the format of the response in the case of an error. On `SUCCESS`, the HTTP Response Header `Content-Type` is set to `text/plain;charset=UnicodeLittle`.

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The video document `id` field value.

`{major_version}`

The video document `major_version_number__v` field value.

`{minor_version}`

The video document `minor_version_number__v` field value.

#### Response Details

On `SUCCESS`, Vault includes the following information in plain text format:

Metadata Field

Description

`Note ID`

The `id` of the video annotation to retrieve.

`Author`

The name of the user who created the annotation.

`Timestamp`

Timestamp when the annotation was created.

`Version of origin`

The original version of the document where the annotation was created.

`Note status`

Indicates the status of a note annotation, either `Open` or `Resolved`.

`Comment text`

The annotation text.

This example includes a reply and the reply details under the parent note. Vault orders annotations by time signature.

## Document Relationships

Learn about [Document Relationships](https://platform.veevavault.help/en/lr/21330) in Vault Help.

### Review Results
- **Location:** `veevavault/services/documents/relationships_service.py`
- **Functions:** `retrieve_document_type_relationships`, `retrieve_document_relationships`, `create_single_document_relationship`, `create_multiple_document_relationships`, `retrieve_document_relationship`, `delete_single_document_relationship`, `delete_multiple_document_relationships`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve Document Type Relationships

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/types/promotional__c/relationships
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "properties": [
        {
            "name": "id",
            "type": "id",
            "length": 20,
            "editable": false,
            "queryable": true,
            "required": true,
            "multivalue": false,
            "onCreateEditable": false
        },
        {
            "name": "source_doc_id__v",
            "type": "id",
            "length": 20,
            "editable": true,
            "queryable": true,
            "required": true,
            "multivalue": false,
            "onCreateEditable": true
        },
        {
            "name": "source_major_version__v",
            "type": "Integer",
            "length": 10,
            "editable": false,
            "queryable": true,
            "required": false,
            "multivalue": false,
            "onCreateEditable": true
        },
        {
            "name": "source_minor_version__v",
            "type": "Integer",
            "length": 10,
            "editable": false,
            "queryable": true,
            "required": false,
            "multivalue": false,
            "onCreateEditable": true
        },
        {
            "name": "target_doc_id__v",
            "type": "id",
            "length": 20,
            "editable": false,
            "queryable": true,
            "required": true,
            "multivalue": false,
            "onCreateEditable": true
        },
        {
            "name": "target_major_version__v",
            "type": "Integer",
            "length": 10,
            "editable": false,
            "queryable": true,
            "required": false,
            "multivalue": false,
            "onCreateEditable": true
        },
        {
            "name": "target_minor_version__v",
            "type": "Integer",
            "length": 10,
            "editable": false,
            "queryable": true,
            "required": false,
            "multivalue": false,
            "onCreateEditable": true
        },
        {
            "name": "relationship_type__v",
            "type": "String",
            "length": 255,
            "editable": false,
            "queryable": true,
            "required": true,
            "multivalue": false,
            "onCreateEditable": true
        },
        {
            "name": "created_date__v",
            "type": "DateTime",
            "length": 0,
            "editable": false,
            "queryable": true,
            "required": false,
            "multivalue": false,
            "onCreateEditable": false
        },
        {
            "name": "created_by__v",
            "type": "ObjectReference",
            "length": 10,
            "object": "users",
            "editable": false,
            "queryable": true,
            "required": false,
            "multivalue": false,
            "onCreateEditable": false
        },
        {
            "name": "source_vault_id__v",
            "type": "id",
            "length": 20,
            "editable": false,
            "queryable": true,
            "required": false,
            "multivalue": false,
            "onCreateEditable": false
        }
    ],
    "relationshipTypes": [
        {
            "value": "crosslink_document_latest__v",
            "label": "CrossLink Latest Bindings",
            "sourceDocVersionSpecific": true,
            "targetDocVersionSpecific": false,
            "system": true,
            "singleUse": false,
            "targetDocumentTypes": [
                {
                    "label": "Attachment",
                    "value": "attachment__v"
                },
                {
                    "label": "Staged",
                    "value": "staged__v"
                },
                {
                    "label": "Medication Packaging Text",
                    "value": "medication_packaging_text__c"
                },
                {
                    "label": "Promotional",
                    "value": "promotional__c"
                },
                {
                    "label": "Unclassified",
                    "value": "undefined__v"
                }
            ]
        },
        {
            "value": "supporting_documents__c",
            "label": "Supporting Documents",
            "sourceDocVersionSpecific": false,
            "targetDocVersionSpecific": false,
            "system": false,
            "singleUse": false,
            "targetDocumentTypes": [
                {
                    "label": "Attachment",
                    "value": "attachment__v"
                },
                {
                    "label": "Staged",
                    "value": "staged__v"
                },
                {
                    "label": "Medication Packaging Text",
                    "value": "medication_packaging_text__c"
                },
                {
                    "label": "Promotional",
                    "value": "promotional__c"
                },
                {
                    "label": "Unclassified",
                    "value": "undefined__v"
                }
            ]
        },
        {
            "value": "references__v",
            "label": "Linked Documents",
            "sourceDocVersionSpecific": true,
            "targetDocVersionSpecific": true,
            "system": true,
            "singleUse": false,
            "targetDocumentTypes": [
                {
                    "label": "Attachment",
                    "value": "attachment__v"
                },
                {
                    "label": "Staged",
                    "value": "staged__v"
                },
                {
                    "label": "Medication Packaging Text",
                    "value": "medication_packaging_text__c"
                },
                {
                    "label": "Promotional",
                    "value": "promotional__c"
                },
                {
                    "label": "Unclassified",
                    "value": "undefined__v"
                }
            ]
        },
        {
            "value": "crosslink_document_latest_steady_state__v",
            "label": "CrossLink Latest Steady State Bindings",
            "sourceDocVersionSpecific": true,
            "targetDocVersionSpecific": false,
            "system": true,
            "singleUse": false,
            "targetDocumentTypes": [
                {
                    "label": "Attachment",
                    "value": "attachment__v"
                },
                {
                    "label": "Staged",
                    "value": "staged__v"
                },
                {
                    "label": "Medication Packaging Text",
                    "value": "medication_packaging_text__c"
                },

                {
                    "label": "Promotional",
                    "value": "promotional__c"
                },
                {
                    "label": "Unclassified",
                    "value": "undefined__v"
                }
            ]
        },
        {
            "value": "basedon__v",
            "label": "Based on",
            "sourceDocVersionSpecific": false,
            "targetDocVersionSpecific": true,
            "system": true,
            "singleUse": false,
            "targetDocumentTypes": [
                {
                    "label": "Attachment",
                    "value": "attachment__v"
                },
                {
                    "label": "Staged",
                    "value": "staged__v"
                },
                {
                    "label": "Medication Packaging Text",
                    "value": "medication_packaging_text__c"
                },
                {
                    "label": "Promotional",
                    "value": "promotional__c"
                },
                {
                    "label": "Unclassified",
                    "value": "undefined__v"
                }
            ]
        },
        {
            "value": "original_source__v",
            "label": "Original Source",
            "sourceDocVersionSpecific": false,
            "targetDocVersionSpecific": true,
            "system": true,
            "singleUse": false,
            "targetDocumentTypes": [
                {
                    "label": "Attachment",
                    "value": "attachment__v"
                },
                {
                    "label": "Staged",
                    "value": "staged__v"
                },
                {
                    "label": "Medication Packaging Text",
                    "value": "medication_packaging_text__c"
                },
                {
                    "label": "Promotional",
                    "value": "promotional__c"
                },
                {
                    "label": "Unclassified",
                    "value": "undefined__v"
                }
            ]
        },
        {
            "value": "crosslink_document_static__v",
            "label": "CrossLink Static Bindings",
            "sourceDocVersionSpecific": true,
            "targetDocVersionSpecific": true,
            "system": true,
            "singleUse": false,
            "targetDocumentTypes": [
                {
                    "label": "Attachment",
                    "value": "attachment__v"
                },
                {
                    "label": "Staged",
                    "value": "staged__v"
                },
                {
                    "label": "Medication Packaging Text",
                    "value": "medication_packaging_text__c"
                },
                {
                    "label": "Doc Roles Doc",
                    "value": "doc_roles_doc__c"
                },
                {
                    "label": "Promotional",
                    "value": "promotional__c"
                },
                {
                    "label": "Unclassified",
                    "value": "undefined__v"
                }
            ]
        }
    ],
    "relationships": [
        {
            "relationship_name": "source__vr",
            "relationship_label": "Source Relationship",
            "relationship_type": "reference_outbound",
            "object": {
                "name": "documents"
            }
        },
        {
            "relationship_name": "target__vr",
            "relationship_label": "Target Relationship",
            "relationship_type": "reference_outbound",
            "object": {
                "name": "documents"
            }
        }
    ]
}
'''

Retrieve all relationships from a document type.

GET `/api/{version}/metadata/objects/documents/types/{type}/relationships`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{type}`

The document type. See [Retrieve Document Types](#Retrieve_Document_Types).

#### Response Details

The example response shows the metadata for the relationship type configured for the specified document type `promotional__c`.

##### Relationship Fields

The relationships object includes the following fields:

Field Name

Description

`id`

The relationship `id` field.

`source_doc_id__v`

The document `id` field of the source document on which the relationship is defined.

`source_major_version__v`

The `major_version_number__v` of the source document. This only applies when the target document is bound to a specific version of the source document.

`source_minor_version__v`

The `minor_version_number__v` of the source document. This only applies when the target document is bound to a specific version of the source document.

`target_doc_id__v`

The document `id` field of the target document which is bound to the source document.

`target_major_version__v`

The `major_version_number__v` of the target document. This only applies when the source document is bound to a specific version of the target document.

`target_minor_version__v`

The `minor_version_number__v` of the target document. This only applies when the source document is bound to a specific version of the target document.

`relationship_type__v`

The relationship type (`basedon__c`, `supporting_documents__c`, `related_claims__c`, `related_pieces__c`, etc.).

`created_date__v`

The date and time when the relationship is created.

`created_by__v`

The user `id` value of the person who creates the relationship.

`source_vault_id__v`

The Vault `id` value where the source document exists. [Learn more](#Domain_Information).

##### Relationship Type Properties

Relationship types and their properties are configurable and vary from Vault to Vault.

Metadata Field

Description

`value`

The relationship type name (API key).

`label`

The relationship type label.

`sourceDocVersionSpecific`

Indicates whether or not the relationship type applies to a specific version of the source document. If `false`, the relationship type applies to all versions.

`targetDocVersionSpecific`

Indicates whether or not the relationship type applies to a specific version of the target document. If `false`, the relationship type applies to all versions.

`system`

Indicates whether or not the relationship type is a standard Vault relationship type.

`singleUse`

Indicates whether or not the relationship type can only be used once for each document.

`targetDocumentTypes`

Lists all document types which are valid target documents for the relationship type.

#### Relationships

The `source__vr` and `target__vr` relationship names can be used to perform document relationship lookup queries.

### Retrieve Document Relationships

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/866/versions/1/1/relationships
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": null,
  "errorCodes": null,
  "relationships": [
    {
      "relationship": {
        "source_doc_id__v": 886,
        "relationship_type__v": "related_pieces__c",
        "created_date__v": "2015-12-15T21:42:01.000Z",
        "id": 214,
        "target_doc_id__v": 890,
        "created_by__v": 46916
      }
    },
    {
      "relationship": {
        "source_doc_id__v": 886,
        "relationship_type__v": "related_pieces__c",
        "created_date__v": "2015-12-15T22:06:28.000Z",
        "id": 216,
        "target_doc_id__v": 884,
        "created_by__v": 46916
      }
    },
    {
      "relationship": {
        "source_doc_id__v": 886,
        "relationship_type__v": "supporting_documents__c",
        "created_date__v": "2015-12-15T21:41:10.000Z",
        "id": 213,
        "target_doc_id__v": 885,
        "created_by__v": 46916
      }
    },
    {
      "relationship": {
        "source_doc_id__v": 886,
        "relationship_type__v": "supporting_documents__c",
        "created_date__v": "2015-12-15T22:06:21.000Z",
        "id": 215,
        "target_doc_id__v": 889,
        "created_by__v": 46916
      }
    }
  ],
  "errorType": null
}
'''

Retrieve all relationships from a document.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/relationships`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

#### Response Details

On `SUCCESS`, Vault returns a list of all relationships configured on the document. In this example, document ID 886 v1.1 has reference relationships with four other documents in our Vault. This is the source document. Two of the referenced documents - `target_doc_id__v` 890 and 884 have the `related_pieces__c` relationship type. The other two referenced documents - `target_doc_id__v` 885 and 887 have the `supporting_documents__c` relationship type.

Note that when Strict Security Mode is on, if the authenticated user does not have explicit role-based _View_ permission to the document (listed in **Sharing Settings**), custom document relationships added at the subtype or classification level are not returned by this API. Without this permission, custom relationships must be added at the document type level to be returned with this API. Learn more about Strict Security Mode in [Vault Help](https://platform.veevavault.help/en/lr/3423).

### Create Single Document Relationship

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "target_doc_id__v=548" \
-d "relationship_type__v=supporting_documents__vs" \
-d "target_major_version__v=0" \
-d "target_minor_version__v=2" \
https://myvault.veevavault.com/api/v25.2/objects/documents/548/versions/0/1/relationships
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Document relationship successfully created.",
    "id": 200
}
'''

Create a new relationship on a document.

You cannot create or delete standard relationship types. Examples of standard relationship types include _Based On_ and _Original Source_. Learn about Document Relationships in [Vault Help](https://platform.veevavault.help/en/lr/21330).

POST `/api/{version}/objects/documents/{document_id}/versions/{major_version_number__v}/{minor_version_number__v}/relationships`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

`X-VaultAPI-MigrationMode`

When set to `true`, creates a document relationship in migration mode. You must have the _Document Migration_ permission to use this header. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### URI Path Parameters

Name

Description

`{document_id}`

The document `id` field value.

`{major_version_number__v}`

The document `major_version_number__v` field value.

`{minor_version_number__v}`

The document `minor_version_number__v` field value.

#### Body Parameters

Field Name

Description

`target_doc_id__v`required

The document `id` of the target document.

`relationship_type__v`required

The relationship type retrieved from the Document Relationships Metadata call above.

`target_major_version__v`conditional

The major version number of the target document to which the source document will be bound. Required for target version-specific relationships.

`target_minor_version__v`conditional

The minor version number of the target document to which the source document will be bound. Required for target version-specific relationships.

#### Response Details

On `SUCCESS`, Vault returns the ID of the newly created document relationship.

### Create Multiple Document Relationships

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Document Relationships\document_relationships.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/relationships/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 10
        },
        {
            "responseStatus": "SUCCESS",
            "id": 11
        },
    ]
}
'''

Create new relationships on multiple documents.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 1000.

You cannot create or delete standard relationship types. Examples of standard relationship types include _Based On_ and _Original Source_. Learn about Document Relationships in [Vault Help](https://platform.veevavault.help/en/lr/21330).

POST `/api/{version}/objects/documents/relationships/batch`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `text/csv`

`X-VaultAPI-MigrationMode`

When set to `true`, creates a document relationship in migration mode. You must have the _Document Migration_ permission to use this header. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### Body Parameters

Create a JSON or CSV input file. There are multiple ways to create document relationships. The following standard fields are required to create document relationships.

Name

Description

`source_doc_id__v`required

Document `id` value of the document on which the relationship is being created.

`target_doc_id__v`required

Document `id` value of the document which is being associated with the source document as a related document.

`relationship_type__v`required

The type of relationship the target document will have with the source document.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-create-doc-relationship-sample-csv-input.csv)[![Download Input File](../../images/download-json-orange.svg)](../../docs/sample-files/bulk-create-document-relationships.json)

##### Create Source Version-Specific Relationships

The following fields are required when creating a source version-specific relationship.

Name

Description

`source_major_version__v`required

The major version number of the source document.

`source_minor_version__v`required

The minor version number of the source document.

`relationship_type__v`required

The type of relationship the target document will have with the source document.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-create-source-version-specific-relationship-sample-csv-input.csv)

##### Create Target Version-Specific Relationships

The following fields are required when creating a target version-specific relationship.

Name

Description

`target_major_version__v`required

The major version number of the target document to which the source document will be bound.

`target_minor_version__v`required

The minor version number of the target document to which the source document will be bound.

`relationship_type__v`required

The type of relationship the target document will have with the source document.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-create-target-version-specific-relationship-sample-csv-input.csv)

#### Query Parameters

Name

Description

`idParam`

To create relationships based on an unique field, set idParam to a unique field name. You can use any object field which has `unique` set to `true` in the object metadata, with the exception of picklists. For example, `idParam=external_id__v`. You must then set `Content-Type` to `text/csv` and include your field name as a column.

#### Response Details

On `SUCCESS`, Vault returns the IDs of the newly created document relationships.

### Retrieve Document Relationship

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/0/relationships/200
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": null,
    "errorCodes": null,
    "relationships": [
        {
            "relationship": {
                "id": 200,
                "source_doc_id__v": 534,
                "relationship_type__v": "supporting_documents__c",
                "created_by__v": 46916,
                "created_date__v": "2015-03-20T20:44:56.000Z",
                "target_doc_id__v": 548
            }
        }
    ],
    "errorType": null
}
'''

Retrieve details of a specific document relationship.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

`{relationship_id}`

The relationship `id` field value. See [Retrieve Document Relationships](#Retrieve_Document_Relationships).

#### Response Details

Field Name

Description

`id`

Relationship ID

`source_doc_id__v`

The source document `id` field value.

`relationship_type__v`

The relationship type.

`target_doc_id__v`

The target document `id` field value.

`created_by__v`

The user `id` field value of the person who created the relationship.

`created_date__v`

The date and time when the relationship was created.

Note that when Strict Security Mode is on, if the authenticated user does not have explicit role-based _View_ permission to the document (listed in **Sharing Settings**), custom document relationships added at the subtype or classification level are not returned by this API. Without this permission, custom relationships must be added at the document type level to be returned with this API. Learn more about Strict Security Mode in [Vault Help](https://platform.veevavault.help/en/lr/3423).

### Delete Single Document Relationship

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/versions/2/0/relationships/200
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Document relationship successfully deleted.",
    "id": 200
}
'''

Delete a relationship from a document.

You cannot create or delete standard relationship types. Examples of standard relationship types include _Based On_ and _Original Source_. Learn about Document Relationships in [Vault Help](https://platform.veevavault.help/en/lr/21330).

DELETE `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

`{relationship_id}`

The relationship `id` field value. See [Retrieve Document Relationships](#Retrieve_Document_Relationships).

#### Response Details

On `SUCCESS`, Vault returns the relationship ID of the deleted relationship.

### Delete Multiple Document Relationships

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Document Relationships\document_relationships.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/relationships/batch
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 10
        },
        {
            "responseStatus": "SUCCESS",
            "id": 11
        },
        {
            "responseStatus": "FAILURE",
            "errors": [
                {
                    "type": "INVALID_DATA",
                    "message": "Error message describing why this relationship was not deleted."
                }
            ]
        }
    ]
}
'''

Delete relationships from multiple documents.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 1000.

You cannot create or delete standard relationship types. Examples of standard relationship types include _Based On_ and _Original Source_. Learn about Document Relationships in [Vault Help](https://platform.veevavault.help/en/lr/21330).

DELETE `/api/{version}/objects/documents/relationships/batch`

#### Headers

Name

Description

`Content-Type`

`application/json` (default) or `text/csv`

`Accept`

`application/json` (default) or `text/csv`

#### Body Parameters

Create a CSV or JSON input file.

Name

Description

`id`required

The ID of the relationship to delete.

#### Response Details

On `SUCCESS`, Vault returns the relationship IDs of the deleted relationships.

## Export Documents

The Export Documents API allows you to use the document `id` field to export a set of documents to your Vault’s [file staging](/docs/#FTP). For example, you could use [VQL](/vql/#sending-queries) to query the `id` of all documents from 2016 where `type__v` = `Promotional Piece`, then pass the results into the Export Documents API. This starts an asynchronous job whose status you can check with the Retrieve Document Export Results API.

You can export the following artifacts for a given document:

-   Source document
-   Renditions

You can export all versions or choose to export only the latest version.

This API does not support the following:

-   Fields
-   Attachments
-   Audit trails
-   Related documents
-   Signature Pages
-   Overlays
-   Protected renditions

To use the Export Documents API endpoints, the authenticated user’s security profile and permission set must grant the following permissions:

-   _File Staging: Access_
-   _API: Access API_

To export renditions, the authenticated user’s security profile must grant the _Document: Download Rendition_ permission.

To export source files, the authenticated user’s security profile must grant the _Document: Download Document_ permission and be in a role on the document lifecycle state that has the _Download Source_ permission.

### Export Documents

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
-H "Accept: application/json" \
--data-binary @"C:\Vault\Documents\export_documents.json" \
https://myvault.veevavault.com/api/v25.2/objects/documents/batch/actions/fileextract?source=true&renditions=false&allversions=true
'''

> Example Body

'''
[{"id": "58"}, {"id":"134"}, {"id":"122"}]
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "url": "/api/v25.2/services/jobs/36203",
    "job_id": "36203"
}
'''

Use this request to export a set of documents to your Vault’s [file staging](/docs/#FTP).

POST `/api/{version}/objects/documents/batch/actions/fileextract`

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Name

Description

`id`required

The `id` value of the document(s) to export.

#### Query Parameters

Name

Description

`source`

Optional: To exclude source files, include a query parameter `source=false`. If omitted, defaults to `true`.

`renditions`

Optional: To include renditions, include a query parameter `renditions=true`. If omitted, defaults to `false`.

`allversions`

Optional: To include all versions or latest version, include a query parameter `allversions=true`. If omitted, defaults to `false`.

#### Response Details

On `SUCCESS`, the response includes the following information:

Field Name

Description

`job_id`

The Job ID value to retrieve the [status](#Retrieve_Job_Status) and results of the document export request.

`url`

URL to retrieve the current job status of the document export request.

### Export Document Versions

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
-H "Accept: application/json" \
--data-binary @"C:\Vault\Documents\export_document_version.json" \
https://myvault.veevavault.com/api/v25.2/objects/documents/versions/batch/actions/fileextract
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "url": "/api/v25.2/services/jobs/40604",
    "job_id": "40604"
}
'''

Export a specific set of document versions to your Vault’s [file staging](/docs/#FTP). The files you export go to the u{userID} folder, regardless of your security profile. You can export a maximum of 10,000 document versions (source files) per request.

POST `/api/{version}/objects/documents/versions/batch/actions/fileextract`

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Prepare a JSON input file with the following body parameters for each document version you wish to export:

Name

Description

`id`required

ID of the document to export.

`major_version_number__v`required

The major version number of the document to export.

`minor_version_number__v`required

The minor version number of the document to export.

#### Query Parameters

Name

Description

`source`

To exclude source files, include a query parameter `source=false`. If omitted, defaults to `true`.

`renditions`

To include renditions, include a query parameter `renditions=true`. If omitted, defaults to `false`.

#### Response Details

On `SUCCESS`, the response includes the following information:

Field Name

Description

`url`

URL to retrieve the current status of the document export job.

`job_id`

The Job ID value of the document export request.

### Retrieve Document Export Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/batch/actions/fileextract/82701/results
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": 23,
            "major_version_number__v": 0,
            "minor_version_number__v": 1,
            "file": "/82701/23/0_1/New Document.png",
            "user_id__v": 88973
        }
    ]
}
'''

After submitting a request to export documents from your Vault, you can query your Vault to determine the results of the request.

Before submitting this request:

-   You must have previously requested a document export job (via the API) which is no longer active.
-   You must have a valid `job_id` value (retrieved from the document export binder request above).
-   You must be a Vault Owner, System Admin or the user who initiated the job.

GET `/api/{version}/objects/documents/batch/actions/fileextract/{jobid}/results`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{job_id}`

The `id` value of the requested export job. This is returned with the export document requests above.

#### Response Details

On `SUCCESS`, the response includes the following information:

Field Name

Description

`job_id`

The Job ID value of the document export request.

`id`

The `id` value of the exported document.

`major_version_number__v`

The major version number of the exported document.

`minor_version_number__v`

The minor version number of the exported document.

`file`

The path on the [file staging](/docs/#FTP).

`user_id__v`

The `id` value of the Vault user who initiated the document export job.

## Document Events

The Document Events are used to track the document and binder distribution events across sub-systems such as iRep, Controlled Copy, Approved Email and Engage.

### Retrieve Document Event Types and Subtypes

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/events
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "events": [
        {
            "name": "distribution__v",
            "label": "Distribution Event",
            "subtypes": [
                {
                    "name": "approved_email__v",
                    "label": "Approved Email",
                    "value": "https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/events/distribution__v/types/approved_email__v"
                },
                {
                    "name": "controlled_copy__v",
                    "label": "Controlled Copy",
                    "value": "https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/events/distribution__v/types/controlled_copy__v"
                },
                {
                    "name": "irep__v",
                    "label": "CRM",
                    "value": "https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/events/distribution__v/types/irep__v"
                },
                {
                    "name": "engage__v",
                    "label": "Engage",
                    "value": "https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/events/distribution__v/types/engage__v"
                },
                {
                    "name": "published_content__v",
                    "label": "Published Content",
                    "value": "https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/events/distribution__v/types/published_content__v"
                },
                {
                    "name": "clm__v",
                    "label": "CLM",
                    "value": "https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/events/distribution__v/types/clm__v"
                }
            ]
        }
    ]
}
'''

GET `/api/{version}/metadata/objects/documents/events`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

On `SUCCESS`, Vault returns the list of events, and event types per each event (if applicable). If the user is not permitted to access the event data, the event type is omitted from the response. In this example, one document event `distribution__v` is configured in our Vault. This “Distribution Event” is configured with six document event “subtypes”.

### Retrieve Document Event Subtype Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/events/distribution__v/types/approved_email__v
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "name": "approved_email__v",
    "label": "Approved Email",
    "properties": [
        {
            "name": "event_date__v",
            "label": "Event Date",
            "type": "DateTime",
            "queryable": true,
            "systemAttribute": true
        },
        {
            "name": "document_id__v",
            "label": "Document ID",
            "type": "ObjectReference",
            "objectType": "Documents",
            "queryable": true
        },
        {
            "name": "major_version_number__v",
            "label": "Document Major Version Number",
            "type": "Number",
            "queryable": true
        },
        {
            "name": "minor_version_number__v",
            "label": "Document Minor Version Number",
            "type": "Number",
            "queryable": true
        },
        {
            "name": "triggered_by__v",
            "label": "User ID",
            "type": "ObjectReference",
            "objectType": "Users",
            "queryable": true,
            "systemAttribute": true
        },
        {
            "name": "event_type__v",
            "label": "Event Type",
            "type": "String",
            "required": true,
            "queryable": true
        },
        {
            "name": "event_subtype__v",
            "label": "Event Subtype",
            "type": "String",
            "required": true,
            "queryable": true
        },
        {
            "name": "classification__v",
            "label": "Event Classification",
            "type": "String",
            "values": [
                {
                    "name": "distribute__v",
                    "label": "Distribute"
                },
                {
                    "name": "view__v",
                    "label": "View"
                },
                {
                    "name": "download__v",
                    "label": "Download"
                }
            ],
            "required": true,
            "queryable": true
        },
        {
            "name": "external_id__v",
            "label": "External ID",
            "type": "String",
            "required": true,
            "queryable": true
        },
        {
            "name": "user_email__v",
            "label": "User Email",
            "type": "String",
            "required": true,
            "queryable": true
        },
        {
            "name": "document_title__v",
            "label": "Document Title",
            "type": "String",
            "queryable": true,
            "systemAttribute": true
        },
        {
            "name": "document_number__v",
            "label": "Document Number",
            "type": "String",
            "queryable": true,
            "systemAttribute": true
        },
        {
            "name": "document_name__v",
            "label": "Document Name",
            "type": "String",
            "queryable": true,
            "systemAttribute": true
        }
    ]
}
'''

GET `/api/{version}/metadata/objects/documents/events/{event_type}/types/{event_subtype}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{event_type}`

The event type. For example, `distribution__v`.

`{event_subtype}`

The event subtype. For example, `approved_email__v`.

#### Response Details

On `SUCCESS`, Vault returns all metadata for the specified event subtype.

### Create Document Event

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "event_type__v=distribution__v" \
-d "event_subtype__v=approved_email__v" \
-d "classification__v=download__v" \
-d "external_id__v=1234" \
-d "user_email__v=vern@veeva.com" \
https://myvault.veevavault.com/api/v25.2/objects/documents/72/versions/0/2/events
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

POST `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/events`

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

`{major_version}`

The document `major_version_number__v` field value.

`{minor_version}`

The document `minor_version_number__v` field value.

#### Body Parameters

Name

Description

`event_type__v`required

The event type. For example, `distribution__v`.

`event_subtype__v`required

The event subtype. For example, `approved_email__v`.

`classification__v`required

The event classification. The available classifications vary based on the `event_subtype__v`.

`external_id__v`conditional

Set an external ID value on the document event. This parameter may be required depending on the document type, subtype, and classification.

Additional fields may be required depending on the document event type, subtype, and classification. Use the [Retrieve Document Event Subtype Metadata](#Retrieve_Document_Event_SubType_Metadata) endpoint to retrieve metadata for the required fields.

#### Response Details

On `SUCCESS`, Vault logs the document event.

### Retrieve Document Events

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/534/events
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "events": [
        {
            "name": "download__v",
            "label": "Approved Email Download",
            "properties": {
                "event_date__v": "2015-03-20T22:06:40.000Z",
                "document_id__v": 534,
                "major_version_number__v": 2,
                "minor_version_number__v": 0,
                "triggered_by__v": 46916,
                "event_type__v": "Distribution Event",
                "event_subtype__v": "Approved Email",
                "classification__v": "Download",
                "external_id__v": "1234",
                "user_email__v": "quinntaylor@myemail.com",
                "event_modified_by__v": 46916,
                "event_modified_date__v": "2015-03-20T22:06:40.000Z",
                "document_number__v": "REF-0059",
                "document_name__v": "WonderDrug Information"
            }
        }
    ]
}
'''

GET `/api/{version}/objects/documents/{doc_id}/events`

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

On `SUCCESS`, Vault returns the list of event objects, each containing the fields as defined by the metadata for its event type. Null and/or false valued fields are omitted from the response.

## Document Templates

Document templates allow quick creation of new documents from a configured template. When users create a new document from a template, Vault copies the template file and uses that copy as the source file for the new document. This bypasses the content upload process and allows for more consistent document creation. Document templates are associated with a specific document type.

Learn more about [Document Template types and limits in Vault Help](https://platform.veevavault.help/en/lr/5509).

### Retrieve Document Template Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/templates
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "data": [
    {
      "name": "name__v",
      "type": "String",
      "requiredness": "required",
      "max_length": 50,
      "editable": true,
      "multi_value": false
    },
    {
      "name": "label__v",
      "type": "String",
      "requiredness": "required",
      "max_length": 100,
      "editable": true,
      "multi_value": false
    },
    {
      "name": "active__v",
      "type": "Boolean",
      "requiredness": "required",
      "editable": true,
      "multi_value": false
    },
    {
      "name": "type__v",
      "type": "Component",
      "requiredness": "required",
      "editable": true,
      "multi_value": false,
      "component": "Doctype"
    },
    {
      "name": "subtype__v",
      "type": "Component",
      "requiredness": "conditional",
      "editable": true,
      "multi_value": false,
      "component": "Doctype"
    },
    {
      "name": "classification__v",
      "type": "Component",
      "requiredness": "optional",
      "editable": true,
      "multi_value": false,
      "component": "Doctype"
    },
    {
      "name": "format__v",
      "type": "String",
      "requiredness": "required",
      "max_length": 200,
      "editable": false,
      "multi_value": false
    },
    {
      "name": "size__v",
      "type": "Number",
      "requiredness": "required",
      "max_value": 9223372036854775807,
      "min_value": 0,
      "scale": 0,
      "editable": false,
      "multi_value": false
    },
    {
      "name": "created_by__v",
      "type": "Number",
      "requiredness": "required",
      "max_value": 9223372036854775807,
      "min_value": 0,
      "scale": 0,
      "editable": false,
      "multi_value": false
    },
    {
      "name": "file_uploaded_by__v",
      "type": "Number",
      "requiredness": "required",
      "max_value": 9223372036854775807,
      "min_value": 0,
      "scale": 0,
      "editable": false,
      "multi_value": false
    },
    {
      "name": "md5checksum__v",
      "type": "String",
      "requiredness": "required",
      "max_length": 100,
      "editable": false,
      "multi_value": false
    }
  ]
}
'''

Retrieve the metadata which defines the shape of document templates in your Vault.

GET `/api/{version}/metadata/objects/documents/templates`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

Field Name

Field Type

Description

Required

Editable

`name__v`

String

Document template name. Used in the API when retrieving/creating/updating templates.

True

True

`label__v`

String

Document template label. The name users see in the UI when selecting templates.

True

True

`active__v`

Boolean

Indicates whether or not the template is available for creating documents.

True

True

`type__v`

Component

The document type to which the template is associated.

True

True

`subtype__v`

Component

The document subtype to which the template is associated.

Conditional \*

True

`classification__v`

Component

The document classification to which the template is associated.

Conditional \*

True

`format__v`

String

Document template format (.doc, .pdf, etc.).

System-Managed

False

`size__v`

Number

Document template size (Kb).

System-Managed

False

`created_by__v`

Number

Vault user ID of the person who created the template.

System-Managed

False

`file_uploaded_by__v`

Number

Vault user ID of the person who uploaded the template file.

System-Managed

False

`md5checksum__v`

String

A string calculated using MD5 algorithm that can be used to uniquely identify the source file.

System-Managed

False

\* The document subtype and classification fields are “conditional” in that they are only required if the template exists at the document subtype or classification level.

### Retrieve Document Template Collection

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/templates
'''

> Response

'''
{
   "responseStatus":"SUCCESS",
   "data":[
      {
         "name__v":"claim_document_template__c",
         "label__v":"Claim Document Template",
         "active__v":true,
         "type__v":"claim__c",
         "format__v": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
         "size__v": 2781904,
         "created_by__v": 12021,
         "file_uploaded_by__v": 12021,
         "md5checksum__v": 98238947109287333
      },
      {
         "name__v":"clinical_study_document_template__c",
         "label__v":"Clinical Study Document Template",
         "active__v":true,
         "type__v":"reference_document__c",
         "subtype__v":"clinical_study__c",
         "format__v": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
         "size__v": 15776,
         "created_by__v": 12021,
         "file_uploaded_by__v": 12021,
         "md5checksum__v": 75886214401031117
      },
      {
         "name__v":"promo_ad_print_document_template__c",
         "label__v":"Promo Ad Print Document Template",
         "active__v":true,
         "type__v":"promotional_piece__c",
         "subtype__v":"advertisement__c",
         "classification__v":"print__c",
         "format__v": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
         "size__v": 82923,
         "created_by__v": 12021,
         "file_uploaded_by__v": 12021,
         "md5checksum__v": 52478042594365555
      }
   ]
}
'''

Retrieve all document templates.

GET `/api/{version}/objects/documents/templates`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

The response lists all document templates which have been added to the Vault. Shown above, three document templates exist in our Vault:

-   The first `claim_document_template__c` exists at the document type level. It is intended for use with new documents of the `claim__c` type.
-   The second `clinical_study_document_template__c` exists at the document subtype level. It is intended for use with new documents of the `clinical_study__c` subtype.
-   The third `promo_ad_print_document_template__c` exists at the document classification level. It is intended for use with new documents of the `print__c` classification.

For information about the document template metadata, refer to the “Retrieve Document Template Attributes” response below.

### Retrieve Document Template Attributes

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/templates/promo_ad_print_document_template__c
'''

> Response

'''
{
   "responseStatus":"SUCCESS",
   "data":[
      {
         "name__v":"promo_ad_print_document_template__c",
         "label__v":"Promo Ad Print Document Template",
         "active__v":true,
         "type__v":"promotional_piece__c",
         "subtype__v":"advertisement__c",
         "classification__v":"print__c",
         "format__v": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
         "size__v": 82923,
         "created_by__v": 12021,
         "file_uploaded_by__v": 12021,
         "md5checksum__v": 52478042594365555
      }
   ]
}
'''

Retrieve the attributes from a document template.

GET `/api/{version}/objects/documents/templates/{template_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{template_name}`

The document template `name__v` field value.

#### Response Details

The response lists all attributes configured on a specific document template in the Vault. Shown above are the attributes configured on the specified template:

Field Name

Description

`name__v`

Name of the document template. This value is not displayed to end users in the UI. It is seen by Admins and used in the API.

`label__v`

Label of the document template. When users in the UI create documents from templates, they see this value in the list of available templates.

`type__v`

Vault document type to which the template is associated.

`subtype__v`

Vault document subtype to which the template is associated. This field is only displayed if the template exists at the document subtype or classification level.

`classification__v`

Vault document classification to which the template is associated. This field is only displayed if the template exists at the document classification level. The template shown in this response is configured for use with documents of the `print__c` classification.

`format__v`

File format of the document template.

`size__v`

Size of the document template (Kb).

`created_by__v`

Vault user ID of the person who created the document template.

`file_uploaded_by__v`

Vault user ID of the person who uploaded the document template.

`md5checksum__v`

A string calculated using MD5 algorithm that can be used to uniquely identify the source file.

### Download Document Template File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/templates/claim_document_template__c/file
'''

> Response

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment;filename="claim_document_template__c.pdf"
'''

Download the file of a specific document template.

GET `/api/{version}/objects/documents/templates/{template_name}/file`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml` For this request, the `Accept` header controls only the error response. On `SUCCESS`, the response is a file stream (download).

#### URI Path Parameters

Name

Description

`{template_name}`

The document template `name__v` field value.

#### Response Details

On `SUCCESS`, Vault retrieves the document template file.

The HTTP Response Header `Content-Type` is set to `application/octet-stream`. The HTTP Response Header `Content-Disposition` contains a filename component which can be used when naming the local file. When retrieving templates with very small file size, the HTTP Response Header `Content-Length` is set to the size of the template file. Note that for template downloads of larger file sizes, the `Transfer-Encoding` method is set to `chunked` and the `Content-Length` is not displayed.

### Create Single Document Template

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-H "Accept: text/csv" \
-F "file=Promo Ad Template.docx" \
-F "label__v=Promo Ad Template" \
-F "type__v=promotional_piece__c" \
-F "subtype__v=advertisement__c" \
-F "classification__v=print__c" \
-F "active__v=true" \
https://myvault.veevavault.com/api/v25.2/objects/documents/templates
'''

> Response

'''
responseStatus,name,errors
SUCCESS,promo_ad_template__c,
'''

Create one basic document template. To create multiple document templates, see [Create Multiple Document Templates](#Bulk_Create_Document_Templates).

You cannot create templates if your Vault exceeds template limits. Learn more about [document template limits in Vault Help](https://platform.veevavault.help/en/lr/5509/#limits).

POST `/api/{version}/objects/documents/templates`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters: Basic Document Template

When creating basic document templates, the following fields are required in all Vaults:

Name

Description

`name__v`optional

The name of the new document template. If not included, Vault will use the specified `label__v` value to generate a value for the `name__v` field.

`label__v`required

The label of the new document template. This is the name users will see among the available templates in the UI.

`type__v`required

The name of the document type to which the template will be associated.

`subtype__v`optional

The name of the document subtype to which the template will be associated. This is only required if associating the template with a document subtype.

`classification__v`optional

The name of the document classification to which the template will be associated. This is only required if associating the template with a document classification.

`active__v`required

Set to true or false to indicate whether or not the new document template should be set to active, i.e., available for selection when creating a document.

`file`required

The filepath of the file for this document template. Maximum allowed size is 4GB.

### Create Multiple Document Templates

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
--data-binary @"C:\Vault\Templates\add_document_templates.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/templates
'''

> Response

'''
{
   "responseStatus":"SUCCESS",
   "data":[
      {
         "responseStatus":"SUCCESS",
         "name":"site_document_template__c"
      },
      {
         "responseStatus":"SUCCESS",
         "name":"tmf_document_template__c"
      },
      {
         "responseStatus":"SUCCESS",
         "name":"trial_protocol_document_template__c"
      },
      {
         "responseStatus":"FAILURE",
         "errors":[
            {
               "type":"INVALID_DATA",
               "message":"Error message describing why this template was not created."
            }
         ]
      }
   ]
}
'''

Create up to 500 document templates. You cannot create templates if your Vault exceeds template limits. Learn more about [document template limits in Vault Help](https://platform.veevavault.help/en/lr/5509/#limits).

POST `/api/{version}/objects/documents/templates`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters: Basic Document Templates

To create basic document templates, create a CSV or JSON input file with the following fields:

Name

Description

`name__v`optional

The name of the new document template. If not included, Vault will use the specified `label__v` value to generate a value for the `name__v` field.

`label__v`required

The label of the new document template. This is the name users will see among the available binder templates in the UI.

`type__v`required

The name of the document type to which the template will be associated.

`subtype__v`optional

The name of the document subtype to which the template will be associated.

`classification__v`optional

The name of the document classification to which the template will be associated.

`active__v`required

Set to `true` or `false` to indicate whether or not the new document template should be set to active, i.e., available for selection when creating a document.

`file`required

The filepath of the file for this document template, from file staging. Maximum allowed size is 4GB.

[![Download Input File](../../images/download-json-orange.svg)](../../docs/sample-files/bulk-create-document-templates.json)

#### Body Parameters: Controlled Document Templates

To create controlled document templates, create a CSV or JSON input file with the following fields:

Name

Description

`name__v`optional

The name of the new document template. If not included, Vault will use the specified `label__v` value to generate a value for the `name__v` field.

`label__v`required

The label of the new document template. This is the name users will see among the available binder templates in the UI.

`active__v`required

Set to `true` or `false` to indicate whether or not the new document template should be set to active, i.e., available for selection when creating a document.

`is_controlled__v`required

Set to `true` to indicate this template is a controlled document template.

`template_doc_id__v`required

The document `id` value to use as the Template Document for this controlled document template. Learn more about [setting up valid Template Documents in Vault Help](https://platform.veevavault.help/en/lr/46025).

#### Example CSV Input: Basic Document Templates

`file`

`name__v`

`label__v`

`type__v`

`subtype__v`

`classification__v`

`active__v`

templates/doc\_template\_1.doc

site\_document\_template\_\_c

SMF Template

site\_master\_file\_\_v

true

templates/doc\_template\_2.doc

TMF Document Template

trial\_master\_file\_\_v

true

templates/doc\_template\_3.doc

Trial Protocol Document Template

central\_trial\_documents\_\_vs

trial\_documents\_\_vs

protocol\_\_vs

true

templates/doc\_template\_4.doc

Clinical Study Report Document Template

central\_trial\_documents\_\_vs

reports\_\_vs

clinical\_study\_report\_\_vs

false

In this example input, we’re creating four new document templates in our Vault:

-   We’ve included the `file` parameter with the path/name of four document template source files located in the “templates” directory of our Vault’s staging server.
-   We’ve only specified the `name__v` value for the first template and given it a different `label__v` value. The other templates will inherit their `name__v` values from the `label__v` values.
-   We’ve specified the document type, subtype, and classification to which each document template will be associated.

### Update Single Document Template

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Accept: application/json" \
-d "name__v=promo_ad_web_document_template__c" \
-d "label__v=Promo Ad Web Document Template" \
-d "active__v=true" \
https://myvault.veevavault.com/api/v25.2/objects/documents/templates/promo_ad_print_document_template__c
'''

> Response

'''
responseStatus,name,errors
SUCCESS,promo_ad_web_document_template__c,
'''

Update a single document template in your Vault.

PUT `/api/{version}/objects/documents/templates/{template_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{template_name}`

The document template `name__v` field value.

#### Body Parameters

You can update the following fields on document templates:

Field Name

Description

`name__v`optional

The name of an existing document template. This is required.

`new_name`optional

Change the name of an existing document template.

`label__v`optional

Change the label of an existing document template. This is the name users will see among the available document templates in the UI.

`active__v`optional

Set to `true` or `false` to indicate whether or not the document template should be set to active, i.e., available for selection when creating a document.

#### Convert Basic Document Template to Controlled Document Template

To convert a basic document template to a controlled document template, specify the Template Document. Vault will automatically update `is_controlled__v` on this template to `true`.

It is not possible to convert a controlled document template into a basic document template.

Field Name

Description

`template_doc_id__v`optional

The document `id` value to use as the Template Document for this controlled document template. Learn more about [setting up valid Template Documents in Vault Help](https://platform.veevavault.help/en/lr/46025).

### Update Multiple Document Templates

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
--data-binary @"C:\Vault\Templates\update_document_templates.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/templates
'''

> Response

'''
{
   "responseStatus":"SUCCESS",
   "data":[
      {
         "responseStatus":"SUCCESS",
         "name":"claim_document_template__c"
      },
      {
         "responseStatus":"SUCCESS",
         "name":"clinical_study_document_template__c"
      },
      {
         "responseStatus":"FAILURE",
         "errors":[
            {
               "type":"INVALID_DATA",
               "message":"Error message describing why this template was not created."
            }
         ]
      }
   ]
}
'''

Update up to 500 document templates in your Vault.

PUT `/api/{version}/objects/documents/templates`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

To update document templates, prepare a CSV or JSON input file. You can update the following fields on document templates:

Name

Description

`name__v`required

Include the name of an existing document template.

`new_name`optional

Change the name of an existing document template.

`label__v`optional

Change the label of an existing document template. This is the name users will see among the available binder templates in the UI.

`active__v`optional

Set to true or false to indicate whether or not the document templates should be set to active, i.e., available for selection when creating a document.

[![Download Input File](../../images/download-json-orange.svg)](../../docs/sample-files/bulk-update-document-templates.json)

#### Convert Basic Document Template to Controlled Document Template

To convert a basic document template to a controlled document template, specify the Template Document. Vault will automatically update `is_controlled__v` on this template to `true`.

It is not possible to convert a controlled document template into a basic document template.

Field Name

Description

`template_doc_id__v`optional

The document `id` value to use as the Template Document for this controlled document template. Learn more about [setting up valid Template Documents in Vault Help](https://platform.veevavault.help/en/lr/46025).

### Delete Basic Document Template

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/templates/promo_ad_web_document_template__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Delete a basic document template from your Vault. You cannot delete controlled document templates. Learn more about [controlled template deletion in Vault Help](https://platform.veevavault.help/en/lr/46018#deleting-controlled-document-templates).

DELETE `/api/{version}/objects/documents/templates/{template_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{template_name}`

The document template `name__v` field value.

## Document Signatures

Retrieve all metadata for signatures on documents and archived documents.

### Retrieve Document Signature Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/query/documents/relationships/document_signature__sysr
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "properties": {
    "name": "document_signature__sysr",
    "fields": [
      {
        "name": "id",
        "type": "id"
      },
      {
        "name": "signature_user__sys",
        "type": "id"
      },
      {
        "name": "signed_document__sys",
        "type": "id"
      },
      {
        "name": "signed_document_major_version__sys",
        "type": "Number"
      },
      {
        "name": "signed_document_minor_version__sys",
        "type": "Number"
      },
      {
        "name": "signature_time__sys",
        "type": "DateTime"
      },
      {
        "name": "manifest_signature__sys",
        "type": "Boolean"
      },
      {
        "name": "task__sys",
        "type": "String"
      },
      {
        "name": "task_label__sys",
        "type": "String"
      },
      {
        "name": "workflow_label__sys",
        "type": "String"
      },
      {
        "name": "workflow_name__sys",
        "type": "String"
      },
      {
        "name": "signature_meaning__sys",
        "type": "String"
      },
      {
        "name": "verdict_name__sys",
        "type": "String"
      },
      {
        "name": "verdict__sys",
        "type": "String"
      },
      {
        "name": "delegate_user__sys",
        "type": "id"
      },
      {
        "name": "task_description__sys",
        "type": "String"
      },
      {
        "name": "workflow__sys",
        "type": "id"
      },
      {
        "name": "signature_name__sys",
        "type": "String"
      },
      {
        "name": "signature_title__sys",
        "type": "String"
      },
      {
        "name": "delegate_title__sys",
        "type": "String"
      },
      {
        "name": "delegate_name__sys",
        "type": "String"
      }
    ]
  }
}

'''

Retrieve all metadata for signatures on documents. Learn more about [signature pages in Vault Help](https://platform.veevavault.help/en/lr/40560).

GET `/api/{version}/metadata/query/documents/relationships/document_signature__sysr`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

On `SUCCESS`, Vault returns all metadata for document signatures.

### Retrieve Archived Document Signature Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/query/archived_documents/relationships/document_signature__sysr
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "properties": {
    "name": "document_signature__sysr",
    "fields": [
      {
        "name": "id",
        "type": "id"
      },
      {
        "name": "signature_user__sys",
        "type": "id"
      },
      {
        "name": "signed_document__sys",
        "type": "id"
      },
      {
        "name": "signed_document_major_version__sys",
        "type": "Number"
      },
      {
        "name": "signed_document_minor_version__sys",
        "type": "Number"
      },
      {
        "name": "signature_time__sys",
        "type": "DateTime"
      },
      {
        "name": "manifest_signature__sys",
        "type": "Boolean"
      },
      {
        "name": "task__sys",
        "type": "String"
      },
      {
        "name": "task_label__sys",
        "type": "String"
      },
      {
        "name": "workflow_label__sys",
        "type": "String"
      },
      {
        "name": "workflow_name__sys",
        "type": "String"
      },
      {
        "name": "signature_meaning__sys",
        "type": "String"
      },
      {
        "name": "verdict_name__sys",
        "type": "String"
      },
      {
        "name": "verdict__sys",
        "type": "String"
      },
      {
        "name": "delegate_user__sys",
        "type": "id"
      },
      {
        "name": "task_description__sys",
        "type": "String"
      },
      {
        "name": "workflow__sys",
        "type": "id"
      },
      {
        "name": "signature_name__sys",
        "type": "String"
      },
      {
        "name": "signature_title__sys",
        "type": "String"
      },
      {
        "name": "delegate_title__sys",
        "type": "String"
      },
      {
        "name": "delegate_name__sys",
        "type": "String"
      }
    ]
  }
}
'''

Retrieve all metadata for signatures on archived documents. Learn more about [signature pages in Vault Help](https://platform.veevavault.help/en/lr/40560).

GET `/api/{version}/metadata/query/archived_documents/relationships/document_signature__sysr`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

On `SUCCESS`, Vault returns all metadata for archived document signatures.

## Document Tokens

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "docIds=101,102,103,104" \
-d "expiryDateOffset=90" \
-d "downloadOption=PDF" \
-d "channel=00W000000000301" \
https://myvault.veevavault.com/api/v25.2/objects/documents/tokens
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "tokens": [
        {
            "document_id__v": 101,
            "token__v": "3003-cb6e5c3b-4df9-411c-abc2-6e7ae120ede7"
        }
        {
            "document_id__v": 102,
            "token__v": "3003-1174154c-ac8e-4eb9-b453-2855de273bec"
        },
        {
            "document_id__v": 103,
            "token__v": "3003-51ca652c-36d9-425f-894f-fc2f42601fa9"
        },
        {
            "document_id__v": 104,
            "errorType": "OPERATION_NOT_ALLOWED",
            "errors": [
                {
                    "type": "INVALID_DOCUMENT",
                    "message": "Document not found [104]."
                }
            ]
        }
    ]
}
'''

The Vault Document Tokens API allows you to generate document access tokens needed by the external viewer to view documents outside of Vault. [Learn more.](http://developer.veevavault.com/docs/vault-document-external-viewer/)

POST `/api/{version}/objects/documents/tokens`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Name

Description

`docIds`required

Include the `docIds` request parameter with a comma-separated string of document `id` values. This will generate tokens for each document. For example: `docIds=101,102,103,104`

`expiryDateOffset`optional

Include the `expiryDateOffset` request parameter set to the number of days after which the tokens will expire and the documents will no longer be available in the viewer. If not specified, the tokens will expire after 10 years by default.

`downloadOption`optional

Include the `downloadOption` request parameter set to `PDF`, `source`, `both`, or `none`. These allow users viewing the document to be able to download a PDF version or source version (Word™, PowerPoint™, etc.) of the document. If not specified, the download options default to those set on each document.

`channel`optional

Include the `channel` request parameter set to the website object record `id` value that corresponds to the distribution channel where the document is being made available. If no website record is specified, Vault will assume the request is for Approved Email.

`tokenGroup`optional

Include the `tokenGroup` request parameter to group together generated tokens for multiple documents in order to display the documents being referenced in the same viewer. This value accepts strings of alphanumeric characters (a-z, A-Z, 0-9, and single consecutive underscores) up to 255 characters in length. The token that is passed as a URL parameter to the External Viewer is the primary token and the document it references will be displayed normally. However, any additional documents that have tokens generated with the same case-sensitive `tokenGroup` string will be displayed in a sidebar of the viewer. The order of documents in the sidebar depends on the order in which the tokens are generated. If multiple tokens are generated with one request, the documents will be ordered top-to-bottom based on the order they are passed to the `docIds` parameter. For example: If passing the parameters `docIds=101,102,103,104` and `tokenGroup=group_1` with the request, the top-to-bottom order in the sidebar will be documents 101, 102, 103, 104. If a new request is then made with the parameters `docIds=105` and `tokenGroup=group_1`, document 105 will be added below document 104 in the previous list.

`steadyState`optional

If set to `true`, Vault generates a token for the latest steady state version of a document. If you do not have _View_ permission, or if a steady-state version does not exist, Vault returns an `INVALID_STATE` error. If omitted, the default value is `false`, and Vault generates a token for the latest version, regardless of state.

#### Response Details

In the example above, tokens are generated for the first three documents. The fourth document could not be found. This indicates either an incorrect document `id` or that the specified document is a binder.
