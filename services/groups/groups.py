import pandas as pd


class GroupsService:
    """
    Service class for managing groups in Veeva Vault

    Groups are key to managing user access in Vault. A group is simply a named list of users.
    By defining groups which reflect the teams and roles in your company, and then assigning
    those groups to document roles, you can manage document access more easily and efficiently.

    In Vaults using Dynamic Access Control (DAC) for documents, Vault also automatically creates
    groups that correspond to one lifecycle role and additional document field criteria.
    These are called Auto Managed Groups.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        :param client: An initialized VaultClient instance
        """
        self.client = client

    def retrieve_group_metadata(self):
        """
        Retrieves metadata about group objects in Vault.

        **API Reference**: Veeva Vault API 25.2 - Groups > Retrieve Group Metadata
        **Endpoint**: GET /api/{version}/metadata/objects/groups

        Returns:
            dict: The JSON response containing metadata for the groups object
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/groups"

        return self.client.api_call(url)

    def retrieve_all_groups(self, include_implied=False):
        """
        Retrieves all groups except Auto Managed groups.

        Args:
            include_implied (bool, optional): When true, the response includes the implied_members__v field.
                These users are automatically added to the group when their security_profiles__v are added to the group.
                If omitted, the response includes only the members__v field. These users are individually
                added to a group by an Admin. Defaults to False.

        Returns:
            dict: The JSON response containing all groups
        """
        url = f"api/{self.client.LatestAPIversion}/objects/groups"

        params = {}
        if include_implied:
            params["includeImplied"] = "true"

        return self.client.api_call(url, params=params)

    def retrieve_auto_managed_groups(self, limit=1000, offset=0):
        """
        Retrieves all Auto Managed groups.

        Auto Managed groups correspond to one lifecycle role and additional document field criteria
        in Vaults using Dynamic Access Control (DAC) for documents.

        Args:
            limit (int, optional): Paginate the results by specifying the maximum number of records per page.
                This can be any value between 1 and 1000. Defaults to 1000.
            offset (int, optional): Paginate the results displayed per page by specifying the amount of offset
                from the entry returned. For example, if you are viewing the first 50 results (page 1) and want
                to see the next page, set this to offset=51. Defaults to 0.

        Returns:
            dict: The JSON response containing all Auto Managed groups
        """
        url = f"api/{self.client.LatestAPIversion}/objects/groups/auto"

        params = {"limit": limit, "offset": offset}

        return self.client.api_call(url, params=params)

    def retrieve_group(self, group_id, include_implied=False):
        """
        Retrieves details of a specific group by ID.

        Args:
            group_id (int): The group id field value
            include_implied (bool, optional): When true, the response includes the implied_members__v field.
                These users are automatically added to the group when their security_profiles__v are added to the group.
                When not used, the response includes only the members__v field. These users are individually
                added to a group by Admin. Defaults to False.

        Returns:
            dict: The JSON response containing the group details
        """
        url = f"api/{self.client.LatestAPIversion}/objects/groups/{group_id}"

        params = {}
        if include_implied:
            params["includeImplied"] = "true"

        return self.client.api_call(url, params=params)

    def create_group(
        self,
        label,
        members=None,
        security_profiles=None,
        active=True,
        description=None,
        allow_delegation_among_members=False,
    ):
        """
        Creates a new group in Vault.

        Args:
            label (str): The group label. Vault uses this to create the group name__v value.
            members (list, optional): List of user IDs to manually assign to the group. Defaults to None.
            security_profiles (list, optional): List of security profiles. This automatically adds all users
                with the security profile to the group. These are implied_members__v. Defaults to None.
            active (bool, optional): By default, the new group will be created as active.
                To set the group to inactive, set this value to False. Defaults to True.
            description (str, optional): A description of the group. Defaults to None.
            allow_delegation_among_members (bool, optional): When set to true, members of this group will only
                be allowed to delegate access to other members of the same group. You can set this field for
                user and system managed groups, with the exception of the Vault Owners group. Defaults to False.

        Returns:
            dict: The JSON response containing the new group ID
        """
        url = f"api/{self.client.LatestAPIversion}/objects/groups"

        data = {"label__v": label}

        if members:
            data["members__v"] = ",".join(str(member) for member in members)

        if security_profiles:
            data["security_profiles__v"] = ",".join(security_profiles)

        if not active:
            data["active__v"] = "false"

        if description:
            data["group_description__v"] = description

        if allow_delegation_among_members:
            data["allow_delegation_among_members__v"] = "true"

        return self.client.api_call(url, method="POST", data=data)

    def update_group(
        self,
        group_id,
        label=None,
        members=None,
        security_profiles=None,
        active=None,
        description=None,
        allow_delegation_among_members=None,
    ):
        """
        Updates an existing group in Vault.

        To add or remove group members without replacing previous users, you can:
        - To add users, set members to a list with the first element being 'add' followed by user IDs.
          For example: ['add', 123, 456]
        - To delete users, set members to a list with the first element being 'delete' followed by user IDs.
          For example: ['delete', 123, 456]

        Changing the security_profiles will automatically replace all previous implied users
        assigned via the previous security profile.

        Args:
            group_id (int): The group id field value
            label (str, optional): Updates the label of the group. Defaults to None.
            members (list, optional): List of user IDs or special format list (see description). Defaults to None.
            security_profiles (list, optional): List of security profiles. Defaults to None.
            active (bool, optional): To set the group to inactive, set this value to False. Defaults to None.
            description (str, optional): Updates the description of the group. Defaults to None.
            allow_delegation_among_members (bool, optional): When set to true, members of this group will only
                be allowed to delegate access to other members of the same group. Defaults to None.

        Returns:
            dict: The JSON response containing the updated group ID
        """
        url = f"api/{self.client.LatestAPIversion}/objects/groups/{group_id}"

        data = {}

        if label is not None:
            data["label__v"] = label

        if members is not None:
            if (
                members
                and isinstance(members[0], str)
                and members[0].lower() in ["add", "delete"]
            ):
                action = members[0].lower()
                user_ids = [str(m) for m in members[1:]]
                data["members__v"] = f"{action} ({','.join(user_ids)})"
            else:
                data["members__v"] = ",".join(str(member) for member in members)

        if security_profiles is not None:
            data["security_profiles__v"] = ",".join(security_profiles)

        if active is not None:
            data["active__v"] = "true" if active else "false"

        if description is not None:
            data["group_description__v"] = description

        if allow_delegation_among_members is not None:
            data["allow_delegation_among_members__v"] = (
                "true" if allow_delegation_among_members else "false"
            )

        return self.client.api_call(url, method="PUT", data=data)

    def delete_group(self, group_id):
        """
        Deletes a user-defined group. You cannot delete system-managed groups.

        Args:
            group_id (int): The group id field value

        Returns:
            dict: The JSON response containing the deleted group ID
        """
        url = f"api/{self.client.LatestAPIversion}/objects/groups/{group_id}"

        return self.client.api_call(url, method="DELETE")
