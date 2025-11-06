<!-- 
VaultAPIDocs Section: # Vault Loader
Original Line Number: 38115
Generated: August 30, 2025
Part 23 of 38
-->

# Vault Loader

The following endpoints allow you to leverage Loader Services to load a set of data objects to your Vault or extract one or more data files from your Vault. Learn more about Vault Loader, such as limits and required permissions, [in Vault Help](https://platform.veevavault.help/en/lr/26597).

## Multi-File Extract

### Extract Data Files

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
--data-binary @"C:\Vault\Loader\extract_objects.json" \
https://myvault.veevavault.com/api/v25.2/services/loader/extract
'''

> Body

'''
[
{
  "object_type": "documents__v",
  "extract_options": "include_renditions__v",
  "fields":[
    "id",
    "name__v",
    "type__v"
    ],
    "vql_criteria__v":"site__v=123 MAXROWS 500 SKIP 100"
},
{   "object_type": "vobjects__v",
  "object": "product__v",
  "fields":[
    "id",
    "name__v",
    "object_type__v"
    ],
    "vql_criteria__v":"site__v=123 MAXROWS 500 SKIP 100"
    },
    {
  "object_type": "groups__v",
  "fields":[
    "id",
    "name__v"
    ]
    }
]
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "url": "/api/v25.2/services/jobs/61907",
    "job_id": 61907,
    "tasks": [
        {
            "task_id": "1",
            "object_type": "documents__v",
            "fields": [
                "id",
                "name__v",
                "type__v"
            ],
            "vql_criteria__v": "site__v=123 MAXROWS 500 SKIP 100",
            "extract_options": "include_renditions__v"
        },
        {
            "task_id": "2",
            "object_type": "vobjects__v",
            "object": "product__v",
            "fields": [
                "id",
                "name__v",
                "object_type__v"
            ],
            "vql_criteria__v": "site__v=123 MAXROWS 500 SKIP 100"
        },
        {
            "task_id": "3",
            "object_type": "groups__v",
            "fields": [
                "id",
                "name__v"
            ]
        }
    ]
}
'''

Create a Loader job to extract one or more data files. Learn more about [extracting data files with Vault Loader in Vault Help](https://platform.veevavault.help/en/lr/31536). You can extract a maximum of 10 data objects per request.

POST `/api/{version}/services/loader/extract`

#### Headers

Name

Description

`Accept`

`application/json`

`Content-Type`

`application/json`

#### Body Parameters

The body of your request should be a JSON file containing the set of data objects to extract.

Name

Description

`object_type`required

The type of data object to extract. The following values are allowed:

-   `vobjects__v`
-   `documents__v`
-   `document_versions__v`
-   `document_relationships__v`
-   `groups__v`

`object`conditional

If `object_type=vobjects__v`, include the object name. For example, `product__v`.

`extract_options`optional

Include to specify whether or not to extract renditions and/or source files for the `documents__v` and `document_versions__v` object types. The following values are allowed:

-   `include_source__v`
-   `include_renditions__v`

If omitted, Vault returns all document properties in the Retrieve Loader Results endpoint.

`fields`required

A JSON array with the field information for the specified object type. For example, `id`, `name__v`, `descriptions__v`, etc.

`vql_criteria__v`optional

A VQL-like expression used to optionally filter the data set to only those records that meet a specified criterion. Learn more about [Criteria VQL](/vql/#Criteria_VQL).

#### Query Parameters

Name

Description

`sendNotification`

To send a Vault notification when the job completes, set to `true`. If omitted, this defaults to `false` and Vault does not send a notification when the job completes.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`job_id`

The Job ID value to retrieve the [status](#RetrieveJobStatus) of the loader extract request.

`tasks`

A set of tasks with a `task_id` for each extract request.

### Retrieve Loader Extract Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/loader/61907/tasks/2/results
'''

> Response

'''
file,rendition_type__v,id,name__v,type__v
/61915/50/0_1/renditions/viewable_rendition__v.pdf,viewable_rendition__v,50,Facts about High Cholesterol Spring 2016,Promotional Material
/61915/8/0_1/renditions/viewable_rendition__v.pdf,viewable_rendition__v,8,ashley-harvey,Personnel
'''

After submitting a request to extract data files from your Vault, you can query Vault to retrieve the results of a specified job task.

GET `/api/{version}/services/loader/{job_id}/tasks/{task_id}/results`

#### Headers

Name

Description

`Accept`

`text/csv`

#### URI Path Parameters

Name

Description

