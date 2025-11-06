## Authentication

### User Name and Password

- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `authenticate_with_username_password`
- **Updates Made:**
    - Corrected the `vaultDNS` parameter from `dns` to `vaultDNS`.
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

### OAuth 2.0 / OpenID Connect

- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `authenticate_with_oauth_openid_connect`
- **Updates Made:**
    - Corrected the `vaultDNS` parameter from `dns` to `vaultDNS`.
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

### Retrieve API Versions

- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `retrieve_api_version`
- **Updates Made:**
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

### Authentication Type Discovery

- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `authentication_type_discovery`
- **Updates Made:**
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

### Session Keep Alive

- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `keep_alive`
- **Updates Made:**
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

### End Session

- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `logout`
- **Updates Made:**
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

### Salesforce™ Delegated Requests

- **Location:** `veevavault/services/authentication/auth_service.py`
- **Function:** `salesforce_delegated_requests`
- **Updates Made:**
    - Updated the docstring to refer to API version 25.2.
- **State:** Compliant with API documentation.

### Delegated Access

- **Location:** `veevavault/services/authentication/auth_service.py`
- **Functions:** `retrieve_delegations`, `initiate_delegated_session`
- **Updates Made:**
    - Updated the docstrings to refer to API version 25.2.
- **State:** Compliant with API documentation.

## Direct Data

### Retrieve Available Direct Data Files

- **Location:** `veevavault/services/directdata/directdata_service.py`
- **Function:** `retrieve_available_direct_data_files`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Download Direct Data File

- **Location:** `veevavault/services/directdata/directdata_service.py`
- **Function:** `download_direct_data_file`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Vault Query Language (VQL)

### Submitting a Query

- **Location:** `veevavault/services/queries/query_service.py`
- **Function:** `query`
- **Updates Made:**
    - Merged two `query` functions into one to fix a function overwriting issue.
- **State:** Compliant with API documentation.

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

## Metadata Definition Language (MDL)

### Execute MDL Script

- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Function:** `execute_mdl_script`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Asynchronous MDL Requests

- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Functions:** `execute_mdl_script_async`, `retrieve_async_mdl_script_results`, `cancel_raw_object_deployment`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve All Component Metadata

- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Function:** `retrieve_all_component_metadata`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve Component Type Metadata

- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Function:** `retrieve_component_type_metadata`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve Component Records

- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Functions:** `retrieve_component_record_collection`, `retrieve_component_record`, `retrieve_component_record_mdl`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Components with Content

- **Location:** `veevavault/services/mdl/mdl_service.py`
- **Functions:** `upload_content_file`, `retrieve_content_file`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

## Documents

### Retrieve Document Fields

- **Location:** `veevavault/services/documents/fields_service.py`
- **Functions:** `retrieve_all_document_fields`, `retrieve_common_document_fields`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve Document Types

- **Location:** `veevavault/services/documents/types_service.py`
- **Functions:** `retrieve_all_document_types`, `retrieve_document_type`, `retrieve_document_subtype`, `retrieve_document_classification`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Retrieve Documents

- **Location:** `veevavault/services/documents/retrieval_service.py`
- **Functions:** `retrieve_all_documents`, `retrieve_document`, `retrieve_document_versions`, `retrieve_document_version`, `retrieve_document_version_text`, `download_document_file`, `download_document_version_file`, `download_document_version_thumbnail`
- **Updates Made:**
    - Added the `retrieve_document_version_text` function.
- **State:** Compliant with API documentation.

### Create Documents

- **Location:** `veevavault/services/documents/creation_service.py`
- **Functions:** `create_single_document`, `create_multiple_documents`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Update Documents

- **Location:** `veevavault/services/documents/update_service.py`
- **Functions:** `update_single_document`, `update_multiple_documents`, `reclassify_single_document`, `reclassify_multiple_documents`, `update_document_version`, `create_multiple_document_versions`, `create_single_document_version`
- **Updates Made:**
    - Corrected the `Content-Type` header and data format for `update_single_document`.
- **State:** Compliant with API documentation.

### Delete Documents

- **Location:** `veevavault/services/documents/deletion_service.py`
- **Functions:** `delete_single_document`, `delete_multiple_documents`, `delete_single_document_version`, `delete_multiple_document_versions`, `retrieve_deleted_document_ids`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Document Locks

- **Location:** `veevavault/services/documents/locks_service.py`
- **Functions:** `retrieve_document_lock_metadata`, `create_document_lock`, `retrieve_document_lock`, `delete_document_lock`, `undo_collaborative_authoring_checkout`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Document Renditions

- **Location:** `veevavault/services/documents/renditions_service.py`
- **Functions:** `retrieve_document_renditions`, `retrieve_document_version_renditions`, `download_document_rendition_file`, `download_document_version_rendition_file`, `add_multiple_document_renditions`, `add_single_document_rendition`, `upload_document_version_rendition`, `update_multiple_document_renditions`, `replace_document_rendition`, `replace_document_version_rendition`, `delete_multiple_document_renditions`, `delete_single_document_rendition`, `delete_document_version_rendition`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Document Attachments

- **Location:** `veevavault/services/documents/attachments_service.py`
- **Functions:** `determine_if_document_has_attachments`, `retrieve_document_attachments`, `retrieve_document_version_attachments`, `retrieve_document_attachment_versions`, `retrieve_document_version_attachment_versions`, `retrieve_document_version_attachment_version_metadata`, `retrieve_document_attachment_metadata`, `retrieve_document_attachment_version_metadata`, `retrieve_deleted_document_attachments`, `download_document_attachment`, `download_document_attachment_version`, `download_document_version_attachment_version`, `download_all_document_attachments`, `download_all_document_version_attachments`, `delete_single_document_attachment`, `delete_single_document_attachment_version`, `delete_multiple_document_attachments`, `create_document_attachment`, `create_multiple_document_attachments`, `restore_document_attachment_version`, `update_document_attachment_description`, `update_multiple_document_attachment_descriptions`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Document Annotations

- **Location:** `veevavault/services/documents/annotations_service.py`
- **Functions:** `retrieve_annotation_type_metadata`, `retrieve_annotation_placemark_type_metadata`, `retrieve_annotation_reference_type_metadata`, `create_multiple_annotations`, `add_annotation_replies`, `update_annotations`, `read_annotations_by_document_version_and_type`, `read_annotations_by_id`, `read_replies_of_parent_annotation`, `delete_annotations`, `export_document_annotations_to_pdf`, `export_document_version_annotations_to_pdf`, `import_document_annotations_from_pdf`, `import_document_version_annotations_from_pdf`, `retrieve_video_annotations`
- **Updates Made:**
    - Aligned function names with the API documentation.
    - Added the missing `retrieve_video_annotations` function.
- **State:** Compliant with API documentation.

### Document Relationships

- **Location:** `veevavault/services/documents/relationships_service.py`
- **Functions:** `retrieve_document_type_relationships`, `retrieve_document_relationships`, `create_document_relationship`, `create_multiple_document_relationships`, `retrieve_document_relationship`, `delete_document_relationship`, `delete_multiple_document_relationships`
- **Updates Made:**
    - Renamed `create_single_document_relationship` to `create_document_relationship` to align with the API documentation.
    - Renamed `delete_single_document_relationship` to `delete_document_relationship` to align with the API documentation.
- **State:** Compliant with API documentation.

### Export Documents

#### Export Documents

- **Location:** `veevavault/services/documents/exports_service.py`
- **Function:** `export_documents`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Export Document Versions

- **Location:** `veevavault/services/documents/exports_service.py`
- **Function:** `export_document_versions`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

