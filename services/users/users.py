import pandas as pd
from typing import Dict, List, Union, Optional, Any


class UserService:
    """
    Service class for managing users in Veeva Vault.

    This service provides methods to interact with Veeva Vault User endpoints
    for creating, retrieving, updating, and managing user accounts and permissions.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance.

        Args:
            client: An initialized VaultClient instance
        """
        self.client = client

    def retrieve_user_metadata(self) -> Dict:
        """
        Retrieves user metadata at the domain level.

        Beginning in v18.1, Admins create and manage users with user__sys object records.
        It's strongly recommended to use the Retrieve Object Metadata endpoint to retrieve user__sys metadata.

        **API Reference**: Veeva Vault API 25.2 - Users > Retrieve User Metadata
        **Endpoint**: GET /api/{version}/metadata/objects/users

        Returns:
            Dict: JSON response containing user metadata including all available fields and properties
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/users"
        return self.client.api_call(url)

    def retrieve_all_users(
        self,
        vaults: Optional[Union[str, List[str]]] = None,
        exclude_vault_membership: bool = True,
        exclude_app_licensing: bool = True,
        limit: int = 200,
        start: int = 0,
        sort: str = "id asc",
    ) -> Dict:
        """
        Retrieves user records at the domain level.

        Beginning in v18.1, Admins create and manage users with user__sys object records.
        It's strongly recommended to use the Retrieve Object Record Collection endpoint
        to retrieve user__sys records.

        Args:
            vaults: Optional. Can be one of:
                - "all" to retrieve all users assigned to all Vaults in your domain
                - "-1" to retrieve all users assigned to all Vaults except the current one
                - A list of Vault IDs as strings (e.g. ["3003", "4004", "5005"])
            exclude_vault_membership: Optional. Set to False to include vault_membership fields.
                Defaults to True (fields not included in response).
            exclude_app_licensing: Optional. Set to False to include app_licensing fields.
                Defaults to True (fields not included in response).
            limit: Optional. The size of the result set in the page (default: 200)
            start: Optional. The starting record number (default: 0)
            sort: Optional. The sort order for the result set (default: "id asc")

        Returns:
            Dict: JSON response containing user records
        """
        url = f"api/{self.client.LatestAPIversion}/objects/users"

        params = {
            "exclude_vault_membership": str(exclude_vault_membership).lower(),
            "exclude_app_licensing": str(exclude_app_licensing).lower(),
            "limit": limit,
            "start": start,
            "sort": sort,
        }

        if vaults:
            if isinstance(vaults, list):
                params["vaults"] = ",".join(vaults)
            else:
                params["vaults"] = vaults

        return self.client.api_call(url, params=params)

    def retrieve_user(
        self,
        user_id: Union[int, str],
        exclude_vault_membership: bool = True,
        exclude_app_licensing: bool = True,
    ) -> Dict:
        """
        Retrieves information for one user.

        Beginning in v18.1, Admins create and manage users with user__sys object records.
        It's strongly recommended to use the Retrieve Object Record endpoint
        to retrieve a user__sys record.

        Args:
            user_id: The user id field value
            exclude_vault_membership: Optional. Set to False to include vault_membership fields.
                Defaults to True (fields not included in response).
            exclude_app_licensing: Optional. Set to False to include app_licensing fields.
                Defaults to True (fields not included in response).

        Returns:
            Dict: JSON response containing user information
        """
        url = f"api/{self.client.LatestAPIversion}/objects/users/{user_id}"

        params = {
            "exclude_vault_membership": str(exclude_vault_membership).lower(),
            "exclude_app_licensing": str(exclude_app_licensing).lower(),
        }

        return self.client.api_call(url, params=params)

    def create_user(
        self, user_data: Dict, domain: bool = False, profile_image: Optional[str] = None
    ) -> Dict:
        """
        Creates a new user account in Veeva Vault.

        Beginning in v18.1, Admins create and manage users with user__sys object records.
        Unless you are adding cross-domain or VeevaID users or adding users to a domain
        without assigning Vault membership, it's strongly recommended to use the
        Create Object Records endpoint to create new users.

        Required fields:
            - user_name__v: The user's Vault username (login credential)
            - user_first_name__v: The user's first name
            - user_last_name__v: The user's last name
            - user_email__v: The user's email address
            - user_timezone__v: The user's time zone
            - user_locale__v: The user's location
            - security_policy_id__v: The user's security policy
            - user_language__v: The user's preferred language

        Optional fields:
            - security_profile__v: The user's security profile (default: document_user__v)
            - license_type__v: The user's license type (default: full__v)

        For cross-domain users, only the following fields are required:
            - user_name__v: The user's Vault username (login credential)
            - security_profile__v: The user's security profile (optional)
            - license_type__v: The user's license type (optional)

        For VeevaID users, only the following fields are required:
            - user_name__v: The user's Vault username (login credential)
            - security_policy_id__v: The name__v of your Vault's VeevaID security policy
            - security_profile__v: The user's security profile (optional)
            - license_type__v: The user's license type (optional)

        Args:
            user_data: Dictionary containing user information
            domain: When set to True, the user will not be assigned to a Vault
            profile_image: Optional. File path to upload a profile picture (JPG, PNG, or GIF)

        Returns:
            Dict: JSON response with the result of the operation
        """
        url = f"api/{self.client.LatestAPIversion}/objects/users"

        params = {}
        if domain:
            params["domain"] = "true"

        # Handle file upload if profile image is provided
        files = None
        if profile_image:
            files = {"file": open(profile_image, "rb")}

        return self.client.api_call(
            url, method="POST", data=user_data, params=params, files=files
        )

    def create_multiple_users(
        self,
        users_data: Union[str, List[Dict]],
        operation: Optional[str] = None,
        id_param: Optional[str] = None,
    ) -> Dict:
        """
        Creates new users and assigns them to Vaults in bulk.

        Beginning in v18.1, Admins create and manage users with user__sys object records.
        Unless you are adding cross-domain or VeevaID users or adding users to a domain
        without assigning Vault membership, it's strongly recommended to use the
        Create Object Records endpoint to create new users.

        The input can be:
        - A CSV string following RFC 4180 format
        - A list of dictionaries containing user data

        Notes:
        - The maximum input size is 1GB
        - The values must be UTF-8 encoded
        - The maximum batch size is 500

        For upsert operations, both operation and idParam must be provided.

        Args:
            users_data: CSV string or list of dictionaries with user information
            operation: Optional. Set to "upsert" to update existing users or create new ones
            id_param: Optional. For upserting, set to "id" or "user_name__v"

        Returns:
            Dict: JSON response with the result of the operation for each user
        """
        url = f"api/{self.client.LatestAPIversion}/objects/users"

        params = {}
        if operation:
            params["operation"] = operation
        if id_param:
            params["idParam"] = id_param

        headers = {}
        if isinstance(users_data, str):  # CSV input
            headers["Content-Type"] = "text/csv"
            return self.client.api_call(
                url, method="POST", data=users_data, params=params, headers=headers
            )
        else:  # JSON input (list of dictionaries)
            return self.client.api_call(
                url, method="POST", json=users_data, params=params
            )

    def update_user(self, user_id: Union[int, str], user_data: Dict) -> Dict:
        """
        Update information for a single user.

        Beginning in v18.1, Admins create and manage users with user__sys object records.
        Unless you are updating domain-only users, it's strongly recommended to use the
        Update Object Records endpoint to update users.

        Permissions:
        System Admins and Vault Owners can update users in the Vaults where they have
        administrative access. System Admins who are also Domain Admins have an
        unrestricted access to users across all Vaults in the domain.

        Special operations:
        - Disable user at domain-level: Set domain_active__v=false
        - Re-enable user at domain-level: Set domain_active__v=true
        - Promote user to Domain Admin: Set is_domain_admin__v=true
        - Update application licensing: Use app_licensing field

        Args:
            user_id: The user id field value (or "me" for the current authenticated user)
            user_data: Dictionary containing fields and values to update

        Returns:
            Dict: JSON response with the user ID and status
        """
        url = f"api/{self.client.LatestAPIversion}/objects/users/{user_id}"

        return self.client.api_call(url, method="PUT", data=user_data)

    def update_my_user(self, user_data: Dict) -> Dict:
        """
        Update information for the currently authenticated user.

        This is a convenience method that calls update_user with "me" as the user_id.

        Args:
            user_data: Dictionary containing fields and values to update

        Returns:
            Dict: JSON response with the user ID and status
        """
        return self.update_user("me", user_data)

    def update_multiple_users(self, users_data: Union[str, List[Dict]]) -> Dict:
        """
        Update information for multiple users at once.

        Beginning in v18.1, Admins create and manage users with user__sys object records.
        Unless you are updating domain-only users, it's strongly recommended to use the
        Update Object Records endpoint to update users.

        Notes:
        - The maximum input file size is 1GB
        - The values must be UTF-8 encoded
        - The maximum batch size is 500
        - This endpoint does not support the security_profile attribute

        The input must include the "id" of each user to update, along with fields to modify.

        Args:
            users_data: CSV string or list of dictionaries with user information

        Returns:
            Dict: JSON response with the result of the operation for each user
        """
        url = f"api/{self.client.LatestAPIversion}/objects/users"

        headers = {}
        if isinstance(users_data, str):  # CSV input
            headers["Content-Type"] = "text/csv"
            return self.client.api_call(
                url, method="PUT", data=users_data, headers=headers
            )
        else:  # JSON input (list of dictionaries)
            return self.client.api_call(url, method="PUT", json=users_data)

    def disable_user(self, user_id: Union[int, str], domain: bool = False) -> Dict:
        """
        Disable a user in a specific Vault or disable a user in all Vaults in the domain.

        This endpoint disables users at the domain level. Beginning in v18.1, Admins create
        and manage users with user__sys object records. To disable users in an individual Vault,
        use the single or bulk Initiate Object Action endpoint to initiate the Make User Inactive
        action on the desired records.

        Permissions:
        System Admins and Vault Owners can update users in the Vaults where they have
        administrative access. System Admins who are also Domain Admins have an
        unrestricted access to users across all Vaults in the domain.

        Args:
            user_id: The user id field value
            domain: Optional. When True, this disables the user account in all Vaults in the domain

        Returns:
            Dict: JSON response with the user ID and status
        """
        url = f"api/{self.client.LatestAPIversion}/objects/users/{user_id}"

        params = {}
        if domain:
            params["domain"] = "true"

        return self.client.api_call(url, method="DELETE", params=params)

    def change_my_password(self, current_password: str, new_password: str) -> Dict:
        """
        Change the password for the currently authenticated user.

        Passwords must meet minimum requirements, which are configured by your Vault Admin.

        Args:
            current_password: The user's current password
            new_password: The user's desired new password (must be different from current)

        Returns:
            Dict: JSON response with the operation status
        """
        url = f"api/{self.client.LatestAPIversion}/objects/users/me/password"

        data = {"password__v": current_password, "new_password__v": new_password}

        return self.client.api_call(url, method="POST", data=data)

    def update_vault_membership(
        self,
        user_id: Union[int, str],
        vault_id: Union[int, str],
        active: Optional[bool] = None,
        security_profile: Optional[str] = None,
        license_type: Optional[str] = None,
    ) -> Dict:
        """
        Updates a user's Vault membership, security profile, and license type.

        This endpoint can be used to:
        - Assign an existing user to a Vault in your domain
        - Remove (disable) an existing user from a Vault in your domain
        - Update the security profile and license type of an existing user

        Permissions:
        System Admins and Vault Owners can update users in the Vaults where they have
        administrative access. System Admins who are also Domain Admins have an
        unrestricted access to users across all Vaults in the domain.

        Args:
            user_id: The user id field value
            vault_id: The system-managed id field value assigned to each Vault in the domain
            active: Optional. Set the user status to active (True) or inactive (False)
            security_profile: Optional. The user's security profile (defaults to document_user__v)
            license_type: Optional. The user's license type (defaults to full__v)

        Returns:
            Dict: JSON response with the operation status
        """
        url = f"api/{self.client.LatestAPIversion}/objects/users/{user_id}/vault_membership/{vault_id}"

        data = {}
        if active is not None:
            data["active__v"] = str(active).lower()
        if security_profile:
            data["security_profile__v"] = security_profile
        if license_type:
            data["license_type__v"] = license_type

        return self.client.api_call(url, method="PUT", data=data)

    def retrieve_application_license_usage(self) -> Dict:
        """
        Retrieve your current license usage compared to the licenses that your organization has purchased.

        This information is similar to the information displayed in the Vault UI from
        Admin > Settings > General Settings.

        Some Vaults use multiple applications, for example, a RIM Vault with Submissions and
        Registrations. In these Vaults, users have a license value for each application they can access.
        Application licensing allows Vault to track available licenses at the application level,
        but does not control a user's access in most Vaults.

        Returns:
            Dict: JSON response with license usage information, including:
                - doc_count: Document views information (PromoMats and Veeva Medical only)
                - applications: An array of application license information
        """
        url = f"api/{self.client.LatestAPIversion}/objects/licenses"

        return self.client.api_call(url, method="GET")

    def retrieve_user_permissions(
        self, user_id: Union[int, str], permission_name: Optional[str] = None
    ) -> Dict:
        """
        Retrieve all object and object field permissions (Read, Edit, Create, Delete)
        assigned to a specific user.

        Args:
            user_id: The ID of the user, or "me" for the currently authenticated user
            permission_name: Optional. Filter to show only a specific permission in the format
                            object.{object name}.{object or field}_actions

        Returns:
            Dict: JSON response with permissions information
        """
        url = f"api/{self.client.LatestAPIversion}/objects/users/{user_id}/permissions"

        params = {}
        if permission_name:
            params["filter"] = f"name__v::{permission_name}"

        return self.client.api_call(url, method="GET", params=params)

    def retrieve_my_permissions(self, permission_name: Optional[str] = None) -> Dict:
        """
        Retrieve all object and object field permissions (Read, Edit, Create, Delete)
        assigned to the currently authenticated user.

        This is a convenience method that calls retrieve_user_permissions with "me" as the user_id.

        Args:
            permission_name: Optional. Filter to show only a specific permission in the format
                            object.{object name}.{object or field}_actions

        Returns:
            Dict: JSON response with permissions information
        """
        return self.retrieve_user_permissions("me", permission_name)

    def validate_session_user(
        self, exclude_vault_membership: bool = True, exclude_app_licensing: bool = True
    ) -> Dict:
        """
        Given a valid session ID, this request returns information for the currently
        authenticated user. If the session ID is not valid, this request returns an
        INVALID_SESSION_ID error type.

        This is similar to a whoami request. Do not use this API to refresh the current
        session duration. To do this, use the Session Keep Alive API.

        Note: When interpreting the response, understand that the following fields are
        based on the Vault user, rather than the domain user:
        - created_date__v
        - created_by__v
        - modified_date__v
        - modified_by__v
        - last_login__v

        If the currently authenticated user is in a delegated session, this request returns
        a delegate_user_id.

        Args:
            exclude_vault_membership: Optional. Set to False to include vault_membership fields.
                Defaults to True (fields not included in response).
            exclude_app_licensing: Optional. Set to False to include app_licensing fields.
                Defaults to True (fields not included in response).

        Returns:
            Dict: JSON response with user information or error
        """
        url = f"api/{self.client.LatestAPIversion}/objects/users/me"

        params = {
            "exclude_vault_membership": str(exclude_vault_membership).lower(),
            "exclude_app_licensing": str(exclude_app_licensing).lower(),
        }

        return self.client.api_call(url, method="GET", params=params)
