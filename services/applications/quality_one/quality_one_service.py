from typing import Dict, Any, Optional, Union, BinaryIO
import json


class QualityOneService:
    """
    Service class for interacting with the Veeva Vault QualityOne application.

    This service provides methods for managing teams and team assignments in QualityOne.
    """

    def __init__(self, client):
        """
        Initialize the QualityOneService with a VaultClient instance.

        Args:
            client: An initialized VaultClient instance for API communication
        """
        self.client = client

    def manage_team_assignments(self, object_name: str, data: Any) -> Dict[str, Any]:
        """
        Manage Team assignments by adding users to Team Roles and removing users from Team Roles
        in batches on one or more existing records. Vault performs updates to Team assignments
        asynchronously on behalf of the user. When the job completes, Vault returns the job_id
        and an email notification with a CSV file containing the results of the job. This endpoint
        does not support initial Team record migrations or the creation of new Teams or Team Roles.
        Learn more about QualityOne Teams in Vault Help.

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
                        For example, risk_event__v, investigation__qdm, audit__qdm.
            data: CSV data containing team assignment information including record_id, user_id,
                 operation, and application_role.

        Returns:
            API response containing jobId
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/qualityone/qms/teams/vobjects/{object_name}/actions/manageassignments"

        headers = {
            "Content-Type": "text/csv",
            "Accept": "text/csv",
        }

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, data=data
        )

    def export_haccp_plan_translatable_fields(
        self, haccp_plan_record_id: str
    ) -> Dict[str, Any]:
        """
        Use this endpoint to export translatable fields from a translation copy of a HACCP Plan
        record and its related transactional records.

        Before submitting this request:
        - Generate a translation copy of a HACCP Plan and ensure the copy has an associated
          HACCP Translation Generation record in the Ready for Export lifecycle state.
        - You must have permission to view all translatable fields in the target HACCP Plan.

        When triggered, Vault exports the following field types for translation:
        - Text
        - Long Text
        - Rich Text

        The API returns the job_id. Learn more about translating HACCP Plans in Vault Help.

        You must run Retrieve HACCP Plan Translatable Fields after running this API in order
        to make the exported data available.

        Args:
            haccp_plan_record_id: The ID field value for the HACCP Plan record you wish to translate.

        Returns:
            API response containing job_id
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/qualityone/haccp_plan/{haccp_plan_record_id}/translatable_fields/actions/export"

        headers = {
            "Accept": "application/json",
        }

        return self.client.api_call(endpoint=endpoint, method="POST", headers=headers)

    def retrieve_haccp_plan_translatable_fields(
        self, haccp_plan_record_id: str
    ) -> Dict[str, Any]:
        """
        After running Export Translatable HACCP Plan Fields, use this endpoint to retrieve the
        exported field data.

        Before submitting this request:
        - The target HACCP Plan must have an associated HACCP Translation Generation record in
          the Export Complete lifecycle state.
        - The user who submits this request must be the same user who invoked the Export HACCP
          Plan Translatable Fields API.

        Args:
            haccp_plan_record_id: The ID field value for the HACCP Plan record you wish to translate.

        Returns:
            API response containing all translatable fields and their values from the target
            HACCP Plan and its related records
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/qualityone/haccp_plan/{haccp_plan_record_id}/translatable_fields/file"

        headers = {
            "Accept": "application/json",
        }

        return self.client.api_call(endpoint=endpoint, method="GET", headers=headers)

    def import_haccp_plan_translatable_fields(
        self, haccp_plan_record_id: str, file_data: Union[str, BinaryIO]
    ) -> Dict[str, Any]:
        """
        Use this endpoint to import translated HACCP Plan data into Vault.

        Before submitting this request:
        - You must first run the Export HACCP Plan Translatable Fields and Retrieve HACCP Plan
          Translatable Fields APIs and modify the returned JSON file with the appropriate
          translated data.
        - The target HACCP Plan must have an associated HACCP Translation Generation record in
          the Export Complete lifecycle state.
        - You must have permission to edit all translatable fields in the target HACCP Plan.

        The following guidelines apply to the input file:
        - Translated field data must be in JSON format.
        - The maximum input JSON file size is 250MB.
        - The following field types are supported for import:
          * Text (Metadata return type = String)
          * Long Text (Metadata return type = LongText)
          * Rich Text (Metadata return type = RichText)

        Args:
            haccp_plan_record_id: The ID field value for the HACCP Plan record you wish to translate.
            file_data: The filepath of the JSON document. The maximum allowed file size is 250MB.

        Returns:
            API response containing job_id
        """
        endpoint = f"api/{self.client.LatestAPIversion}/app/qualityone/haccp_plan/{haccp_plan_record_id}/translatable_fields"

        headers = {
            "Content-Type": "multipart/form-data",
            "Accept": "application/json",
        }

        files = {"file": file_data}

        return self.client.api_call(
            endpoint=endpoint, method="POST", headers=headers, files=files
        )
