<!-- 
VaultAPIDocs Section: # Groups
Original Line Number: 30934
Generated: August 30, 2025
Part 14 of 38
-->

# Groups

Groups are key to managing user access in Vault. A group is simply a named list of users. By defining groups which reflect the teams and roles in your company, and then assigning those groups to document roles, you can manage document access more easily and efficiently. In Vaults using Dynamic Access Control (DAC) for documents, Vault also automatically creates groups that correspond to one lifecycle role and additional document field criteria. These are called Auto Managed Groups.

Learn about [Groups](https://platform.veevavault.help/en/lr/37744) in Vault Help.

## Retrieve Group Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/groups
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "properties": [
    {
      "name": "id",
      "type": "id",
      "length": 20,
      "editable": false,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": false
    },
    {
      "name": "label__v",
      "type": "String",
      "length": 255,
      "editable": true,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "allow_delegation_among_members__v",
      "type": "Boolean",
      "length": 1,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
     },
    {
      "name": "group_description__v",
      "type": "String",
      "length": 200,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    }
  ]
}
'''

GET `/api/{version}/metadata/objects/groups`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

## Retrieve All Groups

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/groups
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "groups": [
    {
      "group": {
        "members__v": [
          25496,
          25513,
          25514,
          25515,
          25519,
          25524,
          25525,
          25526,
          25527,
          25528,
          25532
        ],
        "active__v": true,
        "security_profiles__v": [
          "document_user__v",
          "business_admin__v",
          "system_admin__v",
          "vault_owner__v"
        ],
        "name__v": "all_internal_users__v",
        "modified_by__v": 25524,
        "editable__v": true,
        "allow_delegation_among_members__v": true,
        "modified_date__v": "2016-03-08T21:13:49.000Z",
        "group_description__v": "All Internal Vault Users (System Provided Group)",
        "system_group__v": true,
        "label__v": "All Internal Users",
        "created_date__v": "2014-02-17T10:09:03.000Z",
        "type__v": "System Provided Group",
        "id": 1,
        "created_by__v": 1
      }
    }
  ]
}
'''

Retrieve all groups except Auto Managed groups. You can retrieve Auto Managed groups using the [Retrieve Auto Managed Groups](#Retrieve_Auto_Managed_Groups) endpoint.

GET `/api/{version}/objects/groups`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`includeImplied`

Optional: When `true`, the response includes the `implied_members__v` field. These users are automatically added to the group when their `security_profiles__v` are added to the group. If omitted, the response includes only the `members__v` field. These users are individually added to a group by an Admin.

## Retrieve Auto Managed Groups

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/groups/auto
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "group": {
                "members__v": [],
                "active__v": true,
                "security_profiles__v": [],
                "name__v": "msg1394917493801__c",
                "modified_by__v": 1,
                "editable__v": false,
                "allow_delegation_among_members__v": false,
                "modified_date__v": "2019-06-25T19:17:01.000Z",
                "group_description__v": "Periodic Review-Consumer (Auto Managed Group)",
                "system_group__v": false,
                "label__v": "Periodic Review-Consumer",
                "created_date__v": "2019-06-25T19:02:18.000Z",
                "type__v": "Auto Managed Group",
                "id": 1394917493801,
                "created_by__v": 1
            }
        },
        {
            "group": {
                "members__v": [
                    1003079
                ],
                "active__v": true,
                "security_profiles__v": [],
                "name__v": "msg1394917494202__c",
                "modified_by__v": 1003079,
                "editable__v": false,
                "allow_delegation_among_members__v": false,
                "modified_date__v": "2021-10-04T20:43:30.000Z",
                "group_description__v": "Periodic Review-Editor (Auto Managed Group)",
                "system_group__v": false,
                "label__v": "Periodic Review-Editor",
                "created_date__v": "2021-10-04T20:43:30.000Z",
                "type__v": "Auto Managed Group",
                "id": 1394917494202,
                "created_by__v": 1003079
            }
        },
        {
            "group": {
                "members__v": [
                    1003079
                ],
                "active__v": true,
                "security_profiles__v": [],
                "name__v": "msg1394917494201__c",
                "modified_by__v": 1003079,
                "editable__v": false,
                "allow_delegation_among_members__v": false,
                "modified_date__v": "2021-10-04T20:42:35.000Z",
                "group_description__v": "Periodic Review-Viewer (Auto Managed Group)",
                "system_group__v": false,
                "label__v": "Periodic Review-Technical Writer",
                "created_date__v": "2021-10-04T20:42:36.000Z",
                "type__v": "Auto Managed Group",
                "id": 1394917494201,
                "created_by__v": 1003079
            }
        }
    ],
    "responseDetails": {
        "offset": 0,
        "limit": 1000,
        "size": 3,
        "total": 3
    }
}
'''

Retrieve all Auto Managed groups. Learn more about [Auto Managed groups](https://platform.veevavault.help/en/lr/3200#auto-managed) in Vault Help.

GET `/api/{version}/objects/groups/auto`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`limit`

Paginate the results by specifying the maximum number of records per page in the response. This can be any value between `1` and `1000`. If omitted, defaults to `1000`.

`offset`

Paginate the results displayed per page by specifying the amount of offset from the entry returned. For example, if you are viewing the first 50 results (page 1) and want to see the next page, set this to `offset=51`. If omitted, defaults to `0`.

## Retrieve Group

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/groups/1435176677013
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "groups": [
    {
      "group": {
        "members__v": [
          25518,
          25519,
          25520
        ],
        "active__v": true,
        "security_profiles__v": [],
        "name__v": "cholecap_editors_group__c",
        "modified_by__v": 46916,
        "editable__v": true,
        "allow_delegation_among_members__v": true,
        "modified_date__v": "2015-06-24T20:11:17.000Z",
        "group_description__v": null,
        "system_group__v": false,
        "label__v": "Cholecap Editors Group",
        "created_date__v": "2015-06-24T20:11:17.000Z",
        "type__v": "User Managed Group",
        "id": 1435176677013,
        "created_by__v": 46916
      }
    }
  ]
}
'''

