import json
from .base_service import BaseDocumentService


class DocumentRelationshipsService(BaseDocumentService):
    """
    Service class for managing document relationships in Veeva Vault.

    Document relationships connect documents to each other with specific relationship types.
    Standard relationship types (e.g., Based On, Original Source) cannot be created or deleted.
    """

    def retrieve_document_type_relationships(self, document_type):
        """
        Retrieves relationships for a specific document type.

        Args:
            document_type (str): The document type (e.g., 'promotional__c')

        Returns:
            dict: API response with document type relationship metadata including:
                - properties: Field metadata for relationships
                - relationshipTypes: Available relationship types for this document type
                - relationships: Relationship objects

        API Endpoint:
            GET /api/{version}/metadata/objects/documents/types/{type}/relationships
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/types/{document_type}/relationships"

        return self.client.api_call(url)

    def retrieve_document_relationships(self, doc_id, major_version, minor_version):
        """
        Retrieves all relationships for a specific document version.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number
            minor_version (int): Minor version number

        Returns:
            dict: API response with document relationships

        API Endpoint:
            GET /api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/relationships

        Notes:
            - When Strict Security Mode is on, if the user does not have explicit role-based View
              permission to the document, custom document relationships added at the subtype or
              classification level are not returned.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/relationships"

        return self.client.api_call(url)

    def retrieve_document_relationship(
        self, doc_id, major_version, minor_version, relationship_id
    ):
        """
        Retrieves details of a specific document relationship.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number
            minor_version (int): Minor version number
            relationship_id (str): ID of the relationship to retrieve

        Returns:
            dict: API response with document relationship details

        API Endpoint:
            GET /api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}

        Notes:
            - When Strict Security Mode is on, if the user does not have explicit role-based View
              permission to the document, custom document relationships added at the subtype or
              classification level are not returned.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}"

        return self.client.api_call(url)

    def create_document_relationship(
        self,
        doc_id,
        major_version,
        minor_version,
        target_doc_id,
        relationship_type,
        target_major_version=None,
        target_minor_version=None,
    ):
        """
        Creates a relationship between two documents.

        Args:
            doc_id (str): ID of the source document
            major_version (int): Major version number of the source document
            minor_version (int): Minor version number of the source document
            target_doc_id (str): ID of the target document
            relationship_type (str): Type of relationship
            target_major_version (int, optional): Major version of the target document.
                                                Required for target version-specific relationships.
            target_minor_version (int, optional): Minor version of the target document.
                                                Required for target version-specific relationships.

        Returns:
            dict: API response with details of the created relationship including the relationship ID

        API Endpoint:
            POST /api/{version}/objects/documents/{document_id}/versions/{major_version_number__v}/{minor_version_number__v}/relationships

        Notes:
            - You cannot create standard relationship types (e.g., Based On, Original Source)
            - For bulk operations, use the batch API instead
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/relationships"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = {"target_doc_id": target_doc_id, "relationship_type": relationship_type}

        if target_major_version is not None:
            data["target_major_version"] = target_major_version
        if target_minor_version is not None:
            data["target_minor_version"] = target_minor_version

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(data)
        )

    def create_multiple_document_relationships(
        self,
        relationships_data,
        id_param=None,
        format_type="json",
        migration_mode=False,
    ):
        """
        Creates relationships on multiple documents.

        Args:
            relationships_data (list/str): JSON list of relationship data or CSV content
            id_param (str, optional): To create relationships based on a unique field, set to a unique field name
            format_type (str): Format of input data - 'json' or 'csv'
            migration_mode (bool): When True, creates document relationships in migration mode

        Returns:
            dict: API response with details of the created relationships

        API Endpoint:
            POST /api/{version}/objects/documents/relationships/batch

        Notes:
            - Maximum input file size: 1GB
            - Input values must be UTF-8 encoded
            - CSVs must follow the standard RFC 4180 format
            - Maximum batch size: 1000 relationships
            - You cannot create standard relationship types (e.g., Based On, Original Source)
            - Required fields for all relationships:
                - source_doc_id__v: Document ID of the source document
                - target_doc_id__v: Document ID of the target document
                - relationship_type__v: Type of relationship
            - Additional fields for source version-specific relationships:
                - source_major_version__v: Major version of source document
                - source_minor_version__v: Minor version of source document
            - Additional fields for target version-specific relationships:
                - target_major_version__v: Major version of target document
                - target_minor_version__v: Minor version of target document
            - Migration mode requires Document Migration permission
        """
        url = (
            f"api/{self.client.LatestAPIversion}/objects/documents/relationships/batch"
        )

        # Set content type based on format
        content_type = "application/json" if format_type == "json" else "text/csv"
        headers = {"Content-Type": content_type, "Accept": content_type}

        # Add migration mode header if needed
        if migration_mode:
            headers["X-VaultAPI-MigrationMode"] = "true"

        # Add id_param if provided
        params = {}
        if id_param:
            params["idParam"] = id_param

        # For JSON, ensure data is properly formatted
        data = relationships_data
        if format_type == "json" and isinstance(relationships_data, list):
            data = json.dumps(relationships_data)

        return self.client.api_call(
            url, method="POST", headers=headers, params=params, data=data
        )

    def delete_document_relationship(
        self, doc_id, major_version, minor_version, relationship_id
    ):
        """
        Deletes a relationship from a document.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number of the document
            minor_version (int): Minor version number of the document
            relationship_id (str): ID of the relationship to delete

        Returns:
            dict: API response confirming deletion with the relationship ID

        API Endpoint:
            DELETE /api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}

        Notes:
            - You cannot delete standard relationship types (e.g., Based On, Original Source)
            - For bulk operations, use the batch API instead
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}"

        return self.client.api_call(url, method="DELETE")

    def delete_multiple_document_relationships(
        self, relationships_data, format_type="json"
    ):
        """
        Deletes relationships from multiple documents.

        Args:
            relationships_data (list/str): JSON list of relationship IDs or CSV content
            format_type (str): Format of input data - 'json' or 'csv'

        Returns:
            dict: API response confirming deletion with the relationship IDs

        API Endpoint:
            DELETE /api/{version}/objects/documents/relationships/batch

        Notes:
            - Maximum input file size: 1GB
            - Input values must be UTF-8 encoded
            - CSVs must follow the standard RFC 4180 format
            - Maximum batch size: 1000 relationships
            - You cannot delete standard relationship types (e.g., Based On, Original Source)
            - Required fields:
                - id: The ID of the relationship to delete
            - Some HTTP clients don't support DELETE requests with a body. For these cases,
              use POST method with _method=DELETE query parameter.
        """
        url = (
            f"api/{self.client.LatestAPIversion}/objects/documents/relationships/batch"
        )

        # Set content type based on format
        content_type = "application/json" if format_type == "json" else "text/csv"
        headers = {"Content-Type": content_type, "Accept": content_type}

        # For JSON, ensure data is properly formatted
        data = relationships_data
        if format_type == "json" and isinstance(relationships_data, list):
            data = json.dumps(relationships_data)

        return self.client.api_call(url, method="DELETE", headers=headers, data=data)

    # Legacy method - keeping for backward compatibility
    def create_single_document_relationship(
        self,
        document_id,
        major_version_number,
        minor_version_number,
        target_doc_id,
        relationship_type,
        target_major_version=None,
        target_minor_version=None,
    ):
        """
        Creates a relationship between two specific document versions.
        This is a legacy method - use create_document_relationship instead.

        Args:
            document_id (str): ID of the source document
            major_version_number (int): Major version number of the source document
            minor_version_number (int): Minor version number of the source document
            target_doc_id (str): ID of the target document
            relationship_type (str): Type of relationship
            target_major_version (int, optional): Major version of the target document
            target_minor_version (int, optional): Minor version of the target document

        Returns:
            dict: API response with details of the created relationship
        """
        return self.create_document_relationship(
            document_id,
            major_version_number,
            minor_version_number,
            target_doc_id,
            relationship_type,
            target_major_version,
            target_minor_version,
        )
