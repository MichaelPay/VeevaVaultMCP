<!-- 
VaultAPIDocs Section: # Sandbox Vaults
Original Line Number: 34049
Generated: August 30, 2025
Part 20 of 38
-->

# Sandbox Vaults

Sandbox Vaults provide environments for testing, including development, UAT, and validation testing. Learn more about [sandbox Vaults in Vault Help](https://platform.veevavault.help/en/lr/48988).

## Retrieve Sandboxes

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/sandbox
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "entitlements": [
            {
                "size": "Small",
                "available": 3,
                "allowed": 4,
                "temporary": 0
            },
            {
                "size": "Large",
                "available": 2,
                "allowed": 2,
                "temporary": 0
            },
            {
                "size": "Full",
                "available": 0,
                "allowed": 1,
                "temporary": 0
            }
        ],
        "active": [
            {
                "pod": "DS0",
                "vault_id": 1001054,
                "name": "Testing Sandbox",
                "type": "config",
                "size": "Full",
                "status": "active",
                "domain": "veepharm.com",
                "dns": "myvault.veevavault.com",
                "source_vault_id": 1000660,
                "refresh_available": "2022-12-03T18:25:51.000Z",
                "created_date": "2022-12-02T18:25:51.000Z",
                "created_by": 1,
                "modified_date": "2023-11-01T01:44:40.000Z",
                "modified_by": 1,
                "entitlements": [],
                "release": "limited",
                "expiration_date": "NULL"
            },
            {
                "pod": "DS0",
                "vault_id": 1001074,
                "name": "VeePharm Sandbox",
                "type": "config",
                "size": "Small",
                "status": "active",
                "domain": "veepharm.com",
                "dns": "veepharm-veepharm-sandbox.vaultdev.com",
                "source_vault_id": 1000660,
                "refresh_available": "2022-12-09T16:56:15.000Z",
                "created_date": "2022-12-09T16:56:15.000Z",
                "created_by": 1,
                "modified_date": "2023-11-01T01:44:45.000Z",
                "modified_by": 1,
                "entitlements": [],
                "release": "limited",
                "expiration_date": "NULL"
            }
        ]
    }
}
'''

Retrieve information about the sandbox Vaults for the authenticated Vault.

GET `/api/{version}/objects/sandbox`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

The response contains information about the sandbox Vaults for the authenticated Vault.

Name

Description

`pod`

The name of the POD the sandbox is on.

`vault_id`

The sandbox ID number.

`name`

The name of the sandbox.

`type`

The type of sandbox, such as configuration (`config`).

`size`

The size of the sandbox: `Small`, `Medium`, `Large`, `Very Large`, `Extra Large`, or `Full`. Learn more about [sandbox sizes and their limits in Vault Help](https://platform.veevavault.help/en/lr/48988#sizes).

`status`

The current status of the sandbox:

-   `building`: A new or recently refreshed sandbox
-   `active`: Sandbox is accessible
-   `inactive`: Sandbox is not accessible
-   `deleting`: Sandbox is being deleted

`domain`

The sandbox domain.

`dns`

The sandbox domain name.

`source_vault_id`

The Vault ID of the sandbox’s parent Vault.

`refresh_available`

The date and time when this sandbox can be refreshed. You can refresh a sandbox once every 24 hours.

`release`

The type of release. This can be `general`, `limited`, or `prerelease`. Learn more about [Vault releases in Vault Help](https://platform.veevavault.help/en/lr/11796).

`entitlements`

The sandbox entitlements, including type, availability, and allowed information. The `temporary` entitlement shows only when a temporary entitlement is active.

`expiration_date`

The expiration date of the sandbox Vault. May be `NULL` if the sandbox never expires. Learn more about [sandbox expiration in Vault Help](https://platform.veevavault.help/en/lr/48988#sizes).

## Retrieve Sandbox Details by ID

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/sandbox/1001074
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "pod": "DS0",
        "vault_id": 1001074,
        "name": "VeePharm Sandbox",
        "type": "config",
        "size": "Small",
        "status": "active",
        "domain": "veepharm.com",
        "dns": "veepharm-veepharm-sandbox.vaultdev.com",
        "source_vault_id": 1000660,
        "refresh_available": "2022-12-09T16:56:15.000Z",
        "created_date": "2022-12-09T16:56:15.000Z",
        "created_by": 1,
        "modified_date": "2023-11-01T01:44:45.000Z",
        "modified_by": 1,
        "limits": [
            {
                "name": "total_object_records",
                "used": "43",
                "allowed": "100000"
            },
            {
                "name": "document_versions",
                "used": "1",
                "allowed": "10000"
            }
        ],
        "entitlements": [],
        "release": "limited",
        "expiration_date": "NULL"
    }
}
'''