#### Retrieve Document Export Results

- **Location:** `veevavault/services/documents/exports_service.py`
- **Function:** `get_document_export_results`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.

### Document Events

#### Retrieve Document Event Types and Subtypes

- **Location:** `veevavault/services/documents/events_service.py`
- **Function:** `retrieve_document_event_types`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Events > Retrieve Document Event Types and Subtypes

#### Retrieve Document Event Subtype Metadata

- **Location:** `veevavault/services/documents/events_service.py`
- **Function:** `retrieve_document_event_subtype_metadata`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Events > Retrieve Document Event Subtype Metadata

#### Create Document Event

- **Location:** `veevavault/services/documents/events_service.py`
- **Function:** `create_document_event`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Events > Create Document Event

#### Retrieve Document Events

- **Location:** `veevavault/services/documents/events_service.py`
- **Function:** `retrieve_document_events`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Events > Retrieve Document Events

### Document Signatures

#### Retrieve Document Signature Metadata

- **Location:** `veevavault/services/documents/signatures_service.py`
- **Function:** `retrieve_document_signature_metadata`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Signatures > Retrieve Document Signature Metadata

#### Retrieve Archived Document Signature Metadata

- **Location:** `veevavault/services/documents/signatures_service.py`
- **Function:** `retrieve_archived_document_signature_metadata`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Signatures > Retrieve Archived Document Signature Metadata

### Document Tokens

#### Retrieve Document Tokens

- **Location:** `veevavault/services/documents/tokens_service.py`
- **Function:** `create_tokens`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Tokens > Retrieve Document Tokens

### Document Templates

#### Retrieve Document Template Metadata

- **Location:** `veevavault/services/documents/templates_service.py`
- **Function:** `get_template_metadata`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Templates > Retrieve Document Template Metadata

#### Retrieve Document Template Collection

- **Location:** `veevavault/services/documents/templates_service.py`
- **Function:** `get_templates`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Templates > Retrieve Document Template Collection

#### Retrieve Document Template Attributes

- **Location:** `veevavault/services/documents/templates_service.py`
- **Function:** `get_template`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Templates > Retrieve Document Template Attributes

#### Download Document Template File

- **Location:** `veevavault/services/documents/templates_service.py`
- **Function:** `download_template_file`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Templates > Download Document Template File

#### Create Single Document Template

- **Location:** `veevavault/services/documents/templates_service.py`
- **Function:** `create_template`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Templates > Create Single Document Template

#### Create Multiple Document Templates

- **Location:** `veevavault/services/documents/templates_service.py`
- **Function:** `create_templates_batch`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Templates > Create Multiple Document Templates

#### Update Single Document Template

- **Location:** `veevavault/services/documents/templates_service.py`
- **Function:** `update_template`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Templates > Update Single Document Template

#### Update Multiple Document Templates

- **Location:** `veevavault/services/documents/templates_service.py`
- **Function:** `update_templates_batch`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Templates > Update Multiple Document Templates

#### Delete Basic Document Template

- **Location:** `veevavault/services/documents/templates_service.py`
- **Function:** `delete_template`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Templates > Delete Basic Document Template

## Binders

### Retrieve All Binders

- **Location:** `veevavault/services/binders/retrieval_service.py`
- **Function:** `retrieve_all_binders`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Retrieve Binders > Retrieve All Binders

### Retrieve Binder

- **Location:** `veevavault/services/binders/retrieval_service.py`
- **Function:** `retrieve_binder`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Retrieve Binders > Retrieve Binder

### Retrieve All Binder Versions

- **Location:** `veevavault/services/binders/retrieval_service.py`
- **Function:** `retrieve_all_binder_versions`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Retrieve Binders > Retrieve All Binder Versions

### Retrieve Binder Version

- **Location:** `veevavault/services/binders/retrieval_service.py`
- **Function:** `retrieve_binder_version`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Retrieve Binders > Retrieve Binder Version

### Create Binder

- **Location:** `veevavault/services/binders/creation_service.py`
- **Function:** `create_binder`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Create Binders > Create Binder

### Create Binder from Template

- **Location:** `veevavault/services/binders/creation_service.py`
- **Function:** `create_binder_from_template`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Create Binders > Create Binder from Template

### Create Binder Version

- **Location:** `veevavault/services/binders/creation_service.py`
- **Function:** `create_binder_version`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Create Binders > Create Binder Version

### Update Binder

- **Location:** `veevavault/services/binders/update_service.py`
- **Function:** `update_binder`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Update Binders > Update Binder

### Reclassify Binder

- **Location:** `veevavault/services/binders/update_service.py`
- **Function:** `reclassify_binder`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Update Binders > Reclassify Binder

### Update Binder Version

- **Location:** `veevavault/services/binders/update_service.py`
- **Function:** `update_binder_version`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Update Binders > Update Binder Version

### Refresh Binder Auto-Filing

- **Location:** `veevavault/services/binders/update_service.py`
- **Function:** `refresh_binder_auto_filing`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Update Binders > Refresh Binder Auto-Filing

### Delete Binder

- **Location:** `veevavault/services/binders/deletion_service.py`
- **Function:** `delete_binder`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Delete Binders > Delete Binder

### Delete Binder Version

- **Location:** `veevavault/services/binders/deletion_service.py`
- **Function:** `delete_binder_version`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Delete Binders > Delete Binder Version

### Export Binder

- **Location:** `veevavault/services/binders/export_service.py`
- **Function:** `export_binder`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Export Binders > Export Binder

### Export Binder Sections

- **Location:** `veevavault/services/binders/export_service.py`
- **Function:** `export_binder_sections`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Export Binders > Export Binder Sections

### Retrieve Binder Export Results

- **Location:** `veevavault/services/binders/export_service.py`
- **Function:** `retrieve_binder_export_results`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Export Binders > Retrieve Binder Export Results

### Download Exported Binder Files via File Staging

- **Location:** `veevavault/services/binders/export_service.py`
- **Function:** `download_exported_binder_files`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Export Binders > Download Exported Binder Files via File Staging

### Retrieve Binder Relationship

- **Location:** `veevavault/services/binders/relationships_service.py`
- **Function:** `retrieve_binder_relationship`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Relationships > Retrieve Binder Relationship

### Create Binder Relationship

- **Location:** `veevavault/services/binders/relationships_service.py`
- **Function:** `create_binder_relationship`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Relationships > Create Binder Relationship

### Delete Binder Relationship

- **Location:** `veevavault/services/binders/relationships_service.py`
- **Function:** `delete_binder_relationship`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Relationships > Delete Binder Relationship

### Retrieve Binder Sections

- **Location:** `veevavault/services/binders/sections_service.py`
- **Function:** `retrieve_binder_sections`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Sections > Retrieve Binder Sections

### Retrieve Binder Version Section

- **Location:** `veevavault/services/binders/sections_service.py`
- **Function:** `retrieve_binder_version_section`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Sections > Retrieve Binder Version Section

### Create Binder Section

- **Location:** `veevavault/services/binders/sections_service.py`
- **Function:** `create_binder_section`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Sections > Create Binder Section

### Update Binder Section

- **Location:** `veevavault/services/binders/sections_service.py`
- **Function:** `update_binder_section`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Sections > Update Binder Section

### Delete Binder Section

- **Location:** `veevavault/services/binders/sections_service.py`
- **Function:** `delete_binder_section`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Sections > Delete Binder Section

### Add Document to Binder

- **Location:** `veevavault/services/binders/documents_service.py`
- **Function:** `add_document_to_binder`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Documents > Add Document to Binder

