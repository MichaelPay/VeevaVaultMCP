<!-- 
VaultAPIDocs Section: # Object Lifecycle & Workflows
Original Line Number: 27071
Generated: August 30, 2025
Part 11 of 38
-->

# Object Lifecycle & Workflows

Object lifecycles are the sequences of states (Draft, In Review, etc.) an object record goes through. A lifecycle can be simple (two states that require users to manually move between them) or very complex (multiple states with different security and workflows that automatically move records from one state to another). In Vault, lifecycles simplify the implementation of business logic that traditionally required custom coding or time-consuming manual setup. A set of business rules applies to each state and defines what happens to object records in that state. Admins define these rules for each lifecycle state and Vault automatically applies them to every object record that enters the state.

Learn about [Lifecycles & Workflows](https://platform.veevavault.help/en/lr/52053) in Vault Help.

## Object Record User Actions

The API supports retrieval and initiation of user actions on Vault object records.

### Retrieve Object Record User Actions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/00P000000000301/actions

'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "links": [
                {
                    "rel": "metadata",
                    "href": "/api/v25.2/vobjects/product__v/00P000000000301/actions/Objectlifecyclestateuseraction.product__v.active_state__c.start_workflow_useraction__c",
                    "accept": "application/json",
                    "method": "GET"
                },
                {
                    "rel": "execute",
                    "href": "/api/v25.2/vobjects/product__v/00P000000000301/actions/Objectlifecyclestateuseraction.product__v.active_state__c.start_workflow_useraction__c",
                    "accept": "application/json",
                    "method": "POST"
                }
            ],
            "label": "Start Workflow",
            "type": "workflow",
            "name": "Objectlifecyclestateuseraction.product__v.active_state__c.start_workflow_useraction__c"
        }
    ]
}
'''

Retrieve all available user actions that can be initiated on a specific object record which:

-   The authenticated user has permissions to view or initiate
-   Can be initiated through the API

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/actions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The object `name__v` field value.

`{object_record_id}`

The object record `id` field value.

#### Query Parameters

Name

Description

`loc`

Optional: When `true`, retrieves localized (translated) strings for the `label`.

#### Response Details

On `SUCCESS`, the response lists all available user actions that can be initiated on the specified object record.

-   For users with the _View_ permission, the response includes a link to retrieve the metadata for the specified user action.
-   For users without the _View_ permission, the response returns an `INSUFFICIENT_ACCESS` error.
-   For users with the _Execute_ permission, the response includes a link to initiate the specified action.

Name

Description

`type`

The type of user action. For example, an action of the type State Change will appear as `state_change`. Object actions which are not attached to a lifecycle state appear as type `object_action`.

`name`

The user action name. `object_action` types include the `Objectaction` prefix. Lifecycle user action types, such as `workflow`, include the `Objectlifecyclestateuseraction` prefix.

`label`

The user action label as seen in the UI.

### Retrieve Object User Action Details

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/product_v/0PR0771/actions/Objectaction.product__v.copy_record__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "links": [
            {
                "rel": "metadata",
                "accept": "application/json",
                "Href": "api/v17.3/vobjects/product_v/0PR0771/actions/Objectaction.product__v.copy_record__c",
                "method": "GET"
            },
            {
                "rel": "execute",
                "accept": "application/json",
                "Href":      "api/v17.3/vobjects/product_v/0PR0771/actions/Objectaction.product__v.copy_record__c",
                "method": "POST"
            }
        ],
        "label": "Copy Record",
        "type": "object_action",
        "name": "Objectaction.product__v.copy_record__c"
    }
}
'''

Once you’ve retrieved the available user actions, use this request to retrieve the details for a specific user action.

