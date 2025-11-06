import pandas as pd
import requests
import json
from .base_service import BaseObjectService
from .metadata_service import ObjectMetadataService
from .crud_service import ObjectCRUDService
from .collection_service import ObjectCollectionService
from .rollup_service import ObjectRollupService
from .merge_service import ObjectMergeService
from .types_service import ObjectTypesService
from .roles_service import ObjectRolesService
from .attachments_service import ObjectAttachmentsService
from .layouts_service import ObjectLayoutsService
from .attachment_fields_service import ObjectAttachmentFieldsService
from .actions_service import ObjectActionsService


class ObjectService:
    """
    Main service class for handling Veeva Vault object operations.
    This class aggregates all specialized object service classes.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance
        """
        self.client = client

        # Initialize specialized services
        self.metadata = ObjectMetadataService(client)
        self.crud = ObjectCRUDService(client)
        self.collection = ObjectCollectionService(client)
        self.rollup = ObjectRollupService(client)
        self.merge = ObjectMergeService(client)
        self.types = ObjectTypesService(client)
        self.roles = ObjectRolesService(client)
        self.attachments = ObjectAttachmentsService(client)
        self.layouts = ObjectLayoutsService(client)
        self.attachment_fields = ObjectAttachmentFieldsService(client)
        self.actions = ObjectActionsService(client)

    # ===================================================================
    # Convenience methods that directly call methods on specialized services
    # These are kept for backward compatibility and ease of use
    # ===================================================================

    # ------ Metadata Operations ------

    def retrieve_object_metadata(self, object_name, loc=False):
        """
        Retrieves detailed metadata for a specific object.

        GET /api/{version}/metadata/vobjects/{object_name}

        Args:
            object_name (str): API name of the object
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: Object metadata including fields, relationships, and configurations such as
                 allow_attachments, auditable, role_overrides, system_managed, etc.
        """
        return self.metadata.retrieve_object_metadata(object_name, loc)

    def retrieve_object_field_metadata(self, object_name, object_field_name, loc=False):
        """
        Retrieves detailed metadata for a specific field on an object.

        GET /api/{version}/metadata/vobjects/{object_name}/fields/{object_field_name}

        Args:
            object_name (str): API name of the object
            object_field_name (str): API name of the field
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: Field metadata including type, required status, editable, facetable, etc.
                 Important metadata includes:
                 - required: When true, field value must be set when creating records
                 - editable: When true, field value can be defined by the user
                 - no_copy: When true, field values are not copied when using Make a Copy
                 - facetable: When true, field is available for faceted filtering
                 - format_mask: The format mask expression if it exists on the field
                 - rollup: When true, this field is a Roll-up field
        """
        return self.metadata.retrieve_object_field_metadata(
            object_name, object_field_name, loc
        )

    def retrieve_object_collection(self, loc=False):
        """
        Retrieves a list of all objects in the vault.

        GET /api/{version}/metadata/vobjects

        Args:
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: Collection of all objects with summary information including url, label,
                 name, prefix, status, and configuration_state for each object
        """
        return self.metadata.retrieve_object_collection(loc)

    def describe_objects(self):
        """
        Retrieves metadata about all available objects in the Vault.

        GET /api/{version}/metadata/vobjects

        Returns:
            pandas.DataFrame: A DataFrame containing object metadata sorted by name
        """
        return self.metadata.describe_objects()

    def object_field_metadata(self, object_api_name):
        """
        Retrieves metadata about the fields of a specific object.

        GET /api/{version}/metadata/vobjects/{object_name}

        Args:
            object_api_name (str): API name of the object

        Returns:
            pandas.DataFrame: A DataFrame containing field metadata
        """
        return self.metadata.object_field_metadata(object_api_name)

    # ------ Object Record Collection Operations ------

    def retrieve_object_record_collection(
        self, object_name, fields=None, limit=None, offset=None, sort=None
    ):
        """
        Retrieves a collection of records for a specific object.

        GET /api/{version}/vobjects/{object_name}

        Args:
            object_name (str): API name of the object
            fields (list): List of field names to include in the response
            limit (int): Maximum number of records to return (max 200)
            offset (int): Starting position for record retrieval (for pagination)
            sort (str): Field name to sort by with optional direction (e.g., "name__v:desc")

        Returns:
            dict: Collection of object records with metadata and data sections
                 The response includes the object metadata and the id and name__v of all records
                 By default, Vault returns a maximum of 200 records per page
        """
        return self.collection.retrieve_object_record_collection(
            object_name, fields, limit, offset, sort
        )

    # ------ Object Record Operations ------

    def retrieve_object_record(self, object_name, object_record_id):
        """
        Retrieves a specific object record by ID.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the record to retrieve

        Returns:
            dict: Object record data with all fields and values configured on the record
                 When Custom Sharing Rules are enabled on the object, the response includes
                 manually_assigned_sharing_roles with owner__v, viewer__v, and editor__v information
        """
        return self.crud.retrieve_object_record(object_name, object_record_id)

    # ------ Create & Update Operations ------

    def create_object_records(
        self,
        object_name,
        data,
        content_type="text/csv",
        accept="text/csv",
        additional_headers=None,
    ):
        """
        Creates new object records or upserts existing records in bulk.

        POST /api/{version}/vobjects/{object_name}

        Args:
            object_name (str): API name of the object
            data (str or dict): CSV string or JSON data containing the records to create
            content_type (str): Content type of the request (text/csv or application/json)
            accept (str): Expected response format (text/csv or application/json)
            additional_headers (dict): Additional HTTP headers to include such as:
                                      X-VaultAPI-MigrationMode, X-VaultAPI-NoTriggers

        Returns:
            dict or str: API response (JSON or CSV based on accept header)
                        For each record, includes responseStatus and data with id and url

        Notes:
            - Maximum input file size is 50 MB
            - Values must be UTF-8 encoded
            - CSVs must follow RFC 4180 format
            - Maximum batch size is 500
            - Can be used to create User Tasks or User records
            - For upsert operations, add idParam query parameter to identify records by unique field
        """
        return self.crud.create_object_records(
            object_name, data, content_type, accept, additional_headers
        )

    def update_object_records(
        self, object_name, data, id_param=None, migration_mode=None
    ):
        """
        Updates existing object records in bulk.

        PUT /api/{version}/vobjects/{object_name}

        Args:
            object_name (str): API name of the object
            data (str or dict): CSV string or JSON data containing the records to update
            id_param (str): Field name to use as record identifier (if not the default 'id')
            migration_mode (bool): Whether to enable migration mode for the update

        Returns:
            dict or str: API response with status for each record updated

        Notes:
            - Maximum input size is 50 MB
            - Values must be UTF-8 encoded
            - CSVs must follow RFC 4180 format
            - Maximum batch size is 500
            - Can be used to update user records (user__sys)
            - If an object has field defaults, the value provided overrides the default
            - If Dynamic Security is configured, can add/remove users and groups on roles
            - Cannot update parent objects' status__v field in bulk
        """
        return self.crud.update_object_records(
            object_name, data, id_param, migration_mode
        )

    # ------ Delete Operations ------

    def delete_object_records(self, object_name, data, id_param=None):
        """
        Deletes object records in bulk.

        DELETE /api/{version}/vobjects/{object_name}

        Args:
            object_name (str): API name of the object
            data (str or dict): CSV string or JSON data identifying the records to delete
            id_param (str): Field name to use as record identifier (if not the default 'id')

        Returns:
            dict or str: API response with deletion results for each record

        Notes:
            - Maximum input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow RFC 4180 format
            - Maximum batch size is 500
            - Cannot be used to delete user__sys records (use update to set status to inactive)
            - For cascade delete operations, use cascade_delete_object_record
        """
        return self.crud.delete_object_records(object_name, data, id_param)

    def cascade_delete_object_record(self, object_name, object_record_id):
        """
        Performs a cascade delete operation on a single object record.
        This asynchronous endpoint will delete a parent record and all related
        children and grandchildren.

        POST /api/{version}/vobjects/{object_name}/{object_record_id}/actions/cascadedelete

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the record to delete

        Returns:
            dict: API response containing the job ID and URL to check job status
        """
        return self.crud.cascade_delete_object_record(object_name, object_record_id)

    def retrieve_cascade_delete_results(self, object_name, job_status, job_id):
        """
        Retrieves the results of a cascade delete operation.

        GET /api/{version}/vobjects/cascadedelete/results/{object_name}/{job_status}/{job_id}

        Args:
            object_name (str): API name of the object
            job_status (str): Status of the job (e.g., "success", "failure")
            job_id (str): ID of the cascade delete job

        Returns:
            dict: Status and results of the cascade delete operation
                 Response includes Source Object and Record Id information

        Notes:
            - You must have previously requested a cascade delete job that is no longer active
            - You need a valid job_id from the cascade delete response
        """
        return self.crud.retrieve_cascade_delete_results(
            object_name, job_status, job_id
        )

    # ------ Roll-up Fields Operations ------

    def recalculate_rollup_fields(self, object_name, record_id=None, fields=None):
        """
        Recalculates roll-up field values for a specific object record or all roll-up fields
        for the specified object.

        POST /api/{version}/vobjects/{object_name}/actions/recalculaterollups
        OR
        POST /api/{version}/vobjects/{object_name}/{record_id}/actions/rolluprecalculate

        Args:
            object_name (str): API name of the object
            record_id (str, optional): ID of the record to recalculate. If not provided,
                                     all roll-up fields on the object are recalculated.
            fields (list, optional): List of specific roll-up fields to recalculate

        Returns:
            dict: API response with job ID or success message

        Notes:
            - You can configure up to 25 Roll-up fields on a parent object
            - When performing a full recalculation, Vault evaluates all Roll-up fields asynchronously
            - Record triggers on parent records do not fire when Roll-up fields are updated
            - This endpoint is equivalent to the Recalculate Roll-up Fields action in the Vault UI
            - While a recalculation is running, Admins cannot start another recalculation
        """
        return self.rollup.recalculate_rollup_fields(object_name, record_id, fields)

    def retrieve_rollup_field_recalculation_status(self, object_name, job_id=None):
        """
        Retrieves the status of a roll-up field recalculation job.

        GET /api/{version}/vobjects/{object_name}/actions/recalculaterollups
        OR
        GET /api/{version}/vobjects/{object_name}/actions/rolluprecalculate/{job_id}

        Args:
            object_name (str): API name of the object
            job_id (str, optional): ID of the recalculation job. If not provided,
                                   the status of any active recalculation for the object is returned.

        Returns:
            dict: Status of the recalculation job (RUNNING or NOT_RUNNING)
        """
        return self.rollup.retrieve_rollup_field_recalculation_status(
            object_name, job_id
        )

    # ------ Merge Operations ------

    def initiate_record_merge(self, object_name, payload):
        """
        Initiates a merge operation for object records in bulk.

        POST /api/{version}/vobjects/{object_name}/actions/merge

        Args:
            object_name (str): API name of the object
            payload (dict or list): Merge configuration containing source and target records
                                   Each merge set requires:
                                   - duplicate_record_id: ID of record to be merged and deleted
                                   - main_record_id: ID of record that will remain

        Returns:
            dict: API response with job ID

        Notes:
            - The values in the input must be UTF-8 encoded
            - Maximum batch size is 10 merge sets
            - Maximum concurrent merge requests is 500
            - The object must have Enable Merges configured
            - The initiating user must have proper permissions
            - When merging records, inbound references from other objects pointing to the
              duplicate record are moved to the main record
            - Field values on the main record are not changed
            - When the process is complete, the duplicate record is deleted
            - Record merges do not trigger record triggers
        """
        return self.merge.initiate_record_merge(object_name, payload)

    def retrieve_record_merge_status(self, object_name, job_id):
        """
        Retrieves the status of a record merge job.

        GET /api/{version}/vobjects/merges/{job_id}/status

        Args:
            object_name (str): API name of the object
            job_id (str): ID of the merge job

        Returns:
            dict: Status of the merge job (IN_PROGRESS, SUCCESS, or FAILURE)

        Notes:
            - You must have previously requested a record merge job
            - You need a valid job_id value returned from the record merge operation
        """
        return self.merge.retrieve_record_merge_status(object_name, job_id)

    def retrieve_record_merge_results(self, object_name, job_id):
        """
        Retrieves the results of a completed merge job.

        GET /api/{version}/vobjects/merges/{job_id}/results

        Args:
            object_name (str): API name of the object
            job_id (str): ID of the completed merge job

        Returns:
            dict: Results of the merge job including status for each merge set
                 For FAILURE status, may include error types:
                 - INVALID_DATA: The merge was not attempted
                 - PROCESSING_ERROR: The merge was attempted but failed during processing

        Notes:
            - You must have previously requested a record merge job which is no longer IN_PROGRESS
            - You need a valid job_id value returned from the record merge operation
        """
        return self.merge.retrieve_record_merge_results(object_name, job_id)

    def download_merge_records_job_log(self, object_name, job_id, file_path):
        """
        Downloads the log file for a merge job.

        GET /api/{version}/vobjects/merges/{job_id}/log

        Args:
            object_name (str): API name of the object
            job_id (str): ID of the merge job
            file_path (str): Local path where the log file will be saved

        Returns:
            str: Message indicating successful download

        Notes:
            - You must have previously requested a record merge job which is no longer IN_PROGRESS
            - The same log is available for download through the Vault UI from Admin > Operations > Job Status
            - The merge record job history log contains information about the merge, such as start and
              completion times, relationship processing, attachment processing, etc.
        """
        return self.merge.download_merge_records_job_log(object_name, job_id, file_path)

    # ------ Object Types Operations ------

    def retrieve_details_from_all_object_types(self):
        """
        Retrieves details from all object types. Lists all object types and all fields configured on each object type.

        GET /api/{version}/configuration/Objecttype

        Returns:
            dict: Information about all object types and their configured fields
        """
        return self.types.retrieve_details_from_all_object_types()

    def retrieve_details_from_specific_object(self, object_name_and_object_type):
        """
        Retrieves details from a specific object. Lists all object types and all fields configured
        on each object type for the specified object.

        GET /api/{version}/configuration/{object_name_and_object_type}

        Args:
            object_name_and_object_type (str): The object name followed by the object type in the format
                                            Objecttype.{object_name}.{object_type}

        Returns:
            dict: Information about object types and configured fields for the specific object
        """
        return self.types.retrieve_details_from_specific_object(
            object_name_and_object_type
        )

    def change_object_type(self, object_name, payload):
        """
        Changes the object types assigned to object records. Field values which exist on both the original
        and new object type will carry over to the new type. All other field values will be removed.

        POST /api/{version}/vobjects/{object_name}/actions/changetype

        Args:
            object_name (str): The name of the object
            payload (dict): A dictionary containing at least the "id" and "object_type__v" keys

        Returns:
            dict: Result of the change object type operation

        Notes:
            - Maximum input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow standard format
            - Maximum batch size is 500
            - Any field values that exist on both original and new object type carry over
            - Field values unique to the original type are removed
        """
        return self.types.change_object_type(object_name, payload)

    # ------ Object Roles Operations ------

    def retrieve_object_record_roles(self, object_name, record_id, role_name=None):
        """
        Retrieves the roles assigned to an object record.

        GET /api/{version}/vobjects/{object_name}/{id}/roles{/role_name}

        Args:
            object_name (str): API name of the object
            record_id (str): ID of the record
            role_name (str, optional): Name of a specific role to retrieve (e.g., "owner__v")

        Returns:
            dict: Information about roles assigned to the record, including users and groups
                 assigned to each role and the assignment_type

        Notes:
            - Standard roles include owner__v, viewer__v, and editor__v
            - Admins can create custom roles defined per lifecycle
            - Even though owner__v role is automatically assigned when applying Custom Sharing Rules,
              the assignment_type for roles on objects is always manual_assignment
        """
        return self.roles.retrieve_object_record_roles(
            object_name, record_id, role_name
        )

    def assign_users_groups_to_roles_on_object_records(self, object_name, request_body):
        """
        Assigns users and groups to roles on object records in bulk.

        POST /api/{version}/vobjects/{object_name}/roles

        Args:
            object_name (str): API name of the object
            request_body (dict): JSON structure specifying role assignments

        Returns:
            dict: Result of the role assignment operation

        Notes:
            - Maximum CSV input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow RFC 4180 format
            - Maximum batch size is 500
            - Assigning users and groups to roles is additive, and duplicate groups are ignored
            - User and group assignments are ignored if they are invalid, inactive, or already exist
        """
        return self.roles.assign_users_groups_to_roles_on_object_records(
            object_name, request_body
        )

    def remove_users_groups_from_roles_on_object_records(
        self, object_name, request_body
    ):
        """
        Removes users and groups from roles on object records in bulk.

        DELETE /api/{version}/vobjects/{object_name}/roles

        Args:
            object_name (str): API name of the object
            request_body (dict): JSON structure specifying role assignments to remove

        Returns:
            dict: Result of the role removal operation

        Notes:
            - Maximum CSV input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow RFC 4180 format
            - Maximum batch size is 500
            - Users and groups are ignored if they are invalid or inactive
        """
        return self.roles.remove_users_groups_from_roles_on_object_records(
            object_name, request_body
        )

    # ------ Object Attachments Operations ------

    def determine_if_attachments_are_enabled_on_an_object(self, object_name):
        """
        Determines if attachments are enabled on a specific object.

        GET /api/{version}/metadata/vobjects/{object_name}

        Args:
            object_name (str): The value of object name__v field

        Returns:
            dict: Object metadata which includes the "allow_attachments" property and
                 "attachments" in the list of urls when attachments are enabled
        """
        return self.attachments.determine_if_attachments_are_enabled_on_an_object(
            object_name
        )

    def retrieve_object_record_attachments(self, object_name, object_record_id):
        """
        Retrieves a list of all attachments on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value

        Returns:
            dict: List of attachments and their details including filename, format, size,
                 md5checksum, version, creation information, and version history

        Notes:
            - Attachment versioning uses integer numbers beginning with 1 and incrementing sequentially
            - There is no concept of major or minor version numbers with attachments
        """
        return self.attachments.retrieve_object_record_attachments(
            object_name, object_record_id
        )

    def retrieve_object_record_attachment_metadata(
        self, object_name, object_record_id, attachment_id
    ):
        """
        Retrieves the metadata of a specific attachment on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value

        Returns:
            dict: Metadata details of the specified attachment including filename, description,
                 format, size, md5checksum, version, creation information, and version history

        Notes:
            - The md5checksum__v field is calculated on the latest version of the attachment
            - If an attachment is added with the same MD5 checksum as an existing attachment,
              the new attachment is not added
        """
        return self.attachments.retrieve_object_record_attachment_metadata(
            object_name, object_record_id, attachment_id
        )

    def retrieve_object_record_attachment_versions(
        self, object_name, object_record_id, attachment_id
    ):
        """
        Retrieves all versions of a specific attachment on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value

        Returns:
            dict: Version details of the specified attachment, listing all available versions
                 with their version numbers and URLs
        """
        return self.attachments.retrieve_object_record_attachment_versions(
            object_name, object_record_id, attachment_id
        )

    def retrieve_object_record_attachment_version_metadata(
        self, object_name, object_record_id, attachment_id, attachment_version
    ):
        """
        Retrieves the metadata of a specific version of an attachment on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            attachment_version (str): The attachment version__v field value

        Returns:
            dict: Metadata of the specified attachment version including filename, format, size,
                 md5checksum, version, and creation information
        """
        return self.attachments.retrieve_object_record_attachment_version_metadata(
            object_name, object_record_id, attachment_id, attachment_version
        )

    def download_object_record_attachment_file(
        self, object_name, object_record_id, attachment_id, file_path
    ):
        """
        Downloads the file of a specific attachment on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/file

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            file_path (str): Local path where the file will be saved

        Returns:
            str: Message indicating successful download

        Notes:
            - Downloads the latest version of the specified attachment
            - The Content-Type header is set to the MIME type of the file
            - If MIME type cannot be detected, Content-Type is set to application/octet-stream
            - The Content-Disposition header contains a filename component for naming the local file
        """
        return self.attachments.download_object_record_attachment_file(
            object_name, object_record_id, attachment_id, file_path
        )

    def download_object_record_attachment_version_file(
        self,
        object_name,
        object_record_id,
        attachment_id,
        attachment_version,
        file_path,
    ):
        """
        Downloads a specific version of an attachment file from a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}/file

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            attachment_version (str): The attachment version__v field value
            file_path (str): Local path where the file will be saved

        Returns:
            str: Message indicating successful download

        Notes:
            - The file name is the same as the attachment file name
            - The Content-Type header is set to the MIME type of the file
            - If MIME type cannot be detected, Content-Type is set to application/octet-stream
            - The Content-Disposition header contains a filename component for naming the local file
        """
        return self.attachments.download_object_record_attachment_version_file(
            object_name, object_record_id, attachment_id, attachment_version, file_path
        )

    def retrieve_deleted_object_record_attachments(self, object_name, start_date=None, end_date=None, name_filter=None, id_token=None):
        """
        Retrieves all deleted object record attachments.

        GET /api/{version}/objects/deletions/vobjects/{object_name}/attachments

        Args:
            object_name (str): The object name__v field value
            start_date (str, optional): Start date for filtering results (ISO format)
            end_date (str, optional): End date for filtering results (ISO format)
            name_filter (str, optional): Name filter for attachment names
            id_token (str, optional): Security token string for specific deleted attachment

        Returns:
            dict: List of deleted attachments with details including deletion information

        Notes:
            - After object record attachments are deleted, their information is available for retrieval for 30 days
            - Can use optional query parameters to narrow results to specific date/time ranges
            - Dates and times are in UTC
        """
        return self.attachments.retrieve_deleted_object_record_attachments(object_name, start_date, end_date, name_filter, id_token)

    def create_object_record_attachment(self, object_name, object_record_id, file_path, description=None):
        """
        Creates a new attachment for an object record.

        POST /api/{version}/vobjects/{object_name}/{object_record_id}/attachments

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            file_path (str): Path to the file to attach
            description (str, optional): Description for the attachment

        Returns:
            dict: Response from the API with attachment details including id and version

        Notes:
            - If the attachment already exists, Vault uploads it as a new version of the existing attachment
            - Maximum allowed file size is 4GB
            - The following attributes are determined based on the file: filename__v, format__v, size__v
            - If an attachment with the same filename already exists, it's added as a new version
            - If an attachment with the same MD5 checksum exists, the new attachment is not added
        """
        return self.attachments.create_object_record_attachment(object_name, object_record_id, file_path, description)

    def create_multiple_object_record_attachments(self, object_name, staged_files_payload):
        """
        Creates multiple object record attachments in bulk via staging.

        POST /api/{version}/vobjects/{object_name}/attachments/batch

        Args:
            object_name (str): The object name__v field value
            staged_files_payload (dict): Payload containing the staged file information

        Returns:
            dict: Response from the API with attachment details

        Notes:
            - Maximum input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow standard format
            - Maximum batch size is 500
            - If an attachment with the same name already exists, it's added as a new version
            - Maximum allowed file size for attachments is 100 MB
        """
        return self.attachments.create_multiple_object_record_attachments(object_name, staged_files_payload)

    def restore_object_record_attachment_version(self, object_name, object_record_id, attachment_id, version_number):
        """
        Restores a previous version of an attachment.

        POST /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}?restore=true

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            version_number (str): The version number to restore

        Returns:
            dict: Response from the API with restoration details including id and version
        """
        return self.attachments.restore_object_record_attachment_version(object_name, object_record_id, attachment_id, version_number)

    def update_object_record_attachment_description(self, object_name, object_record_id, attachment_id, description):
        """
        Updates the description of an attachment.

        PUT /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            description (str): New description for the attachment

        Returns:
            dict: Response from the API with update details

        Notes:
            - Description is the only editable field for attachments
            - Maximum length for description is 1000 characters
        """
        return self.attachments.update_object_record_attachment_description(object_name, object_record_id, attachment_id, description)

    def update_multiple_object_record_attachment_descriptions(self, object_name, descriptions_payload):
        """
        Updates descriptions for multiple attachments in bulk.

        PUT /api/{version}/vobjects/{object_name}/attachments/batch

        Args:
            object_name (str): The object name__v field value
            descriptions_payload (dict): Payload containing attachment update information

        Returns:
            dict: Response from the API with update details

        Notes:
            - Maximum input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow standard format
            - Maximum batch size is 500
            - Can only update the latest version of an attachment
        """
        return self.attachments.update_multiple_object_record_attachment_descriptions(object_name, descriptions_payload)

    def delete_object_record_attachment(self, object_name, object_record_id, attachment_id):
        """
        Deletes an attachment (latest version and history) from an object record.

        DELETE /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value

        Returns:
            dict: Response from the API with deletion details
        """
        return self.attachments.delete_object_record_attachment(object_name, object_record_id, attachment_id)

    def delete_multiple_object_record_attachments(self, object_name, attachments_payload):
        """
        Deletes multiple attachments in bulk.

        DELETE /api/{version}/vobjects/{object_name}/attachments/batch

        Args:
            object_name (str): The object name__v field value
            attachments_payload (dict): Payload containing attachment deletion information

        Returns:
            dict: Response from the API with deletion details

        Notes:
            - Maximum input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow standard format
            - Maximum batch size is 500
        """
        return self.attachments.delete_multiple_object_record_attachments(object_name, attachments_payload)

    def delete_object_record_attachment_version(self, object_name, object_record_id, attachment_id, version_number):
        """
        Deletes a specific version of an attachment from an object record.

        DELETE /api/{version}/vobjects/{object_name}/{object_record_id}/attachments/{attachment_id}/versions/{attachment_version}

        Args:
            object_name (str): The object name__v field value
            object_record_id (str): The object record id field value
            attachment_id (str): The attachment id field value
            version_number (str): The version number to delete

        Returns:
            dict: Response from the API with deletion details
        """
        return self.attachments.delete_object_record_attachment_version(object_name, object_record_id, attachment_id, version_number)

    # ------ Object Page Layouts Operations ------

    def retrieve_page_layouts(self, object_name):
        """
        Retrieves all page layouts for a specific object.

        GET /api/{version}/metadata/vobjects/{object_name}/page_layouts

        Args:
            object_name (str): API name of the object

        Returns:
            dict: Collection of page layouts for the object including information such as
                 name, label, object_type, active status, description, default_layout status,
                 and display_lifecycle_stages setting

        Notes:
            - Object page layouts are defined at the object or object-type level
            - Objects with multiple object types can define a different layout for each type
        """
        return self.layouts.retrieve_page_layouts(object_name)

    def retrieve_page_layout_metadata(self, object_name, layout_name):
        """
        Retrieves detailed metadata for a specific page layout.

        GET /api/{version}/metadata/vobjects/{object_name}/page_layouts/{layout_name}

        Args:
            object_name (str): API name of the object
            layout_name (str): Name of the page layout

        Returns:
            dict: Detailed metadata for the page layout including sections, fields, layout rules,
                 and configuration details

        Notes:
            - The page layout APIs consider the authenticated user's permissions
            - Fields hidden from the user will not be included in the API response
            - Layout rules are not applied, but returned as metadata
            - Both active and inactive fields are included in the response
        """
        return self.layouts.retrieve_page_layout_metadata(object_name, layout_name)

    # ------ Attachment Fields Operations ------

    def download_attachment_field_file(
        self, object_name, object_record_id, field_name, file_path
    ):
        """
        Downloads the file stored in an attachment field.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachment_fields/{attachment_field_name}/file

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the record
            field_name (str): API name of the attachment field
            file_path (str): Local path where the file will be saved

        Returns:
            str: Message indicating successful download

        Notes:
            - The Content-Type header is set to the MIME type of the file
            - If MIME type cannot be detected, Content-Type is set to application/octet-stream
            - The Content-Disposition header contains a filename component for naming the local file
        """
        return self.attachment_fields.download_attachment_field_file(
            object_name, object_record_id, field_name, file_path
        )

    def download_all_attachment_field_files(
        self, object_name, object_record_id, directory_path
    ):
        """
        Downloads all files stored in attachment fields for a specific record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/attachment_fields/file

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the record
            directory_path (str): Local directory path where the files will be saved

        Returns:
            dict: Summary of downloaded files

        Notes:
            - Files are packaged in a ZIP file named: "{object label} {object record name} - attachment fields.zip"
            - When extracted, it includes a subfolder for each Attachment field in the response
            - The Content-Type header is set to application/zip;charset=UTF-8
            - The Content-Disposition header contains a filename component for naming the local file
        """
        return self.attachment_fields.download_all_attachment_field_files(
            object_name, object_record_id, directory_path
        )

    def update_attachment_field_file(
        self, object_name, object_record_id, field_name, file_path
    ):
        """
        Updates the file stored in an attachment field.

        POST /api/{version}/vobjects/{object_name}/{object_record_id}/attachment_fields/{attachment_field_name}/file

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the record
            field_name (str): API name of the attachment field
            file_path (str): Path to the file to upload

        Returns:
            dict: API response with update details

        Notes:
            - If you need to update more than one Attachment field, it's best practice
              to update in bulk with Update Object Records
        """
        return self.attachment_fields.update_attachment_field_file(
            object_name, object_record_id, field_name, file_path
        )

    # ------ Deep Copy Operations ------

    def deep_copy_object_record(self, object_name, record_id, payload=None):
        """
        Initiates a deep copy operation for an object record.
        Deep Copy copies an object record, including all of the record's related
        child and grandchild records.

        POST /api/{version}/vobjects/{object_name}/{object_record_ID}/actions/deepcopy

        Args:
            object_name (str): API name of the object
            record_id (str): ID of the record to copy
            payload (dict, optional): Configuration for the deep copy operation,
                                      can include field names to override values

        Returns:
            dict: API response containing the job ID

        Notes:
            - Each deep copy can copy a maximum of 10,000 related records at a time
            - In the request body, you can include field names to override field values in the source record
            - For a regular (non-deep) copy, use Create Object endpoint with source_record_id field
        """
        return self.crud.deep_copy_object_record(object_name, record_id, payload)

    def retrieve_deep_copy_results(self, object_name, job_status, job_id):
        """
        Retrieves the results of a deep copy operation.

        GET /api/{version}/vobjects/deepcopy/results/{object_name}/{job_status}/{job_id}

        Args:
            object_name (str): API name of the object
            job_status (str): Status of the job (e.g., "success", "failure")
            job_id (str): ID of the deep copy job

        Returns:
            dict: Status and results of the deep copy operation

        Notes:
            - You must have previously requested a deep copy job which is no longer active
            - You need a valid job_id value from the deep copy request
            - Response includes details of any errors encountered during the copy process
        """
        return self.crud.retrieve_deep_copy_results(object_name, job_status, job_id)

    # ------ Other Operations ------

    def retrieve_deleted_object_record_id(self, object_name, id_token):
        """
        Retrieves the ID of a deleted object record using a security token.

        GET /api/{version}/objects/deletions/vobjects/{object_name}

        Args:
            object_name (str): API name of the object
            id_token (str): Security token string for the deleted record

        Returns:
            dict: Information about the deleted record

        Notes:
            - After object records are deleted, their IDs are available for retrieval for 30 days
            - Can use optional query parameters to narrow results to specific date/time ranges
            - Dates and times are in UTC
        """
        return self.crud.retrieve_deleted_object_record_id(object_name, id_token)

    def retrieve_limits_on_objects(self):
        """
        Retrieves information about API limits on objects.

        GET /api/{version}/limits

        Returns:
            dict: Information about API limits including:
                 - records_per_object: Maximum number of records per object
                 - custom_objects: Maximum number of custom objects and number remaining
        """
        return self.metadata.retrieve_limits_on_objects()

    def update_corporate_currency_fields(self, object_name, record_id, payload=None):
        """
        Updates corporate currency fields for a specific object record.
        This endpoint updates the field_corp__sys field values based on the Rate of the currency,
        denoted by the local_currency__sys field of the specified record.

        PUT /api/{version}/vobjects/{object_name}/actions/updatecorporatecurrency

        Args:
            object_name (str): API name of the object
            record_id (str): ID of the record to update
            payload (dict, optional): Data with field values to update

        Returns:
            dict: API response with job ID

        Notes:
            - Currency is a field type available on all Vault objects
            - When a user populates a local currency field value, Vault automatically
              populates the related corporate currency field value
            - This endpoint is useful when:
              1. Admins change the Corporate Currency setting for the vault
              2. Admins update the Rate setting for the local currency used by a record
            - If no id is provided, Vault updates corporate fields of all records for the object
        """
        return self.crud.update_corporate_currency_fields(
            object_name, record_id, payload
        )

    # ------ Object User Actions Operations ------

    def retrieve_object_record_user_actions(self, object_name, object_record_id):
        """
        Retrieve all available user actions that can be initiated on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/actions

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the object record

        Returns:
            dict: List of available user actions with metadata and execution links
                 Each action includes:
                 - name: The unique name of the user action
                 - label: Display label for the action
                 - type: Type of action (e.g., "workflow", "lifecycle")
                 - links: Array with metadata and execute endpoints

        Notes:
            - Returns actions that the authenticated user has permissions to view or initiate
            - Only includes actions that can be initiated through the API
            - Actions may include workflow initiations and lifecycle state transitions
        """
        return self.actions.retrieve_object_record_user_actions(object_name, object_record_id)

    def retrieve_object_user_action_details(self, object_name, object_record_id, action_name):
        """
        Retrieve details about a specific user action that can be initiated on an object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/actions/{action_name}

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the object record
            action_name (str): Name of the user action

        Returns:
            dict: Detailed metadata about the user action including:
                 - name: The unique name of the user action
                 - label: Display label for the action
                 - type: Type of action (e.g., "workflow", "lifecycle")
                 - prompts: Array of prompts (fields) that may be required for execution
                 - links: Array with execute endpoint information

        Notes:
            - Provides detailed information about prompts and requirements for action execution
            - Includes field metadata for any required input parameters
        """
        return self.actions.retrieve_object_user_action_details(object_name, object_record_id, action_name)

    def initiate_object_action_on_single_record(self, object_name, object_record_id, action_name, payload=None):
        """
        Initiate a user action on a single object record.

        POST /api/{version}/vobjects/{object_name}/{object_record_id}/actions/{action_name}

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the object record
            action_name (str): Name of the user action to initiate
            payload (dict, optional): JSON data containing any required field values or parameters

        Returns:
            dict: Result of the action initiation, may include job ID for asynchronous actions

        Notes:
            - Some actions may execute synchronously and return immediate results
            - Other actions may be asynchronous and return a job ID for status tracking
            - Required field values should be provided in the payload based on action metadata
            - The authenticated user must have permission to initiate the specified action
        """
        return self.actions.initiate_object_action_on_single_record(object_name, object_record_id, action_name, payload)

    def initiate_object_action_on_multiple_records(self, object_name, action_name, payload):
        """
        Initiate a user action on multiple object records in bulk.

        POST /api/{version}/vobjects/{object_name}/actions/{action_name}

        Args:
            object_name (str): API name of the object
            action_name (str): Name of the user action to initiate
            payload (dict): JSON data containing record IDs and any required field values

        Returns:
            dict: Result of the bulk action initiation, typically includes job ID for tracking

        Notes:
            - Allows initiation of the same action on multiple records simultaneously
            - Payload should include array of record IDs and any required parameters
            - Most bulk actions are asynchronous and return job IDs for status tracking
            - The authenticated user must have permission to initiate the action on all specified records
            - Maximum batch size and other limits may apply based on action type
        """
        return self.actions.initiate_object_action_on_multiple_records(object_name, action_name, payload)
