import json
from .base_service import BaseBinderService


class BinderRelationshipsService(BaseBinderService):
    """
    Service class for managing binder relationships in Veeva Vault
    """

    def retrieve_binder_relationship(
        self, binder_id, major_version, minor_version, relationship_id
    ):
        """
        Retrieves a specific relationship for a binder version.

        GET /api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}

        Headers:
            Accept: application/json (default) or application/xml

        URI Path Parameters:
            binder_id: The binder id field value.
            major_version: The binder major_version_number__v field value.
            minor_version: The binder minor_version_number__v field value.
            relationship_id: The binder relationship id field value.

        Response Details:
            id: Relationship ID.
            source_doc_id: Document ID of the source document.
            relationship_type__v: Relationship type
            created_by__v: User ID of user who created the relationship
            created_date__v: Timestamp when the relationship was created
            target_doc_id__v: Document ID for target document
            target_major_version__v: Major version of the target document; null values indicate that the relationship applies to all major versions
            target_minor_version__v: Minor version of the target document; null values indicate that the relationship applies to all minor versions

        Args:
            binder_id (str): ID of the binder
            major_version (int): Major version number
            minor_version (int): Minor version number
            relationship_id (str): ID of the relationship

        Returns:
            dict: API response containing the relationship details
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}"

        return self.client.api_call(url)

    def create_binder_relationship(
        self,
        binder_id,
        major_version,
        minor_version,
        target_doc_id,
        relationship_type,
        target_major_version=None,
        target_minor_version=None,
    ):
        """
        Creates a relationship between a binder version and a document.

        POST /api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/relationships

        Headers:
            Content-Type: application/x-www-form-urlencoded
            Accept: application/json (default) or application/xml

        URI Path Parameters:
            binder_id: The binder id field value.
            major_version: The binder major_version_number__v field value.
            minor_version: The binder minor_version_number__v field value.

        Body Parameters:
            target_doc_id__v (required): Set the target_doc_id__v to the document id of the "target document"
                to which a relationship will be established with the binder.
            relationship_type__v (required): Set the relationship_type__v to the field value of one of the
                desired relationshipTypes from the "Documents Relationships Metadata" call.
            target_major_version__v (optional): If you're creating a relationship with a specific version of
                the target document, set the target_major_version__v to the major version number of the target document.
            target_minor_version__v (optional): If you're creating a relationship with a specific version of
                the target document, set the target_minor_version__v to the minor version number of the target document.

        Args:
            binder_id (str): ID of the binder
            major_version (int): Major version number
            minor_version (int): Minor version number
            target_doc_id (str): ID of the target document
            relationship_type (str): Type of relationship
            target_major_version (int, optional): Major version of the target document
            target_minor_version (int, optional): Minor version of the target document

        Returns:
            dict: API response containing the created relationship
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/relationships"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {
            "target_doc_id__v": target_doc_id,
            "relationship_type__v": relationship_type,
        }

        if target_major_version is not None:
            data["target_major_version__v"] = target_major_version
        if target_minor_version is not None:
            data["target_minor_version__v"] = target_minor_version

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def delete_binder_relationship(
        self, binder_id, major_version, minor_version, relationship_id
    ):
        """
        Deletes a relationship from a binder version.

        DELETE /api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}

        Headers:
            Accept: application/json (default) or application/xml

        URI Path Parameters:
            binder_id: The binder id field value.
            major_version: The binder major_version_number__v field value.
            minor_version: The binder minor_version_number__v field value.
            relationship_id: The binder relationship id field value.

        Args:
            binder_id (str): ID of the binder
            major_version (int): Major version number
            minor_version (int): Minor version number
            relationship_id (str): ID of the relationship

        Returns:
            dict: API response indicating success or failure
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/relationships/{relationship_id}"

        return self.client.api_call(url, method="DELETE")
