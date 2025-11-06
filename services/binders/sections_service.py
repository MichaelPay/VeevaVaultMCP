import json
from .base_service import BaseBinderService


class BinderSectionsService(BaseBinderService):
    """
    Service class for managing binder sections in Veeva Vault

    Provides functionality to retrieve, create, update, and delete binder sections.
    Binders cannot exceed 50,000 nodes. Nodes include documents, sections, and component binders.
    """

    def retrieve_binder_sections(self, binder_id, section_id=None):
        """
        Retrieves sections of a binder (documents and subsections) from the top-level root node or a specific sub-level node.

        Args:
            binder_id (str): ID of the binder
            section_id (str, optional): ID of a specific section to retrieve. If not included, all sections
                                       from the binder's top-level root node will be returned.

        Returns:
            dict: API response containing binder sections with the following structure:
                - responseStatus: Status of the API call
                - binder.nodes: List of all nodes (documents and sections) at that level
                - node properties include: document_id__v, name__v, order__v, type__v (document or section),
                  id, parent_id__v, section_number__v
        """
        base_url = (
            f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/sections"
        )
        url = f"{base_url}/{section_id}" if section_id else base_url

        return self.client.api_call(url)

    def retrieve_binder_version_section(
        self, binder_id, major_version, minor_version, section_id=None
    ):
        """
        Retrieves sections of a specific binder version from the top-level root node or a specific sub-level node.

        Args:
            binder_id (str): ID of the binder
            major_version (int): Major version number
            minor_version (int): Minor version number
            section_id (str, optional): ID of a specific section to retrieve. If not included, all sections
                                       from the binder's top-level root node will be returned.

        Returns:
            dict: API response containing binder version sections with the same structure as retrieve_binder_sections
        """
        base_url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/sections"
        url = f"{base_url}/{section_id}" if section_id else base_url

        return self.client.api_call(url)

    def create_binder_section(
        self, binder_id, name, section_number=None, parent_id=None, order=None
    ):
        """
        Creates a new section in a binder.

        Binders cannot exceed 50,000 nodes. Nodes include documents, sections, and component binders.
        If a binder has reached its limit, binder nodes cannot be added to the binder or any of its component binders,
        even if the component binders have not reached the 50,000 node limit.

        Args:
            binder_id (str): ID of the binder
            name (str): Name of the section (required)
            section_number (str, optional): Numerical value for the section
            parent_id (str, optional): ID of the parent section. If not provided, the new section will become
                                      a top-level section in the binder.
            order (int, optional): Number reflecting the position of the section within the binder or parent section.
                                 By default, new components appear below existing components.
                                 Note: There is a known issue affecting this parameter. The values may not work as expected.

        Returns:
            dict: API response containing details of the created section, including:
                - responseStatus: Status of the API call
                - id: Node ID of the newly created section
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/sections"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = {"name__v": name}

        if section_number:
            data["section_number__v"] = section_number
        if parent_id:
            data["parent_id__v"] = parent_id
        if order is not None:
            data["order__v"] = order

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(data)
        )

    def update_binder_section(
        self,
        binder_id,
        node_id,
        name=None,
        section_number=None,
        order=None,
        parent_id=None,
    ):
        """
        Updates a binder section.

        Args:
            binder_id (str): ID of the binder
            node_id (str): ID of the section to update (corresponds to section_id__sys when querying binder nodes)
            name (str, optional): New name for the section
            section_number (str, optional): New section number
            order (int, optional): New order for the section within the binder or parent section.
                                 Note: There is a known issue affecting this parameter. The values may not work as expected.
            parent_id (str, optional): New parent section ID (corresponds to parent_section_id__sys when querying binder nodes).
                                     To move the section to a different section in the binder, include the value of the parent
                                     node where it will be moved.

        Returns:
            dict: API response containing details of the updated section, including:
                - responseStatus: Status of the API call
                - id: Node ID of the section
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/sections/{node_id}"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = {}

        if name:
            data["name__v"] = name
        if section_number:
            data["section_number__v"] = section_number
        if order is not None:
            data["order__v"] = order
        if parent_id:
            data["parent_id__v"] = parent_id

        return self.client.api_call(
            url, method="PUT", headers=headers, data=json.dumps(data)
        )

    def delete_binder_section(self, binder_id, section_id):
        """
        Deletes a section from a binder.

        Args:
            binder_id (str): ID of the binder
            section_id (str): ID of the section to delete (binder node id)

        Returns:
            dict: API response indicating success or failure, including:
                - responseStatus: Status of the API call
                - id: Node ID of the deleted section
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/sections/{section_id}"

        return self.client.api_call(url, method="DELETE")
