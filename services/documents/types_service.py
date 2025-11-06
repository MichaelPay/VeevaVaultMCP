from .base_service import BaseDocumentService


class DocumentTypesService(BaseDocumentService):
    """
    Service class for managing document types in Veeva Vault.

    Document type refers both to the structure of hierarchical fields (Type > Subtype > Classification)
    that determines the relevant document fields, rendition types, and other settings for a document,
    and to the highest level in that hierarchy.
    """

    def retrieve_all_document_types(self):
        """
        Retrieves all document types present in the vault. These represent the top-level of
        the document type/subtype/classification hierarchy.

        The response lists all document types configured in the Vault. These vary by Vault
        application and configuration:
        - Standard types end in __v
        - Some Vaults include sample types __c
        - Admins can configure custom types __c

        Endpoint: GET /api/{version}/metadata/objects/documents/types

        Returns:
            dict: API response containing:
                 - types: List of all standard and custom document types
                 - label: Label of each document type as seen in the API and UI
                 - value: URL to retrieve the metadata associated with each document type
                 - lock: URL to retrieve the document lock metadata (document check-out)
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/types"

        return self.client.api_call(url)

    def retrieve_document_type(self, doc_type):
        """
        Retrieve all metadata from a specified document type, including all of its subtypes (when available).

        The response includes all metadata for the specified document type. If the type contains
        subtypes in the document type hierarchy, the list of subtypes and the URLs pointing to
        their metadata will be included. The list of document fields defined for the type are
        also included.

        Endpoint: GET /api/{version}/metadata/objects/documents/types/{type}

        Args:
            doc_type (str): The document type to retrieve metadata for.

        Returns:
            dict: API response containing metadata such as:
                 - name: Name of the document type (used primarily in the API)
                 - label: Label of the document type as seen in the API and UI
                 - renditions: List of all rendition types available for the document type
                 - relationshipTypes: List of all relationship types available
                 - properties: List of all document fields associated to the document type
                 - processes: List of all processes available (when configured)
                 - defaultWorkflows: List of all workflows available
                 - availableLifecycles: List of all lifecycles available
                 - templates: List of all templates available (when configured)
                 - subtypes: List of all standard and custom document subtypes available
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/types/{doc_type}"

        return self.client.api_call(url)

    def retrieve_document_subtype(self, doc_type, doc_subtype):
        """
        Retrieve all metadata from a document subtype, including all of its classifications (when available).

        Endpoint: GET /api/{version}/metadata/objects/documents/types/{type}/subtypes/{subtype}

        Args:
            doc_type (str): The document type.
            doc_subtype (str): The document subtype.

        Returns:
            dict: API response containing metadata such as:
                 - name: Name of the document subtype
                 - label: UI label for the document subtype
                 - properties: List of all document fields associated to the document subtype
                 - classifications: List of classifications (will not appear if none exist)
                 - templates: List of all templates available (will not appear if none exist)
                 - availableLifecycles: List of all lifecycles available
                 - renditions: List of all rendition types available (if configured)
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/types/{doc_type}/subtypes/{doc_subtype}"

        return self.client.api_call(url)

    def retrieve_document_classification(self, doc_type, doc_subtype, classification):
        """
        Retrieve all metadata from a document classification.

        Endpoint: GET /api/{version}/metadata/objects/documents/types/{type}/subtypes/{subtype}/classifications/{classification}

        Args:
            doc_type (str): The document type.
            doc_subtype (str): The document subtype.
            classification (str): The document classification.

        Returns:
            dict: API response containing metadata such as:
                 - name: Name of the document subtype
                 - label: UI label for the document subtype
                 - properties: List of all document fields associated to the classification
                 - templates: List of all templates available (will not appear if none exist)
                 - availableLifecycles: List of all lifecycles available
                 - renditions: List of all rendition types available (if configured)
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/types/{doc_type}/subtypes/{doc_subtype}/classifications/{classification}"

        return self.client.api_call(url)

    def retrieve_document_type_relationships(self, document_type):
        """
        Retrieves the document relationship metadata for a document type.

        This endpoint retrieves information about the relationship types available for the
        specified document type.

        Endpoint: GET /api/{version}/metadata/objects/documents/types/{type}/relationships

        Args:
            document_type (str): The document type to retrieve relationship metadata for.

        Returns:
            dict: API response containing document relationship metadata.
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/types/{document_type}/relationships"

        return self.client.api_call(url)
