from .base_service import BaseDocumentService
import json


class DocumentRetrievalService(BaseDocumentService):
    """
    Service class for retrieving documents from Veeva Vault.

    Implements endpoints for retrieving documents, document versions,
    downloading document files, and more as documented in the Veeva Vault API.
    """

    def retrieve_all_documents(
        self,
        named_filter=None,
        scope=None,
        versionscope=None,
        search=None,
        limit=None,
        sort=None,
        start=None,
    ):
        """
        Retrieve the latest version of documents and binders to which you have access.

        Vault only returns documents to which the logged in user has access,
        and returns a maximum of 200 documents per page by default.

        The boolean field binder__v indicates whether the returned document is a
        document (false) or a binder (true). The boolean field crosslink__v indicates
        whether the returned document is a regular document (false) or a CrossLink
        document (true).

        Args:
            named_filter (str, optional): Filters the results based on predefined options:
                - 'My Documents': Retrieves only documents which you have created.
                - 'Favorites': Retrieves only documents which you have marked as favorites.
                - 'Recent Documents': Retrieves only documents which you have recently accessed.
                - 'Cart': Retrieves only documents in your cart.
            scope (str, optional): Scope of the search:
                - 'contents': Searches only within the document content.
                - 'all': Searches both within the document content and searchable document fields.
            versionscope (str, optional): Scope of the versions to retrieve:
                - 'all': Retrieves all document versions.
                - None: Retrieves only the latest version (default).
            search (str, optional): Search keyword to filter documents based on searchable document fields.
            limit (int, optional): Limit the number of documents to display (default is up to 200 documents per page).
            sort (str, optional): Return documents in a specific order by specifying a document field and order.
                                 For example, 'name__v DESC'. The default is 'id ASC'.
            start (int, optional): The starting record number (default is 0).

        Returns:
            dict: JSON response with a list of documents and binders along with their fields and values.
                  On SUCCESS, Vault lists all documents and binders along with their fields and field values.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents"

        params = {
            "named_filter": named_filter,
            "scope": scope,
            "versionscope": versionscope,
            "search": search,
            "limit": limit,
            "sort": sort,
            "start": start,
        }

        # Filter out None values
        params = {k: v for k, v in params.items() if v is not None}

        return self.client.api_call(url, params=params)

    def retrieve_document(self, doc_id):
        """
        Retrieve all metadata from a document.

        The boolean field binder__v indicates whether the returned document is a
        regular document (false) or a binder (true). The absence of this field means
        it is a document. Binder node structures are not listed as part of the response.

        The boolean field crosslink__v indicates whether the returned document is a
        regular document (false) or a CrossLink document (true).

        Args:
            doc_id (str): The document id field value.

        Returns:
            dict: API response containing document details including metadata, renditions,
                 versions, and attachments. On SUCCESS, Vault returns all fields and values
                 for the specified document.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}"

        return self.client.api_call(url)

    def retrieve_document_versions(self, doc_id):
        """
        Retrieve all versions of a document.

        This endpoint returns a list of all available versions for the specified document,
        including URLs for accessing each version.

        Args:
            doc_id (str): The document id field value.

        Returns:
            dict: API response containing all document versions. On SUCCESS, Vault
                 returns a list of all available versions of the specified document
                 and any available renditions.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions"

        return self.client.api_call(url)

    def retrieve_document_version(self, doc_id, major_version, minor_version):
        """
        Retrieve all fields and values configured on a document version.

        This endpoint allows you to get detailed information about a specific
        version of a document.

        Args:
            doc_id (str): The document id field value.
            major_version (int): The document major_version_number__v field value.
            minor_version (int): The document minor_version_number__v field value.

        Returns:
            dict: API response containing document version details including metadata,
                 renditions, versions, and attachments. On SUCCESS, Vault returns all
                 fields and values for the specified version of the document.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}"

        return self.client.api_call(url)

    def retrieve_document_version_text(self, doc_id, major_version, minor_version):
        """
        Retrieve the plain text of a specific document version.

        Endpoint: GET /api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/text

        Args:
            doc_id (str): The document id field value.
            major_version (str): The document major_version_number__v field value.
            minor_version (str): The document minor_version_number__v field value.

        Returns:
            str: The plain text of the source file from the document.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/text"

        headers = {"Accept": "text/plain"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.text

    def download_document_file(self, doc_id, lockDocument=False):
        """
        Download the latest version of a document file.

        Retrieves the latest version of the source file from the document.

        Args:
            doc_id (str): The document id field value.
            lockDocument (bool): Set to true to check out this document before retrieval.
                                If omitted, defaults to false.

        Returns:
            bytes: Binary data of the document file. The Content-Type is set to
                  application/octet-stream, and the Content-Disposition header
                  contains a filename component.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/file"

        params = {}
        if lockDocument:
            params["lockDocument"] = (
                "true"  # Updated to match the actual parameter name
            )

        headers = {"Accept": "*/*"}

        response = self.client.api_call(
            url, params=params, headers=headers, raw_response=True
        )
        return response.content

    def download_document_version_file(self, doc_id, major_version, minor_version):
        """
        Download the file of a specific document version.

        Retrieves the specified version of the source file from the document.

        Args:
            doc_id (str): The document id field value.
            major_version (str): The document major_version_number__v field value.
            minor_version (str): The document minor_version_number__v field value.

        Returns:
            bytes: Binary data of the document version file. The Content-Type is set to
                  application/octet-stream, and the Content-Disposition header
                  contains a filename component.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/file"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content

    def download_document_version_thumbnail(self, doc_id, major_version, minor_version):
        """
        Download the thumbnail image file of a specific document version.

        This endpoint retrieves the thumbnail image for a specific document version.

        Args:
            doc_id (str): The document id field value.
            major_version (str): The document major_version_number__v field value.
            minor_version (str): The document minor_version_number__v field value.

        Returns:
            bytes: Thumbnail image data. The Content-Type is set to image/png.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/thumbnail"

        headers = {"Accept": "*/*"}

        response = self.client.api_call(url, headers=headers, raw_response=True)
        return response.content

    def search_documents(self, search_criteria):
        """
        Searches for documents using specified criteria.

        This method allows for more advanced search capabilities than the
        retrieve_all_documents method with the search parameter.

        Args:
            search_criteria (dict): Search parameters in JSON format.

        Returns:
            dict: API response with search results.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/search"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(search_criteria)
        )

    def retrieve_document_audit_trail(self, doc_id):
        """
        Retrieves the audit trail for a document.

        This endpoint provides the history of actions performed on a document.

        Args:
            doc_id (str): The document id field value.

        Returns:
            dict: API response with the document's audit trail.
        """
        url = (
            f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/audittrail"
        )

        return self.client.api_call(url)

    def retrieve_deleted_document_ids(self, start_date=None, end_date=None):
        """
        Retrieves IDs of documents that were deleted during a specified date range.

        This endpoint allows you to get information about documents that have been
        deleted from the system.

        Args:
            start_date (str, optional): Start date in the format yyyy-MM-dd.
            end_date (str, optional): End date in the format yyyy-MM-dd.

        Returns:
            dict: API response containing the IDs of deleted documents.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/deletions"

        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date

        return self.client.api_call(url, params=params)

    def retrieve_anchor_ids(self, doc_id):
        """
        Retrieves all anchor IDs from a specific document.

        Anchors are reference points within documents that can be used for
        annotations or other features.

        Args:
            doc_id (str): The ID of the document to retrieve anchor IDs from.

        Returns:
            dict: A dictionary containing the details of the retrieved anchor IDs.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/anchors"

        return self.client.api_call(url)
