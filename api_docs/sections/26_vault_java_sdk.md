<!-- 
VaultAPIDocs Section: # Managing Vault Java SDK
Original Line Number: 39398
Generated: August 30, 2025
Part 26 of 38
-->

# Managing Vault Java SDK

After you’ve deployed Vault Java SDK code, you may need to perform actions on your code besides additional deployment with a VPK. For example, you may need to download source code or disable a single file.

You also may need to delete a single file rather than all files. However, we do not recommend using the following methods to deploy code as you may introduce or delete code which breaks existing deployed code. For best practices, use the [VPK Deploy method](/sdk/#Deploy).

## Retrieve Single Source Code File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://veepharm.veevavault.com/api/v25.2/code/com.veeva.vault.custom.actions.FindPartners
'''

> Response

'''
package com.veeva.vault.custom.actions;
import com.veeva.vault.sdk.api.core.*;
import com.veeva.vault.sdk.api.action.RecordAction;
import com.veeva.vault.sdk.api.action.RecordActionContext;
import com.veeva.vault.sdk.api.action.RecordActionInfo;
import com.veeva.vault.sdk.api.data.Record;
import com.veeva.vault.sdk.api.data.RecordService;
import java.util.List;

@RecordActionInfo(name="get_partners__c", label="Find Partners", object="company__c")
  public class FindPartners implements RecordAction {
    //[...]
  }
}
'''

Retrieve a single source code file from the currently authenticated Vault.

GET `/api/{version}/code/{class_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default)

#### URI Path Parameters

Name

Description

`class_name`

The fully qualified class name of your file.

## Enable Vault Extension

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
https://veepharm.veevavault.com/api/v25.2/code/com.veeva.vault.custom.actions.MyCustomAction/enable
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Enabled"
}
'''

Enable a deployed Vault extension in the currently authenticated Vault. Only available on entry-point classes, such as triggers and actions.

PUT `/api/{version}/code/{class_name}/enable`

#### Headers

Name

Description

`Accept`

`application/json` (default)

`Content-Type`

`multipart/form-data`

#### URI Path Parameters

Name

Description

`class_name`

The fully qualified class name of your file.

## Disable Vault Extension

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
https://veepharm.veevavault.com/api/v25.2/code/com.veeva.vault.custom.actions.MyCustomAction/disable
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Disabled"
}
'''

Disable a deployed Vault extension in the currently authenticated Vault. Only available on entry-point classes, such as triggers and actions.

PUT `/api/{version}/code/{class_name}/disable`

#### Headers

Name

Description

`Accept`

`application/json` (default)

`Content-Type`

`multipart/form-data`

#### URI Path Parameters

Name

Description

`class_name`

The fully qualified class name of your file.

## Add or Replace Single Source Code File

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
https://veepharm.veevavault.com/api/v25.2/code
-F "file=@C:\Vault\Extensions\com\veeva\vault\custom\actions\MyCustomAction.java" \
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Modified file",
    "url": "/api/v25.2/code/com.veeva.vault.custom.actions.MyCustomAction"
}
'''

Add or replace a single `.java` file in the currently authenticated Vault. If the given file does not already exist in the Vault, it is added. If the file already exists in the Vault, the file is updated.

PUT `/api/{version}/code`

#### Headers

Name

Description

`Accept`

`application/json` (default)

`Content-Type`

`multipart/form-data`

#### Body Parameters

Name

Description

`file`required

The `.java` file you wish to add. Maximum allowed size is 1MB.

## Delete Single Source Code File

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://veepharm.veevavault.com/api/v25.2/code/com.veeva.vault.custom.actions.MyCustomAction
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Deleted file"
}
'''

Delete a single source code file from the currently authenticated Vault. You cannot delete a code component currently in-use.

DELETE `/api/{version}/code`

#### Headers

Name

Description

`Accept`

`application/json` (default)

#### URI Path Parameters

Name

Description

`class_name`

The fully qualified class name of your file.

## Validate Imported Package

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://veepharm.veevavault.com/api/v25.2/services/vobject/vault_package__v/0PI000000000401/actions/validate
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseDetails": {
        "summary": "Configuration and components (document fields, lifecycles, and workflows) for Documentation Review and Approval process.",
        "author": "lgills@veepharm.com",
        "package_name": "PKG-0031",
        "package_id": "0PI000000000401",
        "source_vault": "13135",
        "package_status": "Error",
        "total_steps": 21,
        "start_time": "18:09:2018 06:31:11",
        "end_time": "18:09:2018 06:31:13",
        "package_error": "",
        "package_steps": [
            {
                "id": "0IS000000000401",
                "name__v": "00010",
                "step_type__v": "Component",
                "step_label__v": "Writer",
                "step_name__v": "writer__c",
                "type__v": "Picklist",
                "deployment_status__v": "Skipped",
                "deployment_action": "No Change (same as Vault)"
            },
            {
                "id": "0IS000000000404",
                "name__v": "00040",
                "step_type__v": "Component",
                "step_label__v": "Vault Help Content",
                "step_name__v": "help_documents__c",
                "type__v": "Doctype",
                "deployment_status__v": "Deployed with warnings",
                "deployment_action": "Update"
            },
            {
                "id": "0IS000000000420",
                "name__v": "00210",
                "step_type__v": "Component",
                "step_label__v": "documentation_review_and_approval__c.submit_for_annual_review__c",
                "step_name__v": "documentation_review_and_approval__c.submit_for_annual_review__c",
                "type__v": "Workflow",
                "deployment_status__v": "Verified",
                "deployment_action": "Add (missing in Vault)"
            }
        ]
    }
}
'''

