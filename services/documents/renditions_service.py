import json
import os
from .base_service import BaseDocumentService


class DocumentRenditionsService(BaseDocumentService):
    """
    Service class for managing document renditions in Veeva Vault
    """

    def retrieve_document_renditions(self, doc_id):
        """
        Retrieves all renditions for a document.

        This endpoint returns a list of all rendition types configured for the document
        and the available renditions with their retrieval URLs.

        Args:
            doc_id (str): ID of the document

        Returns:
            dict: API response containing:
                - renditionTypes: List of all rendition types configured for the document
                - renditions: List of renditions available and their endpoint URLs
        """
        url = (
            f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/renditions"
        )

        return self.client.api_call(url)

    def retrieve_document_version_renditions(
        self, doc_id, major_version, minor_version
    ):
        """
        Retrieves all renditions for a specific version of a document.

        This endpoint returns a list of all rendition types configured for the document version
        and the available renditions with their retrieval URLs.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number
            minor_version (int): Minor version number

        Returns:
            dict: API response containing:
                - renditionTypes: List of all rendition types configured for the document
                - renditions: List of renditions available and their endpoint URLs
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/renditions"

        return self.client.api_call(url)

    def download_document_rendition_file(
        self, doc_id, rendition_type, steady_state=None, protected_rendition=None
    ):
        """
        Downloads a specific rendition from the latest version of a document.

        Args:
            doc_id (str): ID of the document
            rendition_type (str): Type of rendition to download
            steady_state (bool, optional): When True, downloads rendition from the latest
                steady state version (1.0, 2.0, etc.) of the document
            protected_rendition (bool, optional): When False, downloads the non-protected rendition.
                Defaults to True if omitted. Requires the Download Non-Protected Rendition permission.

        Returns:
            bytes: Binary content of the rendition file
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/renditions/{rendition_type}"

        params = {}
        if steady_state is not None:
            params["steadyState"] = "true" if steady_state else "false"
        if protected_rendition is not None:
            params["protectedRendition"] = "true" if protected_rendition else "false"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(
            url, params=params, headers=headers, raw_response=True
        )
        return response.content

    def download_document_version_rendition_file(
        self,
        doc_id,
        major_version,
        minor_version,
        rendition_type,
        protected_rendition=None,
    ):
        """
        Downloads a specific rendition for a specific version of a document.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number
            minor_version (int): Minor version number
            rendition_type (str): Type of rendition to download
            protected_rendition (bool, optional): When False, downloads the non-protected rendition.
                Defaults to True if omitted. Requires the Download Non-Protected Rendition permission.

        Returns:
            bytes: Binary content of the rendition file
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/renditions/{rendition_type}"

        params = {}
        if protected_rendition is not None:
            params["protectedRendition"] = "true" if protected_rendition else "false"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(
            url, params=params, headers=headers, raw_response=True
        )
        return response.content

    def add_multiple_document_renditions(
        self, file_path, idParam=None, largeSizeAsset=None
    ):
        """
        Adds renditions to multiple documents in bulk.

        You must first load the renditions to file staging. If the largeSizeAsset parameter
        is not set to true, you must include the X-VaultAPI-MigrationMode header.

        The maximum CSV input file size is 1GB, values must be UTF-8 encoded,
        CSVs must follow the standard RFC 4180 format, and the maximum batch size is 500.

        Args:
            file_path (str): Path to CSV file containing rendition details
            idParam (str, optional): Field name to identify documents (e.g., "external_id__v")
            largeSizeAsset (bool, optional): When True, indicates renditions to add are of
                the Large Size Asset (large_size_asset__v) rendition type

        Returns:
            dict: API response with details of added renditions
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/renditions/batch"

        params = {}
        if idParam:
            params["idParam"] = idParam
        if largeSizeAsset is not None:
            params["largeSizeAsset"] = "true" if largeSizeAsset else "false"

        headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        with open(file_path, "rb") as file:
            return self.client.api_call(
                url, method="POST", params=params, headers=headers, data=file
            )

    def add_single_document_rendition(self, doc_id, rendition_type, file_path):
        """
        Adds a rendition to a document.

        If you need to add more than one document rendition, it is best practice to use the bulk API.
        The maximum allowed file size is 4GB.

        Args:
            doc_id (str): ID of the document
            rendition_type (str): Type of rendition to add
            file_path (str): Path to rendition file

        Returns:
            dict: API response with details of added rendition
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/renditions/{rendition_type}"

        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            return self.client.api_call(url, method="POST", files=files)

    def upload_document_version_rendition(
        self, doc_id, major_version, minor_version, rendition_type, file_path
    ):
        """
        Uploads a rendition for a specific document version.

        The maximum allowed file size is 4GB.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number
            minor_version (int): Minor version number
            rendition_type (str): Type of rendition to upload
            file_path (str): Path to rendition file

        Returns:
            dict: API response with details of uploaded rendition
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/renditions/{rendition_type}"

        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            return self.client.api_call(url, method="POST", files=files)

    def update_multiple_document_renditions(self, file_path):
        """
        Updates or re-renders document renditions in bulk.

        The maximum CSV input file size is 1GB, values must be UTF-8 encoded,
        CSVs must follow the standard RFC 4180 format, and the maximum batch size is 500.

        Args:
            file_path (str): Path to CSV file containing rendition details to update

        Returns:
            dict: API response with details of updated renditions
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/batch/actions/rerender"

        headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        with open(file_path, "rb") as file:
            return self.client.api_call(url, method="POST", headers=headers, data=file)

    def replace_document_rendition(self, doc_id, rendition_type, file_path):
        """
        Replaces an existing rendition for a document.

        The maximum allowed file size is 4GB.

        Args:
            doc_id (str): ID of the document
            rendition_type (str): Type of rendition to replace
            file_path (str): Path to new rendition file

        Returns:
            dict: API response with details of replaced rendition
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/renditions/{rendition_type}"

        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            return self.client.api_call(url, method="PUT", files=files)

    def replace_document_version_rendition(
        self, doc_id, major_version, minor_version, rendition_type, file_path
    ):
        """
        Replaces an existing rendition for a specific document version.

        The maximum allowed file size is 4GB.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number
            minor_version (int): Minor version number
            rendition_type (str): Type of rendition to replace
            file_path (str): Path to new rendition file

        Returns:
            dict: API response with details of replaced rendition
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/renditions/{rendition_type}"

        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            return self.client.api_call(url, method="PUT", files=files)

    def delete_multiple_document_renditions(self, csv_file_path):
        """
        Deletes multiple document renditions in bulk.

        The maximum input file size is 1GB, values must be UTF-8 encoded,
        CSVs must follow the standard RFC 4180 format, and the maximum batch size is 500.

        Args:
            csv_file_path (str): Path to CSV file containing rendition details to delete

        Returns:
            dict: API response with deletion status
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/renditions/batch"

        headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        with open(csv_file_path, "rb") as file:
            return self.client.api_call(
                url, method="DELETE", headers=headers, data=file
            )

    def delete_single_document_rendition(self, document_id, rendition_type):
        """
        Deletes a specific rendition from the latest version of a document.

        If you need to delete more than one document rendition, it is best practice to use the bulk API.

        Args:
            document_id (str): ID of the document
            rendition_type (str): Type of rendition to delete

        Returns:
            dict: API response with deletion status
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{document_id}/renditions/{rendition_type}"

        return self.client.api_call(url, method="DELETE")

    def delete_document_version_rendition(
        self, doc_id, major_version, minor_version, rendition_type
    ):
        """
        Deletes a specific rendition from a specific document version.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number
            minor_version (int): Minor version number
            rendition_type (str): Type of rendition to delete

        Returns:
            dict: API response with deletion status
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/renditions/{rendition_type}"

        return self.client.api_call(url, method="DELETE")

    def get_document_rendition_types(self):
        """
        Retrieves the available rendition types.

        Returns:
            dict: API response listing available rendition types
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/renditiontypes"

        return self.client.api_call(url)

    def download_rendition(
        self, doc_id, rendition_type="viewable", major_version=None, minor_version=None
    ):
        """
        Downloads a specific rendition of a document.

        This is a convenience method that calls the appropriate endpoint based on
        whether version information is provided.

        Args:
            doc_id (str): ID of the document
            rendition_type (str): Type of rendition (defaults to "viewable")
            major_version (int, optional): Major version number
            minor_version (int, optional): Minor version number

        Returns:
            bytes: Binary data of the rendition
        """
        # Determine URL based on whether we're downloading a specific version
        if major_version is not None and minor_version is not None:
            url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/renditions/{rendition_type}"
        else:
            url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/renditions/{rendition_type}"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content
