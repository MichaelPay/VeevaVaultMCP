<!-- 
VaultAPIDocs Section: # Logs
Original Line Number: 35235
Generated: August 30, 2025
Part 21 of 38
-->

# Logs

Vault provides several APIs to track actions performed in the system. The Audit APIs retrieve information about audits and audit types. Use the Audit History APIs to retrieve the audit history for specific document or object records. Download Daily API Usage retrieves the API Usage Logs for a specified date.

## Audit

Vault provides robust audit trail and audit logs of all actions performed in the system. These include actions on the documents, objects, the system, logins, and domain levels.

Through the Audit APIs, you can:

-   Retrieve audit types you have access to
-   Retrieve all fields and their metadata for a specific audit type
-   Retrieve all records in the specified audit type

Learn about [Audit Trails](https://platform.veevavault.help/en/lr/517) & [Audit Logs in Vault Help](https://platform.veevavault.help/en/lr/14341).

### Retrieve Audit Types

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/audittrail
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "audittrails": [
        {
            "name": "document_audit_trail",
            "label": "Document Audit Trail",
            "url": "/api/v25.2/metadata/audittrail/document_audit_trail"
        },
        {
            "name": "object_audit_trail",
            "label": "Object Audit Trail",
            "url": "/api/v25.2/metadata/audittrail/object_audit_trail"
        },
        {
            "name": "system_audit_trail",
            "label": "System Audit Trail",
            "url": "/api/v25.2/metadata/audittrail/system_audit_trail"
        },
        {
            "name": "domain_audit_trail",
            "label": "Domain Audit Trail",
            "url": "/api/v25.2/metadata/audittrail/domain_audit_trail"
        },
        {
            "name": "login_audit_trail",
            "label": "Login Audit Trail",
            "url": "/api/v25.2/metadata/audittrail/login_audit_trail"
        }
    ]
}
'''

Retrieve all available audit types you have permission to access.

GET `/api/{version}/metadata/audittrail`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

Name

Description

`name`

Name of the audit type.

`label`

Label of the audit type as seen in the API and UI.

`url`

URL to retrieve the metadata associated with the audit type.

### Retrieve Audit Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/audittrail/login_audit_trail
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "name": "login_audit_trail",
        "label": "Login Audit Trail",
        "fields": [
            {
                "name": "id",
                "label": "ID",
                "type": "Number"
            },
            {
                "name": "timestamp",
                "label": "Timestamp",
                "type": "DateTime"
            },
            {
                "name": "user_name",
                "label": "User Name",
                "type": "String"
            },
            {
                "name": "full_name",
                "label": "Full Name",
                "type": "String"
            },
            {
                "name": "source_ip",
                "label": "Source IP",
                "type": "String"
            }
        ]
    }
}
'''

Retrieve all fields and their metadata for a specified audit trail or log type.

GET `/api/{version}/metadata/audittrail/{audit_trail_type}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{audit_trail_type}`

The name of the specified audit type (`document_audit_trail`, `object_audit_trail`, etc).

