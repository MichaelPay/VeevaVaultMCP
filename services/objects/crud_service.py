import json
from .base_service import BaseObjectService


class ObjectCRUDService(BaseObjectService):
    """
    Service class for handling Veeva Vault object CRUD operations
    (Create, Read, Update, Delete).

    This service provides methods for retrieving, creating, updating,
    and deleting object records, as well as special operations like
    cascade delete and deep copy.
    """

    # ---------- Retrieve Object Record ----------
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
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}"

        return self.client.api_call(url)

    def retrieve_deleted_object_record_id(self, object_name, id_token=None, start_date=None, end_date=None):
        """
        Retrieves the ID of a deleted object record using a security token.

        GET /api/{version}/objects/deletions/vobjects/{object_name}

        Args:
            object_name (str): API name of the object
            id_token (str, optional): Security token string for the deleted record
            start_date (str, optional): Start date for filtering results (ISO format)
            end_date (str, optional): End date for filtering results (ISO format)

        Returns:
            dict: Information about the deleted record

        Notes:
            - After object records are deleted, their IDs are available for retrieval for 30 days
            - Can use optional query parameters to narrow results to specific date/time ranges
            - Dates and times are in UTC
        """
        url = f"api/{self.client.LatestAPIversion}/objects/deletions/vobjects/{object_name}"

        params = {}
        if id_token:
            params["idtoken"] = id_token
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return self.client.api_call(url, params=params)

    # ---------- Create & Upsert Object Records ----------
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
            - Required fields:
              - name__v (unless system-managed)
              - object_type__v or object_type__v.api_name__v (optional)
              - source_record_id (optional, for copying existing records)
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}"

        headers = {"Content-Type": content_type, "Accept": accept}

        if additional_headers:
            headers.update(additional_headers)

        # Convert data to proper format based on content_type
        if content_type == "application/json" and isinstance(data, dict):
            data = json.dumps(data)

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    # ---------- Update Object Records ----------
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
            - Required fields:
              - id or a unique field identified by idParam
              - field values to update
              - state__v and state_label (optional, with X-VaultAPI-MigrationMode)
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}"

        headers = {"Content-Type": "text/csv", "Accept": "text/csv"}

        params = {}
        if id_param:
            params["id_param"] = id_param
        if migration_mode:
            params["migration_mode"] = str(migration_mode).lower()

        # Convert data to proper format if it's a dictionary
        if isinstance(data, dict):
            data = json.dumps(data)
            headers["Content-Type"] = "application/json"
            headers["Accept"] = "application/json"

        return self.client.api_call(
            url, method="PUT", headers=headers, data=data, params=params
        )

    def update_corporate_currency_fields(self, object_name, record_id=None, payload=None):
        """
        Updates corporate currency fields for a specific object record or all records.
        This endpoint updates the field_corp__sys field values based on the Rate of the currency,
        denoted by the local_currency__sys field of the specified record.

        PUT /api/{version}/vobjects/{object_name}/actions/updatecorporatecurrency

        Args:
            object_name (str): API name of the object
            record_id (str, optional): ID of the record to update. If not provided,
                                     updates corporate fields of all records for the object
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
        if record_id:
            url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{record_id}/actions/updatecorporatecurrency"
        else:
            url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/actions/updatecorporatecurrency"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(payload if payload else {})

        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    # ---------- Delete Object Records ----------
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
            - Required fields:
              - id or a unique field identified by idParam
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}"

        headers = {"Content-Type": "text/csv", "Accept": "text/csv"}

        params = {}
        if id_param:
            params["id_param"] = id_param

        # Convert data to proper format if it's a dictionary
        if isinstance(data, dict):
            data = json.dumps(data)
            headers["Content-Type"] = "application/json"
            headers["Accept"] = "application/json"

        return self.client.api_call(
            url, method="DELETE", headers=headers, data=data, params=params
        )

    # ---------- Cascade Delete Object Record ----------
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
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/actions/cascadedelete"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers)

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
        url = f"api/{self.client.LatestAPIversion}/vobjects/cascadedelete/results/{object_name}/{job_status}/{job_id}"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    # ---------- Deep Copy Object Record ----------
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
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{record_id}/actions/deepcopy"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(payload if payload else {})

        return self.client.api_call(url, method="POST", headers=headers, data=data)

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
        url = f"api/{self.client.LatestAPIversion}/vobjects/deepcopy/results/{object_name}/{job_status}/{job_id}"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)