GET `/api/{version}/vobjects/{object_name}/{object_record_id}/actions/{action_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`object_name`

The object `name__v` field value.

`object_record_id`

The object record `id` field value from which to retrieve user action details.

`action_name`

Either the name of the `Objectaction` or `Objectlifecyclestateuseraction` to initiate. This is obtained from the [Retrieve User Actions](#Retrieve_Object_Record_Lifecycle_Actions) request.

#### Response Details

On `SUCCESS`, the response returns metadata for the specified object action.

-   For users with the _View_ permission, the response includes a link to retrieve the metadata for the specified user action.
-   For users without the _View_ permission, the response returns an `INSUFFICIENT_ACCESS` error.
-   For users with the _Execute_ permission, the response includes a link to initiate the specified action.

#### Response Details

On `SUCCESS`, the response lists the fields that must be configured with values in order to initiate the user action. These are based on the controls configured in the workflow start step.

-   For users with the _View_ permission, the response includes a link to retrieve the metadata for the specified user action.
-   For users without the _View_ permission, the response returns an `INSUFFICIENT_ACCESS` error.
-   For users with the _Execute_ permission on the action, the response includes a link to initiate the specified action.

For actions with the `type: workflow`, the following types of controls may be returned:

Name

Description

`instructions`

Contains static instruction text regarding workflow initiation.

`participant`

Used to specify users who will be part of the workflow.

`date`

Date selections for the workflow, such as due date.

`field`

All object fields requiring values.

For each control, the following data may be returned:

Name

Description

`label`

UI Label for the control.

`type`

Type of control (instructions, participants, date, or fields).

`prompts`

The input prompts (if any) which accept values when initiating the workflow. Prompts of type `field` accept values per the metadata specified for the field in the object metadata.

### Initiate Object Action on a Single Record

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d 'due_date__c=2020-03-01T08:00:00.000Z' \
-d 'product__v.generic_name__c=nitroprinaline oxalate' \
-d 'product__v.internal_name__c=Nyaxa' \
-d 'product__v.compound_id__c=CC-127' \
-d 'approvers__c=user:10001399' \
https://myvault.veevavault.com/api/v25.2/vobjects/product__v/00P000000000301/actions/Objectlifecyclestateuseraction.product__v.active_state__c.start_workflow_useraction__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Use this request to initiate an action on a specific object record.

POST `/api/{version}/vobjects/{object_name}/{object_record_id}/actions/{action_name}`

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

`object_name`

The object `name__v` field value.

`object_record_id`

The object record `id` field value from which to retrieve user actions.

`action_name`

The name of the `Objectaction` or `Objectlifecyclestateuseraction` to initiate. You can retrieve this from the [Retrieve User Actions](#Retrieve_Object_Record_Lifecycle_Actions) request. The format for `action_name` is `Objectaction.{vobject}.{action}` or `Objectlifecyclestateuseraction.{vobject}.{state}.{action}`. For example, `Objectlifecyclestateuseraction.country__v.active_state__c.start_wf_useraction__c`.

#### Body Parameters

Include any parameters required to initiate the action as name-value pairs in the request body. You can retrieve the required parameters for your action by [Retrieving Object User Action Details](#Retrieve_Object_Record_Lifecycle_Action_Details).

Name

Description

`{participant_group_name}.assignment_type__c`conditional

The participant group assignment type for a workflow task, either `assigned` or `available`. Required if the workflow initiator must select either _Assigned to every user_ or _Available to any user_ when assigning participants to a task in the workflow start step. For example, `part_reviewers__c.assignment_type__c=assigned`.

`storyEventKey`optional

The ID of the target _Story Event_ object record when executing the [Apply Milestone Template](https://clinical.veevavault.help/en/lr/37552) action. This is only applicable in Clinical Operations Vaults.

##### Values in Required Field Prompts

When providing values for field prompts on a start step, task step, or verdict, required fields cannot be omitted, set as blank, or defaulted to their existing value.

To preserve the existing value of a required field prompt, submit the existing value as the new value.

### Initiate Object Action on Multiple Records

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "ids: 0MO0771, 0MO0772, 0MO0773" \
https://myvault.veevavault.com/api/v25.2/vobjects/monitoring_event__v/actions/Objectaction.monitoring_event__v.copy_record__v
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "data": [
      {
          "responseStatus": "SUCCESS",
          "id": "0MO0771"
      },
      {
          "responseStatus": "SUCCESS",
          "id": "0MO0772"
      },
      {
          "responseStatus": "FAILURE",
          "id": "0MO0773",
          "errors": [
              {
                  "type": "INSUFFICIENT_ACCESS",
                  "message": "User does not have sufficient privileges to perform the action"
              }
          ]
      }
  ]
}
'''

Use this request to initiate an object user action on multiple records. Maximum 500 records per batch.

POST `/api/{version}/vobjects/{object_name}/actions/{action_name}`

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

`object_name`

The object `name__v` field value.

`action_name`

The name of the `Objectaction` or `Objectlifecyclestateuseraction` to initiate. This is obtained from the [Retrieve User Actions](#Retrieve_Object_Record_Lifecycle_Actions) request. The format for `action_name` is `Objectaction.{vobject}.{action}` or `Objectlifecyclestateuseraction.{vobject}.{state}.{action}`. For example, `Objectlifecyclestateuseraction.country__v.active_state__c.start_wf_useraction__c`.

#### Body Parameters

Name

Description

`ids`required

Comma-separated list of object record ids on which to initiate the action.

`{participant_group_name}.assignment_type__c`conditional

The participant group assignment type for a workflow task, either `assigned` or `available`. Required if the workflow initiator must select either _Assigned to every user_ or _Available to any user_ when assigning participants to a task in the workflow start step. For example, `part_reviewers__c.assignment_type__c=assigned`.

##### Values in Required Field Prompts

When providing values for field prompts on a start step, task step, or verdict, required fields cannot be omitted, set as blank, or defaulted to their existing value.

To preserve the existing value of a required field prompt in a workflow on a single record, submit the existing value as the new value.

For a workflow on multiple records, there is no way to preserve existing values in a field if that field is a required prompt. Setting a value for a prompt updates all records to the same single value.

## Multi-Record Workflows

An object workflow is a series of steps configured in Vault to correspond with the specific business processes of your organization. These steps are actions that occur on or in relation to an individual object record or a group of object records on the same object.

Object workflows are specific to an object, meaning that a single workflow cannot apply to multiple objects. A single object record can only be in one workflow at a time.

### Retrieve All Multi-Record Workflows

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/actions
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "name": "Objectworkflow.approval__c",
           "label": "Review & Approval Workflow",
           "type": "multirecordworkflow",
           "cardinality": "OneOrMany"
       }
   ]
}

'''

Retrieve all available multi-record workflows which:

-   The authenticated user has permissions to view or initiate
-   Can be initiated through the API

GET `/api/{version}/objects/objectworkflows/actions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