### Retrieve Audit Details

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/audittrail/login_audit_trail
'''

> Response

'''
{
    "responseDetails": {
        "offset": 0,
        "limit": 200,
        "size": 7,
        "total": 7,
        "object": {
            "name": "login_audit_trail",
            "label": "Login Audit Trail",
            "url": "/api/v25.2/metadata/audittrail/login_audit_trail"
        }
    },
    "data": [
        {
            "id": "152515375538",
            "timestamp": "2017-09-15T16:07:25Z",
            "user_name": "lgills@veepharm.com",
            "full_name": "Lateef Gills",
            "source_ip": "209.136.227.195",
            "type": "User Login",
            "status": "Success",
            "browser": "Unknown",
            "platform": "Unknown"
        },
        {
            "id": "152515371157",
            "timestamp": "2017-09-14T14:19:05Z",
            "user_name": "c.brandon@veepharm.com",
            "full_name": "Cody Brandon",
            "source_ip": "162.218.77.23",
            "type": "Enterprise Home Authentication",
            "status": "Success",
            "browser": "Chrome 60.0.3112.113",
            "platform": "Intel Mac OS X 10.12.6"
        }
    ],
    "responseStatus": "SUCCESS"
}
'''

Retrieve all audit details for a specific audit type. This request supports optional parameters to narrow the results to a specified date and time within the past 30 days.

You can run a full audit export with the same formatting as exports you initiate in the UI once per day per audit type. To execute a full audit export, set `all_dates` to true, leave `start_date` and `end_date` blank, and set `format_result` to `csv`. When the job is complete, you will receive an email containing links to a zipped file for each year.

GET `/api/{version}/audittrail/{audit_trail_type}`

#### Headers

Name

Description

`Accept`

`application/json` (default)

#### URI Path Parameters

Name

Description

`{audit_trail_type}`

The name of the specified audit type (`document_audit_trail`, `object_audit_trail`, etc.). Use the [Retrieve Audit Types API](#Retrieve_Audit_Types) to retrieve types available in your Vault. Requests for `login_audit_trail` only accept one request per user at a time.

#### Query Parameters

You can modify the request by using one or more of the following parameters:

Name

Description

`start_date`

Specify a start date to retrieve audit information. This date cannot be more than 30 days ago. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2016 would use `2016-01-15T07:00:00Z`. If omitted, defaults to the start of the previous day.

`end_date`

Specify an end date to retrieve audit information. This date cannot be more than 30 days ago. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2016 would use `2016-01-15T07:00:00Z`. If omitted, defaults to the current date and time.

`all_dates`

Set to `true` to request audit information for all dates. You must leave `start_date` and `end_date` blank when requesting an export of a full audit trail. You can only run a full audit export (`all_dates = true`) on each audit type once every 24 hours.

`format_result`

To request a downloadable CSV file of your audit details, use `csv`. The response contains a `jobId` to retrieve the job status, which contains a link to download the CSV file. If omitted, the API returns a JSON response and does not start a job. If `all_dates` is `true`, this parameter is required.

`limit`

Paginate the results by specifying the maximum number of histories per page in the response. This can be any value between `1` and `1000`. If omitted, defaults to `200`.

`offset`

Paginate the results displayed per page by specifying the amount of offset from the entry returned. For example, if you are viewing the first 50 results (page 1) and want to see the next page, set this to `offset=51`. If omitted, defaults to `0`.

`objects`

This is an optional parameter when specifying `object_audit_trail` as the `{audit_trail_type}`. Provide a comma-separated list of one or more object names to retrieve their audit details. For example, `objects=product__v,country__v`. If omitted, defaults to all objects.

`events`

This is an optional parameter when specifying `object_audit_trail` or `document_audit_trail` as the `{audit_trail_type}`. Provide a comma-separated list of one or more audit events to retrieve their audit details. For example, `events=Edit,Delete,TaskAssignment`. If omitted, defaults to all audit events. See Vault Help for full lists of [object audit events](https://platform.veevavault.help/en/lr/74202) and [document audit events](https://platform.veevavault.help/en/lr/30435).

Dates and times are in UTC. If the time is not specified, it will default to midnight (T00:00:00Z) on the specified date.

#### Response Details

On `SUCCESS`, the response lists all rows and fields for the specified audit trail type. For example:

Name

Description

`id`

The unique audit trail ID.

`timestamp`

Date and time that the action was performed.

`user_name`

Login name for the user who performed the action. This may show “System” to indicate the action was completed by Vault.

`full_name`

The full name of the user who performed the action.

`on_behalf_of`

If the action completed by `user_name` was representing a different user (such as through [delegated access](https://platform.veevavault.help/en/lr/15015)), this field is the delegating user’s user name. For example, in the case of “tibanez@veepharm.com on behalf of mmurray@veepharm.com,” the `user_name` is tibanez@veepharm.com who completed the action `on_behalf_of` mmurray@veepharm.com.

Note that Vault returns additional fields based on the specified audit type. For example, if the audit type is `object_audit_trail`, Vault returns the `action` field denoting the audit event.

Requesting a CSV file generates a job to prepare the file for download. On `SUCCESS`, the response includes the `jobId` with a link to the CSV file.

When you export a full audit trail (`all_dates = true` and `format_result = csv`,) the response does not include a link to the CSV file. You will instead receive an email when the job is complete. The email contains a download link for each year to Excel files (one file per month for the current year, one file per year for each previous year) of the audit trail.

Name

Description

`url`

The URL to retrieve the current status of the CSV job.

`jobId`

The job ID value is used to retrieve the status and results of the audit trail CSV request.

## Audit History

With this API, you can retrieve the complete audit history of all actions performed for a specified document or object record. For other audit histories, see [Retrieve Audit Details](#Retrieve_Audit_Details).

### Retrieve Complete Audit History for a Single Document

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/42/audittrail?start_date=2021-04-22T23:00:00Z&end_date=2021-04-24T23:00:00Z
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseDetails": {
       "offset": 0,
       "limit": 200,
       "size": 2,
       "total": 2,
       "object": {
           "name": "document_audit_trail",
           "label": "Document Audit Trail",
           "url": "/api/v25.2/metadata/audittrail/document_audit_trail"
       }
   },
   "data": [
       {
           "id": "404",
           "timestamp": "2021-04-23T23:28:38Z",
           "user_name": "olive@veepharm.com",
           "full_name": "Olivia Cattington",
           "action": "EditDocRelationships",
           "item": "VV-00016",
           "field_name": "Supporting Documents",
           "old_value": null,
           "new_value": "VV-00003",
           "workflow_name": null,
           "task_name": null,
           "signature_meaning": null,
           "view_license": null,
           "job_instance_id": null,
           "doc_id": "42",
           "version": "0.1",
           "document_url": "/ui/#doc_info/42/0/1",
           "event_description": "\"VV-00003\" was added as a \"Supporting Documents\" relation"
       },
       {
           "id": "403",
           "timestamp": "2021-04-23T23:28:04Z",
           "user_name": "olive@veepharm.com",
           "full_name": "Olivia Cattington",
           "action": "GetDocumentVersion",
           "item": "VV-00016",
           "field_name": null,
           "old_value": null,
           "new_value": null,
           "workflow_name": null,
           "task_name": null,
           "signature_meaning": null,
           "view_license": null,
           "job_instance_id": null,
           "doc_id": "42",
           "version": "0.1",
           "document_url": "/ui/#doc_info/42/0/1",
           "event_description": "Viewed Document"
       }
   ]
}
'''

Retrieve complete audit history for a single document.

GET `/api/{version}/objects/documents/{doc_id}/audittrail`

#### Headers

Name

Description

`Accept`

`application/json` (default)

#### URI Path Parameters

Name

Description

`{doc_id}`

The document ID for which to retrieve audit history.

#### Query Parameters

Name

Description

`start_date`

Specify a start date to retrieve audit history. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2018 would use `2018-01-15T07:00:00Z`. If omitted, defaults to the Vault’s creation date.

`end_date`

Specify an end date to retrieve audit history. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2018 would use `2018-01-15T07:00:00Z`. If omitted, defaults to today’s date.

`format_result`

To request a CSV file of your audit history, use `csv`. The CSV file ignores the `start_date` and `end_date`.

