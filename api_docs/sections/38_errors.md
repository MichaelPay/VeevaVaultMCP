<!-- 
VaultAPIDocs Section: # Errors
Original Line Number: 44253
Generated: August 30, 2025
Part 38 of 38
-->

# Errors

> Example: Failed Authentication

'''
{
    "responseStatus": "FAILURE",
    "errors": [
        {
            "type": "NO_PASSWORD_PROVIDED",
            "message": "No password was provided for the login call."
        }
    ],
    "errorType": "AUTHENTICATION_FAILED"
}
'''

The response of every API call includes a field called `responseStatus`. Possible values are:

-   `SUCCESS` - The API request was successfully processed.
-   `WARNING` - The API request was successfully processed, but with warnings.
-   `FAILURE` - The API request could not be processed because of user error.
-   `EXCEPTION` - The API request could not be processed because of system error.

For a `responseStatus` other than `SUCCESS`, users can inspect the `errors` field in the response. Each `error` includes the following fields:

-   `type` - The specific type of error, e.g., `INVALID_DATA`, `PARAMETER_REQUIRED`, etc. See below for a full list of `types`. These values are not subject to change for a given version of the API, even when newer versions of the API are available.
    
-   `message` - The message accompanying each error type, e.g., `Missing required parameter [{field_name}]`. When available, the error message includes the specific reason, e.g., the `{field_name}` for the error. These messages are subject to change and are not contractual parts for error handling. Developers should consider error messages for debugging and troubleshooting purposes only and should not implement application logic which relies on specific error strings or formatting.
    

When Vault processes an API request, it returns an HTTP response status code of 200. If Vault returns a response status code other than 200, it is likely due to connectivity problems, and we recommend contacting your network team. We recommend basing your logic on the `responseStatus` field and error types, not on the HTTP response status codes.

## Error Types

Type

Description

`UNEXPECTED_ERROR`

General error catch-all when there is no specific error, or an unidentified error.

`MALFORMED_URL`

The specified resource cannot be found.

`METHOD_NOT_SUPPORTED`

The specified resource does not support the (POST, PUT, GET, DELETE) method. Or, the API request is not supported by this version of API.

`INACTIVE_USER`

User is inactive or not found.

`NO_PASSWORD_PROVIDED`

No password was provided for the login call.

`USERNAME_OR_PASSWORD_INCORRECT`

Authentication failed because an invalid username or password was provided.

`USER_LOCKED_OUT`

The user is locked out. Learn more about [user account lockout in Vault Help](https://platform.veevavault.help/en/lr/1985#user_account_lockout).

`PASSWORD_CHANGE_REQUIRED`

Password change required.

`INVALID_SESSION_ID`

Invalid session ID provided.

`PARAMETER_REQUIRED`

Missing required parameters in the API call.

`INVALID_DATA`

Invalid data provided in the API call.

`INSUFFICIENT_ACCESS`

User does not have sufficient privileges to perform the action. Additionally, the `/actions` endpoints may return this error in cases where the user attempts to access a resource which does not exist.

`OPERATION_NOT_ALLOWED`

Certain rules that must be met to perform this operation have not been met.

`ATTRIBUTE_NOT_SUPPORTED`

The specified resource does not recognize provided attributes.

`INVALID_FILTER`

Provided a non-existent filter to Retrieve Documents.

`INCORRECT_QUERY_SYNTAX_ERROR`

Query string used with VQL has an incorrect query syntax.

`RACE_CONDITION`

A rare condition where the same record is being simultaneously updated by another API call.

`EXCEEDS_FILE_MAX_SIZE`

The size of uploaded file exceeds the maximum size allowed (4 GB).

`API_LIMIT_EXCEEDED`

The [Job Status](#RetrieveJobStatus) endpoint can only be requested once every 10 seconds for each `job_id`. When this limit is reached, this error message is returned and no further calls will be processed until the next 10-second period begins. Learn more about [API Limits](/docs/#api-rate-limits).

`CONFIGURATION_MODE_ENABLED`

Non-Admins cannot access a Vault in Configuration Mode. Learn more about [Configuration Mode in Vault Help](https://platform.veevavault.help/en/lr/36928).

`SDK_ERROR`

An error caused by the Vault Java SDK. This error may also include a custom `subtype`. For more information about this error, check the **Debug Log**.

`OPERATION_IN_PROGRESS`

There is already an operation running on the item specified in the request.

`ITEM_NAME_EXISTS`

When creating an item, this error indicates that an item with the same name already exists in the specified location.

`USER_NOT_FOUND`

The specified user cannot be found.

`FEDERATED_ID_ALREADY_EXISTS`

When creating or updating a user, this error indicates that a user with the same Federated ID already exists in the authenticated Vault. Learn more about [user ID types in Vault Help](https://platform.veevavault.help/en/lr/43346/#about-user-id-types).
