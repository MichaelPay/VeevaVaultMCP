<!-- 
VaultAPIDocs Section: # Batch Release
Original Line Number: 41582
Generated: August 30, 2025
Part 31 of 38
-->

# Batch Release

To use this API, you must have Veeva Batch Release. Learn more about [Batch Release in Vault Help](https://quality.veevavault.help/en/lr/700756/).

## Create Disposition

> Request

'''
curl --location 'https://myvault.veevavault.com/api/v25.2/app/quality/batch_release/disposition' \
--header 'Authorization: {SESSION_ID}' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "batch_id":"VB6000000001001",
    "disposition_plan":"DP-000001"
}'
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseDetails": {
       "job_id": "392501"
   }
}
'''

Create a _Batch Disposition_ record from an existing _Batch_ and _Batch Disposition Plan_. Learn more about [Batch Release in Vault Help](https://quality.veevavault.help/en/lr/700756/).

POST `/api/{version}/app/quality/batch_release/disposition`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/json`

#### Body Parameters

Include parameters as JSON.

Name

Description

`batch_id`required

The ID of the batch for the disposition, for example, `VB6000000001001`. You can find this by using [Retrieve Object Records](#Retrieve_Object_Record_Collection) or in the URL of the _Batch_ record detail page in the Vault UI.

`disposition_plan`required

The name of the disposition plan, for example, `DP-000001`.

#### Response Details

On `SUCCESS`, Vault returns the `job_id` for the _Add Disposition_ job.
