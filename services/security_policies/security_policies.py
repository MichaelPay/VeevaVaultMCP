import pandas as pd


class SecurityPoliciesService:
    """
    Service class for managing security policies in Veeva Vault

    Security policies allow you to create and manage password policies for users.
    These settings control password requirements, expiration period, reuse policy,
    security question policy, and delegated authentication via Salesforce.com™.
    Security policies apply across all Vaults in a multi-Vault domain.
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance
        """
        self.client = client

    def retrieve_security_policy_metadata(self):
        """
        Retrieves the metadata associated with the security policy object.

        Endpoint: GET /api/{version}/metadata/objects/securitypolicies

        Returns:
            dict: JSON response containing the security policy metadata structure
                  including details about the available properties and objects
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/objects/securitypolicies"

        return self.client.api_call(url)

    def retrieve_all_security_policies(self):
        """
        Retrieves all security policies in the Vault.

        Endpoint: GET /api/{version}/objects/securitypolicies

        Returns:
            dict: JSON response containing all security policies with the following fields:
                - name__v: System-managed value automatically assigned to security policies (typically numeric)
                - label__v: Security policy label displayed in Admin UI
                - value__v: URL value to retrieve security policy metadata
        """
        url = f"api/{self.client.LatestAPIversion}/objects/securitypolicies"

        return self.client.api_call(url)

    def retrieve_security_policy(self, security_policy_name):
        """
        Retrieves a specific security policy by name.

        Endpoint: GET /api/{version}/objects/securitypolicies/{security_policy_name}

        Args:
            security_policy_name (str): Security policy name__v field value (typically numeric)

        Returns:
            dict: JSON response containing the security policy details with fields including:
                - policy_details__v: Policy details including name__v, label__v, and is_active__v
                - policy_security_settings__v: Security settings including authentication_type__v,
                  passwords_require_number__v, passwords_require_uppercase_letter__v,
                  min_password_length__v, password_expiration__v, password_history_reuse__v,
                  and other configuration options based on security policy settings

        Note:
            Boolean fields are only returned when the value is set to true.
        """
        url = f"api/{self.client.LatestAPIversion}/objects/securitypolicies/{security_policy_name}"

        return self.client.api_call(url)

    def get_security_policy_dataframe(self):
        """
        Retrieves all security policies and converts them to a pandas DataFrame for easier analysis.

        Returns:
            pandas.DataFrame: DataFrame containing all security policy information
        """
        response = self.retrieve_all_security_policies()

        if response["responseStatus"] == "SUCCESS":
            policies = response.get("security_policies__v", [])
            if policies:
                return pd.DataFrame(policies)
            else:
                return pd.DataFrame(columns=["name__v", "label__v", "value__v"])
        else:
            raise Exception(f"Failed to retrieve security policies: {response}")
