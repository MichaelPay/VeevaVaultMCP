from .base_service import BaseBinderService


class BinderDeletionService(BaseBinderService):
    """
    Service class for deleting binders in Veeva Vault
    """

    def delete_binder(self, binder_id):
        """
        Deletes a binder from the vault.

        HTTP Method: DELETE
        Endpoint: api/{version}/objects/binders/{binder_id}

        Args:
            binder_id (str): The binder 'id' field value to delete

        Returns:
            dict: API response with format:
                {
                  "responseStatus": "SUCCESS",
                  "id": <id>
                }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}"

        return self.client.api_call(url, method="DELETE")

    def delete_binder_version(self, binder_id, major_version, minor_version):
        """
        Deletes a specific version of a binder.

        HTTP Method: DELETE
        Endpoint: api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}

        Args:
            binder_id (str): The binder 'id' field value
            major_version (int): The binder 'major_version_number__v' field value
            minor_version (int): The binder 'minor_version_number__v' field value

        Returns:
            dict: API response with format:
                {
                  "responseStatus": "SUCCESS",
                  "id": <id>
                }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}"

        return self.client.api_call(url, method="DELETE")