### Move Document in Binder

- **Location:** `veevavault/services/binders/documents_service.py`
- **Function:** `move_document_in_binder`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Documents > Move Document in Binder

### Remove Document from Binder

- **Location:** `veevavault/services/binders/documents_service.py`
- **Function:** `remove_document_from_binder`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Documents > Remove Document from Binder

### Retrieve Binder Template Metadata

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `retrieve_binder_template_metadata`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Retrieve Binder Template Metadata

### Retrieve Binder Template Node Metadata

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `retrieve_binder_template_node_metadata`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Retrieve Binder Template Node Metadata

### Retrieve Binder Template Collection

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `retrieve_binder_template_collection`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Retrieve Binder Template Collection

### Retrieve Binder Template Attributes

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `retrieve_binder_template_attributes`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Retrieve Binder Template Attributes

### Retrieve Binder Template Node Attributes

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `retrieve_binder_template_node_attributes`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Retrieve Binder Template Node Attributes

### Create Binder Template

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `create_binder_template`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Create Binder Template

### Bulk Create Binder Templates

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `bulk_create_binder_templates`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Bulk Create Binder Templates

### Create Binder Template Node

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `create_binder_template_node`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Create Binder Template Node

### Update Binder Template

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `update_binder_template`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Update Binder Template

### Bulk Update Binder Templates

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `bulk_update_binder_templates`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Bulk Update Binder Templates

### Replace Binder Template Nodes

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `replace_binder_template_nodes`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Replace Binder Template Nodes

### Delete Binder Template

- **Location:** `veevavault/services/binders/templates_service.py`
- **Function:** `delete_binder_template`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Templates > Delete Binder Template

### Update Binding Rule

- **Location:** `veevavault/services/binders/binding_rules_service.py`
- **Function:** `update_binding_rule`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binding Rules > Update Binding Rule

### Update Binder Section Binding Rule

- **Location:** `veevavault/services/binders/binding_rules_service.py`
- **Function:** `update_binder_section_binding_rule`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binding Rules > Update Binder Section Binding Rule

### Update Binder Document Binding Rule

- **Location:** `veevavault/services/binders/binding_rules_service.py`
- **Function:** `update_binder_document_binding_rule`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binding Rules > Update Binder Document Binding Rule

### Retrieve Binder Roles

- **Location:** `veevavault/services/binders/roles_service.py`
- **Function:** `retrieve_binder_roles`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Roles > Retrieve Binder Roles

### Assign Users & Groups to Binder Roles

- **Location:** `veevavault/services/binders/roles_service.py`
- **Function:** `assign_users_groups_to_binder_roles`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Roles > Assign Users & Groups to Binder Roles

### Remove Users & Groups from Binder Roles

- **Location:** `veevavault/services/binders/roles_service.py`
- **Function:** `remove_user_group_from_binder_role`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder Roles > Remove Users & Groups from Binder Roles

### Retrieve Binder User Actions

- **Location:** `veevavault/services/binders/lifecycle_service.py`
- **Function:** `retrieve_binder_user_actions`
- **Updates Made:**
    - Created new BinderLifecycleService to implement missing lifecycle endpoints.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder User Actions > Retrieve Binder User Actions

### Retrieve User Actions on Multiple Binders

- **Location:** `veevavault/services/binders/lifecycle_service.py`
- **Function:** `retrieve_user_actions_multiple_binders`
- **Updates Made:**
    - Created new BinderLifecycleService to implement missing lifecycle endpoints.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder User Actions > Retrieve User Actions on Multiple Binders

### Retrieve Binder Entry Criteria

- **Location:** `veevavault/services/binders/lifecycle_service.py`
- **Function:** `retrieve_binder_entry_criteria`
- **Updates Made:**
    - Created new BinderLifecycleService to implement missing lifecycle endpoints.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder User Actions > Retrieve Binder Entry Criteria

### Initiate Binder User Action

- **Location:** `veevavault/services/binders/lifecycle_service.py`
- **Function:** `initiate_binder_user_action`
- **Updates Made:**
    - Created new BinderLifecycleService to implement missing lifecycle endpoints.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder User Actions > Initiate Binder User Action

### Initiate Bulk Binder User Actions

- **Location:** `veevavault/services/binders/lifecycle_service.py`
- **Function:** `initiate_bulk_binder_user_actions`
- **Updates Made:**
    - Created new BinderLifecycleService to implement missing lifecycle endpoints.
- **State:** Compliant with API documentation.
- **Section:** Binders > Binder User Actions > Initiate Bulk Binder User Actions

## Document & Binder Roles

### Retrieve All Document Roles

- **Location:** `veevavault/services/objects/objects_service.py`
- **Function:** `retrieve_all_document_roles`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Document & Binder Roles > Document Roles > Retrieve All Document Roles

### Retrieve Document Role

- **Location:** `veevavault/services/objects/objects_service.py`
- **Function:** `retrieve_document_role`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Document & Binder Roles > Document Roles > Retrieve Document Role

### Assign Users & Groups to Roles on a Single Document

- **Location:** `veevavault/services/objects/objects_service.py`
- **Function:** `assign_users_groups_to_roles_on_single_document`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Document & Binder Roles > Document Roles > Assign Users & Groups to Roles on a Single Document

### Assign Users & Groups to Roles on Multiple Documents & Binders

- **Location:** `veevavault/services/objects/objects_service.py`
- **Function:** `assign_users_groups_to_roles_on_multiple_documents_binders`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Document & Binder Roles > Document Roles > Assign Users & Groups to Roles on Multiple Documents & Binders

### Remove Users & Groups from Roles on a Single Document

- **Location:** `veevavault/services/objects/objects_service.py`
- **Function:** `remove_users_groups_from_roles_on_single_document`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Document & Binder Roles > Document Roles > Remove Users & Groups from Roles on a Single Document

### Remove Users & Groups from Roles on Multiple Documents & Binders

- **Location:** `veevavault/services/objects/objects_service.py`
- **Function:** `remove_users_groups_from_roles_on_multiple_documents_binders`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Document & Binder Roles > Document Roles > Remove Users & Groups from Roles on Multiple Documents & Binders

### Retrieve Binder Roles

- **Location:** `veevavault/services/binders/roles_service.py`
- **Function:** `retrieve_binder_roles`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Document & Binder Roles > Binder Roles > Retrieve Binder Roles

### Assign Users & Groups to Binder Roles

- **Location:** `veevavault/services/binders/roles_service.py`
- **Function:** `assign_users_groups_to_binder_roles`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Document & Binder Roles > Binder Roles > Assign Users & Groups to Binder Roles

### Remove Users & Groups from Binder Roles

- **Location:** `veevavault/services/binders/roles_service.py`
- **Function:** `remove_user_group_from_binder_role`
- **Updates Made:**
    - No updates needed.
- **State:** Compliant with API documentation.
- **Section:** Document & Binder Roles > Binder Roles > Remove Users & Groups from Binder Roles

## Document Lifecycle & Workflows

### Retrieve Document User Actions

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `retrieve_document_user_actions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Document User Actions > Retrieve Document User Actions

### Retrieve User Actions on Multiple Documents

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `retrieve_user_actions_on_multiple_documents`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Document User Actions > Retrieve User Actions on Multiple Documents

### Retrieve Document Entry Criteria

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `retrieve_document_entry_criteria`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Document User Actions > Retrieve Document Entry Criteria

### Initiate Document User Action

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `initiate_document_user_action`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Document User Actions > Initiate Document User Action

### Download Controlled Copy Job Results

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `download_controlled_copy_job_results`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Document User Actions > Download Controlled Copy Job Results

### Initiate Bulk Document User Actions

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `initiate_bulk_document_user_actions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Document User Actions > Initiate Bulk Document User Actions