Retrieve information about the sandbox for the given Vault ID.

GET `/api/{version}/objects/sandbox/{vault_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`vault_id`

The Vault ID of the sandbox.

#### Response Details

The response contains information about the sandbox Vaults for the authenticated Vault.

Name

Description

`pod`

The name of the POD the sandbox is on.

`vault_id`

The sandbox ID number.

`name`

The name of the sandbox.

`type`

The type of sandbox, such as configuration (`config`).

`size`

The size of the sandbox: `Small`, `Medium`, `Large`, `Very Large`, `Extra Large`, or `Full`. Learn more about [sandbox sizes and their limits in Vault Help](https://platform.veevavault.help/en/lr/48988#sizes).

`status`

The current status of the sandbox:

-   `building`: A new or recently refreshed sandbox
-   `active`: Sandbox is accessible
-   `inactive`: Sandbox is not accessible
-   `deleting`: Sandbox is being deleted

`domain`

The sandbox domain.

`dns`

The sandbox domain name.

`source_vault_id`

The Vault ID of the sandbox’s parent Vault.

`refresh_available`

The date and time when this sandbox can be refreshed. You can refresh a sandbox once every 24 hours.

`limits`

Sandbox limits, such as total\_object\_records. Note that sandbox usage is updated once every 24 hours, and new/recently refreshed sandboxes initially show 0 usage.

`entitlements`

The sandbox entitlements, including type, availability, and allowed information. The `temporary` entitlement shows only when a temporary entitlement is active.

`release`

The type of release. This can be `general`, `limited`, or `prerelease`. Learn more about [Vault releases in Vault Help](https://platform.veevavault.help/en/lr/11796).

`expiration_date`

The expiration date of the sandbox Vault. May be `NULL` if the sandbox never expires. Learn more about [sandbox expiration in Vault Help](https://platform.veevavault.help/en/lr/48988#sizes).

## Recheck Sandbox Usage Limit

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
https://myvault.veevavault.com/api/v25.2/objects/sandbox/actions/recheckusage
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Recalculate the usage values of the sandbox Vaults for the authenticated Vault. This action can be initiated up to 100 times in a 24-hour period. In the UI, this information is available in **Admin > Settings**. Learn more about [viewing usage details in Vault Help](https://platform.veevavault.help/en/lr/48988/#usage).

POST `/api/{version}/objects/sandbox/actions/recheckusage`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/x-www-form-urlencoded`

## Change Sandbox Size

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
-d "[
{
    “name”: “SandboxA”,
    “size”: “Full”
}
]” \
https://myvault.veevavault.com/api/v25.2/objects/sandbox/batch/changesize
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": null,
   "errorCodes": null,
   "errorType": null
}
'''

Change the size of a sandbox Vault for the authenticated Vault. You can initiate this action if there are sufficient allowances and the current sandbox meets the data and user limits of the requested size. Learn more about [sandbox sizes in Vault Help](https://platform.veevavault.help/en/lr/48988/#sizes).

POST `/api/{version}/objects/sandbox/batch/changesize`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/json`

#### Body Parameters

In the body of the request, include a raw JSON object with the following information:

Name

Description

`name`required

The name of the sandbox Vault.

`size`required

The requested size of the sandbox: `Small`, `Medium`, `Large`, `Very Large`, `Extra Large`, or `Full`. Learn more about [sandbox sizes and their limits in Vault Help](https://platform.veevavault.help/en/lr/48988#sizes).

#### Response Details

On `SUCCESS`, the response includes the `responseStatus` and lists any errors encountered.

## Set Sandbox Entitlements

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
'https://myvault.veevavault.com/api/v25.2/objects/sandbox/entitlements/set' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'name=VeePharm Sandbox' \
-d 'size=Small' \
-d 'allowance=1' \
-d 'grant=true'
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "entitlements": [
            {
                "size": "Small",
                "available": 2,
                "allowed": 4,
                "temporary": 0
            },
            {
                "size": "Large",
                "available": 2,
                "allowed": 2,
                "temporary": 0
            },
            {
                "size": "Full",
                "available": 0,
                "allowed": 1,
                "temporary": 0
            }
        ]
    }
}
'''