`limit`

Paginate the results by specifying the maximum number of histories per page in the response. This can be any value between `1` and `1000`. If omitted, defaults to `200`.

`offset`

Paginate the results displayed per page by specifying the amount of offset from the entry returned. For example, if you are viewing the first 50 results (page 1) and want to see the next page, set this to `offset=51`. If omitted, defaults to `0`.

`events`

Provide a comma-separated list of one or more audit events to retrieve their audit history. See Vault Help for a full list of [document audit events](https://platform.veevavault.help/en/lr/30435). The values passed to this parameter are case sensitive. For example, `events=WorkflowCompletion,TaskAssignment`. If omitted, defaults to all audit events.

Dates and times are in UTC. If the time is not specified, it will default to midnight (T00:00:00Z) on the specified date.

#### Response Details

On `SUCCESS`, the response includes some of the following metadata:

Name

Description

`action`

The name of the action performed on the document. For example, `EditDocRelationships`.

`item`

The document number field value.

`signature_meaning`

The reason a signature was required for any manifested signature.

`view_license`

Returns a value of `View-Based User` only when the user is assigned that license type. Otherwise, returns an empty string.

`event_description`

Description of the action that occurred, for example, “Viewed Document”. Note that when data changes, the description shows both the previous value and the new value.

### Retrieve Complete Audit History for a Single Object Record

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/00P000000000119/audittrail?start_date=2021-04-22T23:00:00Z&end_date=2021-04-23T23:43:00Z
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseDetails": {
       "offset": 200,
       "limit": 200,
       "size": 1,
       "total": 1,
       "object": {
           "name": "object_audit_trail",
           "label": "Object Audit Trail",
           "url": "/api/v25.2/metadata/audittrail/object_audit_trail"
       },
       "previous_page": "/api/v25.2/vobjects/product__v/00P000000000119/audittrail?offset=0&limit=200&uuid=dcff7510-0143-4487-bafe-77d7e63059a2"
   },
   "data": [
       {
           "id": "1807",
           "timestamp": "2021-04-23T23:41:43Z",
           "user_name": "olive@veepharm.com",
           "full_name": "Olivia Cattington",
           "action": "Edit",
           "item": "Product : Gludacta",
           "field_label": "Compound ID",
           "field_name": "compound_id__v",
           "old_value": null,
           "new_value": "null",
           "old_display_value": null,
           "new_display_value": "751789",
           "record_id": "00P000000000119",
           "object_label": "Product",
           "object_name": "product__v",
           "workflow_name": null,
           "task_name": null,
           "verdict": null,
           "reason": null,
           "capacity": null,
           "event_description": "\"Compound ID\" set to \"751789\" ",
           "on_behalf_of": null,
           "grouping_id": "0b9be03a-c89f-488c-b255-5fd548ac5565"
       }
   ]
}
'''

Retrieve complete audit history for a single object record.

Vault does not audit individual field values for newly created records. For example, the audit trail for a new _Product_ record would only include a single entry, and the _Event Description_ would be “Product: CholeCap created”. We recommend [exporting the current record](#Retrieve_Object_Record) along with the audit trail to ensure a complete export of all values. When a user deletes an object record, the audit trail captures all field values.

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/audittrail`

#### Headers

Name

Description

`Accept`

`application/json` (default)

#### URI Path Parameters

Name

Description

`{object_name}`

The `name__v` of the object for which to retrieve audit history.

`{object_record_id}`

The object record ID for which to retrieve audit history.

#### Query Parameters

Name

Description

`start_date`

Specify a start date to retrieve audit history. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2018 would use `2018-01-15T07:00:00Z`. If omitted, defaults to the Vault’s creation date.

`end_date`

Specify an end date to retrieve audit history. Dates must be `YYYY-MM-DDTHH:MM:SSZ` format, for example, 7AM on January 15, 2018 would use `2018-01-15T07:00:00Z`. If omitted, defaults to today’s date.

`format_result`

To request a CSV file of your audit history, use `csv`.

`limit`

Paginate the results by specifying the maximum number of histories per page in the response. This can be any value between `1` and `1000`. If omitted, defaults to `200`.

`offset`

Paginate the results displayed per page by specifying the amount of offset from the entry returned. For example, if you are viewing the first 50 results (page 1) and want to see the next page, set this to `offset=51`. If omitted, defaults to `0`.

`events`

Provide a comma-separated list of one or more audit events to retrieve their audit history. See Vault Help for a full list of [object audit events](https://platform.veevavault.help/en/lr/74202). The values passed to this parameter are case sensitive. For example, `events=Copy,Edit,Delete`. If omitted, defaults to all audit events.

Dates and times are in UTC. If the time is not specified, it will default to midnight (T00:00:00Z) on the specified date.

#### Response Details

On `SUCCESS`, the response includes some of the following metadata:

Name

Description

`action`

The name of the action performed on the object record.

`item`

The name of the object and record.

`event_description`

Description of the action that occurred.

`migration_mode`

Indicates that the object record was created using the `X-VaultAPI-MigrationMode` header. When creating or updating records in migration mode, Vault bypasses entry criteria, entry actions, event actions, validation rules, and reference constraints and allows you to create or update object records in a specific state or state type.

`grouping_id`

The grouping ID that groups audit entries based on a single transaction.

## SDK Debug Log

From the _Logs_ tab in Vault (**Admin > Logs > Developer Logs**), you can view the _Debug Log_. The debug log captures custom Vault Java SDK code execution details and Vault messages at the user-level. This log is not always on by default. To capture data in the debug log, a Vault Admin must set up a debug log session for a particular user. A user can have only one (1) debug log configured for them at a time, and a Vault can have up to 20 users with debug log sessions configured.

Debug logs expire after 30 days. At the end of 30 days, Vault deletes the debug log and all log files.

By default, the _Vault Owner_ and _System Admin_ security profiles have permission to view the debug log and set up debug log sessions for a particular user.

Learn more about the [Debug Log](/sdk/#Debug_Log).

### Retrieve All Debug Logs

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/logs/code/debug
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "id": "0LS000000003006",
            "name": "Record Trigger Troubleshooting",
            "user_id": 61603,
            "log_level": "all__sys",
            "expiration_date": "2025-01-11T03:09:47.000Z",
            "class_filters": [
                {
                    "name": "com.veeva.vault.custom.triggers.HelloWorld",
                    "code_type": "Recordtrigger"
                }
            ],
            "status": "active__sys",
            "created_date": "2024-12-12T03:09:47.000Z"
        }
    ]
}
'''

