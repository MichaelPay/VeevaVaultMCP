<!-- 
VaultAPIDocs Section: # Metadata Definition Language (MDL)
Original Line Number: 1338
Generated: August 30, 2025
Part 4 of 38
-->

# Metadata Definition Language (MDL)

Vault is configured with a set of [component types](/mdl/components) that make up its configuration elements. Use MDL to create, describe (read), update, and drop (delete) Vault components and manage its configuration. Learn more in our [MDL](/mdl/#Intro_MDL) documentation.

## Execute MDL Script

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
--data-binary @"mdl.txt" \
https://myvault.veevavault.com/api/mdl/execute
'''

> Example Body: RECREATE Picklist

'''
RECREATE Picklist color__c (
   label('Color'),
   active(true),
   Picklistentry red__c(
      value('Red'),
      order(1),
      active(true)
   ),
   Picklistentry blue__c(
      value('Blue'),
      order(2),
      active(true)
   ),
   Picklistentry green__c(
      value('Green'),
      order(3),
      active(true)
   )
);
'''

> Example Body: RECREATE Java SDK Trigger

'''
RECREATE Recordtrigger my_custom_trigger_name__c (
active (true),
source_code (<VeevaData>
...
</VeevaData>)
);
'''

> Response: RECREATE Picklist

'''
{
    "responseStatus": "SUCCESS",
    "script_execution": {
        "code": "GEN-S-0",
        "message": "OK",
        "warnings": 0,
        "failures": 0,
        "exceptions": 0,
        "components_affected": 1,
        "execution_time": 0.028
    },
    "statement_execution": [
        {
            "vault": "promo-vee.vaultdev.com",
            "statement": 1,
            "command": "RECREATE",
            "component": "Picklist.color__c",
            "message": "[SUCCESS] RECREATE Picklist color__c",
            "response": "SUCCESS"
        }
    ]
}
'''

This synchronous endpoint executes the given MDL script on a Vault. Note that some large operations require use of the [asynchronous endpoint](#Execute_MDL_Async).

POST `/api/mdl/execute`

#### Headers

Name

Description

`Content-Type`

`application/json` or `application/xml`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

The body of the request should contain the MDL script to execute. Enter the body as raw data. The body must start with one of the following values:

-   `CREATE`
-   `RECREATE`
-   `RENAME`
-   `ALTER`
-   `DROP`

Learn more in the [MDL Commands](/mdl/#MDL_Commands) documentation.

##### Example Body: RECREATE Picklist

In this example, we update our picklists using the RECREATE command. If a picklist exists with the name `color__c`, Vault updates it to conform to the definition provided. If not, Vault creates a new picklist with the definition provided.

#### Response Details

On `SUCCESS`, the response contains details of the execute.

### Review Results
- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Function:** `execute_mdl_script`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Asynchronous MDL Requests

Instead of a [synchronous request](#Execute_MDL), you must use an [asynchronous request](#Execute_MDL_Async) if you are executing one of the following operations on 10,000+ `raw` object records:

-   Enabling lifecycles
-   Enabling or disabling object types
-   Adding or removing a field
-   Updating the max length of any variable-length field, such as _Text_, _Long Text_, or _Rich Text_
-   Adding or removing an `Index`
-   Changing the fields that compose an `Index` or otherwise would cause reindexing to occur

A raw object is a Vault object where the `data_store` attribute is set to `raw`. To determine if an object is a raw object, retrieve the value of the `data_store` parameter from the [Retrieve Object Metadata](#Retrieve_Object_Metadata) endpoint. Learn more about [raw objects in Vault Help](https://platform.veevavault.help/en/lr/62987).

After initiating an asynchronous request, your raw object’s `configuration_state` becomes `IN_DEPLOYMENT`. While a raw object is `IN_DEPLOYMENT`, you cannot edit its fields, list layouts, or indexes. If your raw object deployment request has not yet begun execution, you can [cancel](#Cancel_HVO) the deployment.

If you don’t need to use the [asynchronous request](#Execute_MDL_Async), it is best practice to use the [synchronous request](#Execute_MDL).

### Review Results
- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Functions:** `execute_mdl_script_async`, `retrieve_async_mdl_script_results`, `cancel_raw_object_deployment`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Execute MDL Script Asynchronously

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/json" \
--data-binary @"raw_object.txt" \
https://myvault.veevavault.com/api/mdl/execute_async
'''

> Example Body: RECREATE Picklist

'''
RECREATE Picklist color__c (
   label('Color'),
   active(true),
   Picklistentry red__c(
      value('Red'),
      order(1),
      active(true)
   ),
   Picklistentry blue__c(
      value('Blue'),
      order(2),
      active(true)
   ),
   Picklistentry green__c(
      value('Green'),
      order(3),
      active(true)
   )
);
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "script_execution": {
       "code": "GEN-S-0",
       "message": "OK",
       "warnings": 0,
       "failures": 0,
       "exceptions": 0,
       "components_affected": 1,
       "execution_time": 0.622
   },
   "job_id": 327103,
   "url": "/api/v25.2/services/jobs/327103"
}
'''

This asynchronous endpoint executes the given MDL script on a Vault.

While you can execute any MDL script with this endpoint, it is required if you’re operating on 10,000+ `raw` object records and executing one of the following operations:

-   Enabling lifecycles
-   Enabling or disabling object types
-   Adding or removing a field
-   Updating the max length of any variable-length field, such as _Text_, _Long Text_, or _Rich Text_
-   Adding or removing an `Index`
-   Changing the fields that compose an `Index` or otherwise would cause reindexing to occur

After initiating this request, your raw object’s `configuration_state` becomes `IN_DEPLOYMENT`. While a raw object is `IN_DEPLOYMENT`, you cannot edit its fields, list layouts, or indexes. If your raw object deployment request has not yet begun execution, you can [cancel](#Cancel_HVO) the deployment.

This endpoint can only queue one asynchronous change at a time. If you have multiple requests, you must wait for the previous request to complete or use a VPK.

POST `/api/mdl/execute_async`

#### Headers

Name

Description

`Content-Type`

`application/json` or `application/xml`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

The body of the request should contain the MDL script to execute. Enter the body as raw data. The body must start with one of the following values:

-   `CREATE`
-   `RECREATE`
-   `RENAME`
-   `ALTER`
-   `DROP`

Learn more in the [MDL Commands](/mdl/#MDL_Commands) documentation.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`job_id`

The Job ID value to retrieve the status and results of this request. Use this ID to query for the [job status](#RetrieveJobStatus) and [results](#Retrieve_MDL_Results).

`url`

URL to retrieve the current job status of this request.

`code`

The response code indicating whether the script has passed or failed syntax validation.

`message`

A descriptive message for any warnings, failures, or exceptions. If there are none, returns `OK`.

`warnings`

The number of warnings received while validating the script syntax.

`failures`

The number of errors received while validating the script syntax.

`exceptions`

The number of exceptions received while validating the script syntax.

`components_affected`

The number of components affected by this script.

`execution_time`

The length of time taken to validate this script syntax, in milliseconds.

### Retrieve Asynchronous MDL Script Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/mdl/execute_async/138016/results
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "script_execution": {
       "code": "GEN-S-0",
       "message": "OK",
       "warnings": 0,
       "failures": 0,
       "exceptions": 0,
       "components_affected": 1,
       "execution_time": 1.585
   },
   "statement_execution": [
       {
           "vault": "dev10platform.vaultdev.com",
           "statement": 1,
           "command": "ALTER",
           "component": "Object.10k_raw__c",
           "message": "[SUCCESS] ALTER Object 10k_raw__c",
           "response": "SUCCESS"
       }
   ]
}
'''

After submitting a request to deploy an MDL script asynchronously, you can query Vault to determine the results of the request.

Before submitting this request:

-   You must have previously requested a submission export job (via the API) which is no longer active.
-   You must have a valid `job_id` field value returned from the [Execute MDL Script Asynchronously](#Execute_MDL_Async) request.

GET `/api/mdl/execute_async/{job_id}/results`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{job_id}`

The `job_id` field value returned from the [Execute MDL Script Asynchronously](#Execute_MDL_Async) request.

#### Response Details

On `SUCCESS`, this endpoint returns the results of the asynchronous MDL script execution, including any errors.

### Cancel Raw Object Deployment

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/vobjects/product__c/actions/canceldeployment
'''

> Response

'''
{
   "responseStatus": "SUCCESS"
}
'''

Cancel a deployment of configuration changes to a raw object. To use this endpoint, your raw object `configuration_state` must be `IN_DEPLOYMENT`.

POST `/api/{version}/metadata/vobjects/{object_name}/actions/canceldeployment`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{object_name}`

The name of the object on which to cancel deployment. This object’s `configuration_state` must be `IN_DEPLOYMENT`.

#### Response Details

If the deployment is cancelled successfully, the API returns `SUCCESS`.

## Retrieve All Component Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/components
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
       {
           "url": "/api/v25.2/metadata/components/Securityprofile",
           "name": "Securityprofile",
           "class": "metadata",
           "abbreviation": "SPR",
           "active": true,
           "label": "Security Profile",
           "label_plural": "Security Profile"
       },
       {
           "url": "/api/v25.2/metadata/components/Tab",
           "name": "Tab",
           "class": "metadata",
           "abbreviation": "TAB",
           "active": true,
           "label": "Tab",
           "label_plural": "Tab",
           "vobject": "vof_tab__sys"
       }
   ]
}
'''

Retrieve metadata of all component types in your Vault.

GET `/api/{version}/metadata/components`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

On `SUCCESS`, the response may include the following for each component type in the currently authenticated Vault:

Name

Description

`url`

URL to retrieve metadata for the component type.

`name`

The component type name as used in MDL commands.

`class`

The class of the component type, either `code` for component types that include SDK source code, or `metadata` for component types that do not include SDK source code.

`abbreviation`

The abbreviated component type name.

`label`

The component type label as it appears in the Vault UI.

`label_plural`

The plural component type label as it appears in the Vault UI.

`cacheable`

Indicates whether or not the component type has a cache.

`cache_type_class`

Indicates the caching strategy used by the component type. If `cacheable` is set to `false`, Vault ignores this value.

`vobject`

The associated Vault object, if applicable.

### Review Results
- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Function:** `retrieve_all_component_metadata`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Retrieve Component Type Metadata

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/metadata/components/Picklist
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "name": "Picklist",
        "class": "metadata",
        "abbreviation": "PIL",
        "active": true,
        "attributes": [
            {
                "name": "label",
                "type": "String",
                "requiredness": "required",
                "max_length": 40,
                "editable": true,
                "multi_value": false
            },
            {
                "name": "active",
                "type": "Boolean",
                "requiredness": "required",
                "editable": false,
                "multi_value": false
            }
        ],
        "sub_components": [
            {
                "name": "Picklistentry",
                "json_collection_name": "Picklistentry",
                "attributes": [
                    {
                        "name": "value",
                        "type": "String",
                        "requiredness": "required",
                        "max_length": 128,
                        "editable": true,
                        "multi_value": false
                    },
                    {
                        "name": "order",
                        "type": "Number",
                        "requiredness": "required",
                        "max_value": 9223372036854775807,
                        "min_value": 0,
                        "scale": 0,
                        "editable": true,
                        "multi_value": false
                    },
                    {
                        "name": "active",
                        "type": "Boolean",
                        "requiredness": "required",
                        "editable": false,
                        "multi_value": false
                    }
                ]
            }
        ]
    }
}
'''

Retrieve metadata of a specific component type.

GET `/api/{version}/metadata/components/{component_type}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{component_type}`

The component type name (`Picklist`, `Docfield`, `Doctype`, etc.).

#### Response Details

On `SUCCESS`, the response contains metadata for the specified component type. Metadata returned varies for each component and subcomponent type. See [Component Types](/mdl/components/) for more information.

Note that some attributes return a `default_cap` value. This is the default edibility of a field and is for internal Veeva use only.

### Review Results
- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Function:** `retrieve_component_type_metadata`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Retrieve Component Records

### Retrieve Component Record Collection

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/configuration/Picklist
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": [
        {
            "name": "color__c",
            "label": "Color",
            "Picklistentry": [
                {
                    "name": "red__c",
                    "value": "Red",
                    "order": 1,
                    "active": true
                },
                {
                    "name": "blue__c",
                    "value": "Blue",
                    "order": 2,
                    "active": true
                },
                {
                    "name": "green__c",
                    "value": "Green",
                    "order": 3,
                    "active": true
                }
            ],
            "active": true,
            "used_in": []
        }
    ]
}
'''

Retrieve all records for a specific component type.

This endpoint does not support retrieving `Object` component records. Instead, use [Retrieve Object Collection](#Retrieve_Object_Collection).

GET `/api/{version}/configuration/{component_type}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{component_type}`

The component type name (`Picklist`, `Docfield`, `Doctype`, etc.). To retrieve records for `Object`, see [Retrieve Object Collection](#Retrieve_Object_Collection).

#### Response Details

On `SUCCESS`, the response contains all component records in the Vault for the specified component type. Each component record returns a minimum of API `name` and UI `label`, but most types return more. Complete details of the component can be retrieved using [Retrieve Component Record](#Retrieve_Component_Record) or [MDL](#Retrieve_Component_Record_MDL).

### Retrieve Component Record (XML/JSON)

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/configuration/Picklist.color__c
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "name": "color__c",
        "label": "Color",
        "Picklistentry": [
            {
                "name": "red__c",
                "value": "Red",
                "order": 1,
                "active": true
            },
            {
                "name": "blue__c",
                "value": "Blue",
                "order": 2,
                "active": true
            },
            {
                "name": "green__c",
                "value": "Green",
                "order": 3,
                "active": true
            }
        ],
        "active": true,
        "used_in": []
    }
}
'''

Retrieve metadata of a specific component record as JSON or XML. To retrieve as MDL, see [Retrieve Component Record MDL](#Retrieve_Component_Record_MDL). Not all component types are eligible for record description retrieval. For details, see the Describe column in the [Component Support Matrix](/mdl/#component-support-matrix).

GET `/api/{version}/configuration/{component_type_and_record_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{component_type_and_record_name}`

The component type name (`Picklist`, `Docfield`, `Doctype`, etc.) followed by the name of the record from which to retrieve metadata. The format is `{Componenttype}.{record_name}`. For example, `Picklist.color__c`. Find this with the [Retrieve Component Record Collection](#Retrieve_Component_Record_Collection) endpoint.

#### Query Parameters

Name

Description

`loc`

When localized (translated) strings are available, retrieve them by setting `loc` to `true`.

#### Response Details

On `SUCCESS`, the response contains the complete definition for a specific component record. If a field returns as blank or null, it means the record has no value for that field.

### Retrieve Component Record (MDL)

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/mdl/components/Picklist.color__c
'''

> Response

'''
RECREATE Picklist color__c (
   label('Color'),
   active(true),
   Picklistentry red__c(
      value('Red'),
      order(1),
      active(true)
   ),
   Picklistentry blue__c(
      value('Blue'),
      order(2),
      active(true)
   ),
   Picklistentry green__c(
      value('Green'),
      order(3),
      active(true)
   )
);
'''

Retrieve metadata of a specific component record as MDL. To retrieve as JSON or XML, see [Retrieve Component Record](#Retrieve_Component_Record). Vault does not generate RECREATE statements for all component types. For details, see the Generate RECREATE column in the [Component Support Matrix](/mdl/#component-support-matrix).

GET `/api/mdl/components/{component_type_and_record_name}`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{component_type_and_record_name}`

The component type name (`Picklist`, `Docfield`, `Doctype`, etc.) followed by the name of the record from which to retrieve metadata. The format is `{Componenttype}.{record_name}`. For example, `Picklist.color__c`. Find this with the [Retrieve Component Record Collection](#Retrieve_Component_Record_Collection) endpoint.

#### Response Details

On `SUCCESS`, the response contains a RECREATE MDL statement of metadata for the specified component record. Metadata returned varies based on component type. If a field returns as blank, it means the record currently has no value for that field. Execute this RECREATE with the [Execute](#Execute_MDL) endpoint.

### Review Results
- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Functions:** `retrieve_component_record_collection`, `retrieve_component_record`, `retrieve_component_record_mdl`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Components with Content

The following Vault component types contain binary content as part of their definition:

-   `Formattedoutput`
-   `Overlaytemplate`
-   `Signaturepage`

The following endpoints allow you to upload, reference, and migrate the binary content of a file.

### Upload Content File

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: multipart/form-data" \
-F 'file=@C:\Quote.pdf'
https://myvault.veevavault.com/api/mdl/files
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "data": {
      "name__v": "4be398c32fc2ccf48adaf6ebe53782a1",
      "format__v": "application/pdf",
      "size__v": 4716,
      "sha1_checksum__v": "4be398c32fc2ccf48adaf6ebe53782a1"
         }
    }
'''

This endpoint allows you to upload a content file to be referenced by a component.

Once uploaded, Vault stores the file in a generic files staging area where they will remain until referenced by a component. Once referenced, Vault cannot access the named file from the staging area.

POST `/api/mdl/files`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data` (default) or `application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Response Details

On `SUCCESS`, the response includes the following:

Name

Description

`name__v`

The name of the file which can be used in MDL for referencing the component.

`format__v`

The format of the file.

`size__v`

The file size of the file.

`sha1_checksum__v`

The SHA-1 checksum value generated for the file. Use the checksum to ensure the file was transmitted correctly.

#### Reference Named File

> Example Body: Reference Named File

'''
RECREATE Formattedoutput my_formatted_output__c (
    label(‘My Formatted Output’),
    active(true),
    root_object('Object.product__v'),
    root_object_type('Objecttype.product__v.base__v'),
    output_type('native'),
    template('4be398c32fc2ccf48adaf6ebe53782a1')
);
'''

After uploading a content file, you can reference the file by name using the `file` or `template` attributes in your MDL statement. This example uses the `template` attribute.

To change a component file, you must first upload it and update the component to reference the new file.

### Retrieve Content File

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/mdl/components/Formattedoutput.my_formatted_output__c/files
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "links": [
        {
            "rel": "my_formatted_output__c.template_file",
            "href": "myvault.veevavault.com/api/mdl/components/Formattedoutput.my_formatted_output__c/files/4be398c32fc2ccf48adaf6ebe53782a1",
            "method": "GET",
            "accept": "application/pdf"
        }
    ],
    "data": [
        {
            "name__v": "4be398c32fc2ccf48adaf6ebe53782a1",
            "original_name__v": "Quote.pdf",
            "format__v": "application/pdf",
            "size__v": 654122,
            "sha1_checksum__v": "4be398c32fc2ccf48adaf6ebe53782a1"
        }
    ]
}
'''

Retrieve the content file of a specified component.

GET `/api/mdl/components/{component_type_and_record_name}/files`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`component_type_and_record_name`

The component type of the record followed by the name of the record from which to retrieve the content file. The format is `{Componenttype}.{record_name}`. For example, `Formattedoutput.my_formatted_output__c`.

#### Response Details

On `SUCCESS`, the response includes the following:

Name

Description

`name__v`

The name of the file which can be used in MDL for referencing the component.

`original_name__v`

The original name of the uploaded file.

`format__v`

The format of the file.

`size__v`

The file size of the file.

`sha1_checksum__v`

The SHA-1 checksum value generated for the file. Use the checksum to ensure the file was transmitted correctly.

### Review Results
- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Functions:** `upload_content_file`, `retrieve_content_file`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
