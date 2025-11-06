from .base_service import BaseBinderService


class BinderLifecycleService(BaseBinderService):
    """
    Service class for managing binder lifecycle actions in Veeva Vault.
    
    This service provides methods to retrieve and initiate lifecycle actions (user actions)
    on binders, including workflow operations and state changes.
    
    Lifecycle actions allow you to:
    - Retrieve available user actions on a binder version
    - Retrieve available user actions on multiple binders
    - Get entry criteria for actions
    - Initiate single binder user actions
    - Initiate bulk binder user actions
    """

    def retrieve_binder_user_actions(self, binder_id, major_version, minor_version):
        """
        Retrieve all available user actions on a specific version of a binder.

        Returns actions that:
        - The authenticated user has permission to view or initiate
        - Can be initiated through the API
        - Are not currently in an active workflow

        Args:
            binder_id (str): ID of the binder
            major_version (int): Major version number of the binder
            minor_version (int): Minor version number of the binder

        Returns:
            dict: API response containing available lifecycle actions with the following fields:
                - name__v: The user action name (consumed by the API)
                - label__v: The user action label displayed to users in the UI
                - lifecycle_action_type__v: The action type (workflow, stateChange, etc.)
                - lifecycle__v: The binder lifecycle the action belongs to
                - state__v: The current state of the binder
                - executable__v: Whether the user can execute this action
                - entry_requirements__v: Endpoint to retrieve entry requirements
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions"

        return self.client.api_call(url)

    def retrieve_user_actions_multiple_binders(self, binder_versions):
        """
        Retrieve all available user actions on specific versions of multiple binders.

        Args:
            binder_versions (list): List of binder version specifications in the format
                                   "binder_id:major_version:minor_version" (e.g., ["22:0:1", "23:1:0"])

        Returns:
            dict: API response containing available lifecycle actions for all specified binders.
                 Actions are not returned for binders currently in an active workflow.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/lifecycle_actions"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {"docIds": ",".join(binder_versions)}

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def retrieve_binder_entry_criteria(
        self, binder_id, major_version, minor_version, action_name
    ):
        """
        Retrieve the entry criteria for a user action on a binder.

        Entry criteria are requirements the binder must meet before you can initiate the action.
        They are dynamic and depend on lifecycle configuration, state, or workflow requirements.

        Args:
            binder_id (str): ID of the binder
            major_version (int): Major version number of the binder
            minor_version (int): Minor version number of the binder
            action_name (str): The lifecycle action name (name__v field value)

        Returns:
            dict: API response containing entry criteria properties with the following fields:
                - name: The entry criteria name (used in the API)
                - description: The entry criteria name (used in the UI)
                - type: The data type (String, Number, Date, Boolean, Picklist, ObjectReference)
                - objectTypeReferenced: When type is ObjectReference, the object being referenced
                - required: Whether the criteria must be specified when initiating the action
                - editable: Whether the value can be edited by the user
                - repeating: Whether the field can have multiple values
                - scope: The scope of the entry criteria
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{action_name}/entry_requirements"

        return self.client.api_call(url)

    def initiate_binder_user_action(
        self, binder_id, major_version, minor_version, action_name, entry_criteria=None
    ):
        """
        Initiate a user action on a binder.

        Before initiating, you should retrieve any applicable entry criteria for the action.
        Only some user action types can be initiated through the API.
        The authenticated user must have permission to initiate this action.

        Args:
            binder_id (str): ID of the binder on which to initiate the user action
            major_version (int): Major version number of the binder
            minor_version (int): Minor version number of the binder
            action_name (str): The action name (name__v field value) to initiate
            entry_criteria (dict, optional): Dictionary of entry criteria values required
                                           for the action. Keys should match the entry criteria
                                           names returned from retrieve_binder_entry_criteria.

        Returns:
            dict: API response containing:
                - responseStatus: Status of the request
                - id: ID of the binder
                - workflow_id__v: ID of the initiated workflow (if applicable)
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/versions/{major_version}/{minor_version}/lifecycle_actions/{action_name}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = entry_criteria or {}

        return self.client.api_call(url, method="PUT", headers=headers, data=data)

    def initiate_bulk_binder_user_actions(
        self, user_action_name, binder_versions, lifecycle, state, entry_criteria=None
    ):
        """
        Initiate a user action on multiple binders.

        For each bulk action, you may only select a single workflow that Vault will start
        for all selected and valid binders. The action is only executed on binders that
        are in the specified lifecycle and state.

        Args:
            user_action_name (str): The user action name (name__v field value)
            binder_versions (list): List of binder version specifications in the format
                                   "binder_id:major_version:minor_version" (e.g., ["222:0:1", "223:0:1"])
            lifecycle (str): Name of the binder lifecycle (e.g., "general_lifecycle__c")
            state (str): Current state of the binders (e.g., "draft__c")
            entry_criteria (dict, optional): Dictionary of entry criteria values required
                                           for the action

        Returns:
            dict: API response with responseStatus. On SUCCESS, the initiating user receives
                 a summary email detailing which binders succeeded and failed the action.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/lifecycle_actions/{user_action_name}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        data = {
            "docIds": ",".join(binder_versions),
            "lifecycle": lifecycle,
            "state": state,
        }

        # Add any entry criteria to the data
        if entry_criteria:
            data.update(entry_criteria)

        return self.client.api_call(url, method="PUT", headers=headers, data=data)