<!-- 
ReviewResults Section: ## Vault Objects
API Section Match: 07_vault_objects.md
Original Line Number: 97
API Version: v25R2
Generated: August 30, 2025
-->

## Vault Objects

### Retrieve Object Metadata

- **Location:** `veevavault/services/objects/metadata_service.py`
- **Function:** `retrieve_object_metadata`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve Object Field Metadata

- **Location:** `veevavault/services/objects/metadata_service.py`
- **Function:** `retrieve_object_field_metadata`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve Object Collection

- **Location:** `veevavault/services/objects/metadata_service.py`
- **Function:** `retrieve_object_collection`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve Object Records

- **Location:** Uses VQL queries via `veevavault/services/queries/query_service.py`
- **Function:** `query`
- **Updates Made:**
    - No updates needed. This endpoint correctly uses VQL queries for object record retrieval.
- **State:** Compliant with API documentation.

### Retrieve Object Record

- **Location:** `veevavault/services/objects/crud_service.py`
- **Function:** `retrieve_object_record`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Create & Upsert Object Records

- **Location:** `veevavault/services/objects/crud_service.py`
- **Function:** `create_object_records`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Roll-up Fields

#### Recalculate Roll-up Fields

- **Location:** `veevavault/services/objects/rollup_service.py`
- **Function:** `recalculate_rollup_fields`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Retrieve Roll-up Field Recalculation Status

- **Location:** `veevavault/services/objects/rollup_service.py`
- **Function:** `retrieve_rollup_field_recalculation_status`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Update Object Records

- **Location:** `veevavault/services/objects/crud_service.py`
- **Function:** `update_object_records`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Delete Object Records

- **Location:** `veevavault/services/objects/crud_service.py`
- **Function:** `delete_object_records`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Cascade Delete Object Record

- **Location:** `veevavault/services/objects/crud_service.py`
- **Function:** `cascade_delete_object_record`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve Results of Cascade Delete Job

- **Location:** `veevavault/services/objects/crud_service.py`
- **Function:** `retrieve_cascade_delete_results`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Merge Object Records

#### Initiate Record Merge

- **Location:** `veevavault/services/objects/merge_service.py`
- **Function:** `initiate_record_merge`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Retrieve Record Merge Status

- **Location:** `veevavault/services/objects/merge_service.py`
- **Function:** `retrieve_record_merge_status`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Retrieve Record Merge Results

- **Location:** `veevavault/services/objects/merge_service.py`
- **Function:** `retrieve_record_merge_results`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Download Merge Records Job Log

- **Location:** `veevavault/services/objects/merge_service.py`
- **Function:** `download_merge_records_job_log`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Object Types

#### Retrieve Details from All Object Types

- **Location:** `veevavault/services/objects/types_service.py`
- **Function:** `retrieve_details_from_all_object_types`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Retrieve Details from a Specific Object

- **Location:** `veevavault/services/objects/types_service.py`
- **Function:** `retrieve_details_from_specific_object`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Change Object Type

- **Location:** `veevavault/services/objects/types_service.py`
- **Function:** `change_object_type`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Object Roles

#### Retrieve Object Record Roles

- **Location:** `veevavault/services/objects/roles_service.py`
- **Function:** `retrieve_object_record_roles`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Assign Users & Groups to Roles on Object Records

- **Location:** `veevavault/services/objects/roles_service.py`
- **Function:** `assign_users_groups_to_roles_on_object_records`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Remove Users & Groups from Roles on Object Records

- **Location:** `veevavault/services/objects/roles_service.py`
- **Function:** `remove_users_groups_from_roles_on_object_records`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Object Record Attachments

#### Determine if Attachments are Enabled on an Object

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `determine_if_attachments_are_enabled_on_an_object`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Retrieve Object Record Attachments

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `retrieve_object_record_attachments`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Retrieve Object Record Attachment Metadata

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `retrieve_object_record_attachment_metadata`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Retrieve Object Record Attachment Versions

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `retrieve_object_record_attachment_versions`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Retrieve Object Record Attachment Version Metadata

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `retrieve_object_record_attachment_version_metadata`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Retrieve Deleted Object Record Attachments

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `retrieve_deleted_object_record_attachments`
- **Updates Made:**
    - Added this missing endpoint with proper URL and parameters.
- **State:** Compliant with API documentation.