GET `/api/{version}/objects/groups/{group_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{group_id}`

The group `id` field value.

#### Query Parameters

Name

Description

`includeImplied`

When `true`, the response includes the `implied_members__v` field. These users are automatically added to the group when their `security_profiles__v` are added to the group. When not used, the response includes only the `members__v` field. These users are individually added to a group by Admin.

## Create Group

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "label__v=Cholecap Team US Compliance" \
-d "members__v=45501,45002" \
-d "security_profiles__v=document_user__v"
https://myvault.veevavault.com/api/v25.2/objects/groups
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Group successfully created.",
  "id": 1358979070034
}
'''

POST `/api/{version}/objects/groups`

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

`label__v`required

Enter a group label. Vault uses this to create the group `name__v` value.

`members__v`optional

Add a comma-separated list of user IDs. This manually assigns individual users to the group.

`security_profiles__v`optional

Add a comma-separated list of security profiles. This automatically adds all users with the security profile to the group. These are `implied_members__v`.

`active__v`optional

By default, the new group will be created as active. To set the group to inactive, set this value to `false`

`group_description__v`optional

Add a description of the group.

`allow_delegation_among_members__v`optional

When set to `true`, members of this group will only be allowed to delegate access to other members of the same group. You can set this field for user and system managed groups. If omitted, defaults to `false`. Learn more about [Delegate Access](https://platform.veevavault.help/en/lr/15015).

## Update Group

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "label__v=Cholecap Team" \
-d "members__v=45501,45502,45503,45004" \
https://myvault.veevavault.com/api/v25.2/objects/groups/1358979070034
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Group successfully updated.",
  "id": 1358979070034
}
'''

Update editable group field values. Add or remove group members and security profiles.

PUT `/api/{version}/objects/groups/{group_id}`

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

`{group_id}`

The group `id` field value.

#### Body Parameters

In the body of the request, add any editable fields you wish to update.

Name

Description

`label__v`optional

Updates the label of the group.

`members__v`optional

Add a comma-separated list of user IDs. This manually assigns individual users to the group.

`security_profiles__v`optional

Add a comma-separated list of security profiles.

`active__v`optional

To set the group to inactive, set this value to `false`.

`group_description__v`optional

Updates the description of the group.

`allow_delegation_among_members__v`optional

When set to `true`, members of this group will only be allowed to delegate access to other members of the same group. You can set this field for user and system managed groups. If omitted, defaults to `false`. Learn more about [Delegate Access](https://platform.veevavault.help/en/lr/15015).

#### Request Details

You may change the values of any editable group field. Changing the `security_profiles__v` will automatically replace all previous implied users assigned via the previous security profile.

#### Add or Remove Users

To add or remove group members, add a comma-separated list of user IDs in `members__v`. This replaces all previous users who were manually assigned. This action is not additive.

Alternatively, you can add or remove group members without replacing previous users in the following ways:

-   To add users, set the value of `members__v` to `add` followed by a comma-separated list of user IDs enclosed in parenthesis. For example `add (userID1, userID2)`. This only adds the specified users to the group.
    
-   To delete users, set the value of `members__v` to `delete` followed by a comma-separated list of user IDs enclosed in parenthesis. For example `delete (userID1, userID2)` This only removes the specified users from the group.
    

## Delete Group

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/groups/1358979070034
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": 1358979070034
}
'''

Delete a user-defined group. You cannot delete system-managed groups.

DELETE `/api/{version}/objects/groups/{group_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{group_id}`

The group `id` field value.
