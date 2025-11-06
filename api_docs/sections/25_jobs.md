<!-- 
VaultAPIDocs Section: # Jobs
Original Line Number: 39008
Generated: August 30, 2025
Part 25 of 38
-->

# Jobs

## Retrieve Job Status

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/jobs/1201
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "OK",
  "data": {
    "id": 1201,
    "status": "SUCCESS",
    "method": "POST",
    "links": [
      {
        "rel": "self",
        "href": "/api/v25.2/services/jobs/1601",
        "method": "GET",
        "accept": "application/json"
      }
    ],
    "created_by": 44533,
    "created_date": "2016-04-20T18:14:42.000Z",
    "run_start_date": "2016-04-20T18:14:43.000Z",
    "run_end_date": "2016-04-20T18:14:44.000Z"
  }
}
'''

After submitting a request, you can query your Vault to determine the status of the request. To do this, you must have a valid `job_id` for a job previously requested through the API.

Example Jobs:

-   Binder Export
-   Import Submission
-   Export Submission
-   Create EDL
-   Deploy Package
-   Deep Copy Object Record
-   Cascade Delete Object Record
-   Export Documents

GET `/api/{version}/services/jobs/{job_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{job_id}`

The ID of the job, returned from the original job request.

#### Response Details

On `SUCCESS`, the response includes the following information. All DateTime values for scheduled jobs are in the Vault time zone for the currently authenticated user. Learn more about the [Vault time zone in Vault Help](https://platform.veevavault.help/en/lr/13309#vault_time_zone).

Metadata Field

Description

`id`

The `job_id` field value for the job.

`status`

The status of the job. Possible statuses include `SCHEDULED`, `QUEUED`, `RUNNING`, `SUCCESS`, `ERRORS_ENCOUNTERED`, `QUEUEING`, `CANCELLED`, `TIMEOUT`, `COMPLETED_DUE_TO_INACTIVITY`, and `MISSED_SCHEDULE`. Learn more about [job statuses in Vault Help](https://platform.veevavault.help/en/lr/24762/#about-job-completion-statuses).

`method`

The HTTP method used in the request.

`links`

Once the job is finished, use these endpoints and methods to retrieve other job details. Note that for Controlled Copy jobs, the `artifacts` link will only work with API v18.3+.

`progress`

If the retrieved job is a custom job created with the Vault Java SDK, this array contains a summary of the number of job tasks (`size`) and their status.

`created_by`

The `id` field value of the user who started the job.

`created_date`

The date and time when the job was requested.

`run_start_date`

The date and time when the export job started.

`run_end_date`

The date and time when the export job finished.

## Retrieve SDK Job Tasks

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/jobs/72408/tasks
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "url": "/api/v25.2/services/jobs/72408/tasks?limit=50&offset=0",
   "responseDetails": {
       "total": 1,
       "limit": 50,
       "offset": 0
   },
   "job_id": 72408,
   "tasks": [
       {
           "id": "Task1",
           "state": "SUCCESS"
       }
   ]
}
'''

Retrieve the tasks associated with an SDK job.

