<!-- 
VaultAPIDocs Section: # RIM Submissions Archive
Original Line Number: 42082
Generated: August 30, 2025
Part 34 of 38
-->

# RIM Submissions Archive

To use this API, you must have Veeva RIM Submissions Archive. Learn more about [RIM Submissions Archive in Vault Help](https://regulatory.veevavault.help/en/lr/30705).

## Import Submission

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "file=/nda123456/0000" \
https://myvault.veevavault.com/api/v25.2/vobjects/submission__v/00S000000000101/actions/import
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "warnings": [
    {
      "type": "APPLICATION_MISMATCH",
      "message": "Application folder name does not match the Application record name."
    },
    {
      "type": "SUBMISSION_MISMATCH",
      "message": "Submission folder name does not match the Submission record name."
    }
  ],
  "job_id": 1301,
  "url": "/api/v25.2/services/jobs/1301"
}
'''

Import a submission into your Vault.

Before submitting this request:

-   You must be assigned permissions to use the API and have permissions to view and edit the specified `submission__v` object record.
-   You must create the corresponding object records for the **Submission** and **Application** objects in your Vault.
-   You must create and upload a valid submission import file or folder to [file staging](/docs/#FTP). The submission to import must be in a [specific location and format](#Submission_Location_FTP).

#### Submission Import File Location & Structure

The submission import file must be located in one of the following places, and must be in a specific folder structure.

##### At the Root

If your submission import is located at the file staging root, it must follow the following structure:

`/SubmissionsArchive/``{application_folder}``/``{submission_file_or_folder}`

-   `{application_folder}`: This required folder can have any name you wish.
-   `{submission_file_or_folder}`: If this is a file containing your submission, it must be a `.zip` or `.tar.gz`. If this is a folder, it must contain your submission to import. This required folder can have any name you wish.

For example, `/SubmissionsArchive/``nda654321``/``0001.zip`.

##### Within a User Folder

In some cases, your [Vault user permissions](/docs/#FTP_Staging_Server_Perrmissions) may prevent you from uploading directly to the file staging root. In these cases, you must upload to your user folder using the following structure:

`/u[ID]/Submissions Archive Import/``{application_folder}``/``{submission_folder}`

-   `{application_folder}`: This required folder can have any name you wish.
-   `{submission_folder}`: The folder containing your submission to import. This required folder can have any name you wish. Vault does not support importing `.zip` or `.tar.gz` files from user folders.

For example, `/u5678/Submissions Archive Import/``nda123456``/``0013`.

#### Endpoint

POST `/api/{version}/vobjects/submission__v/{submission_id}/actions/import`

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

`{submission_id}`

The `id` field value of the `submission__v` object record. To get this value, [use VQL to retrieve all records](#Retrieve_Object_Record_Collection) on the `submission__v` object.

#### Body Parameters

Name

Description

`file`

Use the `file` parameter to specify the location of the submission folder or ZIP file previously uploaded to [file staging](/docs/#FTP). In the request, add the `file` parameter to your input and enter the path to the submission folder relative to the file staging root, for example, `/SubmissionsArchive/nda123456/0000`, or to the path to your user file staging folder, for example, `/u5678/Submissions Archive Import/nda123456/0000`. Vault does not support importing `.zip` or `.tar.gz` files from user folders.

#### Response Details

On `SUCCESS`, the response includes the following information:

-   `job_id` - The Job ID value is used to retrieve the [status](#Retrieve_Job_Status) and results of the binder export request.
-   `url` - The URL to retrieve the current status of the import request.

You may also receive one or more `warnings`. The `warnings` shown above indicate that the folders being imported do not match the object records in our Vault. To fix this warning, we can change the folder name or object record name. However, warnings are not fatal and you may choose to take no action.

Before submitting this request, we created a `submission__v` object record and `application__v` object record in our Vault. We also created submissions ZIP file containing a “Submission” folder and “Application” folder. This was loaded to file staging awaiting import. Ideally, we would have named and structured the folders to match that of the submission that was sent to the health authority and which we are now archiving. However, this is not critical to the import process.

## Retrieve Submission Import Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/submission__v/00S000000000101/actions/import/1301/results
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "data": [
    {
      "responseStatus": "SUCCESS",
      "id": 16,
      "major_version_number__v": "1",
      "minor_version_number__v": "0"
    }
  ]
}
'''

