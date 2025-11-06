<!-- 
VaultAPIDocs Section: # Custom Pages
Original Line Number: 40022
Generated: August 30, 2025
Part 27 of 38
-->

# Custom Pages

The Custom Pages APIs allow you to manage the client code for Custom Pages using a client code distribution. The client code distribution contains:

-   The client code that defines how Custom Pages display in the Vault UI
-   Metadata that describes the distribution. This metadata must be placed in a manifest file (`distribution-manifest.json`) in the distribution’s root directory.

Client code distributions are [uploaded](#Add_Replace_Single_Distribution) to and downloaded from Vault as a ZIP file. Learn more about [creating a client code distribution for Custom Pages](/custompages/#Client_Code_Distributions).

When creating Custom Pages, you can also use Vault API to:

-   Create a `Page` component using [MDL](#Execute_MDL). Learn more in the [Custom Pages documentation](/custompages/#Configuring_Custom_Page).
-   [Upload and deploy Vault Java SDK server code to Vault](#Add_Code). However, we do not recommend using Vault API to deploy server code. Learn more about the [recommended way to deploy Custom Pages server code to Vault](/custompages/#Developing_Server_Code).

## Retrieve All Client Code Distribution Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/uicode/distributions
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "name": "hello_world__c",
            "checksum": "997e9213cfe8e87e8527e850e1c0f7d4",
            "size": 2633285
        },
        {
            "name": "data_grid__c",
            "checksum": "aef4acfadc4b50a0324f792e217befd3",
            "size": 493836
        },
        {
            "name": "data_form__c",
            "checksum": "edb0125dd7ac83e66159b25fbdd7172b",
            "size": 2633511
        }
    ]
}
'''

Retrieves a list of all client code distributions in the Vault and their metadata.

This endpoint does not retrieve the contents of distribution manifest files.

GET `/api/{version}/uicode/distributions`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

The response lists all client code distributions in the Vault and the following metadata for each distribution:

Field Name

Description

`name`

The name of the client code distribution.

`checksum`

A unique string used to identify the distribution.

`size`

The size of the unzipped client code distribution in bytes.

## Retrieve Single Client Code Distribution Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/uicode/distributions/custom_pages__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "name": "custom_pages__c",
        "checksum": "aef4acfadc4b50a0324f792e217befd3",
        "size": 493836
    }
}
'''

Retrieve metadata for a specific client code distribution, including its name, size, and details from the uploaded `distribution-manifest.json` file.

GET `/api/{version}/uicode/distributions/{distribution_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{distribution_name}`

The `name` attribute of the client code distribution to retrieve.

#### Response Details

The response contains the following metadata, including metadata provided in the [`distribution-manifest.json` file](/custompages/#Client_Code_Distributions):

Field Name

Description

`name`

The name of the client code distribution.

`checksum`

A unique string used to identify the distribution.

`size`

The size of the unzipped client code distribution in bytes.

`pages`

The pages listed in the `distribution-manifest.json` file. For each page, this includes the `name`, `file`, and `export` values.

`stylesheets`

The optional list of stylesheet paths from the `distribution-manifest.json` file.

`importmap`

The optional `importmap` included in the `distribution-manifest.json` file.

## Download Single Client Code Distribution

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/uicode/distributions/custom_page__c/code
'''

> Response Details

'''
Content-Type: application/zip;charset=UTF-8
Content-Disposition: form-data; name="attachment"; filename="custom_page__c.zip"
'''

Download a ZIP file containing the client code distribution directory, including the client code files and the distribution manifest (`distribution-manifest.json`).

GET `/api/{version}/uicode/distributions/{distribution_name}/code`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{distribution_name}`

The `name` attribute of the client code distribution to download.

#### Response Details

On `SUCCESS`, Vault packages and returns the client code distribution directory as a ZIP file. The HTTP Response Header `Content-Type` is set to `application/zip;charset=UTF-8`. The `Content-Disposition` header contains a filename component which can be used when naming the local file. The filename is `{distribution_name}.zip`.

## Add or Replace Single Client Code Distribution

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F "file=@custom-page.zip" \
https://myvault.veevavault.com/api/v25.2/uicode/distributions/
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "name": "custom_page__c",
        "updateType": "ADDED",
        "checksum": "5e7db21710fc4cddfaf5ad5eafdf7052"
    }
}
'''

Add or replace client code in Vault by uploading a ZIP file of the client code distribution. Vault unpacks and compares the uploaded distribution with other distributions in the Vault and:

-   Adds the distribution if the distribution name is new.
-   Replaces a distribution if it has the same name and the client code filenames or contents are different.
-   Makes no changes if the distribution name exists and the code is the same.

POST `/api/{version}/uicode/distributions/`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`multipart/form-data`

#### File Upload

To upload the file, use the multi-part attachment with the file component `"file={file_name}"`. The maximum allowed total file size for all distributions in a Vault is 50 MB.

#### Response Details

Name

Description

`name`

The name of the distribution as specified in the manifest file.

`updateType`

Whether the distribution was added (`ADDED`), replaced (`MODIFIED`), or left unchanged (`NO_CHANGE`).

`checksum`

A unique string used to identify the distribution and whether the contents have changed.

## Delete Single Client Code Distribution

> Request

'''
curl -X DELETE -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/uicode/distributions/custom_page__c
'''

> Response

'''
{
"responseStatus": "SUCCESS"
}
'''

Delete a specific client code distribution. To delete a distribution, you must first remove all `Page` components associated with it from your Vault.

To delete a single file from an existing distribution, re-package the distribution without the file and re-[upload the distribution to Vault](#Add_Replace_Single_Distribution).

DELETE `/api/{version}/uicode/distributions/{distribution_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{distribution_name}`

The `name` attribute of the client code distribution to delete.
