<!-- 
VaultAPIDocs Section: # Workflows
Original Line Number: 23138
Generated: August 30, 2025
Part 9 of 38
-->

# Workflows

A workflow is a series of steps configured in Vault to align with specific business processes. The different types of steps offer a flexible way to organize a wide variety of processes for an object record, including assigning tasks to users, sending notifications, updating fields, and changing a record’s lifecycle state or sharing settings. Workflow tasks can allow users to enter comments, choose verdicts (approve, deny, etc.), populate fields, or provide eSignatures.

Object workflows are specific to a single lifecycle, meaning that one (1) workflow cannot apply to multiple object lifecycles. A single object record can only be in one (1) workflow at a time. Learn more about [Object Workflows in Vault Help](https://platform.veevavault.help/en/lr/33498).

## Retrieve Workflows

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows?object__v=product__v&record_id__v=00P07551
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseDetails": {
    "total": 2,
    "offset": 0,
    "page_size": 200,
    "object": {
      "name": "objectworkflows",
      "label": "Object Workflow",
      "url": "/api/v25.2/objects/objectworkflows?object__v=product__v&record_id__v=00P07551",
      "label_plural": "Object Workflows"
    }
  },
  "data": [
    {
      "id": 4602,
      "label__v": "Product Workflow",
      "status__v": [
        "active__v"
      ],
      "object__v": "product__v",
      "record_id__v": "00P07551",
      "initiator__v": 52212,
      "started_date__v": "2023-04-03T16:09:28.000Z"
    },
    {
      "id": 3901,
      "label__v": "Product Workflow",
      "status__v": [
        "cancelled__v"
      ],
      "object__v": "product__v",
      "record_id__v": "00P07551",
      "initiator__v": 46916,
      "started_date__v": "2022-05-17T17:22:18.000Z",
      "cancelled_date__v": "2022-05-17T17:24:08.000Z"
    }
  ]
}
'''

Retrieve all current, cancelled, and completed workflow instances for a specific object record or all workflows available to a particular workflow participant.

GET `/api/{version}/objects/objectworkflows`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`object__v`, `record_id__v`

To retrieve all workflows configured on an object, include the Vault object `name__v` and object record `id` field values as `object__v={name__v}&record_id__v={id}`. These two parameters are required when the `participant` parameter is not used.

`participant`

To retrieve all workflows available to a particular user, include the user `id` field value as `participant={id}`. To retrieve your own workflows, set this value to `participant=me()`. This parameter is required when the `object__v` and `record_id__v` parameters are not used.

`status__v`

To retrieve all workflows with specific statuses, include one or more status `name__v` field values. For example: `status__v=active__v`, `status__v=active__v,completed__v`. Workflows with `status__v=active__v` are in progress for the indicated object record. Valid statuses include:

-   `active__v`
-   `completed__v`
-   `cancelled__v`

`offset`

This parameter is used to paginate the results. It specifies the amount of offset from the first record returned. Vault returns 200 records per page by default. If you are viewing the first 200 results (page 1) and want to see the next page, set this to `offset=201`.

`page_size`

This parameter is used to paginate the results. It specifies the size number of records to display per page. Vault returns 200 records per page by default. You can set this value lower or as high as 1000 records per page. For example: `page_size=1000`.

`loc`

When localized (translated) strings are available, retrieve them by including `loc=true`.

#### Response Details

On `SUCCESS`, the response lists all workflows matching the query parameters. Each workflow may include the following fields:

-   `id` - The workflow ID.
-   `label__v` - The workflow label as seen in the UI.
-   `status__v` - The current status of the workflow.
-   `object__v` - The name of the object using the workflow.
-   `record_id__v` - The ID of the object record using the workflow.
-   `initiator__v` - The ID of the user who started the workflow. This is the workflow owner.
-   `started_date__v` - The date and time when the workflow was started.
-   `completed_date__v` - The date and time when the workflow was completed.
-   `cancelled_date__v` - The date and time when the workflow was cancelled.

## Retrieve Workflow Details

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/801
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseDetails": {
    "url": "/api/v25.2/objects/objectworkflows/801",
    "object": {
      "name": "objectworkflows",
      "label": "Object Workflow",
      "url": "/api/v25.2/metadata/objectworkflows",
      "label_plural": "Object Workflows"
    }
  },
  "data": [
    {
      "id": 801,
      "label__v": "Approve",
      "status__v": [
        "active__v"
      ],
      "object__v": "product__v",
      "record_id__v": "00P07551",
      "initiator__v": 46916,
      "started_date__v": "2016-05-12T19:22:15.000Z"
    }
  ]
}
'''

