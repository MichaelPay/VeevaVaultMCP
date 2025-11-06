<!-- 
VaultAPIDocs Section: # Document Lifecycle & Workflows
Original Line Number: 24995
Generated: August 30, 2025
Part 10 of 38
-->

# Document Lifecycle & Workflows

Document lifecycles are the sequences of states (Draft, In Review, etc.) a document goes through during its life. A lifecycle can be simple (two states requiring users to manually move between states) or very complex (multiple states with different security and workflows that automatically move the document to another state). In Vault, lifecycles simplify the implementation of business logic that traditionally required custom coding or time-consuming manual setup.

Lifecycle states are the ordered states within a lifecycle representing the stages a document transitions through as users create, review, approve, and eventually archive or replace it. A set of business rules applies to each state and defines what happens to the document in that state. Admins define these rules for each lifecycle state and Vault automatically applies them to every document that enters the state.

Learn about [Lifecycles & Workflows in Vault Help](https://platform.veevavault.help/en/lr/52053).

## Document User Actions

This API allows you to initiate the following user action types:

-   **Workflow** (legacy): This action starts the specified legacy workflow. Only legacy workflows that are already configured and active for the selected lifecycle are available. To start a document workflow, see [Document Workflows](#Multi_Document_Workflows).
-   **State Change**: This action allows the user to manually move a document into a different lifecycle state. Vault enforces entry criteria and entry actions for the state change.
-   **Controlled Copy**: This action is available in QualityDocs Vaults and with the QualityOne application family. It allows the user to generate and distribute a controlled copy.
-   **Create Presentation**: This action is only available in PromoMats and Medcomms. It creates multiple _Multichannel Slide_ documents and a _Multichannel Presentation_ binder from a single document. This applies to Vaults that are configured for Engage integration or CLM integration.
-   **Create Email Fragment**: This action is only available in PromoMats and MedComms Vaults that are configured for _Approved Email Integration_. It creates an email fragment for a document by applying a master email fragment.

To initiate user actions on binders, see [Binder User Actions](#Binder_User_Actions).

Your Vault may include other user action types, not all of which can be initiated through Vault API. Learn more about [document user action types in Vault Help](https://platform.veevavault.help/en/lr/12339#types).

The API does not support initiation of user actions requiring eSignatures.

### Retrieve Document User Actions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/lifecycle_actions
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": "Success",
   "lifecycle_actions__v": [
       {
           "name__v": "start_review__c",
           "label__v": "Start Review",
           "lifecycle_action_type__v": "workflow",
           "lifecycle__v": "general_lifecycle__c",
           "state__v": "draft__c",
           "executable__v": "false"
       },
       {
           "name__v": "start_approval__c",
           "label__v": "Start Approval",
           "lifecycle_action_type__v": "workflow",
           "lifecycle__v": "general_lifecycle__c",
           "state__v": "draft__c",
           "executable__v": "true",
           "entry_requirements__v": "https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/lifecycle_actions/start_approval__c/entry_requirements"
       },
       {
           "name__v": "approve__c",
           "label__v": "Approve",
           "lifecycle_action_type__v": "stateChange",
           "lifecycle__v": "general_lifecycle__c",
           "state__v": "draft__c",
           "executable__v": "true",
           "entry_requirements__v": "https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/lifecycle_actions/approve__c/entry_requirements"
       }
   ]
}
'''

Retrieve all available user actions on a specific version of a document which:

-   The authenticated user has permission to view or initiate.
-   Can be initiated through the API. See [supported user actions](#Document_Binder_Lifecycle_Actions).
-   Is not currently in an active workflow.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/lifecycle_actions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value from which to retrieve available user actions.

`{major_version}`

The major version number of the document.

`{minor_version}`

The minor version number of the document.

#### Response Details

The response lists all available user actions (`lifecycle_actions__v`) that can be initiated on the specified version of the document.

Name

Description

`name__v`

The user action name (consumed by the API). These vary from Vault to Vault and may be text, numeric, or alphanumeric values.

`label__v`

The user action label displayed to users in the UI.

`lifecycle_action_type__v`

The `workflow` (legacy) and `stateChange` types are the most commonly used and are available in all Vaults. Others may exist.

`lifecycle__v`

The document lifecycle the action belongs to. For example, `general_lifecycle__c`.

`state__v`

The state of the document.

`executable__v`

Indicates if the currently authenticated user has _Execute_ permission for this action. This is `true` if the user can execute the action, otherwise `false`.

`entry_requirements__v`

The endpoint to retrieve the entry requirements for each user action. If no entry criteria exist, this endpoint returns an empty list. If the authenticated user does not have permission to execute this action, `entry_requirements__v` does not appear in the response.

### Retrieve User Actions on Multiple Documents

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "docIds=22:0:1,21:1:0,20:1:0" \
https://myvault.veevavault.com/api/v25.2/objects/documents/lifecycle_actions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "lifecycle_actions__v": [
        {
            "name__v": "make_obsolete__c",
            "label__v": "Make Obsolete",
            "lifecycle_action_type__v": "stateChange",
            "lifecycle__v": "general_lifecycle__c",
            "state__v": "approved__c",
            "entry_requirements__v": "https://myvault.veevavault.com/api/v25.2/objects/documents/lifecycle_actions/make_obsolete__c/entry_requirements?lifecycle=general_lifecycle__c&state=approved__c"
        },
        {
            "name__v": "approve__c",
            "label__v": "Approve",
            "lifecycle_action_type__v": "stateChange",
            "lifecycle__v": "general_lifecycle__c",
            "state__v": "draft__c",
            "entry_requirements__v": "https://myvault.veevavault.com/api/v25.2/objects/documents/lifecycle_actions/approve__c/entry_requirements?lifecycle=general_lifecycle__c&state=draft__c"
        }
    ]
}
'''

Retrieve all available user actions on specific versions of multiple documents.

POST `/api/{version}/objects/documents/lifecycle_actions`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Name

Description

`docIds`required

The `id` and version numbers for each document for which to retrieve the available user actions. Include a comma-separated list of document IDs and major and minor version numbers in the format `{doc_id:major_version:minor_version}`. For example, `22:0:1`.

#### Response Details

The response lists all available lifecycle actions (`lifecycle_actions__v`) that can be initiated on the specified versions of multiple documents.

Name

Description

`name__v`

The lifecycle action name (consumed by the API). These vary from Vault to Vault and may be text, numeric, or alphanumeric values.

`label__v`

The lifecycle action label. This is the “User Action” label seen in the UI.

`lifecycle_action_type__v`

The `workflow` (legacy) and `stateChange` types are the most commonly used and are available in all Vaults. Others may exist.

`lifecycle__v`

The document lifecycle the action belongs to. For example, `general_lifecycle__c`.

`state__v`

The state of the document.

`entry_requirements__v`

The endpoint to retrieve the entry requirements for each lifecycle action. If no entry requirements exist, the endpoint returns an empty list.

Lifecycle actions are not returned for documents which are currently in an active workflow.

### Retrieve Document Entry Criteria

> Request: Start Legacy Workflow

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/lifecycle_actions/start_approval__c/entry_requirements
'''

> Response: Start Legacy Workflow

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": "Success",
   "properties": [
       {
           "name": "user_control_multiple__c",
           "description": "Approver",
           "type": [
               "ObjectReference"
           ],
           "objectTypeReferenced": {
               "name": "User",
               "label": "User"
           },
           "required": true,
           "editable": true,
           "repeating": true,
           "scope": "WorkflowActivation"
       },
       {
           "name": "date_control__c",
           "description": "Approval Due Date",
           "type": [
               "Date"
           ],
           "required": true,
           "editable": true,
           "scope": "WorkflowActivation"
       }
   ]
}
'''

> Request: Change State

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/lifecycle_actions/approve__c/entry_requirements
'''

> Response: Change State

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": "Success",
   "properties": [
       {
           "name": "country__v",
           "description": "Country",
           "type": [
               "ObjectReference"
           ],
           "objectTypeReferenced": {
               "name": "country__v",
               "label": "Country",
               "url": "/api/v25.2/metadata/vobjects/country__v",
               "label_plural": "Countries"
           },
           "required": true,
           "editable": true,
           "repeating": true,
           "scope": "Document",
           "currentSetting": [
               {
                   "name": "00C000000000109",
                   "label": "United States",
                   "value": "/api/v25.2/vobjects/country__v/00C000000000109"
               }
           ],
           "records": "/api/v25.2/vobjects/country__v"
       }
   ]
}
'''

Retrieve the entry criteria for a user action. Entry criteria are requirements the document must meet before you can [initiate the action](#Initiate_Lifecycle_Action). Entry criteria are dynamic and depend on the lifecycle configuration, lifecycle state, or any workflow activation requirements defined in the _Start Step_ of the workflow. Learn more about [entry criteria in Vault Help](https://platform.veevavault.help/en/lr/12617#types).

To retrieve entry criteria, the authenticated user must have permission to execute the action. To check permissions, [Retrieve User Actions](#Retrieve_Lifecycle_Actions) and check for actions where `executable__v` is `true`.

GET `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{name__v}/entry_requirements`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{doc_id}`

The document `id` field value from which to retrieve available user actions.

`{major_version}`

The major version number of the document.

`{minor_version}`

The minor version number of the document.

`{name__v}`

The lifecycle `name__v` field value from which to retrieve entry criteria. Retrieve this value from [Retrieve User Actions](#Retrieve_Lifecycle_Actions).

#### Response Details

The response may include the following metadata elements describing the properties for which values need to be specified:

Name

Description

`name`

The entry criteria name (used in the API). This value must be specified when starting the user action.

`description`

The entry criteria name (used in the UI).

`type`

The entry criteria data type. This value can be one of `String`, `Number`, `Date`, `Boolean`, `Picklist`, or `ObjectReference`.

`objectTypeReferenced`

When `type` is `ObjectReference`, this is the object being referenced. For example: `User`, `Product`, `Country`, etc.

`required`

Boolean value indicating whether or not the entry criteria must be specified when initiating a user action.

`editable`

Boolean value indicating whether or not the value can be edited by the user.

`repeating`

Boolean value indicating whether or not the entry criteria can have multiple values.

`minValue`

Indicates the minimum character length for the value.

`maxValue`

Indicates the maximum character length for the value.

`values`

When `type` is `Picklist`, this provides a list of possible values that can be used.

`currentSetting`

When a value has already been set, this shows the value.

`scope`

Indicates where the entry criteria property is defined. This value can be one of:

-   `Document`: This field must be set on the document before the action can be initiated.
-   `WorkflowActivation`: This field must be included in the body of the initiate request.
-   `ControlledCopy`: This field must be included in the body of the initiate request.
-   `EmailFragment` or `CreatePresentation`

#### Response Details: Start Legacy Workflow

This example requests entry criteria for the `start_approval__c` workflow on document ID 17. The `properties` array in the response shows there are two entry criteria:

##### Approver: user\_control\_multiple\_\_c

Name

Description

`name`

The name of this entry criteria in the API is `user_control_multiple__c`. Use this name when referring to this field in the API.

`description`

The label of this entry criteria in the UI is **Approver**. This should tell you the intended usage of this field.

`type`

This field is an `ObjectReference`.

`objectTypeReferenced`

This field is an `ObjectReference` to a `User`.

`repeating`

This field can accept more than one value, meaning more than one user can be assigned as the approver.

`scope`

The scope is `WorkflowActivation`, which means you can include this data as a name-value pair in the [initiate](#Initiate_Lifecycle_Action) request.

##### Approval Due Date: date\_control\_\_c

Name

Description

`name`

The name of this entry criteria in the API is `date_control__c`. Use this name when referring to this field in the API.

`description`

The label of this entry criteria in the UI is **Approval Due Date**. This should tell you the intended usage of this field.

`type`

This field is a `Date`.

`scope`

The scope is `WorkflowActivation`, which means you can include this data as a name-value pair in the [initiate](#Initiate_Lifecycle_Action) request.

#### Response Details: Change State

This example requests entry criteria for the `approve__c` user action on document ID 17. The `properties` array in the response shows there is one entry criteria:

##### Country: country\_\_v

Name

Description

`name`

The name of this entry criteria in the API is `country__v`.

`description`

The label of this entry criteria in the UI is **Country**.

`type`

This field is an `ObjectReference`.

`objectTypeReferenced`

This field is an `ObjectReference` to the `Country` object.

`repeating`

This field can accept more than one value, meaning the document can belong to more than one country.

`scope`

The scope is `Document`, which means this document field must have a value before you can [initiate](#Initiate_Lifecycle_Action) the action.

`currentSetting`

The field on this document is currently set to `United States`. If you’re okay with this setting, you can [initiate](#Initiate_Lifecycle_Action) the action. If this was blank, you’d need to set it first.

### Initiate Document User Action

> Request: Start Legacy Workflow

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d 'user_control_multiple__c=user%3A10001400&date_control__c=2019-10-31'\
https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/lifecycle_actions/start_approval__c


'''

> Response: Start Legacy Workflow

'''
{
   "responseStatus": "SUCCESS",
   "id": 17,
   "workflow_id__v": "401"
}
'''

> Request: Change State

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/lifecycle_actions/approve__vs
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "id": 17
}
'''

Initiate a user action. Before initiating, you should retrieve any applicable [entry criteria](#Retrieve_Entry_Requirements) for the action.

Only some user action types can be initiated through the API. See [supported user actions](#Document_Binder_Lifecycle_Actions).

The authenticated user must have permission to initiate this action. To check permissions, [Retrieve User Actions](#Retrieve_Lifecycle_Actions) and check for actions where `executable__v` is `true`.

PUT `/api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{name__v}`

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

`{doc_id}`

The document `id` field value on which to initiate the user action.

`{major_version}`

The major version number of the document.

`{minor_version}`

The minor version number of the document.

`{name__v}`

The action `name__v` field value to initiate. Retrieve this value from [Retrieve User Action](#Retrieve_Lifecycle_Actions).

#### Request Details: Start Legacy Workflow

This request is initiating a `start_approval__c` workflow. [Retrieving the entry criteria](#Retrieve_Entry_Requirements) told us what fields we need to add to initiate this action, and that the `scope` is `WorkflowActivation`. This scope means we can add the required entry criteria fields as name-value pairs in the body of this request.

-   `user_control_multiple__c=user%3A10001400` is an `ObjectReference` to a `User`.
-   `date_control__c=2019-10-31` is a `Date`.

#### Request Details: Change State

This request is initiating the `approve__c` user action, which changes the state of the document to _Approved_. [Retrieving the entry criteria](#Retrieve_Entry_Requirements) told us what fields we need to add or update to initiate this action, and that the `scope` is `Document`. This scope means the required entry criteria must be set on the document prior to this request, so there are no additional parameters to add to this initiate request.

### Download Controlled Copy Job Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/actions/draft_to_effective_lifecycle__c.effective__c.downloadControlledCopya95fbf38/39303/results
  -OJ
'''

> Response Headers

'''
Content-Type: application/octet-stream;charset=UTF-8
Content-Disposition: attachment;filename="Download Issued Batch Record - 2018-10-10T22-01-18.473Z.zip"
'''

This endpoint is for Extensible Controlled Copy; `controlled_copy_trace__v` and `controlled_copy_user_input__v` objects. If your organization is not using these objects, you should use the endpoints for [Legacy Controlled Copy](#Document_Events).

After initiating a controlled copy user action, use this endpoint to download the controlled copy. To execute this request in an integration flow, [Retrieve the Job Status](#RetrieveJobStatus) and use the `href` under `"rel": "artifacts"`. We do not recommend executing this request outside of this flow.

Before submitting this request:

-   You must have previously requested an initiate controlled copy job (via the API) which is no longer active
-   You must be the user who initiated the job or have the _Admin: Jobs: Read_ permission

GET `/api/{version}/objects/documents/actions/{lifecycle_and_state_and_action}/{job_id}/results`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`. For this request, the `Accept` header controls only the error response. On `SUCCESS`, the response is a file stream (download).

#### URI Path Parameters

Name

Description

`{lifecycle_and_state_and_action}`

The `name__v` values for the lifecycle, state, and action in the format `{lifecycle_name}.{state_name}.{action_name}`. To get this value, [Retrieve the Job Status](#RetrieveJobStatus) and find the `href` under `"rel": "artifacts"`.

`{job_id}`

The ID of the job, returned from the original job request. For controlled copy, you can find this ID in the [Initiate User Action](#Initiate_Lifecycle_Action) response.

#### Response Details

On `SUCCESS`, Vault downloads your controlled copy.

The HTTP Response Header `Content-Type` is set to `application/octet-stream`. The HTTP Response Header `Content-Disposition` contains a default filename component which you can use when naming the local file.

By default, your file is named in the format `{user action label} - {now()}.zip`, which is consistent with downloading this file through the Vault UI. If you choose to name this file yourself, make sure you add the `.zip` extension.

### Initiate Bulk Document User Actions

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "docIds=222:0:1,223:0:1,224:0:1,225:0:1" \
-d "lifecycle=general_lifecycle__c" \
-d "state=draft__c" \
https://myvault.veevavault.com/api/v25.2/objects/documents/lifecycle_actions/approve__c
'''

> Response

'''
{
  "responseStatus": "SUCCESS"
}
'''

For each bulk action, you may only select a single workflow that Vault will start for all selected and valid documents.

PUT `/api/{version}/objects/documents/lifecycle_actions/{user_action_name}`

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

`{user_action_name}`

The user action `name__v` field value. Find this value with the [Retrieve User Actions on Multiple Documents](#Retrieve_Multiple_Document_User_Actions) endpoint.

#### Body Parameters

Name

Description

`docIds`required

Include a comma-separated list of document IDs and major and minor version numbers. For example, `222:0:1,223:0:1,224:0:1` specifies version 0.1 of document IDs 222, 223, and 224. The user action is only executed on document IDs in the `lifecycle` and `state` specified in the request body. Document IDs listed in this parameter which are not in the specified `lifecycle` and `state` are skipped.

`lifecycle`required

Include the name of the document lifecycle.

`state`required

Include the current state of your document.

#### Request Details

In this request:

-   The input file format is set to accept name-value pairs.
-   The lifecycle is specified. These documents are assigned to the `general_lifecycle__c`.
-   The state is specified. We’re changing the state of all four documents from draft to approved.

#### Response Details

On `SUCCESS`, the initiating user receives a summary email detailing which documents succeeded and failed the requested action.

## Binder User Actions

This API allows you to initiate user actions on binders. See [supported user actions](#Document_Binder_Lifecycle_Actions).

Your Vault may include other user action types, not all of which can be initiated through Vault API. Learn more about [document user action types in Vault Help](https://platform.veevavault.help/en/lr/12339#types).

The API does not support initiation of user actions requiring eSignatures.

### Retrieve Binder User Actions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/17/versions/0/1/lifecycle_actions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "lifecycle_actions__v": [
        {
            "name__v": "request_content__c",
            "label__v": "Send to Content Creator",
            "lifecycle_action_type__v": "workflow",
            "lifecycle__v": "job_processing__c",
            "state__v": "draft__c",
            "executable__v": true,
            "entry_requirements__v": "https://myvault.veevavault.com/api/v25.2/objects/binders/152/versions/0/1/lifecycle_actions/request_content__c/entry_requirements"
        },
        {
            "name__v": "submit_for_review__c",
            "label__v": "Submit for Review",
            "lifecycle_action_type__v": "workflow",
            "lifecycle__v": "job_processing__c",
            "state__v": "draft__c",
            "executable__v": true,
            "entry_requirements__v": "https://myvault.veevavault.com/api/v25.2/objects/binders/152/versions/0/1/lifecycle_actions/submit_for_review__c/entry_requirements"
        },
        {
            "name__v": "review_annotate__c",
            "label__v": "Review & Annotate",
            "lifecycle_action_type__v": "workflow",
            "lifecycle__v": "job_processing__c",
            "state__v": "draft__c",
            "executable__v": true,
            "entry_requirements__v": "https://myvault.veevavault.com/api/v25.2/objects/binders/152/versions/0/1/lifecycle_actions/review_annotate__c/entry_requirements"
        }
    ]
}
'''

Retrieve all available user actions on a specific version of a binder which:

-   The authenticated user has permission to view or initiate.
-   Can be initiated through the API. See [supported user actions](#Document_Binder_Lifecycle_Actions).
-   Is not currently in an active workflow.

GET `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{binder_id}`

The `id` field value of the binder from which to retrieve available user actions.

`{major_version}`

The major version number of the binder.

`{minor_version}`

The minor version number of the binder.

#### Response Details

The response lists all available user actions (`lifecycle_actions__v`) that can be initiated on the specified version of the binder.

Name

Description

`name__v`

The user action name (consumed by the API). These vary from Vault to Vault and may be text, numeric, or alphanumeric values.

`label__v`

The user action label displayed to users in the UI.

`lifecycle_action_type__v`

The `workflow` (legacy) and `stateChange` types are the most commonly used and are available in all Vaults. Others may exist.

`lifecycle__v`

The binder lifecycle the action belongs to. For example, `general_lifecycle__c`.

`state__v`

The state of the binder.

`executable__v`

Indicates if the currently authenticated user has _Execute_ permission for this action. This is `true` if the user can execute the action, otherwise `false`.

`entry_requirements__v`

The endpoint to retrieve the entry requirements for each user action. If no entry criteria exist, this endpoint returns an empty list. If the authenticated user does not have permission to execute this action, `entry_requirements__v` does not appear in the response.

### Retrieve User Actions on Multiple Binders

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "docIds=152:0:1,153:1:0,154:1:0" \
https://myvault.veevavault.com/api/v25.2/objects/binders/lifecycle_actions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "lifecycle_actions__v": [
        {
            "name__v": "read__c",
            "label__v": "Read",
            "lifecycle_action_type__v": "workflow",
            "lifecycle__v": "job_processing__c",
            "state__v": "draft__c",
            "executable__v": true,
            "entry_requirements__v": "https://myvault.veevavault.com/api/v25.2/objects/binders/lifecycle_actions/read__c/entry_requirements?lifecycle=job_processing__c&state=draft__c"
        }
    ]
}
'''

Retrieve all available user actions on specific versions of multiple binders.

POST `/api/{version}/objects/binders/lifecycle_actions`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Name

Description

`docIds`required

The `id` and version numbers of binders for which to retrieve the available user actions. Include a comma-separated list of binder IDs and major and minor version numbers in the format `{binder_id:major_version:minor_version}`. For example, `22:0:1`.

#### Response Details

The response lists all available lifecycle actions (`lifecycle_actions__v`) that can be initiated on the specified versions of multiple binders.

Name

Description

`name__v`

The lifecycle action name (consumed by the API). These vary from Vault to Vault and may be text, numeric, or alphanumeric values.

`label__v`

The lifecycle action label. This is the “User Action” label seen in the UI.

`lifecycle_action_type__v`

The `workflow` (legacy) and `stateChange` types are the most commonly used and are available in all Vaults. Others may exist.

`lifecycle__v`

The binder lifecycle the action belongs to. For example, `general_lifecycle__c`.

`state__v`

The state of the binder.

`entry_requirements__v`

The endpoint to retrieve the entry requirements for each lifecycle action. If no entry requirements exist, the endpoint returns an empty list.

Lifecycle actions are not returned for binders which are currently in an active workflow.

### Retrieve Binder Entry Criteria

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/binders/152/versions/0/1/lifecycle_actions/read__c/entry_requirements
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Success",
    "properties": [
        {
            "name": "user_control_multiple__c",
            "description": "Read",
            "type": [
                "ObjectReference"
            ],
            "objectTypeReferenced": {
                "name": "User",
                "label": "User"
            },
            "required": true,
            "editable": true,
            "repeating": true,
            "scope": "WorkflowActivation"
        }
    ]
}
'''

Retrieve the entry criteria for a user action. Entry criteria are requirements the binder must meet before you can [initiate the action](#Initiate_Lifecycle_Action). Entry criteria are dynamic and depend on the lifecycle configuration, lifecycle state, or any workflow activation requirements defined in the _Start Step_ of the workflow. Learn more about [entry criteria in Vault Help](https://platform.veevavault.help/en/lr/12617#types).

To retrieve entry criteria, the authenticated user must have permission to execute the action. To check permissions, [Retrieve User Actions](#Retrieve_Lifecycle_Actions) and check for actions where `executable__v` is `true`.

GET `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{name__v}/entry_requirements`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{binder_id}`

The binder `id` field value from which to retrieve available user actions.

`{major_version}`

The major version number of the binder.

`{minor_version}`

The minor version number of the binder.

`{name__v}`

The lifecycle `name__v` field value from which to retrieve entry criteria. Retrieve this value from [Retrieve User Actions](#Retrieve_Lifecycle_Actions).

#### Response Details

The response may include the following metadata elements describing the properties for which values need to be specified:

Name

Description

`name`

The entry criteria name (used in the API). This value must be specified when starting the user action.

`description`

The entry criteria name (used in the UI).

`type`

The entry criteria data type. This value can be one of `String`, `Number`, `Date`, `Boolean`, `Picklist`, or `ObjectReference`.

`objectTypeReferenced`

When `type` is `ObjectReference`, this is the object being referenced. For example: `User`, `Product`, `Country`, etc.

`required`

Boolean value indicating whether or not the entry criteria must be specified when initiating a user action.

`editable`

Boolean value indicating whether or not the value can be edited by the user.

`repeating`

Boolean value indicating whether or not the entry criteria can have multiple values.

`minValue`

Indicates the minimum character length for the value.

`maxValue`

Indicates the maximum character length for the value.

`values`

When `type` is `Picklist`, this provides a list of possible values that can be used.

`currentSetting`

When a value has already been set, this shows the value.

`scope`

Indicates where the entry criteria property is defined. This value can be one of:

-   `Binder`: This field must be set on the binder before the action can be initiated.
-   `WorkflowActivation`: This field must be included in the body of the initiate request.
-   `EmailFragment` or `CreatePresentation`

### Initiate Binder User Action

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d 'user_control_multiple__c=user%3A10001400&date_control__c=2019-10-31'\
https://myvault.veevavault.com/api/v25.2/objects/binders/17/versions/0/1/lifecycle_actions/start_approval__c

'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "id": 17,
   "workflow_id__v": "401"
}
'''

Initiate a user action. Before initiating, you should retrieve any applicable [entry criteria](#Retrieve_Entry_Requirements) for the action.

Only some user action types can be initiated through the API. See [supported user actions](#Document_Binder_Lifecycle_Actions).

The authenticated user must have permission to initiate this action. To check permissions, [Retrieve User Actions](#Retrieve_Lifecycle_Actions) and check for actions where `executable__v` is `true`.

PUT `/api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{name__v}`

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

`{binder_id}`

The binder `id` field value on which to initiate the user action.

`{major_version}`

The major version number of the binder.

`{minor_version}`

The minor version number of the binder.

`{name__v}`

The action `name__v` field value to initiate. Retrieve this value from [Retrieve User Action](#Retrieve_Lifecycle_Actions).

### Initiate Bulk Binder User Actions

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "docIds=222:0:1,223:0:1,224:0:1,225:0:1" \
-d "lifecycle=general_lifecycle__c" \
-d "state=draft__c" \
https://myvault.veevavault.com/api/v25.2/objects/documents/lifecycle_actions/approve__c
'''

> Response

'''
{
  "responseStatus": "SUCCESS"
}
'''

For each bulk action, you may only select a single workflow that Vault will start for all selected and valid binders.

PUT `/api/{version}/objects/binders/lifecycle_actions/{user_action_name}`

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

`{user_action_name}`

The user action `name__v` field value. Find this value with the [Retrieve User Actions on Multiple Binders](#Retrieve_Multiple_Binder_User_Actions) endpoint.

#### Body Parameters

Name

Description

`docIds`required

Include a comma-separated list of binder IDs and major and minor version numbers. For example, `222:0:1,223:0:1,224:0:1` specifies version 0.1 of binder IDs 222, 223, and 224. The user action is only executed on binder IDs in the `lifecycle` and `state` specified in the request body. Binder IDs listed in this parameter which are not in the specified `lifecycle` and `state` are skipped.

`lifecycle`required

Include the name of the binder lifecycle.

`state`required

Include the current state of your binder.

#### Request Details

In this request:

-   The input file format is set to accept name-value pairs.
-   The lifecycle is specified. These documents are assigned to the `general_lifecycle__c`.
-   The state is specified. We’re changing the state of all four binders from draft to approved.

#### Response Details

On `SUCCESS`, the initiating user receives a summary email detailing which binders succeeded and failed the requested action.

## Lifecycle Role Assignment Rules

For both standard and custom roles, you can define a subset of users who are allowed in the role and define users that Vault automatically assigns to the role at document creation or when a workflow starts. You can also override the allowed users and default users settings based on standard object-type document fields like Country, Product, Study, etc.

#### Vault Help Resources

-   [Lifecycles & Workflows](https://platform.veevavault.help/en/lr/52053)
-   [Defining Allowed & Default Users for Roles](https://platform.veevavault.help/en/lr/6572)
-   [Users & Groups](https://platform.veevavault.help/en/lr/37744)
-   [Fields & Objects](https://platform.veevavault.help/en/lr/33946)

Note the following limitations:

-   The API can only be used with active lifecycles and roles.
-   If the input contains duplicate field values, only the first instance is processed. The remaining duplicate fields are ignored.
-   The maximum number of roles that can be created or updated per request is 50,000.
-   The lifecycle role default rule cannot be set when creating override rules.
-   A role cannot be assigned more users or groups to default roles than allowed on the role.
-   The default `owner__v` role cannot be edited.

### Retrieve Lifecycle Role Assignment Rules (Default & Override)

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/configuration/role_assignment_rule?lifecycle__v=general_lifecycle__c&role__v=editor__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "lifecycle__v": "general_lifecycle__c",
            "role__v": "editor__c",
            "allowed_users__v": [
                "ally@veepharm.com",
                "beth@veepharm.com",
                "cruz@veepharm.com",
                "dave@veepharm.com"
            ],
            "allowed_groups__v": [
                "global_products_team__c",
                "vault_products_team__c",
                "vault_doc_management__c"
            ],
            "allowed_default_users__v": [
                "ally@veepharm.com"
            ],
            "allowed_default_groups__v": [
                "global_products_team__c"
            ]
        },
        {
            "lifecycle__v": "general_lifecycle__c",
            "role__v": "editor__c",
            "product__v.name__v": "CholeCap",
            "country__v.name__v": "United States",
            "product__v": "0PR0011001",
            "country__v": "0CR0022002",
            "allowed_users__v": [
                "etta@veepharm.com",
                "finn@veepharm.com",
                "greg@veepharm.com",
                "hope@veepharm.com"
            ],
            "allowed_groups__v": [
                "cholecap_us_docs_group__c",
                "cholecap_us_research_group__c",
                "cholecap_us_compliance_group__c",
                "cholecap_us_product_management_group__c"
            ],
            "allowed_default_users__v": [
                "etta@veepharm.com"
            ],
            "allowed_default_groups__v": [
                "cholecap_us_docs_group__c"
            ]
        }
    ]
}
'''

GET `/api/{version}/configuration/role_assignment_rule`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml` or CSV `text/csv`

This endpoint alone will retrieve a list of all lifecycle role assignment rules (default & override) from all roles in all lifecycles in your Vault.

To filter the results by lifecycle or role, add one or both of the following parameters to the request endpoint:

#### Query Parameters

Name

Description

`lifecycle__v`

Include the name of the lifecycle from which to retrieve information. For example: `lifecycle_v=general_lifecycle__c`

`role__v`

Include the name of the role from which to retrieve information. For example: `role__v=editor__c`

`product__v`

Include the ID/name of a specific product to see product-based override rules to default users/allowed users for the lifecycle role. For example: `product__v=0PR0011001` or `product__v.name__v=CholeCap`

`country__v`

Include the ID/name of a specific country to see country-based override rules to default users/allowed users for the lifecycle role. For example: `country__v=0CR0022002` or `country__v.name__v=United States`

`study__v`

In eTMF Vaults only. Include the ID/name of a specific study to see study-based override rules to default users/allowed users for the lifecycle role. For example: `study__v=0ST0021J01` or `study__v.name__v=CholeCap Study`

`study_country__v`

In eTMF Vaults only. Include the ID/name of a specific study country to see study country-based override rules to default users/allowed users for the lifecycle role. For example: `study_country__v=0SC0001001` or `study_country__v.name__v=Germany`

The response will include:

-   The default role assignments
-   The override role assignments when an override condition (when configured on the role) is met
-   The override conditions (when configured on the role)

If you filter the results by one or more override conditions (`product__v` or `country__v`), the response will exclude the default role assignments and role assignments for the override conditions.

#### Request Details

Retrieve lifecycle role assignment rules from a specific role (`editor__c`) in a specific lifecycle (`general_lifecycle__c`):

#### Response Details

In this example response, the `editor__c` role in the `general_lifecycle__c` lifecycle is configured with the following role assignment rules:

**Default Rule**

When a document is assigned this lifecycle, the following users and groups are automatically assigned to the `editor__c` role:

-   `allowed_default_users__v` - The user `ally@veepharm.com` is automatically assigned to the role.
-   `allowed_users__v` - The users `beth@veepharm.com`, `cruz@veepharm.com`, and `dave@veepharm.com` can be (optionally) assigned to the role at any time during the lifecycle.
-   `allowed_default_groups__v` - The group `global_products_team__c` is automatically assigned to the role.
-   `allowed_groups__v` - The groups `vault_products_team__c` and `vault_doc_management__c` can be (optionally) assigned to the role at any time during the lifecycle.

**Override Conditions**

This lifecycle role has been configured with two override conditions which state: If both the product “CholeCap” and country “United States” are assigned to a document, do not apply the default rule, but instead apply the override rule.

The API returns both the system-managed object record `id` and the user-defined object record `name__v` (via the `object__v.name__v` lookup) field values which define the override conditions:

-   `"product__v.name__v": "CholeCap"` - The product object record name.
-   `"country__v.name__v": "United States"` - The country object record name.
-   `"product__v": "0PR0011001"` - The product object record ID.
-   `"country__v": "0CR0022002"` - The country object record ID.

**Override Rule**

When both the product “CholeCap” and country “United States” are assigned (at any time) to a document in this lifecycle, the following (alternate) users and groups are automatically assigned to the `editor__c` role:

-   `allowed_default_users__v` - The user `etta@veepharm.com` is automatically assigned to the role.
-   `allowed_users__v` - The users `finn@veepharm.com`, `greg@veepharm.com`, and `hope@veepharm.com` can be (optionally) assigned to the role during its lifecycle.
-   `allowed_default_groups__v` - The group `cholecap_us_docs_group__c` is automatically assigned to the role.
-   `allowed_groups__v` - The groups `cholecap_us_research_group__c`, `cholecap_us_compliance_group__c`, and `cholecap_us_product_management_group__c` can be (optionally) assigned to the role during its lifecycle.

Note: If the lifecycle role has not been configured with an override rule, the response will only display the default rule.

### Create Lifecycle Role Assignment Override Rules

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
--data-binary @"C:\Vault\Override Rules\create-lifecycle-role-override-rules.json" \
https://myvault.veevavault.com/api/v25.2/configuration/role_assignment_rule
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "responseStatus": "SUCCESS"
        }
    ]
}
'''

POST `/api/{version}/configuration/role_assignment_rule`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml` or `text/csv`

#### Body Parameters

Before submitting this request, prepare a JSON or CSV input file with the following information:

Name

Description

`name__v`required

The `name__v` field values of the lifecycle and role to which the override rule is being added.

`name__v`optional

The `name__v` field values of the allowed and default groups who will be assigned to the role when the override condition is met.

`id`optional

The `id` or `name__v` field values of the object records which define the override condition.

`user_name__v`optional

The `user_name__v` field values of the allowed and default users who will be assigned to the role when the override condition is met.

Note the following scope and limitations:

-   This request can only be used to specify the override rules (conditions, users, and groups). It cannot be used to create default rules.
-   The input may include override rules for multiple lifecycles and roles.
-   Each role may be configured with multiple override rules.

#### Example CSV & JSON Input Files

Create an override rule on the `editor__c` role of the `general_lifecycle__c` with the following override conditions, users, and groups:

`lifecycle__v`

`role__v`

`product__v.name__v`

`country__v.name__v`

`allowed_users__v`

`allowed_groups__v`

`allowed_default_users__v`

`allowed_default_groups__v`

`general_lifecycle__c`

`editor__c`

CholeCap

United States

“etta@veevapharm.com,finn@veevapharm.com,greg@veevapharm.com,hope@veevapharm.com”

“`cholecap_us_docs_group__c`,`cholecap_us_research_group__c`,`cholecap_us_compliance_group__c`,`cholecap_us_product_management_group__c`”

etta@veevapharm.com

`cholecap_us_docs_group__c`

'''
[
{
    "lifecycle__v": "general_lifecycle__c",
    "role__v": "editor__c",
    "product__v.name__v": "CholeCap",
    "country__v.name__v": "United States",
    "allowed_users__v": [
        "etta@veepharm.com",
        "finn@veepharm.com",
        "greg@veepharm.com",
        "hope@veepharm.com"
    ],
    "allowed_groups__v": [
        "cholecap_us_docs_group__c",
        "cholecap_us_research_group__c",
        "cholecap_us_compliance_group__c",
        "cholecap_us_product_management_group__c"
    ],
    "allowed_default_users__v": [
        "etta@veepharm.com"
    ],
    "allowed_default_groups__v": [
        "cholecap_us_docs_group__c"
    ]
}
]
'''

#### Request Details

In this example:

-   The input file format is set to JSON.
-   The response format is not set and will default to JSON.
-   The path/name of the JSON input file is specified.

#### Response Details

For each override rule specified in the input, the response includes a `SUCCESS` or `FAILURE` message.

### Update Lifecycle Role Assignment Rules (Default & Override)

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
--data-binary @"C:\Vault\Override Rules\update-lifecycle-role-override-rules.csv" \
https://myvault.veevavault.com/api/v25.2/configuration/role_assignment_rule
'''

Before submitting this request, prepare a JSON or CSV input file. See the [Create Lifecycle Role Assignment Override Rules](#Create_Override_Rules) request above for details.

PUT `/api/{version}/configuration/role_assignment_rule`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `application/xml` or `text/csv`

#### Response Details

For each default or override rule specified in the input, the response includes a `SUCCESS` or `FAILURE` message.

### Delete Lifecycle Role Assignment Override Rules

> Request: Delete All Overrides

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/configuration/role_assignment_rule?lifecycle__v=general_lifecycle__c&role__v=editor__c
'''

> Response: Delete All Overrides

'''
{
  "responseStatus": "SUCCESS",
  "data": {
    "rules_deleted": 2
  }
}
'''

> Request: Delete Object-Specific Override

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/configuration/role_assignment_rule?lifecycle__v=general_lifecycle__c&role__v=editor__c&product__v.name__v=CholeCap
'''

> Response: Delete Object-Specific Override

'''
{
  "responseStatus": "SUCCESS",
  "data": {
    "rules_deleted": 1
  }
}
'''

Delete override rules configured on a specific lifecycle role.

DELETE `/api/{version}/configuration/role_assignment_rule`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml` or `text/csv`

#### Query Parameters

Name

Description

`lifecycle__v`

Include the name of the lifecycle from which to delete override rules. For example, `lifecycle__v=general_lifecycle__c`.

`role__v`

Include the name of the role from which to delete override rules. For example, `role__v=editor__c`.

`{object_name}`

Optional: To delete overrides on a specific object by ID, include the object ID. For example, `product__v=0PR0011001`.

`{object_name}.name__v`

Optional: To delete overrides on a specific object by name, include the object name. For example, `product__v.name__v=CholeCap`.

#### Response Details

On `SUCCESS`, the example response displays the number of override rules that were deleted from the lifecycle role.

## Document Workflows

Document workflows enable users to send a collection of one or more documents for review and approval using a single workflow. The API allows you to retrieve, manage, and initiate document workflows.

Learn about [Document Workflows](https://platform.veevavault.help/en/lr/52053) in Vault Help.

### Retrieve All Document Workflows

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/actions
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": [
       {
           "name": "Objectworkflow.clinical_study_report_approval__c",
           "label": "Clinical Study Report Approval",
           "type": "multidocworkflow",
           "cardinality": "OneOrMany"
       },
       {
           "name": "Objectworkflow.medical_docs_review_and_approval__c",
           "label": "Medical Docs Review and Approval",
           "type": "multidocworkflow",
           "cardinality": "OneOrMany"
       }
   ]
}
'''

Retrieve all available document workflows that can be initiated on a set of documents which:

-   The authenticated user has permissions to view or initiate
-   Can be initiated through the API

GET `/api/{version}/objects/documents/actions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`loc`

When localized (translated) strings are available, retrieve them by setting `loc` to `true`.

#### Response Details

On `SUCCESS`, the response lists all available document workflows and includes the following:

Name

Description

`name`

The workflow name.

`label`

UI Label for the workflow.

`type`

Type of workflow.

`cardinality`

Indicates how many contents (`One`, `OneOrMany`) can be included in a workflow.

For users without the _Workflow: Start_ permission, the response returns an `INSUFFICIENT_ACCESS` error.

### Retrieve Document Workflow Details

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/documents/actions/Objectworkflow.clinical_study_report_approval__c
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "name": "Objectworkflow.clinical_study_report_approval__c",
       "controls": [
           {
               "type": "instructions",
               "instructions": "Add approvers",
               "prompts": [],
               "label": "Instructions"
           },
           {
               "type": "participant",
               "prompts": [
                   {
                       "label": "Approver",
                       "name": "approver__c"
                   }
               ],
               "required": true,
               "label": "Participants"
           },
           {
               "type": "participant",
               "prompts": [
                   {
                       "label": "Exec Approver",
                       "name": "exec_approver__c"
                   }
               ],
               "required": true,
               "label": "Participants"
           },
           {
               "prompts": [
                   {
                       "label": "Documents",
                       "name": "documents__sys"
                   }
               ],
               "label": "Documents",
               "type": "documents"
           },
           {
               "prompts": [
                   {
                       "multi_value": false,
                       "label": "Description",
                       "name": "description__sys"
                   }
               ],
               "label": "Description",
               "type": "description"
           }
       ],
       "label": "Clinical Study Report Approval",
       "type": "multidocworkflow",
       "cardinality": "OneOrMany"
   }
}
'''

Retrieves the details for a specific document workflow.

GET `/api/{version}/objects/documents/actions/{workflow_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`workflow_name`

The document workflow `name` value.

#### Query Parameters

Name

Description

`loc`

When localized (translated) strings are available, retrieve them by setting `loc` to `true`.

#### Response Details

On `SUCCESS`, the response lists the fields that must be configured with values in order to initiate the document workflow. These are based on the controls configured in the workflow start step.

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

For each control, the following data may be returned:

Name

Description

`label`

UI Label for the control.

`type`

Type of control (`instructions`, `participant`, `date`, `documents`, `description`, or `variable`).

Additionally, the response includes following fields describing the workflow:

Name

Description

`name`

The workflow name.

`label`

UI Label for the workflow.

`type`

Type of workflow (`multidocworkflow`).

`cardinality`

Indicates how many contents (`One`, `OneOrMany`) can be included in a workflow.

### Initiate Document Workflow

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
-d "contents__sys: Document:501,Document:502" \
-d "description__sys: Content Approval" \
https://myvault.veevavault.com/api/v25.2/objects/documents/actions/Objectworkflow.content_document_workflow__c
'''

> Response: Success

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "record_url": "/api/v25.2/vobjects/envelope__sys/0ER000000000501",
        "record_id__v": "0ER000000000501",
        "workflow_id": "1301"
    }
}
'''

> Response: Failure

'''
{
    "responseStatus": "FAILURE",
    "errors": [
      {
      "type": "INVALID_DATA",
      "message": "Invalid value [501,502] for parameter [contents__sys] specified"
    }
  ]
}
'''

Initiate a document workflow on a set of documents.

POST `/api/{version}/objects/documents/actions/{workflow_name}`

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

`{workflow_name}`

The document workflow `name` value.

#### Body Parameters

The following parameters are required, but an Admin may set other fields as required in your Vault. To find which fields are required to start this workflow, [Retrieve Document Workflow Details](#Retrieve_Multi_Document_Workflow_Details).

Name

Description

`contents__sys`required

Input a comma-separated list of document `id` field values, in the format `Document:{doc_id}`. For example, `Document:101,Document:102,Document:103`. To indicate specific document versions, use the format `DocumentVersion:{doc_version_id}`. For example, `DocumentVersion:115_0_1,DocumentVersion:116_0_2`. Maximum 100 documents.

`description__sys`required

Description of the workflow. Maximum 128 characters.

##### Add Participants

To add participants to a workflow, add the name of the participant control to the body of the request. The value should be a comma-separated list of user and group IDs in the format `{user_or_group}:{id}`. For example, `approvers__c: user:123,group:234`. Use [Retrieve Document Workflow Details](#Retrieve_Multi_Document_Workflow_Details) to get the names of all participant controls for the workflow.

#### Response Details

If any document is not in the relevant state or does not meet configured field conditions, the API returns `INVALID_DATA` for the invalid documents and the workflow does not start.

On `SUCCESS`, the response includes the following:

Name

Description

`record_id__v`

The `id` value of the `envelope__sys` record.

`workflow_id`

The workflow `id` field value.

#### Manage Document Workflow Tasks

Document workflows share some of the same capabilities as object workflows and are configured on the `envelope__sys` object. You can use the [Workflow Task](#Workflow_Tasks) endpoints to retrieve document workflow tasks, task details, and initiate document workflow tasks.

#### Remove Documents from Envelope

You can remove one or more documents from an `envelope__sys` object using the `removecontent` action in the [Initiate Workflow Action](#Initiate_Workflow_Action) endpoint.
