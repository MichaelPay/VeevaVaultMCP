<!-- 
VaultAPIDocs Section: # Clinical Operations
Original Line Number: 40339
Generated: August 30, 2025
Part 28 of 38
-->

# Clinical Operations

To use this API, you must have the appropriate Clinical application. Learn more about [Clinical Operations](https://clinical.veevavault.help/en/lr/44699) in Vault Help.

## Create EDLs

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
https://myvault.veevavault.com/api/v25.2/vobjects/study__v/00S07710/actions/etmfcreateedl
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "url": "https://myvault.veevavault.com/api/v25.2/services/jobs/1201",
  "job_id": 1201
}
'''

Create a new Expected Document List.

POST `/api/{version}/vobjects/study__v/{study_id}/actions/etmfcreateedl`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `text/csv`

#### URI Path Parameters

Name

Description

`{study_id}`

The ID of the study.

#### Query Parameters

Name

Description

`applyWhereEdlItemsExist`

Optional: If set to `true`, the Create EDL job is applied to existing EDLs. If omitted, defaults to `false`. This is analogous to the _Apply template where expected documents already exist_ option in the Vault UI.

## Recalculate Milestone Document Field

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
--data-binary @"recalculate_milestones.csv" \
https://myvault.veevavault.com/api/v25.2/objects/documents/milestones/actions/recalculate
'''

> Example CSV Input File

'''
id
7652
9875
541
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": "SUCCESS"
}
'''

Recalculate the`milestone__v` field on a specified set of documents.

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

POST `/api/{version}/objects/documents/milestones/actions/recalculate`

#### Headers

Name

Description

`Content-Type`

`text/csv`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Prepare a CSV input file with document `id` values in an `id` column. Invalid values or invalid columns are ignored.

## Apply EDL Template to a Milestone

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Accept: application/json" \
-d "edl_id=0EL000000000105" \
https://myvault.veevavault.com/api/v25.2/vobjects/milestone__v/0M0007710/actions/etmfcreateedl
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "job_id": 9901,
  "url": "/api/v25.2/services/jobs/9901"
}
'''

Apply an EDL template to a Milestone object record.

POST `/api/{version}/vobjects/milestone__v/{milestone_id}/actions/etmfcreateedl`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{milestone_id}`

The ID of the milestone.

#### Body Parameters

Field Name

Description

`edl_id`

The ID of the EDL template to apply to this milestone.

## Create Milestones from Template

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
https://myvault.veevavault.com/api/v25.2/vobjects/study__v/0ST000000000202/actions/createmilestones
'''

> Response

'''
{
  "responseStatus":"SUCCESS",
  "job_id":130902,
  "url": "/api/v25.2/services/jobs/130902"
}
'''

