import json
from .base_service import BaseBinderService


class BinderRolesService(BaseBinderService):
    """
    Service class for managing binder roles in Veeva Vault.

    This service provides methods to interact with binder roles, including
    retrieving available roles, determining who can be assigned to roles,
    retrieving users assigned to roles, and adding/removing users and groups.

    Through the Role APIs, you can:
    - Retrieve available roles on binders
    - Determine who can be assigned to roles
    - Retrieve default users who are assigned automatically within the Vault UI
    - Retrieve who is currently assigned to a role
    - Add additional users and groups to a role
    - Remove users and groups from roles

    All responses return user and group IDs. To determine user and group names
    and other data, use the Users or Groups API.
    """

    def retrieve_binder_roles(self, binder_id, role_name=None):
        """
        Retrieve all available roles on a binder and the users and groups assigned to them.

        API Documentation: https://developer.veevavault.com/api/25.1/#retrieve-all-binder-roles

        Args:
            binder_id (str): The binder id field value.
            role_name (str, optional): If provided, retrieves only the specified role.

        Returns:
            dict: API response containing binder roles with the following structure for each role:
                - name: The role name available to developers (e.g., "reviewer__v")
                - label: The UI-friendly role label available to Admins (e.g., "Reviewer")
                - assignedUsers: List of IDs of users assigned to this role
                - assignedGroups: List of IDs of groups assigned to this role
                - availableUsers: List of IDs of users available for this role
                - availableGroups: List of IDs of groups available to this role
                - defaultUsers: List of IDs of default users assigned to this role
                - defaultGroups: List of IDs of default groups assigned to this role
        """
        base_url = (
            f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/roles"
        )
        url = f"{base_url}/{role_name}" if role_name else base_url

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def assign_users_groups_to_binder_roles(self, binder_id, role_assignments):
        """
        Assign users and groups to roles on a single binder.

        API Documentation: https://developer.veevavault.com/api/25.1/#assign-users-groups-to-roles-on-a-single-binder

        To assign users and groups to roles on multiple binders, use the documents service's
        assign_users_groups_to_documents_batch() method which handles both documents and binders.

        Args:
            binder_id (str): The binder id field value.
            role_assignments (dict): Dictionary with role assignments, where keys are in the format
                                    "{role_name}.users" or "{role_name}.groups" and values are
                                    comma-separated strings of user or group IDs.
                                    Example: {"reviewer__v.users": "12021,12022",
                                             "consumer__v.groups": "3311303,3311404"}

        Returns:
            dict: API response with details of the users and groups successfully assigned to each role.
                 Example: {
                    "responseStatus": "SUCCESS",
                    "responseMessage": "Roles updated",
                    "updatedRoles": {
                        "reviewer__v": {
                            "users": [12021, 12022],
                            "groups": [3311303, 3311404]
                        }
                    }
                 }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/roles"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(
            url, method="POST", headers=headers, data=role_assignments
        )

    def remove_user_group_from_binder_role(
        self, binder_id, role_name_and_user_or_group, id_value
    ):
        """
        Remove a user or group from a role on a binder.

        API Documentation: https://developer.veevavault.com/api/25.1/#remove-users-groups-from-roles-on-a-single-binder

        To remove users and groups from roles on multiple binders, use the documents service's
        remove_users_groups_from_document_roles_batch() method which handles both documents and binders.

        Args:
            binder_id (str): The binder ID from which to remove roles.
            role_name_and_user_or_group (str): Role name followed by 'user' or 'group'.
                                             Format: "{role_name}.{user_or_group}"
                                             Example: "consumer__v.user" or "reviewer__v.group"
            id_value (str): The ID of the user or group to remove from the role.

        Returns:
            dict: API response indicating success or failure of the removal operation.
                 Example: {
                    "responseStatus": "SUCCESS",
                    "responseMessage": "User/group deleted from role",
                    "updatedRoles": {
                        "consumer__v": {
                            "users": [1008313]
                        }
                    }
                 }

                 On FAILURE, the response returns an error message describing the reason for the
                 failure. For example, a user or group may not be removed if the role assignment
                 is system-managed.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/binders/{binder_id}/roles/{role_name_and_user_or_group}/{id_value}"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, method="DELETE", headers=headers)
