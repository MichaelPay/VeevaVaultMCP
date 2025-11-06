<!-- 
VaultAPIDocs Section: # Security Policies
Original Line Number: 32558
Generated: August 30, 2025
Part 17 of 38
-->

# Security Policies

Vault security policies allow you to create and manage password policies for users. These settings control password requirements, expiration period, reuse policy, security question policy, and delegated authentication via Salesforce.com™. Security policies apply across all Vaults in a multi-Vault domain.

Learn more about [security policies in Vault Help](https://platform.veevavault.help/en/lr/1985).

## Retrieve Security Policy Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/objects/securitypolicies
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseMessage": "Success",
   "metadata": {
       "name": "security_policy",
       "description": "Security Policy",
       "properties": [
           {
               "name": "policy_details__v",
               "type": [
                   "CompleteObject"
               ],
               "description": "Details",
               "objectTypeReferenced": [
                   {
                       "type": "policy_details"
                   }
               ]
           },
           {
               "name": "policy_security_settings__v",
               "type": [
                   "CompleteObject"
               ],
               "description": "Security Settings",
               "objectTypeReferenced": [
                   {
                       "type": "policy_security_settings"
                   }
               ]
           }
       ],
       "objects": [
           {
               "name": "policy_details",
               "description": "Details",
               "properties": [
                   {
                       "name": "name__v",
                       "type": [
                           "string"
                       ],
                       "description": "Public Key"
                   },
                   {
                       "name": "label__v",
                       "type": [
                           "string"
                       ],
                       "description": "Policy Name",
                       "required": true,
                       "maxValue": 60,
                       "minValue": 1,
                       "editable": true,
                       "onCreateEditable": true
                   }
               ]
           },
           {
               "name": "policy_security_settings",
               "description": "Security Policy",
               "properties": [
                   {
                       "name": "authentication_type__v",
                       "type": [
                           "SummaryObject"
                       ],
                       "description": "Authentication Type",
                       "required": true,
                       "editable": true,
                       "onCreateEditable": true
                   },
                   {
                       "name": "passwords_require_number__v",
                       "type": [
                           "boolean"
                       ],
                       "description": "Passwords require a number",
                       "required": true,
                       "editable": true,
                       "onCreateEditable": true
                   },
                   {
                       "name": "passwords_require_uppercase_letter__v",
                       "type": [
                           "boolean"
                       ],
                       "description": "Passwords require an upper-case letter",
                       "required": true,
                       "editable": true,
                       "onCreateEditable": true
                   }
               ]
           }
       ]
   }
}
'''

Retrieve the metadata associated with the security policy object.

GET `/api/{version}/metadata/objects/securitypolicies`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

## Retrieve All Security Policies

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/securitypolicies
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "security_policies__v": [
    {
      "name__v": "821",
      "label__v": "Basic",
      "value__v": "https://myvault.veevavault.com/api/v25.2/objects/securitypolicies/821"
    },
    {
      "name__v": "958",
      "label__v": "Default",
      "value__v": "https://myvault.veevavault.com/api/v25.2/objects/securitypolicies/958"
    },
    {
      "name__v": "957",
      "label__v": "High Security",
      "value__v": "https://myvault.veevavault.com/api/v25.2/objects/securitypolicies/957"
    },
    {
      "name__v": "1909",
      "label__v": "Single Sign-on Okta",
      "value__v": "https://myvault.veevavault.com/api/v25.2/objects/securitypolicies/1909"
    }
  ]
}
'''

GET `/api/{version}/objects/securitypolicies`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

The response lists all `security_policies__v` in the Vault:

Name

Description

`name__v`

System-managed value automatically assigned to security policies. This is typically a numeric value.

`label__v`

Security policy label displayed in Admin UI.

`value__v`

URL value to retrieve security policy metadata.

## Retrieve Security Policy

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/objects/securitypolicies/958
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "responseMessage": "Success",
  "security_policy__v": {
    "policy_details__v": {
      "name__v": "958",
      "label__v": "Default",
      "is_active__v": true
    },
    "policy_security_settings__v": {
      "authentication_type__v": {
        "name__v": "Password",
        "label__v": "Password"
      },
      "passwords_require_number__v": true,
      "passwords_require_uppercase_letter__v": true,
      "min_password_length__v": 8,
      "password_expiration__v": 0,
      "password_history_reuse__v": 0
    }
  }
}
'''

GET `/api/{version}/objects/securitypolicies/{security_policy_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{security_policy_name}`

Security policy name\_\_v field value (retrieved from previous request). This is typically a numeric value.

#### Response Details

Depending on the configuration, the response may include some or all of the following `security_policy__v` fields:

Name

Description

`policy_details__v`

Policy Details

`name__v`

Security Policy ID

`label__v`

Security Policy Label

`description__v`

Security Policy Description

`is_active__v`

Active (true/false)

`policy_security_settings__v`

Policy Security Settings

`authentication_type__v`

Authentication Type

`name__v`

Authentication Type Name

`label__v`

Authentication Type Label

`passwords_require_number__v`

Passwords Require Number (true/false)

`passwords_require_uppercase_letter__v`

Passwords Require Upper-Case Letter (true/false)

`passwords_require_nonalpha_char__v`

Passwords Require Non-Alphanumeric Character (true/false)

`min_password_length__v`

Minimum Password Length (7, 8, 10, or 12 characters)

`password_expiration__v`

Password Expiration (90 days, 180 days, or no expiration)

`password_history_reuse__v`

Password History Reuse (prevent reuse of the last 3 passwords, 5 passwords, or no limitations)

`require_question_on_password_reset__v`

Require Security Question on Password Reset (true/false)

`allow_delegated_auth_sfdc__v`

Allow Salesforce™ Delegated Authentication (true/false)

`sfdc_org_id__v`

Salesforce™ Org ID

Note: Boolean fields are only returned when the value is set to `true`.
