<!-- 
VaultAPIDocs Section: # Users
Original Line Number: 27795
Generated: August 30, 2025
Part 12 of 38
-->

# Users

Learn about [Creating & Managing Users](https://platform.veevavault.help/en/lr/953) and [Managing Users Across Vaults](https://platform.veevavault.help/en/lr/15127) in Vault Help.

To update Vault Membership for multiple Vaults within the same domain, create cross-domain users, or add users to a domain without assigning Vault membership, use the [Create Users](#Create_User) endpoint.

Learn about [Managing the User & Person Objects](https://platform.veevavault.help/en/lr/46534) in Vault Help.

## Retrieve User Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/users
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "properties": [
    {
      "name": "user_name__v",
      "type": "String",
      "length": 255,
      "editable": true,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "user_first_name__v",
      "type": "String",
      "length": 100,
      "editable": true,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "user_last_name__v",
      "type": "String",
      "length": 100,
      "editable": true,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "alias__v",
      "type": "String",
      "length": 40,
      "editable": true,
      "queryable": false,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "user_email__v",
      "type": "String",
      "length": 255,
      "editable": true,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "user_timezone__v",
      "type": "String",
      "length": 255,
      "editable": true,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": true,
      "values": [
        {
          "value": "Pacific/Niue",
          "label": "(GMT-11:00) Niue Time (Pacific/Niue)"
        },
        {
          "value": "Pacific/Pago_Pago",
          "label": "(GMT-11:00) Samoa Standard Time (Pacific/Pago_Pago)"
        },
      ]
    },
    {
      "name": "user_locale__v",
      "type": "String",
      "length": 10,
      "editable": true,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": true,
      "values": [
        {
          "value": "pt_BR",
          "label": "Brazil"
        },
        {
          "value": "es_ES",
          "label": "Spain"
        },
      ]
    },
    {
      "name": "user_title__v",
      "type": "String",
      "length": 255,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "office_phone__v",
      "type": "String",
      "length": 20,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "fax__v",
      "type": "String",
      "length": 255,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "mobile_phone__v",
      "type": "String",
      "length": 20,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "site__v",
      "type": "String",
      "length": 255,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "is_domain_admin__v",
      "type": "Boolean",
      "length": 1,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "active__v",
      "type": "Boolean",
      "length": 1,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "domain_active__v",
      "type": "Boolean",
      "length": 1,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": false
    },
    {
      "name": "security_policy_id__v",
      "type": "ObjectReference",
      "length": 20,
      "object": "securitypolicies",
      "editable": true,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "user_needs_to_change_password__v",
      "type": "Boolean",
      "length": 1,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "id",
      "type": "id",
      "length": 20,
      "object": "users",
      "editable": false,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": false
    },
    {
      "name": "created_date__v",
      "type": "Calendar",
      "length": 0,
      "editable": false,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": false
    },
    {
      "name": "created_by__v",
      "type": "ObjectReference",
      "length": 20,
      "object": "users",
      "editable": false,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": false
    },
    {
      "name": "modified_date__v",
      "type": "Calendar",
      "length": 0,
      "editable": false,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": false
    },
    {
      "name": "modified_by__v",
      "type": "ObjectReference",
      "length": 20,
      "object": "users",
      "editable": false,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": false
    },
    {
      "name": "domain_id__v",
      "type": "ObjectReference",
      "length": 20,
      "object": "domains",
      "editable": false,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": false
    },
    {
      "name": "vault_id__v",
      "type": "ObjectReference",
      "length": 20,
      "object": "vaults",
      "editable": false,
      "queryable": true,
      "required": true,
      "multivalue": true,
      "onCreateEditable": false
    },
    {
      "name": "federated_id__v",
      "type": "String",
      "length": 100,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "salesforce_user_name__v",
      "type": "String",
      "length": 255,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "last_login__v",
      "type": "Calendar",
      "length": 0,
      "editable": false,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": false
    },
    {
      "name": "medidata_uuid__v",
      "type": "String",
      "length": 255,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "user_language__v",
      "type": "String",
      "length": 10,
      "editable": true,
      "queryable": true,
      "required": true,
      "multivalue": false,
      "onCreateEditable": true,
      "values": [
        {
          "value": "en",
          "label": "English"
        },
        {
          "value": "ja",
          "label": "Japanese"
        },
      ]
    },
    {
      "name": "company__v",
      "type": "String",
      "length": 255,
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    },
    {
      "name": "group_id__v",
      "type": "ObjectReference",
      "length": 20,
      "object": "groups",
      "editable": false,
      "queryable": false,
      "required": false,
      "multivalue": true,
      "onCreateEditable": false
    },
    {
      "name": "security_profile__v",
      "type": "ObjectReference",
      "length": 40,
      "object": "Securityprofile",
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true,
      "values": [
        {
          "value": "business_admin__v",
          "label": "Business Administrator"
        },
        {
          "value": "document_user__v",
          "label": "Document User"
        },
        {
          "value": "external_user__v",
          "label": "External User"
        },
        {
          "value": "read_only_user__v",
          "label": "Read-Only User"
        },
        {
          "value": "system_admin__v",
          "label": "System Administrator"
        },
        {
          "value": "vault_owner__v",
          "label": "Vault Owner"
        },
        {
          "value": "view_based_user__v",
          "label": "View-Based User"
        }
      ]
    },
    {
      "name": "license_type__v",
      "type": "Picklist",
      "length": 40,
      "picklist": "license_type__v",
      "editable": true,
      "queryable": true,
      "required": false,
      "multivalue": false,
      "onCreateEditable": true
    }
  ]
}
'''

GET `/api/{version}/metadata/objects/users`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

This response includes a full list of fields for users. Some field `values` are abridged to shorten this example response.

## Retrieve All Users

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/users
'''

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/users?vaults=all
'''

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/users?vaults=-1
'''

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/users?vaults=3003,4004,5005
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "size": 200,
    "start": 0,
    "limit": 200,
    "sort": "id asc",
    "users": [
        {
            "user": {
                "id": 25501,
                "user_name__v": "ewoodhouse@veepharm.com",
                "user_first_name__v": "Elaine",
                "user_last_name__v": "Woodhouse"
              }
        },
        {
            "user": {
                "id": 25502,
                "user_name__v": "bashton@veepharm.com",
                "user_first_name__v": "Bruce",
                "user_last_name__v": "Ashton"
              }
        },
        {
            "user": {
                "id": 25503,
                "user_name__v": "tchung@veepharm.com",
                "user_first_name__v": "Thomas",
                "user_last_name__v": "Chung"
              }
        }
      ]
    }
'''

GET `/api/{version}/objects/users`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Using the endpoint alone with no optional parameters will retrieve users assigned only to the Vault in which the request is made. For customers with multiple Vaults in their domain, users with Domain Admin, System Admin, and Vault Owner privileges can access user information across different Vaults in the domain by including the optional parameter `vaults` set to one of the following values:

Name

Description

`vaults=all`

Retrieve all users assigned to all Vaults in your domain.

`vaults=-1`

Retrieve all users assigned to all Vaults in your domain except for the Vault in which the request is made.

`vaults={Vault IDs}`

To retrieve users assigned only to specific Vaults, enter a comma-separated list of Vault IDs. For example, `3003,4004,5005`.

`exclude_vault_membership`

Optional: Set to `false` to include `vault_membership` fields. If `true` or omitted, `vault_membership` fields are not included in the response.

`exclude_app_licensing`

Optional: Set to `false` to include `app_licensing` fields. If `true` or omitted, `app_licensing` fields are not included in the response.

System Admins and Vault Owners must have administrative access to Vault applications referenced in the `vaults` parameter to be able to access users from those Vault.

The response also supports pagination. By default the page limit is set to 200 records. The pagination parameters are:

Name

Description

`limit`

\[optional, default is 200\] the size of the result set in the page

`start`

\[optional, default is 0\] the starting record number

`sort`

\[optional, default is “id asc”\] the sort order for the result set (`asc` - ascending, `desc` - descending) (e.g. `user_name__v asc`)

#### Vault-Owned Users

When you retrieve legacy users, the response includes multiple system-owned user records that appear in all Vaults. These accounts are used to capture actions that are performed by Vault instead of by a user. These records are not included in license counts, are read-only, and cannot be referenced by another user or document. Learn more in [Vault Help](https://platform.veevavault.help/en/lr/953#System_Owned_Users).

## Retrieve User

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/users/1006546
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "users": [
       {
           "user": {
               "user_name__v": "olive@veepharm.com",
               "user_first_name__v": "Olivia",
               "user_last_name__v": "Cattington",
               "user_email__v": "olivia.cattington@veepharm.com",
               "user_timezone__v": "America/Los_Angeles",
               "user_locale__v": "en_US",
               "user_title__v": "Senior Vice President for Research & Development",
               "is_domain_admin__v": false,
               "active__v": true,
               "domain_active__v": true,
               "security_policy_id__v": 1000181,
               "user_needs_to_change_password__v": false,
               "id": 1006546,
               "created_date__v": "2022-05-23T20:49:06.000Z",
               "created_by__v": 1003079,
               "modified_date__v": "2022-06-16T17:22:49.000Z",
               "modified_by__v": 1,
               "domain_id__v": 1000076,
               "domain_name__v": "veepharm.com",
               "vault_id__v": [
                   1000660,
                   1000659
               ],
               "last_login__v": "2022-05-23T21:01:13.000Z",
               "user_language__v": "en",
               "company__v": "Veepharm",
               "group_id__v": [
                   1,
                   1394917493302,
                   6
               ],
               "security_profile__v": "vault_owner__v",
               "license_type__v": "full__v"
           }
       }
   ]
}
'''

Retrieve information for one user. To get information for all users, see [Retrieve All Users](#Retrieve_All_Users).

GET `/api/{version}/objects/users/{id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{id}`

The user `id` field value. To get information for the currently authenticated user, see [Validate Session User](#Validate_Session).

#### Query Parameters

Name

Description

`exclude_vault_membership`

Optional: Set to `false` to include `vault_membership` fields. Including these fields may decrease performance. If omitted, `vault_membership` fields are not included in the response.

`exclude_app_licensing`

Optional: Set to `false` to include `app_licensing` fields. Including these fields may decrease performance. If omitted, `app_licensing` fields are not included in the response.

## Create Users

Create new user accounts or add existing users as cross-domain users. Learn more about [cross-domain users](https://platform.veevavault.help/en/lr/38996) in Vault Help. Note that users only receive welcome emails if they are assigned to a Vault. For example, a new domain user who does not have any assigned Vaults will not receive a welcome email.

**Suppressing Welcome Emails**: When creating new users, you can prevent Vault from sending welcome emails to a user by setting the `user_needs_to_change_password__v` setting to `false`. This does not work for users with SSO security profiles, but you can work around this limitation by creating the users with a basic security profile and updating them to the SSO security profile with an update action.

### Create Single User

> Request: Add User to Domain

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "user_name__v=ewoodhouse@veepharm.com" \
-F "user_email__v=ewoodhouse@veepharm.com" \
-F "user_first_name__v=Elaine" \
-F "user_last_name__v=Woodhouse" \
-F "user_language__v=en" \
-F "user_timezone__v=America/Denver" \
-F "user_locale__v=en_US" \
-F "security_policy_id__v=821" \
-F "domain=true" \
https://myvault.veevavault.com/api/v25.2/objects/users
'''

> Request: Add User to Current Vault

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "user_name__v=ewoodhouse@veepharm.com" \
-F "user_email__v=ewoodhouse@veepharm.com" \
-F "user_first_name__v=Elaine" \
-F "user_last_name__v=Woodhouse" \
-F "user_language__v=en" \
-F "user_timezone__v=America/Denver" \
-F "user_locale__v=en_US" \
-F "security_policy_id__v=821" \
-F "security_profile__v=business_admin__v" \
-F "license_type__v=full__v" \
-F "file=@C:\Documents\Pictures\profile_image.jpg"
https://myvault.veevavault.com/api/v25.2/objects/users
'''

> Request Details: Add Cross-Domain User

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "user_name__v=ewoodhouse@veepharm.com" \
-F "security_profile__v=business_admin__v" \
-F "license_type__v=full__v" \
https://myvault.veevavault.com/api/v25.2/objects/users
'''

Create one user at a time without the need for a CSV input file or upload profile pictures to [file staging](/docs/#FTP). After creation, you can assign these users to Vaults with the [Update Vault Membership](#Update_Vault_Membership) endpoint.

Some Vaults use multiple applications, for example, a RIM Vault with Submissions and Registrations. If your Vault utilizes user-based licensing, you must use the [Create Multiple Users](#Bulk_Users_API) endpoint with the `app_licensing` field. After creation, you can also manually adjust the user’s application licenses through the Vault UI. Learn more about [license types](https://platform.veevavault.help/en/lr/5721#license-types) and [application licenses in Vault Help](https://platform.veevavault.help/en/lr/5721#application-licensing).

POST `/api/{version}/objects/users`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data` or `application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

The following table provides the required and most common optional parameters to create a user. You may add values to any other editable user field, unless you are adding a [cross-domain](#Create_Single_Cross_Domain_User) user or [VeevaID](#Create_Single_VeevaID_User) user. See [Retrieve Users](#Retrieve_All_Users) for all possible values.

Name

Description

`user_name__v`required

The user’s Vault username (login credential). For example, `ewoodhouse@veepharm.com`

`user_first_name__v`required

The user’s first name.

`user_last_name__v`required

The user’s last name.

`user_email__v`required

The user’s email address.

`user_timezone__v`required

The user’s time zone. Retrieve values from [Retrieve Users](#Retrieve_All_Users).

`user_locale__v`required

The user’s location. Retrieve values from [Retrieve Users](#Retrieve_All_Users).

`security_policy_id__v`required

The user’s security policy. Retrieve values from [Retrieve All Security Policies](#Retrieve_All_Security_Policies).

`user_language__v`required

The user’s preferred language. Retrieve values from [Retrieve Users](#Retrieve_All_Users).

`security_profile__v`optional

The user’s security profile. If omitted, the default value is `document_user__v`.

`license_type__v`optional

The license type is the first level of access control that Vault applies to a user. If your Vault utilizes user-based licensing, assign application licensing using the [Create Multiple Users](#Bulk_Users_API) endpoint. The `license_type__v` cannot be less permissive than a user’s application licensing. If omitted, the default value is `full__v`.

`file`optional

The file path to upload a profile picture. Must be JPG, PNG, or GIF, and less than 10MB in size. Vault automatically resizes images to 64 x 64 pixels and removes the animations in GIFs. Note that when you upload or change a user’s profile image, the change applies across the entire domain and will be visible in all Vaults where the user has membership.

##### Cross-Domain Users

The following are the only fields required to create a cross-domain user. All other fields are ignored.

Name

Description

`user_name__v`required

The user’s Vault username (login credential). For example, `ewoodhouse@veepharm.com`

`security_profile__v`optional

The user’s security profile. If omitted, the default value is `document_user__v`.

`license_type__v`optional

The user’s license type. If omitted, the default value is `full__v`. If your Vault utilizes user-based licensing, assign application licensing using the [Create Multiple Users](#Bulk_Users_API) endpoint.

##### VeevaID Users

The following are the only fields required to add an existing VeevaID user to Vault. All other fields are ignored.

Name

Description

`user_name__v`required

The user’s Vault username (login credential). For example, `ewoodhouse@veepharm.com`

`security_policy_id__v`required

The `name__v` of your Vault’s VeevaID security policy, for example, `25285`. You can retrieve this ID from the [Retrieve All Security Policies](#Retrieve_All_Security_Policies) endpoint.

`security_profile__v`optional

The user’s security profile. If omitted, the default value is `document_user__v`.

`license_type__v`optional

The user’s license type. If omitted, the default value is `full__v`. If your Vault utilizes user-based licensing, assign application licensing using the [Create Multiple Users](#Bulk_Users_API) endpoint.

#### Query Parameters

Name

Description

`domain`

When set to `true`, the user will not be assigned to a Vault.

#### Request Details: Add User to Domain

On `SUCCESS`, the user account is created and set to active. The new user is not assigned a license type or security profile, nor do they have access to any Vaults in your domain. This means they will not receive a welcome email.

#### Request Details: Add User to Current Vault

This request adds one new user to your domain and assigns them to the Vault where the request was made. They will receive a welcome email with instructions for logging into the Vault, and they will not have access to any other Vaults in your domain. To give them access to other Vaults, see [Update Vault Membership](#Update_Vault_Membership).

This example request includes all fields required to create a new user, and two optional fields (security profile and license type). If these optional fields were not included in the request, the user would be assigned the `document_user__v` security profile and `full__v` license type by default.

#### Request Details: Add Cross-Domain User

This request adds the user `ewoodhouse.veevavault.com` to your current domain as a cross-domain user.

All other metadata fields are ignored. Learn more about [cross-domain users in Vault Help](https://platform.veevavault.help/en/lr/38996).

### Create Multiple Users

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Users\create_users.csv" \
https://myvault.veevavault.com/api/v25.2/objects/users
'''

> Response

'''
{
   "responseStatus":"SUCCESS",
   "data":[
      {
         "responseStatus":"SUCCESS",
         "id":"12021"
      },
      {
         "responseStatus":"SUCCESS",
         "id":"12022"
      },
      {
         "responseStatus":"SUCCESS",
         "id":"12023"
      },
      {
         "responseStatus":"FAILURE",
         "errors":[
            {
               "type":"INVALID_DATA",
               "message":"Error message describing why this user was not created."
            }
         ]
      }
   ]
}
'''

Create new users and assign them to Vaults in bulk. You can also add multiple existing users as cross-domain users or VeevaID users.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the standard RFC 4180 format, with some [exceptions](/docs/#CSV_RFC_Deviations).
-   The maximum batch size is 500.
-   If you want to add profile pictures, you must upload these to [file staging](/docs/#FTP).

POST `/api/{version}/objects/users`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `text/csv`

#### Body Parameters

Prepare a JSON or CSV input file. You may add values to any other editable user field, unless you are adding a [cross-domain](#Add_Multiple_Cross_Domain_Users) user or [VeevaID](#Add_Multiple_VeevaID_Users) user. See [Retrieve Users](#Retrieve_All_Users) for all possible values. Using only the required fields will add users to your domain but will not assign them to individual Vaults within your domain. To assign users to individual Vaults, you must also use the required [Vault Membership](#Vault_Membership) parameters.

Name

Description

`user_name__v`required

The user’s Vault username (login credential). For example, `ewoodhouse@veepharm.com`

`user_first_name__v`required

The user’s first name.

`user_last_name__v`required

The user’s last name.

`user_email__v`required

The user’s email address.

`user_timezone__v`required

The user’s time zone. Retrieve values from [Retrieve Users](#Retrieve_All_Users).

`user_locale__v`required

The user’s location. Retrieve values from [Retrieve Users](#Retrieve_All_Users).

`security_policy_id__v`required

The user’s security policy. Retrieve values from [Retrieve All Security Policies](#Retrieve_All_Security_Policies).

`user_language__v`required

The user’s preferred language. Retrieve values from [Retrieve Users](#Retrieve_All_Users).

`file`optional

The file path of a profile picture from file staging. Must be JPG, PNG, or GIF, and less than 10MB in size. Vault automatically resizes images to 64 x 64 pixels and removes the animations from GIFs. Note that when you upload or change a user’s profile image, the change applies across the entire domain and will be visible in all Vaults where user has membership.

`domain`optional

If you set this to `true`, the user will not be assigned to a Vault.

`security_profile__v`optional

The user’s security profile. If omitted, the default value is `document_user__v`.

`license_type__v`optional

The license type is the first level of access control that Vault applies to a user. If your Vault utilizes user-based licensing, assign application licensing using the `app_licensing` field.

`vault_membership`optional

Use this field to assign a user to individual Vaults within your domain. This is required to create cross-domain users or VeevaID users. Learn how to configure this parameter in the [Vault Membership](#Vault_Membership) section.

`app_licensing`optional

Use this field to assign a user to individual applications within your Vault. Learn how to configure this parameter in the [Application Licensing](#Create_Multiple_Application_Licensing) section.

##### Vault Membership

To assign user permissions across Vaults, create cross-domain users,or create VeevaID users, you must include the `vault_membership` column configured with the following fields:

Name

Description

`vault_id`required

The Vault ID to assign the user to.

`active__v`optional

Set the user to active (`true`) or inactive (`false`). If not specified, default value is `true`.

`security_profile__v`optional

Set the user’s security profile, for example, `read_only_user__v`. If not specified, this value defaults to `document_user__v`.

`license_type__v`optional

Set the user’s license type, for example, `read_only__v`. If not specified, this value defaults to `full__v`.

For example, to add an active user to Vault ID 3003 with the `system_admin__v` security profile and the `full__v` license type:

`vault_membership`

`3003`:`true`:`system_admin__v`:`full__v`

##### Application Licensing

To add a user to specific applications within a Vault or across Vaults, you must include the `app_licensing` column configured with the following fields:

Name

Description

`vault_id`required

The Vault ID to assign the user to.

`active__v`optional

Set the user to active (`true`) or inactive (`false`). If not specified, default value is `true`.

`application_name`required

The application to add the user to. For example, use `rimReg_v` to assign a user to the RIM Registrations application.

`license_type__v`optional

Set the user’s license type for a specific application, for example, `read_only__v`. You must select a license value for at least one application. Possible values are:

-   `full__v`
-   `external__v`
-   `learner_user__v`
-   `read_only__v`

Some license values may be invalid depending on the application. The `license_type__v` for an application cannot be more permissive than the user’s Vault-wide license type. If omitted, the default value is `full__v`. The request fails if you provide an invalid `license_type__v` value for a specific application. Learn more about [valid license values by application in Vault Help](https://platform.veevavault.help/en/lr/5721#application-license).

The format for adding these fields is:

`{vault_id}|{application_name}{:active__v}{:license_type__v}`

To add a user to more than one application, separate the applications with a pipe. To add a user to applications in multiple Vaults, separate the Vaults with a semicolon. For example:

`app_licensing`

`3003`|`rimReg_v:true:full__v`|`rimSubs_v:true:full__v;4112`|`rimSubs_v:true:full__v`

This adds an active user to both RIM Registrations and RIM Submissions in Vault ID 3003, and to the RIM Submissions application in Vault ID 4112, all with the `full__v` license type.

##### Add Cross-Domain Users

The following are the only fields required to add cross-domain users. All other fields are ignored. Learn more about cross-domain users in [Vault Help](https://platform.veevavault.help/en/lr/38996).

Name

Description

`user_name__v`required

The user’s Vault username (login credential). For example, `ewoodhouse@veepharm.com`.

`vault_membership`required

Assign this user permissions across domains. Learn how to configure this parameter in the [Vault Membership](#Vault_Membership) section.

##### Add VeevaID Users

The following are the only fields required to add an existing VeevaID user to Vault. All other fields are ignored.

Name

Description

`user_name__v`required

The user’s Vault username (login credential). For example, `ewoodhouse@veepharm.com`.

`vault_membership`required

Assign this user permissions across domains. Learn how to configure this parameter in the [Vault Membership](#Vault_Membership) section.

`security_policy_id__v`required

The `name__v` value of your Vault’s VeevaID security profile, for example, `25285`. You can retrieve this ID from the [Retrieve All Security Policies](#Retrieve_All_Security_Policies) endpoint.

#### Query Parameters: Upsert Users

Upsert is a combination of create and update. Use one input file to create new users and update existing users at the same time. If a matching user record is found in your Vault, it is updated with the field values specified in the input. If no matching user record is found, a new user is created using values in the input.

Name

Description

`operation`

To upsert users, you must include `operation=upsert`

`idParam`

To upsert users, you must include either `idParam=id` or `idParam=user_name__v` to the request endpoint.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-create-users-sample-csv-input.csv)

#### Response Details:

On `SUCCESS`, Vault responds will list the `id` of each user. The order results are displayed in the response is the same as the order of records in the input.

## Update Users

Update information for a user.

System Admins and Vault Owners can update users in the Vaults where they have administrative access. System Admins who are also Domain Admins have an unrestricted access to users across all Vaults in the domain.

Note that some user fields are not available to update through the API. For example, you cannot update user profile pictures through the API. To find out which fields are available to update, you can [Retrieve User Metadata](#Retrieve_User_Metadata) and find all fields marked as `"editable": true`. If a field is missing from this response, it is not editable.

### Update Single User

> Request: Update User Profile Information

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "user_timezone__v=America/Los Angeles" \
-d "company__v=VeevaPharm" \
-d "user_title__v=Product Manager" \
-d "alias__v=Skipper" \
https://myvault.veevavault.com/api/v25.2/objects/users/25001
'''

> Request: Disable User at Domain-Level

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "domain_active__v=false" \
https://myvault.veevavault.com/api/v25.2/objects/users/25001
'''

> Request: Re-Enable User at Domain-Level

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "domain_active__v=false" \
https://myvault.veevavault.com/api/v25.2/objects/users/25001
'''

> Request: Promote a User to Domain Admin

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "is_domain_admin__v=true" \
https://myvault.veevavault.com/api/v25.2/objects/users/25001
'''

> Request: Update User Application Licensing

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "app_licensing=25001|qualityQms_v:true:full__v" \
https://myvault.veevavault.com/api/v25.2/objects/users/25001
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": 25001
}
'''

Update information for a single user. To update information for multiple users, see [Retrieve All Users](#Retrieve_All_Users).

PUT `/api/{version}/objects/users/{id}`

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

`{id}`

The user `id` field value. Use the value `me` to update information for the currently authenticated user.

#### Body Parameters

In the body of the request, add any editable fields you wish to update. To remove existing field values, include the field name and set its value to null.

#### Example Request: Disable User at Domain-Level

Only Domain Admins may use this request.

When updating a user, domain\_active\_\_v can be (optionally) included in the input and set to either true or false to enable or disable the user at the domain-level. Disabling a user at the domain-level will disable the user in every Vault in your domain. Re-enabling a user enables them in the domain but does not re-activate them in their Vaults. After re-enabling a user, you must update their Vault membership to make them active in the individual Vaults.

This request will set the user (ID: 25001) profile to inactive in all Vaults in your domain. The user will still be a member in the Vaults and retain their license types and security profiles, but their user profile will be inactive and they will no longer have access to any Vaults in your domain.

#### Example Request: Re-Enable User at Domain-Level

Only Domain Admins may use this request.

This request will set the (previously inactive) user (ID: 25001) profile to active in your Vault domain. However, they will still be inactive in and unable to access your domain Vaults. Use the Update Vault Membership request below to set their status to active in the individual Vaults in your domain.

#### Example Request: Promote a User to Domain Admin

Only Domain Admins may use this request.

This request will promote a user to Domain Admin. To remove a user from the Domain Admin role, set the `is_domain_admin__v` field to false. Each domain must have at least one user in the Domain Admin role.

#### Example Request: Update User Application Licensing

This request updates a user’s licensing values for a specific application. As of 24R2, Vault enforces valid license values by application. When updating a user’s application licensing values, Vault corrects any invalid application license values based on the user’s initial `license_type__v`. For example, if a user’s initial license type is `full__v` and their application license value for Veeva QMS is `read_only__v`, Vault updates the QMS application license value to `full__v`. If the user’s initial license type is `read_only__v` and their license value for Veeva QMS is `read_only__v`, Vault clears the QMS license value because `read_only__v` is not a valid license value for QMS.

Some license values may be invalid depending on the application. The request fails if you provide an invalid license value for a specific application. Learn more about [valid license values by application in Vault Help](https://platform.veevavault.help/en/lr/5721#application-license).

### Update My User

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "user_title__v=Technical Writer" \
-d "site__v": "San Francisco",
https://myvault.veevavault.com/api/v25.2/objects/users/me
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": 61579
}
'''

Update information for the currently authenticated user.

PUT `/api/{version}/objects/users/me`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

In the body of the request, add any editable fields you wish to update. To remove existing field values, include the field name and set its value to null.

#### Response Details

On `SUCCESS`, the specified values are updated and the request returns the `id` of the currently authenticated user.

### Update Multiple Users

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: text/csv" \
-H "Accept: text/csv" \
--data-binary @"C:\Vault\Users\update_users.csv" \
https://myvault.veevavault.com/api/v25.2/objects/users
'''

> Response

'''
{
   "responseStatus":"SUCCESS",
   "data":[
      {
         "responseStatus":"SUCCESS",
         "id":"12021"
      },
      {
         "responseStatus":"SUCCESS",
         "id":"12022"
      },
      {
         "responseStatus":"SUCCESS",
         "id":"12023"
      },
      {
         "responseStatus":"FAILURE",
         "id":"22124",
         "errors":[
            {
               "type":"INVALID_DATA",
               "message":"Error message describing why this user was not updated."
            }
         ]
      }
   ]
}
'''

Update information for multiple users at once.

-   The maximum input file size is 1GB.
-   The values in the input must be UTF-8 encoded.
-   CSVs must follow the [standard format](https://datatracker.ietf.org/doc/html/rfc4180).
-   The maximum batch size is 500.

PUT `/api/{version}/objects/users`

#### Headers

Name

Description

`Content-Type`

`application/json` or `text/csv`

`Accept`

`application/json` (default) or `text/csv`

#### Body Parameters

Prepare a JSON or CSV input file. You can include any editable user field and value in the input. Note this endpoint does not support the `security_profile` attribute for updating profiles.

Name

Description

`id`required

The ID of the user to update.

`vault_membership`optional

See [Vault Membership](#Vault_Membership) for how to configure.

[![Download Input File](../../images/download-csv-orange.svg)](/docs/sample-files/vault-update-users-sample-csv-input.csv)

## Disable User

> Request: Disable User in a Vault

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/users/25001
'''

> Request: Disable User in All Domain Vaults

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/users/25001?domain=true
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "id": 25001
}
'''

Disable a user in a specific Vault or disable a user in all Vaults in the domain.

#### Permissions

System Admins and Vault Owners can update users in the Vaults where they have administrative access. System Admins who are also Domain Admins have an unrestricted access to users across all Vaults in the domain.

DELETE `/api/{version}/objects/users/{user_id}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{user_id}`

The user `id` field value. See [Retrieve All Users](#Retrieve_All_Users) above.

#### Query Parameters

Name

Description

`domain`

When `true`, this disables the user account in all Vaults in the domain.

#### Request: Disable User in a Vault

This request will set the user (ID: 25001) profile to inactive in the Vault in which the request is made. The user will still be a member in the Vault and retain their license type and security profile, but their user profile will be inactive and they will no longer have access to the Vault.

#### Request: Disable User in All Domain Vaults

This request will set the user (ID: 25001) profile to inactive in all Vaults in your domain. The user will still be a member in the Vaults and retain their license types and security profiles, but their user profile will be inactive and they will no longer have access to any Vaults in your domain.

## Change My Password

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "password__v=CurrentPassword" \
-d "new_password__v=NewPassword" \
https://myvault.veevavault.com/api/v25.2/objects/users/me/password
'''

> Response

'''
{
    "responseStatus": "SUCCESS"
}
'''

Change the password for the currently authenticated user.

POST `/api/{version}/objects/users/me/password`

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

`password__v`required

Enter your current password.

`new_password__v`required

Enter your desired new password. Must be a different value than `password__v`.

Passwords must meet minimum requirements, which are configured by your Vault Admin. Learn about [Configuring Password Requirements](https://platform.veevavault.help/en/lr/1985) in Vault Help.

#### Response Details

On `SUCCESS`, your password is changed.

## Update Vault Membership

> Request: Add User to a Vault

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "active__v=true" \
https://myvault.veevavault.com/api/v25.2/objects/users/25001/vault_membership/3003
'''

> Request: Disable User in a Vault

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "active__v=false" \
https://myvault.veevavault.com/api/v25.2/objects/users/25001/vault_membership/3003
'''

> Request: Set Security Profile & License Type

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "security_profile__v=business_admin__v" \
-d "license_type__v=full__v"
https://myvault.veevavault.com/api/v25.2/objects/users/25001/vault_membership/3003
'''

Use this request to:

-   Assign an existing user to a Vault in your domain.
-   Remove (disable) an existing user from a Vault in your domain.
-   Update the security profile and license type of an existing user.

You cannot use this request to:

-   Create a new user. See [Create Object Records](#Create_User_Object_Record).
-   Update other user profile information. See [Update Object Records](#Update_Object_Record).

Additional information:

-   For a list of user fields and properties, see [Retrieve Users](#Retrieve_All_Users).
-   Learn about [Creating & Managing Users](https://platform.veevavault.help/en/lr/953) and [Managing Users Across Vaults](https://platform.veevavault.help/en/lr/15127) in Vault Help.

#### Permissions

System Admins and Vault Owners can update users in the Vaults where they have administrative access. System Admins who are also Domain Admins have an unrestricted access to users across all Vaults in the domain.

PUT `/api/{version}/objects/users/{user_id}/vault_membership/{vault_id}`

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

`{user_id}`

The user `id` field value. See [Retrieve All Users](#Retrieve_All_Users) above.

`{vault_id}`

The system-managed `id` field value assigned to each Vault in the domain.

#### Body Parameters

Name

Description

`active__v`optional

Set the user status to active (`true`) or inactive (`false`). If omitted, this value defaults to `active__v`.

`security_profile__v`optional

Assigns the user a specific security profile in the Vault. If omitted, defaults to `document_user__v`.

`license_type__v`optional

Assigns the user a specific license type in the Vault. If omitted, defaults to `full__v`.

See the example requests below for additional information about using these input values.

#### Request Details: Add User to a Vault

This request will assign the user (ID: 25001) to the Vault (ID: 3003). There are a few default settings that will be applied here:

The user’s status will be set to active in the Vault. This is the default setting; the `active__v=true` parameter ca be omitted and produce the same results. We’ve not included the optional `security_profile__v` and `license_type__v` in the input. Therefore, the user will be assigned a `full__v` license type and `document_user__v` security profile by default.

#### Request Details: Disable User in a Vault

This request will set the user (ID: 25001) profile to inactive in the Vault (ID: 3003). They will still be a member in the Vault and retain their license type and security profile, but their user profile will be inactive and they will no longer have access to the Vault.

#### Request Details: Set Security Profile & License Type

This request will set the user (ID: 25001) security profile and license type to specific values in the Vault (ID: 3003). If the user is already a member of the Vault, this will change their security profile and license type. If the user is not a member of the Vault, this will assign them to the Vault, set their status to active, and their security profile and license type to the specified values.

## Retrieve Application License Usage

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/licenses
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "doc_count": {
        "licensed": 4000,
        "used": 2380
    },
    "applications": [
        {
            "application_name": "pm_promomats__v",
            "user_licensing": {
                "full__v": {
                    "licensed": 500,
                    "used": 491,
                    "shared": false
                },
                "external__v": {
                    "licensed": 100,
                    "used": 67,
                    "shared": false
                },
                "read_only__v": {
                    "licensed": 100,
                    "used": 28,
                    "shared": false
                }
            }
        },
        {
            "application_name": "pm_multichannel__v",
            "user_licensing": {
                "full__v": {
                    "licensed": 500,
                    "used": 441,
                    "shared": false
                },
                "external__v": {
                    "licensed": 0,
                    "used": 0,
                    "shared": false
                },
                "read_only__v": {
                    "licensed": 0,
                    "used": 0,
                    "shared": false
                }
            }
        }
    ]
}
'''

Retrieve your current license usage compared to the licenses that your organization has purchased. This information is similar to the information displayed in the Vault UI from **Admin > Settings > General Settings**.

Some Vaults use multiple applications, for example, a RIM Vault with Submissions and Registrations. In these Vaults, users have a license value for each application they can access. Application licensing allows Vault to track available licenses at the application level, but does not control a user’s access in most Vaults. A user assigned to multiple applications will use one (1) application license per application. Learn more about [Application Licenses in Vault Help](https://platform.veevavault.help/en/lr/5721/#application-licensing).

GET `/api/{version}/objects/licenses`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

The response contains the following application license details:

Name

Description

`doc_count`

PromoMats and Veeva Medical only: The number of document views across all users with view-based license type against a pre-purchased set of views for the Vault. Learn more about [view-based user licenses in Vault Help](https://platform.veevavault.help/en/lr/5721).

`application_name`

The API name of this application license, for example, `pm_promomats__v`.

`user_licensing`

An array of the available application licenses for the given `application_name`.

`user_licensing.licensed`

The maximum number of users who can be assigned to this application license. For example, if the `full__v` application license has a `licensed` value of `50`, you can assign this license to a maximum of 50 users.

`user_licensing.used`

The number of users currently assigned to this application license. To determine the number of application licenses available for assignment, subtract `used` from `licensed`. For example, if your application license has a `licensed` value of `50` and a `used` value of `40`, you can assign 10 more users to this application license.

`user_licensing.shared`

Indicates if this user license is shared.

## Retrieve User Permissions

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/users/61579/permissions?filter=name__v::object.product__v.object_actions
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "data": [
    {
      "name__v": "object.product__v.object_actions",
      "permissions": {
        "read": true,
        "edit": true,
        "create": false,
        "delete": false
      }
    }
  ]
}
'''

Retrieve all object and object field permissions (_Read_, _Edit_, _Create_, _Delete_) assigned to a specific user.

GET `/api/{version}/objects/users/{id}/permissions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{id}`

The ID of the user. Use the value `me` to retrieve information for the currently authenticated user.

#### Query Parameters

Name

Description

`filter=name__v::{permission_name}`

Filter the results to show only one `specific name__v`, which is in the format `object.{object name}.{object` or `field}_actions`. Wildcards are not supported.

## Retrieve My User Permissions

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/users/me/permissions?filter=name__v::object.user__sys.object_actions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "name__v": "object.user__sys.object_actions",
            "permissions": {
                "read": true,
                "edit": true,
                "create": true,
                "delete": false
            }
        }
    ]
}
'''

Retrieve all object and object field permissions (_Read_, _Edit_, _Create_, _Delete_) assigned to the currently authenticated user.

GET `/api/{version}/objects/users/me/permissions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`filter=name__v::{permission_name}`

Filter the results to show only one `specific name__v`, which is in the format `object.{object name}.{object` or `field}_actions`. Wildcards are not supported.

## Validate Session User

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/users/me
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "users": [
       {
           "user": {
               "user_name__v": "tibanez@veepharm.com",
               "user_first_name__v": "Teresa",
               "user_last_name__v": "Ibanez",
               "user_email__v": "teresa.ibanez@veepharm.com",
               "user_timezone__v": "America/Denver",
               "user_locale__v": "en_US",
               "is_domain_admin__v": true,
               "active__v": true,
               "security_policy_id__v": 1863,
               "id": 61603,
               "created_date__v": "2018-01-09T23:07:48.000Z",
               "created_by__v": 1,
               "modified_date__v": "2024-11-13T00:17:17.000Z",
               "modified_by__v": 1,
               "domain_id__v": 3826,
               "last_login__v": "2024-12-11T00:24:12.000Z",
               "user_language__v": "en",
               "group_id__v": [
                   1392631750202,
                   1392631750402,
                   1392631748902
               ],
               "security_profile__v": "vault_owner__v",
               "license_type__v": "full__v"
           }
       }
   ]
}
'''

Given a valid session ID, this request returns information for the currently authenticated user. If the session ID is not valid, this request returns an `INVALID_SESSION_ID` error `type`. This is similar to a [`whoami` request](https://en.wikipedia.org/wiki/Whoami).

GET `/api/{version}/objects/users/me`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Query Parameters

Name

Description

`exclude_vault_membership`optional

Set to `false` to include `vault_membership` fields. If omitted, defaults to `true` and `vault_membership` fields are not included in the response. As a best practice to increase performance, please use the default setting and do not set this parameter to `false` unless you need these fields.

`exclude_app_licensing`optional

Set to `false` to include `app_licensing` fields. If omitted, defaults to `true` and `app_licensing` fields are not included in the response. As a best practice to increase performance, please use the default setting and do not set this parameter to `false` unless you need these fields.

#### Response Details

On `SUCCESS`, this request returns information for the currently authenticated user. If the session ID is not valid, this request returns an `INVALID_SESSION_ID` error `type`.

When interpreting the response, understand that the following fields are based on the Vault user, rather than the domain user:

-   `created_date__v`
-   `created_by__v`
-   `modified_date__v`
-   `modified_by__v`
-   `last_login__v`

##### Delegated Sessions

If the currently authenticated user is in a [delegated session](#Delegated_Access), this request returns a `delegate_user_id`. For example, if Sophia initiated a delegated session on behalf of Megan, this API call would display Megan’s id and Sophia’s `delegate_user_id`.