Use this request to initiate the [Create Milestones from Template](https://clinical.veevavault.help/en/lr/24430#about_milestone_templates) user action on a study, study country, or site.

POST `/api/{version}/vobjects/{object_name}/{object_record_id}/actions/createmilestones`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded` (default)

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value. This endpoint only works with the `study__v`, `study_country__v`, or `site__v` objects.

`{object_record_id}`

The object record ID field value.

#### Response Details

Name

Description

`job_id`

The ID value for the job.

`url`

URL to retrieve the current status of the job.

## Execute Milestone Story Events

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Clinical_Operations\story_events.csv" \
https://myvault.veevavault.com/api/v25.2/app/clinical/milestone/study_country__v/actions/applytemplate
'''

> Response

'''
"id","story_event__v","status","Job id/Error"
"0SC000000001001","OOV000000000102","SUCCESS","327801"
'''

Use this request to create Milestones based on specific Story Events for multiple studies, study countries, or sites. You can include up to 500 rows in the CSV input.

POST `/api/{version}/app/clinical/milestone/{object_name}/actions/applytemplate`

#### Headers

Name

Description

`Content-Type`

`text/csv`

`Accept`

`application/json` (default) or `text/csv`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value. This endpoint only works with the `study__v`, `study_country__v`, or `site__v` objects.

#### Body Parameters

The CSV file must have the following columns:

Name

Description

`id`

The object record ID for which to create a milestone. This record must be of the same object indicated in the `{object_name}` path parameter. Instead of `id`, you can use a unique field defined by the `idParam` query parameter.

`story_event__v`

Include the name or ID of a single story event to define the milestone sets to create. For example, `story_event__v=OOV000000000705` or `story_event__v.name__v=Candidate Country`.

`external_id__v`

Instead of `id`, you can use this user-defined object external ID.

#### Query Parameters

Name

Description

`idParam`

If you’re identifying objects in your input by a unique field, add `idParam={fieldname}` to the request endpoint. You can use any object field which has `unique` set to `true` in the object metadata, with the exception of picklists. For example, `idParam=external_id__v`.

#### Response Details

On `SUCCESS`, Vault returns the job ID.

## Generate Milestone Documents

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
"https://myvault.veevavault.com/api/v25.2/app/clinical/milestone/actions/generatemilestonedocuments"
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "SUCCESS": "Successfully generated milestone documents"
}
'''

Generate _Milestone Document_ records for up to 500 milestones. _Milestone Document_ records are used to display matched document details in the Milestone Workspace.

Learn more about the [Milestone Workplace in Vault Help](https://clinical.veevavault.help/en/gr/496924/).

POST `/api/{version}/app/clinical/milestone/actions/generatemilestonedocuments`

#### Headers

Name

Description

`Content-Type`

`text/csv`

#### Body Parameters

The CSV file must have a single column with the header `id`. List each milestone ID on a separate row below. Including more than 500 rows results in an error.

#### Response

On `SUCCESS`, Vault starts an _Add Expected Documents_ job to create the _Milestone Document_ records. On completion, Vault sends an email notification containing a link to download a list in CSV format of successfully created records.

## Veeva Site Connect: Distribute to Sites

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
https://myvault.veevavault.com/api/v25.2/app/clinical/safety_distributions/V56000000001004/actions/send
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "job_id": 93601,
        "message": "Distributing documents. You will receive a notification when processing is complete."
   }
}
'''

This API allows sponsors and CROs to send Safety reports and letters to Sites. Learn more about [Safety Distributions in Vault Help](https://clinical.veevavault.help/en/lr/65187).

POST `/api/{version}/app/clinical/safety_distributions/{id}/actions/send`

#### Headers

Name

Description

`Content-Type`

`application/json` (default)

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{id}`

The record ID of the Safety Distribution record to send. Must be in a _Ready_ or _Distributed_ state.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`job_id`

The Job ID value to retrieve the status and results of this request. Use this ID to query for the [job status](#RetrieveJobStatus).

## Populate Site Fee Definitions

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
-d '{ "target_study": "0ST000000006004", "source_study": [ "0ST000000006002", "0ST000000006003" ] }'
https://myvault.veevavault.com/api/v25.2/app/clinical/payments/populate-site-fee-definitions
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Success",
  "data": {
    "status": "SUCCESS",
    "source": "study__v",
    "num_site_fee_defs_created": 2,
    "num_site_fee_defs_duplicates": 2,
    "num_errors": 0
  }
}
'''

Given an existing study with Site Fee Definitions or an eligible Site Fee Template, automatically generate Site Fee Definitions for a new target study. This endpoint is only available in CTMS Vaults with the [Veeva Payments](https://clinical.veevavault.help/en/lr/58941) add-on.

POST `/api/{version}/app/clinical/payments/populate-site-fee-definitions`

#### Headers

Name

Description

`Content-Type`

`application/json` (default)

`Accept`

`application/json` (default)

#### Body Parameters

Name

Description

`target_study`

The new study to populate with Site Fee Definitions.

`source_study`

Optional: To copy the Site Fee Definitions from studies, include an array with the study IDs. You must choose either `source_study` or `source_template`.

`source_template`

Optional: To copy the Site Fee Definitions from Site Fee Templates, include an array with the template IDs. You must choose either `source_study` or `source_template`.

## Populate Procedure Definitions

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
- d '[
{
        "source_holder_object_name" : "study__v",
        "source_holder_object_ids" : ["0ST000000001001"],
        "destination_holder_object_name" : "study__v",
        "destination_holder_object_id" : "0ST000000003001"
}
]'
https://myvault.veevavault.com/api/v25.2/app/clinical/ctms/populate-procedure-definitions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "data": {
        "status": "SUCCESS",
        "source": "study__v",
        "numProcedureDefsCreated": 2,
        "numProcedureDefsDuplicates": 0,
        "numErrors": 0
    }
}
'''

Use this request to initiate the _Populate Procedure Definitions_ user action. This action creates _Procedure Definitions_ for a target study from a source study or an existing _Procedure Template_.

Learn more about [_Procedure Definitions_ in Vault Help](https://clinical.veevavault.help/en/lr/71912#procedure).

POST `/api/{version}/app/clinical/ctms/populate-procedure-definitions`

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json`

#### Body Parameters

Name

Description

`source_holder_object_name`required

The name of the object to create _Procedure Definitions_ from. Possible values are `study__v` or `procedure_template__v`.

`source_holder_object_ids`required

An array of study or _Procedure Template_ IDs to copy _Procedure Definitions_ from.

`destination_holder_object_name`required

The name of the object to create _Procedure Definitions_ for. This must always be `study__v`.

`destination_holder_object_id`required

The ID of the study to populate with _Procedure Definitions_.

#### Response Details

On `SUCCESS`, the response returns the number of _Procedure Definitions_ created, the number of duplicate _Procedure Definitions_ that exist for the indicated study, and the number of errors encountered.

## Initiate Clinical Record Merge

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
--data-binary @"clinical-records-to-merge.json" \
https://myvault.veevavault.com/api/v25.2/app/clinical/objects/person__sys/actions/merge
'''

> Example JSON Request Body

'''
[
   {
       "duplicate_record_id" : "V0B000000008002",
       "main_record_id" : "V0B000000007001"
   },
   {
       "duplicate_record_id" : "V0B000000008001",
       "main_record_id" : "V0B000000007001"
   }
]
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "data": {
        "jobID": "511601"
    }
}
'''

Initiate a record merge operation in bulk to eliminate duplicate Global Directory data in your Clinical Operations Vault. When merging two records together, you must select one record to be the `main_record_id` and one record to be the `duplicate_record_id`. The merging process updates all inbound references (including attachments) from other objects that point to the `duplicate` record and moves those over to the `main` record. Field values on the `main` record are not changed, and when the process is complete, the `duplicate` record is deleted. Record merges do not trigger [record triggers](/sdk/#About_Record_Triggers).

You can only merge two records together in a single operation, one `main` record and one `duplicate` record. This is called a merge set. If you have multiple `duplicate` records you wish to merge into the same `main` record, you need to create multiple merge sets and execute multiple record merges.

-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 10 merge sets.
-   The maximum number of concurrent merge requests is 500.

This request only supports record merges for the following objects:

-   _Person_ (`person__sys`)
-   _Organization_ (`organization__v`)
-   _Location_ (`location__v`)
-   _Contact Information_ (`contact_information__clin`)

Each object above must have **Enable Merges** configured and the initiating user must have the _Application: Object: Merge Records_ permission. To merge records for other objects in your Vault, use [Initiate Record Merge](#Initiate_Record_Merge). Learn more about [record merges for Clinical Operations in Vault Help](https://clinical.veevavault.help/en/lr/31637).

POST `/api/{version}/app/clinical/objects/{object_name}/actions/merge`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `text/csv`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object to merge. Possible values are `person__sys`, `organization__v`, `location__v`, and `contact_information__clin`.

#### Body Parameters

Upload parameters as a JSON or CSV file. You can merge up to 10 merge sets at once.

Name

Description

`duplicate_record_id`required

The ID of the `duplicate` record. Each `duplicate_record_id` can only be merged into one `main_record_id` record. When the merging process is complete, Vault deletes this record.

`main_record_id`required

The ID of the `main` record. The merging process updates all inbound references (including attachments) from other objects that point to the `duplicate` record and moves those over to the `main` record. Vault does not change field values on the `main` record.

#### Response Details

On `SUCCESS`, the job has successfully started and the response includes a `jobID`. On `FAILURE`, the job failed to start. There is no partial success.

## Enable Study Migration Mode

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
--data-binary @"C:\Vault\Studies\enable_migration_mode.json" \
https://myvault.veevavault.com/api/v25.2/app/clinical/studies/actions/enable_migration_mode
'''

> Example JSON Request Body

'''
[
    {
        "id": "0ST000000003001"
    },
    {
        "id": "0ST000000003003"
    }
]
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "data": [
        {
            "url": "/api/v25.2/services/jobs/547532",
            "job_id": "547532"
        }
    ]
}
'''

Enable Study Migration Mode for multiple _Study_ records. Sending a request to this endpoint initiates a job to set the `study_migration__v` field on _Study_ records and their related object records with the value `m__v`. You can enable Study Migration Mode for up to 500 _Study_ records in a single request.

When a _Study_ enters Study Migration Mode, Vault makes study-related object data for that study hidden and uneditable for non-Admin users. Study Migration Mode also bypasses record triggers for the target studies, such as calculating metrics and generating related records. Learn more about [status and archiving studies in Vault Help](https://clinical.veevavault.help/en/lr/4345/#managing-archived-studies). Learn more about [Clinical Study Migrations](/migration/#Clinical_Study_Migrations).

POST `/api/{version}/app/clinical/studies/actions/enable_migration_mode`

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json`

#### Body Parameters

In the body of the request, upload the following parameter as a CSV or JSON input file:

Name

Description

`id`required

The ID of the _Study_ record.

#### Response Details

On `SUCCESS`, the response includes the `jobID`, which you can use to retrieve the job status, and the `url`, which you can use to retrieve the current status of the job.

On `FAILURE`, the response returns the `study_id` of the record that resulted in the failure and an error message describing the reason for the failure. The entire request fails to process if you provide a _Study_ record that does not exist in your Vault or is already in Study Migration Mode.

## Disable Study Migration Mode

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
--data-binary @"C:\Vault\Studies\disable_migration_mode.json" \
https://myvault.veevavault.com/api/v25.2/app/clinical/studies/actions/disable_migration_mode
'''

> Example JSON Request Body

'''
[
    {
        "id": "0ST000000003001"
    },
    {
        "id": "0ST000000003003"
    }
]
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "data": [
        {
            "url": "/api/v25.2/services/jobs/547430",
            "job_id": "547430"
        }
    ]
}
'''

Disable Study Migration Mode for multiple _Study_ records. Sending a request to this endpoint initiates a job to clear the `study_migration__v` field on _Study_ records and their related object records. You can disable Study Migration Mode for up to 500 _Study_ records in a single request.

Learn more about [status and archiving studies in Vault Help](https://clinical.veevavault.help/en/lr/4345/#managing-archived-studies). Learn more about [Clinical Study Migrations](/migration/#Clinical_Study_Migrations).

POST `/api/{version}/app/clinical/studies/actions/disable_migration_mode`

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json`

#### Body Parameters

In the body of the request, upload the following parameter as a CSV or JSON input file:

Name

Description

`id`required

The ID of the _Study_ record.

#### Response Details

On `SUCCESS`, the response includes the `jobID`, which you can use to retrieve the job status, and the `url`, which you can use to retrieve the current status of the job.

On `FAILURE`, the response returns the `study_id` of the record that resulted in the failure and an error message describing the reason for the failure. The entire request fails to process if you provide a _Study_ record that does not exist in your Vault or is already out of Study Migration Mode.

## Retrieve OpenData Clinical Affiliations

> Request

'''
curl --location 'https://myvault.veevavault.com/api/v25.2/app/clinical/opendata/person__sys/V0B000000006002/affiliations' \
--header 'Accept: application/json' \
--header 'Authorization: {SESSION_ID}' \
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": "Success",
   "responseDetails": {
       "size": 1,
       "total": 1
   },
   "data": [
       {
           "contact_information": "OOU000000006005",
           "hco_opendata_id": "65c467c1a76607ca06e84145",
           "hcp_opendata_id": "V01243147864098735105",
           "organization_name": "School of Medicine",
           "customer_primary": true,
           "is_primary": true,
           "first_name": "Ashley",
           "middle_name": "Kiki",
           "last_name": "Terry",
           "suffix": null,
           "address_line_1": "132 My Street",
           "address_line_2": null,
           "city": "Kingston",
           "state": "us-ny",
           "country": "us",
           "email": "ashterry@veepharm.edu",
           "office_phone": null
       }
   ]
}

