import json
from .base_service import BaseObjectService


class ObjectRolesService(BaseObjectService):
    """
    Service class for handling Veeva Vault object role operations.

    Object records can have different roles available to them depending on their
    type and lifecycles. Standard roles include owner__v, viewer__v, and editor__v,
    and Admins can create custom roles defined per lifecycle.
    """

    def retrieve_object_record_roles(self, object_name, record_id, role_name=None):
        """
        Retrieves the roles assigned to an object record.

        GET /api/{version}/vobjects/{object_name}/{id}/roles{/role_name}

        Args:
            object_name (str): API name of the object
            record_id (str): ID of the record
            role_name (str, optional): Name of a specific role to retrieve (e.g., "owner__v")

        Returns:
            dict: Information about roles assigned to the record, including users and groups
                 assigned to each role and the assignment_type

        Notes:
            - Standard roles include owner__v, viewer__v, and editor__v
            - Admins can create custom roles defined per lifecycle
            - Even though owner__v role is automatically assigned when applying Custom Sharing Rules,
              the assignment_type for roles on objects is always manual_assignment
        """
        base_url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/{record_id}/roles"
        url = f"{base_url}/{role_name}" if role_name else base_url

        return self.client.api_call(url)

    def assign_users_groups_to_roles_on_object_records(self, object_name, request_body):
        """
        Assigns users and groups to roles on object records in bulk.

        POST /api/{version}/vobjects/{object_name}/roles

        Args:
            object_name (str): API name of the object
            request_body (dict): JSON structure specifying role assignments

        Returns:
            dict: Result of the role assignment operation

        Notes:
            - Maximum CSV input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow RFC 4180 format
            - Maximum batch size is 500
            - Assigning users and groups to roles is additive, and duplicate groups are ignored
            - User and group assignments are ignored if they are invalid, inactive, or already exist
            - Required fields:
              - id: The object record ID
              - role__v.users: String of user ID values for the role (optional)
              - role__v.groups: String of group ID values for the role (optional)
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/roles"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(request_body)

        return self.client.api_call(url, method="POST", headers=headers, data=data)

    def remove_users_groups_from_roles_on_object_records(
        self, object_name, request_body
    ):
        """
        Removes users and groups from roles on object records in bulk.

        DELETE /api/{version}/vobjects/{object_name}/roles

        Args:
            object_name (str): API name of the object
            request_body (dict): JSON structure specifying role assignments to remove

        Returns:
            dict: Result of the role removal operation

        Notes:
            - Maximum CSV input file size is 1GB
            - Values must be UTF-8 encoded
            - CSVs must follow RFC 4180 format
            - Maximum batch size is 500
            - Users and groups are ignored if they are invalid or inactive
            - Required fields:
              - id: The object record ID
              - role__v.users: String of user ID values to remove (optional)
              - role__v.groups: String of group ID values to remove (optional)
        """
        url = f"api/{self.client.LatestAPIversion}/vobjects/{object_name}/roles"

        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        data = json.dumps(request_body)

        return self.client.api_call(url, method="DELETE", headers=headers, data=data)
