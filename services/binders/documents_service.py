import json
from .base_service import BaseBinderService


class BinderDocumentsService(BaseBinderService):
    """
    Service class for managing documents within binders in Veeva Vault
    """

    def add_document_to_binder(
        self,
        binder_id,
        document_id,
        parent_id=None,
        order=None,
        binding_rule=None,
        major_version_number=None,
        minor_version_number=None,
    ):
        """
        Adds a document to a binder.

        Binders cannot exceed 50,000 nodes. Nodes include documents, sections, and component binders.
        If a binder has reached its limit, binder nodes cannot be added to the binder or any of its
        component binders, even if the component binders have not reached the 50,000 node limit.

        Args:
            binder_id (str): ID of the binder
            document_id (str): ID of the document to add (required)
            parent_id (str, optional): Section ID of the parent section, if the document will be in a
                                      section rather than top-level. Blank means adding the document
                                      at the top-level binder.
            order (int, optional): Position of the document within the binder or section.
                                  By default, new components appear below existing components.
                                  Note: There is a known issue affecting this parameter.
            binding_rule (str, optional): The binding rule indicating which version of the document
                                         will be linked to the binder and the ongoing behavior.
                                         Options are: 'default' (bind to the latest available version),
                                         'steady-state' (bind to latest version in a steady-state),
                                         'current' (bind to current version), or
                                         'specific' (bind to a specific version).
            major_version_number (int, optional): If binding_rule='specific', then this is required
                                                 and indicates the major version of the document to be linked.
            minor_version_number (int, optional): If binding_rule='specific', then this is required
                                                 and indicates the minor version of the document to be linked.

        Returns:
            dict: API response containing the Node ID of the added document
        """
        url = (
            f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/documents"
        )

        # Update header to match documentation (application/x-www-form-urlencoded)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        # Update parameter names to match API documentation
        data = {"document_id__v": document_id}

        if parent_id:
            data["parent_id__v"] = parent_id
        if order is not None:
            data["order__v"] = order
        if binding_rule:
            data["binding_rule__v"] = binding_rule
        if major_version_number is not None:
            data["major_version_number__v"] = major_version_number
        if minor_version_number is not None:
            data["minor_version_number__v"] = minor_version_number

        # Since the content type is application/x-www-form-urlencoded, we should not convert to JSON
        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def move_document_in_binder(
        self, binder_id, section_id, order=None, parent_id=None
    ):
        """
        Moves a document to a different position within a binder.

        Args:
            binder_id (str): ID of the binder
            section_id (str): The binder node id of the document to move
            order (int, optional): A number reflecting the new position of the document
                                  within the binder or section.
                                  Note: There is a known issue affecting this parameter.
            parent_id (str, optional): To move the document to a different section or from
                                      a section to the binder's root node, enter the value
                                      of the new parent node.

        Returns:
            dict: API response containing the new node ID of the document
        """
        # Fix the URL to match documentation - should use 'documents' not 'sections'
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/documents/{section_id}"

        # Update header to match documentation (application/x-www-form-urlencoded)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {}

        if order is not None:
            data["order__v"] = order
        if parent_id:
            data["parent_id__v"] = parent_id

        # Since the content type is application/x-www-form-urlencoded, we should not convert to JSON
        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def remove_document_from_binder(self, binder_id, section_id):
        """
        Removes a document from a binder.

        Args:
            binder_id (str): ID of the binder
            section_id (str): The binder node id of the document to remove

        Returns:
            dict: API response containing the Node ID of the deleted document
        """
        # Fix the URL to match documentation - should use 'documents' not 'sections'
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/documents/{section_id}"

        return self.client.api_call(url, method="DELETE")
