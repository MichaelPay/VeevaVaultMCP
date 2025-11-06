from typing import Dict, Any, Optional, Union, BinaryIO
import json


class SiteVaultService:
    """
    Service class for interacting with the Veeva Vault SiteVault application.

    This service provides methods for managing eConsent and user administration in SiteVault.
    """

    def __init__(self, client):
        """
        Initialize the SiteVaultService with a VaultClient instance.

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def create_user(self, user_data: list) -> Dict[str, Any]:
        """
        Create a new user in Veeva SiteVault. Bulk creation of users is not supported.
        You must be in the organization context to add study assignments for other sites within the organization.

        Guidelines:
        - A Person record is referencing person__sys.
        - A User record is referencing user__sys.
        - A "user" object (create) or a "username" referencing an existing user (edit) must be specified.
        - Only a single user per API call is supported.
        - APIs build on each other and appear in a nested format.
        - If a site, organization, or study is specified, you must complete all the site, organization,
          or study parameters.
        - You must be in the organization context to add study assignments for other sites within the organization.
        - It is possible to make an existing Person/User active if Vault finds an existing Person/User who
          is currently inactive.
        - A person is made inactive in an organization when all access within that organization has been removed.

        Args:
            user_data: A list containing a dictionary with user creation details:
                - user: Object defining the user being created
                  - email: The user's email
                  - first_name: The user's first name
                  - last_name: The user's last name
                  - security_policy_id: The security policy ID for the user
                  - person_type: The type of person (staff__v or external__v)
                  - language: The user's preferred language
                - person_type: The person type (staff__v or external__v)
                - is_investigator: Boolean indicating if the user is an investigator
                - assignments: Object defining the user's permissions
                  - org_assignment: The organization-level permissions
                  - site_assignments: Array of site-level permissions
                  - Optional study_assignments: Array of study-level permissions

        Returns:
            API response containing the newly created person_id and status information
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/sitevault/useradmin/persons"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=user_data
        )

    def edit_user(self, person_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Edit an existing user in Veeva SiteVault. Bulk editing is not supported.
        You must be in the organization context to add study assignments for other sites within the organization.

        Guidelines:
        - A Person record is referencing person__sys.
        - A User record is referencing user__sys.
        - A "user" object (create) or a "username" referencing an existing user (edit) must be specified.
        - Only a single user per API call is supported.
        - APIs build on each other and appear in a nested format.
        - If a site, organization, or study is specified, you must complete all the site, organization,
          or study parameters. For example, if you edit a user with an existing add-on permission and
          do not include it in your call, the user will no longer have that add-on permission.
        - You must be in the organization context to add study assignments for other sites within the organization.
        - It is possible to make an existing Person/User active if Vault finds an existing Person/User
          who is currently inactive.
        - A person is made inactive in an organization when all access within that organization has been removed.

        Args:
            person_id: The ID of the person__sys to edit.
            user_data: A dictionary with user editing details:
                - Optional username: The username associated with the existing User account
                - is_investigator: Boolean indicating if the user is an investigator
                - assignments: Object defining the user's permissions
                  - org_assignment: The organization-level permissions
                  - site_assignments: Array of site-level permissions
                  - Optional study_assignments: Array of study-level permissions

        Returns:
            API response containing the edited person_id and status information
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/sitevault/useradmin/persons/{person_id}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return self.client.api_call(
            endpoint=endpoint, method="PUT", headers=headers, json=user_data
        )

    def retrieve_documents_and_signatories(self, participant_id: str) -> list:
        """
        Retrieve the valid blank ICFs and signatories for a participant.

        Args:
            participant_id: The Veeva SiteVault ID of the participant. You can use the /query interface
                         to query the Participant (subject__v) object for the participant ID.

        Returns:
            A list containing the valid blank ICFs and signatories for the participant.
            Valid blank ICFs are those that are not already sent or in a workflow.
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/sitevault/econsent/participant/{participant_id}"

        return self.client.api_call(endpoint=endpoint, method="GET")

    def send_documents_to_signatories(
        self,
        documents_version_id: str,
        signatory_id: str,
        signatory_role: str,
        subject_id: str,
    ) -> Dict[str, Any]:
        """
        Send documents to signatories for signature.

        Args:
            documents_version_id: The ID of the blank ICF.
            signatory_id: The ID of the signatory.
            signatory_role: The role of the signatory.
            subject_id: The ID of the participant.

        Returns:
            API response listing the participant, blank ICF, signatories, and job ID.
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/sitevault/econsent/send"

        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "documents.version_id__v": documents_version_id,
            "signatory__v.id": signatory_id,
            "signatory__v.role__v": signatory_role,
            "subject__v.id": subject_id,
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )
