import json
from .base_service import BaseObjectService


class ObjectActionsService(BaseObjectService):
    """
    Service class for handling Veeva Vault object user actions operations.

    This service provides methods to retrieve available user actions and initiate
    user actions on object records, including workflow actions and lifecycle
    state transitions.
    """

    def retrieve_object_record_user_actions(self, object_name, object_record_id):
        """
        Retrieve all available user actions that can be initiated on a specific object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/actions

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the object record

        Returns:
            dict: List of available user actions with metadata and execution links
                 Each action includes:
                 - name: The unique name of the user action
                 - label: Display label for the action
                 - type: Type of action (e.g., "workflow", "lifecycle")
                 - links: Array with metadata and execute endpoints

        Notes:
            - Returns actions that the authenticated user has permissions to view or initiate
            - Only includes actions that can be initiated through the API
            - Actions may include workflow initiations and lifecycle state transitions
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/actions"

        return self.client.api_call(url)

    def retrieve_object_user_action_details(self, object_name, object_record_id, action_name):
        """
        Retrieve details about a specific user action that can be initiated on an object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/actions/{action_name}

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the object record
            action_name (str): Name of the user action

        Returns:
            dict: Detailed metadata about the user action including:
                 - name: The unique name of the user action
                 - label: Display label for the action
                 - type: Type of action (e.g., "workflow", "lifecycle")
                 - prompts: Array of prompts (fields) that may be required for execution
                 - links: Array with execute endpoint information

        Notes:
            - Provides detailed information about prompts and requirements for action execution
            - Includes field metadata for any required input parameters
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/actions/{action_name}"

        return self.client.api_call(url)

    def initiate_object_action_on_single_record(self, object_name, object_record_id, action_name, payload=None):
        """
        Initiate a user action on a single object record.

        POST /api/{version}/vobjects/{object_name}/{object_record_id}/actions/{action_name}

        Args:
            object_name (str): API name of the object
            object_record_id (str): ID of the object record
            action_name (str): Name of the user action to initiate
            payload (dict, optional): JSON data containing any required field values or parameters

        Returns:
            dict: Result of the action initiation, may include job ID for asynchronous actions

        Notes:
            - Some actions may execute synchronously and return immediate results
            - Other actions may be asynchronous and return a job ID for status tracking
            - Required field values should be provided in the payload based on action metadata
            - The authenticated user must have permission to initiate the specified action
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/actions/{action_name}"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(payload if payload else {})

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def initiate_object_action_on_multiple_records(self, object_name, action_name, payload):
        """
        Initiate a user action on multiple object records in bulk.

        POST /api/{version}/vobjects/{object_name}/actions/{action_name}

        Args:
            object_name (str): API name of the object
            action_name (str): Name of the user action to initiate
            payload (dict): JSON data containing record IDs and any required field values

        Returns:
            dict: Result of the bulk action initiation, typically includes job ID for tracking

        Notes:
            - Allows initiation of the same action on multiple records simultaneously
            - Payload should include array of record IDs and any required parameters
            - Most bulk actions are asynchronous and return job IDs for status tracking
            - The authenticated user must have permission to initiate the action on all specified records
            - Maximum batch size and other limits may apply based on action type
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/actions/{action_name}"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(payload)

        return self.client.api_call(url, method="POST", headers=headers, data=data)