import json
from typing import Dict, Any, Optional, Union, List
from .base_service import BaseLifecycleWorkflowService


class ObjectLifecycleWorkflowService(BaseLifecycleWorkflowService):
    """
    Service class for handling Veeva Vault object lifecycle and workflow operations.

    This service provides methods for retrieving object record user actions, initiating object
    record user actions, retrieving and managing multi-record workflows, and more.

    Object lifecycles are the sequences of states (Draft, In Review, etc.) an object record
    goes through. A lifecycle can be simple (two states that require users to manually move
    between them) or very complex (multiple states with different security and workflows that
    automatically move records from one state to another).
    """

    def retrieve_object_record_user_actions(
        self, object_name: str, object_record_id: str, loc: bool = False
    ) -> Dict[str, Any]:
        """
        Retrieve all available user actions that can be initiated on a specific object record which:
        - The authenticated user has permissions to view or initiate
        - Can be initiated through the API

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/actions

        Args:
            object_name: The object name__v field value.
            object_record_id: The object record id field value.
            loc: Whether to include localized strings for the label.

        Returns:
            dict: List of available user actions that can be initiated on the specified object record.

        Notes:
            - For users with View permission, includes a link to retrieve the metadata for the action.
            - For users without View permission, returns an INSUFFICIENT_ACCESS error.
            - For users with Execute permission, includes a link to initiate the specified action.
            - The type of user action will be indicated (state_change, workflow, object_action, etc.)
            - The action name includes the prefix Objectaction or Objectlifecyclestateuseraction.
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/actions"

        headers = {"Accept": "application/json"}

        params = {}
        if loc:
            params["loc"] = "true"

        return self.client.api_call(url, params=params, headers=headers)

    def retrieve_object_user_action_details(
        self, object_name: str, object_record_id: str, action_name: str
    ) -> Dict[str, Any]:
        """
        Retrieve the details for a specific user action on an object record.

        GET /api/{version}/vobjects/{object_name}/{object_record_id}/actions/{action_name}

        Args:
            object_name: The object name__v field value.
            object_record_id: The object record id field value.
            action_name: The name of the Objectaction or Objectlifecyclestateuseraction to retrieve.

        Returns:
            dict: Details about the specified object user action.

        Notes:
            - For users with View permission, includes a link to retrieve metadata for the action.
            - For users without View permission, returns an INSUFFICIENT_ACCESS error.
            - For users with Execute permission, includes a link to initiate the specified action.
            - For actions with type: workflow, returns controls like instructions, participant, date, and field.
            - Each control may include label, type, and prompts information.
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/actions/{action_name}"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def initiate_object_action_on_single_record(
        self,
        object_name: str,
        object_record_id: str,
        action_name: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Initiate an action on a specific object record.

        POST /api/{version}/vobjects/{object_name}/{object_record_id}/actions/{action_name}

        Args:
            object_name: The object name__v field value.
            object_record_id: The object record id field value.
            action_name: The name of the Objectaction or Objectlifecyclestateuseraction to initiate.
            data: Required parameters to initiate the action as name-value pairs.

        Returns:
            dict: API response indicating success or failure.

        Notes:
            - The format for action_name is Objectaction.{vobject}.{action} or
              Objectlifecyclestateuseraction.{vobject}.{state}.{action}.
            - When providing values for field prompts, required fields cannot be omitted, set as blank,
              or defaulted to their existing value.
            - To preserve the existing value of a required field, submit the existing value as the new value.
            - For participant groups, you may need to specify assignment_type__c as 'assigned' or 'available'.
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{object_record_id}/actions/{action_name}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(
            url, method="POST", headers=headers, data=data if data else {}
        )

    def initiate_object_action_on_multiple_records(
        self,
        object_name: str,
        action_name: str,
        record_ids: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Initiate an object user action on multiple records. Maximum 500 records per batch.

        POST /api/{version}/vobjects/{object_name}/actions/{action_name}

        Args:
            object_name: The object name__v field value.
            action_name: The name of the Objectaction or Objectlifecyclestateuseraction to initiate.
            record_ids: Comma-separated list of object record ids on which to initiate the action.
            data: Additional data required for the action.

        Returns:
            dict: API response with results for each record (success or failure).

        Notes:
            - The format for action_name is Objectaction.{vobject}.{action} or
              Objectlifecyclestateuseraction.{vobject}.{state}.{action}.
            - For a workflow on multiple records, there is no way to preserve existing values in a field
              if that field is a required prompt. Setting a value updates all records to the same value.
            - For participant groups, you may need to specify assignment_type__c as 'assigned' or 'available'.
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/actions/{action_name}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        request_data = {"ids": record_ids}
        if data:
            request_data.update(data)

        return self.client.api_call(
            url, method="POST", headers=headers, data=request_data
        )

    def retrieve_all_multi_record_workflows(self) -> Dict[str, Any]:
        """
        Retrieve all available multi-record workflows which:
        - The authenticated user has permissions to view or initiate
        - Can be initiated through the API

        GET /api/{version}/objects/objectworkflows/actions

        Returns:
            dict: List of available multi-record workflows.

        Notes:
            - Each workflow includes name, label, type, and cardinality information.
            - For users without the Workflow: Start permission, the response returns an INSUFFICIENT_ACCESS error.
            - An object workflow is a series of steps configured in Vault to correspond with the specific
              business processes of your organization.
            - Object workflows are specific to an object, meaning that a single workflow cannot apply to
              multiple objects. A single object record can only be in one workflow at a time.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/actions"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def retrieve_multi_record_workflow_details(
        self, workflow_name: str
    ) -> Dict[str, Any]:
        """
        Retrieve the fields required to initiate a specific multi-record workflow.

        GET /api/{version}/objects/objectworkflows/actions/{workflow_name}

        Args:
            workflow_name: The multi-record workflow name value.

        Returns:
            dict: Details about the workflow and required fields to initiate it.

        Notes:
            - The response lists the fields that must be configured with values to initiate the workflow.
            - These are based on the controls configured in the workflow start step.
            - The response may include control types like prompts, instructions, participant,
              date, description, and variable.
            - Additionally includes workflow metadata like name, label, type, and cardinality.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/actions/{workflow_name}"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def initiate_multi_record_workflow(
        self, workflow_name: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Initiate a multi-record workflow on a set of records.

        POST /api/{version}/objects/objectworkflows/actions/{workflow_name}

        Args:
            workflow_name: The workflow name value.
            data: Data containing required fields for the workflow, such as contents__sys,
                 description__sys, and any participants.

        Returns:
            dict: API response containing record_url, record_id__v, and workflow_id.

        Notes:
            - If any record is not in the relevant state or does not meet configured field conditions,
              the API returns INVALID_DATA and the workflow does not start.
            - Maximum 100 records can be included.
            - contents__sys should be a comma-separated list of records in the format
              Object:{objectname}.{record_ID}. For example, "Object:product__c.V3O000000005001".
            - The description__sys field is typically required (maximum 128 characters).
            - Required fields cannot be omitted, set as blank, or defaulted to their existing value.
            - For multiple records, there is no way to preserve existing values in a field if that field
              is a required prompt. Setting a value updates all records to the same value.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/objectworkflows/actions/{workflow_name}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(url, method="POST", headers=headers, data=data)
