class VaultLoaderService:
    """
    Service class for managing Vault Loader operations in Veeva Vault.

    This service provides methods to leverage Loader Services to load a set of data objects
    to your Vault or extract one or more data files from your Vault.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def extract_data_files(self, extract_objects, send_notification=False):
        """
        Extract one or more data files from Vault.

        Creates a Loader job to extract one or more data files. You can extract a maximum of 10 data objects per request.

        Corresponds to POST /api/{version}/services/loader/extract

        Args:
            extract_objects (list): A list of dictionaries, each containing the following fields:
                - object_type (str, required): The type of data object to extract. Allowed values:
                  vobjects__v, documents__v, document_versions__v, document_relationships__v, groups__v
                - object (str, conditional): If object_type=vobjects__v, include the object name. For example, product__v.
                - extract_options (str, optional): Include to specify whether or not to extract renditions and/or source files
                  for the documents__v and document_versions__v object types. Allowed values:
                  include_source__v, include_renditions__v
                - fields (list, required): A list of field names for the specified object type.
                  For example: ["id", "name__v", "descriptions__v"]
                - vql_criteria__v (str, optional): A VQL-like expression used to optionally filter the data set
                  to only those records that meet a specified criterion.
            send_notification (bool, optional): If True, sends a Vault notification when the job completes.
                Defaults to False.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - url: The URL to check job status
                - job_id: The Job ID value to retrieve the status of the loader extract request
                - tasks: A set of tasks with a task_id for each extract request
        """
        url = f"api/{self.client.LatestAPIversion}/services/loader/extract"

        params = {}
        if send_notification:
            params["sendNotification"] = "true"

        return self.client.api_call(
            url, method="POST", json=extract_objects, params=params
        )

    def retrieve_loader_extract_results(self, job_id, task_id):
        """
        Retrieve the results of a specified job task.

        After submitting a request to extract data files from your Vault, you can query Vault
        to retrieve the results of a specified job task.

        Corresponds to GET /api/{version}/services/loader/{job_id}/tasks/{task_id}/results

        Args:
            job_id (int): The id value of the requested extract job. Obtain this from the Extract Data Files request.
            task_id (str): The id value of the requested extract task. Obtain this from the Extract Data Files request.

        Returns:
            str: CSV output containing the results of a specific extract job task.
                If the Loader job task was unsuccessful, the response is blank.

        Note:
            If the extract includes document or document version renditions, the CSV output contains paths
            to rendition files on your Vault's file staging. When an export includes multiple rendition types
            for a document or document version, the CSV output includes a separate row for each rendition type.
        """
        url = f"api/{self.client.LatestAPIversion}/services/loader/{job_id}/tasks/{task_id}/results"

        headers = {"Accept": "text/csv"}

        return self.client.api_call(url, headers=headers, raw_response=True)

    def retrieve_loader_extract_renditions_results(self, job_id, task_id):
        """
        Retrieve rendition results of a specified job task.

        After submitting a request to extract object types from your Vault, you can query Vault to retrieve
        results of a specified job task that includes renditions requested with documents.

        Corresponds to GET /api/{version}/services/loader/{job_id}/tasks/{task_id}/results/renditions

        Args:
            job_id (int): The id value of the requested extract job.
            task_id (str): The id value of the requested extract task.

        Returns:
            str: CSV output containing paths to rendition files for documents or document versions
                on your Vault's file staging. When an export includes multiple rendition types for
                a document or document version, the CSV output includes a separate row for each rendition type.
        """
        url = f"api/{self.client.LatestAPIversion}/services/loader/{job_id}/tasks/{task_id}/results/renditions"

        headers = {"Accept": "text/csv"}

        return self.client.api_call(url, headers=headers, raw_response=True)

    def load_data_objects(self, load_objects, send_notification=False):
        """
        Load a set of data files to Vault.

        Create a loader job and load a set of data files. You can load a maximum of 10 data objects per request.

        Corresponds to POST /api/{version}/services/loader/load

        Args:
            load_objects (list): A list of dictionaries, each containing the following fields:
                - object_type (str, required): The type of data object to load. Allowed values:
                  vobjects__v, documents__v, document_versions__v, document_relationships__v, groups__v,
                  document_roles__v, document_versions_roles__v, document_renditions__v, document_attachments__v
                - object (str, conditional): If object_type=vobjects__v, include the object name. For example, product__v.
                - action (str, required): The action type to create, update, upsert, or delete data objects.
                  If object_type=vobjects__v, also allows: create_attachments, delete_attachments, assign_roles, remove_roles.
                - file (str, required): The filepath to reference the CSV load file on file staging.
                - order (int, optional): Specifies the order of the load task.
                - idparam (str, optional): Identify object records by any unique field value. Can only be used if
                  object_type is vobjects__v and action is upsert, update, or delete.
                - recordmigrationmode (bool, optional): Set to true to create or update object records in a noninitial state
                  and with minimal validation.
                - notriggers (bool, optional): If set to true, Record Migration Mode bypasses record triggers.
                - documentmigrationmode (bool, optional): Set to true to create documents, document versions,
                  document version roles, or document renditions in a specific state or state type.
            send_notification (bool, optional): If True, sends a Vault notification when the job completes.
                Defaults to False.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - url: The URL to check job status
                - job_id: The Job ID value to retrieve the status of the loader request
                - tasks: The task_id for each load request
        """
        url = f"api/{self.client.LatestAPIversion}/services/loader/load"

        params = {}
        if send_notification:
            params["sendNotification"] = "true"

        return self.client.api_call(
            url, method="POST", json=load_objects, params=params
        )

    def retrieve_load_success_log(self, job_id, task_id):
        """
        Retrieve success logs of the loader results.

        Corresponds to GET /api/{version}/services/loader/{job_id}/tasks/{task_id}/successlog

        Args:
            job_id (int): The id value of the requested load job.
            task_id (str): The id value of the requested load task.

        Returns:
            str: CSV file that includes the success log of the loader results.
                Example:
                responseStatus,id,name__v,external_id__v,errors,rowId
                SUCCESS,00P000000000807,,,,1
                SUCCESS,00P000000000808,,,,2
                SUCCESS,00P000000000809,,,,3
        """
        url = f"api/{self.client.LatestAPIversion}/services/loader/{job_id}/tasks/{task_id}/successlog"

        headers = {"Accept": "text/csv"}

        return self.client.api_call(url, headers=headers, raw_response=True)

    def retrieve_load_failure_log(self, job_id, task_id):
        """
        Retrieve failure logs of the loader results.

        Corresponds to GET /api/{version}/services/loader/{job_id}/tasks/{task_id}/failurelog

        Args:
            job_id (int): The id value of the requested load job.
            task_id (str): The id value of the requested load task.

        Returns:
            str: CSV file that includes the failure log of the loader results.
                Example:
                responseStatus,name__v
                FAILURE/Versioning Documents
        """
        url = f"api/{self.client.LatestAPIversion}/services/loader/{job_id}/tasks/{task_id}/failurelog"

        headers = {"Accept": "text/csv"}

        return self.client.api_call(url, headers=headers, raw_response=True)
