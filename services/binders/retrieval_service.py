from .base_service import BaseBinderService


class BinderRetrievalService(BaseBinderService):
    """
    Service class for retrieving binders from Veeva Vault.

    Binders in Vault are a special type of document that can contain documents and sections.
    This service provides methods to retrieve binders and their details.
    """

    def retrieve_all_binders(self):
        """
        Retrieves all binders in the vault.

        In Vault, binders are just another kind of document. This endpoint uses the document
        API endpoint and you can distinguish binders from regular documents by checking the
        'binder__v' field (true for binders, false for regular documents).

        Note: This endpoint does not retrieve binder sections or nested binders.
        Alternatively, VQL can be used to find just binders: SELECT id FROM binders.

        HTTP Method: GET
        Endpoint: /api/{version}/objects/documents

        Returns:
            dict: API response containing all documents, including binders where binder__v=true.
                  The response includes document metadata but not the binder structure.

        Response example:
        {
          "responseStatus": "SUCCESS",
          "size": 77,
          "start": 0,
          "limit": 200,
          "documents": [
            {
              "document": {
                "id": 101,
                "binder__v": true,
                "name__v": "CholeCap Presentation",
                ...
              }
            }
          ]
        }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents"

        return self.client.api_call(url)

    def retrieve_binder(self, binder_id, depth=None):
        """
        Retrieves details of a specific binder including its fields and structure.

        By default, the response only includes the first level (root) of the binder structure.
        To retrieve all levels, set the depth parameter to 'all'.

        HTTP Method: GET
        Endpoint: /api/{version}/objects/binders/{binder_id}

        Args:
            binder_id (str): ID of the binder to retrieve
            depth (str, optional): Depth of nodes to retrieve. Set to 'all' to retrieve all
                                   levels of the binder structure. By default, only the
                                   first level is returned.

        Returns:
            dict: API response containing binder details including document metadata
                 and binder structure according to the specified depth.

        Response includes:
        - document metadata
        - versions available
        - binder structure with nodes (documents and sections)
        - parent-child relationships for items in the binder

        For each node, the API returns:
        - order__v: Order of the node within the binder or section (may have accuracy issues)
        - section_number__v: Optional number for sections
        - type__v: Type of node (document or section)
        - document_id__v: The document ID (for document nodes)
        - id: The document or section ID specific to the binder
        - parent_id__v: Section ID of the parent node
        - name__v: Name of the document or section
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}"

        params = {}
        if depth:
            params["depth"] = depth

        return self.client.api_call(url, params=params)

    def retrieve_all_binder_versions(self, binder_id):
        """
        Retrieves all versions of a specific binder.

        Binders have versions just like regular documents.

        HTTP Method: GET
        Endpoint: /api/{version}/objects/binders/{binder_id}/versions

        Args:
            binder_id (str): ID of the binder

        Returns:
            dict: API response containing all versions of the binder

        Response example:
        {
          "responseStatus": "SUCCESS",
          "versions": [
            {
              "number": "0.1",
              "value": "https://vault-domain.veevavault.com/api/v25.2/objects/binders/29/versions/0/1"
            },
            {
              "number": "0.2",
              "value": "https://vault-domain.veevavault.com/api/v25.2/objects/binders/29/versions/0/2"
            }
          ]
        }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions"

        return self.client.api_call(url)

    def retrieve_binder_version(self, binder_id, major_version, minor_version):
        """
        Retrieves a specific version of a binder.

        HTTP Method: GET
        Endpoint: /api/{version}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}

        Args:
            binder_id (str): ID of the binder
            major_version (int): Major version number
            minor_version (int): Minor version number

        Returns:
            dict: API response containing the binder version details including
                 document metadata and the first level of binder structure

        For binders with unbound documents, the response includes versions based on
        binder display options for unbound documents set in the UI.

        If a child node is a binder bound to a specific version, the response includes
        the major and minor versions of that binder.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}"

        return self.client.api_call(url)