### Retrieve Lifecycle Role Assignment Rules

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `retrieve_lifecycle_role_assignment_rules`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Lifecycle Role Assignment Rules > Retrieve Lifecycle Role Assignment Rules

### Create Lifecycle Role Assignment Override Rules

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `create_lifecycle_role_assignment_override_rules`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Lifecycle Role Assignment Rules > Create Lifecycle Role Assignment Override Rules

### Update Lifecycle Role Assignment Rules

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `update_lifecycle_role_assignment_rules`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Lifecycle Role Assignment Rules > Update Lifecycle Role Assignment Rules

### Delete Lifecycle Role Assignment Override Rules

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `delete_lifecycle_role_assignment_override_rules`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Lifecycle Role Assignment Rules > Delete Lifecycle Role Assignment Override Rules

### Retrieve All Document Workflows

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `retrieve_all_document_workflows`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Document Workflows > Retrieve All Document Workflows

### Retrieve Document Workflow Details

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `retrieve_document_workflow_details`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Document Workflows > Retrieve Document Workflow Details

### Initiate Document Workflow

- **Location:** `veevavault/services/lifecycle_and_workflow/document.py`
- **Function:** `initiate_document_workflow`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Document Lifecycle & Workflows > Document Workflows > Initiate Document Workflow

## Object Lifecycle & Workflows

### Retrieve Object Record User Actions

- **Location:** `veevavault/services/lifecycle_and_workflow/object.py`
- **Function:** `retrieve_object_record_user_actions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Object Lifecycle & Workflows > Object Record User Actions > Retrieve Object Record User Actions

### Retrieve Object User Action Details

- **Location:** `veevavault/services/lifecycle_and_workflow/object.py`
- **Function:** `retrieve_object_user_action_details`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Object Lifecycle & Workflows > Object Record User Actions > Retrieve Object User Action Details

### Initiate Object Action on Single Record

- **Location:** `veevavault/services/lifecycle_and_workflow/object.py`
- **Function:** `initiate_object_action_on_single_record`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Object Lifecycle & Workflows > Object Record User Actions > Initiate Object Action on Single Record

### Initiate Object Action on Multiple Records

- **Location:** `veevavault/services/lifecycle_and_workflow/object.py`
- **Function:** `initiate_object_action_on_multiple_records`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Object Lifecycle & Workflows > Object Record User Actions > Initiate Object Action on Multiple Records

### Retrieve All Multi-Record Workflows

- **Location:** `veevavault/services/lifecycle_and_workflow/object.py`
- **Function:** `retrieve_all_multi_record_workflows`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Object Lifecycle & Workflows > Multi-Record Workflows > Retrieve All Multi-Record Workflows

### Retrieve Multi-Record Workflow Details

- **Location:** `veevavault/services/lifecycle_and_workflow/object.py`
- **Function:** `retrieve_multi_record_workflow_details`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Object Lifecycle & Workflows > Multi-Record Workflows > Retrieve Multi-Record Workflow Details

### Initiate Multi-Record Workflow

- **Location:** `veevavault/services/lifecycle_and_workflow/object.py`
- **Function:** `initiate_multi_record_workflow`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Object Lifecycle & Workflows > Multi-Record Workflows > Initiate Multi-Record Workflow

## Workflows

### Retrieve Workflow Tasks

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `retrieve_workflow_tasks`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Retrieve Workflow Tasks

### Retrieve Workflow Task Details

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `retrieve_workflow_task_details`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Retrieve Workflow Task Details

### Retrieve Workflow Task Actions

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `retrieve_workflow_task_actions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Retrieve Workflow Task Actions

### Retrieve Workflow Task Action Details

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `retrieve_workflow_task_action_details`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Retrieve Workflow Task Action Details

### Accept Multi-item Workflow Task

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `accept_multi_item_workflow_task`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Accept Multi-item Workflow Task

### Accept Single Record Workflow Task

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `accept_single_record_workflow_task`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Accept Single Record Workflow Task

### Undo Workflow Task Acceptance

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `undo_workflow_task_acceptance`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Undo Workflow Task Acceptance

### Complete Multi-item Workflow Task

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `complete_multi_item_workflow_task`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Complete Multi-item Workflow Task

### Complete Single Record Workflow Task

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `complete_single_record_workflow_task`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Complete Single Record Workflow Task

### Reassign Multi-item Workflow Task

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `reassign_multi_item_workflow_task`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Reassign Multi-item Workflow Task

### Reassign Single Record Workflow Task

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `reassign_single_record_workflow_task`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Reassign Single Record Workflow Task

### Update Workflow Task Due Date

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `update_workflow_task_due_date`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Update Workflow Task Due Date

### Cancel Workflow Task

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `cancel_workflow_task`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Cancel Workflow Task

### Manage Multi-item Workflow Content

- **Location:** `veevavault/services/workflows/task_service.py`
- **Function:** `manage_multi_item_workflow_content`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflow Tasks > Manage Multi-item Workflow Content


### Retrieve Workflows

- **Location:** `veevavault/services/workflows/workflow_service.py`
- **Function:** `retrieve_workflows`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflows > Retrieve Workflows

### Retrieve Workflow Details

- **Location:** `veevavault/services/workflows/workflow_service.py`
- **Function:** `retrieve_workflow_details`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflows > Retrieve Workflow Details

### Retrieve Workflow Actions

- **Location:** `veevavault/services/workflows/workflow_service.py`
- **Function:** `retrieve_workflow_actions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflows > Retrieve Workflow Actions

### Retrieve Workflow Action Details

- **Location:** `veevavault/services/workflows/workflow_service.py`
- **Function:** `retrieve_workflow_action_details`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflows > Retrieve Workflow Action Details

### Initiate Workflow Action

- **Location:** `veevavault/services/workflows/workflow_service.py`
- **Function:** `initiate_workflow_action`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Workflows > Initiate Workflow Action

### Bulk Workflow Actions

#### Retrieve Bulk Workflow Actions

- **Location:** `veevavault/services/workflows/bulk_action_service.py`
- **Function:** `retrieve_bulk_workflow_actions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Bulk Workflow Actions > Retrieve Bulk Workflow Actions

#### Retrieve Bulk Workflow Action Details

- **Location:** `veevavault/services/workflows/bulk_action_service.py`
- **Function:** `retrieve_bulk_workflow_action_details`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Bulk Workflow Actions > Retrieve Bulk Workflow Action Details

#### Initiate Bulk Workflow Action

- **Location:** `veevavault/services/workflows/bulk_action_service.py`
- **Function:** `initiate_bulk_workflow_action`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Bulk Workflow Actions > Initiate Bulk Workflow Action

## Users

### Retrieve User Metadata

- **Location:** `veevavault/services/users/users.py`
- **Function:** `retrieve_user_metadata`
- **Updates Made:**
    - Added API reference documentation for consistency
- **State:** Compliant with API documentation.
- **Section:** Users > Retrieve User Metadata

### Retrieve All Users

- **Location:** `veevavault/services/users/users.py`
- **Function:** `retrieve_all_users`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Retrieve All Users

### Retrieve User

- **Location:** `veevavault/services/users/users.py`
- **Function:** `retrieve_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Retrieve User

### Create Users

#### Create Single User

- **Location:** `veevavault/services/users/users.py`
- **Function:** `create_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Create Users > Create Single User

#### Create Multiple Users

- **Location:** `veevavault/services/users/users.py`
- **Function:** `create_multiple_users`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Create Users > Create Multiple Users