Retrieve the details for a specific workflow.

GET `/api/{version}/objects/objectworkflows/{workflow_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{workflow_id}`

The workflow `id`field value.

#### Query Parameters

Name

Description

`loc`

When localized (translated) strings are available, retrieve them by including `loc=true`.

#### Response Details

On `SUCCESS`, the response lists the workflow details. The workflow may include the following fields:

-   `id` - The workflow ID.
-   `label__v` - The workflow label as seen in the UI.
-   `status__v` - The current status of the workflow.
-   `object__v` - The name of the object using the workflow.
-   `record_id__v` - The ID of the object record using the workflow.
-   `initiator__v` - The ID of the user who started the workflow. This is the workflow owner.
-   `started_date__v` - The date and time when the workflow was started.
-   `completed_date__v` - The date and time when the workflow was completed.
-   `cancelled_date__v` - The date and time when the workflow was cancelled.

## Retrieve Workflow Actions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/3302/actions
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "name": "cancel",
           "label": "Cancel"
       },
       {
           "name": "replaceworkflowowner",
           "label": "Replace Workflow Owner"
       },
       {
           "name": "addparticipants",
           "label": "Add Participants"
       }
   ]
}
'''

Retrieve all available workflow actions that can be initiated on a specific workflow.

GET `/api/{version}/objects/objectworkflows/{workflow_id}/actions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{workflow_id}`

The workflow `id` field value.

#### Query Parameters

Name

Description

`loc`

When localized (translated) strings are available, retrieve them by including `loc=true`.

#### Response Details

On `SUCCESS`, the response lists all available workflow actions. Each action includes the following fields:

-   `name` - The workflow action name used to initiate the workflow in the request below.
-   `label` - The workflow action label as seen in the UI.

## Retrieve Workflow Action Details

> Request

'''
curl -X GET "Authorization: {SESSION_ID}" \
  https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/1801/actions/removecontent
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "name": "removecontent",
       "label": "Remove Content",
       "controls": [
           {
               "label": "Documents",
               "type": "documents",
               "prompts": [
                   {
                       "name": "documents__sys",
                       "label": "Documents",
                       "required": true
                   }
               ],
               "current_values": [
                   {
                       "document_id__v": "67"
                   },
                   {
                       "document_id__v": "41"
                   }
               ]
           }
       ]
   }
}
'''

Retrieve details about a workflow action. For example, the `prompts` needed to complete a workflow action.

GET `/api/{version}/objects/objectworkflows/{workflow_id}/actions/{workflow_action}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{workflow_id}`

The workflow id field value.

`{workflow_action}`

The `name` of the workflow action. To get this value, you can [Retrieve Workflow Actions](#Retrieve_Workflow_Actions).

#### Response Details

On `SUCCESS`, the response lists all prompts required to complete the workflow action. If the workflow action does not require any prompts, the response will only list SUCCESS. In the example response, the `removecontent` workflow action requires a value for `contents__sys`.

## Initiate Workflow Action

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/801/actions/cancel
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Initiate a workflow action on a specific workflow.

POST `/api/{version}/objects/objectworkflows/{workflow_id}/actions/{workflow_action}`

#### Headers

Name

Description

`Content-Type`

`application/json` (default) or `application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{workflow_id}`

The workflow `id` field value.

`{workflow_action}`

The workflow action name retrieved from Retrieve Workflow Actions.

#### Body Parameters

In the body of the request, add any fields required to initiate the action. These will differ depending on your specified `{workflow_action}`. For more information about fields required for an action, [Retrieve Workflow Action Details](#Retrieve_Workflow_Action_Details). The following tables show common workflow actions in Vault, but there may be other actions which are not listed here.

##### Replace Workflow Owner: replaceworkflowowner

Name

Description

`new_workflow_owner`required

The `id` of the user who will become the new workflow owner, in the format `user:{id}`. For example, `user:6014`.

##### Email Workflow Participants: emailparticipants

Name

Description

`email_recipients`required

A comma-delimited list of email recipients or groups, in the format `user:{user_id}` and `group:{group_label}`. For example, `user:1082,user:4802,group:incompleteTaskOwners,user:3582`. To find available `{group_label}`s, [Retrieve Workflow Action Details](#Retrieve_Workflow_Action_Details) for `emailparticipants`. If a user is not a potential recipient based on their task status, the user will not receive an email.

`email_message`required

The body of the email message to send to users. Maximum 5,000 characters.

`send_copy_to_self`optional

Set to `true` to send a copy of the email to the authenticated user. If omitted, defaults to `false`.

##### Add Participants: addparticipants

Name

Description

`participants`required

The `id` of the user to add as a participant, in the format `user:{id}`. For example, `user:1006`.

##### Remove Documents from Envelope: removecontent

Name

Description

`contents__sys`required

The `id` of the document to remove from the workflow. To remove multiple documents, use a comma-separated list of `id`s.

##### Update Workflow Due Date: updateworkflowduedate

This action changes the current workflow due date to a new date. Only available on workflows already configured with a workflow due date.

Name

Description

`workflow_due_date`required

The new due date for the workflow, in the format `YYYY-MM-DD`.

#### Response Details

If the `{workflow_action}` executes successfully, the response returns `SUCCESS`. For example, the `cancel` workflow action. On `FAILURE`, the response returns an [error](#Errors) `type` and `message` describing the reason for the failure. For example, the API returns `INVALID_DATA` if a user or group cannot be added as a workflow participant because they are not in the appropriate role.

## Workflow Tasks

### Retrieve Workflow Tasks

> Request

'''
curl -L -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks?assignee__v=674737
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseDetails": {
       "total": 2,
       "offset": 0,
       "page_size": 200,
       "object": {
           "name": "objectworkflow_tasks",
           "label": "Object Workflow Task",
           "url": "/api/v25.2/objects/objectworkflows/tasks?assignee__v=674737",
           "label_plural": "Object Workflow Tasks"
       }
   },
   "data": [
       {
           "id": 123101,
           "label__v": "Review",
           "status__v": [
               "available__v"
           ],
           "object__v": "envelope__sys",
           "record_id__v": "0ER00000003G001",
           "instructions__v": "Review and either Approve or Reject each document",
           "created_date__v": "2021-05-31T21:31:29.000Z",
           "workflow__v": "23001"
       },
       {
           "id": 123001,
           "label__v": "R&U WF Task New",
           "status__v": [
               "assigned__v"
           ],
           "object__v": "envelope__sys",
           "record_id__v": "0ER00000003F001",
           "instructions__v": "Complete this new task",
           "assignee__v": "674737",
           "created_date__v": "2021-05-31T18:33:34.000Z",
           "assigned_date__v": "2021-05-31T18:33:34.000Z",
           "workflow__v": "22901",
           "workflow_class__sys": "read_and_understood__sys"
       }
   ]
}
'''

Retrieve all available tasks across all workflows.

GET `/api/{version}/objects/objectworkflows/tasks`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`object__v`, `record_id__v`

To retrieve all workflow tasks configured on an object, include the Vault object `name__v` and object record `id` field values as `object__v={name__v}&record_id__v={id}`. These two parameters are required when the `assignee__v` parameter is not used.

`assignee__v`

To retrieve all workflow tasks available to a particular user, include the user `id` field value as `assignee__v={id}`. To retrieve your own workflow tasks, set this value to `assignee__v=me()`. This parameter is required when the `object__v` and `record_id__v` parameters are not used.

`status__v`

To retrieve all workflow tasks with specific statuses, include one or more status `name__v` field values. For example: `status__v=available__v` or `status__v=available__v,completed__v`.

`offset`

This parameter is used to paginate the results. It specifies the amount of offset from the first record returned. Vault returns 200 records per page by default. If you are viewing the first 200 results (page 1) and want to see the next page, set this to `offset=201`.

`page_size`

This parameter is used to paginate the results. It specifies the size number of records to display per page. Vault returns 200 records per page by default. You can set this value lower or as high as 1000 records per page. For example: `page_size=1000`.

`loc`

When localized (translated) strings are available, retrieve them by including `loc=true`.

#### Response Details

On `SUCCESS`, the response lists all workflow tasks matching the query parameters. Each task may include the following fields:

-   `id` - The task ID.
-   `label__v` - The task label as seen in the UI.
-   `status__v` - The current status of the task.
-   `object__v` - The name of the object using the task.
-   `record_id__v` - The ID of the object record using the task.
-   `instructions__v` - Instructions for completing the task.
-   `assignee__v` - The ID of the user assigned the task. This is the task owner.
-   `created_date__v` - The date and time when the task was created.
-   `assigned_date__v` - The date and time when the task was assigned.
-   `due_date__v` - The date and time when the task is due.
-   `workflow__v` - The workflow ID in which the task is configured.
-   `workflow_class__sys` - Included with a value of `read_and_understood__sys` if the task is a Read & Understood task.

### Retrieve Workflow Task Details

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/123001
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseDetails": {
       "url": "/api/v25.2/objects/objectworkflows/tasks/123001",
       "object": {
           "name": "objectworkflow_tasks",
           "label": "Object Workflow Task",
           "url": "/api/v25.2/metadata/objectworkflows/tasks",
           "label_plural": "Object Workflow Tasks"
       }
   },
   "data": [
       {
           "id": 123001,
           "label__v": "R&U WF Task New",
           "status__v": [
               "assigned__v"
           ],
           "object__v": "envelope__sys",
           "record_id__v": "0ER00000003F001",
           "instructions__v": "Complete this new task",
           "assignee__v": "674737",
           "created_date__v": "2021-05-31T18:33:34.000Z",
           "assigned_date__v": "2021-05-31T18:33:34.000Z",
           "workflow__v": "22901",
           "workflow_class__sys": "read_and_understood__sys"
       }
   ]
}
'''

