<!-- 
VaultAPIDocs Section: # Binders
Original Line Number: 13382
Generated: August 30, 2025
Part 6 of 38
-->

# Binders

Binders organize documents, sections, and other binders into a hierarchical structure that is useful for packaging related documents together for easier management or eventual publishing. Binders are a kind of document and many of the Document API calls, such as metadata, retrieving and setting properties, security, etc. can be used directly on a binder and will not be replicated here. All API calls related to files and renditions will not work on a binder object. Binders do have unique APIs that allow for interrogating and manipulating the binder structure.

Learn about [Documents & Binders](https://platform.veevavault.help/en/lr/21581) in Vault Help.

## Retrieve Binders

### Retrieve All Binders

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "size": 77,
  "start": 0,
  "limit": 200,
  "documents": [
    {
      "document": {
        "id": 101,
        "binder__v": true,
        "coordinator__v": {
          "groups": [],
          "users": [
            25525          ]
        },
        "version_creation_date__v": "2015-03-11T22:04:44.725Z",
        "major_version_number__v": 0,
        "status__v": "Planned",
        "product__v": [
          "1357662840171"
        ],
        "version_created_by__v": 25524,
        "country__v": [],
        "document_number__v": "VV-00127",
        "minor_version_number__v": 1,
        "lifecycle__v": "General Lifecycle",
        "crosslink__v": false,
        "name__v": "CholeCap Presentation"
      }
    }
  ]
}
'''

In Vault, binders are just another kind of document. Therefore, to retrieve a list of all binders in your Vault, you must use the same API endpoint to retrieve documents. By searching the response, you can distinguish binders from documents by using the document field `binder__v` set to `true` or `false`. See the response details below. Note that nested binders (a binder contained within another binder) are not retrieved.

This endpoint does not retrieve binder sections, which means the response will not include binders within other binder sections. To retrieve all metadata configured on a binder, including sections, you must use the binder IDs retrieved from this request in the [Retrieve Binder](#Retrieve_Binder) endpoint.

Alternatively, you can use VQL to find just binders `SELECT id FROM binders`. See [VQL documentation](/vql/#Query_Syntax_Structure) for details.

GET `/api/{version}/objects/documents`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

The example response shows the field names and values configured on two separate documents in our Vault:

-   The first record retrieved `"id": 101` has `"binder__v": true`. This document is a binder.
-   The second record retrieved `"id": 102` has `"binder__v": false`. This document is a regular document.

### Retrieve Binder

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/29?depth=all
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "document": {
    "id": 29,
    "binder__v": true,
    "coordinator__v": {
      "groups": [],
      "users": [
        63606
      ]
    },
    "owner__v": {
      "groups": [],
      "users": [
        46916
      ]
    },
    "approver__v": {
      "groups": [],
      "users": [
        25524
      ]
    },
    "reviewer__v": {
      "groups": [],
      "users": [
        60145
      ]
    },
    "distribution_contacts__v": {
      "groups": [],
      "users": []
    },
    "viewer__v": {
      "groups": [
        3
      ],
      "users": []
    },
    "consumer__v": {
      "groups": [],
      "users": [
        60145
      ]
    },
    "editor__v": {
      "groups": [],
      "users": [
        25496
      ]
    },
    "version_creation_date__v": "2016-03-09T21:55:22.000Z",
    "major_version_number__v": 0,
    "lifecycle__v": "Field Medical",
    "subtype__v": "Training Materials",
    "annotations_links__v": 0,
    "annotations_notes__v": 0,
    "name__v": "VeevaProm Info Binder",
    "locked__v": false,
    "annotations_all__v": 0,
    "status__v": "Draft",
    "type__v": "Field Medical",
    "description__v": "",
    "annotations_unresolved__v": 0,
    "last_modified_by__v": 46916,
    "product__v": [
      "00P000000000102"
    ],
    "version_created_by__v": 46916,
    "document_creation_date__v": "2016-03-09T20:42:18.692Z",
    "country__v": [
      "00C000000000109"
    ],
    "annotations_anchors__v": 0,
    "document_number__v": "VV-MED-00029",
    "annotations_resolved__v": 0,
    "annotations_lines__v": 0,
    "version_modified_date__v": "2016-03-09T21:55:22.000Z",
    "created_by__v": 46916,
    "minor_version_number__v": 2
  },
  "versions": [
    {
      "number": "0.1",
      "value": "https://medcomms-veevapharm.veevavault.com/api/v25.2/objects/binders/29/versions/0/1"
    },
    {
      "number": "0.2",
      "value": "https://medcomms-veevapharm.veevavault.com/api/v25.2/objects/binders/29/versions/0/2"
    }
  ],
  "binder": {
    "nodes": [
      {
        "properties": {
          "document_id__v": 7,
          "name__v": "VeevaProm Information",
          "order__v": 0,
          "type__v": "document",
          "id": "1457556160448:810987462",
          "parent_id__v": "rootNode"
        }
      },
      {
        "properties": {
          "document_id__v": 2,
          "name__v": "VeevaProm Consumer Info",
          "order__v": 300,
          "type__v": "document",
          "id": "1457559259279:-602158059",
          "parent_id__v": "rootNode"
        }
      },
      {
        "properties": {
          "document_id__v": 5,
          "name__v": "VeevaProm Brochure",
          "order__v": 301,
          "type__v": "document",
          "id": "1457556176044:-743019200",
          "parent_id__v": "rootNode"
        }
      },
      {
        "properties": {
          "section_number__v": null,
          "name__v": "First Section Folder",
          "order__v": 401,
          "type__v": "section",
          "id": "1457560333810:-909497856",
          "parent_id__v": "rootNode"
        },
        "nodes": [
          {
            "properties": {
              "document_id__v": 28,
              "name__v": "Alterin Prescribing Information",
              "order__v": 0,
              "type__v": "document",
              "id": "1457560375017:-1371674753",
              "parent_id__v": "1457560333810:-909497856"
            }
          },
          {
            "properties": {
              "document_id__v": 26,
              "name__v": "Alterin Health Notes",
              "order__v": 100,
              "type__v": "document",
              "id": "1457560377637:-2013602559",
              "parent_id__v": "1457560333810:-909497856"
            }
          },
          {
            "properties": {
              "document_id__v": 27,
              "name__v": "Alterin Information Packet",
              "order__v": 200,
              "type__v": "document",
              "id": "1457560379150:954844502",
              "parent_id__v": "1457560333810:-909497856"
            }
          }
        ]
      },
      {
        "properties": {
          "section_number__v": null,
          "name__v": "Second Section Folder",
          "order__v": 501,
          "type__v": "section",
          "id": "1457560348267:1179700878",
          "parent_id__v": "rootNode"
        },
        "nodes": [
          {
            "properties": {
              "document_id__v": 24,
              "name__v": "Nyaxa Information Packet",
              "order__v": 0,
              "type__v": "document",
              "id": "1457560406595:-2060980086",
              "parent_id__v": "1457560348267:1179700878"
            }
          },
          {
            "properties": {
              "document_id__v": 23,
              "name__v": "Nyaxa and Your Health",
              "order__v": 100,
              "type__v": "document",
              "id": "1457560409271:-1499449603",
              "parent_id__v": "1457560348267:1179700878"
            }
          },
          {
            "properties": {
              "document_id__v": 25,
              "name__v": "Nyaxa Prescribing Information",
              "order__v": 200,
              "type__v": "document",
              "id": "1457560412997:-1622511549",
              "parent_id__v": "1457560348267:1179700878"
            }
          }
        ]
      }
    ]
  }
}
'''