### Update Users

#### Update Single User

- **Location:** `veevavault/services/users/users.py`
- **Function:** `update_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Update Users > Update Single User

#### Update My User

- **Location:** `veevavault/services/users/users.py`
- **Function:** `update_my_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Update Users > Update My User

#### Update Multiple Users

- **Location:** `veevavault/services/users/users.py`
- **Function:** `update_multiple_users`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Update Users > Update Multiple Users

### Disable User

- **Location:** `veevavault/services/users/users.py`
- **Function:** `disable_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Disable User

### Change My Password

- **Location:** `veevavault/services/users/users.py`
- **Function:** `change_my_password`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Change My Password

### Update Vault Membership

- **Location:** `veevavault/services/users/users.py`
- **Function:** `update_vault_membership`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Update Vault Membership

### Retrieve Application License Usage

- **Location:** `veevavault/services/users/users.py`
- **Function:** `retrieve_application_license_usage`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Retrieve Application License Usage

### Retrieve User Permissions

- **Location:** `veevavault/services/users/users.py`
- **Function:** `retrieve_user_permissions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Retrieve User Permissions

### Retrieve My User Permissions

- **Location:** `veevavault/services/users/users.py`
- **Function:** `retrieve_my_permissions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Retrieve My User Permissions

### Validate Session User

- **Location:** `veevavault/services/users/users.py`
- **Function:** `validate_session_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Users > Validate Session User

## SCIM

### Discovery Endpoints

#### Retrieve SCIM Provider

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `retrieve_scim_provider`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Discovery Endpoints > Retrieve SCIM Provider

#### Retrieve All SCIM Schema Information

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `retrieve_all_scim_schemas`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Discovery Endpoints > Retrieve All SCIM Schema Information

#### Retrieve Single SCIM Schema Information

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `retrieve_single_scim_schema`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Discovery Endpoints > Retrieve Single SCIM Schema Information

#### Retrieve All SCIM Resource Types

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `retrieve_all_scim_resource_types`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Discovery Endpoints > Retrieve All SCIM Resource Types

#### Retrieve Single SCIM Resource Type

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `retrieve_single_scim_resource_type`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Discovery Endpoints > Retrieve Single SCIM Resource Type

### Users

#### Retrieve All Users with SCIM

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `retrieve_all_users`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Users > Retrieve All Users with SCIM

#### Retrieve Single User with SCIM

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `retrieve_single_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Users > Retrieve Single User with SCIM

#### Retrieve Current User with SCIM

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `retrieve_current_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Users > Retrieve Current User with SCIM

#### Update Current User with SCIM

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `update_current_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Users > Update Current User with SCIM

#### Create User with SCIM

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `create_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Users > Create User with SCIM

#### Update User with SCIM

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `update_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Users > Update User with SCIM

### Retrieve SCIM Resources

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `retrieve_scim_resources`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Retrieve SCIM Resources

### Retrieve Single SCIM Resource

- **Location:** `veevavault/services/scim/scim.py`
- **Function:** `retrieve_single_scim_resource`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** SCIM > Retrieve Single SCIM Resource

## Groups

### Retrieve Group Metadata

- **Location:** `veevavault/services/groups/groups.py`
- **Function:** `retrieve_group_metadata`
- **Updates Made:**
    - Added API reference documentation for consistency
- **State:** Compliant with API documentation.
- **Section:** Groups > Retrieve Group Metadata

### Retrieve All Groups

- **Location:** `veevavault/services/groups/groups.py`
- **Function:** `retrieve_all_groups`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Groups > Retrieve All Groups

### Retrieve Auto Managed Groups

- **Location:** `veevavault/services/groups/groups.py`
- **Function:** `retrieve_auto_managed_groups`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Groups > Retrieve Auto Managed Groups

### Retrieve Group

- **Location:** `veevavault/services/groups/groups.py`
- **Function:** `retrieve_group`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Groups > Retrieve Group

### Create Group

- **Location:** `veevavault/services/groups/groups.py`
- **Function:** `create_group`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Groups > Create Group

### Update Group

- **Location:** `veevavault/services/groups/groups.py`
- **Function:** `update_group`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Groups > Update Group

### Delete Group

- **Location:** `veevavault/services/groups/groups.py`
- **Function:** `delete_group`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Groups > Delete Group

## Clinical Operations

### Create EDLs

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `create_edls`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Create EDLs

### Recalculate Milestone Document Field

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `recalculate_milestone_document_field`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Recalculate Milestone Document Field

#### Apply EDL Template to a Milestone

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `apply_edl_template_to_milestone`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Apply EDL Template to a Milestone

#### Create Milestones from Template

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `create_milestones_from_template`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Create Milestones from Template

#### Execute Milestone Story Events

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `execute_milestone_story_events`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Execute Milestone Story Events

#### Generate Milestone Documents

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `generate_milestone_documents`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Generate Milestone Documents

#### Veeva Site Connect: Distribute to Sites

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `distribute_to_sites`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Veeva Site Connect: Distribute to Sites

#### Populate Site Fee Definitions

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `populate_site_fee_definitions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Populate Site Fee Definitions