`job_id`

The `id` value of the requested extract job. Obtain this from the [Extract Data Files](#Extract_Data_Files) request.

`task_id`

The `id` value of the requested extract task. Obtain this from the [Extract Data Files](#Extract_Data_Files) request.

#### Response Details

On `SUCCESS`:

-   If the Loader job task was successful, the response includes CSV output containing the results of a specific extract job task.
-   If the Loader job task was unsuccessful, the response is blank. To view the failure log, log into your Vault, go to **Admin > Operations > Job Status**, and select the Job ID from the History section.

If the extract includes document or document version renditions, the CSV output contains paths to rendition files on your Vault’s file staging. When an export includes multiple rendition types for a document or document version, the CSV output includes a separate row for each rendition type.

### Retrieve Loader Extract Renditions Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/loader/61907/tasks/1/results/renditions
'''

> Response

'''
file,rendition_type__v,id,name__v,type__v
/61915/50/0_1/renditions/viewable_rendition__v.pdf,viewable_rendition__v,50,Facts about High Cholesterol Spring 2016,Promotional Material
/61915/8/0_1/renditions/viewable_rendition__v.pdf,viewable_rendition__v,8,ashley-harvey,Personnel
'''

After submitting a request to extract object types from your Vault, you can query Vault to retrieve results of a specified job task that includes renditions requested with documents.

GET `/api/{version}/services/loader/{job_id}/tasks/{task_id}/results/renditions`

#### Headers

Name

Description

`Accept`

`text/csv`

#### URI Path Parameters

Name

Description

`job_id`

The `id` value of the requested extract job.

`task_id`

The `id` value of the requested extract task.

#### Response Details

On `SUCCESS`, the response includes CSV output containing paths to rendition files for documents or document versions on your Vault’s file staging. When an export includes multiple rendition types for a document or document version, the CSV output includes a separate row for each rendition type.

## Multi-File Load

### Load Data Objects

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
- H "Content-Type: application/json" \
--data-binary @"filename.json" \
https://myvault.veevavault.com/api/v25.2/services/loader/load
'''

> Body

'''
[
  {
    "object_type": "documents__v",
    "action": "create",
    "file": "documents.csv",
    "documentmigrationmode": true,
    "order": 1
  },
  {
    "object_type": "vobjects__v",
    "object": "veterinary_patient__c",
    "action": "create",
    "file": "patients.csv",
    "recordmigrationmode": true,
    "order": 2
  },
  {
    "object_type": "vobjects__v",
    "object": "product__v",
    "action": "upsert",
    "file": "products.csv",
    "order": 3,
    "idparam": "external_id__v"
  },
  {
    "object_type": "groups__v",
    "action": "update",
    "file": "groups.csv",
    "order": 4
  }
]
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "url": "/api/v25.2/services/jobs/92201",
    "job_id": 92201,
    "tasks": [
        {
            "task_id": "1",
            "object_type": "documents__v",
            "action": "create",
            "documentmigrationmode": true,
            "file": "documents.csv"
        },
        {
            "task_id": "2",
            "object_type": "vobjects__v",
            "object": "veterinary_patient__c",
            "action": "create",
            "recordmigrationmode": true,
            "file": "patients.csv"
        },
        {
            "task_id": "3",
            "object_type": "vobjects__v",
            "object": "product__v",
            "action": "upsert",
            "idparam": "external_id__v",
            "file": "products.csv"
        },
        {
            "task_id": "4",
            "object_type": "groups__v",
            "action": "update",
            "file": "groups.csv"
        }
    ]
}
'''

Create a loader job and load a set of data files. You can load a maximum of 10 data objects per request.

POST `/api/{version}/services/loader/load`

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json`

#### Body Parameters

The body of your request should be a JSON file containing the set of data objects to load.

Name

Description

`object_type`required

The type of data object to load. The following values are allowed:

-   `vobjects__v`
-   `documents__v`
-   `document_versions__v`
-   `document_relationships__v`
-   `groups__v`
-   `document_roles__v`
-   `document_versions_roles__v`
-   `document_renditions__v`
-   `document_attachments__v`

`object`conditional

If the `object_type` = `vobjects__v`, include the object name. For example, `product__v`.

`action`required

The action type to `create`, `update`, `upsert`, or `delete` data objects. If the `object_type`\=`vobjects__v`, the action types `create_attachments`, `delete_attachments`, `assign_roles`, and `remove_roles` are also available.

`file`required

Include the filepath to reference the CSV load file on [file staging](/docs/#FTP).

`order`optional

Specifies the order of the load task.

`idparam`optional

Identify object records by any unique field value. Can only be used if `object_type` is `vobjects__v` and `action` is `upsert`, `update`, or `delete`. You can use any object field which has `unique` set to `true` in the object metadata. For example, `idparam=external_id__v`.

`recordmigrationmode`optional

Set to `true` to create or update object records in a noninitial state and with minimal validation, bypass rules such as entry criteria, create inactive records, and set system-managed fields such as `created_by__v`. Does not bypass record triggers. Use `notriggers` to bypass triggers. The `recordmigrationmode` parameter can only be used if `object_type` is `vobjects__v` and `action` is `create`, `update`, or `upsert`. You must have the [Record Migration](https://platform.veevavault.help/en/lr/22824#vault-owner-actions) permission to use this parameter. Learn more about [Record Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/761685).

`notriggers`optional

If set to `true`, Record Migration Mode bypasses record triggers.

`documentmigrationmode`optional

Set to `true` to create documents, document versions, document version roles, or document renditions in a specific state or state type. Also allows you to set the name, document number, and version number. For `update` actions, only allows you to manually reset document numbers. You must have the [Document Migration](https://platform.veevavault.help/en/lr/22824#vault-owner-actions) permission to use this parameter. Learn more about [Document Migration Mode in Vault Help](https://platform.veevavault.help/en/lr/54028).

#### Query Parameters

Name

Description

`sendNotification`

To send a Vault notification when the job completes, set to `true`. If omitted, this defaults to `false` and Vault does not send a notification when the job completes.

#### About File Validation

Vault evaluates header rows in CSV load files to ensure they include all required fields. Required fields vary depending on the `object_type` and `action`. Learn more about Vault Loader input files for [documents](https://platform.veevavault.help/en/lr/26605#preparing), [document roles](https://platform.veevavault.help/en/lr/26613#preparing), [document attachments](https://platform.veevavault.help/en/lr/67267#prepare), [objects](https://platform.veevavault.help/en/lr/26607#prepare), and [object attachments](https://platform.veevavault.help/en/lr/67288#prepare) in Vault Help.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`job_id`

The Job ID value to retrieve the [status](#RetrieveJobStatus) of the loader extract request.

`tasks`

The `task_id` for each load request.

### Retrieve Load Success Log Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
- H "Content-Type: application/json" \
https://myveevavault.com/api/v25.2/services/loader/61907/tasks/1/successlog
'''

> Response

'''
responseStatus,id,name__v,external_id__v,errors,rowId,event,id_param__value
SUCCESS,00P000000000807,,,,1,created__sys,
SUCCESS,00P000000000808,,,,2,created__sys,
SUCCESS,00P000000000809,,,,3,updated__sys,00P000000000809
'''

Retrieve success logs of loader results.

GET `/api/{version}/services/loader/{job_id}/tasks/{task_id}/successlog`

#### Headers

Name

Description

`Accept`

`text/csv`

#### URI Path Parameters

Name

Description

`job_id`

The `id` value of the requested load job.

`task_id`

The `id` value of the requested load task.

#### Response Details

On `SUCCESS`, the response includes a CSV file with the success log of loader results.

The response may include the following additional information:

Metadata Field

Description

`event`

Whether the record was created (`created__sys`) or updated (`updated__sys`). Only included for upsert actions.

`id_param_value`

The value of the field specified by the `idparam` body parameter if provided when loading data objects. For example, if `idparam=external_id__v`, the `id_param_value` returned is the same as the record’s external ID.

### Retrieve Load Failure Log Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
- H "Content-Type: application/json" \
https://myveevavault.com/api/v25.2/services/loader/61907/tasks/1/failurelog
'''

> Response

'''
responseStatus,name__v
FAILURE/Versioning Documents
'''

Retrieve failure logs of the loader results.

GET `/api/{version}/services/loader/{job_id}/tasks/{task_id}/failurelog`

#### Headers

Name

Description

`Accept`

`text/csv`

#### URI Path Parameters

Name

Description

`job_id`

The `id` value of the requested load job.

`task_id`

The `id` value of the requested load task.

#### Response Details

On `SUCCESS`, the response includes a CSV file with the failure log of loader results.

The response may include the following additional information:

Metadata Field

Description

`id_param_value`

The value of the field specified by the `idparam` body parameter if provided when loading data objects. For example, if `idparam=external_id__v`, the `id_param_value` returned is the same as the record’s external ID.