After Vault has finished processing the submission import job, use this request to retrieve the results of the completed submission binder.

Before submitting this request:

-   You must be assigned permissions to use the API and permissions to view the specified `submission__v` object record.
-   There must be a previously submitted and completed submission import request, i.e., the status of the import job must be no longer active.

GET `/api/{version}/vobjects/submission__v/{submission_id}/actions/import/{job_id}/results`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{submission_id}`

The `id` field value of the `submission__v` object record. To get this value, [use VQL to retrieve all records](#Retrieve_Object_Record_Collection) on the `submission__v` object.

`{job_id}`

The `jobId` field value returned from the [Import Submission](#Import_Submission) request above.

#### Response Details

On `SUCCESS`, the response includes the following information:

Field Name

Description

`id`

The `id` field value of the submission binder which was created by the imported files.

`major_version_number__v`

The major version number of the binder.

`minor_version_number__v`

The minor version number of the binder.

To retrieve the metadata from the newly created submission binder, send `GET` to `/api/{version}/objects/binders/{id}`.

## Retrieve Submission Metadata Mapping

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/submission__v/00S000000000101/actions/ectdmapping
'''

> Response

'''
{
 "responseStatus": "SUCCESS",
    "responseDetails": {
    "total": 2
    },
    "data": [
    {
      "name__v": "1675_00S000000000802",
      "external_id__v": null,
      "drug_substance__v":"Ethyl Alcohol",
      "drug_substance__v.name__v": "",
      "xml_id": "m2-3-s-drug-substance",
      "manufacturer__v":"Veeva",
      "manufacturer__v.name__v": ""
    },
    {
      "name__v": "1681_00S000000000802",
      "external_id__v": null,
      "nonclinical_study__v":"Study001",
      "nonclinical_study__v.name__v": "",
      "xml_id": "S001"
    }
  ]
}
'''

Retrieve the metadata mapping values of an eCTD submission package.

GET `/api/{version}/vobjects/submission__v/{submission_id}/actions/ectdmapping`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `text/csv`

#### URI Path Parameters

Name

Description

`{submission_id}`

The `id` field value of the `submission__v` object record. To get this value, [use VQL to retrieve all records](#Retrieve_Object_Record_Collection) on the `submission__v` object.

#### Response Details

On `SUCCESS`, the response includes the following information for each XML metadata node which requires mapping:

Field Name

Description

`name__v`

The name of the metadata mapping record in the submission metadata.

`external_id__v`

The external ID of the metadata mapping record. This value is only available if the mappings were created or updated externally.

`xml_id`

The XML ID (`leaf_id`) of the section being mapped. This is an identifier from the imported XML of the XML node. This is analogous to the `submission_metadata__v.tag_id__v`.

Mapping Fields:

Possible mappings include: `clinical_site__v`, `clinical_study__v`, `drug_product__v`, `drug_substance__v`, `indication__v`, `manufacturer__v`, and `nonclinical_study__v`.

Mapping fields are returned as a pair of properties: a source property that has the mapping identifier from the imported XML and a second property as `[mapping].name__v` which specifies the target object record. If the second property is empty, the mapping has not been completed. See [Update Submission Metadata Mapping](#Update_Submission_Metadata_Mapping) below.

## Update Submission Metadata Mapping

> Response

'''
[
    {
      "external_id__v": null,
      "drug_substance__v.name__v": "ethyl alcohol",
      "name__v": "1675_00S000000000802",
      "xml_id": "m2-3-s-drug-substance",
      "manufacturer__v.name__v": "Veeva Chemical"
    },
    {
      "external_id__v": null,
      "drug_substance__v.name__v": "ethyl alcohol",
      "name__v": "1677_00S000000000802",
      "xml_id": "m3-2-s-drug-substance",
      "manufacturer__v.name__v": "Veeva Chemical"
    },
    {
      "external_id__v": null,
      "nonclinical_study__v.name__v": "S001",
      "name__v": "1681_00S000000000802",
      "xml_id": "S001"
    },
    {
      "external_id__v": null,
      "clinical_study__v.name__v": "S001",
      "name__v": "1693_00S000000000802",
      "xml_id": "S001"
    }
]
'''

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/submission__v/00S000000000101/actions/ectdmapping
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "name__v": "1675_00S000000000802",
            "responseStatus": "SUCCESS"
        },
        {
            "name__v": "1677_00S000000000802",
            "responseStatus": "SUCCESS"
        },
        {
            "name__v": "1681_00S000000000802",
            "responseStatus": "SUCCESS"
        },
        {
            "name__v": "1693_00S000000000802",
            "responseStatus": "SUCCESS"
        }
    ],
    "responseDetails": {
        "total": 4
    }
}
'''

Update the mapping values of a submission.

PUT `/api/{version}/vobjects/submission__v/{submission_id}/actions/ectdmapping`

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

`{submission_id}`

The `id` field value of the `submission__v` object record. To get this value, [use VQL to retrieve all records](#Retrieve_Object_Record_Collection) on the `submission__v` object.

Note that XML identifiers are read-only and cannot be updated via the API. If including XML identifiers in the request, the values will be ignored.

## Remove Submission

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/submission__v/00S000000000101/actions/import
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "job_id": 15002,
  "url": "/api/v25.2/services/jobs/15002"
}
'''

Delete a previously imported submission from your Vault.

By removing a submission, you delete any sections created in the archive binder as part of the submission import. This will also remove any documents in the submission from the archive binder. This does not delete the documents from Vault, but does mean that they no longer appear in the Viewer tab and users will not be able to access them using cross-document navigation. You must re-import the submission to make it available.

DELETE `/api/{version}/vobjects/submission__v/{submission_id}/actions/import`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{submission_id}`