-   Use this endpoint to retrieve all fields and values configured on a specific binder in you Vault (using the binder ID).
-   The response includes the “first level” of the binder section node structure.
-   To retrieve additional levels in the binder section node structure, use one of the `depth` parameters described below.
-   For binders with unbound documents, the response includes versions based on binder display options for unbound documents set in the UI. Learn more about Document Type Settings in [Vault Help](https://platform.veevavault.help/en/lr/618).

GET `/api/{version}/objects/binders/{binder_id}`

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

Retrieve all fields and values configured on a specific binder in you Vault. By default, the response only includes the first level (root) of the binder structure. To retrieve all levels, use one of the `depth` parameters described below.

#### Query Parameters

Name

Description

`depth`

To retrieve all information in all levels of the binder, set this to `all`. By default, only one level is returned.

#### Response Details

The example response shows fields and values configured on binder `"id": 29`, including the first level of binder nodes in the binder’s structure. In this first level, there is one document `"id": 567` and two sections `"section_number__v": "1"` and `"section_number__v": "2"`. The second example below, uses the `depth=all` request parameter to retrieve all levels of binder nodes in the binder’s structure.

On `SUCCESS`, Vault retrieves the fields and components of the binder in a hierarchical structure clearly showing the parent-child relationships for each item and maintaining the specific order of the objects in each level.

#### Response Details

For each node in a binder, the API returns the following fields:

Field Name

Description

`nodes [n]`

List of all nodes (documents and sections) at each level in the binder.

`properties [n]`

List of all properties associated with each document or section node.

`order__v`

Order of the node (document or section) within the binder or within the binder section. **Note: There is a known issue affecting this parameter. It may not accurately reflect order.**

`section_number__v`

Optional number which can be added to each section.

`type`

Type of node (document or section).

`document_id__v`

The document ID of the document in the binder. This is the same as the document’s actual document `id`

`id`

The document ID or section ID specific to the binder. For documents, this is different from the document’s actual document `id`.

`parent_id__v`

Section ID of the parent node, e.g., “rootNode”.

`name__v`

Name of the document or section. For sections, this is the name of the “subfolder” seen in the binder hierarchy in the UI.

`major_version_number__v`

If the document binding rule is “specific”, this is major version number of the document.

`minor_version_number__v`

If the document binding rule is “specific”, this is minor version number of the document.

### Retrieve All Binder Versions

Retrieve all versions of a binder.

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/29/versions
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "versions": [
    {
      "number": "0.1",
      "value": "https://medcomms-veevapharm.veevavault.com/api/v25.2/objects/binders/29/versions/0/1"
    },
    {
      "number": "0.2",
      "value": "https://medcomms-veevapharm.veevavault.com/api/v25.2/objects/binders/29/versions/0/2"
    }
  ]
}
'''

GET `/api/{version}/objects/binders/{binder_id}/versions`

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

Binders have versions just like regular documents. On `SUCCESS`, Vault returns a list of the available versions for the specified binder.

### Retrieve Binder Version

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/302/versions/0/1
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "document": {
        "id": 302,
        "version_id": "302_0_1",
        "binder__v": true,
        "owner__v": {
            "groups": [],
            "users": [
                1008906
            ]
        },
        "editor__v": {
            "groups": [],
            "users": []
        },
        "reviewer__v": {
            "groups": [],
            "users": []
        },
        "viewer__v": {
            "groups": [
                1394917493401
            ],
            "users": []
        },
        "coordinator__v": {
            "groups": [],
            "users": []
        },
        "approver__v": {
            "groups": [],
            "users": []
        },
        "consumer__v": {
            "groups": [],
            "users": []
        },
        "distribution_contacts__v": {
            "groups": [],
            "users": []
        },
        "version_creation_date__v": "2024-03-29T15:10:26.574Z",
        "major_version_number__v": 0,
        "annotations_links__v": 0,
        "bookmarks_edited__sys": "false",
        "annotations_all__v": 0,
        "global_version_id__sys": "1000660_302_650",
        "annotations_permalink__v": 0,
        "status__v": "Proposed",
        "annotations_auto__v": 0,
        "product__v": [
            "cholecap"
        ],
        "version_created_by__v": 1008906,
        "annotations_anchors__v": 0,
        "document_number__v": "VV-00033",
        "minor_version_number__v": 1,
        "lifecycle__v": "Campaign Document Lifecycle",
        "global_id__sys": "1000660_302",
        "latest_version__v": true,
        "crosslink__v": false,
        "annotations_notes__v": 0,
        "annotations_suggested__v": 0,
        "locked__v": false,
        "name__v": "Cholecap Campaign Toolkit",
        "type__v": "Campaign Document",
        "annotations_unresolved__v": 0,
        "last_modified_by__v": 1006595,
        "annotations_approved__v": 0,
        "document_creation_date__v": "2024-03-29T15:10:26.574Z",
        "archive__v": false,
        "annotations_resolved__v": 0,
        "annotations_lines__v": 0,
        "version_modified_date__v": "2024-10-23T15:52:24.000Z",
        "created_by__v": 1008906,
        "annotations_claim__v": 0
    },
    "versions": [
        {
            "number": "0.1",
            "value": "https://techpubs.vaultdev.com/api/v25.2/objects/binders/302/versions/0/1"
        }
    ],
    "binder": {
        "nodes": [
            {
                "properties": {
                    "section_number__v": "",
                    "name__v": "Component Items",
                    "order__v": 100,
                    "type__v": "section",
                    "id": "1711725042042:-1375762845",
                    "parent_id__v": "rootNode"
                }
            },
            {
                "properties": {
                    "section_number__v": "",
                    "name__v": "TV Commercials",
                    "order__v": 200,
                    "type__v": "section",
                    "id": "1711725061829:-1997055985",
                    "parent_id__v": "rootNode"
                }
            },
            {
                "properties": {
                    "section_number__v": "",
                    "name__v": "Print Templates",
                    "order__v": 300,
                    "type__v": "section",
                    "id": "1711725049747:736173623",
                    "parent_id__v": "rootNode"
                }
            },
            {
                "properties": {
                    "document_id__v": 601,
                    "name__v": "Cholecap Prescribing Information (PI)-WM",
                    "order__v": 950,
                    "type__v": "document",
                    "id": "1712324813123:1222973257",
                    "parent_id__v": "rootNode"
                }
            },
            {
                "properties": {
                    "document_id__v": 502,
                    "name__v": "Role of CholeCap (veevastatin) in Dyslipidemia- A Clinical Study",
                    "order__v": 1050,
                    "type__v": "document",
                    "id": "1712324748962:-340772953",
                    "parent_id__v": "rootNode"
                }
            },
            {
                "properties": {
                    "document_id__v": 1301,
                    "name__v": "Additional Promotional Materials",
                    "order__v": 1150,
                    "type__v": "binder",
                    "id": "1729698491236:1735240281",
                    "minor_version_number__v": 1,
                    "parent_id__v": "rootNode",
                    "major_version_number__v": 0
                }
            }
        ]
    }
}
'''

Retrieve the fields and values configured on a specific version of a specific binder.

GET `/api/{version}/objects/binders/{binder_id}/versions/(major_version}/{minor_version}`

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

`{major_version}`

The binder `major_version_number__v` field value.

`{minor_version}`

The binder `minor_version_number__v` field value.

#### Response Details

On `SUCCESS`, Vault returns the binder contents, fields, and values configured on the binder, including the first level of nodes in the binder’s structure. If a child node has `"type__v": "binder"` and that binder is bound to a specific version, the response includes the major and minor versions.

For binders with unbound documents, the response includes versions based on binder display options for unbound documents set in the UI. Learn more about [Document Type Settings in Vault Help](https://platform.veevavault.help/en/lr/618).

## Create Binders

### Create Binder

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "name__v=WonderDrug Compliance Package" \
-d "type__v=Compliance Package" \
-d "subtype__v=Professional" \
-d "lifecycle__v=Binder Lifecycle" \
-d "product__v=1357662840293" \
-d "major_version_number__v=0" \
-d "minor_version_number__v=1" \
https://myvault.veevavault.com/api/v25.2/objects/binders
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Successfully created binder.",
    "id": 563
}
'''

Use this request to create a new binder in your Vault. Learn about [Creating Binders](https://platform.veevavault.help/en/lr/15089) in Vault Help.

POST `/api/{version}/objects/binders`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

All required binder (document) fields must be included in the request. When creating a binder, no file is included in the request.

Name

Description

`async`

When creating a binder, the binder metadata is indexed synchronously by default. To process the indexing asynchronously, include a query parameter `async` set to `true` (`objects/binders?async=true`). This helps speed up the response time from Vault when processing large amounts of data.

### Create Binder from Template

> Request

Since we’re creating a new binder with the document type “Compliance Package” and subtype “Professional”, we need to find the available templates in the type/subtype metadata:

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/documents/types/compliance_package__v/subtypes/professional__v
'''

> Response

'''
{
    "templates": [
        {
            "label": "Compliance Package Template",
            "name": "compliance_package__v",
            "kind": "binder",
            "definedIn": "compliance_package__v",
            "definedInType": "type"
        },
        {
            "label": "eCTD Compliance Package",
            "name": "ectd_compliance_package_template__v",
            "kind": "binder",
            "definedIn": "compliance_package__v",
            "definedInType": "type"
        }
      ]
}
'''

> Request (Create Binder from Template)

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "fromTemplate=ectd_compliance_package_template__v" \
-d "name__v=CholeCap eCTD Compliance Package" \
-d "type__v=Compliance Package" \
-d "subtype__v=Professional" \
-d "lifecycle__v=Binder Lifecycle" \
-d "product__v=1357662840171" \
-d "major_version_number__v=0" \
-d "minor_version_number__v=1" \
https://myvault.veevavault.com/api/v25.2/objects/binders
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Successfully created binder.",
    "id": 565
}
'''

POST `/api/{version}/objects/binders`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

All required binder (document) fields must be included in the request. When creating a binder, no file is included in the request.

Name

Description

`fromTemplate`required

Include the parameter `fromTemplate` and specify the name of the template as returned from the document metadata as shown below. Only templates of `"kind": binder` are allowed.

#### Response Details

The example response shows the `"templates"` section of the type/subtype response. There are two available templates we can use to create this binder (each template has the `"kind": binder`). Both are defined on the `compliance_package__v` document type. We’ll use the binder template `ectd_compliance_package_template__v` to create our new binder as shown below.

### Create Binder Version

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "New draft successfully created",
    "major_version_number__v": 0,
    "minor_version_number__v": 4
}
'''

Create a new draft version of an existing binder.

Binders cannot be versioned with this endpoint if they exceed 10,000 nodes. Nodes include documents, sections, and component binders.

POST `/api/{version}/objects/binders/{binder_id}`

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

## Update Binders