Set new sandbox entitlements, including granting and revoking allowances, for the given sandbox `name`.

POST `/api/{version}/objects/sandbox/entitlements/set`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/x-www-form-urlencoded`

#### Body Parameters

Name

Description

`name`required

The name of the sandbox Vault, which appears on the [My Vaults](https://platform.veevavault.help/en/lr/18505) page. Providing a new name creates a new sandbox, whereas providing an existing name refreshes the existing sandbox. How often you can refresh a Vault depends on its size. Learn more about [refreshing sandboxes in Vault Help](https://platform.veevavault.help/en/lr/48988/#refresh).

`size`required

The size of the sandbox: `Small`, `Medium`, `Large`, `Very Large`, `Extra Large`, or `Full`. Learn more about [sandbox sizes and their limits in Vault Help](https://platform.veevavault.help/en/lr/48988#sizes).

`allowance`required

The number of entitlements to grant or revoke.

`grant`required

Allowed values `true` and `false`. True grants allowances and false revokes them.

`temporary_allowance`optional

The number of temporary sandbox allowances to grant or revoke.

## Create or Refresh Sandbox

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "type=config" \
-d "size=Small" \
-d "domain=veepharm.com" \
-d "name=Sandbox" \
https://myvault.veevavault.com/api/v25.2/objects/sandbox
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "job_id": 70701,
    "url": "/api/v25.2/services/jobs/70701"
}
'''

Create a new sandbox for the currently authenticated Vault. Include the `source_snapshot` parameter in the request body to create a new sandbox from an existing [snapshot](#Sandbox_Snapshots).

Providing a name which already exists will refresh the existing sandbox Vault. You can also [refresh a sandbox from a snapshot](#Refresh_Sandbox_from_Snapshot).

POST `/api/{version}/objects/sandbox`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/x-www-form-urlencoded`

#### Body Parameters

Name

Description

`source`optional

The source to refresh the sandbox from:

-   `vault`
-   `snapshot`

`source_snapshot`optional

