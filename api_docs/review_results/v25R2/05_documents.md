<!-- 
ReviewResults Section: ## Documents
API Section Match: 05_documents.md
Original Line Number: 606
API Version: v25R2
Generated: August 30, 2025
-->

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