#### Populate Procedure Definitions

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `populate_procedure_definitions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Populate Procedure Definitions

#### Initiate Clinical Record Merge

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `initiate_clinical_record_merge`
- **Updates Made:**
    - Added missing implementation for Clinical Record Merge endpoint.
    - Added comprehensive docstring with API documentation details.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Initiate Clinical Record Merge

#### Enable Study Migration Mode

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `enable_study_migration_mode`
- **Updates Made:**
    - Added missing implementation for Enable Study Migration Mode endpoint.
    - Added comprehensive docstring with API documentation details.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Enable Study Migration Mode

#### Disable Study Migration Mode

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `disable_study_migration_mode`
- **Updates Made:**
    - Added missing implementation for Disable Study Migration Mode endpoint.
    - Added comprehensive docstring with API documentation details.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Disable Study Migration Mode

#### Retrieve OpenData Clinical Affiliations

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `retrieve_opendata_clinical_affiliations`
- **Updates Made:**
    - Added missing implementation for Retrieve OpenData Clinical Affiliations endpoint.
    - Added comprehensive docstring with API documentation details.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Retrieve OpenData Clinical Affiliations

### Change Primary Investigator Affiliation

- **Location:** `veevavault/services/applications/clinical_operations/clinical_operations_service.py`
- **Function:** `change_primary_investigator_affiliation`
- **Updates Made:**
    - Added missing implementation for Change Primary Investigator Affiliation endpoint.
    - Added comprehensive docstring with API documentation details.
- **State:** Compliant with API documentation.
- **Section:** Clinical Operations > Change Primary Investigator Affiliation

## QualityDocs

### Document Role Check for Document Change Control

- **Location:** `veevavault/services/applications/quality_docs/quality_docs_service.py`
- **Function:** `document_role_check_for_document_change_control`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** QualityDocs > Document Role Check for Document Change Control

## QMS

### Manage Quality Team Assignments

- **Location:** `veevavault/services/applications/qms/qms_service.py`
- **Function:** `manage_quality_team_assignments`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** QMS > Manage Quality Team Assignments

## Batch Release

### Create Disposition

- **Location:** `veevavault/services/applications/qms/qms_service.py`
- **Function:** `create_batch_disposition`
- **Updates Made:**
    - Added missing implementation for Batch Release Create Disposition endpoint.
    - Added comprehensive docstring with API documentation details.
- **State:** Compliant with API documentation.
- **Section:** Batch Release > Create Disposition

## QualityOne

### Manage Team Assignments

- **Location:** `veevavault/services/applications/quality_one/quality_one_service.py`
- **Function:** `manage_team_assignments`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** QualityOne > Manage Team Assignments

## QualityOne HACCP

### Export HACCP Plan Translatable Fields

- **Location:** `veevavault/services/applications/quality_one/quality_one_service.py`
- **Function:** `export_haccp_plan_translatable_fields`
- **Updates Made:**
    - Added missing implementation for QualityOne HACCP Export Translatable Fields endpoint.
    - Added comprehensive docstring with API documentation details.
- **State:** Compliant with API documentation.
- **Section:** QualityOne HACCP > Export HACCP Plan Translatable Fields

### Retrieve HACCP Plan Translatable Fields

- **Location:** `veevavault/services/applications/quality_one/quality_one_service.py`
- **Function:** `retrieve_haccp_plan_translatable_fields`
- **Updates Made:**
    - Added missing implementation for QualityOne HACCP Retrieve Translatable Fields endpoint.
    - Added comprehensive docstring with API documentation details.
- **State:** Compliant with API documentation.
- **Section:** QualityOne HACCP > Retrieve HACCP Plan Translatable Fields

### Import HACCP Plan Translatable Fields

- **Location:** `veevavault/services/applications/quality_one/quality_one_service.py`
- **Function:** `import_haccp_plan_translatable_fields`
- **Updates Made:**
    - Added missing implementation for QualityOne HACCP Import Translatable Fields endpoint.
    - Added comprehensive docstring with API documentation details.
- **State:** Compliant with API documentation.
- **Section:** QualityOne HACCP > Import HACCP Plan Translatable Fields

### RIM Submissions Archive

#### Import Submission

- **Location:** `veevavault/services/applications/rim_submissions_archive/rim_submissions_archive_service.py`
- **Function:** `import_submission`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** RIM Submissions Archive > Import Submission

#### Retrieve Submission Import Results

- **Location:** `veevavault/services/applications/rim_submissions_archive/rim_submissions_archive_service.py`
- **Function:** `retrieve_submission_import_results`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** RIM Submissions Archive > Retrieve Submission Import Results

#### Retrieve Submission Metadata Mapping

- **Location:** `veevavault/services/applications/rim_submissions_archive/rim_submissions_archive_service.py`
- **Function:** `retrieve_submission_metadata_mapping`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** RIM Submissions Archive > Retrieve Submission Metadata Mapping

#### Update Submission Metadata Mapping

- **Location:** `veevavault/services/applications/rim_submissions_archive/rim_submissions_archive_service.py`
- **Function:** `update_submission_metadata_mapping`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** RIM Submissions Archive > Update Submission Metadata Mapping

#### Remove Submission

- **Location:** `veevavault/services/applications/rim_submissions_archive/rim_submissions_archive_service.py`
- **Function:** `remove_submission`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** RIM Submissions Archive > Remove Submission

#### Cancel Submission

- **Location:** `veevavault/services/applications/rim_submissions_archive/rim_submissions_archive_service.py`
- **Function:** `cancel_submission`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** RIM Submissions Archive > Cancel Submission

#### Export Submission

- **Location:** `veevavault/services/applications/rim_submissions_archive/rim_submissions_archive_service.py`
- **Function:** `export_submission`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** RIM Submissions Archive > Export Submission

#### Export Partial Submission

- **Location:** `veevavault/services/applications/rim_submissions_archive/rim_submissions_archive_service.py`
- **Function:** `export_partial_submission`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** RIM Submissions Archive > Export Partial Submission

#### Retrieve Submission Export Results

- **Location:** `veevavault/services/applications/rim_submissions_archive/rim_submissions_archive_service.py`
- **Function:** `retrieve_submission_export_results`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** RIM Submissions Archive > Retrieve Submission Export Results

## RIM Submissions

### Copy into Content Plan

- **Location:** `veevavault/services/applications/rim_submissions/rim_submissions_service.py`
- **Function:** `copy_into_content_plan`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** RIM Submissions > Copy into Content Plan

## Safety

### Intake Inbox Item

- **Location:** `veevavault/services/applications/safety/safety_service.py`
- **Function:** `intake_inbox_item`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Safety > Intake > Intake Inbox Item

#### Intake Imported Case

- **Location:** `veevavault/services/applications/safety/safety_service.py`
- **Function:** `intake_imported_case`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Safety > Intake > Intake Imported Case

#### Retrieve Intake Status

- **Location:** `veevavault/services/applications/safety/safety_service.py`
- **Function:** `retrieve_intake_status`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Safety > Intake > Retrieve Intake Status

#### Retrieve ACK

- **Location:** `veevavault/services/applications/safety/safety_service.py`
- **Function:** `retrieve_ack`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Safety > Intake > Retrieve ACK

#### Intake JSON

- **Location:** `veevavault/services/applications/safety/safety_service.py`
- **Function:** `intake_json`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Safety > Intake JSON

#### Import Narrative

- **Location:** `veevavault/services/applications/safety/safety_service.py`
- **Function:** `import_narrative`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Safety > Import Narrative

#### Bulk Import Narrative

- **Location:** `veevavault/services/applications/safety/safety_service.py`
- **Function:** `bulk_import_narrative`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Safety > Bulk Import Narrative

#### Retrieve Bulk Import Status

- **Location:** `veevavault/services/applications/safety/safety_service.py`
- **Function:** `retrieve_bulk_import_status`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Safety > Retrieve Bulk Import Status

## Veeva SiteVault

### Create User

- **Location:** `veevavault/services/applications/site_vault/site_vault_service.py`
- **Function:** `create_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Veeva SiteVault > Users > Create User

#### Edit User

- **Location:** `veevavault/services/applications/site_vault/site_vault_service.py`
- **Function:** `edit_user`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Veeva SiteVault > Users > Edit User

#### Retrieve Documents and Signatories

- **Location:** `veevavault/services/applications/site_vault/site_vault_service.py`
- **Function:** `retrieve_documents_and_signatories`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Veeva SiteVault > Veeva eConsent > Retrieve Documents and Signatories

#### Send Documents to Signatories

- **Location:** `veevavault/services/applications/site_vault/site_vault_service.py`
- **Function:** `send_documents_to_signatories`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Veeva SiteVault > Veeva eConsent > Send Documents to Signatories

## File Staging

### List Items at a Path

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `list_items_at_path`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > List Items at a Path

### Download Item Content

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `download_item_content`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > Download Item Content

### Create Folder or File

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `create_folder_or_file`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > Create Folder or File

### Update Folder or File

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `update_folder_or_file`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > Update Folder or File

### Delete File or Folder

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `delete_file_or_folder`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > Delete File or Folder

### Resumable Upload Sessions

##### Create Resumable Upload Session

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `create_resumable_upload_session`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > Resumable Upload Sessions > Create Resumable Upload Session

##### Upload to a Session

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `upload_to_session`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > Resumable Upload Sessions > Upload to a Session

##### Commit Upload Session

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `commit_upload_session`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > Resumable Upload Sessions > Commit Upload Session

