from typing import Dict, Any, Optional, Union, BinaryIO
import json


class RIMSubmissionsArchiveService:
    """
    Service class for interacting with the Veeva Vault RIM Submissions Archive application.

    This service provides methods for importing, exporting, and managing submissions.
    """

    def __init__(self, client):
        """
        Initialize the RIMSubmissionsArchiveService with a VaultClient instance.

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def import_submission(self, submission_id: str, file: str) -> Dict[str, Any]:
        """
        Import a submission into your Vault.

        Before submitting this request:
        - You must be assigned permissions to use the API and have permissions to view and edit the specified submission__v object record.
        - You must create the corresponding object records for the Submission and Application objects in your Vault.
        - You must create and upload a valid submission import file or folder to file staging. The submission to import must be in a specific location and format.

        Submission Import File Location & Structure:
        The submission import file must be located in one of the following places, and must be in a specific folder structure.

        At the Root:
        If your submission import is located at the file staging root, it must follow the following structure:
        /SubmissionsArchive/{application_folder}/{submission_file_or_folder}

        {application_folder}: This required folder can have any name you wish.
        {submission_file_or_folder}: If this is a file containing your submission, it must be a .zip or .tar.gz. If this is a folder, it must contain your submission to import. This required folder can have any name you wish.

        For example, /SubmissionsArchive/nda654321/0001.zip.

        Within a User Folder:
        In some cases, your Vault user permissions may prevent you from uploading directly to the file staging root. In these cases, you must upload to your user folder using the following structure:
        /u[ID]/Submissions Archive Import/{application_folder}/{submission_folder}

        {application_folder}: This required folder can have any name you wish.
        {submission_folder}: The folder containing your submission to import. This required folder can have any name you wish. Vault does not support importing .zip or .tar.gz files from user folders.

        For example, /u5678/Submissions Archive Import/nda123456/0013.

        Args:
            submission_id: The id field value of the submission__v object record.
            file: The path to the submission folder or ZIP file previously uploaded to file staging.
                In the request, add the file parameter to your input and enter the path to the submission
                folder relative to the file staging root, for example, /SubmissionsArchive/nda123456/0000,
                or to the path to your user file staging folder, for example,
                /u5678/Submissions Archive Import/nda123456/0000.
                Vault does not support importing .zip or .tar.gz files from user folders.

        Returns:
            API response containing job_id, url, and possible warnings
        """
        endpoint = f"api/{self.client.LatestAPIversion}/vobjects/submission__v/{submission_id}/actions/import"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"file": file}

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, data=data
        )

    def retrieve_submission_import_results(
        self, submission_id: str, job_id: str
    ) -> Dict[str, Any]:
        """
        After Vault has finished processing the submission import job, use this request
        to retrieve the results of the completed submission binder.

        Before submitting this request:
        - You must be assigned permissions to use the API and permissions to view the specified submission__v object record.
        - There must be a previously submitted and completed submission import request, i.e., the status of the import job must be no longer active.

        Args:
            submission_id: The id field value of the submission__v object record.
            job_id: The jobId field value returned from the Import Submission request.

        Returns:
            API response containing the id, major_version_number__v, and minor_version_number__v of the submission binder
        """
        endpoint = f"api/{self.client.LatestAPIversion}/vobjects/submission__v/{submission_id}/actions/import/{job_id}/results"

        headers = {"Accept": "application/json"}

        return self.client.api_call(endpoint=endpoint, method="GET", headers=headers)

    def retrieve_submission_metadata_mapping(
        self, submission_id: str
    ) -> Dict[str, Any]:
        """
        Retrieve the metadata mapping values of an eCTD submission package.

        Args:
            submission_id: The id field value of the submission__v object record.

        Returns:
            API response containing metadata mapping records with details for each XML metadata node
            requiring mapping, including name__v, external_id__v, and xml_id.
        """
        endpoint = f"api/{self.client.LatestAPIversion}/vobjects/submission__v/{submission_id}/actions/ectdmapping"

        headers = {"Accept": "application/json"}

        return self.client.api_call(endpoint=endpoint, method="GET", headers=headers)

    def update_submission_metadata_mapping(
        self, submission_id: str, mapping_data: list
    ) -> Dict[str, Any]:
        """
        Update the mapping values of a submission.

        Args:
            submission_id: The id field value of the submission__v object record.
            mapping_data: List of dictionaries containing the mapping values to update.
                        Each dictionary should contain fields like name__v, external_id__v,
                        and mapping fields such as drug_substance__v.name__v, xml_id, etc.

        Returns:
            API response containing results of the update operation
        """
        endpoint = f"api/{self.client.LatestAPIversion}/vobjects/submission__v/{submission_id}/actions/ectdmapping"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="PUT", headers=headers, json=mapping_data
        )

    def remove_submission(self, submission_id: str) -> Dict[str, Any]:
        """
        Delete a previously imported submission from your Vault.

        By removing a submission, you delete any sections created in the archive binder as part
        of the submission import. This will also remove any documents in the submission from the
        archive binder. This does not delete the documents from Vault, but does mean that they
        no longer appear in the Viewer tab and users will not be able to access them using
        cross-document navigation. You must re-import the submission to make it available.

        Args:
            submission_id: The id field value of the submission__v object record.

        Returns:
            API response containing job_id and url for checking job status
        """
        endpoint = f"api/{self.client.LatestAPIversion}/vobjects/submission__v/{submission_id}/actions/import"

        headers = {"Accept": "application/json"}

        return self.client.api_call(endpoint=endpoint, method="DELETE", headers=headers)

    def cancel_submission(self, submission_id: str) -> Dict[str, Any]:
        """
        You can use this request on a submission object record that has a Submissions Archive Status (archive_status__v) of:

        - IMPORT_IN_PROGRESS: This will terminate the import job and set the archive_status__v field
          on the submission__v object record to "Error". The submission must be removed before a
          re-import can be done.

        - REMOVAL_IN_PROGRESS: This will terminate the import removal job and set the archive_status__v
          field on the submission__v object record to "Error". The submission must be removed before
          a re-import can be done.

        - IMPORT_IN_QUEUE: This will remove the import from the job queue and set the archive_status__v
          field on the submission__v object record to "Null".

        - REMOVAL_IN_QUEUE: This will remove the import removal from the job queue and set the
          archive_status__v field on the submission__v object record to "Error".

        To retrieve the archive_status__v, GET /api/{version}/vobjects/submission__v/{submission_id}.

        Args:
            submission_id: The id field value of the submission__v object record.

        Returns:
            API response containing the status of the cancel operation
        """
        endpoint = f"api/{self.client.LatestAPIversion}/vobjects/submission__v/{submission_id}/actions/import"

        headers = {"Accept": "application/json"}

        params = {"cancel": "true"}

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, params=params
        )

    def export_submission(
        self,
        binder_id: str,
        submission_id: str,
        major_version: Optional[str] = None,
        minor_version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Use the following requests to export the latest or most recent version of a Submissions Archive binder.
        These endpoints do not support the export of submissions binders published by RIM Submissions Publishing.
        Learn more about RIM Submissions Publishing in Vault Help.

        Args:
            binder_id: The binder id field value.
            submission_id: The id field value of the submission__v object record.
            major_version: Optional. The major_version_number__v field value of the binder.
            minor_version: Optional. The minor_version_number__v field value of the binder.

        Returns:
            API response containing the URL to check the status of the export job and the job_id
        """
        if major_version is not None and minor_version is not None:
            endpoint = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/actions/export"
        else:
            endpoint = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/actions/export"

        headers = {"Accept": "application/json"}

        params = {"submission": submission_id}

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, params=params
        )

    def export_partial_submission(
        self,
        binder_id: str,
        submission_id: str,
        major_version: str,
        minor_version: str,
        sections_data: Any,
    ) -> Dict[str, Any]:
        """
        Use this request to export only specific sections and documents from the latest version of a submissions
        binder in your Vault. This will export only parts of the binder, not the complete binder. Exporting a
        binder section node will automatically include all of its subsections and documents therein.

        Before submitting this request:
        - The Export Binder feature must be enabled in your Vault.
        - You must be assigned permissions to use the API.
        - You must have the Export Binder permission.
        - You must have the View Document permission for the binder. Only documents in the binder which you have
          the View Document permission are available to export.

        Args:
            binder_id: The binder id field value.
            submission_id: The id field value of the submission__v object record.
            major_version: The major_version_number__v field value of the binder.
            minor_version: The minor_version_number__v field value of the binder.
            sections_data: CSV or JSON data containing the id values of the binder sections
                         and/or documents to be exported.

        Returns:
            API response containing the URL to check the status of the export job and the job_id
        """
        endpoint = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/{major_version}/{minor_version}/actions/export"

        headers = {
            "Content-Type": "text/csv",  # Could be application/json as well
            "Accept": "application/json",
        }

        params = {"submission": submission_id}

        return self.client.api_call(
            endpoint=endpoint,
            method="POST",
            headers=headers,
            params=params,
            data=sections_data,
        )

    def retrieve_submission_export_results(self, job_id: str) -> Dict[str, Any]:
        """
        After submitting a request to export a submission from your Vault, you can query Vault
        to determine the results of the request.

        Before submitting this request:
        - You must have previously requested a submission export job (via the API) which is no longer active.
        - You must have a valid job_id field value returned from the Export Submission request.

        Args:
            job_id: The jobId field value returned from the Export Submission request.

        Returns:
            API response containing details of the export operation including:
            - job_id: The job_id field value of the submission export request.
            - id: The id field value of the exported submission.
            - major_version_number__v: The major version number of the exported submission.
            - minor_version_number__v: The minor version number of the exported submission.
            - file: The path/location of the exported submission (packaged in a ZIP file on file staging).
            - user_id__v: The id field value of the Vault user who initiated the submission export job.
        """
        endpoint = f"api/{self.client.LatestAPIversion}/objects/binders/actions/export/{job_id}/results"

        headers = {"Accept": "application/json"}

        return self.client.api_call(endpoint=endpoint, method="GET", headers=headers)
