<!-- 
VaultAPIDocs Section: # Vault Query Language (VQL)
Original Line Number: 1009
Generated: August 30, 2025
Part 3 of 38
-->

# Vault Query Language (VQL)

When an application invokes a query call, it passes in a **Vault Query Language (VQL)** statement (a SQL-like statement) that specifies the object to query (in the `FROM` clause), the fields to retrieve (in the `SELECT` clause), and any optional filters to apply (in the `WHERE` and `FIND` clauses) to narrow your results. Learn more in the [VQL documentation](/vql/).

## Submitting a Query

> Request

'''
curl -X POST -H "Authorization: {SESSION_ID}" \
-H "X-VaultAPI-DescribeQuery: true" \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Accept: application/json" \
--data-urlencode "q=SELECT id, name__v FROM documents WHERE product__v = ‘cholecap’"
https://myvault.veevavault.com/api/v25.2/query
'''

> Response

'''
{
   "responseStatus": "SUCCESS",
   "queryDescribe": {
       "object": {
           "name": "documents",
           "label": "documents",
           "label_plural": "documents"
       },
       "fields": [
           {
               "type": "id",
               "required": true,
               "name": "id"
           },
           {
               "label": "Name",
               "type": "String",
               "required": true,
               "name": "name__v",
               "max_length": 100
           }
       ]
   },
   "responseDetails": {
       "pagesize": 1000,
       "pageoffset": 0,
       "size": 5,
       "total": 5
   },
   "data": [
       {
           "id": 72,
           "name__v": "Cholecap-2021-brochure"
       },
       {
           "id": 63,
           "name__v": "Cholecap - Multisequence"
       },
       {
           "id": 36,
           "name__v": "Cholecap Study"
       },
       {
           "id": 25,
           "name__v": "Clinical Trial Reference"
       },
       {
           "id": 24,
           "name__v": "Formulary Guidelines"
       }
   ]
}
'''

Retrieve and filter Vault data using a VQL query.

POST `/api/{version}/query`

#### Headers

Name

Description

`Accept`

`application/json` (default) or `application/xml`

`Content-Type`

`application/x-www-form-urlencoded` or `multipart/form-data`

`X-VaultAPI-DescribeQuery`

Set to `true` to include static field metadata in the response for the data record. If not specified, the response does not include any static field metadata. This option eliminates the need to make additional API calls to understand the shape of query response data. [Learn More](#Describe_Query).

`X-VaultAPI-RecordProperties`

Optional: If present, the response includes the record properties object. Possible values are `all`, `hidden`, `redacted`, and `weblink`. If omitted, the record properties object is not included in the response. [Learn more](#Record_Properties).

#### Body Parameters

Name

Description

`q`required

A VQL query of up to 50,000 characters, formatted as `q={query}`. For example, `q=SELECT id FROM documents`. Note that submitting the query as a query parameter instead may cause you to exceed the maximum URL length.

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

#### About the X-VaultAPI-DescribeQuery Header

When you include the `X-VaultAPI-DescribeQuery` header and set it to `true`, the query response includes the following static metadata description:

Name

Description

`name`

The name of the queryable object.

`label`

The label of the queryable object.

`label_plural`

The plural label of the queryable object

The field metadata may include some or all of the following:

Metadata Field

Description

`name`

The name of the field.

`label`

The UI label of the field.

`type`

The data type, for example, `String` or `Number`

`max_length`

The max length of a string field.

`max_value`

The max value of a number field.

`min_value`

The minimum value of a number field.

`scale`

The number of digits after a decimal point in a number field.

`required`

Indicates whether the field is required (`true`/`false`).

`unique`

Indicates whether the value must be unique (`true`/`false`).

`status`

Indicates whether the field is active (`active`/`inactive`).

`picklist`

The picklist name field value.

`encrypted`

Indicates whether the _Contains Protected Health Information (PHI) or Personally Identifiable Information (PHI)_ setting is selected for this field (`true`/`false`). Learn more in [Vault Help](https://platform.veevavault.help/en/lr/15057#protected-info).

`format_mask`

The format mask expression if it exists. Learn more about format masks in [Vault Help](https://platform.veevavault.help/en/lr/15057#Format_Masks).

`function`

The function name if the VQL query applies a [function](/vql/#Functions_Options) to this field.

`alias`

If `true`, the VQL query applies an [alias](/vql/#AS_Clause) to this field. Omitted if `false`.

**Note:** For formula fields, `queryDescribe` should describe the field as specified in the metadata, excluding the `formula` attribute.

#### About the X-VaultAPI-RecordProperties Header

When you include the `X-VaultAPI-RecordProperties` header, the query response includes the `record_properties` object. The `record_properties` object describes the properties of a data record. If set to `all`, for each record, the response includes:

Name

Description

`id`

The record ID.

`field_properties`

Includes arrays of `hidden`, editable (`edit`), and `redacted` fields. To return only hidden or redacted fields, set the `X-VaultAPI-RecordProperties` header to `hidden` or `redacted`, respectively.

`permissions`

Includes whether this record has `read`, `edit`, `create`, and `delete` permissions.

`subquery_properties`

Includes an array of hidden subquery relationships for this record.

`field_additional_data`

Includes configuration data for `link` type formula fields. To return only this data, set the `X-VaultAPI-RecordProperties` header to `weblink`.

For each field, the `field_additional_data` metadata includes the name of the field and the `web_link` object, which contains the following metadata:

Metadata Field

Description

`label`

The text that appears as a link in the Vault UI.

`target`

Determines whether the link will open in a `new_window` or the `same_window`.

`connection`

Populates another Vault’s DNS within the URL utilizing a configured `connection__sys` object record.

#### About the X-VaultAPI-Facets Header

When you include the `X-VaultAPI-Facets` header with a list of facetable fields, the response includes the `facets` object containing the count of unique values for each facetable field. Determine which fields are facetable using the [Retrieve Object Metadata API](#Retrieve_Object_Metadata). For each facetable field included in the header, the response includes:

Name

Description

`label`

The label for the facetable field in the Vault UI.

`type`

The field’s data type.

`name`

The name of the facetable field.

`count`

The number of unique values for this field in the Vault.

`truncated_list`

A boolean indicating that the list is truncated because it contains more than 50 values.

The `values` metadata contains the unique values for the facetable field in the Vault, sorted first by `result_count` and secondly by `value`.

Metadata Field

Description

`value`

A value of this facetable field in the Vault. For example, `ophthalmology__c`.

`result_count`

The number of records with this field value in the Vault.

### Review Results
- **Location:** `veevavault/services/queries/query_service.py`
- **Function:** `query`
- **Updates Made:**
    - Merged two `query` functions into one to fix a function overwriting issue.
- **State:** Compliant with API documentation.
