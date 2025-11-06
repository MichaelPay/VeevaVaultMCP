from .base_service import BaseDocumentService
import json


class DocumentExportsService(BaseDocumentService):
    """
    Service class for exporting documents from Veeva Vault.

    Provides methods to export documents, document versions, and retrieve export results.
    """

    def export_documents(
        self, document_ids, source=True, renditions=False, all_versions=False
    ):
        """
        Exports a set of documents to your Vault's file staging.

        This endpoint allows you to use document IDs to export documents to your Vault's file staging.
        You can export source documents and renditions, and choose to export all versions or only the latest version.
        The maximum number of document versions (source files) you can export per request is 10,000.

        This API doesn't support exporting: Fields, Attachments, Audit trails, Related documents,
        Signature Pages, Overlays, or Protected renditions.

        Args:
            document_ids (list): A list of document IDs to export, formatted as [{"id": "58"}, {"id":"134"}, ...].
            source (bool, optional): Whether to include source files. Defaults to True.
            renditions (bool, optional): Whether to include renditions. Defaults to False.
            all_versions (bool, optional): Whether to include all versions or only latest version. Defaults to False.

        Returns:
            dict: Response containing job_id and URL to check job status.
            Example: {
                "responseStatus": "SUCCESS",
                "url": "/api/v25.2/services/jobs/36203",
                "job_id": "36203"
            }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/batch/actions/fileextract"

        # Add query parameters
        params = {
            "source": str(source).lower(),
            "renditions": str(renditions).lower(),
            "allversions": str(all_versions).lower(),
        }

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response = self.client.api_call(
            url,
            method="POST",
            params=params,
            headers=headers,
            data=json.dumps(document_ids),
        )
        return response

    def export_document_versions(self, version_data, source=True, renditions=False):
        """
        Exports a specific set of document versions to your Vault's file staging.

        The files you export go to the u{userID} folder, regardless of your security profile.

        Args:
            version_data (list): A list of dictionaries with document version information.
                Each dictionary must contain:
                - id: ID of the document to export
                - major_version_number__v: The major version number of the document to export
                - minor_version_number__v: The minor version number of the document to export
            source (bool, optional): Whether to include source files. Defaults to True.
            renditions (bool, optional): Whether to include renditions. Defaults to False.

        Returns:
            dict: Response containing job_id and URL to check job status.
            Example: {
                "responseStatus": "SUCCESS",
                "url": "/api/v25.2/services/jobs/40604",
                "job_id": "40604"
            }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/versions/batch/actions/fileextract"

        # Add query parameters
        params = {"source": str(source).lower(), "renditions": str(renditions).lower()}

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response = self.client.api_call(
            url,
            method="POST",
            params=params,
            headers=headers,
            data=json.dumps(version_data),
        )
        return response

    def get_document_export_results(self, job_id):
        """
        Retrieves the results of a document export job.

        Before submitting this request:
        - You must have previously requested a document export job (via the API) which is no longer active.
        - You must have a valid job_id value (retrieved from the document export request).
        - You must be a Vault Owner, System Admin or the user who initiated the job.

        Args:
            job_id (str): The ID of the requested export job returned from export_documents or export_document_versions.

        Returns:
            dict: A dictionary containing the export results.
            Example: {
                "responseStatus": "SUCCESS",
                "data": [
                    {
                        "responseStatus": "SUCCESS",
                        "id": 23,
                        "major_version_number__v": 0,
                        "minor_version_number__v": 1,
                        "file": "/82701/23/0_1/New Document.png",
                        "user_id__v": 88973
                    }
                ]
            }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/batch/actions/fileextract/{job_id}/results"

        headers = {"Accept": "application/json"}

        response = self.client.api_call(url, method="GET", headers=headers)
        return response

    def export_document_data_as_csv(self, doc_id):
        """
        Exports document data in CSV format.

        Args:
            doc_id (str): ID of the document

        Returns:
            str: CSV data containing document information
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/export"

        headers = {"Accept": "text/csv"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.text

    def export_document_version_data_as_csv(self, doc_id, major_version, minor_version):
        """
        Exports document version data in CSV format.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number
            minor_version (int): Minor version number

        Returns:
            str: CSV data containing document version information
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/export"

        headers = {"Accept": "text/csv"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.text

    def export_document_search_results_as_csv(self, search_criteria):
        """
        Exports document search results in CSV format.

        Args:
            search_criteria (dict): Search criteria for finding documents

        Returns:
            str: CSV data containing search results
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/search"

        headers = {"Content-Type": "application/json", "Accept": "text/csv"}

        response = self.client.api_call(
            url,
            method="POST",
            headers=headers,
            data=json.dumps(search_criteria),
            raw_response=True,
        )
        return response.text