The `id` field value of the `submission__v` object record. To get this value, [use VQL to retrieve all records](#Retrieve_Object_Record_Collection) on the `submission__v` object.

## Cancel Submission

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/submission__v/00S000000000101/actions/import?cancel=true
'''

> Response

'''
{
  "responseStatus": "SUCCESS"
}
'''

You can use this request on a submission object record that has a Submissions Archive Status (`archive_status__v`) of:

Name

Description

`IMPORT_IN_PROGRESS`

This will terminate the import job and set the `archive_status__v` field on the `submission__v` object record to “Error”. The submission must be removed before a re-import can be done. See [Remove Submission](#Remove_Submission) above.

`REMOVAL_IN_PROGRESS`

This will terminate the import removal job and set the `archive_status__v` field on the `submission__v` object record to “Error”. The submission must be removed before a re-import can be done. See [Remove Submission](#Remove_Submission) above.

`IMPORT_IN_QUEUE`

This will remove the import from the job queue and set the `archive_status__v` field on the `submission__v` object record to “Null”. See [Import Submission](#Import_Submission) above.

`REMOVAL_IN_QUEUE`

This will remove the import removal from the job queue and set the `archive_status__v` field on the `submission__v` object record to “Error”. See [Import Submission](#Import_Submission) above.

To retrieve the `archive_status__v`, GET `/api/{version}/vobjects/submission__v/{submission_id}`. See [Retrieve Object Record](#Retrieve_Object_Record) above.

POST `/api/{version}/vobjects/submission__v/{submission_id}/actions/import?cancel=true`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{submission_id}`

The `id` field value of the `submission__v` object record. To get this value, [use VQL to retrieve all records](#Retrieve_Object_Record_Collection) on the `submission__v` object.

#### Query Parameters

Name

Description

`cancel`

You must include cancel = `true` to the request endpoint.

## Export Submission

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/454/actions/export?submission=00S000000000101
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "URL": "https://myvault.veevavault.com/api/v25.2/services/jobs/1201",
  "job_id": 1201
}
'''

Use the following requests to export the latest or most recent version of a Submissions Archive binder. These endpoints do not support the export of submissions binders published by RIM Submissions Publishing. Learn more about [RIM Submissions Publishing in Vault Help](https://regulatory.veevavault.help/en/lr/48611).

To export the latest version of a Submissions Archive binder:

POST `/api/{version}/objects/binders/{binder_id}/actions/export?submission={submission_id}`

To export a specific version of a Submissions Archive binder:

POST `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/actions/export?submission={submission_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{binder_id}`

The binder `id` field value. See [Retrieve Binders](#Retrieve_Binders) above.

`{major_version}`

The `major_version_number__v` field value of the binder.

`{minor_version}`

The `minor_version_number__v` field value of the binder.

`{submission_id}`

The `id` field value of the `submission__v` object record. To get this value, [use VQL to retrieve all records](#Retrieve_Object_Record_Collection) on the `submission__v` object.

#### Response Details

On `SUCCESS`, the response includes the following information:

-   `URL` - The URL to retrieve the current status of the export job.
-   `job_id` - The Job ID value is used to retrieve the [status](#RetrieveJobStatus) and results of the request.

## Export Partial Submission

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
--data-binary @"C:\Vault\Binders\export-submissions-binder-sections.csv" \
https://myvault.veevavault.com/api/v25.2/objects/binders/454/1/0/actions/export?submission=00S000000000101
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "URL": "https://myvault.veevavault.com/api/v25.2/services/jobs/1201",
  "job_id": 1201
}
'''

Use this request to export only specific sections and documents from the latest version of a submissions binder in your Vault. This will export only parts of the binder, not the complete binder. Exporting a binder section node will automatically include all of its subsections and documents therein.

Before submitting this request:

-   The Export Binder feature must be enabled in your Vault.
-   You must be assigned permissions to use the API.
-   You must have the _Export Binder_ permission.
-   You must have the _View Document_ permission for the binder. Only documents in the binder which you have the _View Document_ permission are available to export.

To export the latest version of a submissions binder:

POST `/api/{version}/objects/binders/{binder_id}/actions/export?submission={submission_id}`

To export a specific version of a submissions binder:

POST `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/actions/export?submission={submission_id}`

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

The binder `id` field value. See [Retrieve Binders](#Retrieve_Binders) above.

`{major_version}`

The `major_version_number__v` field value of the binder.

`{minor_version}`

The `minor_version_number__v` field value of the binder.

`{submission_id}`

The `id` field value of the `submission__v` object record. To get this value, [use VQL to retrieve all records](#Retrieve_Object_Record_Collection) on the `submission__v` object.

#### Body

Create a CSV or JSON input file with the `id` values of the binder sections and/or documents to be exported. You may include any number of valid nodes. Vault will ignore `id` values which are invalid.

#### Response Details

On `SUCCESS`, the response includes the following information:

-   `URL` - The URL to retrieve the current status of the export job.
-   `job_id` - The `job_id` field value is used to retrieve the [results](#Retrieve_Submission_Export_Results) of the export request.

## Retrieve Submission Export Results

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
  "file": "/1201/454/1_0/RIM Submission Packet.zip",
  "user_id__v": 44533
}
'''

After submitting a request to export a submission from your Vault, you can query Vault to determine the results of the request.

Before submitting this request:

-   You must have previously requested a submission export job (via the API) which is no longer active.
-   You must have a valid `job_id` field value returned from the [Export Submission](#Export_Submission) request above.

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

The `jobId` field value returned from the [Export Submission](#Export_Submission) request above.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`job_id`

The `job_id` field value of the submission export request.

`id`

The `id` field value of the exported submission.

`major_version_number__v`

The major version number of the exported submission.

`minor_version_number__v`

The minor version number of the exported submission.

`file`

The path/location of the exported submission. This is packaged in a ZIP file on file staging.

`user_id__v`

The `id` field value of the Vault user who initiated the submission export job.

### Download Exported Submission Files via File Staging

Once your submission export job has been successfully completed, you can download the files from [file staging](/docs/#FTP).

#### Prerequisites

Before downloading the files, the following conditions must be met:

-   The submission export job must have been successfully completed.
-   The API user must have a permission set which allows the _Application: File Staging: Access_ permission.

#### Downloading the Files

The exported submission is packaged in a ZIP file on file staging. [Learn more](/docs).