#### Download Object Record Attachment File

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `download_object_record_attachment_file`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Download Object Record Attachment Version File

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `download_object_record_attachment_version_file`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Download All Object Record Attachment Files

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `download_all_object_record_attachment_files`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Create Object Record Attachment

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `create_object_record_attachment`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Create Multiple Object Record Attachments

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `create_multiple_object_record_attachments`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Restore Object Record Attachment Version

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `restore_object_record_attachment_version`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Update Object Record Attachment Description

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `update_object_record_attachment_description`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Update Multiple Object Record Attachment Descriptions

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `update_multiple_object_record_attachment_descriptions`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Delete Object Record Attachment

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `delete_object_record_attachment`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Delete Multiple Object Record Attachments

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `delete_multiple_object_record_attachments`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Delete Object Record Attachment Version

- **Location:** `veevavault/services/objects/attachments_service.py`
- **Function:** `delete_object_record_attachment_version`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Object Page Layouts

#### Retrieve Page Layouts

- **Location:** `veevavault/services/objects/layouts_service.py`
- **Function:** `retrieve_page_layouts`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Retrieve Page Layout Metadata

- **Location:** `veevavault/services/objects/layouts_service.py`
- **Function:** `retrieve_page_layout_metadata`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Attachment Fields

#### Download Attachment Field File

- **Location:** `veevavault/services/objects/attachment_fields_service.py`
- **Function:** `download_attachment_field_file`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Download All Attachment Field Files

- **Location:** `veevavault/services/objects/attachment_fields_service.py`
- **Function:** `download_all_attachment_field_files`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Update Attachment Field File

- **Location:** `veevavault/services/objects/attachment_fields_service.py`
- **Function:** `update_attachment_field_file`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Deep Copy Object Record

- **Location:** `veevavault/services/objects/crud_service.py`
- **Function:** `deep_copy_object_record`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve Results of Deep Copy Job

- **Location:** `veevavault/services/objects/crud_service.py`
- **Function:** `retrieve_deep_copy_results`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve Deleted Object Record ID

- **Location:** `veevavault/services/objects/crud_service.py`
- **Function:** `retrieve_deleted_object_record_id`
- **Updates Made:**
    - Fixed the incorrect URL from `/vobjects/{object_name}/deleted` to `/objects/deletions/vobjects/{object_name}`.
    - Added support for optional query parameters including `start_date` and `end_date`.
- **State:** Compliant with API documentation.

### Retrieve Limits on Objects

- **Location:** `veevavault/services/objects/metadata_service.py`
- **Function:** `retrieve_limits_on_objects`
- **Updates Made:**
    - Fixed the incorrect URL from `/metadata/vobjects/limits` to `/limits`.
- **State:** Compliant with API documentation.

### Update Corporate Currency Fields

- **Location:** `veevavault/services/objects/crud_service.py`
- **Function:** `update_corporate_currency_fields`
- **Updates Made:**
    - Fixed the endpoint method from POST to PUT.
    - Updated the URL structure to support both record-specific and object-wide operations.
    - Made `record_id` parameter optional to support bulk operations.
- **State:** Compliant with API documentation.

### Object Record User Actions

#### Retrieve Object Record User Actions

- **Location:** `veevavault/services/objects/actions_service.py`
- **Function:** `retrieve_object_record_user_actions`
- **Updates Made:**
    - Implemented missing endpoint from scratch.
    - Added to main ObjectService class with convenience method.
- **State:** Compliant with API documentation.

#### Retrieve Object User Action Details

- **Location:** `veevavault/services/objects/actions_service.py`
- **Function:** `retrieve_object_user_action_details`
- **Updates Made:**
    - Implemented missing endpoint from scratch.
    - Added to main ObjectService class with convenience method.
- **State:** Compliant with API documentation.

#### Initiate Object Action on a Single Record

- **Location:** `veevavault/services/objects/actions_service.py`
- **Function:** `initiate_object_action_on_single_record`
- **Updates Made:**
    - Implemented missing endpoint from scratch.
    - Added to main ObjectService class with convenience method.
- **State:** Compliant with API documentation.

#### Initiate Object Action on Multiple Records

- **Location:** `veevavault/services/objects/actions_service.py`
- **Function:** `initiate_object_action_on_multiple_records`
- **Updates Made:**
    - Implemented missing endpoint from scratch.
    - Added to main ObjectService class with convenience method.
- **State:** Compliant with API documentation.

### Object Collection (Internal Service)

#### Retrieve Object Record Collection

- **Location:** `veevavault/services/objects/collection_service.py`
- **Function:** `retrieve_object_record_collection`
- **Updates Made:**
    - No updates needed. This is a separate endpoint from VQL queries for direct object collection retrieval.
- **State:** Compliant with API documentation.
