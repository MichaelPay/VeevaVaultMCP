import pandas as pd
import requests
from typing import Dict, List, Optional, Union, Any


class SCIMService:
    """
    Service class for managing SCIM (System for Cross-domain Identity Management) in Veeva Vault.

    SCIM is designed to make managing user identities in cloud-based applications and services easier.
    Vault API is based on SCIM 2.0.

    All SCIM endpoints require a Vault session ID which can be used as Bearer tokens.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        :param client: An initialized VaultClient instance
        """
        self.client = client

    # Discovery Endpoints

    def retrieve_scim_provider(self) -> Dict[str, Any]:
        """
        Retrieve a JSON that describes the SCIM specification features available on the currently
        authenticated Vault.

        Returns:
            dict: The JSON response containing the SCIM provider configuration.
                  The attributes returned in the JSON object are defined in Section 5 of RFC7643.
        """
        url = f"api/{self.client.LatestAPIversion}/scim/v2/ServiceProviderConfig"

        return self.client.api_call(url)

    def retrieve_all_scim_schemas(self) -> Dict[str, Any]:
        """
        Retrieve information about all SCIM schema specifications supported by a Vault SCIM service provider.

        Returns:
            dict: The JSON response containing all supported SCIM schemas
        """
        url = f"api/{self.client.LatestAPIversion}/scim/v2/Schemas"

        return self.client.api_call(url)

    def retrieve_single_scim_schema(self, schema_id: str) -> Dict[str, Any]:
        """
        Retrieve information about a single SCIM schema specification supported by a Vault SCIM service provider.

        Args:
            schema_id (str): The ID of a specific schema.
                             For example, urn:ietf:params:scim:schemas:extension:veevavault:2.0:User.

        Returns:
            dict: The JSON response containing the specified SCIM schema
        """
        url = f"api/{self.client.LatestAPIversion}/scim/v2/Schemas/{schema_id}"

        return self.client.api_call(url)

    def retrieve_all_scim_resource_types(self) -> Dict[str, Any]:
        """
        Retrieve the types of SCIM resources available. Each resource type defines the endpoints,
        the core schema URI that defines the resource, and any supported schema extensions.

        Returns:
            dict: The JSON response containing all SCIM resource types
        """
        url = f"api/{self.client.LatestAPIversion}/scim/v2/ResourceTypes"

        return self.client.api_call(url)

    def retrieve_single_scim_resource_type(self, resource_type: str) -> Dict[str, Any]:
        """
        Retrieve a single SCIM resource type. Defines the endpoints, the core schema URI which
        defines this resource, and any supported schema extensions.

        Args:
            resource_type (str): A specific resource type. You can retrieve all available types
                                from the Retrieve All SCIM Resource Types endpoint, where the
                                value for this parameter is the id value.

        Returns:
            dict: The JSON response containing the specified SCIM resource type
        """
        url = (
            f"api/{self.client.LatestAPIversion}/scim/v2/ResourceTypes/{resource_type}"
        )

        return self.client.api_call(url)

    # Users Endpoints

    def retrieve_all_users(
        self,
        filter: Optional[str] = None,
        attributes: Optional[str] = None,
        excluded_attributes: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "ascending",
        count: Optional[int] = 1000,
        start_index: Optional[int] = 1,
    ) -> Dict[str, Any]:
        """
        Retrieve all users with SCIM.

        Args:
            filter (str, optional): Filter for a specific attribute value.
                                   Must be in the format {attribute} eq "{value}".
                                   For example, to filter for a particular user name, userName eq "john".
                                   Complex expressions are not supported, and eq is the only supported operator.
            attributes (str, optional): Include specified attributes only.
                                      Enter multiple values in a comma separated list.
                                      For example, to include only user name and email in the response,
                                      attributes=userName,emails.
                                      Note that the schemas and id attributes are always returned.
            excluded_attributes (str, optional): Exclude specific attributes from the response.
                                               Enter multiple values in a comma separated list.
                                               For example, to exclude user name and email from the response,
                                               excludedAttributes=userName,emails.
                                               Note that the schemas and id attributes are always returned
                                               and cannot be excluded.
            sort_by (str, optional): Specify an attribute or sub-attribute to order the response.
                                    For example, you can sort by the displayName attribute,
                                    or the name.familyName sub-attribute.
                                    If omitted, the response is sorted by id.
                                    Note that the following attributes are not supported:
                                    securityPolicy, securityProfile, locale, preferredLanguage
            sort_order (str, optional): Specify the order in which the sortBy parameter is applied.
                                       Allowed values are ascending or descending.
                                       If omitted, defaults to ascending.
            count (int, optional): Specify the number of query results per page, for example, 10.
                                  Negative values are treated as 0, and 0 returns no results except for totalResults.
                                  If omitted, defaults to 1000.
            start_index (int, optional): Specify the index of the first result.
                                        For example, 10 would omit the first 9 results and begin on result 10.
                                        Omission, negative values, and 0 is treated as 1.

        Returns:
            dict: The JSON response containing users data
        """
        url = f"api/{self.client.LatestAPIversion}/scim/v2/Users"

        params = {}

        if filter:
            params["filter"] = filter
        if attributes:
            params["attributes"] = attributes
        if excluded_attributes:
            params["excludedAttributes"] = excluded_attributes
        if sort_by:
            params["sortBy"] = sort_by
        if sort_order:
            params["sortOrder"] = sort_order
        if count:
            params["count"] = count
        if start_index:
            params["startIndex"] = start_index

        return self.client.api_call(url, params=params)

    def retrieve_single_user(
        self,
        user_id: str,
        filter: Optional[str] = None,
        attributes: Optional[str] = None,
        excluded_attributes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a specific user with SCIM.

        Args:
            user_id (str): The ID of a specific user.
            filter (str, optional): Filter for a specific attribute value.
                                   Must be in the format {attribute} eq "{value}".
                                   For example, to filter for a particular user name, userName eq "john".
                                   Complex expressions are not supported, and eq is the only supported operator.
            attributes (str, optional): Include specified attributes only.
                                      Enter multiple values in a comma separated list.
                                      For example, to include only user name and email in the response,
                                      attributes=userName,emails.
                                      Note that the schemas and id attributes are always returned.
            excluded_attributes (str, optional): Exclude specific attributes from the response.
                                               Enter multiple values in a comma separated list.
                                               For example, to exclude user name and email from the response,
                                               excludedAttributes=userName,emails.
                                               Note that the schemas and id attributes are always returned
                                               and cannot be excluded.

        Returns:
            dict: The JSON response containing the specified user data
        """
        url = f"api/{self.client.LatestAPIversion}/scim/v2/Users/{user_id}"

        params = {}

        if filter:
            params["filter"] = filter
        if attributes:
            params["attributes"] = attributes
        if excluded_attributes:
            params["excludedAttributes"] = excluded_attributes

        return self.client.api_call(url, params=params)

    def retrieve_current_user(
        self,
        attributes: Optional[str] = None,
        excluded_attributes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve the currently authenticated user with SCIM.

        Args:
            attributes (str, optional): Include specified attributes only.
                                      Enter multiple values in a comma separated list.
                                      For example, to include only user name and email in the response,
                                      attributes=userName,emails.
                                      Note that the schemas and id attributes are always returned.
            excluded_attributes (str, optional): Exclude specific attributes from the response.
                                               Enter multiple values in a comma separated list.
                                               For example, to exclude user name and email from the response,
                                               excludedAttributes=userName,emails.
                                               Note that the schemas and id attributes are always returned
                                               and cannot be excluded.

        Returns:
            dict: The JSON response containing the current user data
        """
        url = f"api/{self.client.LatestAPIversion}/scim/v2/Me"

        params = {}

        if attributes:
            params["attributes"] = attributes
        if excluded_attributes:
            params["excludedAttributes"] = excluded_attributes

        return self.client.api_call(url, params=params)

    def update_current_user(
        self,
        user_data: Dict[str, Any],
        attributes: Optional[str] = None,
        excluded_attributes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update the currently authenticated user with SCIM.

        Args:
            user_data (dict): A dictionary with the information you want to update for your user.
                             You can include any editable attribute. Invalid attributes are ignored.
                             You can set single-valued attributes to blank using null, or an empty
                             array [] for multi-valued attributes.
                             You can determine which of the core attributes are editable based on schemas.
                             If the mutability is readWrite, the attribute is editable.
            attributes (str, optional): Include specified attributes only in the response.
                                      Enter multiple values in a comma separated list.
                                      For example, to include only user name and email in the response,
                                      attributes=userName,emails.
                                      Note that the schemas and id attributes are always returned.
            excluded_attributes (str, optional): Exclude specific attributes from the response.
                                               Enter multiple values in a comma separated list.
                                               For example, to exclude user name and email from the response,
                                               excludedAttributes=userName,emails.
                                               Note that the schemas and id attributes are always returned
                                               and cannot be excluded.

        Returns:
            dict: The JSON response containing the updated user data
        """
        url = f"api/{self.client.LatestAPIversion}/scim/v2/Me"

        params = {}

        if attributes:
            params["attributes"] = attributes
        if excluded_attributes:
            params["excludedAttributes"] = excluded_attributes

        return self.client.api_call(url, method="PUT", json=user_data, params=params)

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a user with SCIM.

        The following fields are required:
        - schemas: A JSON array of the schemas required to create this user. These may differ
                  depending on the fields you wish to set for this user.
        - userName: The user name for the new user. Must be in the format name@domain.com,
                  and the domain must match the Vault.
        - emails: A JSON array with the email information for a user with:
                - value: The email address in the format name@domain.com.
                - type: The email type, which is work. Other types are not supported.
                Note that the primary sub-attribute is ignored.
        - name: A JSON object for the user's first name (givenName) and last name (familyName).
        - preferredLanguage: The language for the user. Value is the language abbreviation, for example, en.
        - locale: The user's locale, in the format language_country. For example, en_US.
        - timezone: The user's timezone, for example, America/Los_Angeles.
        - securityProfile: A JSON object with the user's security profile, set with the value sub-attribute.

        These fields are optional:
        - securityPolicy: A JSON object with the user's security policy, set with the value sub-attribute.
                         If omitted, defaults to Basic.
        - licenseType: A JSON object with the user's license type, set with the value sub-attribute.
                      If omitted, defaults to full__v.

        Example user_data:
        {
            "schemas": [
                "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User",
                "urn:ietf:params:scim:schemas:core:2.0:User"
            ],
            "userName": "user@domain.com",
            "emails": [
                {
                    "value": "user@domain.com",
                    "type": "work"
                }
            ],
            "name": {
                "familyName": "Last",
                "givenName": "First"
            },
            "preferredLanguage": "en",
            "locale": "en_US",
            "timezone": "America/Los_Angeles",
            "urn:ietf:params:scim:schemas:extension:veevavault:2.0:User": {
                "securityProfile": {
                    "value": "system_admin__v"
                }
            }
        }

        Args:
            user_data (dict): A dictionary with the required information for your new user.

        Returns:
            dict: The JSON response containing the full details of the newly created user
        """
        url = f"api/{self.client.LatestAPIversion}/scim/v2/Users"

        headers = {"Content-Type": "application/scim+json"}

        return self.client.api_call(url, method="POST", json=user_data, headers=headers)

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update fields values on a single user with SCIM.

        Args:
            user_id (str): The id of the user you wish to update.
            user_data (dict): A dictionary with the information you want to update for your user.
                             You can include any editable attribute. Invalid attributes are ignored.
                             You can set single-valued attributes to blank using null, or an empty
                             array [] for multi-valued attributes.
                             You can determine which of the core attributes are editable based on schemas.
                             If the mutability is readWrite, the attribute is editable.

        Returns:
            dict: The JSON response containing the new information for the updated user
        """
        url = f"api/{self.client.LatestAPIversion}/scim/v2/Users/{user_id}"

        headers = {"Content-Type": "application/scim+json"}

        return self.client.api_call(url, method="PUT", json=user_data, headers=headers)

    # Generic SCIM Resources

    def retrieve_scim_resources(
        self,
        resource_type: str,
        filter: Optional[str] = None,
        attributes: Optional[str] = None,
        excluded_attributes: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "ascending",
        count: Optional[int] = 1000,
        start_index: Optional[int] = 1,
    ) -> Dict[str, Any]:
        """
        Retrieve a list of SCIM resources of a specific type.

        Args:
            resource_type (str): The resource type to retrieve. You can retrieve all available
                                types from the Retrieve All SCIM Resource Types endpoint, where
                                the value for this parameter is the endpoint value.
            filter (str, optional): Filter for a specific attribute value.
                                   Must be in the format {attribute} eq "{value}".
                                   For example, to filter for a particular user name, userName eq "john".
                                   Complex expressions are not supported, and eq is the only supported operator.
            attributes (str, optional): Include specified attributes only.
                                      Enter multiple values in a comma separated list.
                                      For example, to include only user name and email in the response,
                                      attributes=userName,emails.
                                      Note that the schemas and id attributes are always returned.
            excluded_attributes (str, optional): Exclude specific attributes from the response.
                                               Enter multiple values in a comma separated list.
                                               For example, to exclude user name and email from the response,
                                               excludedAttributes=userName,emails.
                                               Note that the schemas and id attributes are always returned
                                               and cannot be excluded.
            sort_by (str, optional): Specify an attribute or sub-attribute to order the response.
                                    For example, you can sort by the displayName attribute,
                                    or the name.familyName sub-attribute.
                                    If omitted, the response is sorted by id.
                                    Note that the following attributes are not supported:
                                    securityPolicy, securityProfile, locale, preferredLanguage
            sort_order (str, optional): Specify the order in which the sortBy parameter is applied.
                                       Allowed values are ascending or descending.
                                       If omitted, defaults to ascending.
            count (int, optional): Specify the number of query results per page, for example, 10.
                                  Negative values are treated as 0, and 0 returns no results except for totalResults.
                                  If omitted, defaults to 1000.
            start_index (int, optional): Specify the index of the first result.
                                        For example, 10 would omit the first 9 results and begin on result 10.
                                        Omission, negative values, and 0 is treated as 1.

        Returns:
            dict: The JSON response containing the resources
        """
        url = f"api/{self.client.LatestAPIversion}/scim/v2/{resource_type}"

        params = {}

        if filter:
            params["filter"] = filter
        if attributes:
            params["attributes"] = attributes
        if excluded_attributes:
            params["excludedAttributes"] = excluded_attributes
        if sort_by:
            params["sortBy"] = sort_by
        if sort_order:
            params["sortOrder"] = sort_order
        if count:
            params["count"] = count
        if start_index:
            params["startIndex"] = start_index

        return self.client.api_call(url, params=params)

    def retrieve_single_scim_resource(
        self,
        resource_type: str,
        resource_id: str,
        attributes: Optional[str] = None,
        excluded_attributes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a single SCIM resource.

        Args:
            resource_type (str): The resource type to retrieve. You can retrieve all available
                                types from the Retrieve All SCIM Resource Types endpoint, where
                                the value for this parameter is the endpoint value.
            resource_id (str): The ID of the resource to retrieve. You can retrieve all resource
                              IDs from a particular resource type with the Retrieve SCIM Resources
                              endpoint. For example, business_admin__v.
            attributes (str, optional): Include specified attributes only.
                                      Enter multiple values in a comma separated list.
                                      For example, to include only user name and email in the response,
                                      attributes=userName,emails.
                                      Note that the schemas and id attributes are always returned.
            excluded_attributes (str, optional): Exclude specific attributes from the response.
                                               Enter multiple values in a comma separated list.
                                               For example, to exclude user name and email from the response,
                                               excludedAttributes=userName,emails.
                                               Note that the schemas and id attributes are always returned
                                               and cannot be excluded.

        Returns:
            dict: The JSON response containing the specified resource
        """
        url = (
            f"api/{self.client.LatestAPIversion}/scim/v2/{resource_type}/{resource_id}"
        )

        params = {}

        if attributes:
            params["attributes"] = attributes
        if excluded_attributes:
            params["excludedAttributes"] = excluded_attributes

        return self.client.api_call(url, params=params)
