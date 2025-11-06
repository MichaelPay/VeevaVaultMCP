import json
import requests
from urllib.parse import urlparse
from typing import Dict, Optional, Any, Union


class AuthenticationService:
    """
    Service class for handling authentication with Veeva Vault
    """

    def __init__(self, client):
        """
        Initialize with a VaultClient instance

        Args:
            client: An initialized VaultClient instance
        """
        self.client = client

    def authenticate(
        self,
        vaultURL=None,
        vaultUserName=None,
        vaultPassword=None,
        sessionId=None,
        vaultId=None,
        if_return=False,
        *args,
        **kwargs,
    ) -> Union[Dict[str, Any], None]:
        """
        Main authentication method for Veeva Vault API

        Args:
            vaultURL: URL of the Vault instance
            vaultUserName: User name for authentication
            vaultPassword: Password for authentication
            sessionId: Existing session ID (optional)
            vaultId: Vault ID (optional)
            if_return: Whether to return authentication details

        Returns:
            dict: Authentication details if if_return is True, otherwise None
        """
        # Set defaults if values aren't provided
        self.client.vaultURL = self.client.vaultURL if vaultURL is None else vaultURL
        self.client.vaultUserName = (
            self.client.vaultUserName if vaultUserName is None else vaultUserName
        )
        self.client.vaultPassword = (
            self.client.vaultPassword if vaultPassword is None else vaultPassword
        )
        self.client.sessionId = (
            self.client.sessionId if sessionId is None else sessionId
        )
        self.client.vaultId = self.client.vaultId if vaultId is None else vaultId

        # Parse and normalize URL
        url_parse = urlparse(self.client.vaultURL)
        if len(url_parse.scheme) == 0:
            self.client.vaultURL = "https://" + self.client.vaultURL
            url_parse = urlparse(self.client.vaultURL)

        if len(url_parse.scheme) > 0:
            self.client.vaultDNS = url_parse.netloc

        if (self.client.vaultURL is None) or (len(self.client.vaultURL) == 0):
            raise ValueError(f"No vault URL provided")

        # Authenticate if username and password are provided
        if (
            self.client.vaultUserName
            and self.client.vaultPassword
            and self.client.vaultURL
        ):
            login_result = self.authenticate_with_username_password(
                username=self.client.vaultUserName, password=self.client.vaultPassword
            )

            if login_result.get("responseStatus") == "SUCCESS":
                self.client.sessionId = login_result.get("sessionId")
                self.client.vaultId = login_result.get("vaultId")
                # Update session_id property which some service classes use
                self.client.session_id = login_result.get("sessionId")
            else:
                raise Exception(f"Authentication failed: {login_result}")

        # Validate that we have required parameters after authentication attempt
        if (
            not (self.client.vaultId and self.client.sessionId and self.client.vaultURL)
        ) and (
            not (
                self.client.vaultUserName
                and self.client.vaultPassword
                and self.client.vaultURL
            )
        ):
            raise ValueError(f"Please provide valid authentication parameters")

        # Set API headers for future requests
        self.client.APIheaders = {"Authorization": self.client.sessionId}

        # Get and update API versions
        api_versions = self.retrieve_api_version()

        if if_return:
            return {
                "sessionId": self.client.sessionId,
                "vaultId": self.client.vaultId,
                "vaultURL": self.client.vaultURL,
                "vaultUserName": self.client.vaultUserName,
                "vaultDNS": self.client.vaultDNS,
                "APIheaders": self.client.APIheaders,
                "APIversionList": self.client.APIversionList,
                "LatestAPIversion": self.client.LatestAPIversion,
            }
        return None

    def logout(self) -> Dict[str, Any]:
        """
        Invalidates the current session.

        Documentation URL: https://developer.veevavault.com/api/25.2/#end-session

        Given an active sessionId, inactivate an API session.
        If a user has multiple active sessions, inactivating one session does not
        inactivate all sessions for that user. Each session has its own unique sessionId.

        Returns:
            dict: API response indicating if the logout was successful
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/session"

        headers = {"Accept": "application/json"}

        response = self.client.api_call(url, method="DELETE", headers=headers)

        if response.get("responseStatus") == "SUCCESS":
            # Clear session ID from client
            self.client.sessionId = None
            self.client.session_id = None

        return response

    def get_domain_information(self) -> Dict[str, Any]:
        """
        Retrieves information about the Vault domain

        Returns:
            dict: API response containing domain information
        """
        url = f"api/{self.client.LatestAPIversion}/metadata/vobjects"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, headers=headers)

    def keep_alive(self) -> Dict[str, Any]:
        """
        Keep the current session active by refreshing the session duration.

        Documentation URL: https://developer.veevavault.com/api/25.2/#session-keep-alive

        A Vault session is considered active as long as some activity (either through the UI or API)
        happens within the maximum inactive session duration. This maximum inactive session duration
        varies by Vault and is configured by your Vault Admin. The maximum active session duration
        is 48 hours, which is not configurable.

        Returns:
            dict: API response indicating if the keep-alive was successful
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/keep-alive"

        headers = {"Accept": "application/json"}

        return self.client.api_call(url, method="POST", headers=headers)

    def authenticate_with_username_password(
        self, username: str, password: str, vaultDNS: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Authenticate your account using your Vault user name and password to obtain Vault Session ID.

        Documentation URL: https://developer.veevavault.com/api/25.2/#user-name-and-password

        If the specified user cannot successfully authenticate to the given vaultDNS, the subdomain
        is considered invalid and this request instead generates a session for the user's most
        relevant available Vault.

        Args:
            username: Your Vault user name assigned by your administrator.
            password: Your Vault password associated with your assigned Vault user name.
            vaultDNS: The DNS of the Vault for which you want to generate a session. Optional.

        Returns:
            dict: JSON response containing session ID and related details.
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/auth"

        data = {"username": username, "password": password}

        if vaultDNS:
            data["vaultDNS"] = vaultDNS

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }

        # For authentication we need to make a direct request, can't use client's api_call
        # since it requires an already authenticated session
        response = requests.post(url, data=data, headers=headers).json()

        if response.get("responseStatus") == "SUCCESS":
            self.client.sessionId = response.get("sessionId")
            self.client.session_id = response.get("sessionId")
            self.client.APIheaders = {"Authorization": self.client.sessionId}

        return response

    def authenticate_with_oauth_openid_connect(
        self,
        oath_oidc_profile_id: str,
        access_token: str,
        vaultDNS: Optional[str] = None,
        client_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Authenticate your account using OAuth 2.0 / Open ID Connect token to obtain a Vault Session ID.

        Documentation URL: https://developer.veevavault.com/api/25.2/#oauth-2-0-openid-connect

        When requesting a sessionId, Vault allows the ability for Oauth2/OIDC client applications
        to pass the client_id with the request. Vault uses this client_id when talking with the
        introspection endpoint at the authorization server to validate that the access_token
        presented by the application is valid.

        Args:
            oath_oidc_profile_id: The ID of your OAuth2.0 / Open ID Connect profile.
            access_token: The access token for authorization.
            vaultDNS: The DNS of the Vault for which you want to generate a session. Optional.
            client_id: The ID of the client application at the Authorization server. Optional.

        Returns:
            dict: Response from the API call
        """
        url = f"https://login.veevavault.com/auth/oauth/session/{oath_oidc_profile_id}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        data = {}
        if vaultDNS:
            data["vaultDNS"] = vaultDNS
        if client_id:
            data["client_id"] = client_id

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("responseStatus") == "SUCCESS":
                self.client.sessionId = response_json.get("sessionId")
                self.client.session_id = response_json.get("sessionId")
                self.client.APIheaders = {"Authorization": self.client.sessionId}

        return response.json()

    def retrieve_api_version(self) -> Dict[str, Any]:
        """
        Retrieve all supported versions of the Vault REST API.

        Documentation URL: https://developer.veevavault.com/api/25.2/#retrieve-api-versions

        On success, Vault returns every supported API version. The last version listed
        in the response may be the Beta version, which is subject to change.

        Returns:
            dict: Response from the API call containing the available API versions
        """
        url = f"{self.client.vaultURL}/api/"

        headers = {"Accept": "application/json"}

        if self.client.sessionId:
            headers["Authorization"] = self.client.sessionId

        response = requests.get(url, headers=headers)
        response_json = response.json()

        if response.status_code == 200 and "values" in response_json:
            self.client.APIversionList = []
            for API in response_json["values"].keys():
                self.client.APIversionList.append(float(API.replace("v", "")))
            self.client.APIversionList.sort()
            if self.client.APIversionList:
                self.client.LatestAPIversion = "v" + str(self.client.APIversionList[-1])

        return response_json

    def authentication_type_discovery(
        self, username: str, client_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Discover the authentication type of a user. This API allows applications to dynamically
        adjust the login requirements per user, and support either username/password or
        OAuth2.0 / OpenID Connect authentication schemes.

        Documentation URL: https://developer.veevavault.com/api/25.2/#authentication-type-discovery

        The response specifies the user's authentication type (auth_type):
        - password: The user is configured with a username and password.
        - sso: The user is configured with an SSO Security Policy.

        Args:
            username: The user's Vault user name.
            client_id: Optional. The user's mapped Authorization Server client_id.
                      Applies only to the SSO and OAuth / OpenID Connect Profiles auth_type.

        Returns:
            dict: Response from the API call containing information about the user's
                  authentication type and profiles (if any).
        """
        url = "https://login.veevavault.com/auth/discovery"
        params = {"username": username}

        if client_id:
            params["client_id"] = client_id

        headers = {"Accept": "application/json", "X-VaultAPI-AuthIncludeMsal": "true"}

        response = requests.post(url, headers=headers, params=params)
        return response.json()

    def salesforce_delegated_requests(
        self,
        sfdc_session_token: str,
        my_sfdc_domain: str,
        vault_endpoint: str,
        auth: Optional[str] = None,
        ext_url: Optional[str] = None,
        ext_ns: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Makes a request to the Vault API using Salesforce™ session token, following
        Salesforce™ Delegated Authentication procedure.

        Documentation URL: https://developer.veevavault.com/api/25.2/#salesforce-trade-delegated-requests

        Prerequisites:
        - A valid Vault user with a Security Policy enabled for Salesforce.com™ Delegated Authentication must exist.
        - The trusted 18-character Salesforce.com™ Org ID must be provided.
        - A user with a matching username in Salesforce.com™ Org ID must exist.

        Args:
            sfdc_session_token: Salesforce™ session token.
            my_sfdc_domain: Salesforce™ URL used to validate the session token.
            vault_endpoint: The Vault endpoint to make the request to.
            auth: Optional. Salesforce™ session token, can be used as an alternative to setting in headers.
            ext_url: Optional. Salesforce™ URL for validation, alternative to setting in headers.
            ext_ns: Optional. Set to 'sfdc' to indicate Salesforce™ as the authorization provider, alternative to setting in headers.

        Returns:
            dict: API Response object.
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/{vault_endpoint}"

        headers = {
            "Authorization": sfdc_session_token,
            "X-Auth-Provider": "sfdc",
            "X-Auth-Host": my_sfdc_domain,
        }

        params = {}
        if auth:
            params["auth"] = auth
        if ext_url:
            params["ext_url"] = ext_url
        if ext_ns:
            params["ext_ns"] = ext_ns

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def retrieve_delegations(self) -> Dict[str, Any]:
        """
        Retrieves the vaults where the currently authenticated user has delegate access.

        Documentation URL: https://developer.veevavault.com/api/25.2/#retrieve-delegations

        Vault's delegated access feature provides a secure and audited process for you
        to designate another user to handle Vault responsibilities on your behalf.
        Vault tracks all activities performed by the delegate and logs their activities
        in audit trails that meet compliance standards.

        On SUCCESS, Vault returns the name, Vault ID, DNS, and user ID for any Vaults
        the authenticated user has delegate access to. If the response is empty, the
        authenticated user does not have delegate access to any Vaults.

        Returns:
            dict: A dictionary containing details of the vaults the user has delegate access to, if any.
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/delegation/vaults"

        headers = {"Authorization": self.client.sessionId, "Accept": "application/json"}

        response = requests.get(url, headers=headers)
        return response.json()

    def initiate_delegated_session(
        self, vault_id: str, delegator_userid: str
    ) -> Dict[str, Any]:
        """
        Generate a delegated session ID. This allows you to call Vault API on behalf of
        a user who granted you delegate access.

        Documentation URL: https://developer.veevavault.com/api/25.2/#initiate-delegated-session

        To find which users have granted you delegate access, use the retrieve_delegations() method.

        On SUCCESS, Vault returns a delegated_sessionid. To execute Vault API calls with this
        delegated session, use this delegated_sessionid value as the Authorization header value.

        Args:
            vault_id: The id value of the Vault to initiate the delegated session.
            delegator_userid: The ID of the user who granted the authenticated user delegate access in this Vault.

        Returns:
            dict: Response containing the delegated session ID if successful.
        """
        url = f"{self.client.vaultURL}/api/{self.client.LatestAPIversion}/delegation/login"

        headers = {"Authorization": self.client.sessionId, "Accept": "application/json"}

        data = {"vault_id": vault_id, "delegator_userid": delegator_userid}

        response = requests.post(url, headers=headers, data=data)
        return response.json()