On `SUCCESS`, the response includes the following:

Name

Description

`name`

The workflow name.

`label`

UI label for the workflow.

`type`

Type of workflow.

`cardinality`

Indicates how many contents (`One`, `OneOrMany`) can be included in a workflow.

For users without the _Workflow: Start_ permission, the response returns an `INSUFFICIENT_ACCESS` error.

### Retrieve Multi-Record Workflow Details

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/actions/Objectworkflow.approval__c
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "name": "Objectworkflow.approval__c",
       "controls": [
           {
               "prompts": [
                   {
                       "label": "Contents",
                       "name": "contents__sys"
                   }
               ],
               "type": "contents",
               "label": "Contents"
           },
           {
               "prompts": [
                   {
                       "multi_value": false,
                       "label": "Description",
                       "name": "description__sys"
                   }
               ],
               "type": "description",
               "label": "Description"
           }
       ],
       "label": "Multi-Object",
       "type": "multirecordworkflow",
       "cardinality": "OneOrMany"
   }
}
'''

Retrieves the fields required to initiate a specific multi-record workflow.

GET `/api/{version}/objects/objectworkflows/actions/{workflow_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{workflow_name}`

The multi-record workflow `name` value.

#### Response Details

On `SUCCESS`, the response lists the fields that must be configured with values in order to initiate the workflow. These are based on the controls configured in the workflow start step.

The response may include the following types of controls:

Name

Description

`prompts`

The input prompts which accept values when initiating the workflow.

`instructions`

Contains static instruction text regarding workflow initiation.

`participant`

Used to specify users who will be part of the workflow.

`date`

Date selections for the workflow, such as due date.

`documents`

Used to specify the documents for inclusion in the workflow.

`description`

The document workflow description.

`variable`

The variable prompts which accept values when initiating the workflow.

Additionally, the response includes following fields describing the workflow:

Name

Description

`name`

The workflow name.

`label`

UI Label for the workflow.

`type`

Type of workflow (`multirecordworkflow`).

`cardinality`

Indicates how many contents (`One`, `OneOrMany`) can be included in a workflow.

### Initiate Multi-Record Workflow

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "contents__sys: Object:feature_record__c.V3O000000005001,Object:feature_record__c.V3O000000005002" \
-d "description__sys: CSR Approval" \
-d "exec_approver__c: user:10081" \
https://myvault.veevavault.com/api/v25.2/objects/objectworkflows/actions/Objectworkflow.approval__c
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "record_url": "/api/v25.2/vobjects/envelope__sys/0ER000000009003",
       "record_id__v": "0ER000000009003",
       "workflow_id": "8703"
   }
}
'''

Initiate a multi-record workflow on a set of records. If any record is not in the relevant state or does not meet configured field conditions, the API returns `INVALID_DATA` for the invalid records and the workflow does not start.

POST `/api/{version}/objects/objectworkflows/actions/{workflow_name}`

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

`{workflow_name}`

The workflow `name` value.

#### Body Parameters

The following parameters are required, but an Admin may set other fields as required in your Vault. To find which fields are required to start this workflow, [Retrieve Multi-Record Workflow Details](#Retrieve_Multi_Record_Workflow_Details).

Name

Description

`contents__sys`required

Input a comma-separated list of records, in the format `Object:{objectname}.{record_ID}`. For example, `Object:product__c.V3O000000005001`. Maximum 100 records.

`description__sys`required

Description of the workflow. Maximum 128 characters.

##### Add Participants

To add participants to a workflow, add the name of the participant control to the body of the request. The value should be a comma-separated list of user and group IDs in the format `{user_or_group}:{id}`. For example, `approvers__c: user:123,group:234`. Use [Retrieve Document Workflow Details](#Retrieve_Multi_Document_Workflow_Details) to get the names of all participant controls for the workflow.

##### Values in Required Field Prompts

Required fields cannot be omitted, set as blank, or defaulted to their existing value.

To preserve the existing value of a required field prompt in a workflow on a single record, submit the existing value as the new value.

For a workflow on multiple records, there is no way to preserve existing values in a field if that field is a required prompt. Setting a value for a prompt updates all records to the same single value.

#### Response Details

On `SUCCESS`, the response includes the following:

Name

Description

`record_id__v`

The `id` value of the `envelope__sys` record.

`workflow_id`

The workflow `id` field value.

#### Manage Multi-record Workflow Tasks

Multi-record workflows are configured on the `envelope__sys` object. You can use the [Workflow Task](#Workflow_Tasks) endpoints to retrieve workflow tasks, details, and initiate tasks.

#### Remove Records from Workflow

You can remove one or more records from an `envelope__sys` object using the `removecontent` action in the [Initiate Workflow Action](#Initiate_Workflow_Action) endpoint.
