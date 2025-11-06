# edl_service.py
import json
import pandas as pd


class EDLService:
    """
    Service class for managing Expected Document Lists (EDLs) in Veeva Vault.

    EDLs help you to measure the completeness of projects. Note that if your Vault
    is configured to set milestone values by EDL item, these endpoints may trigger
    updates to a document's milestone fields.

    Note: These endpoints are not available for use in Clinical Operations Vaults.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        :param client: An initialized VaultClient instance
        """
        self.client = client

    def create_placeholder_from_edl_item(self, edl_item_ids):
        """
        Create a placeholder from an EDL item.

        Creates a placeholder from one or more EDL items. Learn about working with
        Content Placeholders in Vault Help.

        Args:
            edl_item_ids (list or str): A list of EDL Item ids or comma-separated string
                                        of EDL Item ids on which to initiate the action.

        Returns:
            dict: The API response containing job_id and url for checking job status
                  {
                      "responseStatus": "SUCCESS",
                      "job_id": 84201,
                      "url": "/api/v25.2/services/jobs/84201"
                  }
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/edl_item__v/actions/createplaceholder"

        if isinstance(edl_item_ids, list):
            edl_item_ids = ", ".join(edl_item_ids)

        data = {"edlItemIds": edl_item_ids}

        return self.client.api_call(
            url,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
        )

    def retrieve_all_root_nodes(self, hierarchy_or_template="edl_hierarchy__v"):
        """
        Retrieves all root EDL nodes and node metadata.

        Learn more about EDL hierarchies in Vault Help.

        Args:
            hierarchy_or_template (str): Choose to retrieve nodes for either
                                        "edl_hierarchy__v" or "edl_template__v".
                                        Default is "edl_hierarchy__v".

        Returns:
            dict: The API response containing root nodes data, for example:
                  {
                    "responseStatus": "SUCCESS",
                    "data": [
                      {
                        "id": "0000000000000JIT",
                        "order__v": 1,
                        "ref_type__v": "edl__v",
                        "ref_name__v": "NewEDL",
                        "url": "/vobjects/edl__v/0EL000000001901",
                        "ref_id__v": "0EL000000001901",
                        "parent_id__v": null
                      }
                    ]
                  }
        """
        url = f"api/{self.client.LatestAPIversion}/composites/trees/{hierarchy_or_template}"
        return self.client.api_call(url)

    def retrieve_specific_root_nodes(
        self, ref_ids, hierarchy_or_template="edl_hierarchy__v"
    ):
        """
        Retrieves the root node ID for the given EDL record IDs.

        Args:
            ref_ids (list): List of EDL record IDs whose root nodes you want to retrieve.
                            Maximum 1,000 IDs per request.
            hierarchy_or_template (str): Choose to retrieve nodes for either
                                        "edl_hierarchy__v" or "edl_template__v".
                                        Default is "edl_hierarchy__v".

        Returns:
            dict: The API response containing requested root node IDs, for example:
                  {
                    "responseStatus": "SUCCESS",
                    "data": [
                      {
                        "responseStatus": "SUCCESS",
                        "id": "0000000000000IR1",
                        "ref_id__v": "0EL000000000401"
                      }
                    ]
                  }
        """
        url = f"api/{self.client.LatestAPIversion}/composites/trees/{hierarchy_or_template}/actions/listnodes"

        data = [{"ref_id__v": ref_id} for ref_id in ref_ids]

        return self.client.api_call(url, method="POST", json=data)

    def retrieve_node_children(
        self, parent_node_id, hierarchy_or_template="edl_hierarchy__v"
    ):
        """
        Given an EDL node ID, retrieves immediate children (not grandchildren) of that node.

        Learn more about EDL hierarchies in Vault Help.

        Args:
            parent_node_id (str): The ID of a parent node in the hierarchy.
            hierarchy_or_template (str): Choose to retrieve node children for either
                                        "edl_hierarchy__v" or "edl_template__v".
                                        Default is "edl_hierarchy__v".

        Returns:
            dict: The API response containing children nodes data, for example:
                  {
                    "responseStatus": "SUCCESS",
                    "data": [
                      {
                        "id": "0000000000000JLL",
                        "order__v": 1,
                        "ref_type__v": "edl_item__v",
                        "ref_name__v": "NewEDL Child",
                        "url": "/vobjects/edl_item__v/0EI000000009401",
                        "ref_id__v": "0EI000000009401",
                        "parent_id__v": "0000000000000JIT"
                      }
                    ]
                  }
        """
        url = f"api/{self.client.LatestAPIversion}/composites/trees/{hierarchy_or_template}/{parent_node_id}/children"
        return self.client.api_call(url)

    def update_node_order(
        self,
        parent_node_id,
        child_node_id,
        new_order,
        hierarchy_or_template="edl_hierarchy__v",
    ):
        """
        Given an EDL parent node, update the order of its children.

        Args:
            parent_node_id (str): The ID of a parent node in the hierarchy.
            child_node_id (str): The ID of the child node to update.
            new_order (int): The new order for the node in the hierarchy (1, 2, etc.)
            hierarchy_or_template (str): Choose to update node order for either
                                        "edl_hierarchy__v" or "edl_template__v".
                                        Default is "edl_hierarchy__v".

        Returns:
            dict: The API response indicating success or failure:
                  {
                    "responseStatus": "SUCCESS"
                  }
        """
        url = f"api/{self.client.LatestAPIversion}/composites/trees/{hierarchy_or_template}/{parent_node_id}/children"

        data = {"id": child_node_id, "order__v": str(new_order)}

        return self.client.api_call(url, method="PUT", json=data)

    def add_edl_matched_documents(self, matches):
        """
        Add matched documents to EDL Items.

        You must have a security profile that grants the Application: EDL Matching:
        Edit Document Matches permission, and EDL Matched Document APIs must be enabled
        in your Vault. To enable this feature, contact Veeva Support.

        Args:
            matches (list): List of dictionaries with the following keys:
                - id (str, required): The EDL Item id to match to documents.
                  EDL Item records and their parent records must have a status__v of active__v.
                - document_id (str, required): The document id to match to an EDL Item.
                - major_version_number__v (int, optional): The major version number of a document.
                  Must be included with minor_version_number__v.
                - minor_version_number__v (int, optional): The minor version number of a document.
                  Must be included with major_version_number__v.
                - lock (bool, optional): If true, locks the EDL Item to match a specific steady state
                  document version or, if version numbers are omitted, the latest steady state
                  document version. If false or omitted, and version numbers are omitted, Vault
                  matches the latest version of the document without regard to state.

        Returns:
            dict: The API response with status and results for each document match
        """
        url = f"api/{self.client.LatestAPIversion}/objects/edl_matched_documents/batch/actions/add"
        return self.client.api_call(url, method="POST", json=matches)

    def remove_edl_matched_documents(self, matches):
        """
        Remove manually matched documents from EDL Items.

        You must have a security profile that grants the Application: EDL Matching:
        Edit Document Matches permission, and EDL Matched Document APIs must be enabled
        in your Vault. To enable this feature, contact Veeva Support.

        Args:
            matches (list): List of dictionaries with the following keys:
                - id (str, required): The EDL Item id to match to documents.
                  EDL Item records and their parent records must have a status__v of active__v.
                - document_id (str, required): The document id to match to an EDL Item.
                - major_version_number__v (int, optional): The major version number of a document.
                  Must be included with minor_version_number__v.
                - minor_version_number__v (int, optional): The minor version number of a document.
                  Must be included with major_version_number__v.
                - remove_locked (bool, optional): If true, removes a matched document from the
                  EDL Item even if the EDL Item is locked to a specific steady state document version.

        Returns:
            dict: The API response with status and results for each document match removal
        """
        url = f"api/{self.client.LatestAPIversion}/objects/edl_matched_documents/batch/actions/remove"
        return self.client.api_call(url, method="POST", json=matches)
