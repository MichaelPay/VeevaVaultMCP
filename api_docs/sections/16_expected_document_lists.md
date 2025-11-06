<!-- 
VaultAPIDocs Section: # Expected Document Lists
Original Line Number: 32049
Generated: August 30, 2025
Part 16 of 38
-->

# Expected Document Lists

Expected Document Lists (EDLs) help you to measure the completeness of projects. Learn about [EDLs in Vault Help](https://platform.veevavault.help/en/lr/32749). Note that if your Vault is configured to set milestone values by EDL item, the following EDL endpoints may trigger updates to a document’s milestone fields. Learn about [milestones in Vault Help](https://clinical.veevavault.help/en/lr/37991#applying_edl_templates_to_milestones).

## Create a Placeholder from an EDL Item

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Accept: application/json" \
-d "edlItemIds=00EI000000000127, 0EI000000000128" \
https://myvault.veevavault.com/api/v25.2/vobjects/edl_item__v/actions/createplaceholder \
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
    "job_id": 84201,
    "url": "/api/v25.2/services/jobs/84201"
}
'''

Create a placeholder from an EDL item. Learn about working with [Content Placeholders in Vault Help](https://platform.veevavault.help/en/lr/15087).

POST `/api/{version}/vobjects/edl_item__v/actions/createplaceholder`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default)

#### Body Parameters

Name

Description

`edlItemIds`required

Comma separated list of EDL Item ids on which to initiate the action.

#### Response Details

On `SUCCESS`, the response includes the following information:

-   `url` - The URL to retrieve the current status of the export job.
-   `job_id` - The Job ID value is used to retrieve the [status](#RetrieveJobStatus) and results of the request.

## Retrieve All Root Nodes

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/composites/trees/edl_hierarchy__v
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "data": [
    {
      "id": "0000000000000JIT",
      "order__v": 1,
      "ref_type__v": "edl__v",
      "ref_name__v": "NewEDL",
      "url": "/vobjects/edl__v/0EL000000001901",
      "ref_id__v": "0EL000000001901",
      "parent_id__v": null
    }
  ]
}
'''

Retrieves all root EDL nodes and node metadata. Learn more about [EDL hierarchies in Vault Help](https://regulatory.veevavault.help/en/lr/37472).

GET `/api/{version}/composites/trees/{edl_hierarchy_or_template}`

#### Headers

Name

Description

`Content-Type`

`application/json` (default) or `text/csv`

`Accept`

`application/json` (default) or `application/xml` or `text/csv`

#### URI Path Parameters

Name

Description

`edl_hierarchy_or_template`

Choose to retrieve nodes for either `edl_hierarchy__v` or `edl_template__v`.

## Retrieve Specific Root Nodes

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
--header 'Content-Type: application/json' \
--data-raw '[
{
  "ref_id__v": "0EL000000000401"
}
]' \
https:myvault.veevavault.com/api/v25.2/composites/trees/edl_hierarchy__v/actions/listnodes
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS",
            "id": "0000000000000IR1",
            "ref_id__v": "0EL000000000401"
        }
    ]
}
'''

Retrieves the root node ID for the given EDL record IDs.

POST `/api/{version}/composites/trees/{edl_hierarchy_or_template}/actions/listnodes`

#### Headers

Name

Description

`Content-Type`

`application/json` (default) or `text/csv`

`Accept`

`application/json` (default) or `application/xml` or `text/csv`

#### URI Path Parameters

Name

Description

`edl_hierarchy_or_template`

Choose to retrieve nodes for either `edl_hierarchy__v` or `edl_template__v`.

#### Body Parameters

In the body of the request, include a raw JSON object with the following information:

Name

Description

`ref_id__v`required

The ID of the EDL record whose root node you’d like to retrieve. Maximum 1,000 IDs per request.

## Retrieve a Node’s Children

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/composites/trees/edl_hierarchy__v/0000000000000JIT/children
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "data": [
    {
      "id": "0000000000000JLL",
      "order__v": 1,
      "ref_type__v": "edl_item__v",
      "ref_name__v": "NewEDL Child",
      "url": "/vobjects/edl_item__v/0EI000000009401",
      "ref_id__v": "0EI000000009401",
      "parent_id__v": "0000000000000JIT"
    }
  ]
}
'''

