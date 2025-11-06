import json
from typing import Dict, Any, Optional, Union, List
from .base_service import BaseWorkflowService


class BulkWorkflowActionService(BaseWorkflowService):
    """
    Service class for handling Veeva Vault bulk workflow action operations.

    This service provides methods for retrieving and executing actions across
    multiple workflows simultaneously.
    """

    def retrieve_bulk_workflow_actions(self):
        """
        Retrieve all available workflow actions that can be initiated in bulk.

        GET /api/{version}/object/workflow/actions

        Returns:
            dict: List of available bulk workflow actions with name and label for each action

        Notes:
            - Returns only actions that:
              - The authenticated user has permissions to view or initiate
              - Can be initiated through the API
        """
        url = f"api/{self.client.LatestAPIversion}/object/workflow/actions"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def retrieve_bulk_workflow_action_details(self, action):
        """
        Retrieve the details for a specific bulk workflow action.

        GET /api/{version}/object/workflow/actions/{action}

        Args:
            action (str): Name of the bulk workflow action

        Returns:
            dict: Metadata for the specified workflow action, including required fields

        Notes:
            - The response contains controls and prompts needed to execute the action
            - For each prompt, data may include multi_value, label, required, and name
        """
        url = f"api/{self.client.LatestAPIversion}/object/workflow/actions/{action}"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def initiate_bulk_workflow_action(self, action, payload):
        """
        Initiate a workflow action on multiple workflows simultaneously.

        POST /api/{version}/object/workflow/actions/{action}

        Args:
            action (str): Name of the bulk workflow action to execute
            payload (dict): Data containing required fields for the action

        Returns:
            dict: API response with job_id for the asynchronous operation

        Notes:
            - Maximum 500 workflows per request
            - Starts an asynchronous job whose status can be checked later
            - Common actions include:
              - cancelworkflows: Cancel active workflows
              - reassigntasks: Reassign all tasks from one user to another (max 500 tasks)
              - canceltasks: Cancel tasks by user ID or task ID
              - replaceworkflowowner: Replace the workflow owner for all workflows
        """
        url = f"api/{self.client.LatestAPIversion}/object/workflow/actions/{action}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(url, method="POST", headers=headers, data=payload)
