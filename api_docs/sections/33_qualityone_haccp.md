<!-- 
VaultAPIDocs Section: # QualityOne HACCP
Original Line Number: 41755
Generated: August 30, 2025
Part 33 of 38
-->

# QualityOne HACCP

To use this API, you must have Veeva QualityOne HACCP. Learn more about [HACCP in Vault Help](https://qualityone.veevavault.help/en/lr/576286/).

## Export HACCP Plan Translatable Fields

> Request

'''
curl -L -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
https://myvault.veevavault.com/api/v25.2/app/qualityone/haccp_plan/V7V00000000R001/translatable_fields/actions/export
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "data": {
        "job_id": "392902"
    }
}
'''

Use this endpoint to export translatable fields from a translation copy of a _HACCP Plan_ record and its related transactional records.

Before submitting this request:

-   Generate a translation copy of a _HACCP Plan_ and ensure the copy has an associated _HACCP Translation Generation_ record in the _Ready for Export_ lifecycle state.
-   You must have permission to view all translatable fields in the target _HACCP Plan_.

When triggered, Vault exports the following field types for translation:

-   _Text_
-   _Long Text_
-   _Rich Text_

The API returns the `job_id`. Learn more about [translating HACCP Plans in Vault Help](https://qualityone.veevavault.help/en/lr/771989).

You must run [Retrieve HACCP Plan Translatable Fields](#Retrieve_Translatable_Fields) after running this API in order to make the exported data available.

POST `/api/{version}/app/qualityone/haccp_plan/{haccp_plan_record_id}/translatable_fields/actions/export`

#### Headers

Name

Description

`Accept`

`application/json` (default)

#### URI Path Parameters

Name

Description

`{haccp_plan_record_id}`

The _ID_ field value for the _HACCP Plan_ record you wish to translate.

#### Response Details

On `SUCCESS`, Vault returns a `job_id`. If the size of the translatable field data to export exceeds 250MB, the request fails.

## Retrieve HACCP Plan Translatable Fields

> Request

'''
curl -L -X GET -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
https://myvault.veevavault.com/api/v25.2/app/qualityone/haccp_plan/V7V00000000R001/translatable_fields/file
'''

> Response

'''
[
    {
        "object_name": "haccp_plan__v",
        "field_metadata": [
            {
                "name": "name__v",
                "type": "String",
                "max_length": 128
            },
            {
                "name": "comparison_id__v",
                "type": "String",
                "max_length": 200
            },
            {
                "name": "external_id__v",
                "type": "String",
                "max_length": 128
            },
            {
                "name": "description__v",
                "type": "String",
                "max_length": 1500
            },
            {
                "name": "title__v",
                "type": "String",
                "max_length": 250
            }
        ],
        "language": "es",
        "records": [
            {
                "id": "V7V00000000R001",
                "md5checksum": "9d4c28675262b14653d94089aad16028",
                "fields": {
                    "name__v": "HACCP Plan for Chocolate",
                    "comparison_id__v": "179483_V7V00000000Q001",
                    "external_id__v": null,
                    "description__v": "This HACCP Plan describes the process for manufacturing chocolate.",
                    "title__v": null
                }
            }
        ]
    },
    {
        "object_name": "haccp_plan_ingredient__v",
        "field_metadata": [
            {
                "name": "external_id__v",
                "type": "String",
                "max_length": 128
            },
            {
                "name": "description__v",
                "type": "String",
                "max_length": 1500
            },
            {
                "name": "comparison_id__v",
                "type": "String",
                "max_length": 200
            },
            {
                "name": "ingredient_name__v",
                "type": "String",
                "max_length": 1500
            }
        ],
        "language": "es",
        "records": [
            {
                "id": "V7W00000000C001",
                "md5checksum": "e7cc04b9d6627df2ff52a2f7d29229a4",
                "fields": {
                    "external_id__v": null,
                    "description__v": "Dark chocolate",
                    "comparison_id__v": "179483_V7W00000000B001",
                    "ingredient_name__v": null
                }
            }
        ]
    }
]
'''

After running [Export Translatable HACCP Plan Fields](#Export_Translatable_Fields), use this endpoint to retrieve the exported field data.

Before submitting this request:

-   The target _HACCP Plan_ must have an associated _HACCP Translation Generation_ record in the _Export Complete_ lifecycle state.
-   The user who submits this request must be the same user who invoked the [Export HACCP Plan Translatable Fields](#Export_Translatable_Fields) API.

GET `/api/{version}/app/qualityone/haccp_plan/{haccp_plan_record_id}/translatable_fields/file`

#### Headers

Name

Description

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{haccp_plan_record_id}`

The _ID_ field value for the _HACCP Plan_ record you wish to translate.

#### Response Details

On `SUCCESS`, Vault returns all translatable fields and their values from the target _HACCP Plan_ and its related records. The returned JSON response can be downloaded into a file and includes the following information:

Name

Description

`object_name`

The name of the _HACCP Plan_ related object.

`field_metadata`

Includes metadata from translatable fields, including the `name`, `type`, and `max-char-length`.

`name`

The exported field’s API name.

`type`

The following field types on the target _HACCP Plan_ are included: _Text_ (Metadata return type = `String`), _Long Text_ (Metadata return type = `LongText`), and _Rich Text_ (Metadata return type = `RichText`)

`max-char-length`

The maximum length of a text field.

`language`

The language code of the target _HACCP Plan_.

`records`

Includes information about the record, including `id`, `md5checksum`, and `fields`.

`id`

The _ID_ field value of the record to which the translatable fields belong.

`md5checksum`

Validates that the translation file references the correct _HACCP Plan_.

`fields`

The translatable fields on the target record.

Replace the untranslated field values in the file with translated values and do not modify anything else in the file. The data structure in the file must be intact in order to successfully [Import HACCP Plan Translatable Fields](#Import_Translatable_Fields).

## Import HACCP Plan Translatable Fields

> Request

'''
curl -L -X POST -H "Authorization: {SESSION_ID}" \
-H "Accept: application/json" \
-H 'Content-Type: multipart/form-data' \
-F 'file=@"V7V00000000R001.json"'
https://myvault.veevavault.com/api/v25.2/app/qualityone/haccp_plan/V7V00000000R001/translatable_fields
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "data": {
       "job_id": "392903"
   }
}
'''

Use this endpoint to import translated _HACCP Plan_ data into Vault.

Before submitting this request:

-   You must first run the [Export HACCP Plan Translatable Fields](#Export_Translatable_Fields) and [Retrieve HACCP Plan Translatable Fields](#Retrieve_Translatable_Fields) APIs and modify the returned JSON file with the appropriate translated data.
-   The target _HACCP Plan_ must have an associated _HACCP Translation Generation_ record in the _Export Complete_ lifecycle state.
-   You must have permission to edit all translatable fields in the target _HACCP Plan_.

The following guidelines apply to the input file:

-   Translated field data must be in JSON format.
-   The maximum input JSON file size is 250MB.
-   The following field types are supported for import:
    -   _Text_ (Metadata return type = `String`)
    -   _Long Text_ (Metadata return type = `LongText`)
    -   _Rich Text_ (Metadata return type = `RichText`)
-   See [Translating HACCP Plans](https://qualityone.veevavault.help/en/lr/771989) for additional guidelines.

POST `/api/{version}/app/qualityone/haccp_plan/{haccp_plan_record_id}/translatable_fields`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data`

`Accept`

`application/json`

#### URI Path Parameters

Name

Description

`{haccp_plan_record_id}`

The _ID_ field value for the _HACCP Plan_ record you wish to translate.

#### Body Parameters

Name

Description

`file`required

The filepath of the JSON document. The maximum allowed file size is 250MB.

#### Response Details

On `SUCCESS`, Vault returns a `job_id` and populates the translatable fields on the target _HACCP Plan_ record and its related records with the values provided in the imported JSON file. On `FAILURE`, the response includes a reason for the failure.
