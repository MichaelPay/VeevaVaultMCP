import pandas as pd
import requests


class BulkTranslationService:
    """
    Service class for managing bulk translations in Veeva Vault.

    This service provides methods to interact with all bulk translation-related API endpoints,
    allowing export and import of bulk translation files for different message types and languages.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def export_bulk_translation_file(self, message_type, language_code):
        """
        Exports a bulk translation file from your Vault.

        Corresponds to POST /api/{version}/messages/{message_type}/language/{lang}/actions/export

        The exported bulk translation file is a CSV editable in any text editor or translation software.
        You can request one (1) message type in one (1) language per request.

        This request starts an asynchronous job that exports the translation file to your Vault's file staging.
        You can then download this file with the Download Item Content request.

        You must have the Admin: Language: Read permission to export a bulk translation file from Vault.

        Args:
            message_type (str): The message type name. Valid values are:
                                'field_labels__sys', 'system_messages__sys',
                                'notification_template_messages__sys', or 'user_account_messages__sys'.
            language_code (str): A valid language code value, for example, 'en'.
                                 Retrieve available values from the Admin Key (admin_key__sys) field on
                                 the Language (language__sys) object. Active and Inactive languages are both valid.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - data: A dictionary containing:
                    - jobId: The ID of the created job
                    - url: The URL to retrieve the job status

        Note:
            When the job is complete, the translation files are available on your Vault's file staging.
            Retrieving the job status of this completed job provides the href to download the CSV from file staging.
        """
        url = f"api/{self.client.LatestAPIversion}/messages/{message_type}/language/{language_code}/actions/export"
        return self.client.api_call(url, method="POST")

    def import_bulk_translation_file(self, message_type, file_path):
        """
        Imports a bulk translation file into Vault.

        Corresponds to POST /api/{version}/messages/{message_type}/actions/import

        While an exported bulk translation file can contain only one (1) language, your import file
        may include multiple languages. Vault reads the language value separately for each row and applies
        any new translations immediately. Vault ignores any rows without changes.

        You must have the Admin: Language: Edit permission to import a bulk translation file to Vault.
        Upload the CSV file to your Vault's file staging before making this request.

        Args:
            message_type (str): The message type name. Valid values are:
                                'field_labels__sys', 'system_messages__sys',
                                'notification_template_messages__sys', or 'user_account_messages__sys'.
            file_path (str): The file path of the CSV file on file staging. Cannot contain ../ or
                             any other path traversal directives.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - data: A dictionary containing:
                    - jobId: The ID of the created job
                    - url: The URL to retrieve the job status

        Notes:
            - The maximum CSV input file size is 1GB.
            - The values in the input must be UTF-8 encoded.
            - CSVs must follow the standard RFC 4180 format, with some exceptions.

            On SUCCESS, the response includes the job_id which allows you to:
            - Retrieve the job status, which specifies if the import job has completed with SUCCESS
            - Retrieve the job summary, which provides details of a successful job
            - Retrieve the job errors, which provides details about the errors encountered in the job (if any)
        """
        url = (
            f"api/{self.client.LatestAPIversion}/messages/{message_type}/actions/import"
        )
        data = {"file_path": file_path}
        return self.client.api_call(url, method="POST", data=data)

    def retrieve_import_job_summary(self, job_id):
        """
        Retrieves the summary of a bulk translation import job.

        Corresponds to GET /api/{version}/services/jobs/{job_id}/summary

        After submitting a request to import a bulk translation file, you can query Vault
        to determine the results of the request.

        Before submitting this request:
        - You must have previously requested an Import Bulk Translation File job (via the API)
          which is no longer active
        - You must be the user who initiated the job or have the Admin: Jobs: Read permission

        Args:
            job_id (str): The id value of the requested import job. This was returned
                          from the Import Bulk Translation File request.

        Returns:
            dict: The JSON response containing:
                - responseStatus: "SUCCESS" if successful
                - data: A dictionary containing:
                    - ignored: The number of rows that were ignored. For example, Vault ignores any rows without changes.
                    - updated: The number of existing rows that were updated successfully.
                    - failed: The number of rows that attempted an update but failed.
                              Use the retrieve_import_job_errors method to retrieve details about these rows.
                    - added: The number of new rows that were added.
        """
        url = f"api/{self.client.LatestAPIversion}/services/jobs/{job_id}/summary"
        return self.client.api_call(url)

    def retrieve_import_job_errors(self, job_id):
        """
        Retrieves the errors from a bulk translation import job.

        Corresponds to GET /api/{version}/services/jobs/{job_id}/errors

        After submitting a request to import a bulk translation file, you can query Vault
        to determine the errors from the request (if any).

        Before submitting this request:
        - You must have previously requested an Import Bulk Translation File job (via the API)
          which is no longer active
        - You must be the user who initiated the job or have the Admin: Jobs: Read permission

        Args:
            job_id (str): The id value of the requested import job. This was returned
                          from the Import Bulk Translation File request.

        Returns:
            str: CSV content containing the line number and error message for any errors
                 encountered in the job.

        Note:
            Unlike other API calls, this method returns the raw CSV content rather than
            a JSON or DataFrame because the API returns a CSV file directly.
        """
        url = f"api/{self.client.LatestAPIversion}/services/jobs/{job_id}/errors"
        headers = {"Accept": "text/csv"}
        response = self.client.api_call(url, headers=headers, return_raw=True)
        return response
