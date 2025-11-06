import os
import json
from typing import Dict, Any, Optional, Union, BinaryIO, List
from .base_service import BaseDocumentService


class DocumentCreationService(BaseDocumentService):
    """
    Service class for creating documents in Veeva Vault
    """

    def create_single_document(
        self,
        file_path=None,
        name_v=None,
        type_v=None,
        subtype_v=None,
        classification_v=None,
        lifecycle_v=None,
        major_version_number_v=None,
        minor_version_number_v=None,
        external_id_v=None,
        product_v=None,
        from_template=None,
        source_vault_id_v=None,
        source_document_id_v=None,
        source_binding_rule_v=None,
        bound_source_major_version_v=None,
        bound_source_minor_version_v=None,
        global_content_type_v=None,
        content_creation_currency_v=None,
        content_creation_cost_v=None,
        suppress_rendition=False,
        options=None,
    ):
        """
        Creates a new document in the Vault.

        There are multiple ways to create a document:
        1. From an uploaded file: Provide file_path and required fields
        2. From a template: Provide from_template and required fields
        3. Placeholder document: Omit file_path and provide required fields
        4. Unclassified document: Set type_v to "undefined__v" and lifecycle_v to "unclassified__v"
        5. CrossLink document: Provide source_vault_id_v, source_document_id_v, and required fields

        Args:
            file_path (str, optional): Path to the file to upload. Required when creating from uploaded file.
                                      The maximum allowed file size is 4GB.
            name_v (str, required): The name of the new document.
            type_v (str, required): The name or label of the document type to assign to the new document.
                                   For unclassified documents, set to "undefined__v".
            subtype_v (str, optional): The name or label of the document subtype (if one exists on the document type).
            classification_v (str, optional): The name or label of the document classification (if one exists on the document subtype).
            lifecycle_v (str, required): The name or label of the document lifecycle to assign to the new document.
                                        For unclassified documents, set to "unclassified__v".
            major_version_number_v (int, optional): The major version number to assign to the new document.
            minor_version_number_v (int, optional): The minor version number to assign to the new document.
            external_id_v (str, optional): An external identifier for the document.
            product_v (str, optional): The product reference for the document.
            from_template (str, optional): The name of the template to apply. Required when creating a document from a template.
            source_vault_id_v (str, optional): Required for CrossLink documents. The Vault id of the Vault containing the source document.
            source_document_id_v (str, optional): Required for CrossLink documents. The document id of the source document.
            source_binding_rule_v (str, optional): For CrossLink documents. Possible values: "Latest version",
                                                 "Latest Steady State version", or "Specific Document version".
                                                 Defaults to "Latest Steady State version".
            bound_source_major_version_v (int, optional): Required when source_binding_rule_v is "Specific Document version".
                                                        The major version number of the source document.
            bound_source_minor_version_v (int, optional): Required when source_binding_rule_v is "Specific Document version".
                                                        The minor version number of the source document.
            global_content_type_v (str, optional): For PromoMats Vaults. The name of the global content type.
            content_creation_currency_v (str, optional): For PromoMats Vaults. The id of the content creation currency type.
            content_creation_cost_v (str, optional): For PromoMats Vaults. The id of the content creation cost.
            suppress_rendition (bool, optional): Whether to suppress generation of viewable renditions. Default is False.
            options (dict, optional): Additional document options or fields.

        Returns:
            dict: API response containing details of the created document.
                 On SUCCESS, returns the document id in "id" field.
                 Example: {"responseStatus": "SUCCESS", "responseMessage": "successfully created document", "id": 773}
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents"

        # Prepare the document metadata
        data = {}

        # Required fields for most document types
        if name_v:
            data["name__v"] = name_v
        if type_v:
            data["type__v"] = type_v
        if lifecycle_v:
            data["lifecycle__v"] = lifecycle_v

        # Optional standard fields
        if subtype_v:
            data["subtype__v"] = subtype_v
        if classification_v:
            data["classification__v"] = classification_v
        if major_version_number_v is not None:
            data["major_version_number__v"] = major_version_number_v
        if minor_version_number_v is not None:
            data["minor_version_number__v"] = minor_version_number_v
        if external_id_v:
            data["external_id__v"] = external_id_v
        if product_v:
            data["product__v"] = product_v
        if from_template:
            data["fromTemplate"] = from_template

        # CrossLink document fields
        if source_vault_id_v:
            data["source_vault_id__v"] = source_vault_id_v
        if source_document_id_v:
            data["source_document_id__v"] = source_document_id_v
        if source_binding_rule_v:
            data["source_binding_rule__v"] = source_binding_rule_v
        if bound_source_major_version_v is not None:
            data["bound_source_major_version__v"] = bound_source_major_version_v
        if bound_source_minor_version_v is not None:
            data["bound_source_minor_version__v"] = bound_source_minor_version_v

        # PromoMats specific fields
        if global_content_type_v:
            data["global_content_type__v"] = global_content_type_v
        if content_creation_currency_v:
            data["content_creation_currency__v"] = content_creation_currency_v
        if content_creation_cost_v:
            data["content_creation_cost__v"] = content_creation_cost_v
        if suppress_rendition:
            data["suppressRendition"] = "true"

        # Add additional options if provided
        if options:
            for key, value in options.items():
                if key not in data:
                    data[key] = value

        # Different handling based on document creation type
        if file_path:
            # Create document from uploaded file
            with open(file_path, "rb") as file:
                files = {
                    "file": (os.path.basename(file_path), file),
                }

                # Add all data fields as form fields
                for key, value in data.items():
                    files[key] = (None, str(value))

                headers = {"Accept": "application/json"}
                return self.client.api_call(
                    url, method="POST", headers=headers, files=files
                )
        else:
            # Create placeholder, template-based, or CrossLink document
            headers = {
                "Content-Type": "multipart/form-data",
                "Accept": "application/json",
            }

            files = {}
            for key, value in data.items():
                files[key] = (None, str(value))

            return self.client.api_call(
                url, method="POST", headers=headers, files=files
            )

    def create_document_with_binary(
        self,
        binary_data,
        filename,
        name_v,
        type_v,
        subtype_v=None,
        classification_v=None,
        lifecycle_v=None,
        major_version_number_v=None,
        minor_version_number_v=None,
        external_id_v=None,
        product_v=None,
        suppress_rendition=False,
        options=None,
    ):
        """
        Creates a new document using binary data instead of a file path.
        This is useful when the file content is already in memory.

        Args:
            binary_data (bytes): Binary content of the file. Maximum allowed file size is 4GB.
            filename (str): Name of the file.
            name_v (str, required): The name of the new document.
            type_v (str, required): The name or label of the document type to assign to the new document.
            subtype_v (str, optional): The name or label of the document subtype (if one exists on the document type).
            classification_v (str, optional): The name or label of the document classification (if one exists on the document subtype).
            lifecycle_v (str, required): The name or label of the document lifecycle to assign to the new document.
            major_version_number_v (int, optional): The major version number to assign to the new document.
            minor_version_number_v (int, optional): The minor version number to assign to the new document.
            external_id_v (str, optional): An external identifier for the document.
            product_v (str, optional): The product reference for the document.
            suppress_rendition (bool, optional): Whether to suppress generation of viewable renditions. Default is False.
            options (dict, optional): Additional document options or fields.

        Returns:
            dict: API response containing details of the created document.
                 On SUCCESS, returns the document id in "id" field.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents"

        # Prepare the document metadata
        data = {"name__v": name_v, "type__v": type_v, "lifecycle__v": lifecycle_v}

        # Add optional parameters if provided
        if subtype_v:
            data["subtype__v"] = subtype_v
        if classification_v:
            data["classification__v"] = classification_v
        if major_version_number_v is not None:
            data["major_version_number__v"] = major_version_number_v
        if minor_version_number_v is not None:
            data["minor_version_number__v"] = minor_version_number_v
        if external_id_v:
            data["external_id__v"] = external_id_v
        if product_v:
            data["product__v"] = product_v
        if suppress_rendition:
            data["suppressRendition"] = "true"

        # Add additional options if provided
        if options:
            for key, value in options.items():
                if key not in data:
                    data[key] = value

        files = {
            "file": (filename, binary_data),
        }

        # Add all data fields as form fields
        for key, value in data.items():
            files[key] = (None, str(value))

        headers = {"Accept": "application/json"}
        return self.client.api_call(url, method="POST", headers=headers, files=files)

    def create_multiple_documents(self, csv_data):
        """
        Creates multiple documents at once with a CSV input.

        This endpoint allows creating up to 500 documents in a single batch operation.
        The CSV must follow the RFC 4180 format and be UTF-8 encoded.

        Args:
            csv_data (str or bytes): CSV data containing document information.
                The CSV should include columns for required fields such as:
                - file: Filepath of the source document (required for uploaded files)
                - name__v: Name of the new document
                - type__v: Document type
                - subtype__v: Document subtype (if applicable)
                - classification__v: Document classification (if applicable)
                - lifecycle__v: Document lifecycle
                - major_version_number__v: Major version number (optional)
                - minor_version_number__v: Minor version number (optional)
                - suppressRendition: Set to true to suppress rendition generation (optional)

                For template-based documents, include 'fromTemplate' column instead of 'file'.

                For content placeholders, include the 'file' column but leave values blank.

                For unclassified documents, set type__v to "undefined__v" and
                lifecycle__v to "unclassified__v".

        Returns:
            dict: API response with details of created documents, including success/failure status for each document.
                 Example:
                 {
                     "responseStatus": "SUCCESS",
                     "data": [
                         {
                             "responseStatus": "SUCCESS",
                             "id": 771,
                             "external_id__v": "ALT-DOC-0771"
                         },
                         {
                             "responseStatus": "FAILURE",
                             "errors": [
                                 {
                                     "type": "INVALID_DATA",
                                     "message": "Error message describing why this document was not created."
                                 }
                             ]
                         }
                     ]
                 }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/batch"

        headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        # Ensure csv_data is bytes
        if isinstance(csv_data, str):
            csv_data = csv_data.encode("utf-8")

        return self.client.api_call(url, method="POST", headers=headers, data=csv_data)

    def create_single_document_version(
        self,
        doc_id,
        create_draft=True,
        file_path=None,
        description=None,
        suppress_rendition=False,
    ):
        """
        Creates a new version of an existing document.

        Args:
            doc_id (str): ID of the document
            create_draft (bool): Whether to create a draft version. Default is True.
            file_path (str, optional): Path to the file for the new version
            description (str, optional): Description of the new version
            suppress_rendition (bool): Whether to suppress rendition generation. Default is False.

        Returns:
            dict: API response with details of the created document version
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions"

        # Prepare parameters
        params = {
            "draft": "true" if create_draft else "false",
            "suppressRendition": "true" if suppress_rendition else "false",
        }

        # Prepare data
        data = {}
        if description:
            data["description__v"] = description

        # Prepare headers and files
        if file_path:
            with open(file_path, "rb") as file:
                files = {
                    "file": (os.path.basename(file_path), file),
                }

                # Add data fields as form fields if present
                if data:
                    for key, value in data.items():
                        files[key] = (None, str(value))

                return self.client.api_call(
                    url, method="POST", params=params, files=files
                )
        else:
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            return self.client.api_call(
                url,
                method="POST",
                headers=headers,
                params=params,
                data=json.dumps(data) if data else None,
            )

    def create_multiple_document_versions(self, csv_data, id_param=None):
        """
        Creates or adds document versions in bulk using CSV data.

        This endpoint allows you to create multiple document versions at once.
        The maximum CSV input file size is 1GB and must be UTF-8 encoded.

        Args:
            csv_data (str or bytes): CSV content containing version details
                The CSV should include columns such as:
                - id or external_id__v: Document identifier
                - file: Path to the source file
                - description__v: Version description (optional)
                - major_version_number__v: Major version number (optional)
                - minor_version_number__v: Minor version number (optional)

            id_param (str, optional): Field name used to identify documents in the input
                                     (e.g., "external_id__v" or "id")

        Returns:
            dict: API response with details of the created document versions
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/versions/batch"

        headers = {"Content-Type": "text/csv", "Accept": "application/json"}

        params = {}
        if id_param:
            params["idParam"] = id_param

        # Ensure csv_data is bytes
        if isinstance(csv_data, str):
            csv_data = csv_data.encode("utf-8")

        return self.client.api_call(
            url, method="POST", headers=headers, params=params, data=csv_data
        )