### Update Binder

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "audience__c=Healthcare Provider" \
-d "country__v=1357662840400" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": 566
}
'''

PUT `/api/{version}/objects/binders/{binder_id}`

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

### Reclassify Binder

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "reclassify=true" \
-d "type__v=Claim" \
-d "lifecycle__v=Binder Lifecycle" \
https://myvault.veevavault.com/api/v25.2/objects/binders/776
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": 776
}
'''

Reclassify allows you to change the document type of an existing binder. A document “type” is the combination of the `type__v`, `subtype__v`, and `classification__v` fields on a binder. When you reclassify, Vault may add or remove certain fields on the binder. You can only reclassify the latest version of a binder and only one binder at a time. The API does not currently support Bulk Reclassify.

Learn more about:

-   Vault Help: [Reclassifying Documents](https://platform.veevavault.help/en/lr/2271).
-   API: [Retrieve Binders](#Vault_Retrieve_Binders_API_Reference)
-   API: [Retrieve Document Fields](#Retrieve_All_Document_Fields)
-   API: [Retrieve Document Types, Subtypes, and Classifications](#Retrieve_All_Document_Types)

#### About this Request

-   You can only reclassify the latest version of a specified binder.
-   You can only reclassify one binder at a time. Bulk reclassify is not currently supported.

PUT `/api/{version}/objects/binders/{binder_id}`

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

`reclassify`required

Set to `true`. Without this, a standard binder update action is performed.

`type__v`optional

The name of the document type being assigned to the binder.

`subtype__v`optional

The name of the document subtype (if one exists on the type).

`classification__v`optional

The name of the document classification (if one exists on the subtype).

`lifecycle__v`optional

The name of the lifecycle.

You can also add or remove values for any other editable field.

Note that additional fields may be required depending on the document type, subtype, and classification being assigned to the binder.

Use the [Document Metadata API](#Retrieve_All_Document_Fields) to retrieve required and editable fields in your Vault.

### Update Binder Version

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "audience__c=Healthcare Provider" \
-d "country__v=1357662840400" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/0/1
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": 566
}
'''

PUT `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}`

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

`{major_version}`

The binder `major_version_number__v` field value.

`{minor_version}`

The binder `minor_version_number__v` field value.

### Refresh Binder Auto-Filing

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "action=refresh_auto_filing" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/actions
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

POST `/api/{version}/objects/binders/{binder_id}/actions`

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

`action=refresh_auto_filing`required

Trigger auto-filing for a specific binder. This is analogous to the **Refresh Auto-Filing** action in the UI.

## Delete Binders

### Delete Binder

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "id": 35
}
'''

DELETE `api/{version}/objects/binders/{binder_id}`

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

### Delete Binder Version

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/versions/0/2
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "id": 124
}
'''

DELETE `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}`

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

`{major_version}`

The binder `major_version_number__v` field value.

`{minor_version}`

The binder `minor_version_number__v` field value.

## Export Binders

The Export Binder API allows you to export a zip archive with all documents from a binder, or a subset of those documents.

You can also export different artifacts for the selected documents, including source documents, renditions, versions, and document fields.

Learn about [Exporting Binders](https://platform.veevavault.help/en/lr/29681) in Vault Help.

### Export Binder

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/454/actions/export
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Job for Binder Export Started",
  "URL": "https://myvault.veevavault.com/api/v25.2/services/jobs/1201",
  "job_id": 1201
}
'''

Use this request to export the latest version or a specific version of a binder in your Vault.

-   This will export the complete binder, including all binder sections and documents.
-   To export only specific binder sections and documents, refer to the next section.
-   After initiating an export, you can retrieve its status, results, and download the exported binder.

To export the latest version of a binder, POST `/api/{version}/objects/binders/{binder_id}/actions/export`

To export a specific version of a binder, POST `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/actions/export`

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

`{major_version}`

The binder `major_version_number__v` field value.

`{minor_version}`

The binder `minor_version_number__v` field value.

#### Exporting Document Source Files

-   By default, the source files of all documents in the binder are exported.
-   Source documents can be any type of file (ZIP, DOCX, CSV, etc.).
-   To exclude source files, add the parameter `source=false` to the request endpoint.
-   For example: `.../actions/export?source=false`

#### Exporting Document Renditions

-   By default, document renditions are not exported.
-   To include renditions, add the parameter `renditiontype={rendition_type}` to the request endpoint.
-   For example: `.../actions/export?renditiontype=viewable_rendition__v`
-   The `viewable_rendition__v` is the most common, which exports the (typically auto-generated) PDF rendition of your document.
-   Note that if the document source file is a PDF, there is no separate viewable rendition to download.

#### Exporting Document Versions

-   By default, the document versions that are exported are determined by the version binding rule configured for the binder, section, or binder document.
-   To override the binding rule and export all major versions of each document, add the parameter `docversion=major` to the request endpoint.
-   For example: `.../actions/export?docversion=major`
-   To override the binding rule and export all major and minor versions of each document, add the parameter `docversion=major_minor` to the request endpoint.
-   For example: `.../actions/export?docversion=major_minor`

#### Exporting Attachments

-   To export binder attachments, include the parameter `attachments=all` or `attachments=latest`
-   For example: `.../actions/export?attachments=all` will export all versions of all attachments.
-   For example: `.../actions/export?attachments=latest` will export the latest version of all attachments.
-   Available in Vault API v15 or later.

#### Exporting Document Field Values & Metadata

-   By default, exported files include the `name__v` field value only.
-   To export additional fields, include a comma-separated list of field values to export.
-   For example, to export the binder name, title, document number, and export file name: `.../actions/export?name__v,title__v,document_number__v,export_filename__v`
-   By default, all document metadata is exported. To exclude the metadata, add the parameter `docfield=false`

#### Combining Multiple Request Parameters

-   To add multiple parameters to the request endpoint, separate each with the ampersand (`&`) character.
-   For example, to exclude the source file and export a rendition: `.../actions/export?source=false&renditiontype=viewable_rendition__v`

#### Response Details

On `SUCCESS`, the response includes the following information:

-   `url` - The URL to retrieve the current status of the binder export job.
-   `job_id` - The Job ID value is used to retrieve the [status](#RetrieveJobStatus) and results of the binder export request.

### Export Binder Sections

> Response

'''
{
  "nodes": [
    {
      "properties": {
        "section_number__v": "02.01.01",
        "name__v": "Investigator Brochure",
        "order__v": 0,
        "type__v": "section",
        "id": "1415381339215",
        "parent_id__v": "1415381339209"
      },
      "nodes": [
        {
          "properties": {
            "document_id__v": 18,
            "name__v": "CHC032-194 Investigator Brochure",
            "order__v": 0,
            "type__v": "document",
            "id": "1415381339220",
            "parent_id__v": "1415381339215"
          }
        },
      ]
    }
  ]
}
'''

> Request CSV Input File

To export just this one section and document from the binder, we would submit the following input file:

'''
id
1415381339215
1415381339220
'''

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
--data-binary @"C:\Vault\Binders\export-binder-sections.csv" \
https://myvault.veevavault.com/api/v25.2/objects/binders/454/1/0/actions/export
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Job for Binder Export Started",
  "URL": "https://myvault.veevavault.com/api/v25.2/services/jobs/1201",
  "job_id": 1201
}
'''

Use this request to export only specific sections and documents from the latest version of a binder in your Vault. This will export only parts of the binder, not the complete binder.

Before submitting this request:

-   The Export Binder feature must be enabled in your Vault.
-   You must be assigned permissions to use the API.
-   You must have the _Export Binder_ permission.
-   You must have the _View Document_ permission for the binder.
-   Only documents in the binder which you have the _View Document_ permission are available to export.

To export the latest version, POST `/api/{version}/objects/binders/{binder_id}/actions/export`

To export a specific version, POST `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/actions/export`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{binder_id}`

The binder `id` field value.

`{major_version}`

The binder `major_version_number__v` field value.

`{minor_version}`

The binder `minor_version_number__v` field value.

#### Query Parameters

Create a CSV or JSON input file with the `id` values of the binder sections and/or documents to be exported.

To retrieve a list of all nodes from a binder, GET `/api/{version}/objects/binders/{binder_id}?depth=all`. You may include any number of valid nodes. Vault will ignore `id` values which are invalid, but will export all which are valid.

For example, the abridged response below includes two nodes from a binder. Node “id”: “1415381339215” is a section (folder) and “id”: “1415381339220” is a document node.

Exporting a binder section node will automatically include all of its subsections and documents therein.

#### Response Details

On `SUCCESS`, the response includes the following information:

-   `url` - The URL to retrieve the current status of the binder export job.
-   `job_id` - The Job ID value is used to retrieve the [status](#RetrieveJobStatus) and results of the binder export request.

### Retrieve Binder Export Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/actions/export/1201/results
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "job_id": 1201,
  "id": 454,
  "major_version_number__v": 1,
  "minor_version_number__v": 0,
  "file": "/1201/454/1_0/Nyaxa Compliance Package.zip",
  "user_id__v": 44533
}
'''

After submitting a request to export a binder from your Vault, you can query Vault to determine the results of the request.

Before submitting this request:

-   You must have previously requested a binder export job (via the API) which is no longer active.
-   You must have a valid `job_id` value (retrieved from the export binder request above).

GET `/api/{version}/objects/binders/actions/export/{job_id}/results`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{job_id}`

The `id` value of the requested export job. This is returned with the export binder requests above.

#### Response Details

On `SUCCESS`, the response includes the following information:

Field Name

Description

`job_id`

The Job ID value of the binder export request.

`id`

The `id` value of the exported binder.

`major_version_number__v`

The major version number of the exported binder.

`minor_version_number__v`

The minor version number of the exported binder.

`file`

The path/location of the downloaded binder ZIP file.

`user_id__v`

The `id` value of the Vault user who initiated the binder export job.

### Download Exported Binder Files via File Staging

Once your binder export job has been successfully completed, you can download the files from [file staging](/docs/#FTP).

#### Prerequisites

Before downloading the files, the following conditions must be met:

-   The binder export job must have been successfully completed.
-   The API user must have a permission set which allows the _Application: File Staging: Access_ permission.

#### Downloading the Files

The exported binder is packaged in a ZIP file on file staging. [Learn more](/docs).

## Binder Relationships

Learn about [Binder Relationships](https://platform.veevavault.help/en/lr/21330) in Vault Help.

### Retrieve Binder Relationship

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/versions/0/3/relationships/202
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
                "source_doc_id__v": 566,
                "relationship_type__v": "supporting_documents__c",
                "created_date__v": "2015-03-24T22:37:20.000Z",
                "id": 202,
                "target_doc_id__v": 254,
                "created_by__v": 46916
            }
        }
    ],
    "errorType": null
}
'''

GET `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}`

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

`{major_version}`

The binder `major_version_number__v` field value.

`{minor_version}`

The binder `minor_version_number__v` field value.

`{relationship_id}`

The binder relationship `id` field value.

#### Response Details

Field Name

Description

`id`

Relationship ID.

`source_doc_id`

Document ID of the source document.

`relationship_type__v`

Relationship type

`created_by__v`

User ID of user who created the relationship

`created_date__v`

Timestamp when the relationship was created

`target_doc_id__v`

Document ID for target document

`target_major_version__v`

Major version of the target document; null values indicate that the relationship applies to all major versions

`target_minor_version__v`

Minor version of the target document; null values indicate that the relationship applies to all minor versions

### Create Binder Relationship

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "target_doc_id__v=13" \
-d "relationship_type__v=supporting_documents__c" \
-d "target_major_version__v=0" \
-d "target_minor_version__v=1" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/versions/0/3/relationships
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Document relationship successfully created.",
    "id": 202
}
'''

POST `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/relationships`

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

`{major_version}`

The binder `major_version_number__v` field value.

`{minor_version}`

The binder `minor_version_number__v` field value.

#### Body Parameters

Name

Description

`target_doc_id__v`required

Set the `target_doc_id__v` to the document `id` of the “target document” to which a relationship will be established with the binder.

`relationship_type__v`required

Set the `relationship_type__v` to the field value of one of the desired `relationshipTypes` from the “Documents Relationships Metadata” call.

`target_major_version__v`optional

If you’re creating a relationship with a specific version of the target document, set the `target_major_version__v` to the major version number of the target document.

`target_minor_version__v`optional

If you’re creating a relationship with a specific version of the target document, set the `target_minor_version__v` to the minor version number of the target document.

### Delete Binder Relationship

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/versions/0/4/relationships/202
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Document relationship successfully deleted.",
    "id": 202
}
'''

DELETE `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}`

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

`{major_version}`

The binder `major_version_number__v` field value.

`{minor_version}`

The binder `minor_version_number__v` field value.

`{relationship_id}`

The binder relationship `id` field value.

## Binder Sections

### Retrieve Binder Sections

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/29/sections
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "binder": {
    "nodes": [
      {
        "properties": {
          "document_id__v": 7,
          "name__v": "VeevaProm Information",
          "order__v": 0,
          "type__v": "document",
          "id": "1457556160448:810987462",
          "parent_id__v": "rootNode"
        }
      },
      {
        "properties": {
          "document_id__v": 2,
          "name__v": "VeevaProm Consumer Info",
          "order__v": 300,
          "type__v": "document",
          "id": "1457559259279:-602158059",
          "parent_id__v": "rootNode"
        }
      },
      {
        "properties": {
          "document_id__v": 5,
          "name__v": "VeevaProm Brochure",
          "order__v": 301,
          "type__v": "document",
          "id": "1457556176044:-743019200",
          "parent_id__v": "rootNode"
        }
      },
      {
        "properties": {
          "section_number__v": null,
          "name__v": "First Section Folder",
          "order__v": 401,
          "type__v": "section",
          "id": "1457560333810:-909497856",
          "parent_id__v": "rootNode"
        }
      },
      {
        "properties": {
          "section_number__v": null,
          "name__v": "Second Section Folder",
          "order__v": 501,
          "type__v": "section",
          "id": "1457560348267:1179700878",
          "parent_id__v": "rootNode"
        }
      }
    ]
  }
}
'''

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/29/sections/1457560348267:1179700878
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "node": {
    "properties": {
      "section_number__v": null,
      "name__v": "Second Section Folder",
      "order__v": 501,
      "type__v": "section",
      "id": "1457560348267:1179700878",
      "parent_id__v": "rootNode"
    },
    "nodes": [
      {
        "properties": {
          "document_id__v": 24,
          "name__v": "Nyaxa Information Packet",
          "order__v": 0,
          "type__v": "document",
          "id": "1457560406595:-2060980086",
          "parent_id__v": "1457560348267:1179700878"
        }
      },
      {
        "properties": {
          "document_id__v": 23,
          "name__v": "Nyaxa and Your Health",
          "order__v": 100,
          "type__v": "document",
          "id": "1457560409271:-1499449603",
          "parent_id__v": "1457560348267:1179700878"
        }
      },
      {
        "properties": {
          "document_id__v": 25,
          "name__v": "Nyaxa Prescribing Information",
          "order__v": 200,
          "type__v": "document",
          "id": "1457560412997:-1622511549",
          "parent_id__v": "1457560348267:1179700878"
        }
      }
    ]
  }
}
'''

Retrieve all sections (documents and subsections) in a binder’s top-level root node or sub-level node.

GET `/api/{version}/objects/binders/{binder_id}/sections/{section_id}`

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

`{section_id}`

Optional: Retrieve all sections (documents and subsections) in a binder’s sub-level node. If not included, all sections from the binder’s top-level root node will be returned.

#### Response Details

Field Name

Description

`nodes [n]`

List of all nodes (documents and sections) at each level in the binder.

`properties [n]`

List of all properties associated with each document or section node.

`hierarchy__v`

Specifies a single record from the `hierarchy__v` object that has been mapped this binder node.

`section_number__v`

Optional number which can be added to each section.

`order__v`

Order of the component (document or section) within the binder or within the binder section. **Note: There is a known issue affecting this parameter. It may not accurately reflect order.**

`type`

Type of node (document or section).

`document_id__v`

The document ID of the document in the binder. This is the same as the document’s actual document `id`

`id`

The document ID or section ID specific to the binder. For documents, this is different from the document’s actual document `id`.

`parent_id__v`

Section ID of the parent node, e.g., “rootNode”.

`name__v`

Name of the document or section. For sections, this is the name of the “subfolder” seen in the binder hierarchy in the UI.

`major_version_number__v`

If the document binding rule is “specific”, this is major version number of the document.

`minor_version_number__v`

If the document binding rule is “specific”, this is minor version number of the document.

### Retrieve Binder Version Section

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/29/versions/0/2/sections
'''

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/29/versions/0/2/sections/1457560348267:1179700878
'''

For a specific version, retrieve all sections (documents and subsection) in a binder’s top-level root node or sub-level node.

GET `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/sections/{section_id}`

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

`{major_version}`

The binder `major_version_number__v` field value.

`{minor_version}`

The binder `minor_version_number__v` field value.

`{section_id}`

Retrieve all sections (documents and subsections) in a binder’s sub-level node. If not included, all sections from the binder’s top-level root node will be returned.

#### Response Details

See [Retrieve Binder Sections](#Retrieve_Binder_Sections) example response.

### Create Binder Section

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "name__v=VeevaProm Additional Information" \
-d "section_number__v=1.3" \
-d "parent_id__v=1427232809771:1381853041" \
-d "order__v=1" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/sections
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": "1427486900128:1467568099"
}
'''

Create a new section in a binder.

Binders cannot exceed 50,000 nodes. Nodes include documents, sections, and component binders. If a binder has reached its limit, binder nodes cannot be added to the binder or any of its component binders, even if the component binders have not reached the 50,000 node limit.

POST `/api/{version}/objects/binders/{binder_id}/sections`

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

Field Name

Description

`name__v`required

Specify a name for the new section.

`section_number__v`optional

Enter a numerical value for the new section.

`parent_id__v`optional

If the new section is going to be a subsection, enter the Node ID of the parent section. If left blank, the new section will become a top-level section in the binder. When querying fields on binder nodes, this field corresponds to the `parent_section_id__sys` field.

`order__v`optional

Enter a number reflecting the position of the section within the binder or parent section. By default, new components appear below existing components. **Note: There is a known issue affecting this parameter. The values you enter may not work as expected.**

#### Response Details

On `SUCCESS`, Vault returns the Node ID of the newly created section. This is unique within the binder, regardless of level.

### Update Binder Section

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "name__v=VeevaProm Additional Information" \
-d "section_number__v=3" \
-d "parent_id__v=rootNode" \
-d "order__v=4" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/sections/1427232809771:1381853041
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": "1427486900128:1467568099"
}
'''

Update a section in a binder.

PUT `/api/{version}/objects/binders/{binder_id}/sections/{node_id}`

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

`{node_id}`

The binder node `id` of the section. When querying fields on binder nodes, this field corresponds to the `section_id__sys` field.

#### Body Parameters

Configure one or more of the following fields with values. These are all optional.

Field Name

Description

`name__v`optional

Change the name of the binder section.

`section_number__v`optional

Update the section number value.

`order__v`optional

Enter a number reflecting the position of the section within the binder or parent section. **Note: There is a known issue affecting this parameter. The values you enter may not work as expected.**

`parent_id__v`optional

To move the section to a different section in the binder, include the value of the parent node where it will be moved. When querying fields on binder nodes, this field corresponds to the `parent_section_id__sys` field.

#### Response Details

On `SUCCESS`, Vault returns the Node ID of the newly created section. This is unique within the binder, regardless of level.

### Delete Binder Section

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/sections/1427486900128:1467568099
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": "1427486900128:1467568099"
}
'''

Delete a section from a binder.

DELETE `/api/{version}/objects/binders/{binder_id}/sections/{section_id}`

#### Headers

Name

Description

`Content-Type`

`application/json` or `application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{binder_id}`

The binder `id` field value.

`{section_id}`

The binder node `id` field value.

#### Response Details

On `SUCCESS`, Vault returns the Node ID of the deleted section.

## Binder Documents

### Add Document to Binder

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "document_id__v=585" \
-d "parent_id__v=1427232809771:1381853041" \
-d "section_id__v=1" \
-d "binding_rule__v=steady-state" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/documents
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": "1427491342404:-1828014479"
}
'''

Add a document to a binder.

Binders cannot exceed 50,000 nodes. Nodes include documents, sections, and component binders. If a binder has reached its limit, binder nodes cannot be added to the binder or any of its component binders, even if the component binders have not reached the 50,000 node limit.

POST `/api/{version}/objects/binders/{binder_id}/documents`

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

Field Name

Description

`document_id__v`required

ID of the document being added to the binder.

`parent_id__v`optional

Section ID of the parent section, if the document will be in a section rather than top-level. Note: the section ID is unique no matter where it is in the binder hierarchy. Blank means adding the document at the top-level binder.

`order__v`optional

Enter a number reflecting the position of the document within the binder or section. By default, new components appear below existing components. **Note: There is a known issue affecting this parameter. The values you enter may not work as expected.**

`binding_rule__v`optional

The binding rule indicating which version of the document will be linked to the binder and the ongoing behavior. Options are: `default` (bind to the latest available version (assumed if binding\_rule is blank)), `steady-state` (bind to latest version in a steady-state), `current` (bind to current version), or `specific` (bind to a specific version).

`major_version_number__v`optional

If `binding_rule__v=specific`, then this is required and indicates the major version of the document to be linked. Otherwise it is ignored.

`minor_version_number__v`optional

If `binding_rule__v=specific`, then this is required and indicates the minor version of the document to be linked. Otherwise it is ignored.

### Move Document in Binder

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "parent_id__v=1457560333810:-909497856" \
-d "order__v=2" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/documents/1457559259279:-602158059
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "id": "1457559259279:-602158059"
}
'''

Move a document to a different position within a binder.

PUT `/api/{version}/objects/binders/{binder_id}/documents/{section_id}`

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

`{section_id}`

The binder node `id` field value.

#### Body Parameters

Field Name

Description

`order__v`optional

Enter a number reflecting the new position of the document within the binder or section. **Note: There is a known issue affecting this parameter. The values you enter may not work as expected.**

`parent_id__v`optional

To move the document to a different section or from a section to the binder’s root node, enter the value of the new parent node.

#### Response Details

On `SUCCESS`, Vault returns the new node ID of the document.

### Remove Document from Binder

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/documents/1427491342404:-1828014479
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": "1427491342404:-1828014479"
}
'''

DELETE `/api/{version}/objects/binders/{binder_id}/documents/{section_id}`

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

`{section_id}`

The binder node `id` field value.

#### Response Details

On `SUCCESS`, Vault returns the Node ID of the deleted document.

## Binder Templates

Learn about [Binder Templates](https://platform.veevavault.help/en/lr/7625) in Vault Help.

### Retrieve Binder Template Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/binders/templates
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
      "name": "filing_model__v",
      "type": "Object",
      "requiredness": "optional",
      "editable": true,
      "multi_value": false
    },
    {
      "name": "enable_dynamic_view__v",
      "type": "Boolean",
      "requiredness": "optional",
      "editable": true,
      "multi_value": false
    },
    {
      "name": "binder_template_parameters__v",
      "type": "String",
      "requiredness": "optional",
      "max_length": 100,
      "editable": false,
      "multi_value": true,
      "ordered": false
    }
  ]
}
'''

Retrieve the metadata which defines the shape of binder templates in your Vault.

GET `/api/{version}/metadata/objects/binders/templates`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

Field Name

Description

`name__v`

Binder template name, e.g., `binder_template_1__c`. This is used in the API when retrieving, creating, updating, or deleting binder templates.

`label__v`

Binder template label, e.g., “Binder Template 1”. This is the name users see in the UI when selecting a binder template.

`type__v`

Vault document type to which the template is associated.

`subtype__v`

Vault document subtype to which the template is associated. This field is only required if the template exists at the document subtype or classification level.

`classification__v`

Vault document classification to which the template is associated. This field is only required if the template exists at the document classification level.

`filing_model__v`

eTMF Vaults only. The filing model for the binder template.

`enable_dynamic_view__v`

eTMF Vaults only. Indicates if the binder template is available in the Dynamic Binder Viewer.

`binder_template_parameters__v`

eTMF Vaults only. Lists the available binder template parameters for the Dynamic Binder Viewer.

Name

Description

`name`

The binder template field name (`name__v`, `label__v`, `type__v`, etc.).

`type`

The binder template field type. This can be one of String, Boolean, Component, or Object (eTMF Vaults).

`requiredness`

Indicates whether or not a value must be added when creating a binder template. These include:  
\- `required` : A value must be added.  
\- `conditional` : For a template to exist at the document subtype or classification level, this is required.

`editable`

Boolean (true/false) field indicating whether or not a value can be added or edited by a user when creating or updating a binder template.

`multi_value`

Boolean (true/false) field indicating whether or not the field can have multiple values.

`component`

The component property applies to the `type__v`, `subtype__v`, and `classification__v` fields and defines the data type that can be set into this field.

### Retrieve Binder Template Node Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/binders/templates/bindernodes
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "data": [
    {
      "name": "id",
      "type": "id",
      "requiredness": "required",
      "editable": true,
      "multi_value": false
    },
    {
      "name": "parent_id__v",
      "type": "id",
      "requiredness": "optional",
      "editable": true,
      "multi_value": false
    },
    {
      "name": "order__v",
      "type": "Number",
      "requiredness": "optional",
      "max_value": 2147483647,
      "min_value": 0,
      "scale": 0,
      "editable": true,
      "multi_value": false
    },
    {
      "name": "node_type__v",
      "type": "Enum",
      "requiredness": "required",
      "editable": true,
      "multi_value": false,
      "enums": [
        "planned_document",
        "section"
      ]
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
      "name": "number__v",
      "type": "String",
      "requiredness": "optional",
      "max_length": 50,
      "editable": true,
      "multi_value": false
    },
    {
      "name": "lifecycle__v",
      "type": "Component",
      "requiredness": "conditional",
      "editable": true,
      "multi_value": false,
      "component": "Documentlifecycle"
    },
    {
      "name": "type__v",
      "type": "Component",
      "requiredness": "conditional",
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
      "requiredness": "conditional",
      "editable": true,
      "multi_value": false,
      "component": "Doctype"
    },
    {
      "name": "document_template__v",
      "type": "String",
      "requiredness": "conditional",
      "max_length": 50,
      "editable": true,
      "multi_value": false
    }
  ]
}
'''

Retrieve the metadata which defines the shape of binder template nodes in your Vault.

GET `/api/{version}/metadata/objects/binders/templates/bindernodes`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml` or `text/csv`

#### Response Details

Binder “nodes” are individual sections or documents in the binder template hierarchy. These can include folders and subfolders in the binder or documents existing within the sections.

Field Name

Description

`id`

For a given binder, these are the binder node (section or planned document) IDs.

`parent_id__v`

For a given binder template node, this is the node ID of its parent node. The top-level node is the `rootNode`.

`node_type__v`

Binder node types include `section` and `planned_document` (content placeholder documents within the binder template).

`label__v`

Binder template node label (name). For `section` node types, this is the name of the folder within the binder template. Example: `"label__v": "Operational Procedures"`. For `planned document` node types, this is the name of the content placeholder document and may include document field tokens. Example: `"label__v": "${study_b} - ${site_b} Operational Procedure"`.

`number__v`

These apply to binder `section` node types and are a numerical representation of the section’s hierarchy within the binder template. Example: Given two folders in a binder (under the root node), each containing three subfolders, the first and second folder numbers would be 01 and 02, respectively. The three subfolder numbers within the first and second folders would then be 01.01, 01.02, 01.03 and 02.01, 02.02, 02.03, respectively.

`order__v`

Order of the node within the binder or within the parent node. **Note: There is a known issue affecting this parameter. It may not accurately reflect order.**

`type__v`

Name of the document type to which templates are associated.

`subtype__v`

Name of the document subtype to which templates are associated.

`classification__v`

Name of the document classification to which templates are associated.

`lifecycle__v`

Name of the binder lifecycle to which templates are associated.

`document_template__v`

Name of the planned document template.

`milestone_type__v`

eTMF Vaults only. Name of the milestone type associated with the planned document template.

`hierarchy_mapping__v`

eTMF Vaults only. Object ID pointing to the lowest level in the TMF reference model.

Metadata Field

Description

`name`

The binder template node field name (`id`, `parent_id__v`, `node_type__v`, etc.).

`type`

The binder template field type. This can be one of ID, String, Number, Enum, or Component.

`requiredness`

Indicates whether or not a value must be added when creating a binder template. These include:  
\- `required` : A value must be added.  
\- `conditional` : For a template to exist at the document subtype or classification level, this is required.

`editable`

Boolean (true/false) field indicating whether or not a value can be added or edited by a user when creating or updating a binder template.

`multi_value`

Boolean (true/false) field indicating whether or not the field can have multiple values.

`component`

The component property applies to the `type__v`, `subtype__v`, `classification__v`, and `lifecycle__v` fields and defines the data type that can be set into this field.

### Retrieve Binder Template Collection

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/templates
'''

> Response

'''
{
   "responseStatus":"SUCCESS",
   "data":[
      {
         "name__v": "study_site_level_file_tmf_rm_30__c",
         "label__v": "Study Site Level File TMF RM 2.0",
         "active__v": true,
         "type__v": "trial_master_file__v",
         "subtype__v": null,
         "classification__v": null,
         "filing_model__v": "0MO000000000101"
      },
      {
         "name__v": "study_site_level_file_tmf_rm_20__c",
         "label__v": "Study Site Level File TMF RM 2.0",
         "active__v": "true",
         "type__v": "site_master_file__v",
         "subtype__v": null,
         "classification__v": null,
         "filing_model__v": "0MO000000000102"
      }
   ]
}
'''

Retrieve the collection of all binder templates in your Vault.

GET `/api/{version}/objects/binders/templates`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

The response lists all binder templates which have been added to the Vault. Shown above, two binder templates exist in our Vault. Both exist at the document type level and are intended for use with the `compliance_package__v` type. For information about the document template metadata, refer to the “Retrieve Binder Template Attributes” response below.

### Retrieve Binder Template Attributes

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/templates/study_site_level_file_tmf_rm_20__c
'''

> Response

'''
{
   "responseStatus":"SUCCESS",
   "data":[
      {
         "name__v": "study_site_level_file_tmf_rm_20__c",
         "label__v": "Study Site Level File TMF RM 2.0",
         "active__v": "true",
         "type__v": "site_master_file__v",
         "subtype__v": null,
         "classification__v": null,
         "filing_model__v": "0MO000000000102"
      }
   ]
}
'''

Retrieve the attributes of a specific binder template in your Vault.

GET `/api/{version}/objects/binders/templates/{template_name}`

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

`{template_name}`

The binder template `name__v` field value.

#### Response Details

The response lists all attributes configured on a specific binder template in the Vault. Shown above are the attributes configured on the specified template:

Field Name

Description

`name__v`

Name of the binder template. This value is not displayed to end users in the UI. It is seen by Admins and used in the API.

`label__v`

Label of the binder template. When users in the UI create binders from templates, they see this value in the list of available templates.

`type__v`

Vault document type to which the template is associated.

`subtype__v`

Vault document subtype to which the template is associated. This field is only displayed if the template exists at the document subtype or classification level.

`classification__v`

Vault document classification to which the template is associated. This field is only displayed if the template exists at the document classification level.

`filing_model__v`

eTMF Vaults only. Filing model for the binder template.

### Retrieve Binder Template Node Attributes

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/templates/study_site_level_file_tmf_rm_20__c/bindernodes
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "id": "5148",
            "parent_id__v": "studySiteLevelFileTMFRM20",
            "order__v": "0",
            "node_type__v": "section",
            "label__v": "Trial Management",
            "number__v": "01"
        },
        {
            "id": "9647",
            "parent_id__v": "studySiteLevelFileTMFRM20",
            "order__v": "100",
            "node_type__v": "section",
            "label__v": "Central Trial Documents",
            "number__v": "02"
        },
        {
            "id": "0908",
            "parent_id__v": "studySiteLevelFileTMFRM20",
            "order__v": "200",
            "node_type__v": "section",
            "label__v": "Site Management",
            "number__v": "03"
        },
        {
            "id": "6671",
            "parent_id__v": "5148",
            "order__v": "0",
            "node_type__v": "section",
            "label__v": "Trial Oversight",
            "number__v": "01.01"
        },
        {
            "id": "4509",
            "parent_id__v": "5148",
            "order__v": "100",
            "node_type__v": "section",
            "label__v": "General",
            "number__v": "01.02"
        },
        {
            "id": "3623",
            "parent_id__v": "6671",
            "order__v": "0",
            "node_type__v": "section",
            "label__v": "Operational Procedure",
            "number__v": "01.01.01",
            "hierarchy_mapping__v": "00H00484"
        },
        {
            "id": "5575",
            "parent_id__v": "6671",
            "order__v": "100",
            "node_type__v": "section",
            "label__v": "Recruitment Plan",
            "number__v": "01.01.02",
            "hierarchy_mapping__v": "00H00488"
        },
        {
            "id": "StudyBSiteBOperationalProcedur",
            "parent_id__v": "3623",
            "order__v": "0",
            "node_type__v": "planned_document",
            "label__v": "${study_b} - ${site_b} Operational Procedure",
            "lifecycle__v": "etmf_lifecycle__c",
            "type__v": "trial_management__c",
            "subtype__v": "trial_oversight__c",
            "classification__v": "operational_procedure_manual__c"
        },
        {
            "id": "StudyBSiteBRecruitmentPlan",
            "parent_id__v": "5575",
            "order__v": "0",
            "node_type__v": "planned_document",
            "label__v": "${study_b} - ${site_b} Recruitment Plan",
            "lifecycle__v": "etmf_lifecycle__c",
            "type__v": "trial_management__c",
            "subtype__v": "trial_oversight__c",
            "classification__v": "recruitment_plan__c"
        },
        {
            "id": "9454",
            "parent_id__v": "4509",
            "order__v": "0",
            "node_type__v": "section",
            "label__v": "Tracking Information",
            "number__v": "01.02.01",
            "hierarchy_mapping__v": "00H00511"
        },
        {
            "id": "5014",
            "parent_id__v": "4509",
            "order__v": "100",
            "node_type__v": "section",
            "label__v": "Filenote",
            "number__v": "01.02.02",
            "hierarchy_mapping__v": "00H00515"
        },
        {
            "id": "StudyBSiteBOperationalProcedu1",
            "parent_id__v": "9454",
            "order__v": "0",
            "node_type__v": "planned_document",
            "label__v": "${study_b} - ${site_b} Tracking Information",
            "lifecycle__v": "etmf_lifecycle__c",
            "type__v": "trial_management__c",
            "subtype__v": "general__c",
            "classification__v": "tracking_information__c"
        },
        {
            "id": "StudyBSiteBFileNote",
            "parent_id__v": "5014",
            "order__v": "0",
            "node_type__v": "planned_document",
            "label__v": "${study_b} - ${site_b} File Note",
            "lifecycle__v": "etmf_lifecycle__c",
            "type__v": "trial_management__c",
            "subtype__v": "general__c",
            "classification__v": "filenote__c"
        },
        {
            "id": "2443",
            "parent_id__v": "9647",
            "order__v": "0",
            "node_type__v": "section",
            "label__v": "Trial Documents",
            "number__v": "02.01"
        },
        {
            "id": "0413",
            "parent_id__v": "9647",
            "order__v": "100",
            "node_type__v": "section",
            "label__v": "Subject Information Sheet",
            "number__v": "02.02"
        },
        {
            "id": "5118",
            "parent_id__v": "2443",
            "order__v": "0",
            "node_type__v": "section",
            "label__v": "Protocol",
            "number__v": "02.01.01",
            "hierarchy_mapping__v": "00H00536"
        },
        {
            "id": "StudyBSiteBTrialProtocol",
            "parent_id__v": "5118",
            "order__v": "0",
            "node_type__v": "planned_document",
            "label__v": "${study_b} - ${site_b} Trial Protocol",
            "lifecycle__v": "etmf_lifecycle__c",
            "type__v": "central_trial_documents__c",
            "subtype__v": "trial_documents__c",
            "classification__v": "protocol__c"
        },
        {
            "id": "StudyBSiteBSubjectInformationS",
            "parent_id__v": "0413",
            "order__v": "0",
            "node_type__v": "planned_document",
            "label__v": "${study_b} - ${site_b} Subject Information Sheet",
            "lifecycle__v": "etmf_lifecycle__c",
            "type__v": "central_trial_documents__c",
            "subtype__v": "subject_documents__c",
            "classification__v": "subject_information_sheet__c"
        },
        {
            "id": "9135",
            "parent_id__v": "0908",
            "order__v": "0",
            "node_type__v": "section",
            "label__v": "Site Selection",
            "number__v": "03.01"
        },
        {
            "id": "StudyBSiteBConfidentialityAgre",
            "parent_id__v": "9135",
            "order__v": "0",
            "node_type__v": "planned_document",
            "label__v": "${study_b} - ${site_b} Confidentiality Agreement",
            "lifecycle__v": "etmf_lifecycle__c",
            "type__v": "site_management__c",
            "subtype__v": "site_selection__c",
            "classification__v": "confidentiality_agreement__c"
        },
        {
            "id": "StudyBSiteBSiteContacts",
            "parent_id__v": "9135",
            "order__v": "100",
            "node_type__v": "planned_document",
            "label__v": "${study_b} - ${site_b} Site Contacts",
            "lifecycle__v": "etmf_lifecycle__c",
            "type__v": "site_management__c",
            "subtype__v": "site_selection__c",
            "classification__v": "site_contact_details__c"
        }
    ]
}
'''

Retrieve the attributes of each node (folder/section) of a specific binder template in your Vault.

GET `/api/{version}/objects/binders/templates/{template_name}/bindernodes`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{template_name}`

The binder template `name__v` field value.

#### Response Details

The response lists all attributes configured on each node of a specific binder template in the Vault. The binder template shown above has six nodes.

Field Name

Description

`id`

The binder node (section or planned document) IDs.

`parent_id__v`

The node ID of a section or planned document’s parent node. The top-level node is the `rootNode`.

`node_type__v`

Binder node types include `section` and `planned_document` (content placeholder documents within the binder template).

`label__v`

Label of the binder section or planned document.

`type__v`

Vault document type to which planned documents are associated.

`subtype__v`

Vault document subtype to which planned documents are associated. This field is only displayed if the planned document exists at the document subtype or classification level.

`classification__v`

Vault document classification to which planned documents are associated. This field is only displayed if the planned document exists at the document classification level.

`lifecycle__v`

Name of the binder lifecycle to which planned documents are associated.

`number__v`

These apply to binder `section` node types and are a numerical representation of the section’s hierarchy within the binder template. Example: Given two folders in a binder (under the root node), each containing three subfolders, the first and second folder numbers would be 01 and 02, respectively. The three subfolder numbers within the first and second folders would then be 01.01, 01.02, 01.03 and 02.01, 02.02, 02.03, respectively.

`order__v`

Order of the node within the binder or within the parent node. **Note: There is a known issue affecting this parameter. It may not accurately reflect order.**

`hierarchy_mapping__v`

eTMF Vaults only. Object ID pointing to the lowest level in the TMF reference model.

### Create Binder Template

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "label__v=Claim Binder Template" \
-d "type__v=claim__c" \
-d "active__v=true" \
https://myvault.veevavault.com/api/v25.2/objects/binders/templates
'''

