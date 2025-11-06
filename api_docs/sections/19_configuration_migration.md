<!-- 
VaultAPIDocs Section: # Configuration Migration
Original Line Number: 33055
Generated: August 30, 2025
Part 19 of 38
-->

# Configuration Migration

The following endpoints allow you to export, import, validate, and deploy Vault Packages (VPKs). These packages allow you to migrate configuration changes between two Vaults. Learn more about [Configuration Migration in Vault Help](https://platform.veevavault.help/en/lr/36919).

## Export Package

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "packageName=PKG-0001" \
--output "myVPK.vpk" \
https://myvault.veevavault.com/api/v25.2/services/package
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "url": "/api/v25.2/services/jobs/60905",
    "job_id": 60905
}
'''

POST `/api/{version}/services/package`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

#### Body Parameters

Name

Description

`packageName`required

The name of the Outbound Package you would like to export.

#### Response Details

On `SUCCESS`, the response includes the following information:

-   `url` - The URL to retrieve the current status of the export job.
-   `job_id` - The Job ID value is used to retrieve the status and results of the request.
-   A separate email with a link to download the .vpk file.

## Import Package

> Request

'''
curl -L -X PUT -H 'Authorization: {Session_ID}' \
-H 'Accept: application/json' \
-F 'file=myFile.vpk'\
https://myvault.veevavault.com/api/v25.2/services/package
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "url": "/api/v25.2/services/jobs/88717",
    "job_id": 88717
}
'''

Asynchronously import and validate a VPK package attached to this request. On completion, Vault sends an email notification which includes a link to the [validation log](https://platform.veevavault.help/en/lr/36919#validation-logs). For packages that include Vault Java SDK code, this checks code compilation and restrictions in use of the JDK. For example, `new` is not allowed for non-allowlisted classes. Learn more about [Vault Java SDK limits and restrictions](/sdk/#Limits_Restrictions).

PUT `/api/{version}/services/package`

#### Headers

Name

Description

`Content-Type`

`multipart/form-data` (default) or `application/x-www-form-urlencoded`

`Accept`

`application/json` (default) or `application/xml`

#### Body Parameters

Name

Description

`file`required

`The .vpk file. See Export Package above.`

#### Response Details

On `SUCCESS`, the response includes the following information: `url` - The URL to retrieve the current status of the import job. `job_id` - The Job ID value is used to retrieve the [status](#retrieve-job-status) and results of the request. A separate email with a link to download the [validation log](https://platform.veevavault.help/en/lr/36919#validation-logs).

## Deploy Package

> Request

'''
curl -X PUT -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
https://myvault.veevavault.com/api/v25.2/vobject/vault_package__v/0PI000000000101/actions/deploy
'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "url": "/api/v25.2/services/jobs/23301",
  "job_id": 23301
}
'''

POST `/api/{version}/vobject/vault_package__v/{package_id}/actions/deploy`

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

`package_id`

The `id` field value of the `vault_package__v` object record used for deployment. See [Import Package](#Import_Package_Config).

#### Response Details

On `SUCCESS`, the response includes the following information:

-   `url` - The URL to retrieve the current status of the export job.
-   `job_id` - The Job ID value is used to retrieve the [status](#RetrieveJobStatus) and results of the request.

## Retrieve Package Deploy Results

> Request

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobject/vault_package__v/0PI000000000101/actions/deploy/results
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseDetails": {
        "total_steps": 1,
        "deployed": 1,
        "deployed_with_warnings": 0,
        "deployed_with_failures": 1,
        "deployed_with_error": 0,
        "failed": 0,
        "skipped": 0,
        "package_status__v": "deployed_with_failures__v",
        "deployment_log": [
            {
                "filename": "PKG-0002-Validation.log",
                "url": "https://myvault.veevavault.com/api/v25.2/vobjects/vault_package__v/0PI000000000101/attachments/1208/versions/1/file",
                "created_date__v": "2024-12-04 14:50:17.699"
            },
            {
                "filename": "PKG-0002-Deployment.log",
                "url": "https://myvault.veevavault.com/api/v25.2/vobjects/vault_package__v/0PI000000000101/attachments/1305/versions/1/file",
                "created_date__v": "2024-12-04 14:52:02.149"
            }
        ],
        "data_deployment_log": [
            {
                "filename": "19523_PKG-0002_2024-12-04_14_52_02_Success_Failure_logs.zip",
                "url": "https://myvault.veevavault.com/api/v25.2/services/package/actions/deploy/data_results/966404/19523_PKG-0002_2024-12-04_14_52_02_Success_Failure_logs.zip"
            }
        ]
    },
    "package_steps": [
        {
            "id": "0IS00000000E011",
            "name__v": "00010",
            "step_type__v": "Data",
            "step_name__v": "product__v",
            "type__v": "Object",
            "deployment_status__v": "deployed_with_failures__v",
            "step_label__v": "DSET-00002-product__v",
            "package_components": [],
            "package_data": [
                {
                    "id": "0PT000000003001",
                    "name__v": "DSET-00002-product__v",
                    "object__v": "product__v",
                    "data_type__v": "Object",
                    "data_action__v": "Create",
                    "record_migration_mode__sys": false,
                    "record_count__sys": "21",
                    "checksum__v": "28cebd01b7b76ccd6bac382f614c8827"
                }
            ],
            "package_code": []
        }
    ]
}

'''