If the source is a `snapshot`, provide the `api_name` of the snapshot to create the sandbox from. You can obtain the `api_name` using the [Retrieve Sandbox Snapshots](#Retrieve_Snapshots) request.

`type`optional

The type of sandbox, such as `config`.

`size`required

The size of the sandbox: `Small`, `Medium`, `Large`, `Very Large`, `Extra Large`, or `Full`. Learn more about [sandbox sizes and their limits in Vault Help](https://platform.veevavault.help/en/lr/48988#sizes).

`domain`required

The domain to use for the new sandbox. Must be a valid domain. You can retrieve valid domains from the [Retrieve Domains](#Retrieve_Domains) endpoint. Only domains of `type: Sandbox` are allowed. Must be lower-case, and must include the domain extension.

`name`required

The name of the sandbox Vault, which appears on the _My Vaults_ page. Providing a new name creates a new sandbox, whereas providing an existing name refreshes the existing sandbox. How often you can refresh a Vault depends on its size. Learn more about [refreshing sandboxes in Vault Help](https://platform.veevavault.help/en/lr/48988/#refresh).

`add_requester`optional

This boolean field adds the currently authenticated user as a Vault Owner in the new sandbox. If set to `false,` the Domain Admin users in the sandbox domain will become Vault Owners in the sandbox Vault. If omitted, defaults to `true`.

`release`optional

The type of release. This can be `general`, `limited`, or `prerelease`. If omitted, defaults to the release level of the source Vault. Learn more about [Vault releases in Vault Help](https://platform.veevavault.help/en/lr/11796).

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`job_id`

The Job ID value to retrieve the status and results of the sandbox creation request.

`url`

URL to retrieve the current status of the sandbox creation request.

## Refresh Sandbox from Snapshot

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "source_snapshot=Sandbox1 Snapshot" \
https://myvault.veevavault.com/api/v25.2/objects/sandbox/1001055/actions/refresh
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "job_id": 165954,
    "url": "/api/v25.2/services/jobs/165954"
}
'''

Refresh a sandbox Vault in the currently authenticated Vault from an existing [snapshot](#Sandbox_Snapshots).

POST `/api/{version}/objects/sandbox/{vault_id}/actions/refresh`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/x-www-form-urlencoded`

#### URI Path Parameters

Name

Description

`vault_id`

The Vault ID of the sandbox to be refreshed.

#### Body Parameters

Name

Description

`source_snapshot`optional

Provide the `api_name` of the snapshot to refresh the sandbox from. You can obtain the `api_name` using the [Retrieve Sandbox Snapshots](#Retrieve_Snapshots) request.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`job_id`

The Job ID value to retrieve the status and results of the sandbox refresh request.

`url`

URL to retrieve the current status of the sandbox refresh request.

## Delete Sandbox

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/sandbox/My Configuration Sandbox
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Sandbox '[My Configuration Sandbox]' submitted for deletion, sandbox Vault id [24143] and parent Vault id [19523]"
}
'''

Delete a sandbox Vault. How often you can delete a Vault depends on its size. Learn more about [deleting sandboxes in Vault Help](https://platform.veevavault.help/en/lr/48988/#delete).

DELETE `/api/{version}/objects/sandbox/{name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`name`

The `name` of the sandbox Vault to delete. This is the name which appears on the _My Vaults_ page.

## Sandbox Snapshots

Snapshots allow your organization to store the configuration and data of sandbox Vaults at a given point in time. You can use snapshots to create and refresh sandbox Vaults. Learn more about [administering sandbox snapshots in Vault Help](https://platform.veevavault.help/en/lr/535936).

### Create Sandbox Snapshot

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "source_sandbox=Sandbox1" \
-d "name=Snapshot1" \
-d "description=First snapshot of a sandbox." \
-d "include_data=false" \
https://myvault.veevavault.com/api/v25.2/objects/sandbox/snapshot
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "job_id": 165944,
    "url": "/api/v25.2/services/jobs/165944"
}
'''

Create a new sandbox snapshot for the indicated sandbox Vault.

POST `/api/{version}/objects/sandbox/snapshot`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/x-www-form-urlencoded`

#### Body Parameters

Name

Description

`source_sandbox`required

The name of the sandbox Vault to take a snapshot of.

`name`required

The name of the new snapshot.

`description`optional

The description of the new snapshot.

`include_data`optional

Set to `true` to include data as part of the snapshot. Set to `false` to include only configuration.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`job_id`

The Job ID value to retrieve the status and results of the snapshot creation request.

`url`

URL to retrieve the current status of the snapshot creation request.

### Retrieve Sandbox Snapshots

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/sandbox/snapshot
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "available": 3,
       "snapshots": [
           {
               "name": "Sandbox A Snapshot",
               "api_name": "sandbox_a_snapshot__c",
               "type": "configuration",
               "description": "New snapshot of a sandbox.",
               "status": "active",
               "upgrade_status": "Good",
               "source_sandbox": "SandboxA",
               "total_object_records": 82,
               "document_versions": 0,
               "vault_version": "22R3.2",
               "update_available": "2022-12-03T00:04:59.000Z",
               "created_date": "2022-12-02T00:04:59.000Z",
               "expiration_date": "2023-04-25T05:00:00.000Z",
               "domain": "veepharm.com",
               "created_by": 1006595
           }
       ]
   }
}
'''

Retrieve information about sandbox snapshots managed by the authenticated Vault.

GET `/api/{version}/objects/sandbox/snapshot`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

The response contains information about the snapshots managed by the authenticated Vault.

Name

Description

`name`

The name of the snapshot.

`api_name`

The API name of the snapshot.

`type`

The type of the source sandbox, such as `configuration`.

`description`

The description of the snapshot.

`status`

The current status of the snapshot:

-   `building`: Snapshot is being created or updated
-   `active`: Snapshot is accessible for use
-   `maintenance`: Snapshot is being upgraded
-   `deleted`: Snapshot is expired

`upgrade_status`

The current upgrade status of the snapshot:

-   `Good`: No upgrade is required for the snapshot
-   `Upgrade Required`: An upgrade is required for the snapshot
-   `Upgrade Available`: An upgrade is available for the snapshot
-   `Expired`: Snapshot has expired

`source_sandbox`

The name of the sandbox Vault the snapshot was created from.

`total_object_records`

The total number of object records in the snapshot.

`document_versions`

The total number of document versions in the snapshot.

`vault_version`

The release version of the source sandbox Vault when the snapshot was created.

`update_available`

The date and time when the snapshot can next be updated. Learn more about [updating snapshots in Vault Help](https://platform.veevavault.help/en/lr/535936/#update).

`expiration_date`

The date and time when the snapshot will expire.

`domain`

The domain of the source sandbox Vault.

### Delete Sandbox Snapshot

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/sandbox/snapshot/sandbox_a_snapshot__c
'''

> Response

'''
{
   "responseStatus": "SUCCESS"
}
'''

Delete a sandbox snapshot managed by the authenticated Vault. Deleted snapshots cannot be recovered. Learn more about [deleting sandbox snapshots in Vault Help](https://platform.veevavault.help/en/lr/535936/#delete).

DELETE `/api/{version}/objects/sandbox/snapshot/{api_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`api_name`

The API name of the snapshot. Obtain this from the [Retrieve Sandbox Snapshots](#Retrieve_Snapshots) request.

#### Response Details

On `SUCCESS`, the response only includes the `responseStatus`.

### Update Sandbox Snapshot

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/sandbox/snapshot/veepharm_snapshot__c/actions/update
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "job_id": 165949,
   "url": "/api/v25.2/services/jobs/165949"
}
'''

Recreate a sandbox snapshot for the same source sandbox Vault. This request replaces the existing snapshot with the newly created one. Learn more about [updating snapshots in Vault Help](https://platform.veevavault.help/en/lr/535936/#update).

POST `/api/{version}/objects/sandbox/snapshot/{api_name}/actions/update`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`api_name`

The API name of the snapshot. Obtain this from the [Retrieve Sandbox Snapshots](#Retrieve_Snapshots) request.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`job_id`

The Job ID value to retrieve the status and results of the snapshot update request.

`url`

URL to retrieve the current status of the snapshot update request.

### Upgrade Sandbox Snapshot

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/sandbox/snapshot/veepharm_snapshot__c/actions/upgrade
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "job_id": 172303,
   "url": "/api/v25.2/services/jobs/172303"
}
'''

Upgrade a sandbox snapshot to match the release version of the source sandbox Vault.

Your request to upgrade a snapshot is only valid if the `upgrade_status=Upgrade Available` or `Upgrade Required`. Use the [Retrieve Sandbox Snapshots](#Retrieve_Snapshots) request to obtain the `upgrade_status` of a snapshot.

POST `/api/{version}/objects/sandbox/snapshot/{api_name}/actions/upgrade`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`api_name`

The API name of the snapshot. Obtain this from the [Retrieve Sandbox Snapshots](#Retrieve_Snapshots) request.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`job_id`

The Job ID value to retrieve the status and results of the snapshot upgrade request.

`url`

URL to retrieve the current status of the snapshot upgrade request.

## Pre-Production Vaults

Pre-production Vaults allow your organization to fully manage a Vault’s lifecycle from initial to go-live. When ready, Vault Admins can promote the pre-production Vault to a production Vault through the Admin UI or API. Learn more about [pre-production Vaults in Vault Help](https://platform.veevavault.help/en/lr/70199).

### Build Production Vault

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "source=UAT"
https://myvault.veevavault.com/api/v25.2/objects/sandbox/actions/buildproduction
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "job_id": 111507,
    "url": "/api/v25.2/services/jobs/111507"
}
'''

Given a pre-production Vault, build a production Vault. This is analogous to the _Build_ action in the Vault UI. After building your Vault, you can promote it to production.

You can build or rebuild the source Vault for a given pre-production Vault no more than three times in a 24 hour period.

POST `/api/{version}/objects/sandbox/actions/buildproduction`

#### Headers

Name

Description

`Accept`

`application/json` (default)

`Content-Type`

`application/x-www-form-urlencoded`

#### Body Parameters

Name

Description

`source`required

The name of the source Vault to build. This can be the current pre-production Vault or a sandbox Vault. Sandboxes must be `active` and match the release type (General or Limited) of the pre-production Vault.

### Promote to Production

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "name=VeePharm"
https://myvault.veevavault.com/api/v25.2/objects/sandbox/actions/promoteproduction
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Given a built pre-production Vault, promote it to a production Vault. This is analogous to the _Promote_ action in the Vault UI.

You must build your pre-production Vault before you can promote it to production.

POST `/api/{version}/objects/sandbox/actions/promoteproduction`

#### Headers

Name

Description

`Accept`

`application/json` (default)

`Content-Type`

`application/x-www-form-urlencoded`

#### Body Parameters

Name

Description

`name`required

The name of the pre-production Vault to promote.
