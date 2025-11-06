from typing import Dict, Any, Optional, Union, BinaryIO
import json


class QualityDocsService:
    """
    Service class for interacting with the Veeva Vault QualityDocs application.

    This service provides methods for working with document roles and document change control.
    """

    def __init__(self, client):
        """
        Initialize the QualityDocsService with a VaultClient instance.

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def document_role_check_for_document_change_control(
        self, object_record_id: str, application_role: str
    ) -> Dict[str, Any]:
        """
        Check if any document added to a Document Change Control (DCC) record has one or more
        users in a specified Application Role. This API only checks documents added to the standard
        Documents to be Released and Documents to be Made Obsolete sections.

        Args:
            object_record_id: The {id} field value of the document_change_control__v object record.
            application_role: The name of the application_role__v.

        Returns:
            API response with a check_result field indicating if the role exists on any document
        """
        endpoint = f"api/{self.client.LatestAPIversion}/vobjects/document_change_control__v/{object_record_id}/actions/documentrolecheck"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"application_role": application_role}

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, data=data
        )
