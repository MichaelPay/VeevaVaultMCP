import json
from .base_service import BaseDocumentService


class DocumentRolesService(BaseDocumentService):
    """
    Service class for managing document roles in Veeva Vault.

    This service provides methods to interact with document roles, including
    retrieving available roles, determining who can be assigned to roles,
    retrieving users assigned to roles, and adding/removing users and groups.

    Through the Role APIs, you can:
    - Retrieve available roles on documents
    - Determine who can be assigned to roles
    - Retrieve default users who are assigned automatically within the Vault UI
    - Retrieve who is currently assigned to a role
    - Add additional users and groups to a role
    - Remove users and groups from roles

    All responses return user and group IDs. To determine user and group names
    and other data, use the Users or Groups API.
    """

    def retrieve_document_roles(self, doc_id, role_name=None):
        """
        Retrieve all available roles on a document and the users and groups assigned to them.

        API Documentation: https://developer.veevavault.com/api/25.1/#retrieve-all-document-roles

        Args:
            doc_id (str): The document id field value.
            role_name (str, optional): If provided, retrieves only the specified role.

        Returns:
            dict: API response containing document roles with the following structure for each role:
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
            f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/roles"
        )
        url = f"{base_url}/{role_name}" if role_name else base_url

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def assign_users_groups_to_document_roles(self, doc_id, role_assignments):
        """
        Assign users and groups to roles on a single document.

        API Documentation: https://developer.veevavault.com/api/25.1/#assign-users-groups-to-roles-on-a-single-document

        If you need to assign users and groups to roles on more than one document, it is best
        practice to use the bulk API method assign_users_groups_to_documents_batch().

        Args:
            doc_id (str): The document id field value.
            role_assignments (dict): Dictionary with role assignments, where keys are in the format
                                    "{role_name}.users" or "{role_name}.groups" and values are
                                    comma-separated strings of user or group IDs.
                                    Example: {"reviewer__v.users": "12021,12022",
                                             "consumer__v.groups": "3311303,3311404"}

        Returns:
            dict: API response with details of the users and groups successfully assigned to each role.
                 Example: {
                    "responseStatus": "SUCCESS",
                    "responseMessage": "Document roles updated",
                    "updatedRoles": {
                        "reviewer__v": {
                            "users": [12021, 12022],
                            "groups": [3311303, 3311404]
                        }
                    }
                 }
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/roles"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        return self.client.api_call(
            url, method="POST", headers=headers, data=role_assignments
        )

    def assign_users_groups_to_documents_batch(
        self, batch_data, content_type="text/csv", accept="application/json"
    ):
        """
        Assign users and groups to roles on multiple documents and binders in bulk.

        API Documentation: https://developer.veevavault.com/api/25.1/#assign-users-groups-to-roles-on-multiple-documents-binders

        Notes:
        - The maximum CSV input file size is 1GB
        - The values in the input must be UTF-8 encoded
        - CSVs must follow the standard RFC 4180 format, with some exceptions
        - The maximum batch size is 1000
        - Assigning users and groups to document roles is additive (existing assignments are preserved)
        - Invalid user/group IDs or those that cannot be assigned due to permissions are ignored

        Args:
            batch_data: CSV content as string or file-like object containing role assignments.
                       For CSV format, headers should include:
                       - id: The document or binder ID
                       - {role_name}.users: User IDs to assign to the role (comma-separated)
                       - {role_name}.groups: Group IDs to assign to the role (comma-separated)

                       Alternatively, when using application/x-www-form-urlencoded format:
                       - docIds: A list of document and binder IDs
                       - {role_name}.users: User IDs to assign to the role (comma-separated)
                       - {role_name}.groups: Group IDs to assign to the role (comma-separated)
            content_type (str, optional): Content type of the batch data. Either "text/csv" or
                                         "application/x-www-form-urlencoded". Defaults to "text/csv".
            accept (str, optional): Desired response format. Either "application/json" or "application/xml".
                                   Defaults to "application/json".

        Returns:
            dict: API response with details of the role assignments, including success/failure
                 information for each document or binder.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/roles/batch"

        headers = {"Content-Type": content_type, "Accept": accept}

        return self.client.api_call(
            url, method="POST", headers=headers, data=batch_data
        )

    def remove_user_group_from_document_role(
        self, doc_id, role_name_and_user_or_group, id_value
    ):
        """
        Remove a user or group from a role on a document.

        API Documentation: https://developer.veevavault.com/api/25.1/#remove-users-groups-from-roles-on-a-single-document

        If you need to remove users and groups from roles on more than one document, it is best
        practice to use the bulk API method remove_users_groups_from_document_roles_batch().

        Args:
            doc_id (str): The document ID from which to remove roles.
            role_name_and_user_or_group (str): Role name followed by 'user' or 'group'.
                                             Format: "{role_name}.{user_or_group}"
                                             Example: "consumer__v.user" or "reviewer__v.group"
            id_value (str): The ID of the user or group to remove from the role.

        Returns:
            dict: API response indicating success or failure of the removal operation.
                 Example: {
                    "responseStatus": "SUCCESS",
                    "responseMessage": "User/group deleted from document role",
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
        url = f"api/{self.client.LatestAPIversion}/objects/documents/{doc_id}/roles/{role_name_and_user_or_group}/{id_value}"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, method="DELETE", headers=headers)

    def remove_users_groups_from_document_roles_batch(
        self, batch_data, content_type="text/csv", accept="application/json"
    ):
        """
        Remove users and groups from roles on multiple documents and binders in bulk.

        API Documentation: https://developer.veevavault.com/api/25.1/#remove-users-groups-from-roles-on-multiple-documents-binders

        Notes:
        - The maximum CSV input file size is 1GB
        - The values in the input must be UTF-8 encoded
        - CSVs must follow the standard RFC 4180 format, with some exceptions
        - The maximum batch size is 1000

        Args:
            batch_data: CSV content as string or file-like object containing role removals.
                       For CSV format, headers should include:
                       - id: The document or binder ID
                       - {role_name}.users: User IDs to remove from the role (comma-separated)
                       - {role_name}.groups: Group IDs to remove from the role (comma-separated)

                       Alternatively, when using application/x-www-form-urlencoded format:
                       - docIds: A list of document and binder IDs
                       - {role_name}.users: User IDs to remove from the role (comma-separated)
                       - {role_name}.groups: Group IDs to remove from the role (comma-separated)
            content_type (str, optional): Content type of the batch data. Either "text/csv" or
                                         "application/x-www-form-urlencoded". Defaults to "text/csv".
            accept (str, optional): Desired response format. Either "application/json" or "application/xml".
                                   Defaults to "application/json".

        Returns:
            dict: API response with details of the role removals, including success/failure
                 information for each document or binder.

                 On SUCCESS, the response lists the IDs of the users or groups removed from the
                 provided document roles. On FAILURE, the response returns an error message describing
                 the reason for the failure. For example, a user or group may not be removed if the
                 role assignment is system-managed.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/documents/roles/batch"

        headers = {"Content-Type": content_type, "Accept": accept}

        return self.client.api_call(
            url, method="DELETE", headers=headers, data=batch_data
        )
