import json
from .base_service import BaseBinderService


class BinderCreationService(BaseBinderService):
    """
    Service class for creating binders in Veeva Vault
    """

    def create_binder(self, binder_data, async_indexing=False):
        """
        Creates a new binder in Vault.

        When creating a binder, the binder metadata is indexed synchronously by default.
        To process the indexing asynchronously, set async_indexing to True.
        No file is included in the request when creating a binder.
        All required binder (document) fields must be included in the request.

        Args:
            binder_data (dict): Data for creating the binder containing all required fields
                               (name__v, type__v, subtype__v, lifecycle__v, etc.)
            async_indexing (bool): Whether to index the binder asynchronously to speed up
                                 response time when processing large amounts of data

        Returns:
            dict: API response containing details of the created binder
                 Example: {"responseStatus": "SUCCESS", "responseMessage": "Successfully created binder.", "id": 563}
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders"

        params = {}
        if async_indexing:
            params["async"] = "true"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(
            url, method="POST", headers=headers, data=binder_data, params=params
        )

    def create_binder_from_template(self, template_name, binder_data):
        """
        Creates a new binder in Vault using a specified template.

        Uses an existing binder template to create a new binder. Only templates of "kind": binder are allowed.
        All required binder (document) fields must be included in the request.
        No file is included in the request when creating a binder.

        Args:
            template_name (str): Name of the template to use as returned from the document metadata
                               (e.g., "ectd_compliance_package_template__v")
            binder_data (dict): Data for creating the binder containing all required fields
                               (name__v, type__v, subtype__v, lifecycle__v, etc.)

        Returns:
            dict: API response containing details of the created binder
                 Example: {"responseStatus": "SUCCESS", "responseMessage": "Successfully created binder.", "id": 565}
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        # Add template information to binder data
        binder_data_with_template = {**binder_data, "fromTemplate": template_name}

        return self.client.api_call(
            url, method="POST", headers=headers, data=binder_data_with_template
        )

    def create_binder_version(self, binder_id):
        """
        Creates a new draft version of an existing binder.

        Binders cannot be versioned with this endpoint if they exceed 10,000 nodes.
        Nodes include documents, sections, and component binders.

        Args:
            binder_id (str): ID of the binder

        Returns:
            dict: API response containing details of the new version
                 Example: {
                     "responseStatus": "SUCCESS",
                     "responseMessage": "New draft successfully created",
                     "major_version_number__v": 0,
                     "minor_version_number__v": 4
                 }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers)