Retrieve all [debug log](/sdk/#Debug_Log) sessions in the authenticated Vault.

GET `/api/{version}/logs/code/debug`

#### Headers

Name

Description

`Accept`

`application/json`

#### Query String Parameters

Name

Description

`user_id`optional

Filter results to retrieve the debug log for this user ID only. If omitted, this request retrieves debug logs for all users in the Vault.

`include_inactive`optional

Set to `true` to include debug log sessions with a `status` of `inactive__sys` in the response. If omitted, defaults to `false` and inactive sessions are not included in the response.

#### Response Details

On `SUCCESS`, the response includes the following `data` for each debug log:

Name

Description

`id`

The numerical ID of this debug log.

`name`

The UI name of this debug log.

`user_id`

The ID of the user associated with this debug log.

`log_level`

The level of error messages captured in this debug log. Learn more about the [log level types in Vault Help](https://platform.veevavault.help/en/lr/14341/#debug-log).

`expiration_date`

The date this session will expire, in the format `YYYY-MM-DDTHH:MM:SS.000Z`. Once expired, Vault deletes the debug log and all log data.

`class_filters`

Class filters applied to this debug log, if any. Class filters allow you to restrict debug log entries to only include entries for specific classes.

`status`

The status of this debug log, either active or inactive. By default, only active logs are included in the response. To include inactive logs, set the `include_inactive` query parameter to `true`.

`created_date`

The date this session was created, in the format `YYYY-MM-DDTHH:MM:SS.000Z`.

### Retrieve Single Debug Log

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/logs/code/debug/0LS000000003006
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "id": "0LS000000003006",
        "name": "Record Trigger Troubleshooting",
        "user_id": 61603,
        "log_level": "all__sys",
        "expiration_date": "2025-01-11T03:09:47.000Z",
        "class_filters": [
            {
                "name": "com.veeva.vault.custom.HelloWorld",
                "code_type": "Pagecontroller"
            },
            {
                "name": "com.veeva.vault.custom.triggers.HelloWorld",
                "code_type": "Recordtrigger"
            }
        ],
        "status": "active__sys",
        "created_date": "2024-12-12T03:09:47.000Z"
    }
}
'''

Given a [debug log](/sdk/#Debug_Log) ID, retrieve details about this debug log.

GET `/api/{version}/logs/code/debug/{id}`

#### Headers

Name

Description

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{id}`

The ID of the debug log to retrieve.

#### Response Details

On `SUCCESS`, the response includes the following `data` for each debug log:

Name

Description

`id`

The numerical ID of this debug log.

`name`

The UI name of this debug log.

`user_id`

The ID of the user associated with this debug log.

`log_level`

The level of error messages captured in this debug log. Learn more about the [log level types in Vault Help](https://platform.veevavault.help/en/lr/14341/#debug-log).

`expiration_date`

The date this session will expire, in the format `YYYY-MM-DDTHH:MM:SS.000Z`. Once expired, Vault deletes the debug log and all log data.

`class_filters`

Class filters applied to this debug log, if any. Class filters allow you to restrict debug log entries to only include entries for specific classes.

`status`

The status of this debug log, either active or inactive. By default, only active logs are included in the response. To include inactive logs, set the `include_inactive` query parameter to `true`.

`created_date`

The date this session was created, in the format `YYYY-MM-DDTHH:MM:SS.000Z`.

### Download Debug Log Files

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/logs/code/debug/0LS000000003006/files
'''

> Response Headers

'''
Content-Type: application/zip;charset=UTF-8
Content-Disposition: attachment;filename="vaultjavasdk_61603_debuglogs_12-18-2024.zip"
'''

