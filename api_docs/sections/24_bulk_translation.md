<!-- 
VaultAPIDocs Section: # Bulk Translation
Original Line Number: 38709
Generated: August 30, 2025
Part 24 of 38
-->

# Bulk Translation

The Bulk Translation API allows you to translate messages in your Vault in bulk. These APIs allow you to quickly compile a list of messages for translation. The exported bulk translation file is editable in Excel, any text editor, or translation software. Learn more about [bulk translation in Vault Help](https://platform.veevavault.help/en/lr/13309/#about-bulk-translation).

There are four (4) types of message translation files:

-   Field Labels
-   System Messages
-   Notification Templates
-   User Account Emails

You must have the _Admin: Language: Edit_ permission to use these endpoints.

## Export Bulk Translation File

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/messages/field_labels__sys/language/en/actions/export
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "jobId": "902101",
        "url": "/api/v25.2/services/jobs/902101"
    }
}
'''

> Response: Retrieve Job Status

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "id": 902101,
       "status": "SUCCESS",
       "links": [
           {
               "rel": "self",
               "href": "/api/v25.2/services/jobs/902101",
               "method": "GET",
               "accept": "application/json"
           },
           {
               "rel": "file",
               "href": "/api/v25.2/services/file_staging/items/PromoMats_English_Field-Labels_5-29-24_15-34-10.csv",
               "method": "GET",
               "accept": "application/json"
           },
           {
               "rel": "content",
               "href": "/api/v25.2/services/file_staging/items/content/PromoMats_English_Field-Labels_5-29-24_15-34-10.csv",
               "method": "GET",
               "accept": "application/octet-stream;charset=UTF-8"
           }
       ],
       "created_by": 61603,
       "created_date": "2024-05-29T21:34:11.000Z",
       "run_start_date": "2024-05-29T21:34:11.000Z",
       "run_end_date": "2024-05-29T21:34:20.000Z"
   }
}
'''

