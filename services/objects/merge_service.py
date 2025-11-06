import json
from .base_service import BaseObjectService


class ObjectMergeService(BaseObjectService):
    """
    Service class for handling Veeva Vault object merge operations.

    Provides functionality to merge duplicate records in Vault by specifying
    a main record and a duplicate record to be merged together.
    """

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
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/actions/mergerecords"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(payload)
        )

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
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/actions/mergerecords/{job_id}"

        return self.client.api_call(url)

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
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/actions/mergerecords/{job_id}/results"

        return self.client.api_call(url)

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
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/actions/mergerecords/{job_id}/log"

        response = self.client.api_call(url, stream=True, raw_response=True)

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return "Merge records job log downloaded successfully"
