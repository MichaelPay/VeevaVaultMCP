import json
from typing import Dict, Any, Optional, Union, List
from .base_service import BaseWorkflowService


class WorkflowService(BaseWorkflowService):
    """
    Service class for handling Veeva Vault workflow operations.

    This service provides methods for retrieving workflows, workflow details,
    workflow actions, workflow action details, and initiating workflow actions.
    """

    def retrieve_workflows(
        self,
        object_name=None,
        record_id=None,
        participant=None,
        status=None,
        offset=None,
        page_size=None,
        loc=False,
    ):
        """
        Retrieves all current, cancelled, and completed workflow instances for a specific object record
        or all workflows available to a particular workflow participant.

        GET /api/{version}/objects/objectworkflows

        Args:
            object_name (str, optional): API name of the object. Required when participant is not used.
            record_id (str, optional): ID of the record. Required when participant is not used.
            participant (str, optional): User ID or 'me()' to retrieve workflows for a specific user.
                                        Required when object_name and record_id are not used.
            status (str or list, optional): Status(es) to filter by (e.g., "active__v", "completed__v", "cancelled__v")
            offset (int, optional): Pagination offset (default 0)
            page_size (int, optional): Records per page (default 200, max 1000)
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: List of workflows matching the query parameters

        Notes:
            - Each workflow may include: id, label__v, status__v, object__v, record_id__v,
              initiator__v, started_date__v, completed_date__v, cancelled_date__v
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows"

        params = {}
        if object_name and record_id:
            params["object__v"] = object_name
            params["record_id__v"] = record_id
        elif participant:
            params["participant"] = participant

        if status:
            if isinstance(status, list):
                params["status__v"] = ",".join(status)
            else:
                params["status__v"] = status

        if offset is not None:
            params["offset"] = offset

        if page_size is not None:
            params["page_size"] = page_size

        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params)

    def retrieve_workflow_details(self, workflow_id, loc=False):
        """
        Retrieves the details for a specific workflow.

        GET /api/{version}/objects/objectworkflows/{workflow_id}

        Args:
            workflow_id (str): The workflow ID
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: Workflow details including id, label__v, status__v, object__v, record_id__v,
                 initiator__v, started_date__v, completed_date__v, cancelled_date__v

        Notes:
            - The workflow owner is identified by the initiator__v field
        """
        url = (
            f"api/{self.client.LatestAPIversion}/objects/objectworkflows/{workflow_id}"
        )

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params)

    def retrieve_workflow_actions(self, workflow_id, loc=False):
        """
        Retrieves all available workflow actions that can be initiated on a specific workflow.

        GET /api/{version}/objects/objectworkflows/{workflow_id}/actions

        Args:
            workflow_id (str): The workflow ID
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: List of available workflow actions with name and label for each action
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/{workflow_id}/actions"

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params)

    def retrieve_workflow_action_details(self, workflow_id, workflow_action, loc=False):
        """
        Retrieves details about a workflow action, such as the prompts needed to complete it.

        GET /api/{version}/objects/objectworkflows/{workflow_id}/actions/{workflow_action}

        Args:
            workflow_id (str): The workflow ID
            workflow_action (str): Name of the workflow action
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: Details about the workflow action including any required prompts
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/{workflow_id}/actions/{workflow_action}"

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params)

    def initiate_workflow_action(self, workflow_id, workflow_action, payload=None):
        """
        Initiates a workflow action on a specific workflow.

        POST /api/{version}/objects/objectworkflows/{workflow_id}/actions/{workflow_action}

        Args:
            workflow_id (str): The workflow ID
            workflow_action (str): Name of the workflow action to initiate
            payload (dict, optional): Data containing required fields for the action

        Returns:
            dict: API response indicating success or failure

        Notes:
            Common workflow actions include:
            - cancel: Cancel the workflow
            - replaceworkflowowner: Replace the workflow owner
            - emailparticipants: Send email to workflow participants
            - addparticipants: Add participants to the workflow
            - removecontent: Remove documents from an envelope
            - updateworkflowduedate: Update the workflow due date
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/{workflow_id}/actions/{workflow_action}"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(payload if payload else {})

        return self.client.api_call(url, method="POST", headers=headers, data=data)