'''

Given a _Person_ or _Organization_ mapped to OpenData Clinical, retrieves contact information associated with the Investigator Site record.

This API returns a maximum of 100 records. If there are more than 100 records to return, Vault truncates records beyond 100 in the returned response. To retrieve more than 100 records, use [Direct Data API](/directdata/).

GET `/api/{version}/app/clinical/opendata/{object_name}/{record_id}/affiliations`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `text/csv`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object to merge. Possible values are `person__sys`, `organization__v`, `location__v`, and `contact_information__clin`.

`{record_id}`

The ID of the `person__sys` or `organization__v` record.

#### Response Details

On `SUCCESS`, the response contains information about the _Person_ or _Organization_ mapped to OpenData Clinical.

Name

Description

`size`

The total number of affiliated records returned in the response. Records beyond 100 are truncated. To retrieve more than 100 records, use [Direct Data API](/directdata/).

`total`

The total number of affiliated records for the given HCP or HCO.

`contact_information`

The record ID of the `contact_information__clin` record whose combination of `hcp_opendata_id__v` and `hco_opendata_id__v` match that of the `investigator_site` record for this entry. Blank value indicates that there is not a `contact_information__clin` in the Vault for this combination.

`customer_primary`

This value is `true` if the `contact_information__clin` is of object type `person_linked_contact_information__v`, false if not this type, and `null` if there is no corresponding `contact_information__clin` record.

`hco_opendata_id`

The `hco_opendata_id` value for the given `investigator_site` record.

`hcp_opendata_id`

The `hcp_opendata_id` value for the given `investigator_site` record.

`organization_name`

Name of the associated site matching the `hco_opendata_id`.

`first_name`

The first name of the associated investigator matching the `hcp_opendata_id`.

`middle_name`

The middle name of the associated investigator matching the `hcp_opendata_id`.

`last_name`

The last name of the associated investigator matching the `hcp_opendata_id`.

`suffix`

The suffix of the associated investigator in the pod database the provided matching the `hcp_opendata_id`.

`is_primary`

The `is_primary` value for the given `investigator_site` record.

`address_line_1`

The `address_line_1` value for the given `investigator_site` record.

`address_line_2`

The `address_line_2` value for the given `investigator_site` record.

`city`

The `city` value for the given `investigator_site` record.

`state`

The `state` value for the given `investigator_site` record.

`country`

The `country` value for the given `investigator_site` record.

`email`

The `email` value for the given `investigator_site` record.

`office_phone`

The `office_phone` value for the given `investigator_site` record.

## Change Primary Investigator Affiliation

> Request

'''
curl --location 'https://myvault.veevavault.com/api/v25.2/app/clinical/opendata/person__sys/primary_affiliations' \
--header 'Accept: application/json' \
--header 'Authorization: {SESSION_ID}' \
--data-raw '[
   {   "person_sys":"V0B000000006002",
       "hco_opendata_id":"65c467c1a76607ca06e84145"
   },
   {
       "person_sys":"V0B000000006007 ",
       "hco_opendata_id":"65c467c1a76607ca06e84148"
   }
]'
'''

> Response

'''
{
"responseStatus": "SUCCESS", 
"data": [ 
    { 
        "person__sys": "V0B000000006002", 
        "primary_affiliation_hco_id": "65c467c1a76607ca06e84145", 
        "old_affiliation_hco_id": "65c467c1a76607ca06e84144" 
    }, 
    { 
        "person__sys": "V0B000000006007", 
        "primary_affiliation_hco_id": "65c467c1a76607ca06e84149", 
        "old_affiliation_hco_id": "65c467c1a76607ca06e84148" 
    } 
    ]
}
'''

Change the Primary Affiliation of an Investigator mapped to OpenData Clinical in bulk. This API supports changes to existing OpenData Clinical investigators and requests to add new Investigators. Update or Create up to 100 records per request.

POST `/api/{version}/app/clinical/opendata/person__sys/primary_affiliations`

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json` (default) or `text/csv`

#### Body Parameters

In the body of the request, include a JSON input with the records to update. Maximum 100 records.

Name

Description

`person_sys`

The record ID of the `person__sys` record whose primary affiliation is being modified.

`hco_opendata_id`

The `hco_link_id` of the OpenData Clinical site that will now be used for the primary affiliation. This will be copied onto the contact information of type `person_linked_contact_information__v`.

#### Response Details

On `SUCCESS`, the response contains information about the _Person_ or _Organization_ mapped to OpenData Clinical.

Name

Description

`person__sys`

The `id` of the `person__sys` record whose primary affiliation has been modified.

`primary_affiliation_hco_id`

The `hco_opendata_id` of the affiliation that will now be used as primary for the investigator.

`old_affiliation_hco_id`

The `hco_opendata_id` of the affiliation that was previously used as primary for the investigator.