> Response

'''
{
   "responseStatus":"SUCCESS",
   "data":[
      {
         "responseStatus":"SUCCESS",
         "name__v":"claim_binder_template__c"
      }
   ]
}
'''

Create a new binder template in your Vault.

POST `/api/{version}/objects/binders/templates`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

When creating binder templates, the following fields are required in all Vaults:

Name

Description

`name__v`optional

The name of the new binder template. If not included, Vault will use the specified `label__v` value to generate a value for the `name__v` field.

`label__v`required

The label of the new binder template. This is the name users will see among the available binder templates in the UI.

`type__v`required

The name of the document type to which the template will be associated.

`subtype__v`optional

The name of the document subtype to which the template will be associated. This is only required if associating the template with a document subtype.

`classification__v`optional

The name of the document classification to which the template will be associated. This is only required if associating the template with a document classification.

`active__v`required

Set to true or false to indicate whether or not the new binder template should be set to active, i.e., available for selection when creating a binder.

In this example:

-   The input format is set to `application/x-www-form-urlencoded`.
-   The response format is not set and will default to JSON.
-   The `name__v` field is not included. Vault will use the specified `label__v` field value to create the `name__v=claim_binder_template__c`.
-   The `label__v` field specifies the binder template label “Claim Binder Template”. This is what users will see among the available templates in the UI.
-   The document `type__v` is specified. This template is being created for binders of `type__v=claim__c`. Since this exists at the document type level, the subtype and classification are not required.
-   The template is being set to `active__v=true`. It will be available for selection when creating a new binder.