##### List Upload Sessions

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `list_upload_sessions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > Resumable Upload Sessions > List Upload Sessions

##### Get Upload Session Details

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `get_upload_session_details`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > Resumable Upload Sessions > Get Upload Session Details

##### List File Parts Uploaded to Session

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `list_file_parts_uploaded_to_session`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > Resumable Upload Sessions > List File Parts Uploaded to Session

##### Abort Upload Session

- **Location:** `veevavault/services/file_staging/file_staging.py`
- **Function:** `abort_upload_session`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** File Staging > Resumable Upload Sessions > Abort Upload Session

## Vault Loader

### Multi-File Extract

#### Extract Data Files

- **Location:** `veevavault/services/vault_loader/vault_loader.py`
- **Function:** `extract_data_files`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Vault Loader > Multi-File Extract > Extract Data Files

##### Retrieve Loader Extract Results

- **Location:** `veevavault/services/vault_loader/vault_loader.py`
- **Function:** `retrieve_loader_extract_results`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Vault Loader > Multi-File Extract > Retrieve Loader Extract Results

##### Retrieve Loader Extract Renditions Results

- **Location:** `veevavault/services/vault_loader/vault_loader.py`
- **Function:** `retrieve_loader_extract_renditions_results`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Vault Loader > Multi-File Extract > Retrieve Loader Extract Renditions Results

### Multi-File Load

##### Load Data Objects

- **Location:** `veevavault/services/vault_loader/vault_loader.py`
- **Function:** `load_data_objects`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Vault Loader > Multi-File Load > Load Data Objects

##### Retrieve Load Success Log Results

- **Location:** `veevavault/services/vault_loader/vault_loader.py`
- **Function:** `retrieve_load_success_log`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Vault Loader > Multi-File Load > Retrieve Load Success Log Results

##### Retrieve Load Failure Log Results

- **Location:** `veevavault/services/vault_loader/vault_loader.py`
- **Function:** `retrieve_load_failure_log`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Vault Loader > Multi-File Load > Retrieve Load Failure Log Results

## Jobs

### Retrieve Job Status

- **Location:** `veevavault/services/jobs/jobs.py`
- **Function:** `retrieve_job_status`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Jobs > Retrieve Job Status

#### Retrieve SDK Job Tasks

- **Location:** `veevavault/services/jobs/jobs.py`
- **Function:** `retrieve_sdk_job_tasks`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Jobs > Retrieve SDK Job Tasks

#### Retrieve Job Histories

- **Location:** `veevavault/services/jobs/jobs.py`
- **Function:** `retrieve_job_histories`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Jobs > Retrieve Job Histories

### Retrieve Job Monitors

- **Location:** `veevavault/services/jobs/jobs.py`
- **Function:** `retrieve_job_monitors`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Jobs > Retrieve Job Monitors

### Start Job

- **Location:** `veevavault/services/jobs/jobs.py`
- **Function:** `start_job`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Jobs > Start Job

## Logs

### Audit

#### Retrieve Audit Types

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `retrieve_audit_types`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > Audit > Retrieve Audit Types

#### Retrieve Audit Metadata

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `retrieve_audit_metadata`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > Audit > Retrieve Audit Metadata

#### Retrieve Audit Details

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `retrieve_audit_details`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > Audit > Retrieve Audit Details

### Audit History

##### Retrieve Complete Audit History for a Single Document

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `retrieve_document_audit_history`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > Audit History > Retrieve Complete Audit History for a Single Document

##### Retrieve Complete Audit History for a Single Object Record

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `retrieve_object_audit_history`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > Audit History > Retrieve Complete Audit History for a Single Object Record

#### SDK Debug Log

##### Retrieve All Debug Logs

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `retrieve_all_debug_logs`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Debug Log > Retrieve All Debug Logs

##### Retrieve Single Debug Log

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `retrieve_single_debug_log`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Debug Log > Retrieve Single Debug Log

##### Download Debug Log Files

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `download_debug_log_files`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Debug Log > Download Debug Log Files

##### Create Debug Log

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `create_debug_log`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Debug Log > Create Debug Log

##### Reset Debug Log

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `reset_debug_log`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Debug Log > Reset Debug Log

##### Delete Debug Log

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `delete_debug_log`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Debug Log > Delete Debug Log

#### SDK Request Profiler

##### Retrieve All Profiling Sessions

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `retrieve_all_profiling_sessions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Request Profiler > Retrieve All Profiling Sessions

##### Retrieve Profiling Session

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `retrieve_profiling_session`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Request Profiler > Retrieve Profiling Session

##### Create Profiling Session

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `create_profiling_session`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Request Profiler > Create Profiling Session

##### End Profiling Session

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `end_profiling_session`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Request Profiler > End Profiling Session

##### Delete Profiling Session

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `delete_profiling_session`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Request Profiler > Delete Profiling Session

##### Download Profiling Session Results

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `download_profiling_session_results`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > SDK Request Profiler > Download Profiling Session Results

#### Retrieve Email Notification Histories

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `retrieve_email_notification_histories`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > Retrieve Email Notification Histories

#### Download Daily API Usage

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `download_daily_api_usage`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > Download Daily API Usage

#### Download SDK Runtime Log

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `download_sdk_runtime_log`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Logs > Download SDK Runtime Log

## Configuration Migration

### Export Package

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `export_package`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Export Package

### Import Package

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `import_package`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Import Package

### Deploy Package

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `deploy_package`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Deploy Package

### Retrieve Package Deploy Results

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `retrieve_package_deploy_results`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Retrieve Package Deploy Results

### Retrieve Outbound Package Dependencies

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `retrieve_outbound_package_dependencies`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Retrieve Outbound Package Dependencies

### Component Definition Query

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `query_component_definitions`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Component Definition Query

### Vault Compare

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `compare_vaults`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Vault Compare

### Vault Configuration Report

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `generate_configuration_report`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Vault Configuration Report

### Validate Package

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `validate_package`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Validate Package

### Validate Inbound Package

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `validate_inbound_package`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Validate Inbound Package

### Enable Configuration Mode

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `enable_configuration_mode`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Enable Configuration Mode

### Disable Configuration Mode

- **Location:** `veevavault/services/configuration_migration/configuration_migration.py`
- **Function:** `disable_configuration_mode`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Configuration Migration > Disable Configuration Mode

## Sandbox Vaults

### Retrieve Sandboxes

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `retrieve_sandboxes`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Retrieve Sandboxes

### Retrieve Sandbox Details by ID

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `retrieve_sandbox_details`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Retrieve Sandbox Details by ID

### Recheck Sandbox Usage Limit

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `recheck_sandbox_usage_limit`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Recheck Sandbox Usage Limit

### Change Sandbox Size

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `change_sandbox_size`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Change Sandbox Size

### Set Sandbox Entitlements

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `set_sandbox_entitlements`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Set Sandbox Entitlements

### Create or Refresh Sandbox

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `create_or_refresh_sandbox`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Create or Refresh Sandbox

### Refresh Sandbox from Snapshot

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `refresh_sandbox_from_snapshot`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Refresh Sandbox from Snapshot

### Delete Sandbox

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `delete_sandbox`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Delete Sandbox

### Sandbox Snapshots

#### Create Sandbox Snapshot

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `create_sandbox_snapshot`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Sandbox Snapshots > Create Sandbox Snapshot

#### Retrieve Sandbox Snapshots

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `retrieve_sandbox_snapshots`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Sandbox Snapshots > Retrieve Sandbox Snapshots

#### Delete Sandbox Snapshot

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `delete_sandbox_snapshot`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Sandbox Snapshots > Delete Sandbox Snapshot

#### Update Sandbox Snapshot

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `update_sandbox_snapshot`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Sandbox Snapshots > Update Sandbox Snapshot

#### Upgrade Sandbox Snapshot

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `upgrade_sandbox_snapshot`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Sandbox Snapshots > Upgrade Sandbox Snapshot

### Pre-Production Vaults

#### Build Production Vault

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `build_production_vault`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Pre-Production Vaults > Build Production Vault

#### Promote to Production