Given a [debug log](/sdk/#Debug_Log) ID, download all of this debug log’s files.

GET `/api/{version}/logs/code/debug/{id}/files`

#### Headers

Name

Description

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{id}`

The ID of the debug log to download.

#### Response Details

On `SUCCESS`, Vault begins a download of the files for the specified debug log. The files are packaged in a ZIP file with the file name: `vaultjavasdk_{user_id}_debuglogs_{MM-DD-YYYY}.zip`.

The HTTP Response Header `Content-Type` is set to `application/zip;charset=UTF-8`. The HTTP Response Header `Content-Disposition` contains a filename component which can be used when naming the local file.

### Create Debug Log

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-d "name=Record Trigger Troubleshooting" \
-d "user_id=12345" \
-d "class_filters=com.veeva.vault.custom.triggers.HelloWorld,com.veeva.vault.custom.triggers.Approval" \
https://myvault.veevavault.com/api/v25.2/logs/code/debug
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "id": "0LS000000003001"
    }
}
'''

Create a new [debug log](/sdk/#Debug_Log) session for a user.

Debug logs have the following limits:

-   Maximum one (1) debug log per user
-   Maximum 20 debug logs per Vault

POST `/api/{version}/logs/code/debug`

#### Headers

Name

Description

`Accept`

`application/json`

`Content-Type`

`multipart/form-data`

#### Body Parameters

Name

Description

`name`required

The UI-friendly name for this debug log, visible to Admins in the Vault UI. Maximum 128 characters.

`user_id`required

The ID of the user who will trigger entries into this debug log.

`log_level`optional

The level of error messages to capture in this log. Choose one of the following:

-   `all__sys` (default)
-   `exception__sys`
-   `error__sys`
-   `warn__sys`
-   `info__sys`
-   `debug__sys`

Learn more about the log level types in [Vault Help](https://platform.veevavault.help/en/lr/14341/#debug-log).

`class_filters`optional

Class filters allow you to restrict debug log entries to only include entries for specific classes. To include class filters for this debug log, include an array or comma-separated list of fully-qualified class `names`. For example, `com.veeva.vault.custom.triggers.HelloWorld`.

### Reset Debug Log

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/logs/code/debug/0LS000000006003/actions/reset
'''

> Response

'''
{
   "responseStatus": "SUCCESS"
}
'''

Given a [debug log](/sdk/#Debug_Log) ID, delete all existing log files and reset the expiration date to 30 days from today.

POST `/api/{version}/logs/code/debug/{id}/actions/reset`

#### Headers

Name

Description

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{id}`

The ID of the debug log to reset.

### Delete Debug Log

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/logs/code/debug/0LS000000003001
'''

> Response

'''
{
   "responseStatus": "SUCCESS"
}
'''

Given a [debug log](/sdk/#Debug_Log) ID, delete this debug log and all log files.

DELETE `/api/{version}/logs/code/debug/{id}`

#### Headers

Name

Description

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{id}`

The ID of the debug log to delete.

## SDK Request Profiler

The _Profiler Log_ allows developers to create SDK request profiling sessions, which allow developers to troubleshoot and improve custom SDK code quality by analyzing results at the SDK request level. The _Profiler Log_ is also available in the Vault UI from **Admin > Logs > Developer Logs**. Learn more about the [Profiler Log in Vault Help](https://platform.veevavault.help/en/lr/14341/#profiler-log).

The authenticated user must have the _Admin: Logs: Vault Java SDK_ permission to perform CRUD operations on profiling sessions.

### Retrieve All Profiling Sessions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/code/profiler
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "id": "0LS000000003002",
           "label": "Baseline",
           "name": "baseline__c",
           "description": null,
           "status": "processing__sys",
           "user_id": null,
           "created_date": "2024-08-23T23:22:00.000Z",
           "expiration_date": "2024-09-22T23:22:00.000Z"
       },
       {
           "id": "0LS000000002001",
           "label": "Hotfix Dry Run 02",
           "name": "hotfix_dry_run_02__c",
           "description": null,
           "status": "complete__sys",
           "user_id": 123456789,
           "created_date": "2024-08-20T02:21:21.000Z",
           "expiration_date": "2024-09-19T02:31:47.000Z"
       },
       {
           "id": "0LS000000001001",
           "label": "Hotfix Dry Run 01",
           "name": "hotfix_dry_run_01__c",
           "description": null,
           "status": "complete__sys",
           "user_id": null,
           "created_date": "2024-08-20T01:42:02.000Z",
           "expiration_date": "2024-09-19T02:11:25.000Z"
       }
   ]
}
'''

List all SDK request profiling sessions in the currently authenticated Vault.

GET `/api/{version}/code/profiler`

#### Headers

Name

Description

`Accept`

`application/json`

#### Response Details

On `SUCCESS`, the response includes the following `data` for each profiling session:

Name

Description

`id`

The numerical ID of this profiling session.

`label`

The UI label of this profiling session. For example, “Baseline”.

`name`

The API name of this profiling session. For example, `baseline__c`. You can use this value to [end the profiling session early](#End_Profiling_Session), [download the results](#Download_Profiling_Session_Results), or [delete the session](#Delete_Profiling_Session).

`description`

The description of this profiling session.

`status`

The status of this session, either:

-   `in_progress__sys`: The session is actively running and collecting SDK request data.
-   `processing__sys`: The session is no longer running, but the session is still active as Vault processes the data. The results are not yet available for download.
-   `complete__sys`: The session is over, and the results are available for download. This session is inactive.

`user_id`

The ID of the user associated with this session. If `null`, this session applies to all users.

`created_date`

The date this session was created, in the format `YYYY-MM-DDTHH:MM:SS.000Z`.

`expiration_date`

The date this session will expire, in the format `YYYY-MM-DDTHH:MM:SS.000Z`. Once expired, Vault deletes the session and all session data.

### Retrieve Profiling Session

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/code/profiler/baseline__c
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "id": "0LS000000003002",
       "label": "Baseline",
       "name": "baseline__c",
       "description": null,
       "status": "complete__sys",
       "user_id": null,
       "created_date": "2024-08-23T23:22:00.000Z",
       "expiration_date": "2024-09-22T23:36:21.000Z"
   }
}
'''

Retrieve details about a specific SDK request profiling session.

GET `/api/{version}/code/profiler/{session_name}`

#### Headers

Name

Description

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{session_name}`

The `name` of the session, for example, `baseline__c`.

#### Response Details

On `SUCCESS`, the response includes the following `data` for each profiling session:

Name

Description

`id`

The numerical ID of this profiling session.

`label`

The UI label of this profiling session. For example, “Baseline”.

`name`

The API name of this profiling session. For example, `baseline__c`. You can use this value to [end the profiling session early](#End_Profiling_Session), [download the results](#Download_Profiling_Session_Results), or [delete the session](#Delete_Profiling_Session).

`description`

The description of this profiling session.

`status`

The status of this session, either:

-   `in_progress__sys`: The session is actively running and collecting SDK request data.
-   `processing__sys`: The session is no longer running, but the session is still active as Vault processes the data. The results are not yet available for download.
-   `complete__sys`: The session is over, and the results are available for download. This session is inactive.

`user_id`

The ID of the user associated with this session. If `null`, this session applies to all users.

`created_date`

The date this session was created, in the format `YYYY-MM-DDTHH:MM:SS.000Z`.

`expiration_date`

The date this session will expire, in the format `YYYY-MM-DDTHH:MM:SS.000Z`. Once expired, Vault deletes the session and all session data.

### Create Profiling Session

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
--data-urlencode "label=Integration User Dry Run" \
https://myvault.veevavault.com/api/v25.2/code/profiler
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "id": "0LS000000003003",
       "name": "hotfix_dry_run_01__c"
   }
}
'''

