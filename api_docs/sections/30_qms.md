<!-- 
VaultAPIDocs Section: # QMS
Original Line Number: 41486
Generated: August 30, 2025
Part 30 of 38
-->

# QMS

To use this API, you must have Veeva QMS. Learn more about [QMS in Vault Help](https://quality.veevavault.help/en/lr/34814).

## Manage Quality Team Assignments

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\QMS\update_quality_team_members.csv" \
https://myvault.veevavault.com/api/v25.2/app/quality/qms/teams/vobjects/quality_event__qdm/actions/manageassignments
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "jobId": "243001"
}
'''

Manage Quality Team members on existing records. This endpoint does not support initial Quality Team record migrations or the creation of new Quality Teams on existing process records. Vault performs updates to Quality Team assignments asynchronously on behalf of the user. Learn more about [Quality Teams in Vault Help](https://quality.veevavault.help/en/lr/52842).

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

POST `/api/{version}/app/quality/qms/teams/vobjects/:{object_name}/actions/manageassignments`

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

The object `name__v` field value for the team-enabled object. For example, `risk_event__v`, `investigation__qdm`, `quality_event__qdm`.

#### Body Parameters

Upload parameters as a CSV file.

Name

Description

`record_id`

The object record’s `id` field value. This record must belong to the object indicated in the `{object_name}` path parameter.

`user_id`

The `id` value of the Vault user whose assignment you wish to manage for the Quality Team.

`application_role`

The name of the `application_role__v` of the Quality Team Role to which to assign the user on the Quality Team. For example, `record_owner__c`.

`operation`

Indicate whether to `ADD` or `REMOVE` the provided user from the Quality Team. The value of this parameter is case-sensitive.

#### Response Details

On `SUCCESS`, the response returns the `job_id` for the action, and the authenticated user will receive an email notification with details of any failures that occur.
