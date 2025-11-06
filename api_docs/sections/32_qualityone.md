<!-- 
VaultAPIDocs Section: # QualityOne
Original Line Number: 41650
Generated: August 30, 2025
Part 32 of 38
-->

# QualityOne

To use this API, you must have Veeva QualityOne. Learn more about [QualityOne in Vault Help](https://qualityone.veevavault.help/en/lr/38220).

## Manage Team Assignments

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\QMS\manage_team_assignments.csv" \
https://myvault.veevavault.com/api/v25.2/app/qualityone/qms/teams/vobjects/car__v/actions/manageassignments
'''

> Example CSV Request Body

'''

record_id,user_id,operation,application_role
VC400000001001,1962069,ADD,approver__c

'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "jobId": "251801"
}
'''

Manage _Team_ assignments by adding users to _Team Roles_ and removing users from _Team Roles_ in batches on one or more existing records. Vault performs updates to _Team_ assignments asynchronously on behalf of the user. When the job completes, Vault returns the `job_id` and an email notification with a CSV file containing the results of the job. This endpoint does not support initial _Team_ record migrations or the creation of new _Teams_ or _Team Roles_. Learn more about [QualityOne Teams in Vault Help](https://qualityone.veevavault.help/en/lr/70759).

-   The maximum CSV input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.

This operation respects the following configurations which impact business logic:

-   Minimum required and maximum users
-   Constraining application roles and user assignment eligibility
-   Object records in locked states
-   New assignments for active users
-   Exclusive role membership restrictions
-   Moving object records to a destination state upon membership completion
-   Task assignment for new and removed users

POST `/api/{version}/app/qualityone/qms/teams/vobjects/:{object_name}/actions/manageassignments`

#### Headers

Name

Description

`Content-Type`

`text/csv`

`Accept`

`text/csv`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value for the team-enabled object. For example, `risk_event__v`, `investigation__qdm`, `audit__qdm`.

#### Body Parameters

Upload parameters as a CSV file.

Name

Description

`record_id`

The object record’s `id` field value. This record must belong to the object indicated in the `{object_name}` path parameter.

`user_id`

The `id` value of the Vault user whose assignment you wish to manage.

`application_role`

The `name__v` value of the `application_role__v` specified on the target Team Role. For example, `record_owner__c`.

`operation`

Indicate whether to `ADD` or `REMOVE` the provided user from the Team. The value of this parameter is case-sensitive. `REMOVE` executes before `ADD`.

#### Response Details

On a `responseStatus` of `SUCCESS`, the response returns the `job_id` for the action. The authenticated user receives a Vault notification and email with the job results and a CSV file containing the IDs of the records updated, the results, and details about any failures.
