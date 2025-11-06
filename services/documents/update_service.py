import os
import json
from .base_service import BaseDocumentService


class DocumentUpdateService(BaseDocumentService):
    """
    Service class for updating documents in Veeva Vault
    """

    def update_single_document(self, doc_id, data, headers=None):
        """
        Updates editable field values on the latest version of a single document.
        Note that this endpoint does not allow you to update the archive__v field.

        Args:
            doc_id (int): The document id field value
            data (dict): A dictionary containing editable field values to update
            headers (dict, optional): Additional headers to include in the request,
                                      such as X-VaultAPI-MigrationMode to allow
                                      document number changes

        Returns:
            dict: API response containing the ID of the updated document

        Documentation:
            PUT /api/{version}/objects/documents/{doc_id}
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}"

        default_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        if headers:
            default_headers.update(headers)

        return self.client.api_call(
            url, method="PUT", headers=default_headers, data=data
        )

    def update_multiple_documents(self, data=None, headers=None, file_path=None):
        """
        Bulk update editable field values on multiple documents.
        You can only update the latest version of each document.
        The maximum CSV input file size is 1GB and batch size is 1,000.

        Args:
            data (dict, optional): When not using CSV, a dictionary containing
                                   docIds (comma-separated list) and field values to update
            headers (dict, optional): Additional headers to include in the request,
                                      such as X-VaultAPI-MigrationMode
            file_path (str, optional): Path to a CSV file containing the updates

        Returns:
            dict: API response containing details of the updated documents

        Documentation:
            PUT /api/{version}/objects/documents/batch
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/batch"

        # Determine content type based on whether we're using CSV file or form data
        content_type = "text/csv" if file_path else "application/x-www-form-urlencoded"

        default_headers = {
            "Content-Type": content_type,
            "Accept": "application/json",
        }

        if headers:
            default_headers.update(headers)

        if file_path:
            with open(file_path, "rb") as file:
                return self.client.api_call(
                    url, method="PUT", headers=default_headers, data=file
                )
        else:
            if isinstance(data, dict):
                data = json.dumps(data)
            return self.client.api_call(
                url, method="PUT", headers=default_headers, data=data
            )

    def reclassify_single_document(
        self,
        doc_id,
        type_v,
        lifecycle_v,
        subtype_v=None,
        classification_v=None,
        document_number_v=None,
        status_v=None,
        reclassify=True,
    ):
        """
        Reclassifies a single document, enabling the change of document type
        or the assignment of a document type to an unclassified document.
        This endpoint is analogous to the Reclassify action in the Vault UI.

        Not all documents are eligible for reclassification. For example,
        you can only reclassify the latest version of a document and you
        cannot reclassify a checked out document.

        Args:
            doc_id (str): The document id field value
            type_v (str): The name of the document type
            lifecycle_v (str): The name of the document lifecycle
            subtype_v (str, optional): The name of the document subtype (if one exists on the type)
            classification_v (str, optional): The name of the document classification (if one exists on the subtype)
            document_number_v (str, optional): The document number for the reclassified document (requires X-VaultAPI-MigrationMode)
            status_v (str, optional): Specifies the document lifecycle state (requires X-VaultAPI-MigrationMode)
            reclassify (bool): Must be set to true to perform reclassification. Defaults to True

        Returns:
            dict: API response containing the ID of the reclassified document

        Documentation:
            PUT /api/{version}/objects/documents/{doc_id}
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {
            "type__v": type_v,
            "lifecycle__v": lifecycle_v,
            "reclassify": "true" if reclassify else "false",
        }

        if subtype_v:
            data["subtype__v"] = subtype_v
        if classification_v:
            data["classification__v"] = classification_v
        if document_number_v:
            data["document_number__v"] = document_number_v
            headers["X-VaultAPI-MigrationMode"] = "true"
        if status_v:
            data["status__v"] = status_v
            headers["X-VaultAPI-MigrationMode"] = "true"

        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def reclassify_multiple_documents(self, csv_file_path, headers=None):
        """
        Reclassifies documents in bulk. Allows you to change the document type
        of existing documents or assign document types to unclassified documents.

        Not all documents are eligible for reclassification.
        The maximum CSV input file size is 1GB and batch size is 500.

        Args:
            csv_file_path (str): The path to the CSV file containing the details
                                 of the documents to be reclassified
            headers (dict, optional): Additional headers to include in the request,
                                      such as X-VaultAPI-MigrationMode

        Returns:
            dict: API response containing the status and IDs of the reclassified documents

        Documentation:
            PUT /api/{version}/objects/documents/batch/actions/reclassify
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/batch/actions/reclassify"

        default_headers = {"Content-Type": "text/csv", "Accept": "text/csv"}

        if headers:
            default_headers.update(headers)

        with open(csv_file_path, "rb") as file:
            return self.client.api_call(
                url, method="PUT", headers=default_headers, data=file
            )

    def update_document_version(self, doc_id, major_version, minor_version, data):
        """
        Updates editable field values on a specific version of a document.

        Args:
            doc_id (int): The document id field value
            major_version (int): The document major_version_number__v field value
            minor_version (int): The document minor_version_number__v field value
            data (dict): A dictionary containing editable field values to update

        Returns:
            dict: API response containing the ID of the updated document

        Documentation:
            PUT /api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def create_multiple_document_versions(self, csv_file_path, headers=None):
        """
        Create or add document versions in bulk.

        The maximum CSV input file size is 1GB.
        The values in the input must be UTF-8 encoded.
        CSVs must follow the standard RFC 4180 format, with some exceptions.
        The maximum batch size is 500.

        Args:
            csv_file_path (str): The path to the CSV file containing the document
                                 versions to be created
            headers (dict, optional): Additional headers to include in the request.
                                      X-VaultAPI-MigrationMode must be set to true.

        Returns:
            dict: API response containing details of the created document versions

        Documentation:
            POST /api/{version}/objects/documents/versions/batch
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/versions/batch"

        default_headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        if headers:
            default_headers.update(headers)
        else:
            # X-VaultAPI-MigrationMode is required for this endpoint
            default_headers["X-VaultAPI-MigrationMode"] = "true"

        with open(csv_file_path, "rb") as file:
            return self.client.api_call(
                url, method="POST", headers=default_headers, data=file
            )

    def create_single_document_version(
        self,
        doc_id,
        create_draft=None,
        file_path=None,
        description=None,
        suppress_rendition=False,
    ):
        """
        Add a new draft version of an existing document. You can choose to either
        use the existing source file or a new source file. These actions increase
        the target document's minor version number.

        Not all documents are eligible for draft creation. For example, you cannot
        create a draft of a checked-out document.

        Args:
            doc_id (str): The document id field value
            create_draft (str, optional): Either 'latestContent' to use existing document
                                          or 'uploadedContent' to use a new file
            file_path (str, optional): Path to the new file (required if createDraft=uploadedContent
                                       or for placeholder documents)
            description (str, optional): Version Description for the new draft version
                                        (maximum 1,500 characters)
            suppress_rendition (bool): Set to true to suppress automatic generation
                                      of the viewable rendition. Defaults to False.

        Returns:
            dict: API response containing details of the new document version

        Documentation:
            POST /api/{version}/objects/documents/{doc_id}
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}"

        if suppress_rendition:
            url += "?suppressRendition=true"

        headers = {"Content-Type": "multipart/form-data", "Accept": "application/json"}

        data = {}
        files = {}

        if create_draft:
            data["createDraft"] = create_draft

        if description:
            data["description__v"] = description

        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as file:
                files["file"] = (os.path.basename(file_path), file)

        return self.client.api_call(
            url, method="POST", headers=headers, data=data, files=files
        )

    def update_document_content(
        self,
        doc_id,
        file_path,
        comment=None,
        reuse_file=False,
        make_latest_version=False,
    ):
        """
        Updates the content file of a document.

        Args:
            doc_id (str): ID of the document to update
            file_path (str): Path to the new file
            comment (str, optional): Comment for the new version
            reuse_file (bool): Whether to reuse an existing file of the same name
            make_latest_version (bool): Whether to make the new version the latest version

        Returns:
            dict: API response with details of the updated document
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/file"

        # Prepare parameters
        params = {}
        if reuse_file:
            params["reuse_file"] = "true"
        if make_latest_version:
            params["make_latest_version"] = "true"

        # Prepare data
        data = {}
        if comment:
            data["comment__v"] = comment

        # Prepare files
        with open(file_path, "rb") as file:
            files = {
                "file": (os.path.basename(file_path), file),
                "data": (None, json.dumps(data) if data else None),
            }

        return self.client.api_call(url, method="POST", params=params, files=files)

    def update_document_metadata(self, doc_id, metadata):
        """
        Updates the metadata of a document.

        Args:
            doc_id (str): ID of the document
            metadata (dict): Updated metadata fields

        Returns:
            dict: API response with details of the updated document
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(metadata)

        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def classify_document(
        self, doc_id, type_v, subtype_v=None, classification_v=None, lifecycle_v=None
    ):
        """
        Updates the classification of a document.

        Args:
            doc_id (str): ID of the document
            type_v (str): New document type
            subtype_v (str, optional): New document subtype
            classification_v (str, optional): New document classification
            lifecycle_v (str, optional): New document lifecycle

        Returns:
            dict: API response with details of the updated document
        """
        url = (
            f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/reclassify"
        )

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = {"type__v": type_v}

        if subtype_v:
            data["subtype__v"] = subtype_v
        if classification_v:
            data["classification__v"] = classification_v
        if lifecycle_v:
            data["lifecycle__v"] = lifecycle_v

        return self.client.api_call(
            url, method="PUT", headers=headers, data=json.dumps(data)
        )

    def init_document_workflow(
        self, doc_id, workflow_name, participants=None, due_date=None, description=None
    ):
        """
        Initiates a workflow for a document.

        Args:
            doc_id (str): ID of the document
            workflow_name (str): Name of the workflow to initiate
            participants (dict, optional): Mapping of roles to users/groups
            due_date (str, optional): Due date for the workflow (ISO format)
            description (str, optional): Description of the workflow

        Returns:
            dict: API response with details of the initiated workflow
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/workflows"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = {"name__v": workflow_name}

        if participants:
            data["participants__v"] = participants
        if due_date:
            data["due_date__v"] = due_date
        if description:
            data["description__v"] = description

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(data)
        )

    def retrieve_document_workflows(self, doc_id):
        """
        Retrieves all workflows for a document.

        Args:
            doc_id (str): ID of the document

        Returns:
            dict: API response with details of document workflows
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/workflows"

        return self.client.api_call(url)
