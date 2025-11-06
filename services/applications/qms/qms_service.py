from typing import Dict, Any, Optional, Union, BinaryIO
import json


class QMSService:
    """
    Service class for interacting with the Veeva Vault QMS application.

    This service provides methods for managing quality teams and quality event records.
    """

    def __init__(self, client):
        """
        Initialize the QMSService with a VaultClient instance.

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def manage_quality_team_assignments(
        self, object_name: str, data: Any
    ) -> Dict[str, Any]:
        """
        Manage Quality Team members on existing records. This endpoint does not support initial
        Quality Team record migrations or the creation of new Quality Teams on existing process records.
        Vault performs updates to Quality Team assignments asynchronously on behalf of the user.
        Learn more about Quality Teams in Vault Help.

        The maximum CSV input file size is 1GB.
        The values in the input must be UTF-8 encoded.
        CSVs must follow the standard RFC 4180 format, with some exceptions.
        The maximum batch size is 500.

        This operation respects the following configurations which impact business logic:
        - Minimum required and maximum users
        - Constraining application roles and user assignment eligibility
        - Object records in locked states
        - New assignments for active users
        - Exclusive role membership restrictions
        - Moving object records to a destination state upon membership completion
        - Task assignment for new and removed users

        Args:
            object_name: The object name__v field value for the team-enabled object.
                        For example, risk_event__v, investigation__qdm, quality_event__qdm.
            data: CSV data containing the team assignment information.

        Returns:
            API response containing job_id
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/quality/qms/teams/vobjects/{object_name}/actions/manageassignments"

        headers = {
            "Content-Type": "text/csv",
            "Accept": "text/csv",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, data=data
        )

    def create_batch_disposition(
        self, batch_id: str, disposition_plan: str
    ) -> Dict[str, Any]:
        """
        Create a Batch Disposition record from an existing Batch and Batch Disposition Plan.
        Learn more about Batch Release in Vault Help.

        To use this API, you must have Veeva Batch Release.

        Args:
            batch_id: The ID of the batch for the disposition, for example, VB6000000001001.
                      You can find this by using Retrieve Object Records or in the URL of the
                      Batch record detail page in the Vault UI.
            disposition_plan: The name of the disposition plan, for example, DP-000001.

        Returns:
            API response containing job_id for the Add Disposition job
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/quality/batch_release/disposition"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        data = {
            "batch_id": batch_id,
            "disposition_plan": disposition_plan
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, json=data
        )
