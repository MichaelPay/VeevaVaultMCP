from .base_service import BaseDocumentService


class DocumentFieldsService(BaseDocumentService):
    """
    Service class for managing document fields in Veeva Vault.
    Provides methods to retrieve document field metadata.
    """

    def retrieve_all_document_fields(self):
        """
        Retrieves metadata for all standard and custom document fields and field properties.

        This endpoint returns information about document fields including whether they are:
        - required: When true, the field value must be set when creating new documents
        - editable: When true, the field value can be defined by the currently authenticated user
        - setOnCreateOnly: When true, the field value can only be set once (when creating new documents)
        - hidden: When true, the field is never available to nor visible in the UI
        - queryable: When true, field values can be retrieved using VQL
        - noCopy: When true, field values are not copied when using the Make a Copy action
        - facetable: When true, the field is available for use as a faceted filter in the Vault UI

        Endpoint: GET /api/{version}/metadata/objects/documents/properties

        Returns:
            dict: API response containing document field metadata
        """
        url = (
            f"api/{self.client.LatestAPIversion}/metadata/objects/documents/properties"
        )

        return self.client.api_call(url)

    def retrieve_common_document_fields(self, doc_ids):
        """
        Retrieves all document fields and field properties which are common to (shared by)
        a specified set of documents. This allows you to determine which document fields
        are eligible for bulk update.

        For shared fields, the response includes additional metadata:
        - shared: When true, this field is a shared field
        - usedIn (key): Lists the document types/subtypes/classifications which share the field
        - usedIn (type): Indicates if the shared field is defined at the document type, subtype,
                         or classification level
        - noCopy: When true, field values are not copied when using the Make a Copy action

        Endpoint: POST /api/{version}/metadata/objects/documents/properties/find_common

        Args:
            doc_ids (str): A comma-separated list of document id field values.

        Returns:
            dict: API response containing all fields shared by the specified documents.
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/properties/find_common"

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data = {"docIds": doc_ids}

        return self.client.api_call(url, method="POST", headers=headers, data=data)