#### Response Details

On `SUCCESS`, Vault returns the name of the new binder template.

### Bulk Create Binder Templates

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
--data-binary @"C:\Vault\Templates\add_binder_templates.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/templates
'''

> Response

'''
{
   "responseStatus":"SUCCESS",
   "data":[
      {
         "responseStatus":"SUCCESS",
         "name":"binder_template_1__c"
      },
      {
         "responseStatus":"SUCCESS",
         "name":"binder_template_2__c"
      },
      {
         "responseStatus":"SUCCESS",
         "name":"binder_template_3__c"
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

Create from 1-500 new binder templates in your Vault.

POST `/api/{version}/objects/binders/templates`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

When creating binder templates, the following fields are required in all Vaults:

Name

Description

`name__v`optional

The name of the new binder templates. If not included, Vault will use the specified `label__v` value to generate a value for the `name__v` field.

`label__v`required

The label of the new binder templates. This is the name users will see among the available binder templates in the UI.

`type__v`required

The name of the document type to which the templates will be associated.

`subtype__v`optional

The name of the document subtype to which the templates will be associated. This is only required if associating the templates with document subtypes.

`classification__v`optional

The name of the document classification to which the templates will be associated. This is only required if associating the templates with document classifications.

`active__v`required

Set to true or false to indicate whether or not the new binder templates should be set to active, i.e., available for selection when creating a binder.

[![Download Input File](../../images/download-json-orange.svg)](../../docs/sample-files/bulk-create-binder-templates.json)

#### Example CSV Input

`name__v`

`label__v`

`type__v`

`subtype__v`

`classification__v`

`active__v`

binder\_template\_1\_\_c

First Binder Template

site\_master\_file\_\_v

true

Binder Template 2

trial\_master\_file\_\_v

true

Binder Template 3

central\_trial\_documents\_\_vs

trial\_documents\_\_vs

protocol\_\_vs

true

Binder Template 4

central\_trial\_documents\_\_vs

reports\_\_vs

clinical\_study\_report\_\_vs

false

In this example input, we’re creating four new binder templates in our Vault:

-   We’ve only specified the `name__v` value for the first template and given it a different `label__v` value. The other templates will inherit their `name__v` values from the `label__v` values.
-   We’ve specified the document type, subtype, and classification to which each binder template will be associated.

In this example:

-   The input file format is set to CSV.
-   The response format is not set and will default to JSON.
-   The path/name of the CSV input file in our local directory is specified.

#### Response Details

On `SUCCESS`, Vault returns the names of the new binder templates.

### Create Binder Template Node

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
--data-binary @"C:\Vault\Templates\add_binder_template_nodes.csv" \
https://myvault.veevavault.com/api/v25.2/objects/binders/templates/binder_template_1__c/bindernodes
'''

Create nodes in an existing binder template.

Binders cannot exceed 50,000 nodes, including component binders. If a binder has reached its limit, binder nodes cannot be added to the binder or any of its component binders, even if the component binders have not reached the 50,000 node limit. If this request would result in a binder that exceeds 50,000 nodes, Vault creates as many nodes as possible and halts the transaction at 50,000.

POST `/api/{version}/objects/binders/templates/{template_name}/bindernodes`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{template_name}`

The binder template `name__v` field value.

#### Body Parameters

When creating binder template nodes, the following fields are required in all Vaults:

Name

Description

`id`required

The ID of the binder node. This must be set to a unique number.

`parent_id__v`required

Enter the `id` of the parent section. To create a node in the top level of the binder (rootNode), leave the value blank.

`node_type__v`required

Set to `section` or `planned_document`.

`label__v`required

Label for the section or planned document. For planned documents, this corresponds to “Planned Name” in the UI.

`type__v`optional

The name of the document type to which the template will be associated.

`subtype__v`optional

The name of the document subtype to which the templates will be associated. This is only required if associating the template with a document subtype.

`classification__v`optional

The name of the document classification to which the template will be associated. This is only required if associating the template with a document classification.

`active__v`optional

Set to true or false to indicate whether or not the binder template should be set to active, i.e., available for selection when creating a binder.

`order__v`optional

Order of the component (planned document or section) within the binder template or within the template section. **Note: There is a known issue affecting this parameter. The values you enter may not work as expected.**

#### Example CSV Input: Create Top-Level Section Binder Nodes

`id`

`node_type__v`

`label__v`

`order__v`

`number__v`

`parent_id__v`

100

section

Folder A

1

01

200

section

Folder B

2

02

300

section

Folder C

3

03

In this example input, we’re creating three new binder nodes in the template.

-   These will be new `section` node types.
-   The required `parent_id__v` name is included but its value left blank. By default, the new sections will be added to the top-level in the binder hierarchy.
-   The optional section order and number are set. These define the position of the three new sections in the binder template hierarchy.

#### Example CSV Input: Create Sub-Level Section Binder Nodes

`id`

`node_type__v`

`label__v`

`order__v`

`number__v`

`parent_id__v`

101

section

SubFolder A1

1

01.01

100

102

section

SubFolder A2

2

01.02

100

In this example input, we’re creating three new binder nodes in the template.

-   These will be new `section` node types.
-   The required `parent_id__v` name is included. If the values are left blank, the new sections will be added to the top-level in the binder hierarchy by default.
-   The optional section order and number are set. These define the position of the three new sections in the binder template hierarchy.

#### Example CSV Input: Create Planned Document Binder Node

`id`

`node_type__v`

`label__v`

`order__v`

`parent_id__v`

`type__v`

`subtype__v`

`classification__v`

`lifecycle__v`

101PD

planned\_document

Planned Document A1

1

101

promotional\_piece\_\_vs

advertisement\_\_vs

web\_\_vs

promotional\_piece\_\_vs

In this example input, we’re creating new binder node of the type `planned_document`.

-   The required `parent_id__v` name is included. If the values are left blank, the planned document will be added to the top-level in the binder hierarchy by default.
-   The optional section order and number are set. These define the position of the planned document in the binder template hierarchy.

In this example:

-   The input file format is set to CSV.
-   The response format is not set and will default to JSON.
-   The path/name of the CSV input file in our local directory is specified.

### Update Binder Template

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Accept: text/csv" \
-d "active__v=true" \
https://myvault.veevavault.com/api/v25.2/objects/binders/templates/binder_template_1__c
'''

> Response

'''
responseStatus,name,errors
SUCCESS,binder_template_1__c,
'''

Update an existing binder template in your Vault.

By changing the document type/subtype/classification, you can move an existing binder template to a different level of the document type hierarchy, effectively reclassifying the template.

See also: **Bulk Update Binder Templates** [below](#Bulk_Update_Binder_Templates).

PUT `/api/{version}/objects/binders/templates`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

You can update the following fields on binder templates:

Name

Description

`name__v`optional

Change the name of an existing binder template.

`label__v`optional

Change the label of an existing binder template. This is the name users will see among the available binder templates in the UI.

`type__v`required

Change the document type to which the template is associated.

`subtype__v`optional

Change the document subtype to which the template is associated. This is only required if associating the template with a document subtype.

`classification__v`optional

Change the document classification to which the template is associated. This is only required if associating the template with a document classification.

`active__v`optional

Set to true or false to indicate whether or not the binder template should be set to active, i.e., available for selection when creating a binder.

In this example:

-   The input file format is set to `application/x-www-form-urlencoded`.
-   The response format is set to `text/csv`.
-   The `active__v` field is set to `false`. We’re changing the status of this binder template from “Active” to “Inactive”.

#### Response Details

On `SUCCESS`, Vault returns the name of the updated binder template.

### Bulk Update Binder Templates

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Templates\update_binder_templates.csv" \
https://myvault.veevavault.com/api/v25.2/objects/binders/templates
'''

> Response

'''
responseStatus,name,errors
SUCCESS,binder_template_2__c,
SUCCESS,binder_template_3__c,
SUCCESS,binder_template_4__c,
'''

Update from 1-500 binder templates in your Vault.

By changing the document type/subtype/classification, you can move an existing binder template to a different level of the document type hierarchy, effectively reclassifying the template.

See also: **Update \[Single\] Binder Template** [above](#Update_Binder_Template).

PUT `/api/{version}/objects/binders/templates`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

You can update the following fields on binder templates:

Name

Description

`name__v`required

Change the name of existing binder templates.

`label__v`optional

Change the label of existing binder templates. This is the name users will see among the available binder templates in the UI.

`type__v`required

Change the document type to which the templates are associated.

`subtype__v`optional

Change the document subtype to which the templates are associated. This is only required if associating the templates with document subtypes.

`classification__v`optional

Change the document classification to which the templates are associated. This is only required if associating the templates with document classifications.

`active__v`optional

Set to true or false to indicate whether or not the binder templates should be set to active, i.e., available for selection when creating a binder.

[![Download Input File](../../images/download-json-orange.svg)](../../docs/sample-files/bulk-update-binder-templates.json)

#### Example CSV Input

`name__v`

`label__v`

`active__v`

binder\_template\_2\_\_c

Second Binder Template

true

binder\_template\_3\_\_c

Binder Template 3

true

binder\_template\_4\_\_c

Binder Template 4

false

In this example input, we’re updating three existing binder templates in our Vault.

-   On the first template, we’re updating both the `name__v` and `label__v` values.
-   On the second template, we’re updating the `name__v` value and setting the `active__v` value to `true`.
-   On the third template, we’re updating the `name__v` value and setting the `active__v` value to `false`.

Including a binder field name in the input but leaving its value blank will clear existing values from the field.

In this example:

-   The input file format is set to CSV.
-   The response format is not set and will default to JSON.
-   The path/name of the CSV input file in our local directory is specified.

#### Response Details

On `SUCCESS`, Vault returns the names of the updated binder templates.

### Replace Binder Template Nodes

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/templates/binder_template_1__c
'''

Replace all binder nodes in an existing binder template. This action removes all existing nodes and replaces them with those specified in the input.

PUT `/api/{version}/objects/binders/templates/{template_name}/bindernodes`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{template_name}`

The binder template `name__v` field value.

#### Example CSV Input

See the **Create Binder Template Node** [above](#Create_Binder_Template_Node) for example inputs, which are the same as those used in this request.

### Delete Binder Template

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/templates/binder_template_1__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Delete an existing binder template from your Vault.

DELETE `/api/{version}/objects/binders/templates/{template_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{template_name}`

The binder template `name__v` field value.

## Binding Rules

Learn about [Version Binding](https://platform.veevavault.help/en/lr/5489) in Vault Help.

### Update Binding Rule

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "binding_rule__v=steady-state" \
-d "binding_rule_override__v=true" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/binding_rule
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": 566
}
'''

PUT `/api/{version}/objects/binders/{binder_id}/binding_rule`

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

`binding_rule__v`optional

Indicates which binding rule to apply (which document versions to link to the section). Options are: `default` (bind to the latest available version (assumed if binding\_rule is blank)), `steady-state` (bind to latest version in a steady-state), or `current` (bind to current version).

`binding_rule_override__v`optional

Set to true or false to indicate if the specified binding rule should override documents or sections which already have binding rules set. If set to `true`, the binding rule is applied to all documents and sections within the current section. If blank or set to `false`, the binding rule is applied only to documents and sections within the current section that do not have a binding rule specified.

### Update Binder Section Binding Rule

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "binding_rule__v=steady-state" \
-d "binding_rule_override__v=true" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/sections/1427232809771:1381853041/binding_rule
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": "1427491342404:-1828014479"
}
'''

PUT `/api/{version}/objects/binders/{binder_id}/sections/{node_id}/binding_rule`

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

`{node_id}`

The binder node `id` field value.

#### Body Parameters

Name

Description

`binding_rule__v`optional

Indicates which binding rule to apply (which document versions to link to the section). Options are: `default` (bind to the latest available version (assumed if binding\_rule is blank)), `steady-state` (bind to latest version in a steady-state), or `current` (bind to current version).

`binding_rule_override__v`optional

Set to true or false to indicate if the specified binding rule should override documents or sections which already have binding rules set. If set to `true`, the binding rule is applied to all documents and sections within the current section. If blank or set to `false`, the binding rule is applied only to documents and sections within the current section that do not have a binding rule specified.

#### Response Details

On `SUCCESS`, Vault returns the Node ID of the updated section.

### Update Binder Document Binding Rule

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "binding_rule__v=specific" \
-d "major_version_number__v=1" \
-d "minor_version_number__v=0" \
https://myvault.veevavault.com/api/v25.2/objects/binders/566/documents/1427491342404:-1828014479/binding_rule
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "id": "1427491342404:-1828014479"
}
'''

PUT `/api/{version}/objects/binders/{binder_id}/documents/{node_id}/binding_rule`

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

`{node_id}`

The binder node `id` field value.

#### Body Parameters

Name

Description

`binding_rule__v`optional

Indicates which binding rule to apply (which document versions to link to the section). Options are: `default` (bind to the latest available version (assumed if binding\_rule is blank)), `steady-state` (bind to latest version in a steady-state), `current` (bind to current version), or `specific` (bind to a specific version).

`major_version_number__v`optional

If `binding_rule__v=specific`, then this is required and indicates the major version of the document to be linked. Otherwise it is ignored.

`minor_version_number__v`optional

If `binding_rule__v=specific`, then this is required and indicates the major version of the document to be linked. Otherwise it is ignored.

#### Response Details

On `SUCCESS`, Vault returns the Node ID of the updated document node within the binder
