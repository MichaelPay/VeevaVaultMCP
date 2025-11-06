import json
from .base_service import BaseBinderService


class BinderUpdateService(BaseBinderService):
    """
    Service class for updating binders in Veeva Vault
    """

    def update_binder(self, binder_id, data):
        """
        Updates an existing binder.

        Args:
            binder_id (str): ID of the binder to update
            data (dict): Data for updating the binder

        Returns:
            dict: API response containing the ID of the updated binder and responseStatus
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def reclassify_binder(self, binder_id, reclassify_data):
        """
        Reclassifies a binder (changes its document type, subtype, classification, etc.).

        A document "type" is the combination of the type__v, subtype__v, and classification__v
        fields on a binder. When you reclassify, Vault may add or remove certain fields on the binder.

        Limitations:
        - You can only reclassify the latest version of a binder
        - You can only reclassify one binder at a time
        - Bulk reclassify is not currently supported

        Args:
            binder_id (str): ID of the binder to reclassify
            reclassify_data (dict): Data for reclassification, must include reclassify=true
                                   and can include type__v, subtype__v, classification__v, lifecycle__v,
                                   plus any other editable fields

        Returns:
            dict: API response containing the ID of the reclassified binder and responseStatus
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}"

        # Ensure reclassify parameter is set to true
        reclassify_data["reclassify"] = "true"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(
            url, method="PUT", headers=headers, data=reclassify_data
        )

    def update_binder_version(
        self, binder_id, major_version, minor_version, update_data
    ):
        """
        Updates a specific version of a binder.

        Args:
            binder_id (str): ID of the binder
            major_version (int): Major version number
            minor_version (int): Minor version number
            update_data (dict): Data for updating the binder version

        Returns:
            dict: API response containing the ID of the updated binder and responseStatus
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(
            url, method="PUT", headers=headers, data=update_data
        )

    def refresh_binder_auto_filing(self, binder_id):
        """
        Refreshes the auto-filing rules for a binder.

        This is only available in eTMF Vaults on binders configured with the TMF Reference Models.
        This is analogous to the Refresh Auto-Filing action in the UI.

        Args:
            binder_id (str): ID of the binder

        Returns:
            dict: API response containing the responseStatus of the refresh operation
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/actions"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"action": "refresh_auto_filing"}

        return self.client.api_call(url, method="POST", headers=headers, data=data)
