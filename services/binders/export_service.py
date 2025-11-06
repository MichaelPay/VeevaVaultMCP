import json
from .base_service import BaseBinderService


class BinderExportService(BaseBinderService):
    """
    Service class for exporting binders from Veeva Vault.

    The Export Binder API allows you to export a zip archive with all documents from a binder,
    or a subset of those documents. You can also export different artifacts for the selected
    documents, including source documents, renditions, versions, and document fields.
    """

    def export_binder(
        self,
        binder_id,
        major_version=None,
        minor_version=None,
        source=True,
        renditiontype=None,
        docversion=None,
        attachments=None,
        fields=None,
        docfield=True,
    ):
        """
        Exports a complete binder, including all binder sections and documents.

        By default, the source files of all documents in the binder are exported.
        Use parameters to control which components of the binder to include.

        Args:
            binder_id (str): ID of the binder to export
            major_version (int, optional): Major version number of the binder
            minor_version (int, optional): Minor version number of the binder
            source (bool): Whether to include source files. Default is True.
                           To exclude source files, set to False.
            renditiontype (str, optional): Type of rendition to include.
                           Common value is 'viewable_rendition__v' to export
                           the PDF rendition of documents.
            docversion (str, optional): Version of documents to include.
                       Options:
                       - 'major': Override binding rule and export all major versions
                       - 'major_minor': Override binding rule and export all major and minor versions
            attachments (str, optional): Whether to include attachments.
                         Options:
                         - 'all': Export all versions of all attachments
                         - 'latest': Export the latest version of all attachments
            fields (str, optional): Comma-separated list of field values to export.
                    By default, only name__v field is included.
            docfield (bool): Whether to include document metadata. Default is True.
                            Set to False to exclude metadata.

        Returns:
            dict: API response containing the export job details with keys:
                - responseStatus: Status of the request
                - responseMessage: Message about the job
                - URL: The URL to retrieve the current status of the binder export job
                - job_id: The Job ID value used to retrieve the status and results
        """
        # Determine URL based on whether we're exporting a specific version
        if major_version is not None and minor_version is not None:
            url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/actions/export"
        else:
            url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/actions/export"

        params = {"source": str(source).lower()}

        if renditiontype:
            params["renditiontype"] = renditiontype
        if docversion:
            params["docversion"] = docversion
        if attachments is not None:
            params["attachments"] = attachments
        if fields:
            params["fields"] = fields
        if docfield is not None:
            params["docfield"] = str(docfield).lower()

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers, params=params)

    def export_binder_sections(
        self,
        binder_id,
        major_version=None,
        minor_version=None,
        node_ids=None,
        input_file_format="csv",
    ):
        """
        Exports only specific sections and documents from a binder.

        This will export only parts of the binder, not the complete binder.
        Exporting a binder section node will automatically include all of its
        subsections and documents therein.

        Args:
            binder_id (str): ID of the binder to export sections from
            major_version (int, optional): Major version number of the binder
            minor_version (int, optional): Minor version number of the binder
            node_ids (list): List of node IDs specifying sections and documents to export
            input_file_format (str, optional): Format of input file ('csv' or 'json'). Default is 'csv'

        Returns:
            dict: API response containing details of the export job with keys:
                - responseStatus: Status of the request
                - responseMessage: Message about the job
                - URL: The URL to retrieve the current status of the binder export job
                - job_id: The Job ID value used to retrieve the status and results

        Note:
            To retrieve a list of all nodes from a binder, use:
            GET /api/{version}/objects/binders/{binder_id}?depth=all
        """
        # Determine URL based on whether we're exporting a specific version
        if major_version is not None and minor_version is not None:
            url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/actions/export"
        else:
            url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/actions/export"

        headers = {"Accept": "application/json"}

        if input_file_format.lower() == "csv":
            headers["Content-Type"] = "text/csv"
            data = "\n".join(map(str, node_ids))
        else:  # input_file_format is 'json'
            headers["Content-Type"] = "application/json"
            data = json.dumps({"id": node_ids})

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def retrieve_binder_export_results(self, job_id):
        """
        Retrieves the results of a completed binder export job.

        After submitting a request to export a binder, use this method to
        determine the results of the request.

        Args:
            job_id (str): ID of the export job (retrieved from the export binder request)

        Returns:
            dict: API response containing the export job results with keys:
                - responseStatus: Status of the request
                - job_id: The Job ID value of the binder export request
                - id: The id value of the exported binder
                - major_version_number__v: The major version number of the exported binder
                - minor_version_number__v: The minor version number of the exported binder
                - file: The path/location of the downloaded binder ZIP file
                - user_id__v: The id value of the Vault user who initiated the export

        Note:
            The binder export job must have been successfully completed and no longer active.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/actions/export/{job_id}/results"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def download_exported_binder_files(self, file_path):
        """
        Downloads the files from a completed binder export.

        Once your binder export job has been successfully completed, you can
        download the exported binder which is packaged in a ZIP file.

        Prerequisites:
        - The binder export job must have been successfully completed
        - The API user must have permission to access File Staging

        Args:
            file_path (str): File path returned by the export operation results

        Returns:
            bytes: Binary data of the exported files as a ZIP archive
        """
        url = file_path

        headers = {"Accept": "application/zip"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content