Export a bulk translation file from your Vault. The exported bulk translation file is a CSV editable in any text editor or translation software. You can request one (1) message type in one (1) language per request. Learn more about the [translation file schema in Vault Help](https://platform.veevavault.help/en/lr/13309/#field-labels-and-system-messages-translation-file).

This request starts an asynchronous job that exports the translation file to your Vault’s file staging. You can then download this file with the [Download Item Content](#Get_Item_Content) request.

You must have the _Admin: Language: Read_ permission to export a bulk translation file from Vault.

POST `/api/{version}/messages/{message_type}/language/{lang}/actions/export`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{message_type}`

The message type name: `field_labels__sys`, `system_messages__sys`, `notification_template_messages__sys`, or `user_account_messages__sys`.

`{lang}`

A valid language code value, for example, `en`. Retrieve available values from the _Admin Key_ (`admin_key__sys`) field on the _Language_ (`language__sys`) object. _Active_ and _Inactive_ languages are both valid.

#### Response Details

On `SUCCESS`, the response includes the `url` and `job_id` of the job. You can use this to [retrieve the status](#Retrieve_Job_Status) and results of the request.

When the job is complete, the translation files are available on your Vault’s file staging. Retrieving the job status of this completed job provides the `href` to [download the CSV](#Get_Item_Content) from file staging.

## Import Bulk Translation File

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-d "file_path=PromoMats_English_Field-Labels_5-29-24_15-34-10.csv" \
https://myvault.veevavault.com/api/v25.2/messages/field_labels__sys/actions/import
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "url": "/api/v25.2/services/jobs/902601",
        "jobId": "902601"
    }
}
'''

Import a bulk translation file into Vault. While an exported bulk translation file can contain only one (1) language, your import file may include multiple languages. Vault reads the language value separately for each row and applies any new translations immediately. Vault ignores any rows without changes. Learn more about the [translation file schema in Vault Help](https://platform.veevavault.help/en/lr/13309/#field-labels-and-system-messages-translation-file).

You must have the _Admin: Language: Edit_ permission to import a bulk translation file to Vault.

Upload the CSV file to your Vault’s file staging before making this request.

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).

POST `/api/{version}/messages/{message_type}/actions/import`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/x-www-form-urlencoded`

#### URI Path Parameters

Name

Description

`{message_type}`

The message type name: `field_labels__sys`, `system_messages__sys`, `notification_template_messages__sys`, or `user_account_messages__sys`.

#### Body Parameters

Name

Description

`file_path`

The file path of the CSV file on file staging. Cannot contain `../` or any other path traversal directives.

#### Response Details

On `SUCCESS`, the response includes the `job_id` which allows you to:

-   [Retrieve the job status](#Retrieve_Job_Status), which specifies if the import job has completed with `SUCCESS`
-   [Retrieve the job summary](#Translation_Summary), which provides details of a successful job
-   [Retrieve the job errors](#Translation_Errors), which provides details about the errors encountered in the job (if any)

## Retrieve Import Bulk Translation File Job Summary

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/jobs/902601/summary
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "ignored": 14057,
       "updated": 14,
       "failed": 179,
       "added": 0
   }
}
'''

After submitting a request to import a bulk translation file, you can query Vault to determine the results of the request.

Before submitting this request:

-   You must have previously requested an [Import Bulk Translation File](#Import_Bulk_Translation) job (via the API) which is no longer active
-   You must be the user who initiated the job or have the _Admin: Jobs: Read_ permission

GET `/api/{version}/services/jobs/{job_id}/summary`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{job_id}`

The `id` value of the requested import job. This was returned from the [Import Bulk Translation File](#Import_Bulk_Translation) request.

#### Response Details

On `SUCCESS`, the response includes the following `data`:

-   `ignored`: The number of rows that were ignored. For example, Vault ignores any rows without changes.
-   `updated`: The number of existing rows that were updated successfully.
-   `failed`: The number of rows that attempted an update but failed. Use the [Retrieve Import Bulk Translation File Job Errors](#Translation_Errors) endpoint to retrieve details about these rows.
-   `added`: The number of new rows that were added.

## Retrieve Import Bulk Translation File Job Errors

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/jobs/902601/errors
'''

> Response

'''
"Line Number","Error Message"
"3760","line 3,760: Translation of ""objectStateBehavior.glossary_definition_lifecycle__sys#approved_state__sys#change_state_to_draft_useraction1__sys.label"" not supported"
"3762","line 3,762: Translation of ""objectStateBehavior.glossary_definition_lifecycle__sys#approved_state__sys#change_state_to_withdrawn_useraction__sys.label"" not supported"
"3764","line 3,764: Translation of ""objectStateBehavior.glossary_definition_lifecycle__sys#draft_state__sys#change_state_to_in_review_useraction__sys.label"" not supported"
"3766","line 3,766: Translation of ""objectStateBehavior.glossary_definition_lifecycle__sys#in_review_state__sys#change_state_to_approved_useraction__sys.label"" not supported"
"3768","line 3,768: Translation of ""objectStateBehavior.glossary_definition_lifecycle__sys#in_review_state__sys#change_state_to_draft_useraction__sys.label"" not supported"
"3770","line 3,770: Translation of ""objectStateBehavior.glossary_definition_lifecycle__sys#withdrawn_state__sys#change_state_to_draft_useraction2__sys.label"" not supported"
'''

After submitting a request to import a bulk translation file, you can query Vault to determine the errors from the request (if any).

Before submitting this request:

-   You must have previously requested an [Import Bulk Translation File](#Import_Bulk_Translation) job (via the API) which is no longer active
-   You must be the user who initiated the job or have the _Admin: Jobs: Read_ permission

GET `/api/{version}/services/jobs/{job_id}/errors`

#### Headers

Name

Description

`Accept`

`text/csv`

#### URI Path Parameters

Name

Description

`{job_id}`

The `id` value of the requested import job. This was returned from the [Import Bulk Translation File](#Import_Bulk_Translation) request.

#### Response Details

On `SUCCESS`, the response includes the line number and error message for any errors encountered in the job.