Retrieve the details of a specific workflow task.

GET `/api/{version}/objects/objectworkflows/tasks/{task_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{task_id}`

The task `id` field value.

#### Query Parameters

Name

Description

`loc`

When localized (translated) strings are available, retrieve them by including `loc=true`.

#### Response Details

On `SUCCESS`, the response lists all workflow tasks matching the query parameters. The task may include the following fields:

-   `id` - The task ID.
-   `label__v` - The task label as seen in the UI.
-   `status__v` - The current status of the task.
-   `object__v` - The name of the object using the task.
-   `record_id__v` - The ID of the object record using the task.
-   `instructions__v` - Instructions for completing the task.
-   `assignee__v` - The ID of the user assigned the task. This is the task owner.
-   `created_date__v` - The date and time when the task was created.
-   `assigned_date__v` - The date and time when the task was assigned.
-   `due_date__v` - The date and time when the task is due.
-   `workflow__v` - The workflow ID in which the task is configured.
-   `workflow_class__sys` - Included with a value of `read_and_understood__sys` if the task is a Read & Understood task.

### Retrieve Workflow Task Actions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/7201/actions
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "data": [
    {
       "name": "complete",
       "label": "Complete"
    },
    {
       "name": "cancel",
       "label": "Cancel"
    }
  ]
}
'''

Retrieve all available actions that can be initiated on a given workflow task.

GET `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{task_id}`

The task `id` field value.

### Retrieve Workflow Task Action Details

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/5702/actions/complete
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "name": "workflow_task__c",
       "label": "Complete Review",
       "type": "task",
       "description": "Initiate the Content Module Approval flow.",
       "controls": [
           {
               "label": "Instruction",
               "type": "instructions",
               "instructions": "Please complete a review of the content within this content module and review the Content Module Asset record status as well."
           },
           {
               "label": "Verdict",
               "type": "verdict",
               "verdict": "verdict_public_key__c",
               "reason": "reason__c",
               "capacity": "capacity__c",
               "verdicts": [
                   {
                       "name": "verdict_approve_module__c",
                       "label": "Approve Module",
                       "esignature": true,
                       "prompts": [],
                       "comment": {
                           "name": "verdict_approve_module_comment__c",
                           "label": "Optional Approval Comments",
                           "type": "comment",
                           "required": false
                       },
                       "reasons": {
                           "label": "Approved",
                           "required": true,
                           "prompts": [
                               {
                                   "name": "reason_0_0__c",
                                   "label": "Passes Inspection"
                               }
                           ]
                       },
                       "capacities": {
                           "label": "Approver",
                           "required": false,
                           "prompts": [
                               {
                                   "name": "capacity_0_0__c",
                                   "label": "General Approver"
                               }
                           ]
                       }
                   },
                   {
                       "name": "verdict_return_to_draft__c",
                       "label": "Return to Draft",
                       "esignature": false,
                       "prompts": [],
                       "comment": {
                           "name": "verdict_return_to_draft_comment__c",
                           "label": "Updates Required",
                           "type": "comment",
                           "required": true
                       },
                       "reasons": {
                           "label": "Fails Inspection",
                           "required": false,
                           "prompts": [
                               {
                                   "name": "reason_1_0__c",
                                   "label": "Poor Quality"
                               },
                               {
                                   "name": "reason_1_1__c",
                                   "label": "Incorrect Data"
                               },
                               {
                                   "name": "reason_1_2__c",
                                   "label": "Other"
                               }
                           ]
                       },
                       "capacities": {
                           "label": "Rejector",
                           "required": false,
                           "prompts": [
                               {
                                   "name": "capacity_1_0__c",
                                   "label": "General Rejector"
                               }
                           ]
                       }
                   }
               ]
           }
       ]
   }
}
'''