After Vault has finished processing the deploy job, use this request to retrieve the results of the completed deployment.

GET `/api/{version}/vobject/vault_package__v/{package_id}/actions/deploy/results`

##### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`package_id`

The `id` field value of the `vault_package__v` object record used for deployment. See [Deploy Package](#Deploy_Package_Config).

#### Response Details

The `deployment_log` provides a URL to download the latest version of the deployment log. If the deployed package includes datasets, the response also provides the `data_deployment_log` with a URL to download the data deployment log.

Learn more about the possible response values for `deployment_status__v` in [Vault Help](https://platform.veevavault.help/en/lr/36919#deploy-status).

## Retrieve Outbound Package Dependencies

> Request: Retrieve Dependencies

'''
curl -X GET -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/outbound_package__v/0PO000000001001/dependencies
'''

> Response: Retrieve Dependencies

'''
{
  "responseStatus": "SUCCESS",
   "responseDetails": {
       "total_dependencies": 1,
       "target_vault_id": 1000486,
       "package_name": "PKG-0001",
       "package_id": "0PO000000001001",
       "package_summary": "Outbound Package",
       "package_description": "Package for deployment",
       "url": "https://myvault.veevavault.com/api/v25.2/vobjects/package_component__v"
   },
   "package_dependencies": [
       {
           "id": "0CD000000000M70",
           "name__v": "Product Label",
           "component_name__v": "product_label__c",
           "component_type__v": "Object",
           "referenced_component_name": "product__v",
           "referenced_component_type": "Object"
        }
    ]
}
'''

> Request: Add Dependencies

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
https://myvault.veevavault.com/api/v25.2/vobjects/package_component__v
'''

> Example JSON Request Body: Add Dependencies

'''
[
   {
       "outbound_package__v": "0PO000000001001",
       "vault_component__v": "0CD000000002810"
   }
]
'''

Outbound packages only include configuration details for the included components. Sometimes, a configuration for one component depends on another component which you may not have explicitly specified.

With this API, you can retrieve all outstanding component dependencies for an outbound package. You can then add these missing dependencies to the package with the [Create Object Records API](#Create_Object_Record).

GET `/api/{version}/vobjects/outbound_package__v/{package_id}/dependencies`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

#### URI Path Parameters

Name

Description

`{package_id}`

The ID of the `outbound_package__v` record from which to retrieve dependencies.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`total_dependencies`

The total number of outstanding component dependencies.

`target_vault_id`

The ID of the target Vault for the outbound package.

`package_name`

The `name__v` value of the outbound package.

`package_id`

The ID of the `outbound_package__v` record with these outstanding dependencies.

`url`

The Vault API request to add missing dependencies to this outbound package. Learn more about [adding dependencies](#Add_Missing_Dependencies).

`package_dependencies`

This array contains information about each of the `total_dependencies`. If there are no outstanding dependencies, this array is not returned.

#### Adding Dependencies

From the `url` in the response, you can add missing dependencies using the [Create Object Records API](#Create_Object_Record) with the following body parameters:

Name

Description

`outbound_package__v`

The ID of the `outbound_package__v` record with these outstanding dependencies. In the retrieve dependencies response body, this is the `package_id` value.

`vault_component__v`

The ID of the component to add. This is the value returned for the dependency in the array. In the retrieve dependencies response body, this is the `id` value of the component within the `package_dependencies` array.

## Component Definition Query

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Accept: application/json" \
--data-urlencode "q=SELECT id, mdl_definition__v FROM vault_component__v WHERE component_type__v = 'Reporttype'"
https://myvault.veevavault.com/api/v25.2/query/components
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "responseDetails": {
       "pagesize": 1000,
       "pageoffset": 0,
       "size": 3,
       "total": 3
   },
   "data": [
   {
       "id": "0CD000000000111",
       "mdl_definition__v": "RECREATE Reporttype binder_section_with_document_and_bind__v (\n   label('Binder Section with Document and Binder'),\n   active(true),\n   description(),\n   primary_object('binder_section'),\n   primary_objects(),\n   configuration({<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<vrt:reportType xmlns:vrt=\"VaultReporttype\">\n  <vrt:upRelationships>\n    <vrt:upRelationship key=\"binder_section.root_binder_id__v\" />\n  </vrt:upRelationships>\n  <vrt:downRelationships>\n    <vrt:downRelationship key=\"documents\" />\n  </vrt:downRelationships>\n</vrt:reportType>\n}),\n   class('Standard')\n);"
   },
   {
       "id": "0CD000000000112",
       "mdl_definition__v": "RECREATE Reporttype binder_with_document__v (\n   label('Binder with Document'),\n   active(true),\n   description(),\n   primary_object('binder'),\n   primary_objects(),\n   configuration({<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<vrt:reportType xmlns:vrt=\"VaultReporttype\">\n  <vrt:downRelationships>\n    <vrt:downRelationship key=\"documents\" />\n  </vrt:downRelationships>\n</vrt:reportType>\n}),\n   class('Standard')\n);"
   },
   {
       "id": "0CD000000000113",
       "mdl_definition__v": "RECREATE Reporttype product_with_document__c (\n   label('Product with Document'),\n   active(true),\n   description('Product with Product (Document)'),\n   primary_object('product__v'),\n   primary_objects(),\n   configuration({<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<vrt:reportType xmlns:vrt=\"VaultReporttype\">\n  <vrt:downRelationships>\n    <vrt:downRelationship key=\"documents.product__v\" />\n  </vrt:downRelationships>\n</vrt:reportType>\n}),\n   class('Standard')\n);"
   }
  ]
}
'''

Retrieve MDL definitions (`mdl_definition__v`) and JSON definitions (`json_definition__v`) of Vault components using a VQL query on the `vault_component__v` and `vault_package_component__v` query targets. Learn more in the [VQL documentation](/vql/#Vault_Component_Definitions).

POST `/api/{version}/query/components`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/x-www-form-urlencoded` or `multipart/form-data`

`X-VaultAPI-RecordProperties`

Optional: If present, the response includes the record properties object. Possible values are `all`, `hidden`, `redacted`, and `weblink`. If omitted, the record properties object is not included in the response. [Learn more](#Record_Properties).

#### Body Parameters

Name

Description

`q`required

A VQL query on the `vault_component__v` or `vault_package_component__v` [query targets](/vql/#Vault_Component_Definitions). The query can be up to 50,000 characters, formatted as `q={query}`. For example, `q=SELECT id FROM vault_component__v`. Note that submitting the query as a query parameter instead may cause you to exceed the maximum URL length.

#### Response Details

On `SUCCESS`, the response includes the following information:

Name

Description

`pagesize`

The number of records displayed per page. This can be modified. [Learn more](/vql/#Limiting_Results).

`pageoffset`

The records displayed on the current page are offset by this number of records. [Learn more](/vql/#Paginating_Results).

`size`

The total number of records displayed on the current page.

`total`

The total number of records found.

`previous_page`

The Pagination URL to navigate to the previous page of results. This is not always available. [Learn more](/vql/#Paginating_Results).

`next_page`

The Pagination URL to navigate to the next page of results. This is not always available. [Learn more](/vql/#Paginating_Results).

`data`

The set of field values specified in the VQL query.

## Vault Compare

> Request

'''
Curl -X POST -H "Authorization: {SESSION_ID}" \
- H "Content-Type: application/x-www-form-urlencoded" \
- d "vault_id=1234" \
- d "results_type=Complete" \
https://myveevavault.com/api/v25.2/objects/vault/actions/compare

'''

> Response

'''
{
  "responseStatus": "SUCCESS",
  "job_id": 16202,
  "url": "/api/v25.2/services/jobs/16202"
}
'''

Compare the configuration of two different Vaults. The Vault you make the request in is the source Vault, and the target Vault for the comparison is listed in the body. Learn more about [Vault Compare in Vault Help](https://platform.veevavault.help/en/lr/40902).

The user who makes the request must be a cross-domain user and must have access to the `vault_component__v` in both Vaults. Learn more about [cross-domain users in Vault Help](https://platform.veevavault.help/en/lr/38996).

POST `/api/{version}/objects/vault/actions/compare`

#### Headers

Name

Description

`Content-Type`

`application/json` (default) or `application/x-www-form-urlencoded`

#### Body Parameters

Name

Description

`vault_id`required

The target Vault `id` for the comparison.

`results_type`optional

To include all configuration values, set this to `complete`. To only see the differences between Vaults, set to `differences`. If omitted, this defaults to `differences`.

`details_type`optional

To show component level details only, set to `none`. To include simple attribute-level details, set to `simple`. To show all attribute-level details, set to `complex`. If omitted, this defaults to `simple`.

`include_doc_binder_templates`optional

To exclude Document and Binder Templates for comparison, set to `false`. If omitted, this defaults to `true` and templates are included.

`include_vault_settings`optional

To exclude Vault Settings for comparison, set to `false`. If omitted, this defaults to `true` and Vault Settings are included.

`component_types`optional

Add a comma separated list of component types to include. For example, `Doclifecycle, Doctype, Workflow`. To exclude all component types, set to `none`. If omitted, this defaults to include all components.

`generate_outbound_packages`optional

If set to `true`, Vault automatically generates an Outbound Package based on differences between the source Vault and target Vault. If omitted, the default value is `false`.

#### Response Details

On `SUCCESS`, the response includes the `url` and `job_id` of the new Comparison Report job. You can use these to find the [Job Status](#Jobs), and using the links from the job status response, download your report. The download is an Excel file. If Vault encounters any MDL component or configuration issues, the job status response also includes a link to download an error log as a CSV file. The authenticated user will also receive an in-app notification with these download links. If there are pending component updates, Vault places the report request in a queue and sends you a notification. Once component update processing is complete, Vault generates the report and sends another notification.

## Vault Configuration Report

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
- H "Content-Type: application/x-www-form-urlencoded" \
- d "include_components_modified_since=2017-01-01" \
https://myveevavault.com/api/v25.2/objects/vault/actions/configreport
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "url": "/api/v25.2/services/jobs/43902",
    "job_id": 43902
}
'''

Generate an Excel report containing configuration information for a Vault. Users must have the _Vault Configuration Report_ permission to use this API.

POST `/api/{version}/objects/vault/actions/configreport`

#### Headers

Name

Description

`Content-Type`

`application/x-www-form-urlencoded`

#### Body Parameters

Name

Description

`include_vault_settings`optional

To exclude Vault Settings for comparison, set to `false`. If omitted, this defaults to `true` and Vault Settings are included.

`include_inactive_components`optional

If set to `true`, inactive components and subcomponents are included in the report. If omitted, defaults to `false` and only active components and subcomponents are included. See [details for inactive workflows](#inactive_workflow_details).

`include_components_modified_since`optional

Only include components modified since the specified date. Provide the date in the format `yyyy-mm-dd`. If omitted, includes all components. This option is not available for subcomponents.

`include_doc_binder_templates`optional

To exclude document and binder templates, set to `false`. If omitted, this defaults to `true` and document and binder templates are included.

`suppress_empty_results`optional

If set to `true`, Vault excludes tabs with only header rows from the report.

`component_types`optional

Add a comma-separated list of component types to include. For example, `Doclifecycle,Doctype,Workflow`. If omitted, this defaults to include all components and Vault includes an Excel object data report in the ZIP file output.

`output_format`optional

Output report as either an `Excel` (XSLX) or `Excel_Macro_Enabled` (XLSM) file. If omitted, defaults to `Excel_Macro_Enabled`.

##### Inactive Document Workflows

Vault ignores the setting `include_inactive_components` for document workflows. If a workflow was active, but is currently in “editing” state, the report shows the latest active version of it. If a workflow has never been active, the report does not include it.

##### Inactive Object Workflows

Vault respects the `include_inactive_components` setting for object workflows. If set to `true`, the report includes all inactive workflows, including those that have never been active. If set to `false`, the report does not include any workflows that are currently in “editing” state, including those that have an active version.

#### Response Details

On `SUCCESS`, the response includes the `url` and `job_id` of the new Configuration Report job. You can use these to find the [Job Status](#Jobs), and using the link from the job status response, download your report. The download is a ZIP file. If Vault encounters any MDL component or configuration issues, the job status response also includes a link to download an error log as a CSV file. The authenticated user will also receive an in-app notification with these download links. If there are pending component updates, Vault places the report request in a queue and sends you a notification. Once component update processing is complete, Vault generates the report and sends another notification.

_Component Modified Date_ values in the report only refer to component-level modifications and do not reflect modifications to subcomponents. For example, modifying an object field does not change the _Component Modified Date_ value for an object, but modifying the object label does. See the [Component Type referenece](/mdl/components) for more information about components and their subcomponents.

## Validate Package

> Request

'''
curl -L -X POST  -H 'Authorization: {Session_ID}' \
-H 'Accept: application/json' \
-F 'file=myFile.vpk' \
https://myvault.veevavault.com/api/v25.2/services/package/actions/validate
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseDetails": {
        "summary": "Auto Claims Linking Config",
        "author": "jennie@veepharm.com",
        "package_name": "PKG-0004-2",
        "package_id": "N/A",
        "source_vault": "51577",
        "package_status": "Blocked",
        "total_steps": 2,
        "total_steps_blocked": 1,
        "start_time": "07:05:2020 06:24:15",
        "end_time": "07:05:2020 06:24:15",
        "package_error": "",
        "package_steps": [
            {
                "name__v": "00010",
                "step_type__v": "Component",
                "step_label__v": "Claim Targets",
                "step_name__v": "annotation_keyword_targets__sys",
                "type__v": "Object",
                "deployment_status__v": "Verified",
                "deployment_action": "Update",
                "dependencies": [
                    {
                        "component_name": "annotation_keyword_targets__sys.base__v",
                        "component_type": "Objecttype",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    },
                    {
                        "component_name": "default_status__v",
                        "component_type": "Picklist",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    }
                ]
            },
            {
                "name__v": "00020",
                "step_type__v": "Component",
                "step_label__v": "Claims Document",
                "step_name__v": "claims_document__c",
                "type__v": "Doctype",
                "deployment_status__v": "Blocked",
                "deployment_action": "Add (missing in Vault)",
                "dependencies": [
                    {
                        "component_name": "document_creation_date__v",
                        "component_type": "Docfield",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    },
                    {
                        "component_name": "reference_documents__c",
                        "component_type": "Doclifecycle",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    },
                    {
                        "component_name": "product__v",
                        "component_type": "Docfield",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    },
                    {
                        "component_name": "air_bulk_03__c",
                        "component_type": "Renditiontype",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "Missing - Block"
                    },
                    {
                        "component_name": "country__v",
                        "component_type": "Docfield",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    }
                ]
            }
        ]
    }
}
'''

Validate a VPK package attached to this request. The validation response will include the same information on dependent components as [validation logs](https://platform.veevavault.help/en/lr/36919#validation-logs) generated through the UI. For packages that include Vault Java SDK code, this checks checks code compilation and restrictions in use of the JDK. For example, `new` is not allowed for non-allowlisted classes. Learn more about [Vault Java SDK limits and restrictions](/sdk/#Limits_Restrictions).

This endpoint does not import your package.

POST `/api/{version}/services/package/actions/validate`

#### Headers

Name

Description

`Accept`

`application/json` (default)

#### Body Parameters

To upload the VPK file, use the multi-part attachment with the file component `”file={filename}”`. The maximum allowed file size is 2GB.

## Validate Inbound Package

> Request

'''
 curl -L -X POST -H 'Authorization: {Session_ID}' \
-H 'Accept: application/json' \
https://myvault.veevavault.com/api/v25.2/services/vobject/vault_package__v/0PI000000000301/actions/validate
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseDetails": {
        "summary": "Auto Claims Linking Config",
        "author": "jennie@veepharm.com",
        "package_name": "PKG-0004-1",
        "package_id": "0PI000000000301",
        "source_vault": "51577",
        "package_status": "Blocked",
        "total_steps": 2,
        "total_component_steps_blocked": 1,
        "start_time": "07:05:2020 06:29:25",
        "end_time": "07:05:2020 06:29:26",
        "package_error": "",
        "package_steps": [
            {
                "id": "0IS000000000301",
                "name__v": "00010",
                "step_type__v": "Component",
                "step_label__v": "Claim Targets",
                "step_name__v": "annotation_keyword_targets__sys",
                "type__v": "Object",
                "deployment_status__v": "Verified",
                "deployment_action": "Update",
                "dependencies": [
                    {
                        "component_name": "annotation_keyword_targets__sys.base__v",
                        "component_type": "Objecttype",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    },
                    {
                        "component_name": "default_status__v",
                        "component_type": "Picklist",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    }
                ]
            },
            {
                "id": "0IS000000000302",
                "name__v": "00020",
                "step_type__v": "Component",
                "step_label__v": "Claims Document",
                "step_name__v": "claims_document__c",
                "type__v": "Doctype",
                "deployment_status__v": "Blocked",
                "deployment_action": "Add (missing in Vault)",
                "dependencies": [
                    {
                        "component_name": "document_creation_date__v",
                        "component_type": "Docfield",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    },
                    {
                        "component_name": "reference_documents__c",
                        "component_type": "Doclifecycle",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    },
                    {
                        "component_name": "product__v",
                        "component_type": "Docfield",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    },
                    {
                        "component_name": "air_bulk_03__c",
                        "component_type": "Renditiontype",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "Missing - Block"
                    },
                    {
                        "component_name": "country__v",
                        "component_type": "Docfield",
                        "subcomponent_name": "",
                        "subcomponent_type": "",
                        "status": "In Target"
                    }
                ]
            }
        ]
    }
}
'''

Validate an imported VPK package before deploying it to your Vault. The validation response includes information on dependent components and whether they exist in the package or in your Vault. You can then add missing dependencies to the package in the source Vault before re-importing and deploying it to your target Vault. Learn more about [validation logs in Vault Help](https://platform.veevavault.help/en/lr/36919#validation-logs).

POST `/api/{version}/services/vobject/vault_package__v/{package_id}/actions/validate`

#### Headers

Name

Description

`Accept`

`application/json`(default)

#### URI Path Parameters

Name

Description

`package_id`

The `id` field value of the `vault_package__v` object record to validate.

## Enable Configuration Mode

> Request

'''
curl -X POST -H 'Authorization: {Session_ID}' \
-H 'Accept: application/json' \
https://myvault.veevavault.com/api/v25.2/services/configuration_mode/actions/enable
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Configuration Mode Active enabled."
}
'''

Enable Configuration Mode in the currently authenticated Vault. When enabled, Configuration Mode locks non-Admin users out of the Vault. Vault Owners and System Admins can still access the Vault to [deploy configuration migration packages](#Deploy_Package_Config) or set up Dynamic Access Control (DAC).

Users with access to multiple Vaults can log in if at least one (1) Vault in the domain is not in Configuration Mode.

Learn more about [Configuration Mode in Vault Help](https://platform.veevavault.help/en/lr/36928).

POST `/api/{version}/services/configuration_mode/actions/enable`

#### Headers

Name

Description

`Accept`

`application/json`(default) or `application/xml`

#### Response Details

On `SUCCESS`, this endpoint enables Configuration Mode in the currently authenticated Vault, terminates sessions for any non-Admin users currently logged in, and prevents other non-Admin users from logging in. Sessions can take up to five (5) minutes to terminate for users accessing the Vault UI and up to 15 minutes for users accessing the API.

## Disable Configuration Mode

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H 'Accept: application/json' \
https://myvault.veevavault.com/api/v25.2/services/configuration_mode/actions/disable
'''

> Response

'''
{
    "responseStatus": "SUCCESS",
    "responseMessage": "Configuration Mode Active disabled."
}
'''

Disable Configuration Mode in the currently authenticated Vault. When you disable Configuration Mode, non-Admin users can now access the Vault.

Learn more about [Configuration Mode in Vault Help](https://platform.veevavault.help/en/lr/36928).

POST `/api/{version}/services/configuration_mode/actions/disable`

#### Headers

Name

Description

`Accept`

`application/json`(default) or `application/xml`

#### Response Details

On `SUCCESS`, this endpoint disables Configuration Mode in the currently authenticated Vault. Vault allows non-Admin users to log back in.
