<!-- 
VaultAPIDocs Section: # QualityDocs
Original Line Number: 41421
Generated: August 30, 2025
Part 29 of 38
-->

# QualityDocs

To use this API, you must have Veeva QualityDocs. Learn more about [QualityDocs in Vault Help](https://quality.veevavault.help/en/lr/5442).

## Document Role Check for Document Change Control

> Request

'''
curl -X POST
https://myvault.veevavault.com/api/v25.2/vobjects/document_change_control__v/00S000000000101/actions/documentrolecheck \
-H "Authorization: {SESSION_ID}" \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'application_role: approver__c'
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "data": {
    "check_result": true
  }
}
'''

Check if any document added to a _Document Change Control_ (DCC) record has one or more users in a specified _Application Role_. This API only checks documents added to the standard _Documents to be Released_ and _Documents to be Made Obsolete_ sections.

POST `/api/{version}/vobjects/document_change_control__v/{object_record_id}/actions/documentrolecheck`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_record_id}`

The `{id}` field value of the `document_change_control__v` object record.

#### Body Parameters

Name

Description

`{application_role}`

The name of the `application_role__v`.

#### Response Details

On `SUCCESS`, the response includes the Boolean `check_result` field. A value of `true` indicates that the given _Application Role_ is in use on at least one document in the given _Document Change Control_ record.