Create a new SDK request profiling session. Profiling sessions allow developers to troubleshoot custom code and improve code quality by analyzing results at the SDK request level.

Vault starts the profiling session immediately on creation. Profiling sessions run for either 20 minutes or up to 10,000 SDK requests, whichever comes first. To end a session early, use the [End Profiling Session](#End_Profiling_Session) endpoint. Once ended, a session’s `status` is `processing__sys` while Vault prepares the data, which may take about 15 minutes. Once the `status` is `complete__sys`, the data is available for download with the [Download Profiling Session Results](#Download_Profiling_Session_Results) endpoint.

Only one profiling session can be active at a time. Because sessions begin immediately on creation, you cannot create a new session until the current session becomes inactive. Additionally, each Vault can only retain profiling session data for up to 10 sessions. If your Vault already has 10 profiling sessions, you must [Delete a Profiling Session](#Delete_Profiling_Session) before creating a new one.

POST `/api/{version}/code/profiler`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json`

#### Body Parameters

Name

Description

`label`required

The UI label for this request.

`user_id`optional

The user ID of the user to associate with this session. When specified, this SDK profiling session runs only for this user. If omitted, defaults to `null` which runs the session for all users.

`description`optional

An Admin-facing description of the session.

#### Response Details

On `SUCCESS`, Vault starts the profiling session immediately and returns the session `id` and `name`.

### End Profiling Session

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/code/profiler/baseline__c/actions/end
'''

> Response

'''
{
   "responseStatus": "SUCCESS"
}
'''

Terminate a profiling session early. By default, profiling sessions run for either 20 minutes or up to 10,000 SDK requests, whichever comes first.

Once ended, a session’s `status` is `processing__sys` while Vault prepares the data, which may take about 15 minutes. Once the `status` is `complete__sys`, the data is available for download with the [Download Profiling Session Results](#Download_Profiling_Session_Results) endpoint.

POST `/api/{version}/code/profiler/{session_name}/actions/end`

#### Headers

Name

Description

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{session_name}`

The `name` of the session, for example, `baseline__c`.

#### Response Details

On `SUCCESS`, the Vault ends the profiling session. The session’s `status` becomes `processing__sys` while Vault prepares the data, which may take about 15 minutes.

### Delete Profiling Session

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/code/profiler/baseline__c
'''

> Response

'''
{
   "responseStatus": "SUCCESS"
}
'''

Delete an inactive profiling session, which deletes the session and all data associated with the session. Inactive sessions have a `status` of `complete__sys`.

DELETE `/api/{version}/code/profiler/{session_name}`

#### Headers

Name

Description

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{session_name}`

The `name` of the session, for example, `baseline__c`.

#### Response Details

On `SUCCESS`, the Vault deletes the specified profiling session and deletes all data associated with the session.

### Download Profiling Session Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/code/profiler/baseline__c/results > file
'''

> Response Headers

'''
Content-Type: application/zip;charset=UTF-8
Content-Disposition: attachment;filename="baseline__c.zip"
'''

Download the Profiler Log for a specific profiling session. A profiling session log is a CSV which contains one row for each SDK request, with a maximum of 100,000 rows.

GET `/api/{version}/code/profiler/{session_name}/results`

#### Headers

Name

Description

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{session_name}`

The `name` of the session, for example, `baseline__c`.

#### Response Details

On `SUCCESS`, Vault downloads the results of the specified profiling session. The HTTP Response Header `Content-Type` is set to `application/zip`. The HTTP Response Header `Content-Disposition` contains a filename component which can be used when naming the local file.

The log is a CSV file with the following information for each SDK request:

Name

Description

`timestamp`

The time this SDK request began executing.

`user_id`

The ID of the user who initiated this request.

`user_name`

The user name of the user who initiated this request.

`execution_id`

This SDK request’s execution ID.

`sdk_request_id`

The ID of this SDK request.

`sdk_count`

The number of SDK entry points evoked during this request.

`sdk_cpu_time`

The CPU time, in nanoseconds.

`sdk_elapsed_time`

The total elapsed time, in milliseconds.

`sdk_gross_memory`

The memory consumed, in bytes.

## Retrieve Email Notification Histories

> Request: 30 Days

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/notifications/histories?start_date=2022-09-10&end_date=2022-10-09
'''

> Response: 30 Days

'''
{
   "responseStatus": "SUCCESS",
   "responseDetails": {
       "offset": 0,
       "limit": 200,
       "size": 3,
       "total": 3
   },
   "data": [
       {
           "send_date": "2022-09-13T06:44:18.000Z",
           "recipient_name": "Teresa Ibanez",
           "recipient_id": 995595,
           "recipient_email": "tibanez@veepharm.com",
           "status": "delivered__sys",
           "error_message": null,
           "subject": "Notification: Review completed, changes not required",
           "workflow_id": 1502,
           "task_id": null,
           "document_id": null,
           "major_version": null,
           "minor_version": null,
           "object_name": "envelope__sys",
           "object_record_id": "0ER00000000E002",
           "sender_name": "Justine Lo",
           "sender_id": 694695,
           "notification_id": 107,
           "included_notification_ids": null,
           "status_date": "2022-09-13T06:44:18.000Z",
           "template_name": "basereviewedapproved__v"
       },
       {
           "send_date": "2022-09-13T06:41:02.000Z",
           "recipient_name": "Teresa Ibanez",
           "recipient_id": 995595,
           "recipient_email": "tibanez@veepharm.com",
           "status": "delivered__sys",
           "error_message": null,
           "subject": "Notification: Documents not approved, changes required",
           "workflow_id": 1501,
           "task_id": null,
           "document_id": null,
           "major_version": null,
           "minor_version": null,
           "object_name": "envelope__sys",
           "object_record_id": "0ER00000000E001",
           "sender_name": "Megan Murray",
           "sender_id": 1083287,
           "notification_id": 106,
           "included_notification_ids": null,
           "status_date": "2022-09-13T06:41:03.000Z",
           "template_name": "baseapprovedwithchangesmdw__v"
       },
       {
           "send_date": "2022-09-13T06:37:18.000Z",
           "recipient_name": "Teresa Ibanez",
           "recipient_id": 1083287,
           "recipient_email": "tibanez@veepharm.com",
           "status": "delivered__sys",
           "error_message": null,
           "subject": "Notification: Mentioned in comment on sample.",
           "workflow_id": null,
           "task_id": null,
           "document_id": 6,
           "major_version": 0,
           "minor_version": 1,
           "object_name": null,
           "object_record_id": null,
           "sender_name": "Olivia Cattington",
           "sender_id": 995595,
           "notification_id": 104,
           "included_notification_ids": null,
           "status_date": "2022-09-13T06:37:18.000Z",
           "template_name": "usermentionnotifications__v"
       }
    ]
}
'''

> Request: All Dates

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/notifications/histories?all_dates=true&format_result=csv
'''

> Response: All Dates

'''
{
   "responseStatus": "SUCCESS",
   "jobId": "639014",
   "url": "/api/v25.2/services/jobs/639014"
}
'''

Retrieve details about the email notifications sent by Vault. Details include the notification date, recipient, subject, and delivery status. In the UI, this information is available in **Admin > Operations > Email Notification Status**. Learn more about [Email Notification Status in Vault Help](https://platform.veevavault.help/en/lr/514128).

GET `/api/{version}/notifications/histories`

#### Headers

Name

Description

`Content-Type`

`application/json` (default)

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

You can modify the request by using one or more of the following parameters:

Name

Description

`start_date`

Specify a start date to retrieve notification history. This date cannot be more than 3 months ago. To retrieve older email notifications, use the `all_dates` parameter instead.  
  
Dates must be in `YYYY-MM-DD` or `YYYY-MM-DDTHH:mm:ssZ` format. If time is omitted (`THH:mm:ssZ`), defaults to the start of the day. If `start_date` is omitted entirely, defaults to the start of the previous day.  
  
If you’ve specified a `start_date`, you must also specify an `end_date`.

`end_date`

Specify an end date to retrieve notification history. This date cannot be more than 30 days away from the specified `start_date`. Dates must be in `YYYY-MM-DD` or `YYYY-MM-DDTHH:mm:ssZ` format. If time is omitted (`THH:mm:ssZ`), defaults to the time of the API request.  
  
If you’ve specified an `end_date`, you must also specify a `start_date`.

`all_dates`

Set to `true` to request notification history for all dates. This request starts a job to prepare a downloadable `.zip` of CSV files of the entire notification history by year. This is similar to requesting **Export Full History** from the Vault UI. When requesting a full notification history, you must leave `start_date` and `end_date` blank and set `format_result` to `csv`. You can request an export of notification history for `all_dates` once every 24 hours.  
  
Emails sent before 22R3 may have data in the `status` column only, and may have blank values in some columns.

`format_result`

To request a downloadable CSV file of your notification history, set this parameter to `csv`. The response contains a `jobId` to retrieve the job status, which provides a link to download the CSV file. If omitted, the API returns a JSON response with notification history and does not start a job. If `all_dates` is `true`, this parameter must be `csv`.

`limit`

Paginate the results by specifying the maximum number of histories per page in the response. This can be any value between `1` and `1000`. If omitted, defaults to `200`.

`offset`

Paginate the results displayed per page by specifying the amount of offset from the entry returned. If omitted, defaults to `0`.

## Download Daily API Usage

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/logs/api_usage?date=2018-01-31 > file
'''

> Response Headers

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment;filename="response.zip"
'''

Retrieve the **API Usage Log** for a single day, up to 30 days in the past. The log contains information such as user name, user ID, remaining burst limit, and the endpoint called. Users with the _Admin: Logs: API Usage Logs_ permission can access these logs.

Note that the daily logs may have a delay of about 15 minutes. If your log does not include appropriate data, know that your data is not lost; it is just not yet populated.

The logs are designed for troubleshooting burst limits and discovering which of your integrations are causing you to hit the limit. These logs should not be used for auditing, as they are not designed with the appropriate level of restrictions. For example, if an API request fails to enter the usage log, the API call is not prevented from executing, which would be required if this log was designed for auditing. In rare cases an API call may not show up as an entry in the log, but know that all calls are accurately reflected in your burst limit counts.

GET `/api/{version}/logs/api_usage?date=YYYY-MM-DD`

#### Headers

Note that this `Accept` header only changes the format of the response in the case of an error. This does not change the file format of the download.

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

You can modify the request by using one or more of the following parameters:

Name

Description

`date`

The day to retrieve the API Usage log. Date is in UTC and follows the format `YYYY-MM-DD`. Date cannot be more than 30 days in the past.

`log_format`

Optional: Specify the format to download. Possible values are `csv` or `logfile`. If omitted, defaults to `csv`. Note that this call always downloads a ZIP file. This parameter only changes the format of the file contained within the ZIP.

#### Response Details

On `SUCCESS`, Vault retrieves the log from the specified date as a .ZIP file. The HTTP Response Header `Content-Type` is set to `application/octet-stream`. The returned CSV or Logfile includes the following data:

Name

Description

`timestamp`

The date and time of this API request, in UTC.

`session_id`

The Session ID of the user who made the request.

`user_id`

The ID of the user who made the request.

`username`

The Vault user name (login credentials) of the user who made the request.

`http_method`

The HTTP Method of the request, for example, POST.

`endpoint`

The Vault API endpoint used for this request.

`http_response_status`

The HTTP response status of the request, for example, 200.

`api_version`

The Vault API version used for this request, for example, v18.1. This value is blank for endpoints which do not have an API version.

`api_response_status`

The API response status, for example, `SUCCESS`. This column may be blank for requests where the response contains binary content, such as files.

`api_response_error_type`

The API response error type, for example, `INSUFFICIENT_ACCESS`.

`execution_id`

Unique ID generated by Vault for each API request. Returned in the response header `X-VaultAPI-ExecutionId`.

`client_id`

The client ID passed with this request. If the API request did not include a client ID, this value is `unknown`. If the API received a `client_id` which was incorrectly formatted, this value is `invalid_client_id`. Learn more about [Client ID in the Vault API Documentation](/docs/#Client_ID).

`client_ip`

The IP address of the client, which is where the call originated.

`burst_limit_remaining`

The number of API calls remaining in your burst limit. Learn more about [API Limits](/docs/#api_rate_limits).

`duration`

The time it takes an API request to execute in Vault, measured in milliseconds. Note the duration does not include transport times between Vault and the client.

`response_delay`

This column is populated whenever API calls are throttled and indicates the length of the delay in milliseconds.

`sdk_count`

This column is populated if the API request invoked custom Vault Java SDK code, and indicates the total number of SDK entry points executed in this request. Learn more about [Vault Java SDK performance metrics](/docs/#SDK_Performance_API_Headers).

`sdk_cpu_time`

This column is populated if the API request invoked custom Vault Java SDK code, and indicates the total CPU processing time required for this request in nanoseconds. Learn more about [Vault Java SDK performance metrics](/docs/#SDK_Performance_API_Headers).

`sdk_elasped_time`

This column is populated if the API request invoked custom Vault Java SDK code, and indicates the total elapsed time for this request in milliseconds. Learn more about [Vault Java SDK performance metrics](/docs/#SDK_Performance_API_Headers).

`sdk_gross_memory`

This column is populated if the API request invoked custom Vault Java SDK code, and indicates the total gross memory required for this request in bytes. Learn more about [Vault Java SDK performance metrics](/docs/#SDK_Performance_API_Headers).

`connection`

The `api_name__sys` of the matching _Connection_ record associated with this request. If this is a trusted Veeva connection, such as Vault Loader, Vault Mobile, or Station Manager, this value is `vault__sys`. If there is no associated connection, this value is blank.

`api_resource`

The API resource for the request. For example, the primary query object for a VQL request.

`api_response_warning_type`

The API request warning type. For example, `DUPLICATE`.

`api_response_warning_message`

The API request warning message. For example, “Duplicate query execution detected. Consider caching commonly required data.”

`api_response_error_message`

The API request error message. For example, “product\_\_b is not a queryable object; please refer to api documentation”.

`reference_id`

The `X-VaultAPI-ReferenceId`header value. If this header was not included in the request, this value is blank.

## Download SDK Runtime Log

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/logs/api_usage?date=2022-01-25 > file
'''

> Response Headers

'''
application/octet-stream;charset=UTF-8
attachment;filename*=UTF-8''44795-SdkLog-2022-01-25.zip
'''

Retrieve the _Runtime Log_ for a single day, up to 30 days in the past. Users with the _Admin: Logs: Vault Java SDK Logs_ permission can access these logs.

The runtime logs create entries 15 minutes after the Vault Java SDK transaction completes. If you’ve recently encountered an error which is not captured in the runtime log, wait for the transaction to finish and check again. If your log does not include appropriate data, know that your data is not lost; it is just not yet populated.

Learn more about the [Vault Java SDK runtime log](/sdk/#Runtime_Log).

GET `/api/{version}/logs/code/runtime?date=YYYY-MM-DD`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`date`

The day to retrieve the runtime log. Date is in UTC and follows the format `YYYY-MM-DD`. Date cannot be more than 30 days in the past.

`log_format`

Optional: Specify the format to download. Possible values are `csv` or `logfile`. If omitted, defaults to `csv`. This request always downloads a ZIP file; this parameter only changes the format of the file contained within the ZIP.

#### Response Details

On `SUCCESS`, Vault retrieves the log from the specified date as a .ZIP file. The HTTP Response Header `Content-Type` is set to `application/octet-stream`.
