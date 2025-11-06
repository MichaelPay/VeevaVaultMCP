import json
from typing import Dict, Any, Optional, Union, List
from .base_service import BaseWorkflowService


class WorkflowTaskService(BaseWorkflowService):
    """
    Service class for handling Veeva Vault workflow task operations.

    This service provides methods for retrieving, accepting, completing, reassigning,
    and managing workflow tasks.
    """

    def retrieve_workflow_tasks(
        self,
        object_name=None,
        record_id=None,
        assignee=None,
        status=None,
        offset=None,
        page_size=None,
        loc=False,
    ):
        """
        Retrieves all available tasks across all workflows.

        GET /api/{version}/objects/objectworkflows/tasks

        Args:
            object_name (str, optional): API name of the object. Required when assignee is not used.
            record_id (str, optional): ID of the record. Required when assignee is not used.
            assignee (str, optional): User ID or 'me()' to retrieve tasks for a specific user.
                                     Required when object_name and record_id are not used.
            status (str or list, optional): Status(es) to filter by (e.g., "available__v", "completed__v")
            offset (int, optional): Pagination offset (default 0)
            page_size (int, optional): Records per page (default 200, max 1000)
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: List of workflow tasks matching the query parameters

        Notes:
            - Each task may include: id, label__v, status__v, object__v, record_id__v, instructions__v,
              assignee__v, created_date__v, assigned_date__v, due_date__v, workflow__v
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks"

        params = {}
        if object_name and record_id:
            params["object__v"] = object_name
            params["record_id__v"] = record_id
        elif assignee:
            params["assignee__v"] = assignee

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

    def retrieve_workflow_task_details(self, task_id, loc=False):
        """
        Retrieves the details of a specific workflow task.

        GET /api/{version}/objects/objectworkflows/tasks/{task_id}

        Args:
            task_id (str): The task ID
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: Task details including id, label__v, status__v, object__v, record_id__v,
                 instructions__v, assignee__v, created_date__v, assigned_date__v, due_date__v,
                 workflow__v, workflow_class__sys
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}"

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params)

    def retrieve_workflow_task_actions(self, task_id, loc=False):
        """
        Retrieves all available actions that can be initiated on a given workflow task.

        GET /api/{version}/objects/objectworkflows/tasks/{task_id}/actions

        Args:
            task_id (str): The task ID
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: List of available task actions with name and label for each action
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions"

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params)

    def retrieve_workflow_task_action_details(self, task_id, task_action, loc=False):
        """
        Retrieves the details of a specific workflow task action.

        GET /api/{version}/objects/objectworkflows/tasks/{task_id}/actions/{task_action}

        Args:
            task_id (str): The task ID
            task_action (str): Name of the task action
            loc (bool): Whether to include localized strings for labels and help text

        Returns:
            dict: Details about the task action, including all fields required to initiate the action

        Notes:
            - Task actions where esignature is true cannot be initiated via the API
            - The response may include controls like instructions, verdict, reasons, and capacities
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions/{task_action}"

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params)

    def accept_multi_item_workflow_task(self, task_id):
        """
        Accept an available task for a multi-record workflow.

        POST /api/{version}/objects/objectworkflows/tasks/{task_id}/actions/mdwaccept

        Args:
            task_id (str): The task ID

        Returns:
            dict: API response indicating success or failure

        Notes:
            - If the task is available to multiple users, any one of the assigned users can accept it
            - Vault may prevent acceptance if you've already accepted, assigned, or completed another task
            - To undo acceptance, use undo_workflow_task_acceptance()
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions/mdwaccept"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers)

    def accept_single_record_workflow_task(self, task_id):
        """
        Accept an available task for a workflow configured for a single record.

        POST /api/{version}/objects/objectworkflows/tasks/{task_id}/actions/accept

        Args:
            task_id (str): The task ID

        Returns:
            dict: API response indicating success or failure

        Notes:
            - If the task is available to multiple users, any one of the assigned users can accept it
            - Vault may prevent acceptance if you've already accepted, assigned, or completed another task
            - To undo acceptance, use undo_workflow_task_acceptance()
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions/accept"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers)

    def undo_workflow_task_acceptance(self, task_id):
        """
        Undo your acceptance of an available workflow task.

        POST /api/{version}/objects/objectworkflows/tasks/{task_id}/actions/undoaccept

        Args:
            task_id (str): The task ID

        Returns:
            dict: API response indicating success or failure

        Notes:
            - Once released, the task is available again to any of the assigned users
            - This endpoint supports single and multi-item workflows
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions/undoaccept"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers)

    def complete_multi_item_workflow_task(self, task_id, payload):
        """
        Complete an open workflow task for a multi-item workflow.

        POST /api/{version}/objects/objectworkflows/tasks/{task_id}/actions/mdwcomplete

        Args:
            task_id (str): The task ID
            payload (dict): Data containing required fields such as verdict, reason, capacity, and comments

        Returns:
            dict: API response indicating success or failure

        Notes:
            - This endpoint does not support initiating task actions requiring eSignatures
            - For single verdict: Include the verdict key and any related comment fields
            - For multiple verdicts: Include contents__sys array with object__v, record_id__v, and verdict info
            - Controls with required=true must be provided
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions/mdwcomplete"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(payload if payload else {})

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def complete_single_record_workflow_task(self, task_id, payload):
        """
        Complete an open workflow task for a workflow configured for a single record.

        POST /api/{version}/objects/objectworkflows/tasks/{task_id}/actions/complete

        Args:
            task_id (str): The task ID
            payload (dict): Data containing required fields such as verdict, reason, capacity, and comments

        Returns:
            dict: API response indicating success or failure

        Notes:
            - This endpoint does not support initiating task actions requiring eSignatures
            - Controls with required=true must be provided
            - If a control (verdict) defines required fields, those must also be provided
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions/complete"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        # For x-www-form-urlencoded, we pass the payload directly without json.dumps

        return self.client.api_call(url, method="POST", headers=headers, data=payload)

    def reassign_multi_item_workflow_task(self, task_id, new_assignee):
        """
        Reassign an open workflow task to another user for a multi-item workflow.

        POST /api/{version}/objects/objectworkflows/tasks/{task_id}/actions/mdwreassign

        Args:
            task_id (str): The task ID
            new_assignee (str): User ID in the format "user:{id}" (e.g., "user:100307")

        Returns:
            dict: API response indicating success or failure

        Notes:
            - Cannot reassign to user already assigned to that task or with restricted role
            - Vault notifies new and previous task owners of the reassignment
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions/mdwreassign"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = {"task_assignee__v": new_assignee}

        return self.client.api_call(
            url, method="POST", headers=headers, data=json.dumps(data)
        )

    def reassign_single_record_workflow_task(self, task_id, new_assignee):
        """
        Reassign an open workflow task to another user for a workflow configured for a single record.

        POST /api/{version}/objects/objectworkflows/tasks/{task_id}/actions/reassign

        Args:
            task_id (str): The task ID
            new_assignee (str): User ID in the format "user:{id}" (e.g., "user:100307")

        Returns:
            dict: API response indicating success or failure

        Notes:
            - Cannot reassign to user already assigned to that task or with restricted role
            - Vault notifies new and previous task owners of the reassignment
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions/reassign"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"task_assignee__v": new_assignee}

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def update_workflow_task_due_date(self, task_id, due_date):
        """
        Update the due date of an assigned workflow task.

        POST /api/{version}/objects/objectworkflows/tasks/{task_id}/actions/updateduedate

        Args:
            task_id (str): The task ID
            due_date (str): New due date in the format YYYY-MM-DD

        Returns:
            dict: API response indicating success or failure

        Notes:
            - This endpoint supports single and multi-item workflows
            - The new task due date cannot be the same as the current task due date
            - Cannot update task due dates configured to sync with an object or document field
            - If workflow is set to sync all task due dates, this won't affect the workflow due date
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions/updateduedate"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"task_due_date__v": due_date}

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def cancel_workflow_task(self, task_id):
        """
        Cancel an open workflow task.

        POST /api/{version}/objects/objectworkflows/tasks/{task_id}/actions/cancel

        Args:
            task_id (str): The task ID

        Returns:
            dict: API response indicating success or failure

        Notes:
            - This endpoint supports single and multi-record workflows
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions/cancel"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers)

    def manage_multi_item_workflow_content(self, task_id, payload):
        """
        Manage content in a multi-item workflow without completing an open workflow task.

        POST /api/{version}/objects/objectworkflows/tasks/{task_id}/actions/mdwmanagecontent

        Args:
            task_id (str): The task ID
            payload (dict): Data containing content information, typically with contents__sys array

        Returns:
            dict: API response indicating success or failure

        Notes:
            - Useful for providing verdicts for specific items without completing the task
            - Does not support initiating task actions requiring eSignatures
            - Must use complete_multi_item_workflow_task() to actually complete the task
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/tasks/{task_id}/actions/mdwmanagecontent"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(payload if payload else {})

        return self.client.api_call(url, method="POST", headers=headers, data=data)