- **Location:** `veevavault/services/sandbox_vaults/sandbox_vaults.py`
- **Function:** `promote_to_production`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Sandbox Vaults > Pre-Production Vaults > Promote to Production

## Picklists

### Retrieve All Picklists

- **Location:** `veevavault/services/picklists/picklist_service.py`
- **Function:** `retrieve_all_picklists`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Picklists > Retrieve All Picklists

### Retrieve Picklist Values

- **Location:** `veevavault/services/picklists/picklist_service.py`
- **Function:** `retrieve_picklist_values`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Picklists > Retrieve Picklist Values

### Create Picklist Values

- **Location:** `veevavault/services/picklists/picklist_service.py`
- **Function:** `create_picklist_values`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Picklists > Create Picklist Values

### Update Picklist Value Label

- **Location:** `veevavault/services/picklists/picklist_service.py`
- **Function:** `update_picklist_value_label`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Picklists > Update Picklist Value Label

### Update Picklist Value

- **Location:** `veevavault/services/picklists/picklist_service.py`
- **Function:** `update_picklist_value`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Picklists > Update Picklist Value

### Inactivate Picklist Value

- **Location:** `veevavault/services/picklists/picklist_service.py`
- **Function:** `inactivate_picklist_value`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Picklists > Inactivate Picklist Value

## Expected Document Lists

### Create a Placeholder from an EDL Item

- **Location:** `veevavault/services/edl/edl.py`
- **Function:** `create_placeholder_from_edl_item`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Expected Document Lists > Create a Placeholder from an EDL Item

### Retrieve All Root Nodes

- **Location:** `veevavault/services/edl/edl.py`
- **Function:** `retrieve_all_root_nodes`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Expected Document Lists > Retrieve All Root Nodes

### Retrieve Specific Root Nodes

- **Location:** `veevavault/services/edl/edl.py`
- **Function:** `retrieve_specific_root_nodes`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Expected Document Lists > Retrieve Specific Root Nodes

### Retrieve a Node's Children

- **Location:** `veevavault/services/edl/edl.py`
- **Function:** `retrieve_node_children`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Expected Document Lists > Retrieve a Node's Children

### Update Node Order

- **Location:** `veevavault/services/edl/edl.py`
- **Function:** `update_node_order`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Expected Document Lists > Update Node Order

### Add EDL Matched Documents

- **Location:** `veevavault/services/edl/edl.py`
- **Function:** `add_edl_matched_documents`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Expected Document Lists > Add EDL Matched Documents

### Remove EDL Matched Documents

- **Location:** `veevavault/services/edl/edl.py`
- **Function:** `remove_edl_matched_documents`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Expected Document Lists > Remove EDL Matched Documents

## Security Policies

### Retrieve Security Policy Metadata

- **Location:** `veevavault/services/security_policies/security_policies.py`
- **Function:** `retrieve_security_policy_metadata`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Security Policies > Retrieve Security Policy Metadata

### Retrieve All Security Policies

- **Location:** `veevavault/services/security_policies/security_policies.py`
- **Function:** `retrieve_all_security_policies`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Security Policies > Retrieve All Security Policies

### Retrieve Security Policy

- **Location:** `veevavault/services/security_policies/security_policies.py`
- **Function:** `retrieve_security_policy`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Security Policies > Retrieve Security Policy

## Domain Information

### Retrieve Domain Information

- **Location:** `veevavault/services/domains/domain.py`
- **Function:** `retrieve_domain_information`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Domain Information > Retrieve Domain Information

### Retrieve Domains

- **Location:** `veevavault/services/domains/domain.py`
- **Function:** `retrieve_domains`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Domain Information > Retrieve Domains

## Bulk Translation

### Export Bulk Translation File

- **Location:** `veevavault/services/bulk_translation/bulk_translation.py`
- **Function:** `export_bulk_translation_file`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Bulk Translation > Export Bulk Translation File

### Import Bulk Translation File

- **Location:** `veevavault/services/bulk_translation/bulk_translation.py`
- **Function:** `import_bulk_translation_file`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Bulk Translation > Import Bulk Translation File

### Retrieve Import Bulk Translation File Job Summary

- **Location:** `veevavault/services/bulk_translation/bulk_translation.py`
- **Function:** `retrieve_bulk_translation_import_summary`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Bulk Translation > Retrieve Import Bulk Translation File Job Summary

### Retrieve Import Bulk Translation File Job Errors

- **Location:** `veevavault/services/bulk_translation/bulk_translation.py`
- **Function:** `retrieve_bulk_translation_import_errors`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Bulk Translation > Retrieve Import Bulk Translation File Job Errors

## Managing Vault Java SDK

### Retrieve Single Source Code File

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `retrieve_source_code_file`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Retrieve Single Source Code File

### Enable Vault Extension

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `enable_vault_extension`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Enable Vault Extension

### Disable Vault Extension

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `disable_vault_extension`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Disable Vault Extension

### Add or Replace Single Source Code File

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `add_or_replace_source_code_file`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Add or Replace Single Source Code File

### Delete Single Source Code File

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `delete_source_code_file`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Delete Single Source Code File

### Validate Imported Package

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `validate_imported_package`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Validate Imported Package

### Retrieve Signing Certificate

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `retrieve_signing_certificate`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Retrieve Signing Certificate

### Queues

#### Retrieve All Queues

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `retrieve_all_queues`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Queues > Retrieve All Queues

#### Retrieve Queue Status

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `retrieve_queue_status`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Queues > Retrieve Queue Status

#### Disable Delivery

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `disable_delivery`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Queues > Disable Delivery

#### Enable Delivery

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `enable_delivery`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Queues > Enable Delivery

#### Reset Queue

- **Location:** `veevavault/services/vault_java_sdk/vault_java_sdk.py`
- **Function:** `reset_queue`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Managing Vault Java SDK > Queues > Reset Queue

## Custom Pages

### Retrieve All Client Code Distribution Metadata

- **Location:** `veevavault/services/custom_pages/custom_pages.py`
- **Function:** `retrieve_all_client_code_distribution_metadata`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Custom Pages > Retrieve All Client Code Distribution Metadata

### Retrieve Single Client Code Distribution Metadata

- **Location:** `veevavault/services/custom_pages/custom_pages.py`
- **Function:** `retrieve_single_client_code_distribution_metadata`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Custom Pages > Retrieve Single Client Code Distribution Metadata

### Download Single Client Code Distribution

- **Location:** `veevavault/services/custom_pages/custom_pages.py`
- **Function:** `download_single_client_code_distribution`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Custom Pages > Download Single Client Code Distribution

### Add or Replace Single Client Code Distribution

- **Location:** `veevavault/services/custom_pages/custom_pages.py`
- **Function:** `add_or_replace_single_client_code_distribution`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Custom Pages > Add or Replace Single Client Code Distribution

### Delete Single Client Code Distribution

- **Location:** `veevavault/services/custom_pages/custom_pages.py`
- **Function:** `delete_single_client_code_distribution`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Custom Pages > Delete Single Client Code Distribution

## RIM Submissions Archive

### Download Exported Submission Files via File Staging

- **Location:** `veevavault/services/applications/rim_submissions_archive/rim_submissions_archive_service.py`
- **Function:** `download_exported_submission_files`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** RIM Submissions Archive > Download Exported Submission Files via File Staging

## Errors

### Error Types

- **Location:** `veevavault/services/logs/logs.py`
- **Function:** `retrieve_error_types`
- **Updates Made:**
    - No updates needed. Implementation is accurate and compliant.
- **State:** Compliant with API documentation.
- **Section:** Errors > Error Types
