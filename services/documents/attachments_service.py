import os
from .base_service import BaseDocumentService


class DocumentAttachmentsService(BaseDocumentService):
    """
    Service class for managing document attachments in Veeva Vault.
    Learn about Document Attachments in Vault Help.
    """

    def determine_if_document_has_attachments(self, doc_id):
        """
        Determines if a document has attachments.

        Args:
            doc_id (str): ID of the document to check

        Returns:
            dict: API response containing attachment information
                  Example:
                  {
                      "attachments": [
                          {
                              "id": 566,
                              "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566"
                          },
                          {
                              "id": 567,
                              "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/567"
                          }
                      ]
                  }

        Notes:
            The "attachments" attribute is displayed in the response for documents in which
            attachments have been enabled on the document type (even if the document has no attachments).
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}"

        return self.client.api_call(url)

    def retrieve_document_attachments(self, doc_id):
        """
        Retrieves all attachments for a document.

        Args:
            doc_id (str): ID of the document

        Returns:
            dict: API response containing document attachments
                  Example:
                  {
                      "responseStatus": "SUCCESS",
                      "data": [
                          {
                              "id": 566,
                              "filename__v": "Site Area Map.png",
                              "format__v": "image/png",
                              "size__v": 109828,
                              "md5checksum__v": "78b36d9602530e12051429e62558d581",
                              "version__v": 2,
                              "created_by__v": 46916,
                              "created_date__v": "2015-01-14T00:35:01.775Z",
                              "versions": [
                                  {
                                      "version__v": 1,
                                      "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/1"
                                  },
                                  {
                                      "version__v": 2,
                                      "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/2"
                                  }
                              ]
                          }
                      ]
                  }

        Notes:
            Unlike "regular" document versioning, attachment versioning uses integer numbers
            beginning with 1 and incrementing sequentially (1, 2, 3,…). There is no concept
            of major or minor version numbers with attachments.
        """
        url = (
            f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments"
        )

        return self.client.api_call(url)

    def retrieve_document_version_attachments(
        self, doc_id, major_version, minor_version
    ):
        """
        Retrieves all attachments for a specific document version.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number
            minor_version (int): Minor version number

        Returns:
            dict: API response containing document version attachments
                  Example:
                  {
                      "responseStatus": "SUCCESS",
                      "data": [
                          {
                              "id": 39,
                              "filename__v": "New",
                              "format__v": "application/x-tika-ooxml",
                              "size__v": 55762,
                              "md5checksum__v": "c5e7eaafc39af8ba42081a213a68f781",
                              "version__v": 1,
                              "created_by__v": 61603,
                              "created_date__v": "2017-10-30T17:03:29.878Z",
                              "versions": [
                                  {
                                      "version__v": 1,
                                      "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/17/versions/0/1/attachments/39/versions/1"
                                  }
                              ]
                          }
                      ]
                  }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/attachments"

        return self.client.api_call(url)

    def retrieve_document_attachment_versions(self, doc_id, attachment_id):
        """
        Retrieves all versions of a document attachment.

        Args:
            doc_id (str): ID of the document
            attachment_id (str): ID of the attachment

        Returns:
            dict: API response containing attachment versions
                  Example:
                  {
                      "responseStatus": "SUCCESS",
                      "data": [
                          {
                              "version__v": 1,
                              "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/1"
                          },
                          {
                              "version__v": 2,
                              "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/2"
                          }
                      ]
                  }

        Notes:
            Unlike documents, attachment versions use integer values starting with version 1
            and incrementing sequentially (2, 3, 4,…). Attachments do not use major or minor
            version numbers.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments/{attachment_id}/versions"

        return self.client.api_call(url)

    def retrieve_document_version_attachment_versions(
        self,
        doc_id,
        major_version,
        minor_version,
        attachment_id,
        attachment_version=None,
    ):
        """
        Retrieves all versions of an attachment for a specific document version.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number of the document
            minor_version (int): Minor version number of the document
            attachment_id (str): ID of the attachment
            attachment_version (str, optional): Specific attachment version to retrieve.
                                              If omitted, the endpoint retrieves all versions
                                              of the specified attachment.

        Returns:
            dict: API response containing attachment versions
                  Example:
                  {
                      "responseStatus": "SUCCESS",
                      "data": [
                          {
                              "id": 39,
                              "filename__v": "New",
                              "format__v": "application/x-tika-ooxml",
                              "size__v": 55762,
                              "md5checksum__v": "c5e7eaafc39af8ba42081a213a68f781",
                              "version__v": 1,
                              "created_by__v": 61603,
                              "created_date__v": "2017-10-30T17:03:29.878Z"
                          }
                      ]
                  }
        """
        if attachment_version:
            url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/attachments/{attachment_id}/versions/{attachment_version}"
        else:
            url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/attachments/{attachment_id}/versions"

        return self.client.api_call(url)

    def retrieve_document_attachment_metadata(self, doc_id, attachment_id):
        """
        Retrieves metadata for a document attachment.

        Args:
            doc_id (str): ID of the document
            attachment_id (str): ID of the attachment

        Returns:
            dict: API response containing attachment metadata
                  Example:
                  {
                      "responseStatus": "SUCCESS",
                      "data": [
                          {
                              "id": 566,
                              "filename__v": "Site Area Map.png",
                              "format__v": "image/png",
                              "size__v": 109828,
                              "md5checksum__v": "78b36d9602530e12051429e62558d581",
                              "version__v": 2,
                              "created_by__v": 46916,
                              "created_date__v": "2015-01-14T00:35:01.775Z",
                              "versions": [
                                  {
                                      "version__v": 1,
                                      "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/1"
                                  },
                                  {
                                      "version__v": 2,
                                      "url": "https://myvault.veevavault.com/api/v25.2/objects/documents/565/attachments/566/versions/2"
                                  }
                              ]
                          }
                      ]
                  }

        Notes:
            The md5checksum__v field is calculated on the latest version of the attachment.
            If an attachment is added which has the same MD5 checksum value as an existing
            attachment on a given document, the new attachment is not added.

            Available metadata fields include: id, version__v, filename__v, description__v,
            format__v, size__v, md5checksum__v, created_by__v, created_date__v, and versions.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments/{attachment_id}"

        return self.client.api_call(url)

    def retrieve_document_attachment_version_metadata(
        self, doc_id, attachment_id, attachment_version
    ):
        """
        Retrieves metadata for a specific version of a document attachment.

        Args:
            doc_id (str): ID of the document
            attachment_id (str): ID of the attachment
            attachment_version (str): Version of the attachment

        Returns:
            dict: API response containing attachment version metadata
                  Example:
                  {
                      "responseStatus": "SUCCESS",
                      "data": [
                          {
                              "id": 566,
                              "filename__v": "Site Area Map.png",
                              "format__v": "image/png",
                              "size__v": 109828,
                              "md5checksum__v": "78b36d9602530e12051429e62558d581",
                              "version__v": 2,
                              "created_by__v": 46916,
                              "created_date__v": "2015-01-14T00:35:01.775Z"
                          }
                      ]
                  }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments/{attachment_id}/versions/{attachment_version}"

        return self.client.api_call(url)

    def download_document_attachment(self, doc_id, attachment_id):
        """
        Downloads a document attachment file (latest version).

        Args:
            doc_id (str): ID of the document
            attachment_id (str): ID of the attachment

        Returns:
            bytes: Binary content of the attachment file

        Notes:
            On SUCCESS, Vault retrieves the latest version of the attachment from the document.
            The file name is the same as the attachment file name.

            The HTTP Response Header Content-Type is set to the MIME type of the file.
            If the MIME type cannot be detected, Content-Type is set to application/octet-stream.
            For small files, the Content-Length header will show the file size.
            For larger files, Transfer-Encoding is set to chunked and Content-Length is not displayed.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments/{attachment_id}/file"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content

    def download_document_attachment_version(
        self, doc_id, attachment_id, attachment_version
    ):
        """
        Downloads a specific version of a document attachment file.

        Args:
            doc_id (str): ID of the document
            attachment_id (str): ID of the attachment
            attachment_version (str): Version of the attachment to download

        Returns:
            bytes: Binary content of the attachment file

        Notes:
            On SUCCESS, Vault retrieves the specified version of the attachment from the document.
            The file name is the same as the attachment file name.

            The HTTP Response Header Content-Type is set to the MIME type of the file.
            If the MIME type cannot be detected, Content-Type is set to application/octet-stream.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments/{attachment_id}/versions/{attachment_version}/file"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content

    def download_document_version_attachment_version(
        self, doc_id, major_version, minor_version, attachment_id, attachment_version
    ):
        """
        Downloads a specific attachment version from a specific document version.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number of the document
            minor_version (int): Minor version number of the document
            attachment_id (str): ID of the attachment
            attachment_version (str): Version of the attachment to download

        Returns:
            bytes: Binary content of the attachment file

        Notes:
            On SUCCESS, Vault retrieves the specified attachment version from the specified document version.
            The file name is the same as the attachment file name.

            The HTTP Response Header Content-Type is set to the MIME type of the file.
            If the MIME type cannot be detected, Content-Type is set to application/octet-stream.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/attachments/{attachment_id}/versions/{attachment_version}/file"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content

    def download_all_document_attachments(self, doc_id):
        """
        Downloads all attachments for a document as a ZIP file.

        Args:
            doc_id (str): ID of the document

        Returns:
            bytes: Binary content of the ZIP file containing all attachments

        Notes:
            On SUCCESS, Vault retrieves the latest version of all attachments from the document.
            The attachments are packaged in a ZIP file with the file name:
            Document {document number} (v. {major version}.{minor version}) - attachments.zip.

            The HTTP Response Header Content-Type is set to application/zip.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments/files"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content

    def download_all_document_version_attachments(
        self, doc_id, major_version, minor_version
    ):
        """
        Downloads all attachments for a specific document version as a ZIP file.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number of the document
            minor_version (int): Minor version number of the document

        Returns:
            bytes: Binary content of the ZIP file containing all attachments

        Notes:
            On SUCCESS, Vault retrieves the latest version of all attachments from the specified
            version of the document. The file name is the same as the attachment file name.

            The HTTP Response Header Content-Type is set to the MIME type of the file.
            If the MIME type cannot be detected, Content-Type is set to application/octet-stream.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/attachments/file"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content

    def delete_single_document_attachment(self, doc_id, attachment_id):
        """
        Deletes a document attachment.

        Args:
            doc_id (str): ID of the document
            attachment_id (str): ID of the attachment to delete

        Returns:
            dict: API response with deletion status
                  Example:
                  {
                      "responseStatus": "SUCCESS"
                  }

        Notes:
            On SUCCESS, Vault deletes the specific attachment and all its versions.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments/{attachment_id}"

        return self.client.api_call(url, method="DELETE")

    def delete_single_document_attachment_version(
        self, doc_id, attachment_id, attachment_version
    ):
        """
        Deletes a specific version of a document attachment.

        Args:
            doc_id (str): ID of the document
            attachment_id (str): ID of the attachment
            attachment_version (str): Version of the attachment to delete

        Returns:
            dict: API response with deletion status
                  Example:
                  {
                      "responseStatus": "SUCCESS"
                  }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments/{attachment_id}/versions/{attachment_version}"

        return self.client.api_call(url, method="DELETE")

    def delete_multiple_document_attachments(
        self, input_file, content_type="text/csv", accept="text/csv", id_param=None
    ):
        """
        Deletes multiple document attachments in bulk.

        Args:
            input_file (str): Path to the file containing attachment details to delete
            content_type (str): Content type of the input file (default: text/csv)
            accept (str): Expected response format (default: text/csv)
            id_param (str, optional): Field name used to identify attachments in the input
                                      Add idParam=external_id__v if identifying attachments by external id

        Returns:
            dict: API response with deletion status
                  Example:
                  {
                      "responseStatus": "SUCCESS",
                      "data": [
                          {
                              "responseStatus": "SUCCESS",
                              "id": 26
                          }
                      ]
                  }

        Notes:
            Delete multiple document attachments in bulk with a JSON or CSV input file.
            This works for version-specific attachments and attachments at the document level.

            - The maximum input file size is 1GB
            - The values in the input must be UTF-8 encoded
            - CSVs must follow the standard RFC 4180 format, with some exceptions
            - The maximum batch size is 500

            Input file fields:
            - id (conditional): The attachment ID to delete
            - external_id__v (optional): Identify documents by their external ID
            - document_id__v (optional): The source document id value
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/attachments/batch"

        headers = {"Content-Type": content_type, "Accept": accept}

        params = {}
        if id_param:
            params["idParam"] = id_param

        with open(input_file, "rb") as file:
            return self.client.api_call(
                url, method="DELETE", headers=headers, params=params, data=file
            )

    def create_document_attachment(self, doc_id, file_path):
        """
        Adds an attachment to a document.

        Args:
            doc_id (str): ID of the document
            file_path (str): Path to the file to attach

        Returns:
            dict: API response with details of the created attachment
                  Example:
                  {
                      "responseStatus": "SUCCESS",
                      "data":
                      {
                          "id": "567",
                          "version__v": 3
                      }
                  }

        Notes:
            Create an attachment on the latest version of a document. If the attachment already exists,
            Vault uploads the attachment as a new version of the existing attachment.

            To create a version-specific attachment, or to create multiple attachments at once,
            use the bulk API.

            The maximum allowed file size is 2GB.
        """
        url = (
            f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments"
        )

        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            return self.client.api_call(url, method="POST", files=files)

    def create_multiple_document_attachments(self, input_file_path):
        """
        Adds multiple attachments to documents in bulk.

        Args:
            input_file_path (str): Path to the CSV file containing attachment details

        Returns:
            dict: API response with details of the created attachments
                  Example:
                  {
                      "responseStatus": "SUCCESS",
                      "data": [
                          {
                              "responseStatus": "SUCCESS",
                              "id": 39,
                              "version": 1
                          }
                      ]
                  }

        Notes:
            Create multiple document attachments in bulk with a JSON or CSV input file.
            You must first load the attachments to file staging.
            This works for version-specific attachments and attachments at the document level.

            - The maximum input file size is 1GB
            - The values in the input must be UTF-8 encoded
            - CSVs must follow the standard RFC 4180 format, with some exceptions
            - The maximum batch size is 500

            Input file fields:
            - document_id__v (required): The document ID to add this attachment
            - filename__v (required): The name for the new attachment including file extension
            - file (required): The filepath of the attachment on file staging
            - description__v (optional): Description of the attachment. Maximum 1000 characters
            - major_version_number__v (optional): The major version of the source document
            - minor_version_number__v (optional): The minor version of the source document
            - external_id__v (optional): Set an external ID value on the attachment
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/attachments/batch"

        headers = {"Content-Type": "text/csv", "Accept": "text/csv"}

        with open(input_file_path, "rb") as file:
            return self.client.api_call(url, method="POST", headers=headers, data=file)

    def restore_document_attachment_version(
        self, doc_id, attachment_id, attachment_version
    ):
        """
        Restores a specific version of a document attachment.

        Args:
            doc_id (str): ID of the document
            attachment_id (str): ID of the attachment
            attachment_version (str): Version of the attachment to restore

        Returns:
            dict: API response with restoration status
                  Example:
                  {
                      "responseStatus": "SUCCESS",
                      "data":
                      {
                          "id": "567",
                          "version__v": 3
                      }
                  }

        Notes:
            On SUCCESS, Vault restores the specific version of an existing attachment to make
            it the latest version. The response will contain the attachment ID and version
            of the restored attachment.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments/{attachment_id}/versions/{attachment_version}/restore"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(url, method="POST", headers=headers)

    def update_document_attachment_description(
        self, doc_id, attachment_id, description
    ):
        """
        Updates the description of a document attachment.

        Args:
            doc_id (str): ID of the document
            attachment_id (str): ID of the attachment
            description (str): New description for the attachment (maximum 1000 characters)

        Returns:
            dict: API response with update status
                  Example:
                  {
                      "responseStatus": "SUCCESS"
                  }

        Notes:
            Update an attachment on the latest version of a document.
            To update a version-specific attachment, or to update multiple attachments at once,
            use the bulk API.

            description__v is the only editable field. Maximum character length is 1000.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/attachments/{attachment_id}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"description__v": description}

        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def update_multiple_document_attachment_descriptions(
        self, input_file_path, id_param=None
    ):
        """
        Updates descriptions for multiple document attachments in bulk.

        Args:
            input_file_path (str): Path to the CSV file containing attachment descriptions
            id_param (str, optional): Field name used to identify attachments in the input
                                    Add idParam=external_id__v if identifying attachments by external id

        Returns:
            dict: API response with update status
                  Example:
                  {
                      "responseStatus": "SUCCESS",
                      "data": [
                          {
                              "responseStatus": "SUCCESS",
                              "id": 38,
                              "version": 2
                          }
                      ]
                  }

        Notes:
            Update multiple document attachments in bulk with a JSON or CSV input file.
            This works for version-specific attachments and attachments at the document level.
            You can only update the latest version of an attachment.

            - The maximum input file size is 1GB
            - The values in the input must be UTF-8 encoded
            - CSVs must follow the standard RFC 4180 format, with some exceptions
            - The maximum batch size is 500

            Input file fields:
            - id (conditional): The attachment ID to update
            - external_id__v (conditional): Identify attachments by their external ID
            - description__v (required): Description of the attachment. Maximum 1,000 characters
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/attachments/batch"

        headers = {"Content-Type": "text/csv", "Accept": "text/csv"}

        params = {}
        if id_param:
            params["idParam"] = id_param

        with open(input_file_path, "rb") as file:
            return self.client.api_call(
                url, method="PUT", headers=headers, params=params, data=file
            )