Retrieve the details of a specific workflow task action. The response lists the details of the task action, including all fields required to initiate the action. Note that task actions where `esignature` is `true` cannot be initiated via the API.

GET `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions/{task_action}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{task_id}`

The task `id` field value.

`{task_action}`

The name of the task action retrieved from [Retrieve Workflow Task Actions](#Retrieve_Workflow_Task_Actions).

#### Query Parameters

Name

Description

`loc`

When localized (translated) strings are available, retrieve them by including `loc=true`.

### Accept Multi-item Workflow Task

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/9626/actions/mdwaccept
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Accept an available task for a multi-record workflow. If the task is available to multiple users, any one of the assigned users can accept the task. To undo your acceptance of an available workflow task, use [Undo Workflow Task Acceptance](#Undo_Workflow_Task_Acceptance).

Vault may prevent you from accepting a task if you’ve already accepted, assigned, or completed another task, or have a restricted role.

POST `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions/mdwaccept`

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

`{task_id}`

The task `id` field value.

#### Response Details

On `SUCCESS`, Vault accepts the available workflow task on behalf of the authenticated user.

### Accept Single Record Workflow Task

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/9626/actions/accept
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Accept an available task for a workflow configured for a single record. If the task is available to multiple users, any one of the assigned users can accept the task. To undo your acceptance of an available workflow task, use [Undo Workflow Task Acceptance](#Undo_Workflow_Task_Acceptance).

Vault may prevent you from accepting a task if you’ve already accepted, assigned, or completed another task, or have a restricted role.

POST `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions/accept`

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

`{task_id}`

The task `id` field value.

#### Response Details

On `SUCCESS`, Vault accepts the available workflow task on behalf of the authenticated user.

### Undo Workflow Task Acceptance

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/9626/actions/undoaccept
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Undo your acceptance of an available workflow task. Once released, the task is available again to any of the assigned users. This endpoint supports single and multi-item workflows.

POST `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions/undoaccept`

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

`{task_id}`

The task `id` field value.

#### Response Details

On `SUCCESS`, Vault reeases the available workflow task on behalf of the authenticated user. The task is available again to any of the assigned users.

### Complete Multi-item Workflow Task

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
--data-binary @"complete-task.json" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/9626/actions/mdwcomplete
'''

> Example JSON Request Body: Single Verdict

'''
{
   "verdict_public_key__c": "verdict_not_approved__c",
   "verdict_not_approved_comment__c": "Needs to be redone."
}
'''

> Example JSON Request Body: Multiple Verdicts

'''
{
   "task_comment__v": "Some of these batches need to be reprocessed.",
   "contents__sys": [
    {
       "object__v": "batch__v",
       "record_id__v": "0BA000000000101",
       "verdict_public_key__c": "verdict_not_approved__c",
       "verdict_not_approved_comment__c": "Needs to be redone."
    },
    {
       "object__v": "batch__v",
       "record_id__v": "0BA000000002001",
       "verdict_public_key__c": "verdict_approved__c"
    },
    {
       "object__v": "batch__v",
       "record_id__v": "0BA000000002002",
       "verdict_public_key__c": "verdict_not_approved__c",
       "verdict_not_approved_comment__c": "Does not meet standards."
    }
   ]
}
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Complete an open workflow task for a multi-item workflow. This endpoint does not support initiating task actions requiring eSignatures (where `esignature` is `true`). To provide multiple verdicts for items without completing an open workflow task, use [Manage Multi-item Workflow Content](#Manage_Multi-item_Workflow_Content).

POST `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions/mdwcomplete`

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{task_id}`

The task `id` field value.

#### Body Parameters

Controls with `required=true` in the [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details) response must be provided. If a control (such as `verdict`) defines a set of required fields, those must also be provided. For example, a specific verdict may prompt for comments, reasons, or capacities.

For workflows where `type` is set to `multidocworkflow` and `cardinality` is set to `One`, Vault pre-populates document field values in field prompts. If you include keys for field prompts without values, Vault submits a blank field value on the document.

In the body of the request, upload parameters as a JSON file. This request may require the following body parameters:

Name

Description

`verdict_public_key__c`conditional

The verdict name. Retrieve possible verdict `name` values by sending a request to [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details).

`reason__c`conditional

The reason name. Retrieve possible reason `name` values by sending a request to [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details).

`capacity__c`conditional

The capacity name. Retrieve possible capacity `name` values by sending a request to [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details).

#### Response Details

On `SUCCESS`, Vault completes the workflow task on behalf of the authenticated user.

### Complete Single Record Workflow Task

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d 'verdict_not_approved_comment__c=Can'\''t approve this batch.' \
-d 'verdict_public_key__c=verdict_not_approved__c'
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/9201/actions/complete
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Complete an open workflow task for a workflow configured for a single record. This endpoint does not support initiating task actions requiring eSignatures (where `esignature` is `true`).

POST `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions/complete`

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

`{task_id}`

The task `id` field value.

#### Body Parameters

Controls with `required=true` in the [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details) response must be provided. If a control (such as `verdict`) defines a set of required fields, those must also be provided. For example, a specific verdict may prompt for comments, reasons, or capacities.

This request may require the following body parameters:

Name

Description

`verdict_public_key__c`conditional

The verdict name. Retrieve possible verdict `name` values by sending a request to [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details).

`reason__c`conditional

The reason name. Retrieve possible reason `name` values by sending a request to [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details).

`capacity__c`conditional

The capacity name. Retrieve possible capacity `name` values by sending a request to [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details).

#### Response Details

On `SUCCESS`, Vault completes the workflow task on behalf of the authenticated user.

### Reassign Multi-item Workflow Task

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-d 'task_assignee__v=user:2135709'
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/9626/actions/mdwreassign
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Reassign an open workflow task to another user for a multi-item workflow.

You cannot reassign a task to a user who is already assigned to that specific task, has completed that task, or is configured with a restricted role. However, you can reassign a user to continuing iterations of the same task if an Admin has enabled users in the workflow to only complete one task.

POST `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions/mdwreassign`

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

`{task_id}`

The `id` of the task to reassign.

#### Body Parameters

Name

Description

`task_assignee__v`required

The `id` of the user who will become the new task assignee, in the format `user:{id}`. For example, `user:100307`.

#### Response Details

Returns `SUCCESS` if the task was successfully reassigned. Vault notifies the new task owner and the previous task owner of the reassignment.

### Reassign Single Record Workflow Task

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-d 'task_assignee__v=user:2135709'
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/7102/actions/reassign
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Reassign an open workflow task to another user for a workflow configured for a single record.

You cannot reassign a task to a user who is already assigned to that specific task, has completed that task, or is configured with a restricted role. However, you can reassign a user to continuing iterations of the same task if an Admin has enabled users in the workflow to only complete one task.

POST `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions/reassign`

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

`{task_id}`

The `id` of the task to reassign.

#### Body Parameters

Name

Description

`task_assignee__v`required

The `id` of the user who will become the new task assignee, in the format `user:{id}`. For example, `user:100307`.

#### Response Details

Returns `SUCCESS` if the task was successfully reassigned. Vault notifies the new task owner and the previous task owner of the reassignment.

### Update Workflow Task Due Date

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-d 'task_due_date__v=2025-03-12'
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/7102/actions/updateduedate
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Update the due date of an assigned workflow task. This endpoint supports single and multi-item workflows.

If the workflow is configured to set all task due dates to the workflow due date, updates to individual task due dates will not affect the overall workflow due date. You cannot update task due dates that are configured to sync with an object or document field.

POST `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions/updateduedate`

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

`{task_id}`

The `id` of the task.

#### Body Parameters

Name

Description

`task_due_date__v`required

The new due date for the task, in the format `YYYY-MM-DD`. The new task due date cannot be the same as the current task due date.

#### Response Details

Returns `SUCCESS` if the due date was successfully updated. Vault notifies the task owner of the new due date.

### Cancel Workflow Task

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/7102/actions/cancel
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Cancel an open workflow task. This endpoint supports single and multi-record workflows.

POST `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions/cancel`

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

`{task_id}`

The task `id` field value.

#### Response Details

Returns `SUCCESS` if the task was canceled successfully.

### Manage Multi-item Workflow Content

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
--data-binary @"manage-content.json" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/tasks/9626/actions/mdwmanagecontent
'''

> Example JSON Request Body: Multiple Verdicts

'''
{
   "contents__sys": [
{
       "object__v": "batch__v",
       "record_id__v": "0BA000000000101",
       "verdict_public_key__c": "verdict_not_approved__c",
       "verdict_not_approved_comment__c": "Needs to be redone."
    },
    {
       "object__v": "batch__v",
       "record_id__v": "0BA000000002001",
       "verdict_public_key__c": "verdict_approved__c"
    },
    {
       "object__v": "batch__v",
       "record_id__v": "0BA000000002002",
       "verdict_public_key__c": "verdict_not_approved__c",
       "verdict_not_approved_comment__c": "Does not meet standards."
    }
   ]
}
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Manage content in a multi-item workflow without completing an open workflow task. For example, you can use this endpoint to provide verdicts for specific items without completing the task. This endpoint does not support initiating task actions requiring eSignatures (where `esignature` is `true`).

POST `/api/{version}/objects/objectworkflows/tasks/{task_id}/actions/mdwmanagecontent`

#### Headers

Name

Description

`Content-Type`

`application/json`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{task_id}`

The task `id` field value.

#### Body Parameters

Controls with `required=true` in the [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details) response can be provided. If a control (such as `verdict`) defines a set of required fields, those can also be provided. For example, a specific verdict may prompt for comments, reasons, or capacities.

In the body of the request, upload parameters as a JSON file. This request may include the following body parameters:

Name

Description

`verdict_public_key__c`conditional

The verdict name. Retrieve possible verdict `name` values by sending a request to [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details).

`reason__c`conditional

The reason name. Retrieve possible reason `name` values by sending a request to [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details).

`capacity__c`conditional

The capacity name. Retrieve possible capacity `name` values by sending a request to [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details).

#### Response Details

On `SUCCESS`, Vault modifies the contents in the multi-item workflow according to the JSON payload provided. Use [Retrieve Workflow Task Action Details](#Retrieve_Workflow_Task_Action_Details) to confirm any changes to `current_values`. You must use [Complete Multi-item Workflow Task](#Complete_Multi-item_Workflow_Task) to complete the open workflow task.

## Bulk Active Workflow Actions

The API allows you to retrieve actions and action details and to execute actions for up to 500 workflows at once. These can be object, document, or legacy workflows.

### Retrieve Bulk Workflow Actions

Retrieve all available workflow actions that can be initiated on a workflow which:

-   The authenticated user has permissions to view or initiate
-   Can be initiated through the API

> Request

'''
curl -L -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/object/workflow/actions
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "name": "canceltasks",
           "label": "Cancel Tasks"
       },
       {
           "name": "cancelworkflows",
           "label": "Cancel Workflows"
       },
       {
           "name": "reassigntasks",
           "label": "Reassign Tasks"
       },
       {
           "name": "replaceworkflowowner",
           "label": "Replace Workflow Owner"
       }
   ]
}
'''

GET `/api/{version}/object/workflow/actions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

On `SUCCESS`, the response lists all available workflow actions for a Vault.

Name

Description

`name`

The workflow action name.

`label`

The workflow action label as seen in the UI.

### Retrieve Bulk Workflow Action Details

Once you’ve retrieved the available workflow actions, use this request to retrieve the details for a specific workflow action.

> Request

'''
curl -L -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/object/workflow/actions/cancelworkflows
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "name": "cancelworkflows",
       "controls": [
           {
               "prompts": [
                   {
                       "multi_value": true,
                       "label": "Workflow Ids",
                       "required": true,
                       "name": "workflow_ids"
                   }
               ],
               "type": "field",
               "label": "Fields"
           }
       ]
   }
}
'''

GET `/api/{version}/object/workflow/actions/{action}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`action`

The `name` of the workflow action. To get this value, [Retrieve Bulk Workflow Actions](#Retrieve_Bulk_Workflow_Actions).

#### Response Details

On `SUCCESS`, the response returns metadata for the specified workflow action, including the fields required to execute the action.

For each control, the following data may be returned:

Name

Description

`label`

UI label for the control.

`type`

Type of control.

`prompts`

The input prompts which accept values when initiating a workflow action.

For each prompt, the following data may be returned:

Name

Description

`multi_value`

If `true`, indicates that the field accepts multiple values.

`label`

UI label for the prompt.

`required`

If `true`, indicates that the field is required to initiate the workflow action.

### Initiate Workflow Actions on Multiple Workflows

Use this request to initiate a workflow action on multiple workflows. This starts an asynchronous job whose status you can check with the Retrieve Job Status endpoint. Maximum 500 workflows per request.

> Request

'''
curl -L -X POST -H "Authorization: {SESSION_ID}" \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'workflow_ids=2903,2904,2905' \
https://myvault.veevavault.com/api/v25.2/object/workflow/actions/cancelworkflows
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "job_id": 93601
   }
}
'''

POST `/api/{version}/object/workflow/actions/{action}`

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

`action`

The `name` of the workflow action. To get this value, [Retrieve Bulk Workflow Actions](#Retrieve_Bulk_Workflow_Actions).

#### Body Parameters

In the body of the request, add any fields required to initiate the action. To find which fields are required for an action, [Retrieve Bulk Workflow Action Details](#Retrieve_Bulk_Workflow_Action_Details).

##### Cancel Active Workflows: cancelworkflows

Name

Description

`workflow_ids`required

Input a comma-separated list of `workflow_id__v` field values. Maximum 500 workflows.

`cancellation_comment`optional

If this workflow requires a comment for cancellation, use this parameter to provide a comment.

##### Reassign Workflow Tasks: reassigntasks

Note that this action can reassign a maximum of 500 tasks.

Name

Description

`current_task_assignee`required

Input the user ID of the user whose tasks you wish to reassign. You cannot reassign specific tasks for a user, only all tasks currently assigned to a user.

`new_task_assignee`required

Input the user ID of the user who will receive the newly assigned tasks.

##### Cancel Workflow Tasks: canceltasks

When cancelling tasks, you can do so by user ID or task ID. Use one of the following parameters:

Name

Description

`user_ids`conditional

To cancel tasks by user ID, input a comma-separated list of the user IDs for the users whose tasks you wish to cancel. You cannot cancel specific tasks for a user, only all tasks currently assigned to a user. Maximum 100 user IDs per request.

`task_ids`conditional

To cancel tasks by task ID, input a comma-separated list of the task IDs to cancel. You cannot cancel task IDs for a specific user, only all instances of the given task IDs.

##### Replace Workflow Owner: replaceworkflowowner

Name

Description

`new_workflow_owner`required

Input the ID of the user who will become the new workflow owner. For example, `54937`.

`current_workflow_owner`required

Input the ID of the user who is the current workflow owner. For example, `87944`.

#### Response Details

On `SUCCESS`, the response returns the `job_id` for the action, and the authenticated user will receive an email notification with details of any failures that occur. On `FAILURE`, the response returns an [error](#Errors) `type` and `message` describing the reason for the failure. For example, the API returns `INVALID_DATA` if a task cannot be reassigned because the new task assignee is not in the appropriate role.
