import json
from .base_service import BaseDocumentService


class DocumentEventsService(BaseDocumentService):
    """
    Service class for managing document events in Veeva Vault.

    Document Events are used to track document and binder distribution events
    across sub-systems such as iRep, Controlled Copy, Approved Email and Engage.
    """

    def retrieve_document_event_types(self):
        """
        Retrieves all document event types and subtypes.

        Returns:
            dict: API response with list of document events and their subtypes

        API Endpoint:
            GET /api/{version}/metadata/objects/documents/events

        Notes:
            - If the user is not permitted to access an event type, it will be omitted from the response
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/events"

        return self.client.api_call(url)

    def retrieve_document_event_subtype_metadata(self, event_type, event_subtype):
        """
        Retrieves metadata for a specific document event subtype.

        Args:
            event_type (str): The event type (e.g., 'distribution__v')
            event_subtype (str): The event subtype (e.g., 'approved_email__v')

        Returns:
            dict: API response with metadata for the specified event subtype

        API Endpoint:
            GET /api/{version}/metadata/objects/documents/events/{event_type}/types/{event_subtype}
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/documents/events/{event_type}/types/{event_subtype}"

        return self.client.api_call(url)

    def create_document_event(
        self,
        doc_id,
        major_version,
        minor_version,
        event_type,
        event_subtype,
        classification,
        external_id=None,
        **additional_fields,
    ):
        """
        Creates a document event for a specific document version.

        Args:
            doc_id (str): ID of the document
            major_version (int): Major version number of the document
            minor_version (int): Minor version number of the document
            event_type (str): The event type (e.g., 'distribution__v')
            event_subtype (str): The event subtype (e.g., 'approved_email__v')
            classification (str): The event classification (e.g., 'download__v')
            external_id (str, optional): External ID value for the document event
            **additional_fields: Additional fields required by the event type/subtype

        Returns:
            dict: API response confirming the event creation

        API Endpoint:
            POST /api/{version}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/events

        Notes:
            - Required fields vary based on the document event type, subtype, and classification
            - Use retrieve_document_event_subtype_metadata to determine required fields
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/versions/{major_version}/{minor_version}/events"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {
            "event_type__v": event_type,
            "event_subtype__v": event_subtype,
            "classification__v": classification,
        }

        if external_id is not None:
            data["external_id__v"] = external_id

        # Add any additional fields provided
        data.update(additional_fields)

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def retrieve_document_events(self, doc_id):
        """
        Retrieves all events for a specific document.

        Args:
            doc_id (str): ID of the document

        Returns:
            dict: API response with document events

        API Endpoint:
            GET /api/{version}/objects/documents/{doc_id}/events

        Notes:
            - Null and/or false valued fields are omitted from the response
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/events"

        return self.client.api_call(url)