GET `/api/{version}/services/jobs/{job_id}/tasks`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{job_id}`

The ID of the SDK job, returned from the original job request.

## Retrieve Job Histories

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/jobs/histories
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": "OK",
   "url": "/api/v25.2/services/jobs/histories?limit=50&offset=0",
   "responseDetails": {
       "total": 2753,
       "limit": 50,
       "offset": 0,
       "next_page": "/api/v25.2/services/jobs/histories?limit=50&offset=50"
   },
   "jobs": [
      {
           "job_id": 361402,
           "title": "User Account Activation",
           "status": "SUCCESS",
           "created_by": 1,
           "created_date": "2020-12-15T07:00:31.000Z",
           "modified_by": 1,
           "modified_date": "2020-12-16T07:05:06.000Z",
           "run_start_date": "2020-12-16T07:00:00.000Z",
           "run_end_date": "2020-12-16T07:06:07.000Z"
       },
       {
           "job_id": 361401,
           "title": "Synchronize Portal Assets",
           "status": "SUCCESS",
           "created_by": 1,
           "created_date": "2020-12-15T05:01:24.000Z",
           "modified_by": 1,
           "modified_date": "2020-12-16T05:00:09.000Z",
           "run_start_date": "2020-12-16T05:00:00.000Z",
           "run_end_date": "2020-12-16T05:01:12.000Z"
       }
   ]
}
'''

Retrieve a history of all completed jobs in the authenticated Vault. A completed job is any job which has started and finished running, including jobs which did not complete successfully. In-progress or queued jobs do not appear here.

GET `/api/{version}/services/jobs/histories`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`start_date`

Sets the date to start retrieving completed jobs, in the format `YYYY-MM-DDTHH:MM:SSZ`. For example, for 7AM on January 15, 2016, use `2016-01-15T07:00:00Z`. If omitted, defaults to the first completed job.

`end_date`

Sets the date to end retrieving completed jobs, in the format `YYYY-MM-DDTHH:MM:SSZ`. For example, for 7AM on January 15, 2016, use `2016-01-15T07:00:00Z`. If omitted, defaults to the current date and time.

`status`

Filter to only retrieve jobs in a certain status. Allowed values are `success`, `errors_encountered`, `failed_to_run`, `missed_schedule`, `timeout`, `completed_due_to_inactivity`, and `cancelled`. If omitted, retrieves all statuses. Learn more about [job statuses in Vault Help](https://platform.veevavault.help/en/lr/24762/#about-job-completion-statuses).

`limit`

Paginate the results by specifying the maximum number of histories per page in the response. This can be any value between `1` and `200`. If omitted, defaults to `50`.

`offset`

Paginate the results displayed per page by specifying the amount of offset from the first job history returned. If omitted, defaults to `0`. If you are viewing the first 50 results (page 1) and want to see the next page, set this to `offset=51`.

## Retrieve Job Monitors

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/jobs/monitors
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": "OK",
   "url": "/api/v25.2/services/jobs/monitors?limit=50&offset=0",
   "responseDetails": {
       "total": 3,
       "limit": 50,
       "offset": 0
   },
   "jobs": [
       {
           "job_id": 72505,
           "title": "User Account Activation",
           "status": "SCHEDULED",
           "created_by": 1,
           "created_date": "2021-02-03T04:01:29.000Z",
           "modified_by": 1,
           "modified_date": "2021-02-03T04:01:29.000Z",
           "run_start_date": "2021-02-04T04:00:00.000Z"
       },
       {
           "job_id": 72518,
           "title": "Task Reminder Notification",
           "status": "SCHEDULED",
           "created_by": 1,
           "created_date": "2021-02-03T09:01:53.000Z",
           "modified_by": 1,
           "modified_date": "2021-02-03T09:01:53.000Z",
           "run_start_date": "2021-02-04T09:00:00.000Z"
       }
   ]
}
'''

Retrieve monitors for jobs which have not yet completed in the authenticated Vault. An uncompleted job is any job which has not finished running, such as scheduled, queued, or actively running jobs. Completed jobs do not appear here.

GET `/api/{version}/services/jobs/monitors`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`start_date`

Sets the date to start retrieving uncompleted jobs, based on the date and time the job instance was created. Value must be in the format `YYYY-MM-DDTHH:MM:SSZ`. For example, for 7AM on January 15, 2016, use `2016-01-15T07:00:00Z`. If omitted, defaults to the first completed job.

`end_date`

Sets the date to end retrieving uncompleted jobs, based on the date and time the job instance was created. Value must be in the format `YYYY-MM-DDTHH:MM:SSZ`. For example, for 7AM on January 15, 2016, use `2016-01-15T07:00:00Z`. If omitted, defaults to the current date and time.

`status`

Filter to only retrieve jobs in a certain status. Allowed values are `scheduled`, `queued`, `running`. If omitted, retrieves all statuses.

`limit`

Paginate the results by specifying the maximum number of jobs per page in the response. This can be any value between `1` and `200`. If omitted, defaults to `50`.

`offset`

Paginate the results displayed per page by specifying the amount of offset from the first job instance returned. If omitted, defaults to `0`. If you are viewing the first 50 results (page 1) and want to see the next page, set this to `offset=51`.

## Start Job

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/start_now/72505
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "url": "/api/v25.2/services/jobs/72505",
   "job_id": 72505
}
'''

Moves up a `scheduled` job instance to start immediately. Each time a user calls this API, Vault cancels the scheduled instance of the specified job for the current interval. For example, if a job is scheduled to run daily at 11PM PST, calling this API against it at 4PM PST will cause the job to not run as scheduled at 11PM PST the same day. Vault will resume running the job at 11PM PST the next day regardless of how many times this API is called before 11PM PST the previous day.

This is analogous to the _Start Now_ option in the Vault UI.

POST `/api/{version}/services/jobs/start_now/{job_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{job_id}`

The ID of the scheduled job instance to start.