Validate a previously imported VPK package with Vault Java SDK code. Note that this endpoint does not validate component dependencies for Configuration Migration packages.

POST `/api/{version}/services/vobject/vault_package__v/{package_id}/actions/validate`

#### Headers

Name

Description

`Accept`

`application/json` (default)

#### URI Path Parameters

Name

Description

`package_id`

The ID of the package to validate. You can find this in the API response of a package import, or in the URL of package in the Vault UI.

## Retrieve Signing Certificate

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/certificate/00001
'''

The following endpoint allows you to retrieve a signing certificate included in a Spark message header to verify that the received message came from Vault.

GET `/api/{version}/services/certificate/{cert_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{cert_id}`

The `cert_id` is provided in each Spark message in the `X-VaultAPISignature-CertificateId` header.

#### Response Details

On `SUCCESS`, the response includes the public key certificate (`.pem`) file used for [Message Verification](/sdk/#Message_Verification).

## Queues

Vault Spark is a message queue system that enables applications to send and receive messages to and from durable queues using a First-in, First-Out (FIFO) method.

The following endpoints allow you to manage queues for [Spark Messaging](/sdk/#Vault_Integrations) and SDK job queues.

The current user must have the relevant _Admin: Spark Queues_ or _Admin: SDK Job Queues_ to perform actions on each queue type. For example, if the API user does not have access to SDK job queues, **Retrieve All Queues** only returns available Spark messaging queues.

### Retrieve All Queues

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/queues
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "name": "new_study_queue__c",
            "status": "active",
            "type": "outbound",
            "url": "https://myvault.veevavault.com/api/v25.2/services/queues/new_study_queue__c"
        },
        {
            "name": "qms_change_queue__c",
            "status": "active",
            "type": "inbound",
            "url": "https://myvault.veevavault.com/api/v25.2/services/queues/qms_change_queue__c"
        }
    ]
}
'''

Retrieve all queues in a Vault.

GET `/api/{version}/services/queues`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

On `SUCCESS`, the response lists all available queues and their operational statuses.

### Retrieve Queue Status

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/queues/new_study_queue__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "name": "new_study_queue__c",
            "status": "active",
            "type": "outbound",
            "delivery": "enabled",
            "messages_in_queue": 365,
            "connections": [
              {
                "name": "aws_study_integration",
                "last_message_delivered": "error"
                "error" {
                    "message_id": "834798hof83998",
                    "date_time": "2012-04-25T21:49:27.719Z",
                    "message": "no response"
                }
              }
    ]
}
'''

Retrieve the status of a specific queue.

GET `/api/{version}/services/queues/{queue_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{queue_name}`

The name of a specific queue. For example, `queue__c.`

#### Response Details

On `SUCCESS`, the response includes the following:

Name

Description

`delivery`

Indicates whether the delivery status is `enabled` or `disabled`.

`messages_in_queue`

Displays the number of messages in the queue.

`last_message_delivered`

Indicates if the last message delivered was successful or encountered an error. If `ok`, the message was delivered successfully. If the message encounters an error, the response includes the `message_id`, `date_time`, and the `message` text.

### Disable Delivery

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/queues/new_study_queue__c/actions/disable_delivery
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

The following endpoint allows you to disable the delivery of messages in an outbound Spark messaging queue, or an SDK job queue. This stop messages from exiting the queue. For example, disabling delivery on an SDK job queue stops messages from being delivered to the processor.

This endpoint is not available for inbound Spark messaging queues. There is no way to stop received messages from processing in an inbound Spark queue.

PUT `/api/{version}/services/queues/{queue_name}/actions/disable_delivery`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{queue_name}`

The name of a specific Queue.

### Enable Delivery

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/queues/new_study_queue__c/actions/enable_delivery
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

The following endpoint allows you to enable the delivery of messages in an outbound Spark messaging queue, or an SDK job queue. This allows messages to exit the queue. For example, enabling delivery on an SDK job queue allows messages to be delivered to the processor.

PUT `/api/{version}/services/queues/{queue_name}/actions/enable_delivery`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{queue_name}`

The name of a specific Queue.

### Reset Queue

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/services/queues/new_study_queue__c/actions/reset
'''

> Response

'''
{
 "responseStatus": "SUCCESS",
 "responseMessage": "Deleted messages in queue."
}
'''

Delete all messages in a specific queue. This action is final and cannot be undone.

PUT `/api/{version}/services/queues/{queue_name}/actions/reset`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{queue_name}`

The name of a specific queue.
