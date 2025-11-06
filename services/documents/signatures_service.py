from .base_service import BaseDocumentService


class DocumentSignaturesService(BaseDocumentService):
    """
    Service class for managing document signatures in Veeva Vault.

    This service provides access to metadata related to document signatures
    for both active and archived documents.
    """

    def retrieve_document_signature_metadata(self):
        """
        Retrieves all metadata for signatures on documents.

        Returns:
            dict: API response with metadata for document signatures

        API Endpoint:
            GET /api/{version}/metadata/query/documents/relationships/document_signature__sysr

        Notes:
            - Returns fields such as signature user, time, workflow details, verdict, etc.
            - Learn more about signature pages in Vault Help
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/query/documents/relationships/document_signature__sysr"

        return self.client.api_call(url)

    def retrieve_archived_document_signature_metadata(self):
        """
        Retrieves all metadata for signatures on archived documents.

        Returns:
            dict: API response with metadata for archived document signatures

        API Endpoint:
            GET /api/{version}/metadata/query/archived_documents/relationships/document_signature__sysr

        Notes:
            - Document archive is not available in all Vaults
            - Returns fields such as signature user, time, workflow details, verdict, etc.
            - Learn more about signature pages in Vault Help
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/query/archived_documents/relationships/document_signature__sysr"

        return self.client.api_call(url)