Given an EDL node ID, retrieves immediate children (not grandchildren) of that node. Learn more about EDL hierarchies in [Vault Help](https://regulatory.veevavault.help/en/lr/37472).

GET `/api/{version}/composites/trees/{edl_hierarchy_or_template}/{parent_node_id}/children`

#### Headers

Name

Description

`Content-Type`

`application/json` (default) or `text/csv`

`Accept`

`application/json` (default) or `application/xml` or `text/csv`

#### URI Path Parameters

Name

Description

`edl_hierarchy_or_template`

Choose to retrieve node children for either `edl_hierarchy__v` or `edl_template__v`.

`parent_node_id`

The ID of a parent node in the hierarchy.

## Update Node Order

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
-d '{"id": "0000000000000JLL","order__v": "2"}'
https://myvault.veevavault.com/api/v25.2/composites/trees/edl_hierarchy__v/0000000000000JIT/children
'''

> Response

'''
{
  "responseStatus": "SUCCESS"
}
'''

Given an EDL parent node, update the order of its children.

PUT `/api/{version}/composites/trees/{edl_hierarchy_or_template}/{parent_node_id}/children`

#### Headers

Name

Description

`Content-Type`

`application/json` (default) or `text/csv`

`Accept`

`application/json` (default) or `application/xml` or `text/csv`

#### URI Path Parameters

Name

Description

`edl_hierarchy_or_template`

Choose to update node order for either `edl_hierarchy__v` or `edl_template__v`.

`parent_node_id`

The ID of a parent node in the hierarchy.

#### Body Parameters

Expressed as a JSON or a CSV.

Name

Description

`id`required

The ID of the child node to update.

`order__v`required

The new order for the node in the hierarchy, such as “1”, “2”, etc.

## Add EDL Matched Documents

> Request

'''
curl -L -X POST -H 'Authorization: {SESSION_ID}' \
-H 'Content-Type: application/json' \
--data-raw '[
   {
       "id": "0EI000000003001",
       "document_id": "21",
       "major_version_number__v": 1,
       "minor_version_number__v": 0,
       "lock": true
   }
]'
'https://myvault.veevavault.com/api/v25.2/objects/edl_matched_documents/batch/actions/add' \
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "responseStatus": "SUCCESS",
           "id": "0EI000000003001",
           "document_id": "21",
           "major_version_number__v": "1",
           "minor_version_number__v": "0",
           "lock": "true"
       }
   ]
}
'''

Add matched documents to EDL Items. You must have a security profile that grants the _Application: EDL Matching: Edit Document Matches_ permission, and EDL Matched Document APIs must be enabled in your Vault. To enable this feature, contact [Veeva Support](https://support.veeva.com/hc/en-us).

POST `/api/{version}/objects/edl_matched_documents/batch/actions/add`

#### Headers

Name

Description

`Content-Type`

`application/json` (default) or `text/csv`

`Accept`

`application/json` (default)

#### Body Parameters

Expressed as JSON or CSV.

Name

Description

`id`required

The EDL Item `id` to match to documents. EDL Item records and their parent records must have a `status__v` of `active__v`.

`document_id`required

The document `id` to match to an EDL Item.

`major_version_number__v`optional

The major version number of a document. You must also include `minor_version_number__v` to use this parameter.

`minor_version_number__v`optional

The minor version number of a document. You must also include `major_version_number__v` to use this parameter.

`lock`optional

If set to `true`, locks the EDL Item to match a specific steady state document version or, if version numbers are omitted, the latest steady state document version. If set to `false` or omitted, and version numbers are omitted, Vault matches the latest version of the document without regard to state.

#### Response Details

On `SUCCESS`, the response includes a `SUCCESS` or `FAILURE` status and any applicable error messages for each EDL Item to document match in the body of your request.

## Remove EDL Matched Documents

> Request

'''
curl -L -X POST -H 'Authorization: {SESSION_ID}' \
-H 'Content-Type: application/json' \
--data-raw '[
  {
      "id": "0EI000000003001",
      "document_id": "21",
      "major_version_number__v": 1,
      "minor_version_number__v": 0,
      "remove_locked": true
  },
    {
      "id": "0EI000000003001",
      "document_id": "22",
      "major_version_number__v": 0,
      "minor_version_number__v": 1,
      "remove_locked": true
  }
]'
'https://myvault.veevavault.com/api/v25.2/objects/edl_matched_documents/batch/actions/remove' \
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "responseStatus": "FAILURE",
           "errors": [
               {
                   "type": "INVALID_DATA",
                   "message": "Can not remove an automatically matched Document"
               }
           ],
           "id": "0EI000000003001",
           "document_id": "22",
           "major_version_number__v": "0",
           "minor_version_number__v": "1",
           "lock": "true"
       },
       {
           "responseStatus": "SUCCESS",
           "id": "0EI000000003001",
           "document_id": "21",
           "major_version_number__v": "1",
           "minor_version_number__v": "0",
           "lock": "true"
       }
   ]
}
'''

Remove manually matched documents from EDL Items. You must have a security profile that grants the _Application: EDL Matching: Edit Document Matches_ permission, and EDL Matched Document APIs must be enabled in your Vault. To enable this feature, contact [Veeva Support](https://support.veeva.com/hc/en-us).

POST `/api/{version}/objects/edl_matched_documents/batch/actions/remove`

#### Headers

Name

Description

`Content-Type`

`application/json` (default) or `text/csv`

`Accept`

`application/json` (default)

#### Body Parameters

Expressed as JSON or CSV.

Name

Description

`id`required

The EDL Item `id` to match to documents. EDL Item records and their parent records must have a `status__v` of `active__v`.

`document_id`required

The document `id` to match to an EDL Item.

`major_version_number__v`optional

The major version number of a document. You must also include `minor_version_number__v` to use this parameter.

`minor_version_number__v`optional

The minor version number of a document. You must also include `major_version_number__v` to use this parameter.

`remove_locked`optional

If set to `true`, removes a matched document from the EDL Item even if the EDL Item is locked to a specific steady state document version.

#### Response Details

On `SUCCESS`, the response includes a `SUCCESS` or `FAILURE` status and any applicable error messages for each matched document to remove from an EDL Item in the body of your request.
