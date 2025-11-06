<!-- 
VaultAPIDocs Section: # Authentication
Original Line Number: 11
Generated: August 30, 2025
Part 1 of 38
-->

# Authentication

Authenticate your account using one of the methods outlined below. The response returns a session ID that you can use in subsequent API calls. Session IDs time out after a period of inactivity, which varies by Vault. Learn more about [session duration and management](/docs/#Session_Mangement).

After acquiring a Vault Session ID, include it on every subsequent API call inside the `Authorization` HTTP request header.

#### Basic Authorization

Name

Description

`Authorization`

{`sessionId`}

Alternatively, you can use Salesforce™ or OAuth2/OIDC Delegated Requests. Retrieve Document Attachment Version Metadata Vault API also accepts Vault Session IDs as Bearer tokens. Include `Bearer` keyword to send Vault Session IDs with as bearer tokens:

#### Bearer Token Authorization

Name

Description

`Authorization`

Bearer {`sessionId`}

## User Name and Password

> Request

'''
curl -X POST https://myvault.veevavault.com/api/v25.2/auth \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Accept: application/json" \
-d "username={username}&password={password}"
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "sessionId": "3B3C45FD240E26F0C3DB4F82BBB0C15C7EFE4B29EF9916AF41AF7E44B170BAA01F232B462BE5C2BE2ACB82F6704FDA216EBDD69996EB23A6050723D1EFE6FA2B",
  "userId": 12021,
  "vaultIds": [
    {
      "id": 1776,
      "name": "PromoMats",
      "url": "https://promomats-veevapharm.veevavault.com/api"
    },
    {
      "id": 1777,
      "name": "eTMF",
      "url": "https://etmf-veevapharm.veevavault.com/api"
    },
    {
      "id": 1779,
      "name": "QualityDocs",
      "url": "https://qualitydocs-veevapharm.veevavault.com/api"
    }
  ],
  "vaultId": 1776
}
'''

Authenticate your account using your Vault user name and password to obtain a Vault Session ID.

If the specified user cannot successfully authenticate to the given `vaultDNS`, the subdomain is considered invalid and this request instead generates a session for the user’s [most relevant available Vault](/docs#Auth_Defaulting). A DNS is considered invalid for the given user if the user cannot access any Vaults in that subdomain, for example, if the user does not exist in that DNS or if all Vaults in that DNS are inactive. For this reason, it is best practice to inspect the response, compare the desired Vault ID with the list of returned Vault IDs, and confirm the DNS matches the expected login.

Vault limits the number of Authentication API calls based on the user name and the domain name used in the API call. To determine the Vault Authentication API burst limit for your Vault or the length of delay for a throttled response, check the [response headers](/docs/#Auth_API_Rate_Limit_Headers) or the [API Usage Logs](https://platform.veevavault.help/en/lr/14341#API_Usage_Logs).

POST `https://{vaultDNS}/api/{version}/auth`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data` or `application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`vaultDNS`

The DNS of the Vault for which you want to generate a session. If the requesting user cannot successfully authenticate to this `vaultDNS`, this request generates a session for the user’s [most relevant available Vault](/docs#Auth_Defaulting).

`version`

The Vault API version. Your authentication version does not need to match the version in subsequent calls. For example, you can authenticate with v17.3 and run your integrations with v20.1.

#### Body Parameters

Name

Description

`username`required

Your Vault user name assigned by your administrator.

`password`required

Your Vault password associated with your assigned Vault user name.

`vaultDNS`optional

The DNS of the Vault for which you want to generate a session. If specified, this optional `vaultDNS` body parameter overrides the value in the URI `vaultDNS`. If the requesting user cannot successfully authenticate to this `vaultDNS`, this request generates a session for the user’s [most relevant available Vault](/docs#Auth_Defaulting). If this `vaultDNS` body parameter is omitted, this request instead generates a session for the domain specified in the URI `vaultDNS`.

#### Response Details

On `SUCCESS`, this request returns a valid `sessionId` for any Vault DNS where the user has access.

The Vault DNS for the returned session is calculated in the following order:

1.  Generates a session for the DNS in the optional `vaultDNS` body parameter
    -   If this `vaultDNS` is invalid, generates a session for the user’s [most relevant available Vault](/docs#Auth_Defaulting):
        1.  Generates a session for the Vault where the user last logged in
        2.  If the user has never logged in, or if the last logged-in Vault is inactive, generates a session for the oldest active Vault where that user is a member
        3.  If the user is not a member of any active Vaults, the user cannot authenticate and the API returns `FAILURE`
2.  If the optional `vaultDNS` body parameter is omitted, generates a session for the DNS specified in the `vaultDNS` URI parameter
    -   If this `vaultDNS` is invalid, generates a session for the user’s [most relevant available Vault](/docs#Auth_Defaulting):
        1.  Generates a session for the Vault where the user last logged in
        2.  If the user has never logged in, or if the last logged-in Vault is inactive, generates a session for the oldest active Vault where that user is a member
        3.  If the user is not a member of any active Vaults, the user cannot authenticate and the API returns `FAILURE`

An invalid DNS is any DNS which the specified user cannot access, for example, if the DNS does not exist, if the user does not exist in that DNS, or if all Vaults in that DNS are inactive.

It is best practice to inspect the response, compare the desired Vault ID with the list of returned `vaultIds`, and confirm the DNS matches the expected login.

This API only returns `FAILURE` if it is unable to return a valid `sessionId` for any Vault the user can access.

### Review Results
- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `authenticate_with_username_password`
- **Updates Made:**
    - Corrected the `vaultDNS` parameter from `dns` to `vaultDNS`.
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

## OAuth 2.0 / OpenID Connect

> Request

'''
curl -X POST \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Authorization: Bearer 1C29326C3DF" \
-H "Host: Bearer 1C29326C3DF" \
https://myserver.com/auth/oauth/session/_9ad0a091-cbd6-4c59-ab5a-d4f2870f218c
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "sessionId": "3B3C45FD240E26F0C3DB4F82BBB0C15C7EFE4B29EF9916AF41AF7E44B170BAA01F232B462BE5C2BE2ACB82F6704FDA216EBDD69996EB23A6050723D1EFE6FA2B",
  "userId": 12021,
  "vaultIds": [
    {
      "id": 1776,
      "name": "PromoMats",
      "url": "https://promomats-veevapharm.veevavault.com/api"
    },
    {
      "id": 1777,
      "name": "eTMF",
      "url": "https://etmf-veevapharm.veevavault.com/api"
    },
    {
      "id": 1779,
      "name": "QualityDocs",
      "url": "https://qualitydocs-veevapharm.veevavault.com/api"
    }
  ],
  "vaultId": 1776
}
'''

Authenticate your account using OAuth 2.0 / Open ID Connect token to obtain a Vault Session ID. Learn more about [OAuth 2.0 / Open ID Connect in Vault Help](https://platform.veevavault.help/en/lr/43329).

When requesting a `sessionId`, Vault allows the ability for Oauth2/OIDC client applications to pass the `client_id` with the request. Vault uses this `client_id` when talking with the introspection endpoint at the authorization server to validate that the `access_token` presented by the application is valid. Learn more about [Client ID in the Vault API Documentation](/docs/#Client_ID).

POST `https://login.veevavault.com/auth/oauth/session/{oath_oidc_profile_id}`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

`Authorization`

Bearer {`access_token`}

`Accept`

application/json (default)

#### URI Path Parameters

Name

Description

`oath_oidc_profile_id`

The ID of your OAuth2.0 / Open ID Connect profile.

#### Body Parameters

Name

Description

`vaultDNS`optional

The DNS of the Vault for which you want to generate a session. If omitted, the session is generated for the user’s [most relevant available Vault](/docs#Auth_Defaulting).

`client_id`optional

The ID of the client application at the Authorization server.

### Review Results
- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `authenticate_with_oauth_openid_connect`
- **Updates Made:**
    - Corrected the `vaultDNS` parameter from `dns` to `vaultDNS`.
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

## Retrieve API Versions

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "values": {
       "v7.0": "https://myvault.veevavault.com/api/v7.0",
       "v8.0": "https://myvault.veevavault.com/api/v8.0",
       "v9.0": "https://myvault.veevavault.com/api/v9.0",
       "v10.0": "https://myvault.veevavault.com/api/v10.0",
       "v11.0": "https://myvault.veevavault.com/api/v11.0",
       "v12.0": "https://myvault.veevavault.com/api/v12.0",
       "v13.0": "https://myvault.veevavault.com/api/v13.0",
       "v14.0": "https://myvault.veevavault.com/api/v14.0",
       "v15.0": "https://myvault.veevavault.com/api/v15.0",
       "v16.0": "https://myvault.veevavault.com/api/v16.0",
       "v17.1": "https://myvault.veevavault.com/api/v17.1",
       "v17.2": "https://myvault.veevavault.com/api/v17.2",
       "v17.3": "https://myvault.veevavault.com/api/v17.3",
       "v18.1": "https://myvault.veevavault.com/api/v18.1",
       "v18.2": "https://myvault.veevavault.com/api/v18.2",
       "v18.3": "https://myvault.veevavault.com/api/v18.3",
       "v19.1": "https://myvault.veevavault.com/api/v19.1",
       "v19.2": "https://myvault.veevavault.com/api/v19.2",
       "v19.3": "https://myvault.veevavault.com/api/v19.3",
       "v20.1": "https://myvault.veevavault.com/api/v20.1",
       "v20.2": "https://myvault.veevavault.com/api/v20.2",
       "v20.3": "https://myvault.veevavault.com/api/v20.3",
       "v21.1": "https://myvault.veevavault.com/api/v21.1"
   }
}
'''

Retrieve all supported versions of Vault API.

GET `/api/`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

On success, Vault returns every supported API version. The last version listed in the response may be the Beta version, which is subject to change. Learn more about [Vault API versioning](/docs/#versioning).

### Review Results
- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `retrieve_api_version`
- **Updates Made:**
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

## Authentication Type Discovery

> Request

'''
curl -X POST \
-H "Accept: application/json" \
-H "X-VaultAPI-AuthIncludeMsal: true" \
https://login.veevavault.com/auth/discovery?username=olivia@veepharm.com&client_id=veepharm-clinical-it-client-int0
'''

> Response: Password User

'''
{
    "responseStatus": "SUCCESS",
    "errors": [],
    "data": {
        "auth_type": "password"
    }
}
'''

> Response: SSO User

'''
{
"responseStatus": "SUCCESS",
   "errors": [],
   "data": {
       "auth_type": "sso",
       "auth_profiles": [
           {
               "id": "_a45afc-4773-4e17-9831-2905b2a6",
               "label": "OAuth Azure",
               "description": "This Security Profile connects with Microsoft Azure.",
               "vault_session_endpoint": "https://veepharm.com/auth/oauth/session/_a45a10fc-4773-290ab2a6",
               "use_adal": true,
               "use_msal": true,
               "as_metadata": {
                   "token_endpoint": "https://login.microsoftonline.com/dcf3-468/oauth2/v2.0/token",
                   "token_endpoint_auth_methods_supported": [
                       "client_secret_post",
                       "private_key_jwt",
                       "client_secret_basic"
                   ],
                   "jwks_uri": "https://login.microsoftonline.com/4618-934/discovery/v2.0/keys",
                   "response_modes_supported": [
                       "query",
                       "fragment",
                       "form_post"
                   ],
                   "subject_types_supported": [
                       "pairwise"
                   ],
                   "id_token_signing_alg_values_supported": [
                       "RS256"
                   ],
                   "response_types_supported": [
                       "code",
                       "id_token",
                       "code id_token",
                       "id_token token"
                   ],
                   "scopes_supported": [
                       "openid",
                       "profile",
                       "email",
                       "offline_access"
                   ],
                   "issuer": "https://login.microsoftonline.com/7c5d9e-53443/v2.0",
                   "request_uri_parameter_supported": false,
                   "userinfo_endpoint": "https://graph.microsoft.com/oidc/userinfo",
                   "authorization_endpoint": "https://login.microsoftonline.com/7c3-9343/oauth2/v2.0/authorize",
                   "device_authorization_endpoint": "https://login.microsoftonline.com/57-618-954-543/oauth2/v2.0/devicecode",
                   "http_logout_supported": true,
                   "frontchannel_logout_supported": true,
                   "end_session_endpoint": "https://login.microsoftonline.com/7c577a96e043/oauth2/v2.0/logout",
                   "claims_supported": [
                       "cloud_instance_name",
                       "cloud_instance_host_name",
                       "cloud_graph_host_name",
                       "msgraph_host",
                       "auth_time",
                       "nonce",
                       "preferred_username",
                       "name",
                       "email"
                   ],
                   "kerberos_endpoint": "https://login.microsoftonline.com/7c5-556343/kerberos",
                   "tenant_region_scope": "NA",
                   "cloud_instance_name": "microsoftonline.com",
                   "cloud_graph_host_name": "graph.windows.net",
                   "msgraph_host": "graph.microsoft.com",
                   "rbac_url": "https://pas.windows.net"
               },
               "oauthProviderType": "Azure"
           }
       ]
   }
}
'''

Discover the authentication type of a user. With this API, applications can dynamically adjust the login requirements per user, and support either username/password or OAuth2.0 / OpenID Connect authentication schemes.

POST `https://login.veevavault.com/auth/discovery`

#### Headers

Name

Description

`Accept`

`application/json` (default)

`X-VaultAPI-AuthIncludeMsal`

Set to `true` to include information about MSAL, an authentication library available for some SSO profiles. If omitted, the response does not include MSAL information.

#### Query Parameters

Name

Description

`username`

The user’s Vault user name.

`client_id`

Optional: The user’s mapped Authorization Server `client_id`. This only applies the SSO and OAuth / OpenID Connect Profiles `auth_type`. Learn more about [Client ID in the Vault API Documentation](/docs/#Client_ID).

#### Response Details

The response specifies the user’s authentication type (`auth_type`):

-   `password`: The user is configured with a username and password.
-   `sso`: The user is configured with an SSO Security Policy.

##### SSO Security Policy

If the user’s `auth_type` type is `sso`, the response specifies the user’s authentication profiles (`auth_profiles`). If the user’s Security Policy is associated with:

-   A _SAML_ profile, the `auth_profiles` array is empty. Learn about [SAML profiles in Vault Help](https://platform.veevavault.help/en/lr/43346).
-   An _OAuth 2.0 / OpenID Connect_ profile, the `auth_profiles` array contains information about the policy. Learn about [Configuring OAuth 2.0 / OpenID Connect Profiles in Vault Help](https://platform.veevavault.help/en/lr/43329).

##### auth\_profiles

The `auth_profiles` array contains information about the _OAuth 2.0 / OpenID Connect_ Security Policy configured in the Vault UI by your Vault Administrator.

Name

Description

`id`

The security policy ID.

`label`

The label for this security profile, displayed to Admins in the Vault UI.

`use_adal`

If `true`, indicates ADAL is available for use as an authentication library. For example, if the Authorization Server Provider is set to use `ADFS` or `Azure`, the `use_adal` field will appear in the response as `true`.

`use_msal`

If `true`, indicates MSAL is available for use as an authentication library. If multiple libraries are available, best practice is to use MSAL. This field is included in the response only if the `X-VaultAPI-AuthIncludeMsal` header is set to `true` in the initial request.

`as_metadata`

Information about the _AS Metadata_ uploaded by your Vault Administrator during profile configuration.

`oauthProviderType`

The configured _Authorization Server Provider_. For example, `ADFS` or `Okta`.

##### Client ID

If the user provides a `client_id` and Client Application client ID mapping is defined on the OAuth 2.0 / OpenID Connect profile, the `as_client_id` field will appear in the response with the Authorization Server client ID value. If there is no defined mapping for the specified `client_id`, Vault will not include the `as_client_id` field in the response. Learn about [Client ID Mapping](https://platform.veevavault.help/en/lr/43329) in Vault Help.

### Review Results
- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `authentication_type_discovery`
- **Updates Made:**
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

## Session Keep Alive

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/keep-alive
'''

> Response

'''
{
   "responseStatus": "SUCCESS"
}
'''

Given an active `sessionId`, keep the session active by refreshing the session duration.

A Vault session is considered active as long as some activity (either through the UI or API) happens within the maximum inactive session duration. This maximum inactive session duration varies by Vault and is configured by your Vault Admin. The maximum active session duration is 48 hours, which is not configurable. Learn more about [best practices for session management](/docs/#Session_Mangement).

POST `/api/{version}/keep-alive`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Authorization`

The Vault `sessionId` to keep active.

### Review Results
- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `keep_alive`
- **Updates Made:**
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

## End Session

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/session
'''

> Response

'''
{
"responseStatus": "SUCCESS"
}
'''

Given an active `sessionId`, inactivate an API session. If a user has multiple active sessions, inactivating one session does not inactivate all sessions for that user. Each session has its own unique `sessionId`.

DELETE `/api/{version}/session`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Authorization`

The Vault `sessionId` to end.

### Review Results
- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `logout`
- **Updates Made:**
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

## Salesforce™ Delegated Requests

> Request

'''
curl -X GET \
-H "Authorization: {SFDC_SESSION_TOKEN}" \
-H "X-Auth-Provider: sfdc" \
-H "X-Auth-Host: https://{my_sfdc_domain}" \
https://myveevavault.com/api/{version}/{Vault_Endpoint}
'''

If your Vault uses Salesforce™ Delegated Authentication, you can call Vault API using your Salesforce™ session token. Learn about Salesforce™ Delegated Authentication in [Vault Help](https://platform.veevavault.help/en/lr/9594).

The following prerequisites apply:

-   A valid Vault user must exist with a Security Policy enabled for Salesforce.com™ Delegated Authentication.
-   The trusted 18-character Salesforce.com™ Org ID must be provided.
-   A user with a matching username must exist in Salesforce.com™ Org ID.

#### Headers

Name

Description

`Authorization`

Your Salesforce™ session token.

`X-Auth-Host`

Salesforce™ URL which Vault can use to validate the Salesforce™ session token.

`X-Auth-Provider`

Set to `sfdc` to indicate that Salesforce™ is the authorization provider.

#### Query Parameters

You can also use query string parameters instead of the headers outlined above.

Name

Description

`auth`

Your Salesforce™ session token.

`ext_url`

Salesforce™ URL which Vault can use to validate the Salesforce™ session token.

`ext_ns`

Set to `sfdc` to indicate that Salesforce™ is the authorization provider.

### Review Results
- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `salesforce_delegated_requests`
- **Updates Made:**
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

## Delegated Access

Vault’s delegated access feature provides a secure and audited process for you to designate another user to handle Vault responsibilities on your behalf. Vault tracks all activities performed by the delegate and logs their activities in audit trails that meet compliance standards. Learn more about [delegated access in Vault Help](https://platform.veevavault.help/en/lr/15015).

With Vault API’s delegated access endpoints, you can generate a delegated session ID for any Vaults where you have delegate access. This allows you to call Vault API on behalf of any user who granted you delegate access. For example, a user may grant delegate access to an IT professional for help troubleshooting a problem. Your organization may also utilize delegate access for shared accounts, such as a “Migration User.”

Delegation is Vault-specific: If your IT professional needs access to both your PromoMats and Submissions Vaults, you will need to grant them delegate access in both Vaults.

### Retrieve Delegations

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/delegation/vaults
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "delegated_vaults": [
       {
           "id": 19523,
           "name": "PromoMats",
           "dns": "mypromomatsvault.veevavault..com",
           "delegator_userid": "61579"
       }
   ]
}
'''

Retrieve Vaults where the currently authenticated user has delegate access. You can then use this information to [Initiate a Delegated Session](#Initiate_Delegated_Session).

GET `/api/{version}/delegation/vaults`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

On `SUCCESS`, Vault returns the name, Vault ID, DNS, and user ID for any Vaults the authenticated user has delegate access to. If the response is empty, the authenticated user does not have delegate access to any Vaults.

### Initiate Delegated Session

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-d "vault_id=5791" \
-d "delegator_userid=67899" \
https://myvault.veevavault.com/api/v25.2/delegation/login
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "delegated_sessionid": "1C8DBD593EDCEAD647E5E4C97A438F1F43A25C8679BB8431BDC789BC0BAAE76E0DC42D478721624765A2BA2E923852"
}
'''

Generate a delegated session ID. This allows you to call Vault API on behalf of a user who granted you delegate access. To find which users have granted you delegate access, [Retrieve Delegations](#Retrieve_Delegations).

POST `/api/{version}/delegation/login`

#### Headers

Name

Description

`Authorization`

The `sessionId` of the currently authenticated user who will initiate the delegated session. Cannot be a `delegated_sessionid`.

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Name

Description

`vault_id`required

The `id` value of the Vault to initiate the delegated session.

`delegator_userid`required

The ID of the user who granted the authenticated user delegate access in this Vault.

#### Response Details

On `SUCCESS`, Vault returns a `delegated_sessionid`. To execute Vault API calls with this delegated session, use this `delegated_sessionid` value as the `Authorization` header value.

### Review Results
- **Location:** `veevavault/services/authentication/auth_service.py`
- **Functions:** `retrieve_delegations`, `initiate_delegated_session`
- **Updates Made:**
    - Updated the docstrings to refer to API version 25.2.
- **State:** Compliant with API documentation.
